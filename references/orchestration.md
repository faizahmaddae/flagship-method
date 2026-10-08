# Orchestration

How to split a slice across agents without losing quality, and how to run the same pipeline alone.
The pipeline itself, its order and its definition of done live in
`references/planning-and-slices.md` §5–§6; this file says who runs each step. In the source project
the quality came from the tail of every workflow (review → fixer → mutation proofs → checker), not
from the fan-out. Cut parallelism when you must; never cut the tail.

**Read when:** a slice has two or more parts that can be built independently; you are writing a
prompt for another agent; agent work was interrupted; multi-agent tools are unavailable and you need
the same rigour alone (§11).

## Contents
1. When to orchestrate
2. Foundation inline, then fan out
3. Contract-first parallelism
4. Ownership and integration
5. The shared context block
6. Report schemas and triage
7. Topologies
8. Prompt skeletons
9. Recovery and continuity
10. Effort and models
11. Solo fallback
12. Orchestration checklist

---

## 1. When to orchestrate

Orchestrate when at least one holds:
- the slice splits into 2–8 parts that own disjoint files (lanes);
- the slice is risky (money, saved data, lifecycle, platform policy, release) and needs independent
  review;
- a decision needs several sources read in parallel: a dependency, a sister integration, your own
  rules, current platform facts;
- an audit must cover many screens, states or content items.

Stay single-agent when the change is one tightly coupled edit, when the shared foundation does not
exist yet (lay it first, §2), or when writing the context block would cost more than the work.

*Example (shipped puzzle game):* the whole product, from scaffold to store-ready, took about 2.2
calendar days: 22 workflows, ~157 subagents, ~50 agent-hours. A typical slice used 6–10 agents for
1.5–3 h; the largest (six themed worlds and the meta screens in parallel) used 13 agents for 5 h.
The owner wrote about a dozen short messages in total; the method and the docs carried the work.

---

## 2. Foundation inline, then fan out

