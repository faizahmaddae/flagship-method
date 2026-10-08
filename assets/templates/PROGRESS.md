# PROGRESS — {{PROJECT_NAME}}

<!-- flagship-method template: the handoff. Any fresh session, or a different model, must be able
to act from this file alone. The eleven sections below have fixed names and a fixed order, because
tools and agents look for them; never add, rename or reorder one. Rewrite the file as the last act
of every session. Use numbers, not adjectives, and paths, not descriptions. The cold-start path is
Current phase → In progress → How to verify. A slot only a later phase can fill gets one line
instead of a guess: "Written in Phase <n.m>; decided so far: <…>".
How to write each section: flagship-method references/project-kit.md §9. -->

## Current phase

Kit (before Phase 0), **in review** ({{DATE}}). [TODO: what this phase delivered, in 2–3 lines,
with commit hashes.] **What is left:** [TODO: 1–3 ordered items.] Nothing has been uploaded or
published: any upload waits for an explicit request from {{OWNER}}, and anything public waits for
their device test and approval.
<!-- Add standing hazards as conditionals: "If <X> changes, redo <Y> before <Z>: <check C> only
checks <format>, not <content>." -->

## Done

<!-- One entry per slice, oldest first. Shape:
- **<Phase/slice title>** (<YYYY-MM-DD>; committed as <hash>). <How it was built: lanes, integration,
  review counts>. DECISIONS #..; DESIGN §..; ARCHITECTURE §..; traps "Hit in <slice>".
  - **<Area>:** <what was built, with file paths and key numbers>.
  - **Tests** (+N: <before> → <after>): <files, and what each proves>.
  - **Mutation proofs** (isolated copy <path>; harness <path>; logs <path>): **k of n killed by
    assertions, none a compile error**: <list>. Survivors: <what they taught>.
  - **Looked at** (≥ 3 looks; <render folder>): look 1 <found>; look 2 <found>; look 3 <accepted>.
  - **Results:** analysis clean; tests <count> passing (<before>); <every tool selftest, with its
    case count>; setup twice byte-identical (<n> files). **Not run:** <device or store items, and
    why>. When a gate was not re-run, give a checkable reason ("no native change: diffed").
  - **Fixer pass** (<n> findings, each verified first): (1) **<symptom in user terms>** (<root
    cause>): <fix>; guard <test> seen to fail without it. (2) … Mutation proofs: k of k. Docs
    amended: ….

Retrofit only: the first entry records the tree as found, before any adoption commit:
- **State on adoption** (<YYYY-MM-DD>; at <hash>). What exists and what was verified by running:
  - **Code:** <files and layers as found; UI kit and state library; save keys; SDKs and their ids,
    sample ids included; app ids and platform flags>.
  - **Baseline:** <analysis; tests: n passing, m failing (each failing test goes to the quarantine
    table under How to verify)>; `git status --short` after the first build: <what the toolchain
    rewrote>.
  - **Content or data:** <the proof probe's verdicts>.
  - **Looked at** (<render folder>): <what the as-found looks found; the quality bar's answers>.
  - **Not run / not verified, and why:** <...>.

Example (shipped puzzle game, shortened; the shape is the point, delete it once you have your own
entries):
- **Phase 4 slice 4.6 — age signals and progress sync between devices** (2026-10-05; committed
  as <hash>). DECISIONS #108 (the merge rule for every field), #109 (age signals); DESIGN screen 11
  "As built"; ARCHITECTURE §1 (amended), §4, §7; the skill's traps "Hit in Phase 4 slice 4.6".
  (Shortened to the sync part.)
  - **Save v6** = v5 + a per-install ledger of numbers that only grow; a pure merge in the core;
    sync after the first frame, on every change event, on resume, 5 s after the last change and at
    once on leaving; never before the cloud copy is read, never a fresh profile, never over a newer
    build's copy.
  - **Tests** (+148: 3,820 → 3,968), among them: every field's merge rule; the join's algebra over
    24 random histories; five 400-step two-phone histories through last-writer-wins against a model,
    identical at the end with every count exact.
  - **Mutation proofs** (isolated copy): **49 of 49 killed by assertions, none a compile error.** The
    first run had 2 survivors: an equality check blind to the ledger (the test also changed the
    counters; it now builds documents that differ only in the ledger) and "a newer copy does not
    halt sync" (two guards held one rule; the test now also asserts the copy is never read again).
  - **Looked at:** the settings sync line, three looks (render folder named).
  - **Results:** analysis clean; 3,976 passing, 1 skipped; setup script twice byte-identical (93
    files); debug builds pass on both platforms. **Not run:** sync between two real phones (a device
    check).
  - **Fixer pass** (6 findings, each verified first), among them: **a reinstall that finished
    today's daily before the cloud copy arrived lost a 13-day streak** (the merged settled day
    counted a side with no kept day): fixed; two settled-day tests seen to fail without it. New
    guards: 7 of 7 mutations killed by assertions.
-->

## In progress

