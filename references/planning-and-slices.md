# Planning, slices and the session loop

This file covers how work is ordered (phases and owner gates), how it is cut (slices), how each
slice is carried to done (the pipeline and the definition of done), and how it passes between
sessions (the session loop, recovery and retrofit).

**Read when:** writing or amending PLAN; at the start and end of every session; choosing the next
step; closing a slice; before an owner gate; after an interruption; adopting the method in a
project that is already underway (§10).

## Contents
1. Phases 0–5, and the small product profile
2. The vertical slice at final quality
3. Owner gates: answers that lag, delivery, the one question
4. Slice sizing
5. The slice pipeline (canonical)
6. Definition of done (canonical)
7. The session loop
8. Refilling the backlog, and "checked and left alone"
9. Recovery from interruption
10. Retrofit: adopting the method mid-project

---

## 1. Phases 0–5

Adapt the phases to the project, but keep two properties. Each phase leaves something you can run
and judge, and the owner never sees anything below final quality.

| Phase | Must prove | Typical contents | Accept when (examples) |
|---|---|---|---|
| **0 Scaffold, guards first** | The skeleton builds on every platform, and the rules are enforced before there is code to break them | Hand-written dependency manifest (only Phase 0's needs); native setup script; fonts; design tokens; architecture guard; render harness; one themed screen. Retrofit: the adoption baseline (§10) | Analysis clean; tests green, including guard, paint, bounds and font tests, each guard **seen to fail**; the setup script generates every platform and its checks pass; the app runs on simulator and emulator; the screenshot matches DESIGN §2 |
| **1 The core, proven** | The domain is correct before anything is drawn on it | Pure domain core; content pipeline (offline generator with selftest, verify and a review mode) or the data layer (strict versioned saves, migrations, seed fixtures); parity between independent implementations; tests of every transition and refusal | Every shipped item (games) or every data transition and migration (apps) proven in the app's own tests; review output *read* as content; verification of the whole pack or fixture set under a stated time (60 s) |
| **2 Vertical slice → OWNER GATE** | The product's feel, on a narrow scope, at the final bar | The first ~20 minutes of use, finished: art, hero, input, motion, sound, haptics, persistence, onboarding, motion-off path, accessibility basics | The quality bar answered "yes" in writing on the core screens across the look matrix; the largest content or the longest real data fits; skip shows the next action within 300 ms (test); every item played (games) or every core flow driven end to end (apps) by real gestures in a test; the owner uses it on their device and says yes (§3) |
| **3 Breadth** | Scale content and features without dropping the bar | All content, themes, meta-features, the second lighting (if any), localisation, accessibility everywhere, sharing, stats | The same bar on every screen; every content or data guard runs over every item and state |
| **4 Money, services, hardening** | Earn and observe without harming the product | One slice per dependency group: the money model's foundation, each ad format or the paywall and its entitlement, purchases, analytics + crash reporting, age signals, sync or accounts, release hardening | Every policy rule a constant with a test that fails without it; each adapter tested against a strict SDK fake; the release build cold-launched and used |
| **5 Release prep → owner device test → owner approval → upload** | The store sees only true things, and the owner approves after testing | Icon; store copy; screenshots and preview from the real app; privacy policy; ratings; release verifiers | Static and run gates pass; the copy checker passes; the end-of-project list is complete; the owner approves |

For an app, "the core" means domain model + data layer + sync, and "content" means seed data and
fixtures held to the same proof discipline (`references/domain-apps.md`). A product without money
skips that part of Phase 4; a tiny product follows the small product profile below. The gates, the
final-quality slice and the release approval never get adapted away.

### Small product profile (Proposed)

*Proposed, from one trial on a one-screen utility; tune it on the next small product.* For a core of
about 30 lines, the full kit scaffolded 254 TODO markers and 1,268 lines of docs, and the pipeline
gave a settings sheet the same twelve steps as a sync engine. Nothing said what to cut, so a model
either imposes the whole ceremony or improvises the cuts.
- **When it applies:** one or two core screens; no services, accounts, sync or money model; a time
  box of about two weeks. Record the choice in DECISIONS, and leave the profile the moment one of
  these stops being true.
- **What merges:** Phases 0 and 1 when the core is a pure function under about 200 lines; Phases 3
  and 4; Phase 5 preparation overlaps Phase 3.
- **What compresses:**
  - skeptics (§5 step 2) only on risky slices;
  - one combined review of the research and the kit (`references/kickoff.md` §6, §9);
  - on a low-risk slice, one solo review pass with the "do the tests prove anything?" lens
    (`references/verification.md` §10);
  - mutation proofs for every Phase 0 guard and every guard over critical logic (money arithmetic,
    the rules), not for every cosmetic test;
  - in the kit, a slot that does not apply says "none: <reason> (DECISIONS #n)", and a slot only a
    later phase can fill holds its "Written in Phase" line (`references/project-kit.md` §12).
- **What never changes:** the three gates; the vertical slice at final quality; at least three looks
  per visual change; every guard seen to fail; the cold launch of the integrated build; no upload
  without the owner's request for that specific upload.
- **The calendar line.** PLAN gets one line mapping the deadline to dates for Gate 0, the feel gate
  and the release gate, with the owner-side lead times counted in (rule 10 below). When the dates
  slip, cut scope from Phase 3, never a "never changes" item.

**Rules for writing PLAN** (the doc's shape: `references/project-kit.md` §10):
1. **Acceptance means running something:** tests, renders, the simulator, a script. "Reading the code
   shows" is never acceptance. When something can only be judged on hardware ("feels immediate"),
   state it as unverified and put it on PROGRESS's Device checks.
2. **Dependencies enter in the phase that uses them.** PLAN names the phase for each later one. In
   the shipped puzzle game, audio and preferences came in Phase 2, and the analytics, ads, review
   and purchase SDKs in Phase 4, so unused SDKs never shaped the early code.
   - When porting a sister project's setup script, write a table: source step → keep / adapt / drop /
     move → phase. Steps that must always run (display name, orientation, device family) move out
     of conditional blocks.
   - Fix placeholders in borrowed configs before you use them. One recommended manifest pointed at a
     shader file that did not exist.
3. **Don't start a phase until the previous one's criteria hold,** unless the owner relaxes that.
   Record the relaxation as a DECISIONS entry.
4. **State gaps in the phase header:** "complete, with two gaps, stated"; "rendered, not played".
5. **Write the test list into the plan before building any stateful feature.** Cover every
   transition, every refusal, and the edges. *Example (daily streak):* always credited; one miss
   with a token held; one miss without; two misses with two tokens and with one; earning at 7 days;
   the cap; the archive across a simulated year. If you cannot write the list, the design is not
   ready.
6. **Every phase block says what is in the phase and what is not; every slice says what is in the
   slice and what is not.** *Example:* "home has no daily card and no map yet; the complete screen
   shows the share card but does not share it, because there is no share plugin yet; after the
   last slice level, a warm 'more coming soon' card with Replay."
7. **Put a checkpoint before wiring a risky asset.**
   - Render the asset in isolation, look three times, and compare it side by side with the
     benchmark at the same size.
   - Pre-write the failure path, as a plan B with a trigger: "fails after three looks on any of
     a, b, c → ask the owner one money question".
   - *Example:* the mascot checkpoint passed against the genre leader, so no external animation
     tool was bought.
8. **Add an unplanned phase when a comparison exposes an absence.** In an earlier game, a whole
   "between levels" layer was missing until a side-by-side with the leader showed it.
9. **Strike a wrong criterion, with a dated reason.** Don't silently drop it.
   *Example (shipped puzzle game):* "~~profile on the simulator and a low-tier emulator~~
   **Corrected 2026-10-03:** neither says anything about a low-tier phone. Instead: frame-budget
   tests in CI, plus a profile build on a real phone with a frame-log flag." The matching DECISIONS
   entry recorded the replacement.

   > **Dated facts (as of 2026-10 — re-verify before relying):** the Flutter tool allowed only debug
   > builds on the iOS simulator, and Android emulators drew with the host machine's GPU, so neither
   > could measure a phone's frame times.
10. **Plan the waiting, not only the coding.** Owner-side lead times (developer accounts, store
    records, verification, review) run in calendar weeks while code takes days. An earlier game's
    launch plan put about 9–11 working days of effort at 3–8 calendar weeks elapsed.
    - Ask early only for items that are slow or permanent, as the Phase 2 gate prerequisites. Batch
      everything else into the end-of-project list.
    - Put every feature that changes the privacy forms (analytics and crash reporting) in one
      slice. Forms are free to change before the first submission and cost a revision after.

## 2. The vertical slice at final quality

**Why it comes before breadth.**
- The owner had rejected the previous project on output quality.
- A rough build anchors judgement low, and broad rough content gets judged as the product.
- The slice tests the one thing code cannot: whether it feels good. It does that at the lowest cost
  of change.

**What it contains: narrow scope, full depth.**
- *Example (shipped puzzle game):* 20 levels; home, level, complete and settings screens; the full
  solve celebration; a v1 sound pack; haptics; the tutorial; persistence; the motion-off path; a
  quality switch. No daily mode, no map, no ads.
- *Example (app):* onboarding; the core create/view/edit flow; one success moment; empty, error and
  offline states, all at the final look. No secondary settings, no sync.

**Before the gate, run a gate-polish pass.** Look at the whole slice the way the owner will meet it:
cold launch, first run, the first ten minutes, on the slice's phone sizes. In the shipped game this
pass found enough to earn its own heading in the trap log.

Internal mood boards are fine. Owner-facing builds are never drafts.

## 3. Owner gates: answers that lag, delivery, the one question

The default has three gates. The protocol for talking to the owner (language, batching, approvals,
reporting) is in `references/working-with-the-owner.md`.
- **Gate 0, the kit.** The owner confirms the brief, the name, the ids (provisional is fine) and
  the scope (`references/kickoff.md` §10).
- **The feel gate, after Phase 2.**
- **The release gate, after Phase 5.**

**Answers that lag never block research or reversible work.** Send each question block at once.
Proceed on the recommendations you sent, each recorded as a DECISIONS entry marked **ASSUMED** and
listed in PROGRESS's ASSUMED answers table (`references/project-kit.md` §6 rule 13). When the
answer arrives, a new entry confirms or supersedes it. Nothing permanent rests on an ASSUMED
answer: **Gate 0 is where ASSUMED answers about permanent things** (the name, the app or bundle
id, product ids, a paid vendor) are confirmed. If the answers never come, scaffold under the working
name with provisional ids and keep building; the first store record, upload or purchase waits.

**The feel gate:**
1. **Prerequisites first, early and non-blocking.** One short list in the owner's language, holding
   only what is slow or permanent:
   - which phone they will use, and whether a developer install on it is possible;
   - confirm the permanent name and app id, needed before any store record or upload ("permanent
     from the first upload");
   - create the store record, which reserves the name (store APIs typically cannot create it);
     recommended early because it is slow, never a condition of a non-public gate build;
   - register the domain and start trademark clearance (recommended; the gate does not wait).
2. **Deliver by a non-public route by default.** In order of preference:
   - a cable or developer install on the owner's own phone;
   - a locally built package they install themselves;
   - a screen recording from a simulator, only if they have no suitable phone. It shows look and
     motion, not touch, haptics or the speaker; say so, and keep those on the Device checks.

   **Any upload, an internal test track included, happens only when the owner explicitly asks for
   that specific upload.** One request covers that one build, not the next; a tool that can upload
   is not permission to upload.
3. **The owner uses it on their own device (or watches the recording) and answers one question,**
   fitted to how the product is used. One wording each; the PLAN goal sheet holds the project's
   version, in the owner's language:

   | Product | The gate question |
   |---|---|
   | Game | "Do you want to play the next level?" (name the real unit: board, puzzle, round, run) |
   | Daily-use app | "Would you open this again tomorrow without being asked?" |
   | Episodic tool (used when something happens: a shared bill, a trip, a tax return) | "Next time <the trigger> happens, would you reach for this first?" |

   "Without being asked" matters for any app that sends reminders: the reminder does the asking, so
   the question judges the pull, not the push. An episodic tool fails a daily question by design;
   the owner answers it with a real instance of the trigger if one comes up before the gate.
4. **If the answer is no:** ask what felt wrong, in their words. Record it verbatim (translated) in
   DECISIONS, fix it, and re-gate.
5. **Their device use is also the first real-device performance check.** Write the numbers down.
6. **Nothing in the next phase starts before a yes,** unless the owner relaxes this. Record that.

**The release gate.** Nothing is submitted for review or released to the public until the owner
has tested the exact build on their own device and approved explicitly in chat. Every upload,
before or after approval, needs their explicit request for that specific upload. Signing keys and
device tests are the owner's, at the end. All other work continues in the meantime
(`references/release-and-store.md` §0).

## 4. Slice sizing

A slice is one coherent, committable change that a single review pass can hold. Number it within
its phase (2.1, 4.3); the git log then reads as the plan.

- **One risk per slice.** Phase 4 of the shipped game ran one dependency group per slice: ads
  foundation, interstitial, rewarded, purchases, analytics + crash, age signals + sync, release
  hardening. Each slice's review still found 6–11 real defects. Two SDKs in one slice would have
  doubled what each review had to hold.
- **Split broad polish by concern.** The heaviest trap batch in the shipped game's log (31 entries)
  came from a single "night theme, accessibility, share, stats, polish" slice.
- **The test for a slice:** you can write its test list and its "Not in the slice" list before you
  start. If you can't, it is two slices, or it needs a research step first.
- **Risky integrations** (ads, consent, payments, subscriptions, sync, accounts) get a research step
  inside the slice: readers, then a designer, then two skeptics, then numbered decisions and
  numbered tests (`references/orchestration.md`).
- **Lanes** (when agents run in parallel): 2–8 per slice, each owning disjoint files. Use a
  dependency-ordered sequence where needed: state and sound in parallel, then the board, then the
  screen (`references/orchestration.md`).
- **The rhythm that held:** about 20 commits over four days in the shipped game, roughly one slice
  plus its fixer pass per commit.

## 5. The slice pipeline (canonical)

This is the one order. `SKILL.md`, the PLAN template and the builder-skill template copy it.

```
 1 plan written → 2 skeptics → 3 freeze contracts → 4 build (≥ 3 looks on anything visible)
 → 5 integrate (one owner per rule; cold-launch the integrated build) → 6 analyze + full suite
 → 7 adversarial review (reviewers re-run and re-render) → 8 fixer (verify first; a guard per fix)
 → 9 mutation proofs (isolated copy) → 10 confirming look + every gate re-run, determinism included
 → 11 docs → 12 one commit
```

1. **Plan written.** DESIGN's "Plan (written before building)" for every screen and effect, the test
   list, In / Not in, and the contracts the slice needs. Keep the brief as a research file when a
   slice spans sessions.
2. **Skeptics.** One or two reviewers attack the plan before any code exists, which matters most on
   risky slices. The skeptics on the shipped game's ads design found six design defects, two of
   which would have blocked ads for the session or frozen the game. They also found 12 rules that
   had no failing-without test.
3. **Freeze contracts.** Before lanes start, write the data formats (versioned), the ports and the
   file ownership into ARCHITECTURE. *Example:* the content JSON contract (format 1) was fixed before
   the generator, engine and solver lanes split. They integrated with node-for-node parity over 206
   shared fixtures.
4. **Build.** Lanes own disjoint files. Each runs its own tests, reads the installed source of every
   new call, and does **≥ 3 looks** on anything visible across the look matrix (canonical:
   `references/visual-design.md` §13.1), writing down what each look found. Lanes report
   cross-lane needs instead of editing other lanes' files.
5. **Integrate, as its own step, with its own findings:**
   - merge;
   - give every rule one owner, and every saved document one latest version (two lanes had bumped
     the same settings schema independently);
   - grep for stale numbers and phrases;
   - turn "still a stub" tests into "no X is still a stub" guards;
   - run the generators and the setup script twice and check they are byte-identical;
   - make debug builds on every platform;
   - **cold-launch the integrated build and look;**
   - fix PROGRESS's stale lines.

   *Incident:* only a cold launch of the integrated build showed the entry point throwing a type
   error before the first frame. The app sat on its launch screen while every test was green.
6. **Analyze and run the full suite** on the integrated tree, slow tests included, yourself. A
   count that disagrees with the lanes' reports is a finding.
7. **Adversarial review.** Reviewers each take a distinct lens, re-run the suite and re-render the
   screens themselves (never trusting the builder's renders), and report evidence only
   (`references/verification.md`, `references/orchestration.md`). Count the findings by severity,
   then give each finding a disposition:
   - fixed, with a guard;
   - answered by a recorded decision;
   - left for a named device check;
   - a doc amendment.
8. **Fixer.** Verify each finding before fixing it, by reproducing it or reasoning it true. The fixer
   may push back. Each fix ships with a guard seen to fail without it. Record the "tests that could
   not fail" that the review exposed.
9. **Mutation proofs.** Run them in an isolated full copy, never the shared tree. Report "k of n
   killed by assertion, none a compile error", investigate every survivor, and re-run on a fresh
   copy of the final tree (`references/verification.md`).
10. **A confirming look, then every gate on the final tree.** Look again at everything the fixes
    touched, in the same cells of the look matrix. Then re-run: selftests, content verification,
    analysis, the full suite including slow tests, tool selftests, determinism (every generator,
    setup script, icon and screenshot builder run twice, byte-identical), debug builds, and the
    relevant release gates. Record the results line. If a gate was not re-run, say why, with a
    reason someone can check.
11. **Docs:**
    - DECISIONS (the next free number);
    - DESIGN "As built";
    - ARCHITECTURE amendments;
    - MONETIZATION, if the slice touched money or data;
    - the builder skill's traps (under a dated heading);
    - PROGRESS: Done with its counts, Next, Device checks, the END-OF-PROJECT LIST.
12. **One commit,** with a scoped message that says why ("Phase 4 slice 4.3 — rewarded videos for a
    hint and a bonus"). Record the hash in PROGRESS.

**What the tail found, after the lanes had tested their own work:**

| Measure (shipped puzzle game) | Value |
|---|---|
| Real findings per slice review | 4–27 (one slice: 26 findings, 22 fixed, 2 left for a device check, 2 doc amendments) |
| Slices whose first mutation run had survivors | at least 4 |
| Fixer-pass trap entries | about 74 under 9 headings |
| Where the worst defects were found | review and fixer passes: a lost purchase, a release check that could not fire, a child-safety fallback |

Budget review, fixer and mutation proofs as a fixed part of every slice. They are not extras. The
small product profile (§1) scales them down; it never drops them.

**Solo fallback.** Without parallel agents, run the same twelve steps in the same order, alone.
The step-by-step mapping, and how to review your own work as a stranger (a context break, findings
written to a file before any fix), are in `references/orchestration.md` §11. The order matters more
than the parallelism.

## 6. Definition of done (canonical)

This is the canonical list, in pipeline order. Each builder skill keeps a copy in the same order,
adding only its phone sizes, themes and content checks.

- [ ] **Plan:** the screens and effects were planned in DESIGN before building, with the test list
      and In / Not in; a risky slice had a skeptic review.
- [ ] **Contracts:** shared data formats, ports and file ownership were written into ARCHITECTURE
      before lanes split.
- [ ] **Build:** every new call was read in the installed source (no fabricated API). Visual work
      was looked at ≥ 3 times across the look matrix, with the renders listed and what each look
      found; anything that moves was watched on a simulator; the quality bar is answered in
      writing. A content or data change had its review output read the way a user meets it.
- [ ] **Integration** gave every rule one owner and every saved document one latest version, swept
      stale wording, and cold-launched the integrated build and looked at it.
- [ ] **Analysis** is clean, and the full test suite is green, slow tests included, run by you now.
- [ ] **Review:** an adversarial review ran, and the reviewers re-ran and re-rendered.
- [ ] **Fixer:** every finding was verified, then fixed with a guard or answered by a recorded
      decision; tests that could not fail are recorded.
- [ ] **Guards:** every new guard was seen to fail with its fix removed, in an isolated copy, by
      assertion and not by a compile error. Every invariant touched has a guard; a changed renderer
      is covered across its parameter range (extremes, every pose, every size it is drawn at).
- [ ] **Final tree:** a confirming look at everything the fixes touched; every gate re-run; the
      generators and the setup script ran twice, byte-identical; debug builds pass on each platform.
- [ ] **Docs:** DECISIONS recorded with its honesty blocks; DESIGN "As built"; ARCHITECTURE amended;
      traps appended under a dated heading; PROGRESS updated (counts, hash, what was not verified
      and why, Device checks, the exact next step).
- [ ] **Commit:** one commit with a scoped message.

## 7. The session loop

1. **Orient.** Read CLAUDE.md, then the builder skill, then PROGRESS → PLAN → ARCHITECTURE →
   DECISIONS → DESIGN (before visual, motion or sound work) → RESEARCH → MONETIZATION, if the kit
   has it (before money or data). For a cold start in PROGRESS: Current phase → In progress → How to
   verify.
2. **Baseline.** Run the How-to-verify block yourself. If it is red, fixing it is the task. First
   decide whether the code or the environment is red. Counts that disagree with PROGRESS are a
   finding: correct PROGRESS. In a retrofit, green means no failure outside the quarantine list.
3. **Choose the next step:**
   - PROGRESS's exact next step;
   - if none, the first unmet acceptance criterion of the current phase in PLAN;
   - if every criterion holds, the gate, or else the next phase;
   - if Next is empty mid-phase, refill it (§8).
4. **Slice.** Use the pipeline (§5), scaled to the work. A one-line fix still gets its test, a look
   if it is visible, a PROGRESS line and a commit.
5. **Look** at what you made, the way the user meets it.
6. **Record** decisions, As-built notes and traps in the session that produced them. Owner questions
   go into the `When | Ask` table.
7. **Hand off.** Rewrite PROGRESS in its eleven sections (`assets/templates/PROGRESS.md`), leave the
   tree green, and commit.

**Low capacity:** stop starting things. Get the tree green, write PROGRESS (state, exact next step,
hazards), append traps, and commit if green. If you are mid-slice and cannot finish, never commit
red. Write "<slice> — in the working tree, not committed: <what is done, what is not>" under In
progress, so the next session or a finisher continues from it.

**Session hygiene that preserved quality across handoffs:**
- **Format only the files you touched.** A whole-tree format command reformatted other lanes' files
  and dragged unrelated changes into commits.
- **Scope find-and-replace** to the source, test and docs folders. A global substitution rewrote a
  gitignored cache.
- **Never mutate the shared tree** for a negative control; never revert a file in it to drop a probe
  (it discards anyone else's edits in that file).
- **Give worktree or branch agents the exact base commit.** They start from the default branch.
- **Check what a shared simulator is running** before you drive it. Another session may own it.

## 8. Refilling the backlog, and "checked and left alone"

**An empty Next list is not a finished product.** Re-run the rubric and refill it. In an earlier
game this "has never come back empty yet"; one sweep found a whole mode that had never had a feel
pass. Sweep:
- the quality bar on every screen, then the side-by-side with the category leader: name the one
  element they polished that you left plain (`references/visual-design.md`, "The quality bar");
- a second sweep **by state and sequence** rather than by screen: between screens, change while
  moving, settings off, empty/one/full. A screen-by-screen pass misses what happens between two
  screens that are each fine;
- DECISIONS' Unverified and Open blocks, PROGRESS's Small open items and Device checks;
- the release checklist (`references/release-and-store.md` §9).

**Backlog item format:**
```
- [ ] (<severity>) <what, in plain words> — <why: the rubric question it fails> — accept when: <runnable check>[ — owner said: "<verbatim>"]
```
Severity scale:
- **blocker:** money or progress lost, or the product unusable;
- **major:** a user would complain;
- **minor:** a user would notice;
- **polish:** we would notice.

**"Checked and left alone."** A pass that changes nothing where nothing is wrong is the pass working.
- Record each item you checked and deliberately left unchanged, with the measured reason. The next
  session then won't redo the check, and nobody "fixes" it to justify a pass. *Example:* a sparse
  board was measured to be width-limited, and loosening the cap would have doubled the off-screen
  overhang.
- Record refuted review findings under "Refuted — do not re-find".
- An earlier owner's standing instruction: "if it is already in its best state, don't overengineer."

## 9. Recovery from interruption

Interruptions happen: the owner stops a run, a login expires, capacity ends, a lane crashes.
1. **Establish the facts before acting:**
   - which runs completed;
   - which were halted, and where;
   - what partial work is in the tree (`git status`, `git diff` against the last commit, each lane's
     scratch folder and logs);
   - which notifications are stale.
2. **Report** to the owner in their language: "Nothing was lost: finished work is in the tree, and
   the last commit is still <hash>." Then list what will be resumed and what will not be redone.
3. **Don't rerun from scratch; finish from the tree.** The finisher (an agent, or you):
   - reads the tree and the predecessor's scratch;
   - checks the work against *every* item of the original task;
   - finishes what is missing;
   - runs any precondition step first (a generation step that a finished lane's change needs before
     tests mean anything);
   - looks at the outputs;
   - runs the full verification;
   - writes the report the predecessor would have written, from what it verified, not from
     assumptions.

   Then the normal review → fix → check tail runs. *Example:* a sound builder halted after about 42
   minutes, at its very end. A finisher completed it from the tree; nothing was rebuilt.
4. **Persist every lane's report to a file the moment it returns.** Pass the *path* to finishers,
   never a placeholder (incident: `references/orchestration.md` §9; `references/traps.md` T-9).
5. **Restore truthfulness.** Replace stale "not committed" labels with hashes and recount the tests.

Finisher prompt:
```
You are the finisher. A previous <role> implemented <what it did> and was interrupted at <point>.
Do NOT redo its work. Read `git status` / `git diff <hash>` and its scratch at <path> to learn exactly
what exists; check it against EVERY item of the task; finish what is missing or half-done; run
<precondition step> first; look at the outputs yourself; run the full verification. Write the report
the builder would have written, from what you verify yourself, not from assumptions.
```

## 10. Retrofit: adopting the method mid-project

A retrofit is the kickoff run over a tree that already exists. Take the steps in this order; each
names where the full method lives. *Example (a trial adoption of a small word game):* the tree
arrived red (the platform template's counter test looked for a counter the app never had); 6 of 9
source files imported the platform UI kit; the ids were still the generator's placeholder, with
tablet and landscape on by default; of three hand-typed boards, two had dead ends and one could not
be finished; and the toolchain's first dependency fetch rewrote a tracked config file. Each became
a recorded fact and a Phase 0 item, not a silent fix.

1. **Run and render as found,** before writing any doc.
   - Run `git status --short` first, and again after the first build. Some toolchains rewrite
     tracked files on their first run (the dependency fetch above added analyzer excludes and
     generated platform files; a later `git add -A` committed them, and the commit had to be
     amended). Commit such changes deliberately, gitignore generated paths, and keep
     `git status --short` (expect empty) in the baseline (Flutter:
     `references/stack-flutter.md` §1).
   - Build; run every test and record each red test by name (fix nothing yet); cold-launch;
     render or screenshot the main screens across the look matrix and answer the quality bar on
     them.
   - Prove existing content or data with a probe, and record the ids, platform flags, save keys and
     SDK configuration (sample ids included) exactly as found.

   This record becomes PROGRESS's first Done entry, **State on adoption (<date>, <hash>)**.
2. **The goal sheet, with the first question block sent at once** (`references/kickoff.md` §2,
   §4). A retrofit adds three questions that are permanent or costly here:
   - Has any build been uploaded? Which name and ids are already live, and so permanent?
   - Whose progress or data must survive (users, testers)? This decides migration versus a fresh
     save format.
   - Is there a launch date?

   Work continues on your recommendations, marked ASSUMED (§3).
3. **Compressed research tracks** (`references/kickoff.md` §5.7): competitors and complaints coded
   by script; the stack as found, with versions read in source; a proof probe for the existing
   content or data.
4. **Identity: keep, evolve or replace,** recorded as a DECISIONS entry with the renders that
   decided it (`references/kickoff.md` §Identity). A look that fails the quality bar everywhere is
   evidence, not a constraint; a look that users already know may be evolved rather than replaced.
5. **Scaffold to a staging folder and merge by hand.** With `--retrofit` (the command:
   `references/kickoff.md` §8), `init_kit.py` writes the whole kit to `<dest>/.flagship-kit/` (or
   `--stage <dir>`) when any target exists, with a `MERGE.md` listing what to merge and what to
   move, and never touches existing files. Merge:
   - an existing CLAUDE.md: fold the router sections into it and keep its project-specific lines;
   - existing docs: move each part into the kit doc whose question it answers
     (`references/project-kit.md` §2), and record the moves in DECISIONS;
   - PROGRESS: Current phase is the adoption kit, or the latest phase whose acceptance criteria hold
     *when you run them*; Done starts with State on adoption; Next is the gap;
   - DECISIONS: each load-bearing existing choice as "Recorded after the fact (adoption, <date>);
     evidence: the code at <hash>". Never invent a reason: write "reason not recorded". Don't
     relitigate these in the adoption pass; supersede them later, on evidence;
   - ARCHITECTURE §1: the target table, with today's code admitted as LEGACY rows (step 8);
   - the builder skill's traps: catalogue entries converted to the project format, plus
     **Inherited (from this project's history)**: one entry per fix commit or issue that names a
     mechanism, citing the commit.

   Delete the staging folder once merged; never commit it.
6. **Kit review** (`references/kickoff.md` §9), with one retrofit question added to BUILDABILITY:
   does every LEGACY row and every quarantined test have an owning slice and an expiry?
7. **Gate 0** (§3): the ASSUMED answers about permanent things are confirmed, live ids above all.
8. **Phase 0 is the adoption baseline, guards first:**
   - **The layer guard, with a ratchet.** ARCHITECTURE §1 states the target. Each legacy directory
     or file is admitted as a row marked `LEGACY (expires: <slice>)`; a UI kit imported almost
     everywhere gets one LEGACY exception, not one per file. The guard fails on any *new*
     violation and on an expired row, never on a recorded one: removing a legacy row is free,
     adding one fails (mechanics: `references/architecture.md` §2.5).
   - **A quarantine list, never a silent skip.** Each red test from step 1 goes into PROGRESS's
     quarantine table: the test, why it fails, the slice that owns it, an expiry. The baseline is
     green when nothing fails outside the list. An evidence probe that fails by design (as-found
     content that Phase 1 replaces) is named as such and kept out of the baseline block, or it keeps
     the baseline red forever and invites a fresh session to "fix" content that is due to go.
   - **Pin current behaviour before replacing it:** characterization tests over the flows and saves
     that must keep working.
   - **Migrate a UI kit or a state library by strangler.** New and touched screens go on the new
     layer, one screen per slice, each with before and after looks; the ratchet bans new imports of
     the old one at once, and its last LEGACY row leaves with its last screen. Keep an existing state
     library if state can be made immutable and tested through it; replace it when the core is
     rewritten anyway; either way, record its lifecycle traps (Flutter: `references/stack-flutter.md`
     §2 for leaving Material, §3 for an existing state library).
   - **Bring the platform folders under the setup script:** a keep / adapt / drop table from the
     hand-edited folders, and an id check (placeholder ids, default device families and
     orientations become explicit decisions).
   - Banned words and the content or data verifier, each guard seen to fail.
9. **Then the normal phases.** The next owner-facing build is at final quality. If the product is
   below the bar, Phase 2 is a final-quality vertical slice that rebuilds the existing core flow
   (rebuild rather than patch when the quality bar is "no" across the board), then the owner gate.
   Nothing new reaches the owner before that gate.
