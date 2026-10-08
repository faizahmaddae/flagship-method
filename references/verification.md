# Verification

How to make "it is green" mean something: the doctrine, the anatomy of a guard that cannot lie,
the test shapes that found real defects, the mutation-proof protocol, the adversarial review
protocol and the cold-launch rule. Stack-neutral; mechanics live in `references/stack-flutter.md`
and `references/stack-other.md`.

**Read when:** writing any test, guard, lint or check script; reviewing anyone's work, including
your own; before calling a slice done; whenever a suite went green faster than you expected.

## Contents
1. The doctrine
2. Anatomy of a guard that cannot lie
3. Assert the right thing
4. Cover the whole variant space
5. Fakes, seams and adapters
6. Rendered output: raster, pixel and bounds guards
7. Whole-product tests
8. Cold launch: run the real thing
9. Mutation proofs
10. Adversarial review
11. What this does not prove
12. Shell-gate and tooling hygiene
13. Verification checklist

---

## 1. The doctrine

**A guard counts only once it has been seen to fail.** Remove the fix or the feature, watch the
guard go red with a message that names the fault, then restore. A guard that cannot fail looks
exactly like one that passes.

*Why:* in the source project, roughly a third of the logged traps were tests that passed while the
thing they guarded was broken or removed. Adversarial reviews run after self-tested lanes still
found 4–27 real defects per slice, and first mutation runs had survivors in at least four slices.
The worst defects (pending purchases granted, a release check that could not fire, an age fallback
on the unsafe side) came from that review-and-mutation tail, not from the first suite. Budget the
tail as a fixed, non-optional part of every slice.

Four layers of evidence, each blind where another sees:

| Layer | Catches | Blind to |
|---|---|---|
| Guards and tests (§2–7) | regressions of what you thought to doubt | what you did not think of; their own vacuity |
| Mutation proofs (§9) | guards that cannot fail | defects no guard aims at |
| Adversarial review (§10) | wrong assumptions, missing cases, seams | what nobody runs |
| Running and looking (§8; `references/visual-design.md` §Look loop) | startup, the shipped artefact, feel, ugliness | what the run did not touch |

Three corollaries hold everywhere:
1. **Check the thing that ships:** the real source tree, the shipped data, the built artefact, the
   release build on a device. Never a proxy, a model of the output, or a test-only path.
2. **Judge by the rules, never by a stored answer.** A rules judge accepts every valid answer and
   cannot be broken by a stored-answer bug.
3. **Read the output as its audience meets it.** Assertions only check what you already doubted.
   *Example (shipped puzzle game):* 2,027 generated boards were proven unique and valid, yet reading
   levels 1–20 as a player found one whose numbers sat in a straight row and "looked like a
   barcode". It became a rule in the generator and in both verifiers.

Most verification faults were checks pointed at the wrong thing: an adjacent claim, the wrong units,
the wrong parent, the wrong font, absence of effect, a tautology, two guards on one rule. Sections
2–6 are the counter-measures.

---

## 2. Anatomy of a guard that cannot lie

1. **Parse the real target; never regex raw text.** Tokenise code (line, block, nested and doc
   comments; every string form; interpolation; adjacent-literal concatenation); strip config
   comments, respecting quotes, before matching keys; read plists, manifests and XML with their own
   parsers. *Why:* a regex guard banning a UI library was wrong both ways: a comment in the
   dependency manifest once satisfied it, and a doc comment later tripped it.
2. **Refuse to guess.** An unterminated string, a directive without its terminator, an unreadable
   file: report "the guard cannot read this file and will not guess" as a violation naming the line.
3. **Prove it ran on something (anti-vacuity).** Before trusting "zero violations", assert the scan
   saw real input: a non-empty file list, directives found > 0, the parsed doc table's expected row
   keys, a known key in the real config, a pruning rule that changed the result at least once ("the
   cut rule never changed a node count: is it on?"), a label walk that found ≥ 10. A parser that
   finds nothing reports green forever.
4. **Ship a test of the test:** a **must-catch** list covering every syntactic or structural shape
   (both quote styles, multi-line, aliases, re-exports, conditional forms, split literals) and a
   **must-ignore** list of near misses (comments, strings that mention the pattern, identifiers
   named like keywords, look-alike words). Assert exact counts and message contents.
   *Example (shipped puzzle game):* the banned-words scan of player-facing strings had 17 must-catch
   cases, including a phrase split across two adjacent literals and one beside an interpolation,
   and 16 must-ignore cases, including package names and longer words containing a banned word.
   *Incident:* a "nothing left to fill" check knew one of a kit's two marker forms and reported a
   kit that was still mostly template as finished. A must-catch case per form, and a must-ignore
   case for the check's own command line, would have failed it (`references/traps.md` T-38a).
5. **A negative control must fail for its own reason.** Require the failure message to contain that
   rule's text. Drive selftests from a table of `(label, input, expected_substring | None)` and
   report three outcomes: expected pass but failed; expected failure but passed; failed, but not for
   the expected reason. A fixture that fails on a typo or another rule proves nothing.
   *Example (shipped puzzle game):* the level verifier's controls were 24 corruptions of one valid
   level (a move off the grid, a wall on the route, a middle number removed so two solutions exist,
   a bool where an int belongs …), plus one built so that only the "decorative wall" rule could
   fire: after adding the wall it recomputed every other derived field.
6. **Two guards on one claim make a negative control lie.** Deleting either stays green because the
   other still fails the input, or the control fails for the other guard's reason. Neutralise the
   other guard in the fixture, or test the rule where it is owned. *Example:* a duplicate puzzle
   always duplicates its route, so the route-dedup control first "worked" only via the puzzle dedup.
7. **No unused fixtures.** Record every fixture a selftest opens; fail if the folder holds one no
   case used. An orphan is a rule someone believes is covered.
8. **Messages that tell the fix:**
   `path:line  <offending thing>  breaks <RULE-ID>: <why>; allowed: <list>; fix: <how>`. Over
   content, collect every offender and fail once with the count and the first 25, each labelled
   ("level 37: …", "day 412 (2027-12-19): …").
9. **No silent skips.** Every "OK here" path is a named flag (`--allow-stale`) that prints "allowed
   explicitly"; the default is fail. A gate that cannot run (missing tool, no device, several
   devices and no serial) fails with the fix. A stub for a step whose input is not yet ported fails
   loudly once that input appears.

