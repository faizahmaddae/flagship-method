# Other stacks: translating the harnesses

The method is stack-neutral; its harnesses are not. This page maps each harness the Flutter playbook
builds (`references/stack-flutter.md`) to SwiftUI, Jetpack Compose, React Native and the web, so a
project on another stack knows which tool to try first and which gaps to plan around.

**Read when:** the stack is not Flutter: at kickoff (the identity probes in §0, and to plan the
Phase 0 harnesses), when filling the baseline block (§Baseline commands), and whenever a reference
says "(Flutter: …)" and you need the equivalent.

> **Dated facts (as of 2026-10 — re-verify before relying):** every tool and API below is named from
> general knowledge as of 2026-10. **None was exercised by the shipped projects this skill comes
> from**, which were all Flutter. Three were run while testing this skill (2026-10): the headless
> Chrome probe in §0 (macOS, Chrome); the SwiftPM finding in §1 (a target with no declared
> dependencies built with `import SwiftUI`); and the SwiftUI render facts in §5 with the SwiftUI test
> command in §Baseline commands (a Swift package probe on an iOS simulator and on a macOS host).
> Treat every other row as a lead: read the tool's docs or installed source for the version you will
> use, then prove the harness can fail before you trust it.

**Tags.** **[known]**: an established tool or API whose existence and purpose are not in doubt; its
fitness for *this* harness is still yours to prove. **[Unverified]**: plausible, but not confirmed to
exist in this form or to do this job; build a 30-minute probe before planning on it. **[gap]**: no good
equivalent known; plan the workaround named.

## Contents
Baseline commands · 0. Identity probes before Phase 0 · 1. Layer contract · 2. Per-frame values off
state · 3. Custom painting and shaders · 4. Raw pointer input · 5. Raster tests and the bounds ring ·
6. Preview rendering to PNG · 7. Frame-budget tests · 8. Real-device frame timing · 9. Text-scale
matrix · 10. Accessibility audit · 11. Reduce motion · 12. Fonts in tests · 13. Bounded awaits ·
14. Debug flags dead in release · 15. Native project regeneration · 16. Release artefact and run
gate · 17. Porting checklist

---

## Baseline commands: analysis and tests

CLAUDE.md's baseline block and PROGRESS "How to verify" need a static-analysis gate and a test
command, and the definition of done opens with "analysis clean". Fill them from this table, make
each row fail once on purpose (a planted warning, a planted failing test) before trusting it, and
write the expected test count beside the command, so a run that silently skips tests shows.

| Stack | Analysis gate | Test command |
|---|---|---|
| SwiftUI | a build with warnings as errors (`SWIFT_TREAT_WARNINGS_AS_ERRORS=YES`); SwiftLint `--strict` if adopted [Unverified until probed] | `xcodebuild test -scheme <scheme> -destination 'platform=iOS Simulator,name=<phone>'`, in the package folder or with `-project`/`-workspace` (`xcodebuild -list` names the schemes) [verified 2026-10 on a Swift package; never macOS `swift test` for anything drawn: §5] |
| Compose | Android lint with `warningsAsErrors`, detekt, and Kotlin's all-warnings-as-errors option [Unverified until probed] | `./gradlew testDebugUnitTest` (JVM tests, Paparazzi or Roborazzi included); `./gradlew connectedDebugAndroidTest` on a device [Unverified until probed] |
| React Native | `tsc --noEmit` and `eslint . --max-warnings 0` [Unverified until probed] | Jest; device flows with Maestro or Detox [Unverified until probed] |
| Web | `tsc --noEmit` and `eslint . --max-warnings 0` [Unverified until probed] | the unit runner (Vitest or Jest) and `playwright test` [Unverified until probed] |

## 0. Identity probes before Phase 0: a headless browser

