---
name: flagship-method
description: A field-tested method and quality bar for building a premium, store-ready mobile game or app from idea to release. It covers understanding the goal, research, project identity, the project doc kit, architecture, verification that is proven to verify, visual design, motion and feel, sound, UX, localisation, accessibility, performance, honest monetization, privacy and release. Use it whenever someone wants to start, plan or scaffold a new app or game ("I want to build...", "let's make a game", "start a new app project", or in Persian "می‌خواهم یک اپ/بازی بسازم"), wants an app or game to reach a premium or polished bar, wants to adopt this method on an existing project, or continues a project whose repo has a docs/SLUG/PROGRESS.md and a SLUG-builder skill made by this method. Also use it to review a mobile build against a premium bar. Do not use it for unrelated one-off coding tasks.
---

# flagship-method: how to build something that feels finished

This is a working method, not a style guide. It was distilled from shipping three mobile games
with an AI builder and a demanding owner. One of them went from research to store-ready in a few
days of agent sessions, with 4,000+ tests, every guard proven to fail, and every screen looked at.
**What the owner valued was the whole path:**
- the goal understood correctly;
- decisions made from evidence and recorded;
- small, verified steps;
- details checked and fixed until the result felt different.

This skill makes that path repeatable for games and for apps, in any stack (deepest in Flutter).

**Contents:**
- The three directives
- Start here
- The lifecycle
- The session loop
- The slice pipeline
- The quality bar
- Non-negotiables
- Working with the owner
- Decide-and-record slots
- Reference map
- Scripts

## The three directives

1. **Put the high-quality thinking into the docs.** The next worker may be a smaller model, or
   you with no memory. A decision, number, trap or reason that lives only in a conversation is
   lost. The project's docs are the product's brain (`references/project-kit.md`).
2. **The product is judged by how it looks and feels.** A green test suite under programmer art
   is a failure, not a milestone. The owner sees only work at final quality.
3. **Every project finds its own identity.** This skill transfers the bar and the method, never
   a look. Derive each project's look, motion, sound and voice from its audience, its category
   and its competitors' gaps (`references/kickoff.md` §Identity).
   - **Universal:** rules about order, causality and honesty.
   - **Identity slots:** rules about personality (bounce, gloss, ambience, musical cues,
     wordlessness), decided per project.
   - Examples from past projects show a method at work. Do not reuse them as styles or motifs.

## Start here: which mode, and what to read first

| Situation | Mode | Read first (the minimum set) |
|---|---|---|
| Idea only, empty or new repo ("I want to build X") | **Kickoff** | `references/kickoff.md` in full; `references/project-kit.md` §1–§3; the first two sections of `references/domain-games.md` or `references/domain-apps.md`; the templates while you fill them |
| Repo has `docs/<slug>/PROGRESS.md` or `.claude/skills/<slug>-builder/` | **Session loop** (below) | The project's own `CLAUDE.md`, then its PROGRESS |
| Existing project without the kit ("make this premium", "adopt the method") | **Retrofit** | `references/planning-and-slices.md` §Retrofit, then kickoff as it directs |
| A review or polish request on any build | **Audit** | `references/visual-design.md` (quality bar and look loop); `references/verification.md` (adversarial review) |

**References are lookups.** Read a file's Contents line first, then only the sections the
current step needs. Read the rest when its phase arrives. Reading everything up front costs
thousands of lines of context and buys nothing.

Once a project has its kit, **its own builder skill and docs win** on anything they decide. This
skill remains the source of the method and the bar.

## The lifecycle