Guard checklist (every guard, test, lint and script check):
- [ ] Reads the real target, parses structure; unreadable input is a violation.
- [ ] Anti-vacuity assertion; must-catch and must-ignore lists; no unused fixtures.
- [ ] Every negative fails for its own reason (message substring asserted).
- [ ] Run by the main suite; selftest cases asserted by name (§7.4).
- [ ] Mutation-reviewed: name the one-line weakening that would still pass; add the case that
      kills it.
- [ ] Message names file:line, the thing, the rule, what is allowed, the fix; cannot be skipped by
      being unable to run.

---

## 3. Assert the right thing

Name the property, then measure exactly that property.

1. **Literal spec numbers, never the constant under test.** `expect(scale, 0.96)`, not
   `expect(scale, Press.scale)`: a test that loops over the constant it guards cannot fail on it.
   Copy the number from the design doc, or parse the doc (§7.3). *Incident:* "the mutation survived:
   the test derived its band from the constant itself"; pinned to literal rows, removing the band
   failed it. Installers too: a selftest comparing the installed tree with the installer's own
   constants cannot see a wrong constant (a consent default set to granted, or never written).
2. **Re-implement the rule independently in the test.** Never import the generator's helper to check
   the generator; write the rule fresh and say so in a comment. A shared helper means a shared bug
   passes both. *Incident:* a builder that compared aggregates shipped a "big" level that was not
   bigger or harder than a same-size regular one; the per-pair rule in the test caught it. Compare
   pairwise, never by aggregate.
3. **Assert the claim, not its neighbour.** *Example (sorting game):* "the Play button has the
   largest area" was false (it dominates by colour and type size); "is the text there?" measured a
   19 px label, not the tap target; "is it in the tree?" passed zero-opacity cards and lazily
   unbuilt list items; a guard checked a horizontal row when the bug existed only under bounded
   width. Measure the box a finger hits, the rendered opacity, whether text exceeded its lines,
   whether rects intersect, inside the parent the component really lives in.
4. **Check in the units the failure happens in:** pixels, points, glyph ink, milliseconds. Relative
   bars when the fault scales, absolute when it does not. *Incident (sorting game):* an overhang
   check allowed 0.6 × the item's width, so the tolerance grew with the thing it bounded and an item
   hanging 73 pt off a 430 pt phone passed. The reverse: a fixed 1.2 pt alignment bar sat under both
   residual and fault on small text; it became `max(0.7, 0.09 × fontSize)`.
5. **Assert magnitude and shape, not presence.** "Does something happen near T?" passes on any small
   event. An overlap check that accepted any graze passed an overlay 90% off the picture; measure
   how far in, against an independent search rather than the rule's own formula. Assert what should
   happen: a test whose only assertion was "no effect" passed a tap that landed off the test surface.
6. **Shape the detector to the defect's signature.** A rim light is a line, brighter than *both*
   sides, not merely a step. A seam check 2.5 px either side of an edge cannot see a lobe 0.09 H
   deep; guard how far the blend reaches. A shadow guard needs a narrow band at the edge (1.5 px,
   not 7 px), or the part's own gradient swamps it.
7. **Measure before you guard.** Take an element's real extent from its rendered pixels, in its
   largest variant, and pin it in a paint test. *Incident:* a guard guessed the mascot reached 0.85
   cell above its cell; in its tallest hat it reached 0.37, and the guess had pushed every corner
   badge into the sky.
8. **Guard the observable output, not a model of it.** A gait model that "never slides" still
   painted sliding feet; the guard moved to the painted feet plus a pixel cross-check. A clamp on an
   overshoot curve froze the rest state at 1.2×: test the output at rest.