Kickoff renders each candidate direction before the app exists (`references/kickoff.md` §Identity).
React Native has no headless renderer (§5), and before Phase 0 no stack has an app to screenshot. So
render the candidates as SVG or HTML **from one shared data set** and screenshot them with headless
Chrome. Label every file "not the real stack". Make the real-stack render harness the first item of
Phase 0 (§6, §17) and re-render the chosen direction there before Phase 2 judges it.
1. **One small script** (Python or Node) writes one SVG or HTML file per direction × state: the hero at
   its smallest real size, a full screen at 390×844 pt, the payoff, the empty state, and each
   lighting the identity plans. Every file is a function of the same data, so only the identity
   differs.
2. **Bundle the candidate faces** with `@font-face` pointing at local, licence-checked files; never
   rely on system fonts.
3. **Render:**
   ```bash
   CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"   # Linux: google-chrome or chromium
   "$CHROME" --headless=new --hide-scrollbars --force-device-scale-factor=3 \
     --window-size=390,844 --screenshot="$PWD/out/a_screen.png" "file://$PWD/probes/a_screen.html"
   ```
   The window size is in CSS px (equal to pt here), so the PNG is 1170×2532. Give `--screenshot` an
   absolute path. Add `--virtual-time-budget=3000` if anything loads or animates asynchronously (local
   `@font-face` files loaded without it).
4. **Prove the face loaded:** render one line as `font-family: Probe, monospace` and again as plain
   `monospace`. Byte-identical PNGs mean the face never loaded (checked both ways: a missing font file
   gave identical bytes, the real one did not).
5. **Look at the PNGs themselves,** at real size and in `scripts/contact_sheet.py`, never at a
   file-browser preview: macOS Quick Look cropped a tall SVG to a square and hid half the faults.

*Example (an expense-splitter kickoff on React Native):* three directions as SVG from one data set;
four looks found five real faults before any app code existed: label collisions, a small balance
that read as settled, and a payoff line drawn across every initial.

Native stacks before their scaffold can use the same route. Where a scratch project is cheap, render
in the real stack instead: SwiftUI's `ImageRenderer` in a Swift package test run by `xcodebuild test`
on an iOS simulator (verified 2026-10; a macOS host draws macOS controls and ignores text scale: §5),
or Compose through Paparazzi or Roborazzi in a scratch module [known tools; as probes Unverified].

## 1. Layer contract enforcement

The shape does not change (`references/architecture.md`): an allow-list table in
`docs/<slug>/ARCHITECTURE.md`, a test that reads it, must-catch and must-ignore fixtures, and an
anti-vacuity assert.
- **SwiftUI:** make each layer its own SwiftPM target, so the compiler refuses undeclared imports of
  your *own* modules [known]. It does **not** stop system frameworks: SwiftUI, UIKit and Combine need
  no declared dependency, and a `Core` target with no dependencies built cleanly with `import SwiftUI`
  (verified 2026-10, Swift 6.4). Ban them in Core with an import scan over Core's sources, lexer-based like the
  Flutter guard, with must-catch and must-ignore fixtures (a `#if canImport(UIKit)` block, an import
  inside a comment) [Unverified as a ready tool: write it]. A second net: also build Core on Linux in
  CI, which has neither SwiftUI nor UIKit (macOS lacks UIKit but has SwiftUI) [Unverified: probe it].
  Add a test that compares `Package.swift`'s target dependencies with the doc table [Unverified as a
  ready tool: write it].
- **Compose:** one Gradle module per layer (a pure Kotlin/JVM `:core` cannot see Android) [known];
  Konsist or ArchUnit tests for package rules inside a module [known]; detekt's `ForbiddenImport`
  [known].
- **React Native / web:** ESLint `no-restricted-imports` or `import/no-restricted-paths` per
  directory, `eslint-plugin-boundaries`, or dependency-cruiser with a rules file [known]. TypeScript
  project references make `core` a separate compilation unit [known], but like SwiftPM they bound only
  your own projects: a package in `node_modules` (`react`, `react-native`) still resolves from `core`,
  so the lint rule is the guard.
- Lint rules match globs or patterns: add fixtures that must fire and must not, because a lint that
  never fires looks exactly like a clean tree.

## 2. Per-frame values off state