Nothing in flight; the tree is green. <!-- Only after running the whole "How to verify" block.
Otherwise describe half-done work exactly: "<slice> — in the working tree, not committed: <done>;
<not done>". Then the hazards: files that must never be replaced, and gitignored outputs with the
commands that regenerate them. -->

**The exact next step:** [TODO: one sentence.]

## Next (ordered)

1. [TODO: the next item, with the runnable check that will accept it.]
<!-- Never delete a finished item. Strike it and point to where it was done:
1. ~~<item>~~ **done** (Done "<entry>"; DECISIONS #n). <residual, if any>. -->

## How to verify the current state

```bash
[TODO: command]   # what it proves (~time; expect <count>)
[TODO: command]   # what it proves (~time; expect <count>)
```
<!-- Fastest and most fundamental first. Mark checks that need a device, credentials or a generated
tree. Update the counts at every commit; a count that does not match a fresh run is a finding.
Under the block: "If <X> changes on purpose: regenerate with <Y>, then <Z>."

Retrofit only: the quarantine table. A failing test is listed here, never silently skipped; the
baseline is green when nothing fails outside this table. Name an evidence probe that fails by
design as such, and keep it out of the CLAUDE.md baseline.
| Test | Why it fails | Owning slice | Expires |
|---|---|---|---|
| <test name> | <cause, as found> | <phase/slice that fixes it> | <slice or date> | -->

## Open questions

| When | Ask |
|---|---|
| Before the Phase 2 gate build | [TODO: e.g. which phone they will use; confirm the permanent name and app id] |
<!-- A question waits for its moment. Strike answered rows and write the answer in place:
| ~~<moment>~~ | **Answered <date>:** <answer> |
Conditional rows are fine: | Only if <checkpoint> fails | <question> |
The first question block, exactly as sent, lives in PLAN "Goal". -->

**Messages drafted, not yet sent** (dated, verbatim; e.g. a question block or the Gate 0 message
waiting for its moment): none.

**ASSUMED answers** (recommendations adopted while the owner's answer is pending; nothing permanent
rests on them, and Gate 0 confirms the permanent ones):

| DECISIONS # | Assumed (our recommendation) | Permanent? | Confirm by |
|---|---|---|---|
| [TODO: n, or "none"] | [TODO: the recommendation adopted] | [TODO: yes / no] | [TODO: Gate 0 / a phase start] |

**Asking {{OWNER}}:** in {{OWNER_LANGUAGE}}, briefly, numbered, each with a recommendation.
[TODO: what to ask them, and what never to ask them.]

## Device checks

<!-- Everything tests could not prove, written so it can be run as written, grouped by area (core
feel and the signature moment; haptics and touch latency; sound on the speaker and on headphones;
permission and consent prompts; money flows in test mode; sync between two devices; screen reader;
a launch in every lighting the product ships; a frame log on the oldest supported phone).
DECISIONS' Unverified items land here. This section becomes the first group of the END-OF-PROJECT
LIST, by reference. Item shape:
- <Area>: on <oldest supported device>, with <flag or tool>: <scenario>; pass = <observable result>;
  fail looks like <…>; write the numbers in <doc §>. -->

- [TODO: the first device check, or "none yet"]

## END-OF-PROJECT LIST FOR {{OWNER}} (asked in {{OWNER_LANGUAGE}}, in one go, when the product is ready; nothing before)

<!-- Everything only the owner can do: accounts, consoles, keys, money, legal choices, approvals.
Accumulate it here and keep building everything else meanwhile. Group 1 is always the device
testing: "the Device checks above, runnable as written". Each other item stands alone:
1. **<Area> (DECISIONS #..):** in <console> → <menu path>: <action> with **<exact values>** (flag
   anything that can never be changed). Then <command>. <Order constraint, e.g. "before the build
   goes to review">. <What to check on the device>. <Fallback if the judgement goes the other way>.
Item anatomy: flagship-method references/working-with-the-owner.md §13. -->

1. **Device testing:** the Device checks above.

## Standing owner preferences

<!-- Each standing preference or boundary: the release gate, the owner's language, bans,
authorisations granted (scope, date) and where you were rightly stopped. Shape:
- **<Rule>** (<date>). Why: <the owner's reason>. How to apply: <do / don't>.
If the environment keeps memory notes for THIS project, write the note there too and name it here.
Never write into another project's memory. -->

- **No upload of any kind without an explicit request, and nothing public before a device test and
  approval** (the method's default, {{DATE}}). Why: the release lever belongs to the owner. How to
  apply: do all other work, release preparation included; never upload, publish or change an
  account setting unasked. Replace this line with the owner's own words once they state the rule.

## Traps hit

<!-- Titles only, plus a pointer: "<slice>'s traps are in the builder skill §6 ('Hit in <slice>'):
<title>; <title>." The bodies live in the skill. -->

## Small open items (not blocking)

<!-- - <known weakness>; <why it is fine for now>; <what would close it>.
Also record here what you checked and deliberately left alone, with the measured reason, so the
next session does not redo the check. -->
