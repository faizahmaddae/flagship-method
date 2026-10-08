# Flutter playbook

How each part of the method is done in Flutter: the identity probe, what to drop, pinning a state
library without letting it touch animation, painting, testing what was painted, and honest native
folders and release builds. Universal rules live in the other references; unless marked otherwise,
every number here came from a shipped project.

**Read when:** the stack is Flutter: at kickoff for the identity probe (§0) and, for a real-time game,
the engine verdict (§15); before Phase 0 scaffolding; when adopting an existing Flutter app (§2, §3);
before the first painter, shader or widget test; before release prep. Other stacks:
`references/stack-other.md`.

> **Dated facts (as of 2026-10 — re-verify before relying):** Flutter 3.47.5 stable, Dart 3.13
> (SDK constraint ^3.13); riverpod / flutter_riverpod 3.4.3; riverpod_lint 3.1.9 as an analyzer
> `plugins:` entry (no dev dependency); flutter_lints ^6.0.0; audioplayers ^6.8.1; in_app_purchase
> 3.3.1 (storekit 0.4.13, android 0.5.3); google_mobile_ads 9.1.0. `kTouchSlop` 18, `kPanSlop` 36
> logical px. Impeller renders on iOS and current Android and keeps no raster cache;
> `ImageFilter.shader` works only on Impeller and not under `flutter test`. The iOS simulator runs
> debug builds only (no profile or release mode). The §0 probe ran exactly as printed; the other
> snippets are excerpts checked against these versions' source: read the installed source
> (`~/.pub-cache/hosted/pub.dev/<pkg>-<ver>/`, `$FLUTTER_ROOT/packages/flutter/lib/src/`) first.

## Contents
0. Identity probe before Phase 0 · 1. Layers, analyzer, dependencies · 2. Drop Material, or keep it
(and migrating off it) · 3. State: pin your library's lifecycle · 4. Painters · 5. Gestures and
motion · 6. Fragment shaders · 7. What Impeller pays for · 8. Fonts, icons and scripts · 9. Tests
that paint · 10. Startup · 11. Services, plugins, channels, sound · 12. Native folders: the setup
script · 13. Release traps · 14. Ads, purchases, analytics and store capture · 15. Game loop and
engine verdict · 16. Traps

## 0. Identity probe before Phase 0: a scratch package

Kickoff renders each candidate direction in the real stack before any app exists
(`references/kickoff.md` §Identity), with no app and no `flutter create`: a throwaway package
(`probe/`, in a scratch folder outside the repo) holding this `pubspec.yaml`, a `fonts/` folder with
the candidate faces (licence checked, §8) and `test/probe_test.dart` below. Run
`flutter pub get --offline` (plain `pub get` if the cache is cold), then `flutter test`; PNGs land in
`out/`. Keep the chosen PNGs and source in `docs/<slug>/reference/identity/`, analyzer-excluded.

```yaml
name: identity_probe
publish_to: none
environment: {sdk: ^3.13.0}
dependencies: {flutter: {sdk: flutter}}
dev_dependencies: {flutter_test: {sdk: flutter}}
```

```dart
// Identity probes rendered headless to PNG. Not shipped.
import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/services.dart'; // FontLoader, ByteData, Uint8List
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';

const Size phone = Size(390, 844); // a reference phone, logical pt
const double dpr = 3;
const String face = 'Probe';
const List<String> faceFiles = <String>['fonts/Probe-Regular.ttf', 'fonts/Probe-Bold.ttf'];
const Color ink = Color(0xFF23324A), paper = Color(0xFFF3EEE4);
typedef Draw = void Function(Canvas c, Size s);

// `flutter test` ignores pubspec fonts and draws every glyph as a box: register the files by hand.
Future<void> loadFonts() async {
  final FontLoader loader = FontLoader(face);
  for (final String f in faceFiles) {
    loader.addFont(Future<ByteData>.value(ByteData.sublistView(File(f).readAsBytesSync())));
  }
  await loader.load();
}

// toImage/toByteData finish on the raster thread, which fake time never reaches: use runAsync.
Future<Uint8List> pixels(WidgetTester t, Size size, Draw draw, ui.ImageByteFormat format) async {
  final ui.PictureRecorder rec = ui.PictureRecorder();
  draw(Canvas(rec)..scale(dpr), size);
  final ui.Picture pic = rec.endRecording();
  return (await t.runAsync(() async {
    final ui.Image img = await pic.toImage((size.width * dpr).round(), (size.height * dpr).round());
    final ByteData d = (await img.toByteData(format: format))!;
    img.dispose();
    pic.dispose();
    return d.buffer.asUint8List(d.offsetInBytes, d.lengthInBytes);
  }))!;
}

Future<void> savePng(WidgetTester t, String name, Size size, Draw draw) async =>
    (File('out/$name.png')..parent.createSync(recursive: true))
        .writeAsBytesSync(await pixels(t, size, draw, ui.ImageByteFormat.png));

void label(Canvas c, String text, Offset at, double size, {FontWeight w = FontWeight.w400}) {
  final TextPainter tp = TextPainter(textDirection: TextDirection.ltr, text: TextSpan(text: text,
      style: TextStyle(fontFamily: face, fontSize: size, fontWeight: w, color: ink)))..layout();
  tp.paint(c, at);
  tp.dispose();
}

// One record per candidate direction; every direction draws the SAME data. Replace the bodies.
final List<({String name, Draw hero, Draw screen, Draw payoff})> directions = [
  (
    name: 'a_flat_ink',
    hero: (Canvas c, Size s) =>
        c.drawCircle(s.center(Offset.zero), s.width * 0.4, Paint()..color = ink),
    screen: (Canvas c, Size s) {
      c.drawRect(Offset.zero & s, Paint()..color = paper);
      label(c, 'Today', const Offset(24, 80), 30, w: FontWeight.w700);
    },
    payoff: (Canvas c, Size s) {
      c.drawRect(Offset.zero & s, Paint()..color = paper);
      for (int i = 0; i < 7; i++) {
        c.drawCircle(Offset(40.0 + i * 50, 300), 18, Paint()..color = ink);
      }
    },
  ),
];

void main() {
  setUpAll(loadFonts);
  testWidgets('the face loaded: two glyphs paint differently', (WidgetTester t) async {
    Future<Uint8List> glyph(String g) => pixels(t, const Size(40, 40),
        (Canvas c, Size s) => label(c, g, Offset.zero, 32), ui.ImageByteFormat.rawStraightRgba);
    expect(await glyph('a'), isNot(equals(await glyph('b'))), reason: 'identical = fallback boxes');
  });
  for (final d in directions) {
    testWidgets('probe ${d.name}', (WidgetTester t) async {
      await savePng(t, '${d.name}_hero_48pt', const Size(48, 48), d.hero);
      await savePng(t, '${d.name}_screen', phone, d.screen);
      await savePng(t, '${d.name}_payoff', phone, d.payoff);
    });
  }
}
```