Before any lane starts, the lead writes every shared file itself, so no lane blocks another or edits
a shared file:
- the dependency manifest and lockfile, lint config, fonts, and design tokens (reproduce the design
  doc's contrast figures exactly before writing tokens);
- data contracts with their fixtures, and shared test helpers (font loading, raster helpers, port
  fakes);
- stub files and registry or manifest entries for everything lanes will add. *Example:* an
  architecture lane created all five themed-world stubs and registered their shader files, "so the
  world lanes never edit" the manifest.

Record the HEAD hash and the green baseline ("tree green: N tests, analyzer clean") of the
foundation. Every lane builds on it and every reviewer diffs against it.

---

## 3. Contract-first parallelism

1. **Write the contract into the shared context before building:** the data format with a version
   number; exact type, function and constructor names and signatures; shared constants (caps,
   epochs). Say "other lanes code against exactly these names".
2. **Decouple with primitive inputs.** *Example:* the solver lane took primitive inputs only (no
   import of the puzzle type), so it was built and tested before the engine existed.
3. **Give the downstream lane a compiling placeholder** to replace. One lane created a minimal
   placeholder screen component that compiled, put its exact constructor in its report, and the next
   lane replaced it.
4. **Freeze before the split.** A data format changes only on both sides at once, with a version
   bump. *Example:* the level format was fixed in the architecture doc before a generator lane (one
   language) and engine and solver lanes (another language) ran in parallel. They integrated with
   node-for-node parity on 206 shared fixtures.
5. **Make the integrator own the cross-check** that proves the lanes fit: a verifier over every
   shipped item, a parity test, a composition test.

---

## 4. Ownership and integration

Every lane prompt states these rules:
- An explicit list of files the lane owns; touch nothing else. A needed change outside the lane goes
  in `openIssues`, and the integrator applies it.
- Run only your own tests. Wait for shared tool locks instead of fighting them.
- Format only the files you changed, never the whole tree or a glob.
- Destructive controls and mutations run only in an isolated copy with a lane-unique scratch name
  (`references/verification.md` §9).
- Never commit, upload, touch consoles or accounts, add secrets, create fake config, or write memory
  notes. Only the lead commits, after its own verification, and only the lead writes memory notes,
  into this project's memory alone (`references/traps.md` T-17, T-17f).
- Never fabricate an API: read the real source in the dependency cache or SDK.

Lane splits that worked (2–8 lanes): scaffold in 4 (setup script · architecture guards · fonts and
palette tests · render and app shell); content in 3 (generator · engine · solver); painters in 2
(board · mascot); the play loop as a sequence (state ∥ sound → board → screen); meta screens in 8;
polish in 4 (night · polish · accessibility · social); ads foundation in 3 (native tooling · core
wiring · visuals); release prep in 3 (store copy · screenshots and preview · icon).

**Integration is a phase with its own findings:** merge and apply every `openIssues` change → one
owner per rule and one latest version per saved document (several lanes bumped the same settings
schema; the integrator made one version that reads every older one) → grep for stale numbers and
phrases any lane changed (109 in code vs 110 in docs; "15 uniforms" in five files) → invert "still a
stub" tests → see each new guard fail → generators twice, byte-identical → debug builds on every
platform → cold launch and look. Integration found bugs no lane saw: the entry point threw a type
error before the first frame, "so the app never left its launch screen".

---

## 5. The shared context block

Every agent prompt starts with the same block, so no agent needs session memory. Keep it in one
constant and prepend it to every role's prompt.

```
CONTEXT
Repo <path>, branch <b>, HEAD <hash>; tree green: <N> tests, analyzer clean.
Built so far: <one paragraph>.
OWNER'S ANSWERS: <verbatim gist, dated>. ASSUMED until answered: <…>. Decided by the lead (record,
  never ask the owner): <…>.
READ FIRST: CLAUDE.md; the builder skill (.claude/skills/<slug>-builder/SKILL.md) §<traps>;
  docs/<slug>/DESIGN.md §<x>, §<y>; ARCHITECTURE.md §<z>; DECISIONS #<n>, #<m>.
  (Name exact sections and decision numbers, never "read the docs".)
HOUSE RULES THAT BITE (restated for this slice): <import bans>; <test library>; <banned words>;
  <format only touched files>; <every drawing routine has a paint test and a bounds test>.
THE TASK: <scope with numbers>; NOT in this slice: <…>; acceptance: <criteria>.
LANE RULES: you own <files>. Parallel lanes run in this same tree: touch nothing else; report
  outside needs in openIssues; run only your tests; no commit, no upload, no console, no secrets,
  no fake config, no memory notes.
ISOLATION: mutate only in a copy: <recipe or script>.
DEFINITION OF DONE: analyzer clean for your files; your tests green; every new guard SEEN TO FAIL
  once with its protection removed (say how); visual work rendered, every image opened, ≥3 looks
  recorded; docs you made stale updated; honest report: if something failed or you skipped it,
  say so.
NEVER FABRICATE AN API: read the real source at <dependency cache / SDK path>.
Today is <date>. Facts that may have changed since your training: check them and cite them.
```

---

## 6. Report schemas and triage

A structured report makes an agent state what it ran, how its guards failed, what it decided, which
traps it hit and what is still open. The `decisions` and `traps` fields feed `DECISIONS.md` and the
builder skill's trap list after every slice. In the source project those reached about 119
decisions and about 300 trap entries with no separate doc-writing effort.

**BUILD** (builders, finishers):
```json
{ "type": "object",
  "properties": {
    "summary":          {"type": "string"},
    "files":            {"type": "array", "items": {"type": "string"}},
    "renders":          {"type": "array", "items": {"type": "string"}},
    "looks":            {"type": "array", "items": {"type": "object", "properties": {
                           "look": {"type": "integer"}, "wrong": {"type": "string"}, "changed": {"type": "string"}}}},
    "verification":     {"type": "string", "description": "exact commands and results, with counts"},
    "negativeControls": {"type": "string", "description": "how each new guard was seen to fail"},
    "decisions":        {"type": "array", "items": {"type": "string"}, "description": "choice + reason"},
    "traps":            {"type": "array", "items": {"type": "string"}, "description": "mechanism → fix"},
    "openIssues":       {"type": "array", "items": {"type": "string"}, "description": "incl. outside-lane needs"} },
  "required": ["summary", "files", "verification", "negativeControls", "openIssues"] }
```

**REVIEW** (one per lens):
```json
{ "type": "object",
  "properties": {
    "findings": {"type": "array", "items": {"type": "object", "properties": {
        "severity": {"enum": ["high", "medium", "low"]},
        "file":     {"type": "string"},
        "problem":  {"type": "string"},
        "evidence": {"type": "string", "description": "what you ran or read that proves it"},
        "fix":      {"type": "string"}},
      "required": ["severity", "file", "problem", "evidence", "fix"]}},
    "visualVerdict": {"type": "string", "description": "honest judgement against the quality bar (seven questions, two edge checks)"},
    "verdict":       {"type": "string"}
  },
  "required": ["findings", "verdict"] }
```

**FIX**: one entry per finding `{id, verdict: fixed|rejected, evidence, change, guard, proof}`, then
the final verification line. **CHECK**: plain text (green or not, exact counts, problems).
**RESEARCH reader**: `{report: markdown with file:line and URLs, risks: [string]}`, with anything
unconfirmed marked "unverified".

**Triage in code.** Never ask an agent to triage its own findings:
```
all = for each review i: findings tagged with lens[i]
actionable = all where severity in (high, medium)
if all is empty: skip the fix stage
fixer gets: actionable + "lows: fix the cheap, clearly right ones" + the builder's report
```
Protocol for reviewers, fixer and checker (rules, severities, dispositions):
`references/verification.md` §10.

---

## 7. Topologies

Choose the topology from the dependency graph, not from habit. Every topology ends in the same
tail, steps 7–12 of `references/planning-and-slices.md` §5: adversarial review → fixer → mutation
proofs rerun on the final tree → checker (a confirming look at everything the fixes touched, every
gate re-run) → the lead's own pass, docs and one commit.

| Topology | Shape (before the tail) | Use for |
|---|---|---|
| Pipeline per lane | each lane: build → its own reviewer → its own fixer, no barrier; integrate; the rest of the tail runs once | independent lanes on disjoint files (scaffold, painters) |
| Lanes → integrator | parallel build → integrator writes the cross-check, cold-launches | outputs that must fit (generator + engine + solver) |
| Waves | foundations in parallel → dependent builds → the last build stage also integrates | dependency chains (state ∥ sound → board → screen) |
| Risky slice | research-first → plan and skeptics → build → integrate | ads, purchases, analytics, age rules, sync, release hardening, store prep |
| Research-first | 4 readers → designer → 2 skeptics → brief | go/no-go on a dependency or a policy-heavy design |
| Judge panel | judges by perspective → fixer → re-render → judges again | hero character, icon, key screen, a gate build |
| Audit until dry | critics → triage → skeptics → fixer, repeated | pre-gate audits, after a redesign |
| Finisher | finisher per cut-off role → the usual tail | interrupted work (§9) |

Waves may nest: an architecture lane, then five world lanes in parallel alongside a meta-screens
lane. Tell the last build stage: "you are the LAST build stage: run the whole suite and fix anything
broken between lanes; report every cross-lane change."

**Research-first** (before integrating a risky dependency or a policy-heavy feature):
1. Four read-only readers, one source each: (a) the dependency itself (source, docs, its tests run
   in a temp copy, the published version diffed against the repo); (b) a sister project's
   integration and its traps, if one exists; (c) this project's own rules as a numbered requirements
   checklist with exact sources and code hook points; (d) current platform, store and legal facts
   with URLs, dates and "unverified" marks. Every reader gets the owner's answers so far, verbatim
   and dated, with each open question as an explicit ASSUMED answer: readers who lacked them
   guessed who would make the signing key and who would test, and the brief had to void those
   items (`references/traps.md` T-17b).
2. A designer writes the verdict (yes, yes-with-gaps, or no; each gap classed as handled locally,
   needs an upstream change, or a blocker), the integration design, an ordered slice plan with
   acceptance criteria, what needs the owner, and the open risks.
3. Two skeptics: one tries to refute the verdict from the source; the other attacks the design
   against the project's rules and platform policy and finds gaps in the test plan.
4. The lead writes a brief of numbered decisions (D1…Dn) folding in every accepted skeptic defect,
   archives everything into `docs/<slug>/research/`, and builds slice by slice from the brief.

*Why:* the skeptics could not refute the verdict, but before any code existed they found six design
defects (two would have blocked ads for a whole session or frozen the game) and 12 rules with no
test that failed without them. The brief then carried six slices with nothing new to ask the owner.

Each later slice that touches an external platform starts with its own read-only researcher, whose
report is pasted into the builder's, reviewers' and fixer's context. Researchers answer named
questions: versions and compatibility, behaviour without config, policies, store setup the owner
will need, and a recommended integration. One found the law further along than the notes said,
which turned a planned no-op into real work. The brief had allowed for exactly that: "if research
finds no obligation, build the port plus a no-op, record the decision, and put the re-check on
PROGRESS."

**Judge panel for visuals.** Three judges, each rendering the current state itself and judging it
against the project's own design doc and identity (`references/kickoff.md` §7), never against
another product's look. One perspective each: **the hero itself** (silhouette at real size, light
direction if the style is lit, edges, attachment); **every context** (every screen, size, theme,
accessory, dark mode); **guards and derived assets** (icons, store art and previews regenerated from
the source drawing code). Icons are judged at full and home-screen sizes, under the platform masks,
on light and dark wallpapers, beside genre icons. Each judge returns pass/fail per criterion with
crops as evidence; fix, re-render and judge again until all pass, then the lead looks too
(`references/visual-design.md` §Look loop).