| Stage | What it produces | Exit gate | Read |
|---|---|---|---|
| **Understand** | Goal sheet: the real goal, what the owner will judge by, constraints, decision rights. The first questions are sent at once. | None. Research starts at once on the recommended answers, marked ASSUMED | `kickoff.md`, `working-with-the-owner.md` |
| **Research** | Parallel tracks: competitors (reviews coded by script), feasibility probes that actually run, stack, art/sound sourcing and licences, money/legal/store eligibility. Every fact tagged Verified, Proposed or Unverified | Adversarial review of the research; corrections recorded | `kickoff.md` §Research |
| **Identity** | Identity brief: audience, art direction as checkable rules, feel brief, sound brief, voice, "what we will not be" | Rendered identity probes looked at (≥3 looks) | `kickoff.md` §Identity |
| **Kit** | CLAUDE.md router, `<slug>-builder` skill, PLAN, ARCHITECTURE, DECISIONS, DESIGN, RESEARCH, PROGRESS (+ MONETIZATION, RELEASE) | Adversarial kit review. **Gate 0:** the owner confirms everything permanent (name, ids, scope) | `project-kit.md`, `scripts/init_kit.py` |
| **Phase 0: Scaffold** | Guards first (layer test, design tokens, fonts, render harness, native setup script or committed-folder policy); the app boots and is looked at | Baseline green; every guard seen to fail; first renders looked at | `architecture.md`, `verification.md` |
| **Phase 1: Core** | Pure domain core and content/data pipeline, proven | Every item proven; core usable in tests | `architecture.md`, the domain file |
| **Phase 2: Vertical slice** | The first ~20 minutes of use at **final** quality: look, motion, sound, haptics, accessibility | **Owner gate:** they use it on their own device (installed by a non-public route) and answer one feel question | `planning-and-slices.md`, `visual-design.md`, `motion-and-feel.md` |
| **Phase 3: Breadth** | All content, screens, meta-features, themes, localisation, accessibility audits, polish | Every acceptance criterion verified by running something | the domain references |
| **Phase 4: Money, services, hardening** | Monetization (if any), analytics, crash reporting, sync, accounts, release tooling | Policies as pure functions with tests; release gates proven | `monetization-and-privacy.md`, `release-and-store.md` |
| **Phase 5: Release prep** | True store copy, screenshots and preview from the real app, ratings, privacy answers, the end-of-project list | **The owner tests on a device and explicitly approves. Only then submit.** | `release-and-store.md`, `working-with-the-owner.md` |

Adapt the phases to the project. A tiny product (one or two core screens, no services or money, a
short time box) follows the **small product profile**: `references/planning-and-slices.md` §1
says what merges, what compresses, and how the deadline maps to gate dates. An app without money
skips that part. **Never adapt away:**
- the gates;
- the vertical slice at final quality;
- the rule that nothing is uploaded unless the owner explicitly asks for that specific upload.

## The session loop (every session, no exceptions)

1. **Orient.** Read the project's docs in order: PROGRESS → PLAN → ARCHITECTURE → DECISIONS →
   DESIGN (before any visual, motion or sound work) → RESEARCH → the domain docs the task touches.
2. **Run the baseline yourself.** PROGRESS saying "green" is a claim. If the tree is red on
   arrival, fixing it is the task. First decide whether the code or the environment is red.
3. **Take the exact next step** from PROGRESS "In progress" or "Next".
   - Do not relitigate a recorded decision without new evidence.
   - If evidence changes it, supersede it with a new DECISIONS entry.
4. **Work in slices**, through the pipeline below.
5. **Hand off.** Rewrite PROGRESS in its fixed sections (`assets/templates/PROGRESS.md`). Above
   all, write "In progress: the exact next step", and what this session did *not* verify. Leave
   the tree green.
   - When capacity runs low: get green, write PROGRESS, record traps, and start nothing new.

## The slice pipeline (canonical: `references/planning-and-slices.md` §5–§6)

```
 1 plan written      2 skeptics attack it      3 freeze contracts (data shapes, ports, file ownership)
 4 build (in lanes if available; the builder does ≥3 looks on anything visible)
 5 integrate (one owner per rule; cold-launch the integrated build)      6 analyze + full suite
 7 adversarial review by non-authors (they re-run and re-render)          8 fixer (verify each finding first; a guard per fix)
 9 mutation proofs for new guards (isolated copy)                          10 confirming look at everything fixes touched; re-run every gate incl. determinism
11 docs (DECISIONS, DESIGN as-built, PROGRESS)                             12 one scoped commit
```

**Definition of done.** These are the canonical eleven items, in pipeline order; the details
are in `references/planning-and-slices.md` §6. A slice is not done until every one holds.
- [ ] **Plan:** the slice was planned before building (In / Not in, test list). A risky slice
  had a skeptic review.
- [ ] **Contracts:** data formats, ports and file ownership were written down before lanes split.
- [ ] **Build:**
  - No API was fabricated.
  - Anything visible was looked at ≥3 times across the look matrix
    (`references/visual-design.md` §13.1), and the quality bar was answered in writing.
  - Content and data were read the way a user meets them.
- [ ] **Integration:** every rule has one owner, and the integrated build was cold-launched and
  looked at.
- [ ] **Analysis** is clean, and the full suite is green, run by you now.
- [ ] **Review:** an adversarial review by non-authors ran; the reviewers re-ran and re-rendered.
- [ ] **Fixer:** each finding was verified, then fixed with a guard or answered by a recorded
  decision.
- [ ] **Guards:** every new guard was **seen to fail** with its fix removed, by assertion, in an
  isolated copy (`references/verification.md`).
