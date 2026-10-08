# ARCHITECTURE — {{PROJECT_NAME}}

The contract you build to. If a change doesn't fit this shape, either the change is in the wrong
place or this document needs updating first. Decide which before writing code.

<!-- flagship-method template. Layer design: flagship-method references/architecture.md. Doc shape
and maintenance: references/project-kit.md §7. Stack: {{STACK}}. Flutter rows:
references/stack-flutter.md §Layers; other stacks: references/stack-other.md §1.
A section that does not apply (no services, no network) says "none: <reason> (DECISIONS #n)". A
slot only a later phase can fill (a device measurement, as-built input numbers) gets one line
instead of a guess: "Written in Phase <n.m>; decided so far: <…>"
(references/project-kit.md §12). -->

## 1. Directories and allowed imports (the guard test enforces this literally)

<!-- Parsed by the architecture guard test (name it here once it exists; PLAN Phase 0, first guard).
The test fails until this table and the encoded rules are identical: change both together. Keep the
cell forms the parser understands (code spans, "as `x/`", "plus …", "everything", "everything
except X", "nothing"). A directory with no row fails, so a new folder is a deliberate decision. The
rows below are an example shape; replace them with this project's layers.
Retrofit: this table states the TARGET. Admit today's code as rows or exceptions marked
`LEGACY (expires: <slice>)`; the guard fails on any new violation and on an expired row, never on a
recorded one, so the legacy list can only shrink (flagship-method references/planning-and-slices.md
§10; guard mechanics: references/architecture.md §2.5). -->

| Directory | Holds | Internal imports allowed | External imports allowed |
|---|---|---|---|
| `[TODO: src/core/]` | rules, models, the save model, policies, ports, null objects | `[TODO: src/core/]` | the standard library only |
| `[TODO: src/state/]` | the reactive store: notifiers, providers, view models | core, state | the state library, pinned exactly |
| `[TODO: src/services/]` | port implementations (one SDK per file) | core, services | each SDK in exactly one file (§7) |
| `[TODO: src/theme/]` | design tokens, palettes, type, the surface recipe | theme | the drawing API only |
| `[TODO: src/render/]` | renderers; engine types wrapped in our own types | core, render, theme | the drawing API, not the widget layer |
| `[TODO: src/motion/]` | choreography, one ticker each | core, render, theme | no timers, no state, no services |
| `[TODO: src/widgets/, src/screens/]` | UI | everything except services and the root | the UI toolkit, not raw engine types |
| `[TODO: root files]` | the composition root | everything | everything except [TODO: the banned UI kit, or "nothing banned"] |

**Nothing below the composition root imports it.** Exports count as imports, and every URI of a
conditional import counts.

**One-file exceptions** (parsed by the guard test; each has an exit condition):
<!-- - **One-file exception** (DECISIONS #n): `<file>` may import `<uri>` with exactly `show A, B`,
  for <why>. Narrow it when <condition>. -->

**Notes on the table:**
<!-- - **Amended YYYY-MM-DD** (<phase/slice>; DECISIONS #n): <what was added, why, guarded by
  <test>>. Never edit a row silently. -->

## 2. Core model (pure)

[TODO: the domain types and the rules, in a few lines each. The core has no clock inside: time is
passed in.]
<!-- kind:game -->
[TODO: the judge: the player is judged by the rules, never by comparison with a stored answer.]
<!-- /kind:game -->
<!-- kind:app -->
[TODO: the derived values (balances, totals, streaks): computed from stored facts, never stored as
counters; money as integer minor units, if any.]
<!-- /kind:app -->

## 3. Content / data pipeline and its contract

<!-- kind:game -->
[TODO: offline generator → shipped asset → re-proved in CI by an independent verifier.]
<!-- /kind:game -->
<!-- kind:app -->
[TODO: the data layer: local store, migrations, seed fixtures.]

**Authority per kind of data** (flagship-method references/domain-apps.md §6, item 6.1; one row per
kind; DECISIONS #[TODO: n]):

| Data | Shape | Who decides | How copies merge |
|---|---|---|---|
| [TODO: e.g. check-ins] | [TODO: one device; one user on several devices; shared between people; server-authoritative] | [TODO: the device / the join / the operation log / the server] | [TODO: the rule] |

<!-- Shared or server data only; delete the rest of this block for data that stays on one person's
devices. Mutations go through an operation log with idempotency keys (domain-apps §6, items 6.2–6.3). -->
**Optimistic or pending** (item 6.4): optimistic, shown at once and reconciled: [TODO: actions];
pending, waiting for the server's answer: [TODO: e.g. pay, book, send].

**Conflict rule per field** (item 6.5):

| Field | Kind | Rule |
|---|---|---|
| [TODO: field] | [TODO: free text / set / counter / money / list order / edit against delete] | [TODO: the rule chosen] |
<!-- /kind:app -->

**The data contract (format [TODO: 1]):** [TODO: the exact fields and types, the notation, the
version number.] Freeze it here before lanes split. A change of format is a DECISIONS entry and a
version bump.

## 4. State

| Name | Kind | Holds |
|---|---|---|
| [TODO: name] | [TODO: kind] | [TODO: what it holds] |

Rules:
1. State is immutable. Every change makes a new value; a no-op returns the identical instance.
2. Per-frame values (fingers, springs, poses, particles) never go through the store. They live in
   animation objects owned by the view that paints them.
3. The model commits first and emits events; the choreography catches up.
4. Loads that must surface a failure are not retried automatically.

## 5. Rendering

| # | Layer | Repaints when | Kept as |
|---|---|---|---|
| 1 | [TODO: e.g. background] | [TODO: e.g. on theme change only] | [TODO: e.g. a cached picture] |

Anything on its own clock gets its own layer. How the budget is proved: [TODO: a frame-budget test
that checks each moment repaints only its own layers, or this stack's substitute
(flagship-method references/stack-other.md §7), with its DECISIONS entry].

> **Dated facts (renderer cost, measured on [TODO: device] on [TODO: date] — re-measure on
> change):** [TODO: what the renderer charges for: blurs, save layers, shaders, path complexity.]

## 6. Input

[TODO: the numbers that define the feel of input (touch slop, commit band, grab radius) and how a
cancelled gesture is discarded, not submitted. As-built notes go here, dated.]

## 7. Services (ports and their one implementation each)

<!-- A product with no SDK or platform service writes "none: <reason> (DECISIONS #n)" here and keeps
the bounds table for its own platform calls (the save read, file access). One bullet per port:
- **<Port>** → `<file>` (<package> <exact version>, read in source on <date>): never throws into
  the app; no platform channel touched at construction (it connects in `start()`); test seam: <how
  fakes are injected>; null object: <name>. -->

| Call | Bound | Fallback | Why that side is safe |
|---|---|---|---|
| [TODO: e.g. the save read] | [TODO: e.g. 3 s] | [TODO: e.g. refuse writes for the session] | [TODO: e.g. a fresh profile could replace a real save] |

## 8. Platform folders (generated)

[TODO: if the platform folders are generated, keep this paragraph; if they are committed and edited
by hand, replace it with the written policy (flagship-method references/stack-other.md §15) or
"none: <reason> (DECISIONS #n)".] The platform folders are generated by `[TODO: setup script]` and
never edited by hand. The script
validates its inputs before deleting anything, applies each edit, verifies each edit, re-verifies
everything on the final tree, and produces byte-identical output on a second run.
[TODO: what it writes: display name, orientation, device family, permissions, privacy manifest,
icons, launch screen, SDK ids from gitignored env files.]

## Where new things go

| You are adding | It goes in | And you must also |
|---|---|---|
| a screen | `[TODO: screens dir]` | add it to the accessibility and device-size audits in the same commit |
| an SDK | one file in `[TODO: services dir]` behind a port | add its row or exception in §1, a null object, a strict-fake adapter test, its row in §7 |
| a saved field | the save model in `[TODO: core dir]` | bump the save version; read every older version exactly; refuse newer |
| a renderer | `[TODO: render dir]` | a paint test and a bounds test, and add it to the render harness |