**Audit until dry.** Critics in parallel by perspective (logic and economy, graphics, motion,
language, UX and accessibility) plus play-testers (first run, every mode, stress and edge cases);
one sweep by screen and one by state and sequence; a triage lead merges duplicates; skeptics try to
refute the top of the list against the source; a fixer verifies and fixes. Then a fresh round on the
fixed tree. Stop when a round returns no high or medium findings, or at a fixed cap (three rounds is
a sensible default), and escalate what remains.

*Why (word game):* a 17-agent critique (5 code critics, 3 play-testers, a triage lead, 8 skeptics)
found 4 blockers that 579 green tests had missed, all in the seams between screen, profile, clock
and seed that the tests stubbed; the skeptics refuted one headline finding outright.

---

## 8. Prompt skeletons

Each prompt starts with the CONTEXT block (§5). Pass earlier agents' reports as file paths to read
first, never inline placeholders (§9).

**Builder (lane):**
```
FILES YOUR LANE OWNS: <list>.  SPEC: <doc §§, decision #s>.
YOU ARE THE BUILDER of <lane>. <Task with exact numbers, names and acceptance criteria.>
LOOK: render to <preview dir>; open every image; budget THREE looks; for each, write what was wrong
against DESIGN and what you changed.
PROVE: for each guard you add, remove its protection in an isolated copy and show it fails with its
own message.
Return the BUILD schema.
```