9. **One scenario per term of a compound condition.** For `a || b || c`, one test where only `a`
   holds, one where only `b` holds, and so on. *Incident:* every offer test began with the reveal
   idle, so the reveal term of a "busy" check could be deleted green. Every status a failure can
   produce needs a test that produces it (forcing sync status "on" survived until a test produced a
   refused write). Early-return verdicts get one test per branch, everything else eligible.
10. **Inputs that differ only in the field under test.** A save-equality test that also changed the
    counters could not see equality ignoring the ledger; build documents differing only in the ledger.
11. **Version tests relative to the current version.** "Newer is refused" uses `current + 1`; one
    built from a literal version became valid at the next bump and stopped failing. "Older migrates"
    gets its own builder that strips newer keys.
12. **A removed timeout must fail fast, as an assertion.** Inject a short bound, use real time where
    no fake clock exists, and wrap the await in a test-level timeout whose handler calls `fail`;
    otherwise removing the bound gives only a slow, confusing harness timeout. Advance fake time in
    steps shorter than every other timer, and assert before letting animations settle (a settle has
    already spent the fake time).
13. **Define "idle" by the precise runtime signal** (no running animation, no pending frame
    callbacks), not "no frame scheduled": an accessibility rebuild schedules a frame with no motion.
14. **Read the mutated line under the test.** Confirm the test executes it. One gate mutation hit a
    path its test never ran; the real evidence was a failure elsewhere.

---

## 4. Cover the whole variant space

A guard's case list is its blind spot. Enumerate the axes the product really varies and loop over
all of them; tests are cheap next to a missed variant.

- **Every content item, not a sample.** *Example (shipped puzzle game):* a share card's badge
  covered the mascot on 10 campaign levels and 99 dailies, invisible in three previews; a panel
  badge rested ~90% above the picture on 705 boards. 2,027 boards were proven in about a second, so
  sampling has no excuse.
- **Every pose and parameter corner.** Read where the product sets each control; paint every value
  it uses plus the min/max corners. The celebration drew a side view with raised ears that no guard
  pose covered; the fixed guard painted 22 poses (every lift × turn corner, the run's leap and
  landing).
- **The branch real data never reaches.** If a guard runs only over shipped data, check some input
  reaches the guarded branch; if none does, add a synthetic one and see it fail. A card-height
  shrink loop was wrong only on narrow phones that no shipped board reached; a synthetic narrow
  phone proved the guard. Boards of ≤ 63 cells never touch a cache key's high word.
- **Shapes that hide stride bugs.** Square-only fixtures hid a transposed stride in a symmetry
  routine; always include non-square cases in geometry tests.
- **The longest copy at the largest text.** A 2× look at the shortest string proves nothing about
  the longest; one card hid both its buttons at 2×.
- **Every theme after any tint change.** A per-theme fix sank another theme.
- **Every day, not known dates.** A habit tracker's solar-calendar conversion matched four known
  new-year dates while a day-by-day probe found 98 breaks, all at 1 January (the wrong year's leap
  flag). Prove date code over every day of a wide range against an independent implementation, in
  several time zones (`references/ux-and-accessibility.md` §Localisation).

**The device matrix** varies what people change, not only the window: "a matrix that only varies
width and height is a window matrix." Its axes are the look matrix's (canonical:
`references/visual-design.md` §13.1), run by tests instead of eyes, extended with what only a
machine checks cheaply: real safe-area insets, every size when tablets ship, and text beyond 2×.

| Axis | Values that found defects |
|---|---|
| Size | the smallest supported phone and a standard one (~360×780 and ~390×844 at minimum); ~6 sizes if tablets ship |
| Text scale | 1, ~1.3 (largest standard), 2 (large accessibility), with the longest copy; up to 3 where the platform goes |
| Theme | every palette or theme, in every lighting the product ships |
| Locale and direction | every shipped language and script direction; for right-to-left, a rendered-tree test failing on any visible untranslated word |
| States | empty, one, full, busy, failed |
| Safe areas | real insets on the view (cards slid under the home indicator in tests without them) |
| Motion | On and Off; outcomes identical for the same input (Off removes presentation motion only; motion that is the task continues) |

Matrix rules:
- Fail on any caught layout error, truncation, overlap or off-screen control. Overflows are caught
  errors: "nothing fails, nobody finds out until a screenshot arrives from a device nobody owns".
- Measure the drawn size, not the configured scale. A shrink-to-fit box left the text scaler at 2
  and drew glyphs at 1.05× (elsewhere 0.52×); the audit now checks the painted transform's height
  ratio is 1 ± 0.01.
- Add every new screen to the matrix in the same commit. Decide layouts by measuring labels, never
  by width thresholds: one chosen on a 440 pt preview never fired on a 390 pt phone for three weeks.
- The matrix answers "does it fit?"; "too much room" and "in the right place" still need eyes.

Accessibility audit rules (labels, roles, real 44 pt touch found by hit-testing, traversal order):
`references/ux-and-accessibility.md` §9–10 and §18.

---

## 5. Fakes, seams and adapters