- Render at least the hero at its smallest real size (48 pt here), a full screen and the payoff; add
  the empty state and each lighting the identity plans. A widget-tree probe (real layout, right to
  left, 2× text) pumps `Directionality` around a `RepaintBoundary` and captures it as §9.3 does.
- **The tofu test is the font proof:** without `setUpAll(loadFonts)` it fails. For a non-Latin
  script, compare two letters of that script.
- Look at every PNG (`scripts/contact_sheet.py`; the look loop: `references/visual-design.md`). The
  probe proves the stack can draw the direction; feel waits for Phase 2. **If speed is the identity**
  (optional, Proposed): draw the hero and one hazard at top speed from a `Draw Function(double t)`,
  save 8 frames 1/60 s apart, and view them with `--filmstrip`: trails and silhouettes must read.

## 1. Layers, analyzer, dependencies

Map the layer contract (`references/architecture.md`) onto `lib/`. Example (shipped puzzle game):

| Directory | Holds | May import |
|---|---|---|
| `core/` | rules, models, policies, ports, event derivation | `dart:` core/math/typed_data/convert/collection/async; `meta` |
| `state/` | providers, notifiers, clock providers | core, `package:riverpod/*` |
| `services/` | port implementations; the only home of plugins | core, one plugin per file |
| `theme/` | tokens, motion numbers, palettes | `dart:ui`, painting |
| `render/` | painters; wrappers of engine types | core, theme, `dart:ui`, painting/rendering/foundation |
| `motion/` | choreography, pure timelines, springs | core, theme, render, animation/physics/scheduler |
| `widgets/`, `screens/` | widgets | all of the above except services and `dart:ui` |
| `main.dart`, `app.dart` | composition root | everything not banned; nothing imports them |

- The guard reads directives with a lexer and parses this table from `docs/<slug>/ARCHITECTURE.md`
  (`references/verification.md`). `export` counts as an import, every URI of a conditional import
  counts, and a `part` file in another layer smuggles that layer's imports.
- `widgets.dart` re-exports animation, painting and part of foundation (not `ValueListenable`): allow
  umbrella libraries on purpose. Import `dart:ui` as `ui`: unprefixed beside painting, `Gradient`
  silently means painting's class. Wrapping engine types (`ui.FragmentProgram`, `ui.Picture`,
  `ui.Image`) in render-layer classes is what lets widgets ban `dart:ui`.

```yaml
# analysis_options.yaml: no deprecation is ignorable when you own every widget
include: package:flutter_lints/flutter.yaml
plugins: {riverpod_lint: 3.1.9}
analyzer:
  language: {strict-casts: true, strict-raw-types: true}
  errors: {deprecated_member_use: error}
  exclude: [build/**, android/**, ios/**, tool/preview/out/**]
linter: {rules: [prefer_final_locals, prefer_const_constructors, avoid_print, always_declare_return_types]}
```

Use explicit types (collection literals too), sealed classes for results and events, and
`abstract final class Tokens { static const … }` namespaces. Every dependency carries its reason:
`# <Purpose> (DECISIONS #n). <ver>, checked <date>: <suite passes here; no Material in its lib/;
privacy manifest; min OS>. Only lib/services/<f>.dart imports it.`

**The toolchain writes to tracked files:** `flutter pub get` (which `flutter test` and `flutter run`
also run) rewrites `analysis_options.yaml` and writes generated files under `ios/` and `android/`.
Commit the excludes deliberately, gitignore the generated paths and keep `git status --short` clean
in the baseline; a retrofit settles this before its first commit (`references/planning-and-slices.md`
§Retrofit: one adoption commit swept the yaml and 8 generated files in with `git add -A`).

> **Dated facts (as of 2026-10 — re-verify before relying):** on Flutter 3.47.5 both `flutter pub get`
> and `flutter test` inserted `analyzer: exclude: [build/**]` (plus platform folders when present).

## 2. Drop Material, or keep it

**Drop it** (`WidgetsApp`, own controls, no `material.dart` or `cupertino.dart` in `lib/`) when the
product draws its own look: games, and branded apps whose controls are all custom. Material then adds
a look to fight, an icon font you never use, and deprecations you do not control. **Keep it** (or
Cupertino) for forms-heavy apps: `TextField`, selection toolbars, pickers and platform dialogs are
expensive to rebuild well and screen-reader users expect them. Middle path: ban it everywhere except
one `forms/` row of the layer table.
- `WidgetsApp` needs `color` (the app-switcher colour) and a `pageRouteBuilder` returning the house
  route; `textStyle` sets the app-wide `DefaultTextStyle`, and `builder` wraps every route in the
  quality and motion scopes.
- Leave `uses-material-design` out of `pubspec.yaml` (it bundles the icon font). The guard bans both
  libraries with a lexer and reads pubspec keys with comments stripped (a regex guard was wrong both
  ways: a doc comment tripped it, a pubspec comment satisfied it). Unused Material inside a plugin's
  own `lib/` is acceptable.
