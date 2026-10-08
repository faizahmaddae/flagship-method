# Performance

How to keep every frame inside budget on the oldest phone you support, and how to prove it: tests that
pin what each moment may repaint, layers split by how often they change, a quality tier that degrades
once and never flickers, and frame numbers taken from a real device rather than a simulator.

**Read when:** building any painter, animation, shader or particle effect; laying out a screen with
motion; planning Phase 2's performance criteria; before the owner's device test; when a frame log or
a user says "it stutters".

## Contents
1. The budget
2. Frame-budget tests in CI
3. Repaint isolation: layers by change frequency
4. One ticker, only while something can change
5. Per-frame work: pools, bakes, no blur on movers
6. Know your renderer's cost model
7. Shader rules
8. Quality tiers: an Auto that trips once
9. Startup budget
10. Assets, fonts and size
11. Real-device profiling
12. The profiling log
13. Checklist

## 1. The budget

- **A frame costs what it repaints and what it rebuilds.** Neither shows in a test that checks only
  the final screen, so cost needs its own tests (§2).
- **Budget = one 60 Hz frame, 16.67 ms, for each pipeline stage.** Build (UI thread) and raster (GPU
  thread) are pipelined, so either one running long drops a frame. Keep 60 Hz as the full-look floor
  on 120 Hz displays: a 120 Hz phone that misses some 8.3 ms frames still runs smoothly at 60.
- **Animate what the user watches.** "The obvious animation is usually the expensive one": put motion
  on the five things in the user's eye line, not on a 275-cell background pattern.
- **Write the cost into the code.** Every painter or effect's header carries a **Cost** line: draw
  count, blurs, offscreen layers, per-pixel work, and the test that pins it. *Example budgets
  (shipped puzzle game):* at most 8 small draws per board cell with no layer and no blur; the mascot
  ≤ 85 draws with zero mask blurs; whole views 59–81 draws.

## 2. Frame-budget tests in CI

**Log each frame, then assert per moment.** In UI tests, hook the framework's debug callbacks to
record, frame by frame, every painter that painted and every UI component that rebuilt. Then assert:
- which painters may paint, and in which time window of the moment;
- the exact set of component types allowed to rebuild (an exact set, not "few").

*Example assertions (shipped puzzle game):* "the backdrop painter never runs during the reveal"; "the
card's picture is painted exactly once (its settle is a transform)"; "the completion stamp repaints
only until 500 ms"; "the caption repaints only while the time counts up"; "never the screen, the
panel or the card rebuilds; rebuilt types == {switcher, two listenable builders, one text}".

**Cover the hot moments, at every quality tier:** first touch, continuous input (drawing, dragging,
scrolling), a collect or reward, the completion sequence, idle with ambient motion, panels opening,
screen transitions, list scroll.

**What these tests caught:** a week strip repainting through a whole reveal (a layout-reading
wrapper rebuilt when a busy flag flipped); a state change inside a frame that rebuilt the reactive
store's root scope (`references/architecture.md` §3.3).