**Reviewer (one lens):**
```
YOU ARE AN ADVERSARIAL REVIEWER of <slice> (uncommitted: git diff against HEAD <hash>, plus
untracked files). The task was: <original task>. The builder's report is at <file>: do not trust
it; verify by reading files and RUNNING things; re-render and re-measure yourself.
Do NOT edit the shared tree; mutate only in an isolated copy under <scratch>/<unique>.
LENS: <one failure mode>. Try specifically: <scenarios>.
Report only real defects, each with evidence (command output, numbers, file:line). Prefer few strong
findings; ignore style nits; an empty list is valid if the work is solid. Also check that the docs
say only true things about the code. Return the REVIEW schema.
```

**"Do the tests prove anything?" reviewer:** the reviewer preamble, plus:
```
LENS: DO THE TESTS PROVE ANYTHING? In an isolated copy (cp -R the whole tree, uncommitted changes
included), apply these mutations one at a time, run only the relevant tests, and record which guard
catches each and whether by assertion or by compile error:
1. <threshold off by one> … N. <the two sides of a cross-check drifting apart>
Every survivor is a finding. Then name one weakening not on the list that you expect to survive,
and try it.
```

**Fixer:**
```
YOU ARE THE FIXER. Builder report: <file>. Findings (JSON): <actionable + lows note>.
For EACH finding: first verify it yourself (reproduce, measure or read). If false or not worth
changing, say why, with evidence. If real, fix it at the root in the shared tree, with a guard that
fails without the fix (prove it in an isolated copy). Re-look at any changed visual. Update docs the
fix makes stale. Then run <full verification>. Do NOT commit.
Return the FIX schema: per finding verdict, change, guard, proof; then counts.
```