- Icons are painters (§8). Test harnesses use the app's own root: a `MaterialApp` harness throws for
  locales a non-Material app lacks, and tests a tree that never ships.
- The house route reads the motion switch at creation **and at pop**: the framework fixes durations
  when the controller is made, so motion turned off in Settings would still animate its own Back.

### Migrating an existing app off Material (strangler)

Adoption order: `references/planning-and-slices.md` §Retrofit; the guard's ratchet:
`references/architecture.md` §2.5.
1. **Pin today's behaviour first:** characterization tests through the real root on every flow you
   will touch (known bugs named as such), and as-found renders of every screen.
2. **No new imports:** today's importers are legacy rows with an expiry; a new importer fails.
3. **One screen per slice,** the vertical slice first: rebuild it on widgets-layer pieces, delete its
   legacy row, and show before and after looks across the matrix.
4. **Mixed trees while moving:** `TextField`, `InkWell` and `ListTile` assert a `Material` ancestor
   in debug, and `TextField` also `MaterialLocalizations`. Keep the `MaterialApp` root until the last
   Material screen has moved, or swap it early and give the rest a `Material` wrapper plus
   `DefaultMaterialLocalizations.delegate`; record which in DECISIONS. Harnesses follow the real root.
5. **Remove `uses-material-design` last,** after the last `Icons.*` has become a painter.

## 3. State: pin your library's lifecycle

Whatever library holds state, **pin each lifecycle behaviour with a small passing reference test
before product code** (`references/kickoff.md` §5.3), kept in the suite so an upgrade that changes
one fails loudly: what counts as a change and whether a no-op notifies; whether failed loads retry;
when dispose hooks run and what is readable there; what keeps a value alive; whether listeners fire
synchronously; what happens behind a covered screen; whether a second test pump reuses a container.

One pinned example: **Riverpod 3.4.3**, hand-written providers, no code generation, the lint plugin
on, so every provider reads plainly in a diff and no build step can be forgotten. Never mark a
notifier `final class` if a test must fake it. The three rules (`references/architecture.md`
§3.1–§3.3) in Riverpod terms:
1. **Immutable values with `==`:** store `List.unmodifiable`; a no-op returns the *identical*
   instance (tests assert `identical`). Because `state =` is filtered by `==` (dated block below), a
   list mutated in place and reassigned never notifies.
2. **Per-frame values never go through providers:** they are `ValueNotifier`s owned by the drawing
   widget, handed to painters as `repaint:` (§4). Values that change *inside* a frame (route on top,
   panel settled) are plain `ChangeNotifier`s held by a provider and written post-frame. Incident: a
   gate held as provider state and changed mid-frame made Riverpod rebuild its `ProviderScope` in
   debug; the frame-budget test (§9.6) caught it.
3. **Commit synchronously, then emit** events derived by a pure (before, after) function.

```dart
class BoardNotifier extends Notifier<Session> {
  BoardNotifier(this.key);
  final BoardKey key;
  final StreamController<BoardEvent> _events = StreamController<BoardEvent>.broadcast();
  late final Stream<BoardEvent> events = _events.stream;       // one stream for the notifier's life
  @override
  Session build() {
    final Ref built = ref;
    built.onDispose(() { if (!built.mounted) unawaited(_events.close()); });   // final dispose only
    return Session.start(ref.watch(puzzleProvider(key)));
  }
  void extend(Cell cell) {
    final Session before = state, after = before.extend(cell);   // pure core
    if (identical(after, before)) return;                         // no-op: nothing notifies
    state = after;                                                // commit first, then emit
    BoardEvents.of(before, after).forEach(_events.add);
  }
}
final NotifierProviderFamily<BoardNotifier, Session, BoardKey> boardProvider =
    NotifierProvider.autoDispose.family<BoardNotifier, Session, BoardKey>(BoardNotifier.new);
```