- [ ] **Final tree:**
  - a confirming look at everything the fixes touched;
  - every gate re-run;
  - generators and setup scripts run twice, byte-identical.
- [ ] **Docs:**
  - DECISIONS has its honesty blocks;
  - DESIGN has its "As built";
  - traps are appended;
  - PROGRESS says what was not verified.
- [ ] **Commit:** one scoped commit.

Multi-agent orchestration multiplies this pipeline: foundation inline, then lanes, then review
lenses, then a fixer, then a checker that edits nothing. Every step also works solo, in sequence
(`references/orchestration.md`).

## The quality bar (canonical: `references/visual-design.md`, "The quality bar")

### The seven questions

These came from builds an owner rejected as "an app, not a game". Each question names one of
the reasons, and every one has failed in a real build at least once. Each has a game reading and
an app reading.

1. **Alive at rest?** Is the screen alive at rest, in the measure the identity sets? Stillness
   may be a decision, never a default.
2. **Does touch have weight?** Every touch gets an immediate response with physical character
   that suits the identity. Never a one-frame snap. A controlled avatar never lags input; its
   weight lives in secondary motion.
3. **Do results arrive?** Earned or completed things travel from where they happen to where they
   are kept. The destination changes only when they land.
4. **Is every surface from the one material system?** This includes second-ring surfaces:
   toggles, toasts, errors, loading. In a flat style, the material is the surface system:
   fills, rules, elevation, type.
5. **Does each screen arrive?** One overlapping movement. Never pop, never queue. A
   reduced-motion variant exists.
6. **Does it read at its emptiest?** Zero, one and full.
7. **Does the thing arrive before its container?** Only a filmstrip shows this.

### Two edge checks

- **E1:** change while moving is handled. New input hurries the animation home; it never queues
  and never teleports.
- **E2:** a stuck user sees the way out.

Domain extras live in their own files: games add G1–G3 (`references/domain-games.md` §1), and
apps add A1–A4 (`references/domain-apps.md` §2). Refer to every question by name, never by
number.

If a screen passes everything and still feels plain, put it beside the category winner's
equivalent and **name the one element they polished that you left plain.** That comparison
produced most of the breakthroughs.

### What "not good enough" looked like

- **Frames each correct, but in the wrong order or at the wrong time.** Exits before the prize,
  an empty box before its contents, a sound before its impact.
- **Secondary surfaces left as flat platform defaults** next to designed ones.
- **Edges nobody screenshotted:** empty states, off-path modes, motion turned off, transitions.
- **Gaps between what the screen said and what the code did.**

### The look loop: you must see what you made

Never judge a visual from its code:
1. Render to PNG headlessly across the matrix.
2. Open every image.
3. Write down the faults.
4. Fix them at the source.
5. Re-render.

**Budget at least three looks per visual change.** In one game, the first renders had four
faults that every test passed:
- a trail recoloured itself on every move;
- the mascot's ears were hidden, so it read as a loaf of bread;
- a reward was invisible under the path;
- paw prints read as dirt.

Use contact sheets for variants and filmstrips for sequences (`scripts/contact_sheet.py`). Judge
at real viewing conditions: icon sizes and masks, greyscale, the phone speaker for sound.
**Cold-launch the real app** every phase. One cold launch caught a startup crash that every test
missed.

## Non-negotiables

1. **Never fabricate an API.**
   - Read the installed package or SDK source. When the source and a research brief disagree,
     the source wins.
   - Pin surprising library behaviour with small reference tests.
2. **Facts carry their status and date.**
   - Tag research Verified, Proposed or Unverified.
   - Date anything volatile (versions, store rules, law) and re-verify it before relying on it.
3. **A guard counts only once it has been seen to fail.** The commonest failure in these projects
   was a test that lied: it passed with the guarded thing broken. Defences:
   - negative controls;
   - anti-vacuity asserts;
   - literal spec numbers;
   - hostile fakes;
   - mutation proofs in an isolated copy.
4. **Prove generated content and critical data; never trust them.**
   - An independent verifier re-proves every shipped item in CI.
   - Judge the user by the rules, never against a stored answer.
5. **Look at what you made** (the look loop). Fix flaws at the source and regenerate every derived
   asset.
6. **The model runs ahead of the animation.**
   - State commits first; presentation catches up.
   - Input is never blocked except by named, skippable sequences (next action live within 300 ms).
   - Motion Off removes presentation motion: transitions, shake, hit-stop, flashes, parallax,
     camera moves, ambient life and celebrations. Motion that *is* the task (a real-time
     simulation, a video, a live map) continues.
   - Outcomes are identical for the same input. Assists that change the task are separate,
     labelled options, never the Motion switch.