**Checker:**
```
YOU ARE THE FINAL INDEPENDENT CHECKER. Do not edit anything. The fixer reported: <file>.
Run <analyzer>, <full suite: exact pass/fail counts, failures verbatim; rerun a lone failure alone>,
<every selftest and verifier>, <each generator and setup script twice: byte-identical?>.
git status; git diff --check; skim the diff for TODOs, debug prints,
placeholders, banned imports or words, hard-coded prices, production ids, personal data, stray
files. Open every new image and give a one-line verdict each. Return a short plain report.
```

**Researcher:**
```
YOU ARE A READ-ONLY RESEARCHER (today is <date>). Edit nothing; if you run a package's tests, copy
it to a fresh temp dir first. Answer: <numbered questions>. Cite file:line for code and URL + date
for web facts; mark anything you could not confirm "unverified". Return the RESEARCH schema.
```

**Designer and skeptics:** the designer gets every reader's report and returns verdict, design,
slice plan, owner needs and risks (§7). Skeptic 1: "Try to REFUTE the verdict; re-check each
decisive claim in the source (file:line)." Skeptic 2: "Attack the design against <rules doc> and
platform policy; find every case where a rule could be broken and every rule with no test that
fails without it."

**Finisher:** the CONTEXT block, the original task text, then the finisher prompt in
`references/planning-and-slices.md` §9, pointed at the predecessor's scratch folder and mutation
logs. Return the BUILD schema.

Pseudo-code for a risky slice, mapped onto whatever orchestration tool you have; the numbers are
the steps of `references/planning-and-slices.md` §5, and every result is saved to a file:
```
brief   = research-first (readers → designer → 2 skeptics)    ; 1 plan, 2 skeptics
lead: freeze contracts and the foundation                      ; 3
build   = agent(CONTEXT + brief_path + BUILDER, effort=high)   ; 4, with its own ≥ 3 looks
lead: integrate, cold launch, analyzer + full suite             ; 5, 6
reviews = parallel([agent(CONTEXT + REVIEWER(lens)) for lens in 3 lenses])   ; 7
fix     = if any findings: agent(CONTEXT + FIXER(actionable))   ; 8
mutate  = agent(CONTEXT + mutation list on a fresh copy of the final tree)   ; 9
check   = agent(CONTEXT + CHECKER)                              ; 10, default effort
lead: own pass → docs (DECISIONS, DESIGN as built, PROGRESS) → one commit   ; 11, 12
```

---

## 9. Recovery and continuity

The interruption procedure (establish the facts first, report to the owner, finish from the tree
with a finisher, never rerun from scratch) lives in `references/planning-and-slices.md` §9. What
orchestration adds:
- **Save every report to a file the moment it returns** (`<scratch>/<slice>_<lane>.md`) and pass
  paths, never inline pastes or placeholders (`references/traps.md` T-9). *Incident:* a relaunch
  passed `{"laneC":"SEE_FILE"}` instead of the report; the lead stopped it within a minute, before it
  changed anything, pointed the script at the saved file, relaunched, and told the owner.
