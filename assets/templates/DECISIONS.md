# DECISIONS — {{PROJECT_NAME}}

Each entry records what was decided and why. **Don't relitigate an entry without new evidence.**
If evidence changes, add a new entry that supersedes the old one; don't rewrite history.

**Evidence:** `research/*.md`, [TODO: n] research tracks written [TODO: date], with their derived
data in `research/data/`. Research review: [TODO: f] findings, [TODO: c] confirmed. Kit review:
[TODO: f] findings, [TODO: c] confirmed, all addressed. (One combined review of both? Give one
tally and say so.) Cite a report when you add an entry.

**ASSUMED answers.** When an answer from {{OWNER}} has not arrived, the recommendation we sent is
adopted provisionally, in an entry whose title ends **ASSUMED**, and listed in PROGRESS "Open
questions". Nothing permanent (a name, an app or bundle id, a product id, a paid vendor, published
text) rests on an ASSUMED entry; Gate 0 confirms those. When the answer arrives, a new entry
confirms or supersedes it; the ASSUMED entry is never edited.

<!-- kind:game -->
**Notation (used everywhere in this repo):** [TODO: e.g. "sizes are rows×cols: a 9×7 board is 9
rows by 7 columns".] **Terms:** [TODO: words with one fixed meaning here.]
<!-- /kind:game -->
<!-- kind:app -->
**Notation (used everywhere in this repo):** [TODO: e.g. "money is an integer number of minor units
of an ISO 4217 currency, never a float or a formatted string".] **Terms:** [TODO: words with one
fixed meaning here, e.g. "member" vs "user".]
<!-- /kind:app -->

<!-- flagship-method template. How to write entries: flagship-method references/project-kit.md §6.
A header slot only a later step can fill (the kit-review tally before the review) reads "Written in
Phase <n.m>; decided so far: <…>" until then.

Entry shape (use the blocks that have content; a substantial entry has most of them):

### #N — <Subject>: <the decision as a rule> (<YYYY-MM-DD>, <phase/slice>[, <review | fixer pass | owner>][; amends #M's "<clause>"])[ **ASSUMED**]
**Context:** <the problem, in one or two lines>
**Evidence:** <numbers: counts, measurements, prices, ratios; cite research/<file>>
**Decided:** <the rule, with constant names and values; where it lives>
**Rejected:** <alternative> — <concrete, quantified reason>
**Consequences:** <costs accepted; what to re-check if X changes>
**Guarded:** <test or tool> — <what it measures>; seen to fail by <mutation>
**Accepted, recorded:** <known gap> — <why it is tolerable; which side it errs on>
**Unverified:** <claim> — <the exact command or device step that would verify it>
**Open:** <a judgement for the owner, for ears, or for a device>
**Revisit only if:** <measurable trigger> [and who must approve]

Rules:
- The title is the rule itself, readable from a table of contents.
- An amended entry gets one bold line: **Amended by #N:** <one-line new state>.
- Correct a wrong statement in place, openly: *(Corrected <when>: the first record said "<X>".)*
- The owner's answers are entries too: "asked in <language> on <date>, answered <date>", each item
  with its consequence and the ASSUMED entry it confirms or supersedes.
- Copy every Unverified item into PROGRESS "Device checks", and every Open item for the owner into
  the END-OF-PROJECT LIST or the "Open questions" table.

Example entry (from a shipped puzzle game, shortened; the shape is the point, delete it when you
have your own):

### #N — A failed save is remembered: the next unchanged commit writes again instead of answering "saved" (2026-10-05, Phase 4 purchases slice, at the commit)
**Context:** a purchase whose grant failed to save was redelivered by the store in the same session.
Nothing had changed since the failed write, so the commit answered "saved", the transaction was
finished, and the granted items lived only in memory: a crash would have lost what the user paid for.
**Decided:** the progress store remembers a failed write, and an unchanged commit after one writes
again.
**Rejected:** answering an unchanged commit with "saved": that is true only while every earlier
write succeeded.
**Guarded:** the purchases state test, against a store fake that refuses one write.
-->
<!-- if:monetization -->
<!-- A fuller example, with every honesty block (shipped puzzle game, shortened):

### #89 — An interstitial is counted as it is handed to the SDK, not when it closes (2026-10-04, Phase 4 slice 4.2 review)
**Context:** the ad ledger was written only after the show's future resolved. A player who swiped
the app away under the ad (a common reaction) lost it from the save, and the relaunched app could
show the next ad one level later.
**Decided:**
- `handOffFullScreen(kind)` commits the stamp, the cleared levels and the count **before** the SDK's
  show is called. The show waits for that write, bounded by `saveWait` (1 s; a local write takes
  milliseconds).
- `settleFullScreen(handOff, shown:)` after the SDK answers: if shown, the time moves to the close
  (never backwards); if not shown, the count is withdrawn, **but only while the ledger is still
  exactly what the hand-off wrote**. A change made meanwhile is never undone.
**Rejected:** counting at the close (the old order), which is lost on a process death under the ad.
**Guarded:** the saved document already holds the ad when the SDK is called; a relaunch from a
document saved under a held ad is refused at the next level; a failed show is withdrawn; a change
made under the ad survives both answers; the wait is bounded. Each guard was seen to fail by a
mutation in an isolated copy ("counting after the show", "a withdrawal that undoes a later change").
**Accepted, recorded:** a process death between the hand-off and the settle leaves the ad counted:
the safe side (one fewer ad, never one more).
**Unverified:** the audio session after a real full-screen video, on a device (PROGRESS "Device
checks").
-->
<!-- /if:monetization -->

---

### #1 — [TODO: the product: what it is, and the one rule, as a sentence] ({{DATE}}, kickoff)

**Context:** [TODO: the problem the product solves, and for whom.]
**Evidence:** [TODO: the numbers that justify it; cite research/<file>.]
**Decided:** [TODO: the product and its one rule, exactly as CLAUDE.md states it.]
**Rejected:** [TODO: the alternatives considered, each with a concrete reason.]

### #2 — Decision rights: {{OWNER}} keeps money, accounts, legal identity, keys, release and scope; the builder decides design and engineering from evidence ({{DATE}}, kickoff)

**Context:** who decides what, so nobody waits for a decision the builder owns and nothing
irreversible happens without the owner (flagship-method references/kickoff.md §3).
**Decided:**

| Domain | Delegates | Co-decides | Decides |
|---|---|---|---|
| Product scope and hard requirements | | | [TODO: ✓ (default)] |
| Look, feel, sound, UX | [TODO: ✓ (default)] | [TODO: only if they ask to] | |
| Engineering, stack, architecture | [TODO: ✓ (commissioner)] | [TODO: developer-owner, on request] | |
| Money, accounts, legal identity, keys, release | | | ✓ (always) |

**Owner profile:** [TODO: commissioner or developer-owner, per domain, with the signals that showed
it.]