7. **Accessibility and localisation are built and audited, not declared:**
   - real touch targets of at least 44 pt, found by hit-testing;
   - the core loop usable with a screen reader; for time-critical real-time play, every
     non-play flow, with a play-accessibility route decided in DESIGN;
   - no hue-only signals;
   - nothing flashes more than 3 times in any second above the general and red flash thresholds,
     guarded by frame analysis (`references/ux-and-accessibility.md` §15);
   - reading text works at 2× by measured fit;
   - RTL, digits and calendars proven by probes when the audience needs them.
8. **Every platform await has a bound, but never time out into the unsafe side.** For example, a
   late age answer must never default to "adult", and a slow store must never lock out a paying
   user.
9. **Every user-facing claim is true to the code.**
   - Map each store claim to code.
   - Keep one banned-word list for every surface; the project chooses it.
   - Date dormant features.
10. **Honest monetization.**
    - The model is chosen from evidence.
    - Policies are pure functions with literal numbers and one test per rule.
    - No interruption mid-task, at launch or on a reward screen. No dark patterns.
11. **No secrets, production ids, signing keys or fake configs in git.** Use gitignored env files
    and committed examples, with scripts that fail if a secret is tracked.
12. **Nothing outward or irreversible happens without the owner.** That covers uploads (test tracks
    included), publishing, purchases, account settings, credentials and signing keys. Broad
    authorisation is used narrowly.
13. **Record decisions and don't relitigate them.**
    - DECISIONS is append-only; amendments link both ends.
    - Answers still pending are marked ASSUMED until the owner confirms them.
14. **Determinism.** Generators, setup scripts, icons, packs and store assets run twice and come
    out byte-identical.

## Working with the owner, in short

- **Decision rights:**
  - The owner keeps the irreversible public step, money, accounts, legal identity, keys, product
    scope, and how the finished thing feels on their device.
  - Decide everything else from evidence and record it.
  - Never hand a non-expert owner a design choice. A developer-owner who wants to co-decide gets
    options, each with a recommendation.
- **How to ask:**
  - In the owner's language, briefly, as a numbered list.
  - Give every question your recommendation and its reason.
  - Explain jargon and flag what is permanent.
  - Say "nothing is blocked" when that is true.
- **When you cannot perceive a quality** (sound, real-device feel), say so, and build the owner a
  small tool that records their verdicts.
- **Report your own mistakes and side effects on real systems at once,** in plain words.
- **Collect every owner-only action into one END-OF-PROJECT list,** asked once at the end, with
  exact values, console paths and fallbacks.
- **Use one upload sentence, verbatim:** "Nothing is uploaded unless you ask for that specific
  upload, and nothing goes to review or the public before you have tested it on your device and
  approved."

Full protocol and message templates: `references/working-with-the-owner.md`.

## Decide-and-record slots

These are not defaults. Each project decides them in its own DECISIONS, from evidence. The past
values are worked examples from one ad-funded puzzle game, not answers.

| Slot | Decide | Example from one past project |
|---|---|---|
| Owner and language | Who approves; the language for questions | The owner wrote only in their native language; every question was asked in it |
| Platforms and form factors | Phones, tablets, orientation | iPhone only, portrait only, Android phones |
| Stack and UI kit | Framework; platform widget kit or custom-drawn; game engine or not | Custom-drawn with painters and shaders; no platform widget kit; no engine |
| Identity (look, motion personality, sound, voice) | The identity brief | A lit clay material with one key light, bouncy arrivals, a tonal cue system, a nearly wordless UI. **Yours will differ.** |
| Lightings | One lighting (dark-only or light-only), or two that follow the system, with a reason | Two: a day scene, and a night scene re-lit with the same structure |
| Real-time feel (games with a controlled avatar) | Input-latency budget, avatar smoothing, hitbox ratio, time-to-retry, hit-stop | Not applicable there: a turn-based puzzle |
| Art provenance | Hand-built, licensed or commissioned; AI-generated or not | No AI-generated art anywhere a user sees it (legal and consistency reasons, dated) |
| Content or data limits | Sizes, counts, difficulty ceiling | Boards at most 9×7; difficulty capped at a one-step what-if |
| Fairness promises | Lives, timers, undo, retries, streak forgiveness | Undo, retrace and restart always free; no lives, no timers |
| Monetization | Model, cadence, caps, what a purchase removes | First interstitial only after level 20 *and* 8 minutes of play; Remove Ads removes the breaks only |
| Audience and rating | Adult-coded or family; rating choices | An adult target audience for an ad-funded "cute" game, with a fallback icon ready |
| Banned words | Competitor names; claims that would be false here | Never another product's name; never "no ads" there, because a purchase removed only some ads |
| Locales | Languages, script direction, calendars, digits | English, nearly wordless; a predecessor shipped right-to-left Persian |