1. **Every fake at least as hostile as the real dependency.** Each line is an escape that happened:
   - a fake answering every call at once proved no timeout; six bounds could be deleted green. Give
     the fake a gate that holds every bounded call, and assert the operation ends within its bound;
   - a fake showing an ad synchronously hid the window between ask and show (the real service first
     awaited a mute, up to 2 s);
   - a fake that stayed "ready" through its own show hid a screen going quiet mid-reward. Drop
     readiness while showing, as the real SDK does;
   - a fake counting the *call* could not see the window inside a fetch-then-show call;
   - a fake transaction without the platform's own flags made the service "complete" a restore the
     real plugin never asks to complete; a fake that only sent the real product id missed the
     empty-id purchase one store sends on cancel. Build real data shapes, read from the plugin's
     source or captured on a device;
   - a fake priced like the real store could not catch a hard-coded price. Use distinctive values
     nobody would type, no two alike ("5,49 €", "2,29 €", "5,79 €");
   - real dependencies answer late, fail, and change state during a call; fakes must too.
2. **Fakes at a seam hide the adapter under it.** Test each shipped adapter directly against a strict
   stand-in for the SDK that fails on any call it may not make, overriding only the allowed calls;
   save and restore real global hooks (error handlers) around the test. *Incident:* with every
   service test green, the analytics and crash adapters could grant ad storage, enable collection in
   debug, drop the fatal flag or lose the previous error handler; 4 of 10 adapter mutants survived
   until the adapters had their own tests.
3. **One construction path.** Tests that build a component through another constructor prove
   nothing about production. *Incident:* the ad service built its own consent gateway whenever a
   test passed a delay, so the app's real initialisation arguments never ran in any test. One
   factory; a composition test that builds the real app graph (native bridges stubbed) and pins
   the startup order; a test seam used only when a test supplies it.
4. **Debug-only switches never reach a release:** compile three ways
   (`references/release-and-store.md` §1.4).
5. **Isolate automated runs from real accounts.** Simulator preview recordings ran the real cloud
   mirror and wrote a save into the owner's account. Fakes or isolated accounts; disclose any side
   effect (`references/working-with-the-owner.md`).

---

## 6. Rendered output: raster, pixel and bounds guards

The look loop lives in `references/visual-design.md` §Look loop; this section is its machine half,
guards that hold what the eyes found. Thresholds come from the project's own `docs/<slug>/DESIGN.md`;
the numbers below illustrate the method. Mechanics: `references/stack-flutter.md` §9.

1. **Every drawing routine gets a test that paints it and reads pixels back.** "Did it throw?" is not
   a paint test: a three-colour gradient with no stops passed analysis and every maths check and
   threw on the first device frame; a lid swung outside its box over a heading while every paint
   test passed. Sample pixels at positions derived from the design's proportions and assert
   relationships. *Example (shipped puzzle game):* rim darker than fill by > 30 luma, gloss lighter
   by > 15, ≥ 3:1 against the tile's darker stop, shadow below not above; an early cell keeps its
   colour (±2/255) as the path grows, which caught colour computed from cells drawn so far instead
   of the whole board.
2. **A paint test proves a routine runs, not that it draws the right thing.** Assert geometry: a
   "star" with inner ratio 0.942 was a 16-gon for four phases; the pentagram's 0.381966 proved the
   fix. Derive dependent geometry from its source; never type it twice.
3. **The pixel-guard protocol** (each step answers an incident):
   - compare with the same render *without the feature* (a test-only switch), not a palette rule: a
     "≥ 3:1 line across every wall" guard was met by the gutter between tiles and passed with every
     wall removed;
   - look in the region only this feature changes: a far-edge light was hidden by another element
     moving pixels on that side;
   - crop to what a person compares: greyscale over a whole strip diluted a mark that was 0.45% of
     it;
   - use a mean difference *and* a count of changed pixels: a prop moved 15 pt stayed under a
     0.25/255 mean;
   - paint the background over the whole integer image and assert every pixel opaque: premultiplied
     edge pixels over a fractional box gave ~300 near-black "legible" pixels and the control passed;
   - render at the real device pixel ratio: a 1× canvas made a 0.8 pt outline look absent.
4. **Bounds ring tests.** Drawing surfaces usually do not clip. Render every state and pose on a
   larger canvas with a transparent ring (24 px works); fail on any pixel outside the documented
   box, and assert the box is tight (layout budgets depend on it). A routine that clips itself makes
   a bounds sweep unable to fail: check its outer pixel ring instead. Sample motion densely (a
   thrown object wholly outside at its peak touches no edge); do not trust rectangles around arcs
   (99 stray pixels escaped through a rounded corner); assert save/restore balance.
5. **Never by hue alone:** compare each pair of states a person must tell apart as luminance
   (`references/visual-design.md` §5.5).
6. **Contrast as the screen shows it:** 8-bit quantised, then linearised
   (`references/visual-design.md` §5.2). Parse the design doc's contrast table in a test and hold
   each figure to ±0.01; unquantised maths drifted (3.69 vs 3.71:1).
7. **Hashes and goldens.** If a change must leave an output byte-identical, hash it *before* writing
   code; afterwards there is nothing to compare against. *Example:* a night variant was added to a
   background shader with the day frames byte-identical against hashes taken first. Know where every
   pin lives (one outside the render tests folder surprised a deliberate change); re-pin only on a
   deliberate change and say so; on a renderer upgrade, regenerate and look, or use a CI tolerance.
   A hash proves "unchanged", not "right": also test the purpose (the filter removes rumble; the
   overlay covers nothing).
