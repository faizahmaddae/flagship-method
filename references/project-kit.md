# The project kit

The kit is the set of documents every project carries. It lets any worker (a smaller model, a
parallel lane, or you with no memory) continue at full quality. This file gives each doc's
jurisdiction, says which doc wins a conflict, and explains how to write and maintain each one.
Skeletons are in `assets/templates/`; `scripts/init_kit.py` copies them into a project.

**Read when:** creating the kit at kickoff (§1–§3 first, the rest while filling each doc); before
editing any kit doc; when two docs disagree; at the kit review before Gate 0 (§15); when adopting
the method mid-project (`references/planning-and-slices.md` §10).

## Contents
1. Why the kit exists
2. The set: where each doc lives, what it answers, how it is scaffolded
3. Precedence: which doc wins
4. CLAUDE.md: the thin router
5. The builder skill and its trap log
6. DECISIONS: the append-only log
7. ARCHITECTURE: an executable contract
8. DESIGN: conventions that keep the look decided
9. PROGRESS: the handoff, in eleven fixed sections
10. PLAN
11. RESEARCH, and keeping evidence honest
12. MONETIZATION, RELEASE and `store/` (optional docs); slots only a later phase can fill
13. Docs that tests parse
14. Maintenance rules for every doc
15. Kit health checklist

---

## 1. Why the kit exists

- **Thinking is the scarce resource.** Spend it on the plan, the decisions, the architecture
  contract and the builder skill, and write all of it down. A conversation is gone next session.
- **It carries a project across many hands.** In the shipped puzzle game, the kit took the project
  from research to release-ready in about four calendar days of agent sessions: 20+ commits, tests
  from 149 to 4,100, dozens of handoffs between sessions and lanes, no lost state. Every cold
  session oriented from PROGRESS alone.
- **Kit errors are the cheapest errors you will ever fix.** That kit, together with the research it
  was drafted from, went through one combined adversarial review (three lenses) before any code
  existed: 82 findings, 71 confirmed, all addressed before Phase 0.
- **Prose rules drift; executable rules don't.** "A rule nobody has ever checked is a rule you do not
  actually know" (an earlier game, after a "the core imports no UI framework" line proved false). So
  the kit's load-bearing rules are parsed or enforced by tests (§13).

## 2. The set: where each doc lives, what it answers, how it is scaffolded

| Doc | Path | Answers | Read |
|---|---|---|---|
| `CLAUDE.md` | repo root | how to orient; the core rule; the baseline; house rules | first, every session |
| builder skill | `.claude/skills/<slug>-builder/SKILL.md` | how to work here: method, invariants, definition of done, traps | before writing any code |
| PROGRESS | `docs/<slug>/PROGRESS.md` | where we are; the exact next step; how to verify; what only the owner can do | every session |
| PLAN | `docs/<slug>/PLAN.md` | the goal; phases, acceptance criteria, owner gates | every session |
| ARCHITECTURE | `docs/<slug>/ARCHITECTURE.md` | the layer contract (test-enforced), state, pipelines, services | before adding a file, layer or dependency |
| DECISIONS | `docs/<slug>/DECISIONS.md` | what was decided and why, with evidence | before changing anything that looks odd |
| DESIGN | `docs/<slug>/DESIGN.md` | identity brief, quality bar, art direction, motion, sound, screens | before ANY visual, UI, motion or sound work |
| RESEARCH | `docs/<slug>/RESEARCH.md` + `research/` | verified facts (summary) and the full reports | when a fact matters |
| MONETIZATION | `docs/<slug>/MONETIZATION.md` (optional) | the money model, or "none"; ads, subscription or purchase policy as constants; consent; analytics and privacy decisions | before touching money, data collection, consent or analytics |
| RELEASE | `docs/<slug>/RELEASE.md` (optional) | how a release is built and proved | before building a release |
| `store/` | `docs/<slug>/store/` (with RELEASE; created in Phase 5) | the store texts exactly as pasted, and the claim, rating and privacy-answer tables checked against the code | before changing any store-visible text or privacy answer |

**Supporting folders** (`init_kit.py` creates each with a one-line README):
`docs/<slug>/research/` holds the full reports, derived data and the scripts that produced the
numbers; raw third-party text that may not be committed stays in a local, gitignored
`docs/<slug>/research/raw/` (§11). `docs/<slug>/reference/` holds reference renders, probe code,
and small tests that pin a library's real behaviour, with a README saying "API demos, not code to
copy".

**Optional docs, and one home for each answer.**
- Write MONETIZATION when the product earns money **or** collects data (ads, purchases,
  subscriptions, analytics, crash reports). Its template opens with "Model", so "no money, but crash
  reports" is a valid fill. Keep the file name even when its title says "money and privacy": the
  router and the precedence block name it.
- Write RELEASE when there is a store or a production deploy. RELEASE owns `store/`.
- MONETIZATION holds the *decisions* (what is collected and why, the banned-word list, the claims
  policy). `store/` holds what the forms and pages actually say: `text/<store>/`, `LISTING.md`,
  `RATINGS.md`, `PRIVACY_ANSWERS.md` (shapes: `references/release-and-store.md` §5.1 and §7).

**One doc per question.** A new concern becomes a section of the doc whose question it answers. A
genuinely new doc (a feel doc split from DESIGN, say) joins CLAUDE.md's reading order and the
precedence block in the same commit.

### Scaffolding: variants, markers and the check