- **Resume a halted workflow by role.** Launch a finisher for each cut-off role and tell it which
  lanes finished ("lane C FINISHED; lanes S and I were cut off mid-work and their PARTIAL work is in
  the tree"), with an inventory of what exists; then run the usual tail on the result.
- **Hand over preconditions.** If a finished lane changed something that takes effect only after a
  generation step, tell the next agents to run that step before judging test results.
- **Concurrency hygiene:** tell each workflow to ignore the other's uncommitted files; do not change
  repo state a running workflow is testing (real config was held aside while a run tested the
  no-config path; `references/traps.md` T-17a); wait for tool locks.
- **Archive research, briefs and skeptic notes** from scratch into `docs/<slug>/research/` before
  later slices depend on them. A session's scratch space is not durable. Archived reports are
  evidence: never edit one silently; a correction goes in a dated "Errata" block at its top plus a
  DECISIONS entry (what to keep, and where: `references/project-kit.md` §11).

---

## 10. Effort and models

- Use high reasoning effort for builders, reviewers and fixers on risky slices, and the default for
  the read-only final checker. Inherit the session's model unless the owner says otherwise.
- Spend the strongest effort where independence matters: reviewers and fixers judge work they did
  not write.
- Put the thinking into the context block and the docs. A prompt that names exact sections,
  numbers and acceptance criteria lets any capable model build at full quality; a vague one does
  not.

> **Dated facts (as of 2026-10 — re-verify before relying):** the workflow tool used in the source
> project capped concurrent agents at about min(16, CPUs − 2) per workflow. Resuming a workflow
> replayed unchanged agent calls from a cache. Agents could take a JSON schema for their final
> report and a per-agent effort setting. Check your own tool's documentation for its current limits
> and API before writing a workflow script.

---

## 11. Solo fallback

When no multi-agent tool exists, run the same pipeline in sequence: the twelve steps of
`references/planning-and-slices.md` §5, in the same order. The multi-agent version works because of
three properties; recreate each deliberately: review independent of authorship, evidence demanded
for every claim, and reports written down.

**Sequence** (step numbers from planning §5)
1. **Plan and attack it (1–2).** Write the plan to a file. After a break, reread it cold against the
   task and the relevant trap groups, one lens per pass, and write the defects down before fixing.
2. **Freeze contracts (3).** Write the foundation and the contract to files first (§2–3).
3. **Build (4)** the lanes one at a time, in dependency order. Each lane meets its own definition of
   done (tests, guards seen to fail, ≥ 3 looks), then writes its BUILD report to
   `<scratch>/<slice>_<lane>.md` as if handing it to a stranger.
4. **Integrate (5–6)** with the checklist (§4), cold launch included; then the analyzer and the full
   suite.
5. **Review as a stranger (7)**, one lens per pass, three passes (one is always "do the tests prove
   anything?"):
   - snapshot first: commit to a branch, or save `git diff <base>`. Review the diff cold, not your
     memory of it;
   - reread the original task and the spec sections *before* the diff, never after;
   - write each lens's scenarios, and the mutation list, before opening the tests or the code, so
     you do not aim them at what you know already passes;
   - re-derive every number you claimed (re-measure, re-render); never quote your own build report;
   - write findings to a file, with evidence and severity, before fixing anything. Fixing while
     reviewing ends the review at the first find;
   - look at renders after a gap, at real size, beside the previous accepted render;
   - for each claim, ask "what evidence would a hostile reviewer demand?", then produce it.
6. **Fix (8):** verify each finding (your own findings can be wrong too); fix with a guard seen to
   fail.
7. **Mutation proofs (9):** rerun the whole list on a fresh copy of the final tree.
8. **Checker pass (10)** in a fresh context if you can get one: a new session, or a single
   fresh-context subagent if any such tool exists, reading only PROGRESS, the diff and the checklist.
   Otherwise run the checklist mechanically, command by command, and paste the counts. Either way,
   look again at everything the fixes touched, and re-run every gate, determinism included.
9. **Docs and one commit (11–12)**, after the lead's pass (`references/verification.md` §10).

**What you lose:** true independence. Compensate with time gaps between building and reviewing,
written checklists, and mutation proofs, which do not depend on who wrote the code. If only a
single-subagent tool exists, spend it on a reviewer, not a builder: independence is worth most there.

---

## 12. Orchestration checklist

- [ ] Foundation and contracts written by the lead; HEAD and the green baseline recorded.
- [ ] Each lane has owned files, exact spec sections and its definition of done. One CONTEXT block
      is shared by every agent, carrying the owner's answers (ASSUMED ones marked).
- [ ] Reports use the schemas and are saved to files the moment they return; paths are passed on,
      never placeholders.
- [ ] An integration pass with its checklist, including a cold launch.
- [ ] Three lenses, one of them "do the tests prove anything?" with an enumerated mutation list.
- [ ] The fixer verified every finding; the mutation list was rerun on the final tree; the checker
      edited nothing and re-ran every gate; the lead ran its own pass.
- [ ] Research archived to `docs/<slug>/research/`; corrections as dated errata, never silent edits.
- [ ] PROGRESS updated, and the owner told what ran, what was found and what is next.
- [ ] No agent committed, uploaded, wrote a memory note or touched an account.