8. **Glyph check ("tofu").** Rasterise two different glyphs per bundled face; identical output means
   the face is missing. Cover the script's unique letters; prove the bundled face is used, not the
   test fallback font.
9. **Frame analysis over time** for what no single frame shows: flashing. Record the busiest moment,
   count flashes per window over a sliding second, and carry a strobe control that must fail
   (Proposed; the rule and the method: `references/ux-and-accessibility.md` §Flashing and
   photosensitivity).

---

## 7. Whole-product tests

1. **Playthroughs by real gestures.** Drive the real app root through real screens with synthetic
   pointer events, across every content boundary to the end, in both motion settings; assert
   identical progress, saved state equal to in-memory state, and record per-item timings.
   - *Why:* caches and leaks fail only after many items. A cache that disposed everything when full
     disposed an image a caller still held, at level 30 of a 200-level run. The whole campaign by
     synthetic finger took ~60 s.
   - Vary the finger: steady (3 samples a cell), fast (1 a cell), a corners-only swipe, a sloppy
     thumb that rounds corners and lands low. Assert "a finger that follows the route never sees a
     refusal".
   - Pin cross-cutting policies end to end. *Example (shipped puzzle game):* levels 1–21 at 30 s a
     board show exactly one interstitial, at Next 20 → 21, motion on and off.
   - Tag long runs `slow`, but keep them in the default run before every commit.
2. **Model-based randomised tests** for saves, merges, ledgers, policies and any persistent state
   machine: thousands of random operations (2,000–5,000) against a simple model, clocks moving both
   ways; for sync, random multi-device histories through the real bookkeeping. *Example:* a join
   that was commutative but not associative made two simulated phones rewrite each other's documents
   for ever; "the random two-phone model test caught it; pairwise tests did not". A clock clamp
   saved from a merge looped only under skewed clocks.
