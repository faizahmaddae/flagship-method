# {{PROJECT_NAME}}

<!-- flagship-method template: the thin router every session reads first.
Keep it to one screen (60–90 lines). Status belongs in PROGRESS, history and reasons in DECISIONS.
Fill every TODO marker from the kickoff evidence; delete these guidance comments once the section
is filled. A slot only a later phase can fill (the baseline timings before Phase 0 exists) gets one
line instead of a guess: "Written in Phase <n.m>; decided so far: <…>". How to write each part:
flagship-method references/project-kit.md §4. -->

{{ONE_LINE}} For {{PLATFORMS}}, built with {{STACK}}. [TODO: how it earns (or "no money"), the
audience, and the language of the UI.]

**The rule:** [TODO: the core mechanic or domain invariant in ONE exact sentence. The tests judge
the user or the data by this sentence, so write it precisely.]

**Read `.claude/skills/{{SLUG}}-builder/SKILL.md` before writing any code.**

## Orientation (every session, no exceptions)

1. `docs/{{SLUG}}/PROGRESS.md`: where we are, and the exact next step.
2. `docs/{{SLUG}}/PLAN.md`: the goal, the phases and acceptance criteria. Phase 2 ends in a gate
   with {{OWNER}}.
3. `docs/{{SLUG}}/ARCHITECTURE.md`: the layer contract (a test enforces its §1 table), state usage
   and the pipelines.
4. `docs/{{SLUG}}/DECISIONS.md`: why things are this way. Don't relitigate them without new evidence.
5. `docs/{{SLUG}}/DESIGN.md`: **read before ANY visual, UI, animation or sound work.** Its identity
   brief and "Quality bar" sections are mandatory.
6. `docs/{{SLUG}}/RESEARCH.md`: verified facts, with the full reports in `docs/{{SLUG}}/research/`.
<!-- if:monetization -->
- `docs/{{SLUG}}/MONETIZATION.md`: **read before touching money, purchases, ads, analytics, consent
  or privacy decisions.**
<!-- /if:monetization -->
<!-- if:release -->
- `docs/{{SLUG}}/RELEASE.md`: **read before building a release.** `docs/{{SLUG}}/store/` holds
  every store text and its checks; read it before changing anything a store shows.
<!-- /if:release -->

**When the docs conflict:**
- PROGRESS and PLAN decide *what next*;
- DECISIONS and ARCHITECTURE decide *how*;
- RESEARCH decides *the facts*;
- DESIGN decides *the look and feel*;
<!-- if:monetization -->
- MONETIZATION decides *money and data*;
<!-- /if:monetization -->
<!-- if:release -->
- RELEASE and `store/` decide *how a release is built and proved, and what the store pages say*;
<!-- /if:release -->
- a run beats any doc. A real conflict is fixed in the docs first, in the same commit as the code.

## Verify the baseline before you continue

```bash
[TODO: the fastest, most fundamental check]   # ~N s: what it proves
[TODO: static analysis]                       # ~N s
[TODO: the full test suite]                   # ~N min: includes the architecture guard and the verifier
```
<!-- Order: fastest and most fundamental first. Keep the timings honest; update them when they drift.
Example (Flutter): `flutter analyze` then `flutter test`. Other stacks: the analyzer gate and the
test command per stack in flagship-method references/stack-other.md ("Baseline commands"), each
probed before it is trusted.
Example (content pipeline): `python3 tool/build_<content>.py selftest   # ~20 s: solver, grader,
every builder guard` and `python3 tool/build_<content>.py verify   # ~12 s: re-proves the shipped pack`.
Retrofit: green means no failure outside the quarantine list in PROGRESS "How to verify". An
evidence probe that fails by design stays out of this block, or the baseline is red forever. -->

If the tree is not green when you arrive, **fixing that is the task**. Verify it yourself rather than
trusting PROGRESS. First find out whether the code or the environment is red.

## The two things to understand first

1. **[TODO: the correctness guarantee, in a few words].**
<!-- kind:game -->
   - [TODO: how it is enforced, e.g. "every level is generated offline and re-proved in CI by an
     independent solver".]
   - [TODO: how the player is judged, e.g. "by the rules, never by comparison with a stored answer".]
<!-- /kind:game -->
<!-- kind:app -->
   - [TODO: how it is enforced, e.g. "every write commits locally first and survives a crash; the
     save reads every older version exactly and refuses a newer one".]
   - [TODO: how a user's data is kept right, e.g. "balances and totals are derived from stored
     facts, never stored as counters".]
<!-- /kind:app -->
2. **[TODO: the edge this product lives or dies by].**
   - [TODO: the evidence for it, with its confound stated.]
   - [TODO: the named edge items from the identity brief.]
   - How it looks and feels is what {{OWNER}} judges. Build to DESIGN.md's bar, and look at what
     you made.

## House rules that bite

<!-- 10–15 rules a capable newcomer would plausibly break. Each one must be checkable by a test, a
grep or a script, and must cite the DECISIONS entry that justifies it. Kinds that earned a place in
past projects (examples, not defaults): import bans per layer; a banned UI-kit import; the exact
state-library version with no code generation; state is immutable; per-frame values never go through
the state store; the project's banned words in user-facing and store text; money placement rules;
one notation (a puzzle game: sizes as rows×cols; a money app: integer minor units); device and
orientation scope; every renderer has a test that actually paints it; never run the platform's bare
project generator over the repo (use the setup script). A trap that bites twice gets promoted to a
rule here. -->

- [TODO: rule] (DECISIONS #[TODO: n]; enforced by [TODO: test or script]).
- [TODO: rule] (DECISIONS #[TODO: n]; enforced by [TODO: test or script]).
- Nothing outward or irreversible (any upload, a test track included; publishing; a purchase; an
  account setting) happens without {{OWNER}}'s explicit request or approval for that specific step.
- End every session by updating `docs/{{SLUG}}/PROGRESS.md`.

## Precedents

<!-- Earlier projects whose method or code this one inherits, and exactly what each is the precedent
for. Name only what lives in this repo or in the flagship-method skill: a fresh session cannot open
another project's files or memory notes, so copy what matters into this repo. Delete the section if
there are none. -->

- This project follows the flagship-method skill (the method and the quality bar).