## Reference map

| When you are about to… | Read |
|---|---|
| Start a project, interview the owner, research, find the identity | `references/kickoff.md` |
| Ask the owner anything, gate a phase, handle permissions or accounts, report a mistake | `references/working-with-the-owner.md` |
| Create or maintain CLAUDE.md, the builder skill, PLAN, DECISIONS, DESIGN, PROGRESS… | `references/project-kit.md`, `assets/templates/` |
| Plan phases, size a slice, check done, hand off, recover, scale down a tiny product, **retrofit** | `references/planning-and-slices.md` (retrofit guard ratchet: `references/architecture.md` §2.5) |
| Run parallel agents, reviewers, fixers; or the same work solo | `references/orchestration.md` |
| Design layers, state, saves, sync, clocks, timeouts, content pipelines, setup scripts | `references/architecture.md` |
| Budget frames, isolate repaints, profile, tune quality tiers | `references/performance.md` |
| Write any test or guard, run mutation proofs, review adversarially | `references/verification.md` |
| Touch anything visible: the quality bar, identity rules, colour, type, layout, lightings and dark mode, icon, the look loop | `references/visual-design.md` |
| Animate, tune input feel, haptics, sound | `references/motion-and-feel.md` |
| Design flows, copy, onboarding, prompts; accessibility; localisation, RTL and calendars | `references/ux-and-accessibility.md` |
| Choose a money model; ads, subscriptions, purchases, consent, analytics, age | `references/monetization-and-privacy.md` (model chooser §1; subscriptions §5.7) |
| Prepare a release, write store copy, make screenshots, verify the artefact, handle account deletion | `references/release-and-store.md` |
| Start any slice (scan its group first) | `references/traps.md` |
| A game: content generation, difficulty, tutorials, daily, streaks, mascot; real-time and action games | `references/domain-games.md` |
| An app: shared and server data, accounts, flows, forms, states, widgets, notifications, market health | `references/domain-apps.md` |
| Flutter (identity probe before Phase 0: §0) | `references/stack-flutter.md` |
| SwiftUI, Compose, React Native or the web (baseline commands; identity probes: §0) | `references/stack-other.md` |

## Scripts (`<skill-dir>` is the folder holding this SKILL.md, e.g. `~/.claude/skills/flagship-method`)

**`init_kit.py`** scaffolds the kit. Always pass `--dest`. Never run it from inside the skill
folder. It never overwrites. Run it first as a dry run:

```bash
python3 <skill-dir>/scripts/init_kit.py --dest <project-root> --kind app --name "Name" --slug name --one-line "…" --owner "…" --language "…" --stack "…" --platforms "…" --with-monetization --with-release --dry-run
```

- **Variants:**
  - `--kind` is `app` or `game`.
  - `--with-monetization` is for a product that earns money or collects data.
  - `--with-release` is for a product that ships to a store or to production.
- **`--one-line`** is one sentence that ends with a full stop.
- **Run it again without `--dry-run`** to write the kit.
- **Existing project:** add `--retrofit`. The kit goes to a staging folder for you to merge by
  hand.
- **Filling the kit:** fill it with real content from kickoff. An unfilled template is programmer
  art in docs.
  - `--check --dest <root> --slug <slug>` lists every remaining `[TODO` marker and validates the
    builder skill's frontmatter. It exits 2 when there is no kit, so it never passes vacuously.
  - `--selftest` proves the script itself. Its cases live in `scripts/init_kit_selftest.py`,
    which ships next to it.

**`contact_sheet.py`** tiles rendered PNGs into a labelled grid, or with `--filmstrip` into a
filmstrip, for the look loop. It needs Pillow, installed in a venv (see README):

```bash
~/.venvs/flagship/bin/python -I <skill-dir>/scripts/contact_sheet.py build/looks/home/ --cols 4 --cell 390x844 --out build/looks/home_1.png
```

**`code_reviews.py`** codes exported store reviews by regex themes into counts:
- complaints in 1–3★ reviews, loves in 4–5★ reviews, and complaints inside 4–5★ reviews, per app
  and theme;
- optionally, the store average set against the mean of recent written reviews.
- `--help` gives the input format.

> **Dated facts.** The package versions, store and ad policies, privacy rules and laws quoted in
> these references were checked around 2026-10. Treat every one as a lead to re-verify against the
> installed source or the official documentation, never as a rule.