3. **Docs parsed by tests.** Where a doc states a rule or number (the layer import table, contrast
   figures, a sound table, the store claims table), a test parses it and compares. The doc's format
   becomes an API: document it ("rows starting with a backticked id are cue rows; a later row
   wins"). The first run usually finds the doc wrong, which is the point: amend the doc, then the
   code. One source of truth across languages: an app-language test reads the generator's
   constants; one banned-word list serves every text.
4. **Tool selftests, wrapped by CI with named cases.** Every rule-enforcing script (privacy guard,
   copy checker, release verifier, installers, generators) has `--selftest`; the suite runs it and
   asserts each case line by name (`ok  <label>`) plus a summary (`selftest: 0 failure(s)`), so
   deleting a case turns the suite red.
   - Reach every step: each path the script reads is overridable by an environment variable;
     external tools are fakes on `PATH` printing fixtures in the real tool's format.
   - A `stderr:` expectation requires the substring where only the fail function writes, which
     catches a FAIL hidden behind an earlier step's FAIL.
   - Checkers over a tree: copy the tree per case, apply one edit at an anchor that must exist
     (abort if missing), require the specific failure; the unmodified copy must pass.
   - Pass in every repo state (config absent or present), skipping explicitly with a reason; write
     `strip` as the exact inverse of `install`, with a round-trip check.
5. **Determinism: build twice, compare bytes** — generators, setup scripts, icon and screenshot
   generators, in two processes, as a test (rules: `references/architecture.md` §9). A real-time
   simulation: the same seed and input log give the same state hash at every frame rate and through
   an injected hitch (`references/domain-games.md` §14.1).
6. **Natural negative controls.** Run a new validation rule on pre-change data first: it should fail
   on the known offenders. Regenerate, then check only the offenders changed. *Example:* "no
   straight run of ≥ 4 numbers" failed exactly 4 campaign levels, and only those 4 changed.
7. **Independent proofs for data you must never get wrong:** builder, independent verifier, and the
   app's own engine re-proving every shipped item in CI; two implementations compared by work
   counters (node counts), not answers, since weaker pruning still gets answers right
   (`references/architecture.md` §10).
8. **"Still a stub" tests invert at integration** into "no X is still a stub"; otherwise they fail
   the moment a lane does its job and guard nothing afterwards.
9. **Frame-budget tests** pin which painters repaint and which components rebuild in each moment:
   `references/performance.md` §2.

---

## 8. Cold launch: run the real thing

1. **Cold-launch the real entry point after every integration and every phase, and read the device
   log.** No UI test runs the real entry point. *Incident:* a runtime type error thrown before the
   first frame left the app on its launch screen while every test passed; only a cold launch showed
   it. A malformed backend config killed the app natively, before any app code ran. Add a guard
   test that a throwing or hanging initialisation still reaches the first frame
   (`references/architecture.md` §8).
2. **Prove liveness through the accessibility tree**, not a screenshot or process id: a launch
   screen identical to the first frame hides a dead app, and a platform may keep a crashed process
   warm. Wait (≤ 30 s) for a node only your UI publishes, such as the main button's label.
3. **Check endless motion is really live:** two device frames some seconds apart must differ.
4. **Separate tool behaviour from app behaviour before fixing anything.** A drawn path missed its
   last cell on the simulator; a variant with a held final sample showed the automation tool's
   lift-off injection was at fault. An apparently lost save was a reinstall with a fresh data
   container. Run a controlled variant first.
5. **Drive automation by accessibility labels, not pixels.** A layout change cannot move a label; an
   app playable by taps for screen readers doubles as the automation API.
6. **Test the artefact that ships, on the device class the reviewer uses:** static artefact verifier,
   then the run gate (fresh install of the release build, cold start, core flows, health after each
   stage, screenshots looked at). *Incident (sorting game):* a release-only code shrinker removed a
   constructor loaded by reflection, and every release build died before its first frame while
   analysis was clean and 605 tests green. A store reviewer used a tablet in phone-compatibility
   mode that nobody had launched. Procedures: `references/release-and-store.md` §2–3.
7. **When a store rejects, reproduce the rejection before believing any explanation.** Six
   investigators agreed on a cause with high confidence and were wrong; one release build on a
   simulator settled it.

---

## 9. Mutation proofs

"Seen to fail", applied systematically. Run it for every new guard in a slice, again in the review's
"do the tests prove anything?" lens (§10), and again on the final tree after the fixer pass.

**Protocol**
1. **Enumerate before you run.** A numbered, slice-specific list of 10–25 one-line weakenings, each a
   believable bug: a threshold off by one; `and` ↔ `or`; `>=` → `>`; a branch dropped; a bound
   removed; two steps swapped; a constant nudged; a stand-in put back; the two sides of a
   cross-check drifting apart. Write it before reading the tests, so it is not biased towards what
   they already catch.
2. **An isolated copy, never the shared tree.** Copy source, tests, assets, manifest and lockfile,
   lint config, the resolved dependency metadata (including any package graph the build tool reads)
   and local path packages, plus `.git` when a tool under test reads git; or `cp -R` the whole repo
   with uncommitted work, or use `git worktree`. Run tests offline there, with lane-unique scratch
   names. *Why:* parallel lanes share one tree, and a copy missing build metadata made every run
   error, which reads as "the mutation still passes".
3. **Apply by an exact, unique anchor:** the tool asserts the old text occurs exactly once before
   replacing it. *Incidents:* `sed` with the wrong indentation matched nothing, so the sabotage never
   applied and the test "passed"; a tool replaced the first of two identical mentions; a
   `git checkout -- <file>` during a control twice discarded a chapter of uncommitted work (commit or
   copy first).
4. **Classify by exit status and failure type:** killed by assertion, compile error, survived,
   timeout. Only assertion kills count; a compile error proves nothing. Never classify by grepping
   output: a classifier grepping "Error: " counted an assertion that threw an "unimplemented" error
   as a compile error.
5. **Investigate every survivor.** It is one of:
   - **a weak test:** write the case that kills it (inputs differing only in the mutated field, a
     hostile fake, the missing branch scenario) and rerun;
   - **masked by a second guard on the same rule** (a first mutation "lied: the presenter re-checks
     after the frame"): neutralise the other guard, or test at the owning level;
   - **hidden by a fallback:** mutate the function's result, not one input (a theme removed from a
     puzzle was still found through the level id);
   - **equivalent** (nothing observable changes): explain why, and show a sibling mutation failing.
6. **Rerun the whole list on a fresh copy of the final tree** after the fixer pass.
7. **Keep the harness and logs** in scratch and report one line: "k of n killed by assertion, none a
   compile error; survivors: …, each fixed or explained."

Harness shape (any language):
```
mkcopy <dest>      # repo + dependency metadata + path packages (+ .git if needed);
                   # first prove the unmutated suite passes there
mutations = [ (id, file, exact_old_text, new_text, test_command), ... ]
for m in mutations:
    fresh copy (or revert the previous mutation)
    assert count(exact_old_text in file) == 1; apply
    run test_command with a timeout; save output to logs/<id>.txt
    outcome = assertion | compile | survived | timeout   # by exit status and failure type
print per-id outcome and failing test name; totals; survivors
```

Example mutation lists (shipped puzzle game, generalised):
- **Ad policy:** first-ad threshold 20 → 19; `and` → `or` between two first-ad conditions; minimum
  gap 150 s → 149 s; session cap 4 → 5; an hourly cap in fixed buckets instead of sliding; a
  rewarded ad not counted in the gap; a failed show recorded as shown; a future timestamp not
  clamped; background time counted; the verdict computed after an early return; a decoder that
  accepts a newer version.
- **Purchases:** a consumable granted twice on redelivery; completion before the grant is persisted;
  a pending purchase granted; restore grants consumables; "unknown entitlement" treated as a
  non-buyer; a hard-coded price; a plugin call without a timeout.
- **Sync merge:** remote time instead of the minimum; a local-only item dropped; counters added
  instead of joined; a newer document overwritten; no debounce; a failure blocking the local save.
- **Sound:** a theme mapped to the wrong cue; a stand-in cue put back; a cue 6 dB louder; a
  high-pass removed; a button's press cue removed; a render material changed without its sound rule.
- **Store copy:** a banned word in each text source; a length limit exceeded; a caption drifting
  from its source; a URL constant drifting from the docs; a cap raised under copy that states it.

Reference numbers: 4–61 mutations per stage (most slices 30–50) and 7–31 per fixer pass. First runs
had survivors in at least four slices, each a weak test: counters changed along with the ledger;
two guards held one rule; an await had no bound; the adapters had no tests.

---

## 10. Adversarial review

Mandatory roles, whether run as agents (prompts, schemas, topologies: `references/orchestration.md`)
or alone (`references/orchestration.md` §11, Solo fallback).

**When.** Every slice; never skipped for money, saved data, lifecycle, endless motion, release or
store text, or your own redesigns. *Why (word game):* an author who "had been both its designer and
its only reviewer and had judged it by looking at two screenshots" shipped faults. A five-critic
review raised 27 findings, refuted 5 and kept 22; two were introduced hours earlier (money buttons
shrunk to 36–38 pt, ornaments painted off the panel).

**Non-authors, one lens each.** Choose three lenses from how *this* slice can fail. One is always
**"do the tests prove anything?"**, carrying the enumerated mutation list (§9). Lens sets that found
what a generic reviewer missed:

| Slice | Lenses |
|---|---|
| Sound | audio quality against the spec · wiring and behaviour · do the tests prove anything |
| Ads foundation | policy and platform · wiring, lifecycle, concurrency · mutations |
| Purchases | store correctness · visuals, copy, accessibility · mutations |
| Cloud sync | policy and legal · data safety · mutations |
| Release | release readiness · visuals · mutations |
| Store prep | truth and compliance · visuals · do the guards prove anything |
| Character redraw | the character · accessories, dark mode, every screen · guards and derived assets |

A lens names its scenarios. Data safety's brief: "try to make the mirror lose or corrupt progress"
(two devices racing, a reinstall, a newer document, a corrupt value, the size limit, an account
switch, a debounce dropping the last write). For audits, sweep once by screen and once by state and
sequence: "a screen-by-screen pass structurally misses what happens between two screens that are
each fine".

**Reviewer rules**
1. Take the builder's report and the original task; do not trust the report.
2. Verify by reading and running; re-render images and re-measure numbers (a 300 ms skip, a contrast
   figure) yourself.
3. Edit nothing in the shared tree; mutate only in an isolated copy.
4. Every finding carries evidence: command output, a measured number, or `file:line`.
5. Few strong findings; no style nits; an empty list is valid when the work is solid.
6. Severity: **high** = data loss, money, crash, policy rejection, a guard that cannot fail on a
   core rule; **medium** = wrong behaviour a user meets, a visual fault against the design doc, a
   stated rule with no test; **low** = cheap polish.
7. Check that the docs say only true things about the code.
8. Testers confirm the build flavour first (a release build without the QA menu wasted a session).

**Triage.** Actionable = high + medium; lows go to the fixer as "fix the cheap, clearly right ones";
an empty review skips the fix stage. Dispositions: fixed with a guard; answered by a recorded
decision; left for a named device check; doc amendment. "All real" is valid, after each finding is
verified.

**Fixer.** Verify each finding first (reproduce, measure or read). If false or not worth changing,
push back with evidence. If real, fix at the root with a guard that fails without the fix (proved in
an isolated copy), re-look at changed visuals, update docs the fix made stale, rerun everything.
Return per finding: verdict, change, guard, proof. Audits overrule polish: a no-break space added
for nicer wrapping made "40 hints" wider than its tile at 2× text, and was reverted.

**Checker (edits nothing)** reruns everything from scratch and returns a short plain report:
- [ ] Analyzer and full suite with exact counts and failures verbatim; a lone failure rerun alone to
      tell flakiness from a defect.
- [ ] Every tool selftest and content verifier.
- [ ] `git diff --check`; `git status` for stray files, secrets, fake config, a present ignored env
      file, build output.
- [ ] The diff skimmed for TODOs, debug prints, placeholders, banned imports and words, hard-coded
      prices, production ids, personal data.
- [ ] Every new image opened, one-line verdict each.

**Lead.** Rerun the suite; read the fixer's verdicts and diff; look at the images; cold-launch on
device targets; fix residual nits, each with a guard seen to fail; check docs against code; update
the handoff; commit one slice. The lead's own pass still found a purchase confirmed while its grant
existed only in memory (after a failed save and a redelivery).

*Reference counts (shipped puzzle game):* one combined review of the research and the kit drafted
from it raised 82 findings (71 confirmed, all addressed); slices raised 4–27 each (a character
painter 2 high + 5 medium; the play loop 8 medium + 11 low; the first full loop 26: 22 fixed, 2 left
for a device check, 2 doc amendments).

---

## 11. What this does not prove

Every gate, results block and prototype states its blind spots beside its result.
- **Per gate:** a "what a pass does not prove" section in its doc ("the preview check verifies the
  file's format, not what it shows"; "the first launch of a release build on <platform> is the
  owner's device; no tool here could start one").
- **Per results block:** end with "Not run / not verified:"; when a gate was not rerun, give a
  checkable reason ("no native or dependency change (diffed), so setup and device builds stand").
- **Per prototype or probe:** three lists: proved (by running); found by looking (would have shipped
  otherwise); not proved (needs a device or a human sense).
- **Accumulate** the not-proved items in PROGRESS's "Device checks" section (the template), which
  becomes the owner's end-of-project device-check list (real-phone frame timings, feel in motion,
  sound on a phone speaker, the audio session after a full-screen ad, consent and sandbox purchases,
  sync between two devices, the screen reader). Make each runnable as written, adding a release-dead
  debug switch where the real trigger is unreachable (a minor's account, a consent region). How the
  owner gets it: `references/working-with-the-owner.md` §12.

Template:
```
### Results (<date>, HEAD <hash>)
- <gate>: <command> → <exact result and counts>
- Mutations: k/n killed by assertion, none a compile error; survivors: <fixed/explained>
- Looked at: <files> — look 1: <fault>; look 2: <fault>; look 3: accepted
- Not run / not verified: <item> — <why> — <who checks it, when>
- What a pass here does not prove: <blind spots>
```

---

## 12. Shell-gate and tooling hygiene

Gate scripts decide releases. Each trap below made a check fail exactly when the answer was yes, or
pass without running.
1. **`cmd | grep -q` under `set -o pipefail`** reports a match as a miss: `grep -q` exits on the first
   match, the writer gets SIGPIPE, the pipeline fails. It failed this way on a real release artefact
   the first time. Read output into a variable, then `grep -q … <<< "$var"`.
2. **`set -e` plus a command that exits non-zero when it finds nothing** (`pid="$(… pidof …)"`) ends
   the script silently. Add `|| true` and comment it as load-bearing.
3. **bash 3.2 under `set -u`** read `$NAME»` as an unbound variable when a UTF-8 locale was exported:
   brace `${NAME}` next to non-ASCII. It also mis-parses an apostrophe in a quoted heredoc inside
   `$( )`.
4. **zsh does not word-split `$VAR`;** a loop wrote garbage into a source file. Run such loops in
   bash.
5. **`rsync --exclude ios`** excludes every directory of that name; anchor it (`/ios`).
6. **Python `s[s.index(a):s.index(b)]` with `b` before `a`** is empty, and `replace('', x)` then
   inserts `x` between every character (a whole file mangled). Find `b` after `a`; assert the slice
   is non-empty.
7. **Python `False == 0`** in structure compares: tag booleans by type before comparing config.
8. **Never `source` an env file;** it executes data. Parse it.
9. **Edit by structure, not old value.** A `sed` matching an old value silently stops matching after
   a rename. Ask the build system for effective settings (inheritance included); check build-phase
   membership, not file presence.
10. **Read binary formats with their own tools;** bytes that "agreed" with any version were a
    constant.
11. **Invert a check when the bad value is always present.** A library's test ids are compiled into
    every build, so "is the sample id absent?" cannot work; check every production id is present.
12. **Filter device logs by your own process id;** the automation tool's own error lines look like
    yours.
13. **Formatters and globs touch other people's files;** format an explicit list of files you
    changed.

---

## 13. Verification checklist

Per slice, on top of the definition of done in `references/planning-and-slices.md` §6, in pipeline
order:
- [ ] Every new guard seen to fail for its own reason, fix removed, in an isolated copy, by
      assertion; anti-vacuity, must-catch and must-ignore cases present.
- [ ] Expected values are literals or parsed from the spec, never the constant under test.
- [ ] Guards loop over the whole variant space (content × themes × lightings shipped × sizes ×
      poses × text scales × locales and directions × states × motion).
- [ ] Fakes hold calls, drop readiness, use real shapes and distinctive values; adapters tested
      under the seam; one construction path.
- [ ] Every drawing routine painted and read back; bounds ring; pixel guards compare against the
      render without the feature.
- [ ] Playthrough by real gestures in both motion settings, if the slice touches a flow.
- [ ] Integrated build cold-launched, device log read, images looked at.
- [ ] Three-lens adversarial review; findings verified before fixing; a guard per fix.
- [ ] Mutation list (10–25) run; every survivor fixed or explained; rerun on the final tree.
- [ ] Checker green: every gate re-run, generators and setup twice and byte-identical, tool
      selftests run by the suite with cases by name; a confirming look; the lead's pass.
- [ ] Results block with exact counts and "not verified" / "does not prove" lines.

> **Dated facts (as of 2026-10 — re-verify before relying):** the incidents above involved these
> platform behaviours; check current official docs or the installed SDK source before designing
> around them.
> - One mobile store's restore marked pending purchases as restored, and the same store sent a
>   purchase update with an empty product id on cancel.
> - An ad SDK reported "not ready" while its own full-screen video was showing.
> - Release builds with a crash reporter attached did not print the engine's unhandled-exception
>   line, so the project's own handlers printed a unique marker line instead.
> - macOS still shipped bash 3.2 as `/bin/bash`.