The exact command is in `references/kickoff.md` §8 (and `SKILL.md` §Scripts). What it does:
- **`--kind game|app`** (required) keeps the matching variant wherever the templates differ by
  product type: invariants, PLAN's Phase 1–3 criteria, the gate question, the quality-bar extras,
  the examples. `--with-monetization` and `--with-release` add the optional docs, and the router
  and precedence lines that name them. Without a flag, no file mentions the missing doc.
- **One marker form.** Every slot reads `[TODO: what goes here]`. A placeholder left without a value
  becomes `[TODO: NAME]`. Guidance comments (`<!-- … -->`) are deleted once their section is filled.
- **`{{OWNER}}`** is the owner's name or the words "the owner". No template starts a sentence or a
  heading with it, so either value reads correctly.
- **The check:** `python3 <skill-dir>/scripts/init_kit.py --check --dest <project-root> --slug <slug>`
  lists every remaining `[TODO` marker by file and line and exits 1 while any remain. Use it, not a
  hand-written grep: a grep pattern copied into PROGRESS matches its own line and never comes back
  clean. Slots only a later phase can fill, in any doc, take the "Written in Phase" line (§12).
- **Existing files** are never touched. With `--retrofit`, a run whose targets exist writes the
  whole kit to a staging folder for a hand merge (`references/planning-and-slices.md` §10).

## 3. Precedence: which doc wins

Write this block into CLAUDE.md and the builder skill (the templates drop the clauses for optional
docs the kit does not have):

> **When the docs conflict:** PROGRESS and PLAN decide *what next*; DECISIONS and ARCHITECTURE
> decide *how*; RESEARCH decides *the facts*; DESIGN decides *the look and feel*; MONETIZATION
> decides *money and data*; RELEASE and `store/` decide *how a release is built and proved, and what
> the store pages say*.

The rules beneath it:
1. **The run beats every doc.** If PROGRESS says green and the baseline is red, the baseline wins.
   In an earlier game, "PROGRESS says green" was wrong twice.
2. **The owner's recorded answers outrank the plan.** Record each as a DECISIONS entry naming the
   plan rule it relaxes, and annotate the plan line. *Example (shipped puzzle game):* the owner
   relaxed "nothing in Phase 3 before a gate yes" to "no upload before my approval after device
   testing", and every phase proceeded. An answer still marked ASSUMED (§6 rule 13) is your
   recommendation, not the owner's word: it never outranks anything permanent.
3. **Research is evidence, not the plan.** Every report carries "Kept as evidence; DECISIONS wins
   where they differ." *Example:* research proposed the first interstitial at level 8 and 6 minutes;
   after the adversarial review, and with competitors' free periods measured at 14–45 levels, the
   decision became level 20 and 8 minutes. A suggested subtitle used a competitor's title; refused.
4. **Within a pair, the newer recorded decision wins, and the older text is fixed in the same
   commit.** *Example:* an entry replaced ARCHITECTURE's "temp file + rename" save with one
   key-value string, said "supersedes ARCHITECTURE §7", and §7 was rewritten.
5. **Code and docs.** ARCHITECTURE opens with: "If a change doesn't fit this shape, either the
   change is in the wrong place or this document needs updating first. Decide which before writing
   code." A real conflict is fixed in the docs first, then the code.
6. **The builder skill restates invariants; DECISIONS is their source.** If they differ, the skill
   is wrong. *Example (sort game):* the skill still said "input is refused during a pour" after
   DECISIONS had changed it to "not gated; hurry the one in flight", and a session built to it.

## 4. CLAUDE.md: the thin router

Every session starts here, so every line must be worth reading every time. Aim for one screen,
60–90 lines. Template: `assets/templates/CLAUDE.md`.

Shape, in order:
1. **Title** (project and product name), then **two or three lines:** what it is, the platforms, how
   it earns (or that it does not), the audience and UI language.
2. **The rule:** the core mechanic or domain invariant in one exact sentence; the tests judge the
   user or the data by it. *Example (shipped puzzle game):* "draw ONE path through every cell exactly
   once, orthogonally, visiting the numbered cells 1…k in order, never crossing a wall." *Example
   (a trial run on an expense-splitting app):* "balances are derived from the group's expense log,
   identically to the cent on every phone."
3. **"Read `.claude/skills/<slug>-builder/SKILL.md` before writing any code."** Then the reading
   order, one clause per doc, with conditional triggers ("DESIGN: read before ANY visual, UI,
   animation or sound work"), then the precedence block (§3). Optional docs appear only if the kit
   has them.
4. **The baseline:** commands in one code block, fastest first, each with a trailing
   `# ~N s: what it covers`. Then: "If the tree is not green when you arrive, fixing that is the
   task. Verify it yourself rather than trusting PROGRESS." First find out whether the code or the
   environment is red. *Example:* a copy of the repo without `.git` failed release-tooling tests
   that read git history; in the real tree they passed. In a retrofit, "green" means no failure
   outside PROGRESS's quarantine list, and an evidence probe that fails by design stays out of this
   block.
5. **The two things to understand first:** the correctness guarantee and how it is enforced; and
   the edge the product lives or dies by, with its evidence *and its confound*. *Example:* "every
   level is proven" (generated offline, re-proved in CI, the user judged by the rules), and "the
   look is the product's edge" (a charming competitor led a field of plain look-alikes, but its
   publisher's marketing confounds that, so the store page matters too).
6. **House rules that bite:** 10–15 bullets. A rule belongs here only if a capable newcomer would
   plausibly break it *and* a test, grep or script can check it. Each bullet cites its DECISIONS
   entry and names its enforcement. Typical kinds: import bans per layer and a banned UI-kit
   import; the exact state-library version, with no code generation; per-frame values off the
   state store; the project's banned words in user-facing and store text; monetisation placement
   rules; one notation for sizes or money; device and orientation scope; "every renderer has a test
   that actually paints it"; never run the platform's bare project generator (use the setup
   script); end every session by updating PROGRESS.