Rule: state management holds durable values; per-frame values bypass it and reach the drawing code
directly (`references/performance.md`).
- **SwiftUI:** `TimelineView(.animation)` driving a `Canvas`; `Animatable`/`animatableData` inside
  shapes [known]. Keep per-frame values out of `@Observable` objects that large view bodies read.
- **Compose:** read animated values in draw or layout lambdas (`Modifier.drawBehind {}`,
  `graphicsLayer {}`, `offset {}`), so recomposition is skipped; `Animatable`, `withFrameNanos`
  [known].
- **React Native:** Reanimated shared values with `useAnimatedStyle` worklets on the UI thread;
  react-native-skia values driving a Skia `Canvas` [known]. Never `setState` per frame.
- **Web:** `requestAnimationFrame` writing to a canvas or `style.transform` through refs [known];
  never framework state per frame.

## 3. Custom painting and shaders

- **SwiftUI:** `Canvas`, `Shape`/`Path`; Metal shaders through `.colorEffect`/`.layerEffect`/
  `.distortionEffect` (iOS 17+) [known].
- **Compose:** `Canvas`/`DrawScope`; AGSL `RuntimeShader` on Android 13+ only [known], so older
  devices need the designed fallback from day one.
- **React Native:** react-native-skia (`Canvas`, `RuntimeEffect` shaders) [known].
- **Web:** Canvas 2D, WebGL or WebGPU fragment shaders [known].
- The shader rules in `references/performance.md` §7 are GPU rules and apply to MSL, AGSL and GLSL
  alike: `1.0 - smoothstep(lo, hi, x)`, a sin-free hash, time wrapped at whole cycles, half-level
  dither, a per-pixel budget in the header, a fallback that still looks designed.

## 4. Raw pointer input for drawing

The trap generalises: gesture recognisers wait for a slop distance before they start, so the first
cell of a drag feels dead. Cancel discards and never submits.
- **SwiftUI:** `DragGesture(minimumDistance: 0)` [known]; measure first-touch latency on a device. For
  full control, a `UIViewRepresentable` with `touchesBegan/Moved/Ended/Cancelled` [known].
- **Compose:** `pointerInput { awaitEachGesture { awaitFirstDown(); … } }` [known];
  `detectDragGestures` waits for touch slop.
- **React Native:** Gesture Handler `Gesture.Pan().minDistance(0)` or `Gesture.Manual()` [known];
  check the slop semantics of the version you install [Unverified].
- **Web:** Pointer Events with `touch-action: none` and `setPointerCapture`; `pointercancel`
  discards [known].

## 5. Raster tests and the bounds ring

Every painter gets a test that rasterises it and samples pixels at design proportions, and a test
that nothing paints outside its declared bounds (render on a larger transparent canvas, assert alpha
0 in the ring).
- **SwiftUI:** `ImageRenderer(content:)` → `cgImage`, then read pixels through a `CGContext` [known],
  on the iOS simulator (dated block below). Whether `Canvas` content past its frame is drawn without
  `.clipped()` [Unverified]: probe it, then write the ring test either way.
- **Compose:** `captureToImage()` in compose-ui-test, then `toPixelMap()` [known]; JVM-side rendering
  with Paparazzi (layoutlib) or Roborazzi (Robolectric) to PNG, read back as a `BufferedImage` [known].
- **React Native:** [gap] for native views: there is no headless renderer. Skia drawings can be
  snapshotted (`makeImageSnapshot` on the canvas ref) [known]; for views, use device screenshots
  (Maestro, Detox) and sample pixels in a script [known tools, pipeline Unverified].
- **Web:** a headless browser (Playwright) with `canvas.getContext('2d').getImageData` or a
  screenshot buffer [known].

