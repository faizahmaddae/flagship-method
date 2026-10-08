# PLAN — {{PROJECT_NAME}}

<!-- flagship-method template. The goal, the phases, what each must prove, and the owner gates.
Adapt the phases to the project, but keep the final-quality vertical slice, the gates and the
release approval. How to plan: flagship-method references/planning-and-slices.md; the doc's shape:
references/project-kit.md §10. A slot only a later phase can fill gets one line instead of a guess:
"Written in Phase <n.m>; decided so far: <…>" (references/project-kit.md §12). A criterion that does
not fit this product is never left as fixed text: write "none: <reason> (DECISIONS #n)". -->

## Goal (from kickoff, {{DATE}})

<!-- The kickoff goal sheet (flagship-method references/kickoff.md §12.1). An empty field becomes a
research question or an owner question, never a guess. -->

| Field | |
|---|---|
| One line | {{ONE_LINE}} |
| The owner's words (verbatim: original language, then translation) | [TODO: what they asked for, word for word] |
| For whom, and when or where they use it | [TODO: the users and their context] |
| Use pattern | [TODO: game, daily use, or episodic (name the trigger that opens it); it picks the gate question] |
| Platforms, device scope, regions, UI languages | {{PLATFORMS}}; [TODO: regions, UI languages, script direction] |
| The owner's country for store accounts and payouts | [TODO: the country, or ASSUMED until answered (RESEARCH "Legal and store eligibility")] |
| Money model (or none) | [TODO: the model, with the DECISIONS entry] |
| The gate question, in {{OWNER_LANGUAGE}} | [TODO: the wording for this product's use pattern, from flagship-method references/planning-and-slices.md §3] |
| Rejected before, and why (verbatim) | [TODO: the past rejection, and the bar questions it became; or "nothing recorded"] |
| Hard constraints and permanent bans | [TODO: e.g. budget, deadline, art provenance] |
| Existing accounts, packages, procedures, sister projects | [TODO: what exists, or "none"] |
| Release lever | [TODO: the irreversible public step], held by {{OWNER}}; every upload only on their request for that specific upload; nothing to review or the public before their device test and approval |
| Research answers | [TODO: what the research tracks settle] |
| Only {{OWNER}} can answer | the first question block below |

### First question block (as sent)

<!-- Paste the block exactly as sent, in the owner's language: at most five numbered items, each with
a recommendation (flagship-method references/kickoff.md §4). Research does not wait for it. Until an
answer arrives, its recommendation stands as an ASSUMED DECISIONS entry; when it arrives, note the
entry it became after the item. -->

Sent [TODO: date, channel, language]:

> [TODO: the block, verbatim]

## How this plan works

The plan is phased. **A phase is done only when every acceptance criterion has been verified by
running something** (tests, a render, a simulator, a script), never by reading code. Inside a phase,
ship small slices through the pipeline: plan written → skeptics → freeze contracts → build (≥ 3
looks on anything visible) → integrate (cold launch) → analyze + full suite → adversarial review →
fixer → mutation proofs → confirming look and every gate → docs → one commit.

**Profile and calendar:** [TODO: the full profile, or the small product profile with what merges
and what compresses (flagship-method references/planning-and-slices.md §1); the deadline mapped to
dates for Gate 0, the Phase 2 owner gate and the release gate, or "no deadline".]

**Order:**
- Phase 1 builds and proves the core.
- Phase 2 builds the first ~20 minutes of use **at final quality**, and {{OWNER}} judges it on their
  own device.
- Content, features and money scale only after a yes.

<!-- kind:game -->
**Notation:** [TODO: e.g. "sizes are written rows×cols everywhere (DECISIONS, header)".]
<!-- /kind:game -->
<!-- kind:app -->
**Notation:** [TODO: e.g. "money is an integer number of minor units everywhere (DECISIONS, header)".]
<!-- /kind:app -->

<!-- Per phase, keep these blocks: In the phase / Not in the phase / Checkpoint (only for risky
assets) / Accept when (runnable checks only, with numbers) / Gate prerequisites / Gate. Slices
inside a phase use In the slice / Not in the slice.
A criterion that proves wrong is struck, never deleted:
~~<old criterion>~~ **Corrected <YYYY-MM-DD> (DECISIONS #n):** <why it was wrong>. Instead: <new>.
Retrofit: Phase 0 becomes "Phase 0 — Adoption baseline, guards first" (flagship-method
references/planning-and-slices.md §10): a green baseline with a quarantine table; the layer guard
with LEGACY rows that may only shrink; characterization tests over flows and saves that must keep
working; the existing platform folders brought under the setup script (keep / adapt / drop, an id
check); secrets and sample ids out of the code. -->

---

## Phase 0 — Scaffold, guards first

### In the phase
1. **The dependency manifest, written by hand,** with only what Phase 0 uses. [TODO: the phase each
   later dependency arrives in, e.g. "audio and preferences in Phase 2; analytics and money SDKs in
   Phase 4".]
2. **The native setup script** (never the platform's bare project generator over the repo).
   [TODO: the script that regenerates the platform folders, or the written policy for committed
   native folders (flagship-method references/stack-other.md §15), or "none: <reason> (DECISIONS #n)"]
   [TODO: if it is ported from a sister project, a table: source step → keep / adapt / drop / move →
   phase. Steps that must always run move out of conditional blocks.]
3. **Fonts and design tokens** from DESIGN §2.
4. **Guard tests:** the architecture guard parsing ARCHITECTURE §1 (first); the banned-word guard;
   the font test (glyphs differ, no fallback boxes, every script the UI uses); a paint test and a
   bounds test for the first renderer.
5. **The render harness:** a test that paints screens to PNG in [TODO: a gitignored folder].
6. **One themed screen,** the entry point and the composition root.

### Not in the phase
No feature, no content and no screen beyond the one themed screen.

### Accept when
- Analysis is clean, and the full test suite is green, including the guard, paint, bounds and font
  tests, **each guard seen to fail** on a planted violation in an isolated copy.
- [TODO: "The setup script generates every platform, its own checks pass, and a second run is
  byte-identical", or the committed-folder policy's own check, or "none: <reason> (DECISIONS #n)"]
- The app runs on [TODO: simulator and emulator], cold-launched.
- The screenshot matches DESIGN §2 (looked at, three looks).

## Phase 1 — The core, proven

### In the phase
<!-- kind:game -->
1. [TODO: the pure core: rules, models, the judge (by the rules, never by a stored answer).]
2. [TODO: the content pipeline: an offline generator with `selftest`, `verify` and a `--review`
   mode, deterministic.]
3. [TODO: an independent verifier in the app's own tests, with parity over shared fixtures.]
<!-- /kind:game -->
<!-- kind:app -->
1. [TODO: the pure domain core: models, rules, and derived values (balances, totals, streaks)
   computed from stored facts.]
2. [TODO: the data layer: strict versioned saves and migrations, seed fixtures; for shared or
   server data, an operation log with idempotency keys (flagship-method references/domain-apps.md).]
3. [TODO: an independent check of the critical logic, e.g. a property test that conserves every
   cent over random groups, or a calendar conversion checked against a reference library.]
<!-- /kind:app -->
4. **Tests, listed before building:** every transition; every refusal; [TODO: edge cases such as
   time zones and daylight saving, the caps, a simulated year].

### Not in the phase
[TODO: e.g. "no new screen; the core runs in tests and behind the one themed screen only".]

### Accept when
<!-- kind:game -->
- Every shipped item is re-proven in the app's own tests.
- The review output has been *read* the way a player meets it, and items from every bucket look
  right.
- [TODO: a performance number, e.g. "verifying the whole pack takes under 60 s in tests".]
<!-- /kind:game -->
<!-- kind:app -->
- Every transition, refusal and migration has a test; the save reads every older version exactly
  and refuses a newer one.
- The seed fixtures load through the real data layer and read right to a user (rendered and looked
  at, not only asserted).
- [TODO: a performance number, e.g. "deriving a year of data takes under N ms in tests".]
<!-- /kind:app -->

## Phase 2 — Vertical slice at final quality → GATE

### In the slice
<!-- By area, concretely. Example areas: the main screen and its hero element; input and motion;
sound and haptics; the core screens; persistence; onboarding; the motion-off path; a quality
switch; accessibility basics. -->
| Area | In the slice | Not in the slice |
|---|---|---|
| [TODO: area] | [TODO: what is in] | [TODO: what is not] |

### Checkpoint (before wiring the risky asset)
[TODO: e.g. "Render the hero's pose sheet; look three times; compare it side by side with
<benchmark> at the same size. If it fails on any of <a, b, c> after three looks, follow DECISIONS #n
(plan B)."]

### Accept when
- The quality bar in DESIGN (the seven questions, the two edge checks and this project's extras) is
  answered "yes" in writing on [TODO: the core screens], across the look matrix (flagship-method
  references/visual-design.md §13.1) with this project's sizes, themes, lightings and locales.
<!-- kind:game -->
- The largest content renders and fits at both sizes.
- Every item in the slice is played through the real app by real gestures in a test, with motion on
  and off giving identical progress.
<!-- /kind:game -->
<!-- kind:app -->
- The longest real data (names, amounts, translated strings) renders and fits at both sizes and at
  2× text.
- Every core flow in the slice is driven end to end through the real app by real gestures in a
  test, with motion on and off giving identical stored data.
<!-- /kind:app -->
- Every renderer has a paint test and a bounds test.
- Frame budget: [TODO: this stack's form (flagship-method references/performance.md §2; other
  stacks: references/stack-other.md §7): a CI test that pins what each moment repaints or
  re-renders, where the stack has one; where it has none, a profiler run on a device, listed in
  PROGRESS "Device checks" (DECISIONS #n).] Frame timings come from a real device (the owner's
  device at the gate), recorded in PROGRESS.
- A skip shows the next action within 300 ms (a test).

### Gate prerequisites (asked early in {{OWNER_LANGUAGE}}, as one short list, marked non-blocking)
1. Which phone the owner will use, and whether a developer install on it is possible.
2. Confirm the name and the app id before any store record or upload. **They are permanent from the
   first upload.**
3. Create the store record (it reserves the name). It is slow, so ask early; a non-public gate build
   does not wait for it.
4. Register the domain and start trademark clearance (recommended; the gate does not wait for it).
<!-- If the owner may not be able to hold developer accounts or receive payouts in the target stores
(RESEARCH "Legal and store eligibility"), items 2 and 3 follow the alternative recorded in
DECISIONS. -->

### Gate
1. **Delivery, non-public by default:** [TODO: a cable or developer install on the owner's phone; or
   a locally built package they install; or, only without a suitable phone, a simulator recording].
   An upload of any kind, an internal test track included, happens only if {{OWNER}} explicitly asks
   for that specific upload.
2. **The one question** (the gate question in the Goal table), asked in {{OWNER_LANGUAGE}} after
   use on their own device.
3. **If the answer is no:** ask what felt wrong, in their words. Record it in DECISIONS, fix it, and
   re-gate.

**Nothing in Phase 3 starts before a yes**, unless {{OWNER}} relaxes this (record it in DECISIONS).

## Phase 3 — Breadth

### In the phase
[TODO: all content or every flow; every screen and feature; the second lighting, if any;
localisation; accessibility everywhere; sharing; stats. Split broad polish by concern (theme,
accessibility, social, polish).]

### Not in the phase
[TODO: e.g. "money, analytics, sync and accounts (Phase 4)".]

### Accept when
- The same quality bar holds on every screen across the whole look matrix (flagship-method
  references/visual-design.md §13.1).
<!-- kind:game -->
- Every content guard runs over every shipped item, every theme and both phone sizes.
- [TODO: the whole content played through by a test.]
<!-- /kind:game -->
<!-- kind:app -->
- Every data guard runs over every fixture, and every flow is driven end to end in a test.
- Network: [TODO: every flow also driven offline and with the server refusing a change; or "none:
  local-only (DECISIONS #n)".]
- [TODO: the accessibility and text-size audits over every screen.]
<!-- /kind:app -->

## Phase 4 — Money, services and hardening

<!-- Open the phase with the owner's few decision questions (e.g. "a tracking prompt, yes or no?").
One dependency group per slice. Risky integrations get readers → a designer → two skeptics →
numbered decisions and numbered tests before any code. -->

### In the phase
<!-- if:monetization -->
- [TODO: one slice per dependency group of the money model in MONETIZATION, e.g. consent and the
  policy foundation; each ad format; the paywall and the entitlement function; purchases and
  restore.]
<!-- /if:monetization -->
- [TODO: analytics and crash reporting together, if any (the privacy forms change once); sync or
  accounts, with in-app account deletion if accounts exist; age signals, if required.]
- [TODO: release hardening: the static release verifier and the run gate, each seen to fail.]

### Not in the phase
[TODO: e.g. "no new user-facing feature".]

### Accept when
<!-- if:monetization -->
- Every money rule is a named constant with a test that fails without it (MONETIZATION).
<!-- /if:monetization -->
- [TODO: each adapter is tested against a strict fake of its SDK; or "none: no SDKs (DECISIONS
  #n)".]
- Every platform await has a bound, and no timeout falls back to the unsafe side.
- The release build is installed fresh, cold-launched, used, and its log read.

## Phase 5 — Release preparation → the owner's device test → approval → upload

### In the phase
[TODO: the icon; store copy mapped to code; screenshots and preview from the real app; the privacy
policy and privacy answers; ratings; the review notes; the END-OF-PROJECT LIST reconciled.]
<!-- if:release -->
The store texts and their checks live in `docs/{{SLUG}}/store/` (RELEASE.md §8).
<!-- /if:release -->

### Not in the phase
No new user-facing feature, and no upload that {{OWNER}} has not explicitly asked for.

### Accept when
- The static gate and the run gate pass on the exact artefacts that will upload, except for the
  owner-only inputs.
- The store-copy checker passes: lengths, every claim mapped to code, one banned-word list, dormant
  features dated.
- The owner has tested the exact build on their own device and **explicitly approved**. Only then is
  anything submitted for review or released.