7. **Precedents:** earlier projects this one inherits from, and what each is the precedent for.
   Name only what lives in the repo or in this skill; a fresh session cannot open another project's
   files or memory notes. *Incident:* a PROGRESS file said "read these by path" for three notes in
   another project's memory, a dead link for anyone else. Copy the content in.

Keep out of CLAUDE.md: status (PROGRESS), history and reasons (DECISIONS), tutorials, anything that
changes per session.

## 5. The builder skill and its trap log

The builder skill lives at `.claude/skills/<slug>-builder/SKILL.md`. Its subject is *how to work on
this project*, addressed to any model. It is not a description of the code. Template: the folder
`assets/templates/project-skill/` (the file is named `SKILL.md.template`, so this skill holds only
one SKILL.md; the init script writes it under its real name). It is the strongest template in the
kit; fill it with care.

**Frontmatter description formula:** "Operating method for building and shipping <product>, built
with <stack>. Hard bans: <bans>. Use this whenever ANY model works on <slug>. It teaches HOW to work
here — <the 4–6 verbs of the method>. Read with docs/<slug>/<doc list> before writing code." Keep it
under 1,024 characters, with no angle brackets in the filled text (skill validators reject them).

**Body order:**
1. One paragraph: the product, the stack, the lineage. Then two directives: the thinking goes into
   the docs; and the owner's real judging criterion, in words that forbid the easy failure ("a green
   test suite under programmer art is a failure").
2. §0 **Orient** (three lines). §1 **The method**, made specific: how correctness is proven, the
   layers, state rules, verify by running, verify by looking (three looks), feel tuned on a device,
   slices, never fabricate an API (and where the real sources live on this machine).
3. §2 **Non-negotiable invariants,** numbered; each cites its DECISIONS entry and names its guard.
   §3 **Definition of done:** this project's copy of the canonical list, in its order
   (`references/planning-and-slices.md` §6), with only the project specifics added.
4. §4 **Handoff,** naming the PROGRESS sections (§9). §5 **When stuck, and what to ask the owner,**
   including the owner's profile: a non-technical commissioner who wants you to decide, or a
   developer-owner who wants to co-decide (`references/working-with-the-owner.md`).
5. §6 **Traps.**

Keep §0–§5 to about 100–150 lines; they change rarely. §6 grows every session. In the shipped
puzzle game it reached about 900 lines: about 300 entries under 31 dated headings, in four days.

**Invariant slots** (fill per project; delete what does not apply; each needs an enforcement):
- *Every product:* motion never blocks input, and motion off gives identical outcomes · money rules
  as constants, each with a failing-without test · the project's banned words · art provenance ·
  every renderer has paint and bounds tests, with fonts loaded in tests · saves atomic and versioned
  · no production secrets or ids in the repo · an accessibility baseline · nothing outward without
  the owner.
- *Games:* every shipped item proven · the player judged by the rules, never by a stored answer ·
  fairness promises (free undo, no lives or timers) · promises about content access.
- *Apps:* a user's data is never lost, duplicated or misdated · every mutating request to a server
  is idempotent (a local-only app writes "none: no requests (DECISIONS #n)") · derived values
  (balances, streaks, totals) are computed from stored facts, never stored as counters · what stays
  free stays free.

### The trap log (§6)

**Append-only, dated, grouped by when the trap was found:**
- `### Inherited (these bite here first)`: seeded at kickoff from `references/traps.md`, only what
  applies to this stack and domain. In the source, traps inherited from two earlier games bit first.
- `### Inherited (from this project's history)`: retrofit only. One entry per fix commit or issue
  that names a mechanism, citing the commit.
- `### Found by research (YYYY-MM-DD)`: written before code exists, naming the version researched.
  Eleven such traps (a state library's automatic retry of failing loads, a gesture recogniser's
  start delay, a solver's memory at the largest board…) prevented bugs instead of recording them.
- `### Hit in <phase/slice> — <topic> (YYYY-MM-DD)`, one per slice, and separately `### Hit in the
  <slice> fixer pass (YYYY-MM-DD)`: review findings are a different class (they passed the slice's
  own tests). Nine fixer-pass headings held about 74 entries.

**Entry format** (canonical for every project log): mechanism → incident → fix → guard.
```
- **<Mechanism, as a general sentence>.** <What happened here, with numbers>. <Fix>. (<guarding test or tool>)
```
The mechanism comes first so the reader can generalise, the incident so they believe it, the fix so
they can act, and the guard so they know it is held. *Example:* "**A translucent cue over a varied
background vanishes.** Hint dots at 35% alpha measured 1.2–1.7:1 on every theme's tiles. Drawn
opaque in the palette's rim colour, which carries the ≥ 3:1 rule. (contrast test over every theme by
day and night, with a negative control)".

**Rules:**
1. Write the trap in the session that hit it; lessons written the same session rarely survived to a
   third occurrence. Trap bodies live in the skill; PROGRESS lists titles only.
2. Mark a repeat "(again)" and never delete either entry: a repeat proves the log is read but not
   remembered. In the source, three traps recurred: shell word-splitting in a zsh loop, a language
   keyword used as a pattern name, and awaiting a stream cancel inside a widget test.