> **Dated facts (SwiftUI, verified 2026-10 in a Swift package probe: `xcodebuild test` on an iOS 27
> simulator, and `swift test` on a macOS host — re-verify before relying):**
> - **Render on the iOS simulator.** The macOS host drew macOS metrics and controls (one string drew
>   76 px wide there, 96 px on iOS) and ignored `.dynamicTypeSize`: `.large` and `.accessibility3`
>   both drew 76×18 px, against 96×23 and 214×53 on the simulator. A macOS host suits custom-drawn
>   content only, never text scale or controls.
> - **`ImageRenderer` drew `Text`, shapes and a bordered `Button`, but drew `TextField`, `Toggle`,
>   `Stepper` and a segmented `Picker` as yellow (#FFCC00) placeholder boxes** on the simulator (on
>   macOS, `Toggle` became a checkbox and the rest placeholders). Capture screens with platform
>   controls from an app-hosted UI test or a simulator screenshot (§6).
> - A `UIHostingController` drawn with `drawHierarchy` in a package test with no host app passed and
>   wrote a fully transparent PNG.
> - So every SwiftUI render harness carries two anti-vacuity asserts: the image is neither blank nor
>   uniform and has no placeholder-yellow area; and the drawn size at the largest text setting
>   exceeds the drawn size at the default.

## 6. Preview rendering to PNG (the look loop)

A harness that renders every screen across the look matrix (`references/visual-design.md` §13.1)
into a gitignored folder, then `scripts/contact_sheet.py` to look at them.
- **SwiftUI:** a unit test rendering custom-drawn screens with `ImageRenderer` at device sizes, on the
  iOS simulator (§5 dated block); screens with platform controls through an app-hosted UI test
  (`XCUIScreen.main.screenshot()`) or `xcrun simctl io booted screenshot` [known];
  swift-snapshot-testing [known; check what it draws for platform controls].
- **Compose:** Paparazzi or Roborazzi in record mode; the Compose Preview Screenshot Testing Gradle
  plugin [known, check its maturity]; device captures with `adb exec-out screencap -p` [known].
- **React Native:** Storybook stories plus device screenshots; Maestro `takeScreenshot` [known].
- **Web:** Playwright screenshots over a viewport list; Storybook's test runner [known].
- Byte-equal goldens break on renderer and OS upgrades on every stack: keep "hash before you change"
  for additive work and use thresholds for device captures (`references/verification.md`).

## 7. Frame-budget tests (what repaints, what rebuilds)

A CI test that pins what a moment may redraw and re-render, because a final-screen assertion cannot
see the cost.
- **SwiftUI:** [gap] for a CI log of which bodies ran. `Self._printChanges()` explains a body run in
  debug [known]; a counter incremented in `body` under test is a crude probe [Unverified as reliable].
  XCTest performance metrics for animations and scrolling exist; check which signpost metrics cover
  your case [Unverified].
- **Compose:** count recompositions with a `SideEffect { count++ }` probe in a test [known pattern];
  Layout Inspector recomposition counts while developing [known].
- **React Native:** React's `<Profiler onRender>` counts renders [known]; Reassure for render-count
  regressions in CI [known]. UI-thread work (Reanimated) is invisible to both.
- **Web:** React Profiler in tests; a Playwright CDP trace; `PerformanceObserver` with
  `long-animation-frame` in Chromium [known].
- Where the stack has no CI form ([gap]), the substitute is a profiler run on a device (§8), listed
  in PROGRESS "Device checks" with its DECISIONS entry; never a criterion nobody can run.

## 8. Real-device frame timing

Simulators and emulators do not measure frames honestly (`references/performance.md`).
- **iOS:** Instruments (Animation Hitches, SwiftUI templates); MetricKit hitch data from the field
  [known].
- **Android (Compose and React Native):** Macrobenchmark `FrameTimingMetric`, JankStats,
  `adb shell dumpsys gfxinfo <package> framestats` [known]; Flashlight for React Native [Unverified].
- **Web:** Chrome DevTools Performance on a mid-range Android phone through remote debugging [known].

## 9. Text-scale matrix