**Wiring.** Family keys are value-equal sealed classes (`Board(3)` read twice is one session;
`autoDispose` starts the next visit fresh). Root: `ProviderScope(retry: (_, _) => null, …)`; tests:
`ProviderContainer.test(retry: (_, _) => null, overrides: <Override>[…])`; with retry on, a save that
fails to load retries for seconds instead of falling back. One provider per port: must-wire ports
throw naming themselves (`Provider<Haptics>((Ref ref) => _unwired('hapticsProvider'))`: "is not
wired: main.dart (or the test) must override it"); safe-absent ports default to a recording null
object (`references/architecture.md` §1.3). App-lifetime services: `ref.listenManual(p, (_, _) {})`
in the root `initState`. Narrow rebuilds with `select`. Type the root builder as `ProviderScope`
(`missing_provider_scope` reads `runApp`'s static argument type). Test rig: a retry-off container,
a hand-driven `FakeClock`, a store that keeps `jsonDecode(jsonEncode(doc))` so later mutation cannot
hide, an event probe, and a `settle()` that flushes microtasks and broadcast deliveries.

> **Dated facts (riverpod 3.4.3, as of 2026-10 — re-verify before relying; each bit a real build and
> was then pinned by a reference test):**
> - `state =` is filtered by `==`. Default retry: Exceptions (not Errors) up to 10 times, 200 ms
>   doubling to 6.4 s. `ref.listen` fires synchronously from `state =`: a widget that causes and
>   hears a change flags its own calls (`_own = true; n.extend(c); _own = false;`).
> - A `Notifier` survives provider rebuilds, but **every `onDispose` runs on every rebuild**: a stream
>   closed there died while the notifier lived on. Close only when `!ref.mounted`; emit
>   `SessionStarted` on rebuild. `state` and `ref` are unreadable in the final `onDispose`: keep the
>   latest via `listenSelf`, read ports into fields once per build.
> - Only `ref.watch` or `container.listen` keeps an `autoDispose` provider alive, never a stream
>   subscription; a cancelled subscription never gets `onDone`.
> - A covered route's providers pause, so a change made while covered lands just after Back and a
>   fade plays late: track "covered at the last build or uncovered within two frames" and cut.
>   Changing a provider in `State.dispose` throws, as during build: capture objects in `initState`.
> - A screen depending on its own route rebuilds wholesale whenever any route comes or goes,
>   restarting child timers (a rating prompt never fired): a **leaf probe** widget reports "on top"
>   post-frame into a plain object. A second `pumpWidget` of the root keeps the first container, so
>   new overrides are ignored and a negative control "passes": pump `const SizedBox()` between.

### An existing state library (retrofit)

Keep it if its state can be made immutable and its lifecycle pinned by reference tests; replace it
when the core is being rewritten anyway or a pinned behaviour cannot be worked around.
1. **Pin current behaviour first,** as in §2 (the flows and the saves they write). *Example (a
   retrofitted word game):* an in-place `List.add` that never notified, the `==` trap above.
2. **Strangle, never fork:** new and touched screens use the target library, one screen per slice.
   Two libraries never own one value; a legacy notifier feeds new code through one adapter provider
   that exposes an immutable snapshot.
3. **Mutable globals** become ports or providers one by one, each a legacy row with an expiry
   (`references/architecture.md` §2.5). Record keep-or-replace in DECISIONS with the pinned facts.

## 4. Painters

The project's own look lives in `references/visual-design.md` and its DESIGN doc; the cost rules in
`references/performance.md` §3–§5. The Flutter mechanics:

```dart
class RibbonPainter extends CustomPainter {
  RibbonPainter({required this.frame, required this.palette}) : super(repaint: frame);
  final ValueListenable<RibbonFrame> frame;     // per-frame value: read in paint, never via rebuild
  final Palette palette;
  @override void paint(Canvas canvas, Size size) => _draw(canvas, size, frame.value, palette);
  @override bool shouldRepaint(RibbonPainter old) => old.palette != palette || old.frame != frame;  // config only
}   // the notifier publishes only when the value changed (value-equal frame classes)
```

- **One `RepaintBoundary` + `CustomPaint` per layer on its own schedule**, siblings in one `Stack` in
  the order of the layer table. Mark recorded-`Picture` layers `isComplex: true`; re-record only when
  content, geometry, palette or quality changes, and dispose old pictures. **A ticking backdrop is a
  sibling of content, never `CustomPaint(child: app)`.**
- **`LayoutBuilder` repaints its layer on every rebuild below it.** Fence it
  (`RepaintBoundary(child: SizedBox.expand(child: LayoutBuilder(…)))`); a boundary *below* cannot.
- **`CustomPaint` does not clip.** Each painter declares its overflow and lays its face out inside
  `box.deflate(overflow)`. Blur bound: 3σ + 1 px anti-aliasing, rounded up, plus any lip or shadow
  shift on that side. Characters get a rest box for layout and a full box for any pose (§9.2).
- **Draw in unit space**, origin at the ground point, scaled at paint; build fixed paths once
  (`final Path _head = () {…}();`). Hairlines `max(unitWidth, 0.8 / pixelsPerUnit)`; bands sized in
  height units double on a large hero, so cap them at a reference size.
- Overlapping translucent pieces: draw opaque with `BlendMode.src` into a bounded `saveLayer` and
  composite once. Gradients with three or more colours need explicit stops (they threw on the first
  device frame). Themes are values, never branches; no `Random()` at paint
  (`references/architecture.md` §1.6, §9).
- Debug hooks are `@visibleForTesting static` callbacks or counters costing one null check, never
  test-only logic. Each painter file opens with a library doc: rules with their incident, **Motion
  off**, **Quality low**, **Bounds**, **Cost**, and the tests that pin it.

## 5. Gestures and motion

- **A raw `Listener` for anything the finger draws.** `GestureDetector`'s pan waits for `kPanSlop`,
  so the first cell feels dead. Track one pointer id. `onPointerCancel` **discards** (the system took
  the gesture); committed cells stay. If the model changes under a held finger for another reason
  (Undo by a second finger), end the drag. Thresholds: `references/motion-and-feel.md`.
- Decorative overlays are `IgnorePointer` **and** `ExcludeSemantics`: `IgnorePointer` keeps labels, so
  a `button: true` under it is announced as a dead button. Direct manipulation that commits on
  pointer-down still needs a semantic tap path: each cell a `Semantics(button: true, onTap: …)` node.
- **One motion flag.** Fold the in-app motion setting and the OS setting into `disableAnimations` on
  one root `MediaQuery`, read it with `MediaQuery.maybeDisableAnimationsOf(context)`, and keep the
  widget tree's shape the same either way. Prove presentation "off" with
  `SchedulerBinding.instance.transientCallbackCount == 0` after the action, not `hasScheduledFrame`;
  a running simulation's ticker is the task and keeps going (§15, `references/motion-and-feel.md` §10).
- **Springs from design numbers:** `SpringDescription.withDurationAndBounce(duration: …, bounce: …)`;
  bounce 0 is critically damped. **Curves are objects, not formulas:** `Curves.easeOutCubic` is
  `Cubic(0.215, 0.61, 0.355, 1.0)`, not `1 − (1 − u)³` (0.978 vs 0.986 at u = 0.76): sample the
  curve object, or a timeline lands its beats early.

## 6. Fragment shaders

The shader rules are GPU rules and live in `references/performance.md` §7. The Flutter mechanics:
- **A canvas `FragmentShader` painted by a `CustomPainter`, never `ImageFilter.shader`** (Impeller-only
  and unsupported under `flutter test`: top dated block). List the files under `flutter: shaders:` in
  `pubspec.yaml`; load with `ui.FragmentProgram.fromAsset` once per asset (`_loading[asset] ??= …`,
  `null` from the `catch`), and test the fallback through an explicit failed load (the engine caches
  programs per key). **Preload in `main()` under one 2 s cap, through an `async` body** (§10); a slow
  program is adopted when it lands.
- Wrap `FragmentProgram`/`FragmentShader` in render-layer classes; the widget owns and disposes its
  shader instance. Its `Ticker` drives a `ValueNotifier<double>` (the painter's `repaint`) only while
  animate, ambient, motion on, quality high and shader loaded all hold.
- Shader files `#include <flutter/runtime_effect.glsl>`, read the pixel with `FlutterFragCoord().xy`,
  write `out vec4 fragColor`, and declare uniforms in the one documented order (`uSize` at 0–1,
  `uTime` at 2, …) that the painter fills with `setFloat(i, …)` before
  `canvas.drawRect(Offset.zero & size, Paint()..shader = s)`. Adding a uniform changes every shader,
  the Dart writer and the count test in one step. A helper called before its definition fails the
  shader build, which leaves its log in the project root.

## 7. What Impeller pays for

The cost model, draw budgets and the dated Impeller facts are in `references/performance.md` §1 and
§5–§6. The Flutter API side:
- Bake with `RenderRepaintBoundary.toImageSync` (it asserts the boundary is painted: snapshot in a
  post-frame callback); a cache hands out `ui.Image.clone()`s that holders `dispose()`.
- Frame monitor: `SchedulerBinding.instance.addTimingsCallback`; slow = `buildDuration` **or**
  `rasterDuration` > 16.67 ms. Never in debug builds (slow by design; the iOS simulator runs only
  those, so every screenshot would show the low look). An `APP_FRAME_LOG` define prints
  p50/p90/p99/max every 5 s from a profile or release build on a phone.
- Pin draw counts with a counting canvas (§9.7).

## 8. Fonts, icons and scripts

- **Bundle fonts; never fetch.** Cut a static file per used weight from the upstream variable font
  (`fonttools varLib.instancer`; pin each upstream sha256; ship the OFL licence and attribution):
  static files draw a weight identically on Impeller, Skia and under `flutter test`.
- **`flutter test` does not load pubspec fonts.** Load them in every test that rasterises or measures
  text, as §0's `loadFonts` does, from a family → files map kept exactly as the pubspec lists it. Tofu
  and weight tests: `references/visual-design.md` (the runner does not fake bold; check each file's
  OS/2 `usWeightClass`). **Icons are painters,** not glyphs.
- **Direction.** Lay out with `EdgeInsetsDirectional`, `AlignmentDirectional`, `PositionedDirectional`
  and `start`/`end`, so a right-to-left locale mirrors for free. A `CustomPainter` never mirrors by
  itself: read `Directionality.of(context)` where a drawing must flip, and wrap what must never flip
  (a game board, a media scrubber, a chart's time axis) in `Directionality(textDirection:
  TextDirection.ltr)`.
- **Mixed runs and other scripts** (rules and incidents: `references/ux-and-accessibility.md`
  §Localisation): isolate a signed figure (`'\u2068$figure\u2069'`) or give it its own
  `textDirection`; assert placement with `TextPainter.getBoxesForSelection`; route letter-spacing
  through one function that returns 0 for joined scripts. The language test pumps each screen in the
  right-to-left language and fails on any Latin letter in the `text.toPlainText()` of
  `tester.widgetList<RichText>(find.byType(RichText))`.

## 9. Tests that paint

Every painter has a test that rasterises it, and someone looks at a preview of every screen. Doctrine
and pixel recipes (relationships sampled at design proportions, hashes before additive changes,
device-capture thresholds, "compare without the feature"): `references/verification.md` §6.

### 9.1 Raster helpers

`toImage`/`toByteData` complete on the raster thread, which the fake clock never reaches: awaited
directly, the test hangs until killed. Run both under `tester.runAsync`, as §0's `pixels` does, and
read `rawStraightRgba`: the default raw readback is premultiplied. Pixel tests usually draw at 1×. Use
shipped data as the fixture and assert its assumption first.

### 9.2 The bounds ring

Paint on a canvas `ring` (e.g. 24) larger on every side, translated by the ring, and list every pixel
with alpha outside `overflow.inflateRect(Offset(ring, ring) & box)`; expect the list empty. Run it over
every state and pose, sampling motion densely (a thrown thing wholly outside touches no edge at its
peak), and assert the bound is tight. A self-clipping painter defeats this (it just shrinks): test
its outer pixel ring instead.

### 9.3 Preview tests: render to PNG and look

Tests under `test/preview/` render screens, characters and icons into a gitignored
`tool/preview/out/<topic>/` (`before_*`, `v1_*`, …). They assert only that rendering worked; whether
it looks right is a question for someone with the PNG open. §0's helpers move into `test/support/`.

```dart
await loadAppFonts(); addTearDown(t.view.reset);
for (final Size phone in const <Size>[Size(390, 844), Size(360, 780)]) {
  t.view..physicalSize = phone * 3..devicePixelRatio = 3;      // the default test view is 800×600
  await t.pumpWidget(const SizedBox());                        // drop the previous scope
  await t.pumpWidget(RepaintBoundary(key: shot, child: appRoot(fakes())));
  await t.pump(const Duration(milliseconds: 700));             // never pumpAndSettle with ambient on
  final ui.Image img = (await t.runAsync(() =>
      (t.renderObject(find.byKey(shot)) as RenderRepaintBoundary).toImage(pixelRatio: 2)))!;
  await savePng(t, img, 'home/v1_${phone.width.toInt()}');
}
```

Render the look matrix (`references/visual-design.md` §13.1); sequences become filmstrips of fixed
steps (a 1 Hz simulator screenshot cannot see a 300 ms beat). Byte pins: `references/traps.md` T-31.

### 9.4 Text-scale matrix

Every screen × 2 reference phones × text scale {1, ~1.3, 2}, through the real root (which text
scales how: `references/ux-and-accessibility.md` §13). Declare screens as records `({String name,
Fakes Function() fakes, Widget home, … then, … reading})` so a new screen joins every audit in one
line. Per case set `t.platformDispatcher.textScaleFactorTestValue = scale` (cleared in a tear-down),
then expect no exception, no text problem (`didExceedMaxLines`, a min intrinsic height above its
box, a word wider than its box, text off screen) and a clean §9.5 audit.
- Reading text must follow the scale **and be drawn at it**: `textScaler.scale(100) / 100 == scale`
  *and* `getTransformTo(null)` vertical scale 1 ± 0.01. A `FittedBox(scaleDown)` leaves the scaler
  alone and shrinks the glyphs; a value drew at 0.52 unnoticed until the transform check existed.
- `softWrap: false` with a fade overflow fails silently: compare min intrinsic width to the box.
  Assert buttons are whole on their card ("nothing clipped" passed a button scrolled out of view).

### 9.5 Accessibility audit that hit-tests

The semantics tree alone passed a control wrapped in `ExcludeSemantics` and a `Semantics` wrapper
larger than its gesture detector. Audit both trees:
- Every tappable node: a label, an announced role, ≥ 44×44 pt (skip nodes cut by the screen or a
  scrolling viewport, as the framework's guideline does). Each screen has a heading; traversal order
  equals an expected list.
- **Every tap handler has a node:** each `RenderSemanticsGestureHandler` with `onTap` and each
  `RenderPointerListener` taking a lift that `tester.hitTestOnBinding(center)` reaches sits under a
  tappable node (skip tap-anywhere layers ≥ 90% × 75% of the screen). **The touch is as big as the
  node:** points 1 pt inside each edge of its central 44×44 hit a handler holding the node's centre.
- Merge traps: `Semantics(container: true, sortKey: …)` without `explicitChildNodes: true` merges its
  children; a list item is its own boundary (keys go inside it); siblings sort by position, so a
  scroll view's items precede a top bar painted over them (`OrdinalSortKey`).

### 9.6 Frame-budget tests

A frame costs what it repaints and rebuilds, which a final-screen assertion cannot see. A
`FrameLog` sets `debugOnProfilePaint` and `debugOnRebuildDirtyWidget` to append each painted
`RenderObject` and each rebuilt `Element`'s widget to the current frame's lists (`next()` opens a
frame), and unsets both in the test body (a tear-down is too late). What to assert per moment, and
what it caught: `references/performance.md` §2. Filter painters with
`o is RenderCustomPaint && o.painter is MyPainter`; compare rebuilt `widget.runtimeType`s to an exact
set. `FadeTransition`/`RenderOpacity` above 0 is itself a repaint boundary, so a control removing
only your `RepaintBoundary` "passes".

### 9.7 Playthroughs by gesture, and draw counts

- Play every shipped item through the real root by gesture (`t.startGesture(first)`, then
  `g.moveTo(p)` with a 16 ms `pump` per sample, then `g.up()`), motion on and off, rotating finger
  styles (`references/verification.md` §7); compare the save on disk to memory. Tag it `slow` and keep
  it in the plain run (`references/traps.md` T-35).
- Draw counts without rasterising: a `CountingCanvas implements Canvas` whose `noSuchMethod` counts
  `memberName`s and blurred paints and returns null. Members with a non-nullable return
  (`getTransform`, `getSaveCount`) then throw unless overridden
  (`Float64List getTransform() => Matrix4.identity().storage;`), so a painter recorded through it
  undoes its own transforms arithmetically, never reading them back.

## 10. Startup: nothing before `runApp` throws or waits unbounded

The rule: `references/architecture.md` §8 (incident: `references/traps.md` T-36). In Dart, **never
call `.timeout` with a void `onTimeout` on a future whose run-time type you do not control:**
`=> Future.wait(…)` is a `Future<List<…>>` (its `onTimeout: () {}` threw a covariance `TypeError`),
and `(…) async => throw e` is a `Future<Never>` whatever its declared type. Await it inside your own
function with a declared type (`Future<void> all() async { await …; }`) and time out that.

```dart
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final Analytics analytics = startAnalytics();        // never awaited; events queue until attached
  ambientMotionEnabled = true;                         // tests never call main(): ambient stays off there
  await SystemChrome.setPreferredOrientations(<DeviceOrientation>[DeviceOrientation.portraitUp])
      .timeout(const Duration(seconds: 1), onTimeout: () {});
  final Future<List<Override>> services = openServices(analytics);   // 3 s bounds, memory fallback
  await preloadShaders(assets);
  ParticleAtlas.warm();                                // baked now, not mid-gesture on the first burst
  runApp(appRoot(overrides: await services));
}
Future<void> preloadShaders(Iterable<String> assets) {
  Future<void> all() async { await Future.wait(assets.map(Programs.load)); }   // a REAL Future<void>
  return all().timeout(const Duration(seconds: 2), onTimeout: () {});
}
```

The ambient-motion switch is off unless `main()` sets it, so `pumpAndSettle` terminates; tests
covering ambient turn it on and restore the previous value. **Cold-launch `main()` on a simulator or
device after every integration.**

## 11. Services, plugins, platform channels, sound

The port rules (one SDK per file, lazy `start()`, bounded awaits, backend seams) are in
`references/architecture.md` §1 and §7. Flutter specifics:
- Reading the IAP singleton on Android connected to the store at once, and a handler-less channel
  then failed a finished test: read it in `start()`. A Dart timeout does not cancel the platform
  message. A strict SDK fake (`references/traps.md` T-42) is `implements <SdkClass>` with a
  `noSuchMethod` that fails.
- **Platform channels live in one in-repo plugin** (`packages/<app>_<feature>/`, ~140 lines of Swift
  in one game): one thin Dart class, namespaced channel names, methods that may throw
  (`MissingPluginException` off-platform); the service bounds and catches every call.
- **Haptics** return at once (detach the future, swallow errors, no timer per click); selection clicks
  are rate-gated by skipping (≥ 35 ms).
- **Lifecycle** via `AppLifecycleListener`: `resumed` is back; `hidden`/`paused`/`detached` are away
  (flush, stop clocks, settle shows silently, end the analytics attempt); `inactive` (a system sheet)
  is neither. Grant day-based things on resume too: iOS may keep an app suspended for days.
- **Large assets:** `AssetBundle.load` bytes, then decode and parse in one `compute` (why:
  `references/performance.md` §9 dated block).
- **Sound** (policy: `references/motion-and-feel.md` §17): one player pool per file, source set once,
  replay by `stop()` + `resume()` (re-setting the source re-prepares it); set the global audio context
  **before the first player exists**; build real players inside `runAsync` in tests (built in the
  fake zone they hang).

> **Dated facts (audioplayers ^6.8.1 and platform audio, as of 2026-10 — re-verify before relying):**
> Android copies the audio context at player creation, so a context set later never applies. On iOS
> `playbackRate` keeps pitch (pitch variants became separate files) and loops by seek(0) + resume,
> which is not gapless. `HapticFeedback.successNotification` is silent below Android API 30: accept
> it rather than design a second pattern.

## 12. Native folders: the setup script

**Never run a bare `flutter create .` in an existing repo:** it overwrites `main.dart`,
`pubspec.yaml`, `analysis_options.yaml`, `README.md`, `.gitignore` and `.metadata`, which encode
decisions. One script regenerates the gitignored `android/` and `ios/` (method:
`references/architecture.md` §11; its edits: `references/release-and-store.md` §1.1). The Flutter
shape, a sketch (verify the generated file names against your Flutter version):

```bash
set -euo pipefail; cd "$(dirname "$0")"     # header: WHY (the incidents); NEVER a bare `flutter create .`
HAND=(pubspec.yaml analysis_options.yaml README.md .gitignore CLAUDE.md lib/main.dart)
validate_inputs; before=$(shasum "${HAND[@]}")   # ALL inputs checked before anything is deleted
tmp=$(mktemp -d); flutter create --org "$ORG" --project-name "$NAME" --platforms android,ios "$tmp/app" >/dev/null
rm -rf android ios; cp -R "$tmp/app/android" "$tmp/app/ios" .
rm -f ios/Flutter/Generated.xcconfig ios/Flutter/flutter_export_environment.sh   # the scaffold path leaks here
flutter pub get >/dev/null; patch_label; check_label || exit 1   # each edit, then its check; at the end, ALL again
[[ "$before" == "$(shasum "${HAND[@]}")" ]] || { echo "!! a hand-written file changed" >&2; exit 1; }
if grep -rq "$tmp" android ios; then echo "!! temp path leaked" >&2; exit 1; fi
```

- The scaffolder fills the development team from the keychain, so the team patch's negative control
  needs a *different* team id.
- Gradle reads `android/key.properties`, which a regeneration deletes (the next release silently
  debug-signed): keep it outside the generated folder and copy it in; the verifier checks the cert.

> **Dated facts (as of 2026-10 — re-verify before relying):** `flutter build ios --config-only` also
> ran `pod install`, rewriting the Xcode project with random object ids (two runs, two trees);
> `flutter pub get` already writes the Podfile, so the script uses that.

## 13. Release traps

The static verifier, the run gate, symbol uploads and platform traps are in
`references/release-and-store.md` (§1, §2, §3, §8). The Flutter and Android mechanics:
- **R8 no-arg constructors, concretely** (a Room `*Database_Impl`, pulled in by an ads SDK through
  WorkManager, lost `<init>()` and the app died at start). Collect every class the merged manifest
  builds by name (`aapt2 dump xmltree`: activities, services, receivers, providers, startup
  initializers, component registrars in meta-data) plus every `*Database_Impl`; in
  `apkanalyzer dex packages --defined-only` require the class row **and** its `<init>()` method row.
- **Debug-only `--dart-define`s, proven dead** (method: `references/architecture.md` §12.2): classify
  every `(bool|int|String).fromEnvironment(` key, then run a probe file (not named `_test.dart`) in
  child `flutter test` processes: with every debug define; the same plus
  `--dart-define=dart.vm.product=true` (`kReleaseMode` true at compile time); with no define.
- **Crash handlers print the marker:** both `FlutterError.onError` and
  `PlatformDispatcher.instance.onError` `debugPrint('app: uncaught error: <first line>')`, then
  record: framework errors non-fatal, dispatcher errors fatal (return `true`); never also chain a
  printing handler (errors print twice). An `expect` inside a guarded zone hangs 30 s. Mapping
  uploads run only when the upload keystore config exists (prove it with `./gradlew -m`).
- **Test the artefact that uploads:** `flutter build` leaves a stale APK beside a fresh AAB; build a
  universal APK from the AAB with bundletool and read the version code back off the device.
- The topmost `AnnotatedRegion` for the status bar wins: paint a root override last.

> **Dated facts (as of 2026-10 — re-verify before relying):** for the iOS 27 UIScene requirement, a
> Flutter app needs four parts: `SceneDelegate.swift` in Runner, its Sources-phase membership, an
> Info.plist scene manifest naming it, and plugin registration through the implicit-engine callback.
> google_mobile_ads 9.1.0 needed a Podfile module-map patch to compile on iOS.

## 14. Ads, purchases, analytics and store capture

Rules: `references/monetization-and-privacy.md` §3, §5.5, §8; `references/release-and-store.md` §6.
- **Back while a full-screen ad is on its way** (monetization §3): set the flag inside the
  `setState` that rebuilds `PopScope<void>(canPop: !_adPending, …)`, which refuses system Back and
  `Navigator.maybePop` (route the on-screen Back there; a modal barrier's dismiss already goes there).
  A flag set outside `setState` reaches nothing, and system Back ignores `IgnorePointer`. At show
  time, in the screen and in the service, show only if `mounted`, `ModalRoute.of(context)?.isCurrent`
  and `SchedulerBinding.instance.lifecycleState` is null or `resumed`; otherwise skip, never defer.
- **Store screenshots from the real root:** `t.view.physicalSize = pt * dpr`, `devicePixelRatio =
  dpr`, `padding`/`viewPadding` = `FakeViewPadding(top: insetTop * dpr, bottom: insetBottom * dpr)`,
  `addTearDown(t.view.reset)` (example: 440×956 pt at 3× = 1320×2868 px). Waits are loops of
  `pump(const Duration(milliseconds: 16))`; the ambient switch goes on before the first `pumpWidget`
  (a `const` screen is not rebuilt to start its clocks); pump `const SizedBox()` between scenes.
  Capture with `RenderRepaintBoundary.toImage(pixelRatio: dpr)` under `runAsync`; Flutter's PNG
  encoder writes RGBA, so strip the alpha channel.
- **The preview-video entry point:** a separate `main` built with `-t`, unknown to `lib/`. Inject
  input with `GestureBinding.instance.handlePointerEvent(PointerDownEvent(pointer: id, position: p,
  timeStamp: t, kind: PointerDeviceKind.touch))`, then moves and an up, so raw `Listener`s see it. A
  simulator debug build's `print` reaches the unified log, not the console: append timed marks to a
  file under `Directory.systemTemp` and cut the video by them.

> **Dated facts (in_app_purchase 3.3.1 and the Firebase plugins, as of 2026-10 — re-verify before
> relying). Each quirk goes into a fake in the plugin's real shape (monetization §5.5):**
> - Android: pass `autoConsume: false` and consume after the grant is saved. The iOS StoreKit plugin
>   asserts `autoConsume == true`: pass true there, and call `completePurchase` without awaiting it
>   (it can wait forever).
> - Play answers a cancel or a failure with one purchase whose `productID` is empty: let it answer
>   every buy in flight. Play's restore stamps PENDING purchases `restored`: read the billing
>   purchase state, and never grant or acknowledge a pending one. A StoreKit 2 restored transaction
>   has `pendingCompletePurchase == false`: nothing to complete.
> - `initializeApp` without a config never answered on an emulator: bound it (5 s), never await it
>   before `runApp`. A malformed config (an iOS API key not `AIza` + 35 characters) killed the app
>   natively at launch, past any Dart `try`: check its shape in the setup script and launch a
>   hand-made config once. `logEvent` takes only `String` or `num` (debug-checked only: bools as 0/1).

## 15. Game loop and engine verdict

*Proposed, translated: the shipped games were turn-based, on painters, tickers and springs with no
engine.* Loop rules (fixed step, capped catch-up, swept collision, determinism, raw input):
`references/domain-games.md` §Real-time and action games. The Flutter mechanics:
- **One `Ticker`** from the play widget drives the loop: add each tick's elapsed delta to an
  accumulator, run whole steps of the pure `core/` simulation, cap the catch-up, and write the
  interpolated render state into a `ValueNotifier` the painters take as `repaint:` (§4). Pause on
  lifecycle away (§11): the first tick after a return can carry the whole absence. Per-step state
  never enters a provider (§3); the store hears outcomes (a run ended, a new best).
- **Input:** a raw `Listener` (§5) queues pointer samples stamped with the next step's number; that
  step consumes them, unsmoothed.
- **Determinism in plain Dart tests:** replay a seed and an input log under ticker deltas of 1/30,
  1/60 and 1/120 s plus an injected hitch, and compare state hashes; randomness comes only from a
  seeded generator in `core/`. Widget tests drive the ticker at a fixed rate with `pump(Duration)`.

**When an engine pays.** Decide in kickoff Track C with a probe of the hardest scene (peak object
count at top speed) on the low-tier phone, recorded in the DESIGN technology-verdict format.
*Example (shipped puzzle game, no physics):* an engine (Flame) was rejected: its loop never stops,
its canvas has no semantics (no screen-reader path), its components are a second UI world that
cannot read app state, a breaking major release was in development, and it added 0.38 MB. An engine
or physics package pays when the game needs most of: rigid bodies with joints or stacking; a camera
over a world larger than the screen; hundreds of independently moving, colliding objects; tilemaps or
sprite sheets from an artist's editor. Without those, painters plus one ticker stay smaller, testable
and accessible; menus, results, store and settings stay widgets either way.

## 16. Traps: Dart, widget tests, shell

**Dart.** A void `onTimeout` on a future you did not type throws (§10). `1.0 == 1` on the VM: check
`is int` on JSON. `Int32List.fromList` truncates silently; `Int64List` breaks on web.
`whenComplete(() => map.remove(key))` where the map holds that future deadlocks: use a block body.
Sealed subtypes share the library. `when` is a pattern keyword. `double.fromEnvironment` does not
exist. `@visibleForTesting` members are unusable from `tool/`.

**Widget tests.** `pump(d)` fires timers before building, so one big pump lands a beat without the
timers it starts: pump frame by frame, then hold in steps. A controller started outside a frame
starts on the next; a ticker's time starts at its first frame. `SingleTickerProviderStateMixin`
allows one `createTicker`. Build controllers in `initState`, never as lazy `late final` (a
reduced-motion path first touched one in `dispose` and crashed for every reduced-motion user). A
zero-duration `AnimatedSize` asserts when its child changes. Never `await` a broadcast `cancel()`
(it hangs at 0% CPU). A `const` screen ignores a second `pumpWidget`; covered routes are offstage to
finders (`skipOffstage: false`); semantics-label finders also match modal barriers; `WidgetSpan` text
carries U+FFFC. Lifecycle walks the OS's states (resumed → inactive → hidden → paused).
First-frame-rasterized waits never complete; `Isolate.run` and `toImage` need `runAsync`; a test
`Timeout` cannot interrupt synchronous work. `Stopwatch` does not advance under fake async. A harness
missing a newly used port throws from a `Timer`. Mutation copies need `.dart_tool/package_config.json`
and any path packages; run them with `--no-pub`. Stack-neutral test traps: `references/traps.md` §3,
§4, §10 and §11 (T-34, T-41, T-45, T-106, T-114).

**Shell (setup and gate scripts).** The traps (`grep -q` under `pipefail`, zsh word splitting, macOS
bash 3.2, unanchored `rsync` excludes, Python `False == 0`) are in `references/verification.md` §12.
Flutter's own: `dart format lib` reformats other lanes' files, so format an explicit list.