**Pin draw counts without rasterising.** A recording fake canvas counts draw calls, blurs and layers
per painter, so draw budgets run in milliseconds. The fake answers only the queries it overrides
(current transform, save count), so painters undo their own transforms arithmetically instead of
reading them back (Flutter's fake: `references/stack-flutter.md` §9.7).

**Prove the test can fail, honestly.** Remove a repaint boundary and watch the test go red. Know first
which constructs add their own layer: a negative control that removed only the inner boundary still
passed because an opacity wrapper above it was itself a boundary (Flutter: `references/stack-flutter.md`
§9.6). Alpha changes below 1/255 never repaint; move the child in the control to force one. More on
negative controls: `references/verification.md`.

Flutter hooks and their traps: `references/stack-flutter.md` §Tests. Other stacks have equivalents
(recomposition counters, view-update logging, paint flashing): `references/stack-other.md`.

## 3. Repaint isolation: layers by change frequency

**Split the scene into layers by how often each changes.** Each independently changing layer is its
own repaint boundary, and the layers are siblings in one stack. Write the table, with these four
columns, in the architecture doc's rendering section (`assets/templates/ARCHITECTURE.md` §5):

| # | Layer | Repaints when | Kept as |
|---|---|---|---|
| 1 | Backdrop | its own ticker, only if ambient motion, motion and high quality are all on | shader, or a baked still at low |
| 2 | Static base (board, list chrome) | content identity, geometry, palette or quality changes | recorded picture |
| 3 | The thing the user is building (path, selection) | on each committed change, plus springs | live painter |
| 4 | Static overlay drawn above it | as layer 2 | recorded picture |
| 5 | Items that react (collectibles, badges) | on their events only | live painter, cached text |
| 6 | Transient effects (particles, hint marks) | while alive | one atlas draw |
| 7 | Character or mascot | its own clock | own layer |
| 8 | Accessibility overlay | never paints | — |

*Example (shipped puzzle game):* the path end's idle pulse got its own layer so its clock never
repaints the path's blurred shadow; a bumped wall is lifted out of the recorded picture and shaken alone.

**Rules:**
- A ticking backdrop is a **sibling** of the content, never a parent wrapping the app. Full-screen
  flights (a reward travelling across the screen) each get their own boundary.
- A wrapper that reads its constraints to build children repaints its own layer whenever anything
  below rebuilds. Fence it with a boundary *above* (a boundary below cannot stop it), or use known
  sizes in hot components.
- Record stills once; re-record only when (content identity, geometry, palette, quality) change;
  dispose old pictures.
- Per-frame values reach painters as listenables the painter repaints on, never through the reactive
  store and never through UI rebuilds. The "should repaint" check compares configuration only.
  Publish a frame value only when it changed (value-equal frame objects).
- Keep the UI tree's shape constant across states: wrapping a child only in some states rebuilds it.
- Lay text out once at a reference size and scale the canvas to draw it (cache by text and colour,
  small LRU): a figure that changes size every frame must build no new text layouts.

## 4. One ticker, only while something can change

- One ticker per choreographer, created lazily, running only while an effect is live, stopped when
  the last effect ends, so a still screen renders no frames. Bank its time on stop so a restart
  continues smoothly.
- A ticker's time starts at its first frame, not when started: stamp new effects at the first frame
  after creation ("pending beats"), or the first beat is skipped.
- **Motion Off starts no presentation ticker:** not slower, nothing scheduled. A simulation ticker
  that *is* the task keeps running (`references/motion-and-feel.md` §10)
  (`references/motion-and-feel.md`).
- Gate endless ambient motion with one global switch that tests leave off unless they turn it on;
  otherwise every "wait until settled" in tests times out.
- A running animation controller renders every vsync: it is not a timer. A wall-clock timer keeps
  counting in the background: stop it on pause.
- **Endless clocks wrap on a whole period.** Every endless motion completes whole cycles in one period
  (e.g. 1200 s) and the clock wraps there: no visible jump, and single-precision time never loses
  precision in long sessions.

## 5. Per-frame work: pools, bakes, no blur on movers

- **One particle system.** A fixed pool of typed arrays allocated once; each particle a closed-form
  function of (launch state, age), so it looks identical at 30/60/120 Hz with no integration error;
  drawn with **one** atlas draw call from an atlas baked at startup (baking on first use hitched the
  first burst, mid-gesture). Budget it: e.g. 256 at high quality, 64 at low, ambient drift ≤ 24 alive.
  Off entirely when motion or quality says so: frozen particles read as dirt.
- **No allocation per frame, no randomness at paint time** (variety from `hash(index, salt)`).
- **Bake what is drawn often but changes rarely** into an image and draw the image. *Example:* 200
  level thumbnails kept as recorded pictures would redraw 200 boards, blurs included, on every scroll
  frame; baked images cost one draw each.
- **Caches own their images and hand out clones** that holders dispose. *Incident:* a shared cache
  disposed an image still on screen, seen only at item 30 of 200 in a whole-content playthrough: test
  caches with many keys in one process.
- **No blur on anything that repaints every frame.** Soft shadows become radial gradients or two
  offset fills (the nearer adding to the farther); occlusion creases become dark radial smudges.

## 6. Know your renderer's cost model

**Learn what your renderer keeps between frames and what it redraws, then draw within it.** Classify
every expensive effect you use (blurs, offscreen layers, shaders, clips, image filters) as cheap or
dear *for the renderer and version you ship*. Verify by reading the engine source at that version or
by measuring on a device, and write the result in a dated block under the architecture doc's
rendering section. A plan item like "cache the shadow" means nothing on a renderer that caches
nothing.

> **Dated facts (as of 2026-10 — re-verify before relying):** Flutter 3.47's Impeller renderer
> has no raster cache (read from engine source: disabled on Metal, GL and Vulkan). A recorded picture
> is replayed, blurs and all, on every frame that touches its region: every frame on Android, and on
> iOS wherever the damage reaches (a ticking full-screen shader damages everything). Cheap: mask blur
> on filled rounded rects, circles, ovals and filled convex paths (analytic). Dear: mask blur on
> strokes or non-convex paths, and an image-filter blur on an offscreen layer (a Gaussian pass every
> time). Shader image filters do not work under the test runner or off Impeller. Flutter API side:
> `references/stack-flutter.md` §7.

**Offscreen layers are for correctness, not decoration.** Use one, bounded to the drawn area, to
composite a translucent stack once: pieces drawn opaque inside it replace each other, and the whole
composites at the layer's alpha, so overlaps never darken joints. Never open one per part per frame.

**Give every dear effect a designed low form** (used by §8):
- **Stepped shadow:** the shape unblurred as a core, plus a fringe one sigma further along the light at
  0.4 of the alpha, with the core alpha solved so the overlap composites to exactly the blurred peak
  `a`: `core = 1 − (1 − a) / (1 − 0.4a)`.
- Inner shading becomes linear gradients following the blur's normal-CDF profile; corners composite
  in a small layer so two edges combine as `1 − (1 − t)(1 − l)`.
- A low form never reaches further than the blur did, so bounds tests hold at both qualities.

## 7. Shader rules

- **Prove it paints under the test runner before depending on it**, so "every painter has a test that
  paints it" still holds. Shader tests assert real pixel colours with no try/catch (a probe test that
  swallowed its own exception could not fail).