3. **Promote a trap the second time it bites** into a mechanical check (a lint, a script check, a
   template line, a guard test, or a CLAUDE.md house rule), so it stops depending on memory. Add
   "promoted to <check>" to the entry.
4. **Convert catalogue entries when you copy them.** `references/traps.md` numbers its entries T-n;
   that numbering belongs to the catalogue. In the project log, write the entry in the format above,
   with "Here:" and how it applies or already bit in this project, and end with "(catalogue T-n)".
   An inherited entry may be one line: `- **<Mechanism>.** <Fix>. (catalogue T-n)`.

## 6. DECISIONS: the append-only log

The decision log is the spine of the method. Template: `assets/templates/DECISIONS.md` (it contains
a filled example entry).

**Header:** the rules ("Each entry records what was decided and why. Don't relitigate an entry
without new evidence. If evidence changes, add a new entry that supersedes the old one; don't
rewrite history."); an evidence line (the research tracks with their date, then **both** review
tallies: "research review: n findings, m confirmed; kit review: f findings, c confirmed, all
addressed", or one combined tally if the review covered both; "cite a report when you add an
entry"); the ASSUMED rule (rule 13); and the notation and terms, defined once. "Sizes are rows×cols
everywhere" stopped width/height transpositions across a game's generator, data and app; "money is
an integer number of minor units" does the same job in an app.

**The first entries:** #1 the product and its one rule; #2 the decision-rights matrix per domain
(`references/kickoff.md` §3); then the owner's answers and the kickoff decisions.

**Entry format:**
```
### #N — <Subject>: <the decision as a rule> (<YYYY-MM-DD>, <phase/slice>[, <review | fixer pass | owner>][; amends #M's "<clause>"])[ **ASSUMED**]
**Context:** <the problem, one or two lines>
**Evidence:** <numbers: counts, measurements, prices, ratios; cite research/<file>>
**Decided:** <the rule, with constant names and values; where it lives; the one file that imports X>
**Rejected:** <alternative> — <concrete, quantified reason>
**Consequences:** <costs accepted; what to re-check if X changes>
**Guarded:** <test or tool> — <what it measures>; seen to fail by <mutation>
**Accepted, recorded:** <known gap> — <why tolerable; which side it errs on>
**Unverified:** <claim> — <the exact command or device step that would verify it>
**Open:** <a judgement for the owner, for ears, or for a device>
**Revisit only if:** <measurable trigger> [and who must approve]
```
A small entry needs Context, Decided and a reason; a substantial one carries every block with content.

**Rules:**
1. **The title is the rule,** not a topic label: "Judge by the rules, never by the stored solution";
   "An interstitial is counted as it is handed to the SDK, not when it closes".
2. **Evidence before opinion.** Use numbers from research or measurement. *Example:* "ad frequency is
   32% of 1–3★ reviews" became "never mid-level; first interstitial after level 20".
3. **Rejected alternatives carry concrete reasons,** so the next agent does not "discover" them
   again. *Examples:* "a third-party plugin: a solo fork, 33 downloads, drops events"; "an offscreen
   mask per part per frame".
4. **Honesty blocks.** For each claim ask "did a tool here observe this, or am I inferring it?"
   Inferred claims go under **Unverified** with the step that would verify them. **Accepted** says
   which side a gap errs on ("unknown entitlement counts as a buyer: a buyer never sees an ad; a
   non-buyer may miss one"). Unverified and Open items are copied into PROGRESS's Device checks or
   END-OF-PROJECT LIST; they write the release checklist.
5. **As-built entries:** "<feature>, as built; amends #N", naming files, constants with values,
   deviations from the plan and why, and review fixes. Without one, a plan that proved impossible
   stays in the log looking authoritative.
6. **Amendments link both ends.** The new title says "amends #M's '<clause>'"; the old entry gets
   one bold line, `**Amended by #N:** <one-line new state>.` In a log of ~120 entries, ~20 were
   amended (one launch screen through three entries), and every chain stayed readable.
7. **Never relitigate without new evidence, but a reason that proves false *is* new evidence.**
   *Example (sort game):* "deliberately not doing a daily mode: it needs a content pipeline" was
   simply wrong (a seeded generator already existed, 0.27 ms a day). A new entry reopened it.
8. **Correct openly:** `*(Corrected <when>: the first record said "<X>".)*` beside the corrected
   sentence. *Example:* an entry claimed a redesigned part kept "the same length". The fixer measured
   0.34 H against 0.31 H, and the entry was corrected in place, with the note.
9. **Owner answers are entries:** "#N — <owner>'s answers to <the question block> (<date>)". Write
   "asked in <language> on <date>, answered <date>", then numbered items, each with its consequence
   for the plan and the ASSUMED entry it confirms or supersedes.
10. **Review and fixer entries** list each finding as scenario → fix → guard seen to fail, plus a
    "Tests that could not fail" sub-list (*example:* six plugin-call bounds could be deleted with
    everything green, because the fake answered at once). Tag rules born from a finding with its id
    ("(skeptic H3)"), so each rule is traceable to the risk it closes.
11. **Lanes that may not edit DECISIONS** report their decisions; the integrator records them,
    marked "Recorded after the fact". **Exceptions** are explicit, narrow, and carry an exit condition.
12. **Plan-B triggers are written in advance:** "Trigger: the <checkpoint> fails, after three looks,
    on any of: <three testable criteria>. Then ask the owner ONE money question." Record the outcome
    as its own entry ("The mascot checkpoint passed; no external animator").
13. **ASSUMED answers.** Questions never block research. When an owner answer has not arrived, adopt
    the recommendation you sent, as an entry whose title ends **ASSUMED**, and list it in PROGRESS's
    ASSUMED answers table. Nothing permanent (a name, an app or bundle id, a product id, a paid
    vendor, published text) may rest on an ASSUMED entry; Gate 0 is where those must be confirmed.
    When the answer arrives, a new entry confirms or supersedes it; never edit the ASSUMED entry.

## 7. ARCHITECTURE: an executable contract

Template: `assets/templates/ARCHITECTURE.md`. Layer design and the guard's mechanics are in
`references/architecture.md` §1–§2. The doc's shape:

1. **Open with the precedence sentence** (§3, rule 5).
2. **§1 Directories and allowed imports:** a table with the columns Directory | Holds | Internal
   imports allowed | External imports allowed; composition-root files get their own rows.
   - A test parses this markdown table and fails until it equals the encoded rules ("change
     ARCHITECTURE §1 and the rules file together"). A directory with no row fails, so every new
     folder is a deliberate decision. Keep the cell forms the parser knows, "nothing" included.
   - **One-file exceptions** go in a bullet list with a fixed prefix, parsed by the same test:
     `- **One-file exception** (DECISIONS #n): <file> may import <uri> with exactly show A, B, for
     <why>. Narrow it when <condition>.`
   - **Retrofit: legacy rows with a ratchet.** The table states the target; today's code is
     admitted as rows or exceptions marked `LEGACY (expires: <slice>)`. The guard fails on a new
     violation and on an expired row, never on a recorded one, so the list can only shrink
     (`references/planning-and-slices.md` §10).
   - **Amendments** go under the table, never as silent row edits: `**Amended YYYY-MM-DD**
     (<phase/slice>; DECISIONS #n): <what was added, why, guarded by …>`.
   - *Incident:* the guard's first run showed the doc, read literally, forbade what the code needed.
     The doc was amended first, then the encoding.
3. **One SDK, one importer:** for each SDK with side effects, name the one file allowed to import
   it; a test lists every importer and compares the list exactly.
4. **The remaining sections:** §2 core model (pure) · §3 content or data pipeline, with its
   versioned data contract, frozen before lanes split; for an app (`--kind app`), three more slots:
   the authority per kind of data, the actions shown optimistically or held as pending, and the
   conflict rule per field (`references/domain-apps.md` §6) · §4 state (a name | kind | holds
   table, plus the rules) · §5 rendering (# | layer | repaints when | kept as, plus a dated block of
   the renderer's measured costs) · §6 input numbers (slop, commit band, grab radius) · §7 services
   (one bullet per port: package and version, never-throws, test seams; and a Call | Bound |
   Fallback | Why that side is safe table) · §8 generated platform folders (what the setup script
   writes and verifies).
5. **"Where new things go"** table: You are adding | It goes in | And you must also. *Example:* a new
   screen also joins the accessibility and device-size audits, in the same commit.

## 8. DESIGN: conventions that keep the look decided

Template: `assets/templates/DESIGN.md`. What goes in it (identity, art-direction rules, tokens,
material or surface system, type, motion, sound) is in `references/visual-design.md` and
`references/motion-and-feel.md`. These conventions keep it trustworthy:

1. **Header:** "Read before any visual, UI, animation or sound work. PLAN says *when*, ARCHITECTURE
   *where*, DECISIONS *why*; this says *what it must be like*. Values marked *Proposed* are starting
   values to tune on a device. Record each change here with the reason."
2. **The identity brief comes first** (`references/kickoff.md` §Identity): statement, leak check,
   hero, lightings, feel brief, sound brief, voice, "what we will not be", the edge, rejected
   directions, the plan-B trigger; its art-direction rules go to DESIGN §2.1. It is this project's
   own; this skill's examples show methods, never a default look. Later sections point to it
   rather than restating it.
3. **"Quality bar (read before any visual work)"** follows: the seven questions and two edge checks
   in short form, each with *this project's* reading (canonical text: `references/visual-design.md`,
   "The quality bar"), the domain extras that apply (G… for games, A… for apps), the three-look loop,
   comparison with the category winners, "the owner sees only final-quality work", and the reference
   renders. Link to the skill for the reasons; don't paste them.
4. **The legend: Verified** (on the web with URL and date, in the installed SDK source with its
   version, or by a render) / **Proposed** (a choice with reasons; numbers tuned on a device) /
   **Unverified** (marked where it appears). It kept tuned numbers from passing as measured ones.
5. **"Decisions at a glance":** a Question | Decision table, including the rejections ("not X, not
   Y"). It answers a new session's first questions without reading 900 lines, and it stops rejected
   options being relitigated. A row the identity brief already answers says "see Identity brief".
6. **Technology verdicts,** one per candidate: Verdict · Verified (version, licence, renders under
   the test runner) · The catch · Allowed uses · Plan B. Prefer what the builder can create, diff and
   test as text (`references/kickoff.md` §5.4).
7. **Per screen or effect, a "Plan (written before building)" and an "As built".** The plan:
   layout; exact words for every state; what is NOT on the screen; motion and sound cues;
   semantics; text-size behaviour; acceptance renders by file name. The As built (three looks;
   render folder): Look 1, what was wrong; Look 2, what changed; Look 3, accepted; the test that
   guards the result and what it asserts; a fixer-pass line when one applies. *Example:* a
   purchases sheet's sync line. In Look 1 the glyph sat in its own column and drifted to the
   card's edge when the text wrapped; in Look 2 it rode inline in the paragraph; Look 3 tightened
   the gap from 7 to 5 pt at 2× text and accepted it. Motion tables label each number "set from
   renders" or "set on a device".
8. **Hard details get numbered versions,** each with what it read as (*example:* a mascot's ears:
   v1 read as stuck-on pads, v2 lost the rim, v3 left a pale cap, v4 faded the shadow, v5 shipped),
   so nobody retries a rejected version. **Tuned numbers keep their history** (old → new, why, on
   which device), so nobody reverts a tuned value to the first guess.
9. **After any probe or prototype, write three lists:** what it proved, what looking at it found,
   what it did not prove. The did-not-prove items become acceptance items in PLAN. Add an honest
   judgement of your own art against the benchmark, with plan B, its cost, and the seam that makes
   swapping cheap.
10. **Close with "Unverified and open questions" and "Sources"** (URL, date queried, SDK version).

## 9. PROGRESS: the handoff, in eleven fixed sections

Template: `assets/templates/PROGRESS.md` (canonical for the sections; it contains a filled example
Done entry). Any fresh session, or a different model, must be able to act from this file alone. It
is rewritten as the last act of every session and as part of every slice's definition of done.

**Fixed sections, fixed names, fixed order:**
1. Current phase
2. Done
3. In progress, ending with "**The exact next step:** …"
4. Next (ordered)
5. How to verify the current state
6. Open questions (the `When | Ask` table, the messages drafted but not yet sent, the ASSUMED
   answers)
7. Device checks (what tests could not prove)
8. END-OF-PROJECT LIST FOR <owner>
9. Standing owner preferences
10. Traps hit (index)
11. Small open items (not blocking)

The cold-start path is Current phase → In progress → How to verify; Done is the record.

**Current phase:** one dense paragraph: phase number and name, a bold status ("built and
committed", "in review", "in progress"), date, commit hashes, what it delivered, then **What is
left:** (1–3 items). Then standing hazards as conditionals: "If X changes, redo Y before Z: check C
only checks <format>, not <content>." *Example:* "If the mascot painter changes again, re-record the
app preview before the upload: the preview check reads only the file's format, not what it shows",
written after a painter change had already left a stale preview once.

**Done entries** all share one anatomy: title · date · commit · decisions and doc sections touched ·
how it was built (lanes) · what was built (paths, numbers) · tests +N (before → after) · mutation
proofs, k of n killed by assertion (harness, logs) · looked at (≥ 3 looks, files, what each look
found) · the results line for every gate · **Not run / not verified, and why** · the fixer pass. Use
numbers, not adjectives: "3,474 passing (3,353 before)". When a gate was not re-run, give a reason
someone can check: "no native or manifest change (diffed), so the setup script's runs stand". In a
retrofit the first entry is **State on adoption** (`references/planning-and-slices.md` §10).

**In progress:** "Nothing in flight; the tree is green" (only after running the whole How-to-verify
block), or the half-done state exactly: "<slice> — in the working tree, not committed: lanes A and B
done; C has <what>". Then the hazards: files never to replace (a real config pair that a
fake-config tool must not overwrite), and gitignored outputs with the commands that regenerate
them. Then **The exact next step**, in one sentence.

**Next:** ordered; finished items are struck, never deleted (`~~<item>~~ **done** (Done "<entry>";
DECISIONS #n). <residual>`), which keeps residuals in view ("still waits for the store pages").

**How to verify:** a copy-paste block, fastest check first, each command with
`# what it proves (~time; expect <count>)`. Mark checks that need a device, credentials or a
generated tree. Put lines like "If X changes on purpose: regenerate with Y, then Z" under the
block. Update the counts at every commit. A count that does not match a fresh run is a finding.
**Retrofit:** a quarantine table (`| Test | Why it fails | Owning slice | Expires |`) sits under the
block. A red test is listed there, never silently skipped; green means no failure outside it.

**Open questions:** a `When | Ask` table, never a backlog. Each question waits for its moment (a
gate, a phase start, the end of the project). Strike answered rows and write "**Answered <date>:**
<answer>". Some rows are conditional ("Only if the mascot checkpoint fails | budget for an
animator"). Below it, the **Messages drafted, not yet sent** line (dated and verbatim: a question
block or the Gate 0 message waiting for its moment, or "none"), so a drafted message is neither
lost nor sent twice; then the **ASSUMED answers** table (`| DECISIONS # | Assumed | Permanent? |
Confirm by |`), and one line on the owner: their language, what to ask them, what never to ask.

**Device checks:** everything a test could not prove, written so it can be run as written:
`<Area>: on <oldest supported device>, with <flag or tool>: <scenario>; pass = <observable result>;
write the numbers in <doc §>`. Group them as `references/working-with-the-owner.md` §12 lists.
DECISIONS' Unverified items land here. This section becomes the first group of the
END-OF-PROJECT LIST, by reference, not by copy.

**END-OF-PROJECT LIST:** everything only the owner can do, accumulated as you go and asked once
(item anatomy: `references/working-with-the-owner.md` §13).

**Standing owner preferences:** each standing preference or boundary (the release gate, the owner's
language, bans, authorisations granted and where you were rightly stopped) as rule, why, how to
apply, date. If the environment keeps memory notes for *this* project, write the note there too
and name it here; never write into another project's memory.

**Traps hit:** titles, plus a pointer to the builder skill's dated heading, where the bodies live.

**Small open items:** each known weakness you chose not to fix, why it is fine for now, and what would
close it. *Examples:* "archive targets are exactly 44.0 pt on a 360 pt phone, with no slack"; "undo
history is an unbounded chain, fine for real sessions; cap it if needed". Record here, too, what you
checked and deliberately left alone, with the measured reason.

**Truthfulness rules:** PROGRESS is code: stale "not committed" labels and wrong counts are defects
(replace the labels with hashes). Record every side effect on a real external system and how the
owner should treat it (*examples:* error probes on a release build reached the real crash-reporting
project, "ignore them"; a simulator recording wrote a save into the owner's real cloud account).
Record each authorisation the owner gave (what, date, what was done), and anything you were rightly
stopped from changing, as a precise instruction for the owner.

## 10. PLAN

Template: `assets/templates/PLAN.md`. Its content (phases, acceptance by running, the vertical
slice, gates, slice sizing, retrofit) is in `references/planning-and-slices.md`. The doc's shape:
1. **Goal** (from kickoff, `references/kickoff.md` §12.1): the owner's words verbatim, the gate
   question, what was rejected before, the release lever. Then **the first question block, exactly
   as sent**, with its date and, as answers arrive, the DECISIONS entry each became.
2. **How the plan works:** "a phase is done only when every acceptance criterion has been verified
   by running something"; the slice pipeline in its canonical order; the phase order; the notation;
   with a deadline, the calendar line (`references/planning-and-slices.md` §1, small product
   profile).
3. **One block per phase:** **In the phase** / **Not in the phase** / **Checkpoint** (risky assets
   only) / **Accept when** (runnable checks only, with numbers) / **Gate prerequisites** / **Gate**
   (the delivery route and the one question). Slices inside a phase use **In the slice / Not in the
   slice**. In a retrofit, Phase 0 is the **adoption baseline**.
4. **The phase that brings each dependency.** Wrong criteria are struck with a dated correction,
   never deleted.

## 11. RESEARCH, and keeping evidence honest

Template: `assets/templates/RESEARCH.md`. The research method is in `references/kickoff.md`
§Research. RESEARCH.md is a short summary of verified facts. The full reports live in `research/`.
- **Summary shape:** "summary of verified facts, <date>" → a Report | Covers table → where the
  derived data lives → a moved-files table (old scratch path → repo path) → sections for Market,
  Users (complaint and love tables with counts), Feasibility (measured), Stack (verified on this
  machine, with versions), Money, Legal and store eligibility (statuses with dates).
- **Each report:** the repo note "kept as evidence; DECISIONS wins" → the status legend → for
  competitor reports, "Corrections to the brief" → evidence with sources → the proposal → a closing
  "Not verified" list → sources (URL and date) → files.
- **Reports are evidence; never edit one silently.** A factual error found later goes in an
  **Errata** block at the top of the report (date, what was wrong, what is right, the review id),
  plus the DECISIONS entry that acts on it. The body stays as written, so the reasoning that led to
  earlier decisions stays readable.
- **What may be committed.** Always: the scripts, the query date and parameters, and the derived
  counts. Raw third-party text (store reviews, forum posts) only when its licence and the authors'
  privacy allow; otherwise keep it in a local, gitignored `research/raw/` and state the gap under
  "Not verified" (a re-run will differ: review feeds return the newest reviews). Competitor
  screenshots never enter the repo.
- **Move research out of the scratchpad into the repo before anything depends on it;** scratch
  paths vanish. **Volatile facts** (versions, store rules, law) carry a date; re-check them at each
  phase and at release, and supersede a wrong entry openly. *Example:* a law's start date was
  recorded a year early; the re-check at implementation time caught it, and a later entry fixed it.

## 12. MONETIZATION, RELEASE and `store/` (optional docs)

**MONETIZATION** (`assets/templates/MONETIZATION.md`; the rules are in
`references/monetization-and-privacy.md`). Shape:
- **Model first:** the chosen model (ads, one-time unlock, consumables, subscription, paid upfront,
  or none) with its evidence, and what stays free.
- **Then only the model's own sections** (the template carries all three; delete those the model
  has none of): ads (interstitial rule table counted in the product's unit of play, level, run,
  round or task, rewarded placements, "As built"), subscription (paywall placement, trial and renewal disclosure, restore, grace and
  billing retry, price changes, cancellation, the entitlement rule) or purchases (id, permanent |
  type | price | gives). Every rule is a named constant with a test that fails without it.
- **Always:** "Not used, and why" → SDKs (dated) → consent and the tracking prompt → analytics,
  crash reports and privacy decisions → audience, age, backup and the fallback store art → listing
  decisions (banned words, claims policy; the texts live in `store/`) → revenue arithmetic,
  labelled "a sanity check only".

**RELEASE** (`assets/templates/RELEASE.md`; the content is in `references/release-and-store.md` §4).
Shape: the line "Nothing here sends anything to a store" → §0 inputs (Input | Where | Without it) →
§1 baseline → §2 regenerate the platform folders and set the owner's version numbers (never
invented, never reused) → §3/§4 per platform → §5 what a passing run does NOT prove → §6 reference
numbers (dated, with the commit) → §7 side effects of a release build → §8 the `store/` folder.

**`store/`** is created in Phase 5 by the release work: `text/<store>/` (one file per store text,
exactly as pasted, held to a registry), `LISTING.md` (the claim and length tables, the screenshot
caption list, the decisions made in the copy), `RATINGS.md`, `PRIVACY_ANSWERS.md`. Shapes and
checks: `references/release-and-store.md` §5 and §7.

**Slots only a later phase can fill, in every kit doc** (not only the optional ones). At kickoff,
fill what is decided (for MONETIZATION: the model, what stays free, the banned words, the
audience). Replace each slot that only a later phase can fill with one line, "Written in Phase
<n.m>; decided so far: <…>"; that phase re-reads the template section when it writes it. Typical
ones: a renderer cost measured on a device (ARCHITECTURE §5), the input numbers as built (§6), the
motion table's device values and the haptics table (DESIGN), a probe's proved / found / not-proved
lists, every release number. A slot that does not apply gets "none: <reason> (DECISIONS #n)" (no
services, no SDKs, one lighting). Then whatever the TODO check still lists is a real gap.
*Incidents:* in a trial adoption the two optional docs carried 36 slots no one could fill until
Phases 4 and 5; in a trial on a one-screen utility the core docs still showed 150 markers after a
complete kickoff fill, many of them device measurements and as-built tables. Neither check could
tell those from real gaps.

## 13. Docs that tests parse

Wherever a doc states a rule or a number the code must match, make the doc the single source and
have a test read it. Pairs that held: ARCHITECTURE §1 ↔ the import guard; DESIGN's contrast figures
↔ the palette tests (±0.01); DESIGN's sound table ↔ the sound-pack test; the store-claims table ↔
the code each claim names. Two pairs that had drifted before they were joined: a beat map copied
into the sound generator (600–1300 ms there, 450–1350 ms in the app), and two banned-word lists,
where the shorter one let eight banned words through the screenshot captions.

Rules:
1. **A parsed doc is an API.** Put a comment above the table naming the test and its format rules.
   *Example:* a sound table parsed by rule "rows starting with a pipe and a backtick are cue rows; a
   later row wins". A second table in that doc must not start its rows with a backticked id.
2. **Assert non-vacuity** (the parser found the expected rows) before comparing; the failure names
   both files to change. **Expect the first run to find the doc wrong:** amend the doc (the contract)
   first, then the code.
3. **Tests compare with the spec's literal numbers,** never with the code constant they protect
   (`expect(scale, 0.96)`, not `expect(scale, Press.scale)`), or they parse the doc. More in
   `references/verification.md`.

## 14. Maintenance rules for every doc

1. **A slice updates every doc it touched, in the same commit.** Its Done entry lists them:
   DECISIONS #.., DESIGN §.. As built, ARCHITECTURE §.., MONETIZATION, the skill's trap heading.
2. **Strike, don't delete** finished Next items, wrong criteria and answered questions:
   `~~old~~ **Corrected <date>:** new, because <reason>`. **Correct openly,** never silently.
   Research reports take an Errata block instead (§11).
3. **Stale lines are defects.** At integration, grep for every number and phrase a lane changed.
   *Examples:* "15 uniforms" survived in five files after a 16th was added; a comment said 109 where
   the docs said 110 (measured: 110).
4. **Reasons go stale, so give each one a check.** *Example:* a ratings doc said "the app has no web
   access", which became false when a privacy-policy link landed.
5. **The repo is self-contained:** research, probes, reference renders and release procedures all
   live in it. **Volatile facts carry dates** and the instruction to re-verify. **Notation and terms
   are defined once,** then used identically in code, data and docs.
6. **No secrets or production ids in any doc:** gitignored env files, with a committed `.example`
   holding the vendor's sample values. **Language:** docs use one working language; questions go to
   the owner in theirs, recorded as "asked in <language> on <date>" with the gist translated.

## 15. Kit health checklist

Run it as part of the kit review's BUILDABILITY lens before Gate 0 (`references/kickoff.md` §9),
and again whenever a session finds the docs disagreeing with each other.

- [ ] `python3 <skill-dir>/scripts/init_kit.py --check --dest <project-root> --slug <slug>` exits 0:
      no `[TODO` marker is left, later-phase slots hold their "Written in Phase" line, slots that do
      not apply say "none: <reason>", and the guidance comments of filled sections are gone.
- [ ] CLAUDE.md fits one screen: one exact core rule, a timed baseline, the precedence block, house
      rules that each cite a DECISIONS entry and an enforcement, and optional docs named only if
      they exist.
- [ ] The builder skill has both directives, numbered invariants each naming its guard, a
      definition of done in the canonical order with this project's sizes and themes, and traps
      seeded from the catalogue (converted to the project format), from research and, in a
      retrofit, from the project's history.
- [ ] The DECISIONS header has the evidence line with the review tallies, the ASSUMED rule and the
      notation; #2 holds the decision-rights matrix; every title is a rule; owner answers are
      verbatim with dates; substantial entries carry the honesty blocks.
- [ ] ARCHITECTURE §1 is in the parser's table form (in a retrofit, LEGACY rows with expiries), and
      the guard is the first guard item of PLAN Phase 0. Seeing it fail belongs to Phase 0's exit,
      not to this review.
- [ ] DESIGN opens with this project's own identity brief (lightings, feel and sound briefs, "what
      we will not be", the plan-B trigger), then the quality bar with this project's readings, the
      legend, Decisions at a glance, the technology verdicts, and empty Plan / As built slots for
      the Phase 2 screens.
- [ ] PROGRESS has its eleven sections, a one-sentence exact next step, How-to-verify counts that
      match a fresh run, the timing table, and every open ASSUMED answer listed.
- [ ] PLAN opens with the goal and the first question block as sent; every phase has In / Not in;
      every acceptance criterion is runnable; the owner gate names its delivery route and the one
      question for this product's use pattern.
- [ ] RESEARCH tags facts Verified or Unverified, dates volatile facts, keeps reports in the repo,
      and states any raw data kept out of it.
- [ ] No ASSUMED answer has made anything permanent; no path outside the repo; no committed secret;
      no other product's name in user-facing text.