Every screen × 2 reference phones × {1, ~1.3, 2}: nothing clipped, cut or overflowing, and reading
text **drawn** at the scale. Check the drawn size, not the setting: each stack has a silent shrinker
(`minimumScaleFactor` in SwiftUI, `adjustsFontSizeToFit` in React Native, fit-text helpers on the web,
`FittedBox` in Flutter).
- **SwiftUI:** `.environment(\.dynamicTypeSize, .accessibility3)` in render tests on the iOS
  simulator only (a macOS host ignored it: §5 dated block), asserting the drawn size grows;
  `xcrun simctl ui booted content_size accessibility-extra-extra-extra-large` on the simulator [known].
- **Compose:** `CompositionLocalProvider(LocalDensity provides Density(density, fontScale = 2f))` in
  tests; Paparazzi's device config font scale; `adb shell settings put system font_scale 2.0` [known].
- **React Native:** `allowFontScaling` and `maxFontSizeMultiplier` per `Text` [known]. Jest renders no
  layout [gap]: run the matrix on devices with the simctl and adb commands above.
- **Web:** root `font-size` at 200% *and* browser zoom at 200% (WCAG text resize), looped in Playwright
  [known].

## 10. Accessibility audit

The rule (`references/ux-and-accessibility.md`): every control has a label, a role and a ≥ 44 pt
touch area found by hit-testing, and every tap handler is reachable by a screen reader.
- **SwiftUI / iOS:** `XCUIApplication().performAccessibilityAudit()` (Xcode 15+); AccessibilitySnapshot
  for snapshot-level checks [known]. Hit-test with `XCUIElement.isHittable` and its frame [known].
- **Compose:** Accessibility Test Framework checks (Espresso's `AccessibilityChecks` for views; a
  Compose test-rule equivalent in recent versions [Unverified]); `assertTouchHeightIsEqualTo`,
  `assertHeightIsAtLeast(48.dp)`, and `SemanticsNode.touchBoundsInRoot` for the real touch area [known].
- **React Native:** Testing Library queries by role and label; `eslint-plugin-react-native-a11y`
  [known]; on device, Xcode's Accessibility Inspector and Android's Accessibility Scanner [known].
- **Web:** axe-core through `@axe-core/playwright`, Lighthouse [known]; hit-test with
  `document.elementFromPoint` at the centre and 1 px inside each edge [known].
- Every stack: a decorative overlay that blocks touches must also be hidden from the screen reader.

## 11. Reduce motion

Motion Off removes presentation motion (transitions, shake, flashes, parallax, ambient life,
celebrations); motion that is the task (a real-time simulation, a video, a live map) continues;
outcomes are identical for the same input; pressed states still show
(`references/motion-and-feel.md` §10).
- **SwiftUI:** `@Environment(\.accessibilityReduceMotion)` [known].
- **Android / Compose:** "Remove animations" sets `Settings.Global.ANIMATOR_DURATION_SCALE` to 0 [known];
  whether every Compose animation honours it on its own [Unverified]: read it and gate yourself.
- **React Native:** `AccessibilityInfo.isReduceMotionEnabled()` plus its change listener; Reanimated's
  `useReducedMotion` [known].
- **Web:** `matchMedia('(prefers-reduced-motion: reduce)')` and the CSS media query [known].

## 12. Fonts in tests

Test runners often draw a fallback face, so every measurement and pixel is wrong and tofu passes.
- **iOS:** register the bundled files in the test target with `CTFontManagerRegisterFontsForURL` [known].
- **Compose:** fonts from `res/font` in Paparazzi or Roborazzi renders [Unverified]: prove it with a
  two-glyph tofu test.
- **Web:** `await document.fonts.ready` before any screenshot or measurement [known].
- Every stack: paint two different glyphs and compare (identical pixels are the bug); compare two
  weights to catch a missing one.

## 13. Bounded awaits

Every platform, plugin and network await gets a bound and a fallback, and never times out into the
unsafe side (`references/architecture.md`). In every stack, a timeout stops *your wait*, not the call:
mark state before awaiting, and let in-flight work clean itself up.
- **Swift:** no built-in timeout; race the call against `Task.sleep` in a throwing task group [known].
- **Kotlin:** `withTimeoutOrNull` [known]; cancellation reaches only cooperative calls.
- **JS/TS:** `Promise.race` with a timer; `AbortSignal.timeout(ms)` for fetch [known].