- **Preload every program before the first frame, bounded** (e.g. 2 s overall); load once per process;
  remember a failure (a broken asset will not mend on retry).
- **Fallback in the product's own look.** A plain gradient fallback read as programmer art; at low
  quality bake the shader's still frame once into an image (≤ 2× pixel ratio, ~5 MB on a 390×844 pt
  phone) instead of running a still shader per pixel per frame. Keep the gradient only for a shader
  that failed to load.
- **One uniform layout for every shader,** documented as an index table in each shader header and in
  the code that writes it, pinned by a test, so the app side never changes per theme.
- **Write the per-pixel budget in the header** ("no derivatives; five value-noise lookups per ground
  pixel; three distance functions per sky pixel") and branch by screen region (row bands), so each
  pixel pays only for its band.
- **Portability traps tests cannot catch** (the test renderer differs from the device GPU; verify on
  every GPU backend you ship, e.g. Metal and OpenGL ES/Vulkan):
  - `smoothstep(e0, e1, x)` with `e0 ≥ e1` is undefined on Metal/Vulkan/SPIR-V; write a falling edge as
    `1.0 − smoothstep(lo, hi, x)` and say so in every header;
  - `sin()` of large arguments turns to noise on mediump GPUs: use a sin-free hash;
  - add half a level of dither so long gradients never band;
  - work in height units (`p = frag / height`) so shapes keep proportions on every phone;
  - apply perspective vertically only to ground patterns (full perspective converges into streaks);
    fade fine grain before the horizon so it never shimmers.
- **Adding a variant** (a night mode): gate every new part on its uniform, so the existing frames stay
  byte-identical; hash them before the change and hold them in a test.

## 8. Quality tiers: an Auto that trips once

**Offer Auto, High and Low.** Every expensive effect has a designed low form in the project's own
look (`references/visual-design.md`): the low path must look designed, not stripped.

**Auto's rules:**
1. Start High.
2. Degrade **once per session** when frames are *sustainedly* slow, and never recover within it. Low
   is cheaper by design, so a monitor that could recover would measure the cheap frames, climb back,
   and flicker.
3. Never save the tripped state (one hot minute would become permanent). A return after ≥ 30 min in
   the background starts a new session at High.
4. An explicit High or Low always wins.
5. Off in debug builds: debug frames are slow by design, and some simulators run debug builds only
   (§11), so every screenshot would show the low look.

**Monitor numbers** (example, shipped puzzle game, marked provisional until device logs): a frame is
over budget when build *or* raster exceeds 16.67 ms; trip when 15 of the last 60 rendered frames are
over; require a full window; ignore the first 3 s after the first report (launch, first decodes).
Know what the threshold lets through: a phone that steadily drops one frame in five (~48 fps of
visible judder) stays High under 15/60. Tune it from device logs (e.g. toward 10/60) and record the
change as a decision.

**Degrade list (example):** full-screen shader → baked still; dear blurs → stepped forms; particle
pool 256 → 64; ambient drift off.

**Wiring:** resolve quality once at the root and pass it to painters as an explicit parameter (no
globals); previews and tests set it fixed. Run the frame-budget tests and the bounds tests at both
qualities, and put the low look on the review sheet beside the high one.

## 9. Startup budget

The rules that keep startup from hanging (bounded awaits, nothing that needs a sheet before the first
frame) live in `references/architecture.md` §8. For speed:
- **Warm what the first interaction needs before the first frame:** shaders (bounded), the particle
  atlas (baked synchronously), the first-gesture sounds (loaded in the background, dropped if stale),
  and the settings that decide whether to animate.
- **Parse large data off the UI thread in one hop:** load bytes; decode and parse in one background call.
- **Defer SDKs:** analytics starts first and is never awaited; ads start after the user has finished a
  few tasks, at a calm moment; nothing with UI starts on cold launch.
- **Measure cold start on release builds,** first install and later launches, and record both.
  *Example (shipped puzzle game, release build on an emulator, so relative only):* 3.7 s on first
  install, 0.94–1.36 s after.
- **Warm up before recording.** A debug build stalled 158 ms compiling the first run of a heavy
  sequence and 77 ms after one warm-up pass: play it once off camera before capturing store previews.

> **Dated facts (as of 2026-10 — re-verify before relying):** in Flutter 3.47, `AssetBundle.loadString`
> decodes assets over 50 KB on a separate isolate and caches the string for the app's life; parsing it
> on another isolate then costs two spawns and a pinned copy (a 660 KB content pack). Load bytes and
> decode plus parse in one `compute` call.

## 10. Assets, fonts and size

- **Bundle fonts; never fetch them at run time.** Cut static weight instances from variable fonts: a
  static file draws its weight identically on every renderer and under the test runner. Pin each
  upstream file's sha256; test that each file's own weight class matches the declared weight; load the
  same font files in tests.
- **Draw icons as painters, not font glyphs:** no icon font, no missing-glyph boxes.
- **Ship raster assets at the density they display at.** *Example:* full-screen launch images at 3×
  (~1.7 MB each); 2× softened visibly on 3× phones.
- **Size budgets are checks:** e.g. the generated sound pack fails above 9 MB. Measure what each
  dependency adds before accepting it.
- **Record sizes per release** so regressions are visible. *Example (shipped puzzle game):* universal
  APK 61.5 MB, AAB 63.6 MB, one-phone download ≈ 15 MB, iOS release app 35.6 MB.

## 11. Real-device profiling

> **Dated facts (as of 2026-10 — re-verify before relying):** Flutter's iOS simulator runs debug
> builds only (no profile mode), and an Android emulator renders with the host computer's GPU, so
> neither says anything about a low-tier phone; a plan that said "profile on the simulator" was wrong.

**Performance acceptance = CI frame-budget tests + a release or profile build with a frame-log flag,
run on the oldest supported device, numbers written into the doc.**

Profile these scenarios (adapt to the product):
- [ ] the most expensive themes or screens, at High;
- [ ] a theme crossfade (two full-screen shaders at once) and the dark-mode switch;
- [ ] the largest content with every accessibility option that adds drawing turned on;
- [ ] a 120 Hz display;
- [ ] a long session (≥ 20 min: precision, caches, heat);
- [ ] first launch after a fresh install;
- [ ] Low forced, to confirm it really is cheaper.

Until device numbers exist, rank costs with a relative proxy (software-rasteriser ms per frame per
theme), labelled "not a GPU figure". If the owner holds the devices, each scenario becomes an item on
the owner's device list (`references/working-with-the-owner.md`):
`<Area>: on <oldest supported device>, with <flag or tool>: <scenario>; pass = <observable result>;
write the numbers in <doc §>.`

## 12. The profiling log

Build the frame log into the app behind a compile-time flag (proven dead in release:
`references/architecture.md` §12.2). Feed it the engine's per-frame timings (only rendered frames are
reported, so idle time prints nothing). Print one line per 5 s window, nearest-rank percentiles,
prefixed with the quality tier and scenario:

