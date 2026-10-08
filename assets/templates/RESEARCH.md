# RESEARCH — {{PROJECT_NAME}} (summary of verified facts, {{DATE}})

This file is the summary. The evidence is in the track reports in `research/`, each with its sources
and an explicit "Not verified" list. **The reports are kept as evidence: where they differ from
DECISIONS, DECISIONS wins.** A report found wrong later gets a dated **Errata** block at its top and
a DECISIONS entry; its body is never edited silently.

<!-- flagship-method template. Research method: flagship-method references/kickoff.md §Research;
keeping evidence: references/project-kit.md §11. Tag every fact Verified (web with URL and date,
installed source with version, or a run you did), Proposed (a choice with reasons), or Unverified
(marked where it appears). Move every report, probe and data file out of the scratchpad into the
repo before anything depends on it. A slot only a later phase can fill gets one line instead of a
guess: "Written in Phase <n.m>; decided so far: <…>". -->

| Report | Covers |
|---|---|
| `research/competitors.md` | [TODO: n competitors; n reviews coded by script; installs; how they earn] |
| `research/feasibility.md` | [TODO: probes that ran, with measured numbers] |
| `research/stack.md` | [TODO: versions, APIs read in source, behaviour pinned by tests] |
| `research/design.md` | [TODO: the winners' visual language; the identity probes] |
| `research/money-legal.md` | [TODO: prices and the money model's evidence; name and trademark checks; store eligibility for the owner's region; law] |

**Data:** `research/data/` holds [TODO: the coding scripts, their query dates and parameters, and the
derived counts; benchmarks; name and store check scripts]. [TODO: where raw third-party text is
kept: in the repo only if its licence and the authors' privacy allow (a DECISIONS entry);
otherwise in `research/raw/`, which `research/.gitignore` keeps out of git, with the gap stated
under "Not verified".] Competitor screenshots never enter the repo. `docs/{{SLUG}}/reference/`
holds renders and probe code.

**Moved files.** Scratch paths vanish at the end of a session; the canonical copies are:

| Old scratch path | Repo path |
|---|---|
| [TODO: scratch path] | [TODO: repo path] |

---

## Market

[TODO: demand and supply, with numbers and dates. Corrections to the brief, each with the datum that
refutes it.]

## Users

<!-- From the coded reviews: complaints (1–3★) and loves (4–5★), with counts per theme. Store
averages hide anger, so add the mean of recent written reviews beside each average. -->

| Complaint (1–3★) | Count | The rule it implies |
|---|---|---|
| [TODO: theme] | [TODO: n] | [TODO: rule] |

| Love (4–5★) | Count | The pillar it implies |
|---|---|---|
| [TODO: theme] | [TODO: n] | [TODO: pillar] |

## Feasibility (measured)

[TODO: what a probe actually ran, the numbers, the hardware and concurrency, and what it did not
prove.]

## Stack (verified on this machine)

> **Dated facts (as of {{DATE}} — re-verify before relying):** [TODO: SDK and package versions, and
> the behaviours read in their source.]

## Money

[TODO: the evidence by design strength (randomised > survey > observational > vendor case study);
the arithmetic, labelled "a sanity check only"; or "no money", with the reason.]

## Legal and store eligibility

> **Dated facts (as of {{DATE}} — re-verify before relying):** [TODO: name and trademark screening
> results ("not legal advice"); whether the owner can hold developer accounts and receive payouts in
> the target stores from their region; store rules by guideline number; law statuses with their
> dates. Re-check at each release.]

## Not verified

- [TODO: each claim no tool here could confirm, and what would confirm it.]