## 14. Debug flags proven dead in release

Same three-way proof as Flutter: debug with the flag (it must take effect), release with the flag (it
must do nothing), release without (the shipped defaults).
- **Swift:** `#if DEBUG` compile conditions; build Release and search the binary's strings for the
  flag's key [known].
- **Android:** `BuildConfig.DEBUG` plus R8 dead-code removal; inspect the dex with `apkanalyzer`
  [known].
- **React Native / web:** `__DEV__` or `process.env.NODE_ENV` replaced at build time; grep the
  production bundle for the flag's name and its mock values [known].

## 15. Native project regeneration

The rule from the Flutter setup script: generated native folders are rebuilt by one idempotent script
that validates inputs first, checks every edit, and reruns every check at the end
(`references/release-and-store.md`).
- **SwiftUI:** XcodeGen or Tuist generate the `.xcodeproj` from a committed spec; keep the project
  gitignored [known]. Read effective settings with `xcodebuild -showBuildSettings`.
- **Compose:** Gradle files are the source and nothing regenerates; version catalogs and convention
  plugins keep them reviewable [known].
- **React Native:** Expo prebuild (Continuous Native Generation) with config plugins regenerates
  `ios/` and `android/`: the same shape as the Flutter script [known]. In bare React Native the native
  folders are committed: patch them by script, with checks.
- **Web wrapped as an app (Capacitor and similar):** native folders are usually committed; treat them
  like bare React Native [Unverified for your wrapper].

## 16. Release artefact and run gate

What a green build cannot show must be checked on the artefact itself, and then the release build
must be started and played (`references/release-and-store.md`).
- **iOS (any stack):** `codesign -d --entitlements - --xml`, `security cms -D -i
  embedded.mobileprovision`, `dwarfdump --uuid` against the uploaded dSYM [known].
- **Android (any stack):** bundletool, `apksigner verify --print-certs`, `aapt2 dump`, `apkanalyzer`
  [known]. The R8 no-arg-constructor check in `references/stack-flutter.md` §13 applies to every
  Android app.
- **React Native:** source maps uploaded for the exact build; grep the JS bundle for test ids [known].
- **Web:** grep the production bundle for test keys; keep source maps private [known].
- **Run gate:** fresh install, cold start, prove the app's own code ran through the accessibility tree
  (XCUITest, UIAutomator, Maestro or Playwright) within 30 s, play the core flow, health check after
  each stage.

## 17. Porting checklist (Phase 0 on a non-Flutter stack)

- [ ] First: the real-stack render harness with its anti-vacuity asserts (SwiftUI: `xcodebuild test`
  on an iOS simulator destination, never macOS `swift test`: §5), and the chosen identity
  re-rendered in it (§0 probes were not the real stack).
- [ ] The baseline row (§Baseline commands) probed: the analysis gate and the test command each seen
  to fail once, then written into CLAUDE.md's baseline block with honest timings and the expected
  test count.
- [ ] Layer guard with must-catch and must-ignore fixtures, seen to fail on a deliberate violation.
  Retrofitting an existing codebase: legacy rows under a ratchet (`references/architecture.md` §2.5).
- [ ] Raster harness: one component rendered to pixels, a sample-and-assert test, a bounds ring test.
- [ ] Preview harness writing PNGs to a gitignored folder, viewed through a contact sheet.
- [ ] Text-scale matrix and accessibility audit driven by one list of screens.
- [ ] A render-count or frame-budget probe on the hottest interaction.
- [ ] Native regeneration script (or a written policy for committed native folders) with checks.
- [ ] A release-artefact verifier skeleton and a run-gate plan.
- [ ] In DECISIONS: each chosen tool, its version, what you verified, every [Unverified] item you
  turned into a fact, and every [gap] with its workaround. Write the verified rows into
  `docs/<slug>/ARCHITECTURE.md` as the project's own stack page.