```
[high crossfade] frames n=291 in 5.0 s | build ms p50 3.2 p90 5.1 p99 8.7 max 12.4 | raster ms p50 7.9 p90 11.2 p99 17.0 max 21.3 | over 16.7 ms: 4 (1.4%)
```
(Numbers illustrative.) A window closes on the first frame that starts ≥ 5 s after it opened.

Record each run as a row in the design or progress doc:

| Date | Device (model, OS, Hz) | Build (mode, commit) | Scenario | Quality | Build p50/p90/p99/max | Raster p50/p90/p99/max | Over % | Verdict → action |
|---|---|---|---|---|---|---|---|---|

Read it like this: p90 inside budget at High on the oldest device means keep the look. A sustained
over-budget share above the trip threshold means Auto must have tripped: check it did and Low then fits.
A p99 or max spike at one moment is a hitch to hunt (first use of an asset, a bake, a layout pass), not
a reason to degrade. Re-tune provisional thresholds from these rows; record the change as a decision.

## 13. Checklist

Per slice that touches rendering or motion:
- [ ] Each new painter has a Cost line, a paint test, a bounds test and a draw-count budget.
- [ ] The frame-budget test covers the new moment at both qualities, and was seen to fail.
- [ ] New moving things sit on their own layer; nothing ticks while idle; motion off starts no presentation ticker.
- [ ] No blur on anything that repaints every frame; every dear effect has a designed low form.
- [ ] Nothing allocates or lays out text per frame; particles come from the pool.
- [ ] Shaders: preloaded, bounded, uniform table pinned, portable edges, verified on each GPU backend.
- [ ] Startup: new assets warmed or deferred on purpose; cold start re-measured if the path changed.
- [ ] The scenario is on the device-profiling list, with the oldest supported device named.
