# Non-game apps

How to hold a non-game app (a tool, a tracker, a shared ledger, a reader, a service client) to the
same bar. It covers the decisions an app makes at kickoff, the quality bar read for apps, and the
app staples the source games never needed: shared data, servers that decide, accounts, widgets and
market health.

**Evidence labels.** The method was proven on three mobile games, so every rule here says where it
comes from:
- **Proven:** shipped in the source products, mostly in their app-like parts (settings, purchase
  sheets, cloud sync, consent, empty states, accessibility). It transfers as it is.
- **Trial:** from a trial project built with this method (a habit tracker, an expense splitter):
  its review coding, probes, kit reviews and plans. Probes and reviews ran there; plans were written
  but not built; nothing shipped.
- **Translation / Proposed:** reasoned from the evidence, not yet proven in a shipped app. Verify it
  with the look loop, the tests and device play before trusting it.

**Read when:** the product is not a game (kickoff reads §1–§2), or you are working on a game's
app-like surfaces (settings, accounts, purchases, sync, forms).

**Contents:** 1 Kickoff: what transfers, and the app decisions · 2 Identity and the quality bar,
read for apps · 3 Feel, translated · 4 Flows and forms · 5 Your own data: one user, local and
synced · 6 Data shared between people, and servers that decide · 7 The offline queue · 8 Accounts,
deletion and export · 9 Empty, loading, error and offline · 10 Notifications, permission prompts
and widgets · 11 Consistency without pressure · 12 Settings and onboarding · 13 Perceived
performance · 14 Market health · 15 The same verification bar

---

## 1. Kickoff: what transfers, and the app decisions

| Category | What |
|---|---|
| **Transfers unchanged** | the doc kit, phases and owner gates; slices and the definition of done; guards seen to fail; the look loop; contrast method and floors; tokens; a second lighting, if any, as a re-lighting; accessibility built and audited; copy that never over-claims; system prompts at safe moments; save and sync correctness; release gates |
| **Changes form** | "material" becomes the project's one surface system; the mascot becomes the hero object of each screen (the document, the card, the balance); "rewards" become completions and confirmations; ambient life becomes live state; sound becomes a small cue family whose kind the sound brief decides, often off by default |
| **Drop** | currencies and economies, lives, confetti for routine actions, streak *pressure* (consistency itself can stay: §11), screen shake, a mascot that carries no information |

**Make these decisions at kickoff and record each one in DECISIONS.** Each one changes the plan, the
architecture or the store obligations, and each is expensive to change after Phase 1.

| Decision | Options | What it changes |
|---|---|---|
| **Use pattern** | daily (trackers, journals, learning) or episodic (opened when something happens: splitting a bill, a trip, a tax return, a scan) | the owner's gate question (`references/planning-and-slices.md` §Owner gates), the retention metric (§14), whether reminders and streaks exist at all (§10, §11) |
| **Data shape** | one device; one user's devices; shared between people; server-authoritative (often several of these in one product) | the architecture, the core feasibility probe, the test backends (§5, §6) |
| **Accounts** | none; optional (backup, a second device, sharing); required | deletion and export obligations (§8), the privacy label, when sign-in appears |
| **Money model** | none, one-time unlock, subscription, ads | `references/monetization-and-privacy.md` §Choose the model from evidence, and §Subscriptions and paywalls |
| **OS surfaces** | home-screen widgets, a watch app, a share target, notifications | a native-view probe (§10); each surface is an entry path to teach (§12) |
| **Languages, scripts, calendars** | which UI languages; their direction, digits, calendar and week start | `references/ux-and-accessibility.md` §Localisation, RTL and calendars |
| **People in the data who are not users** | for example a group member who never installed the app | a privacy answer before Gate 0 (§6.6) |

**Decide the use pattern from evidence, not hope.** *Example (expense-splitter trial):* the review
coding showed that people open a splitter when a cost is shared (trips were 46 of 52 love mentions),
not every day. The gate question became one about the next real shared cost, tested by the owner
with a friend on their own phones. A daily-use question would have failed a good product by design.

The identity is still the project's own (`references/kickoff.md` §Identity). A utility without a
derived identity ends up as platform defaults plus one brand colour, which reads as a template. A
utility of one or two screens with no services, accounts, sync or money follows the small product
profile (`references/planning-and-slices.md` §Small product profile).

## 2. Identity and the quality bar, read for apps

### 2.1 Identity for utilities

- **Derive an identity anyway.** It needs typography, one accent with one meaning, a surface system,
  a spacing and radius scale, a motion character, and one hero element per screen (the document,
  the card, the chart). Write it as checkable rules (`references/visual-design.md` §Art direction).
- **Decide explicitly between platform-native controls and a fully custom look.** Both are
  legitimate; mixing them is not, because default controls beside designed ones read as unfinished.
  *Incident (proven):* the three most-pressed buttons were the only undesigned things on screen, and
  the owner said they made the whole product look like an app.
- **If you go custom, never borrow platform-owned shapes as decoration:** rails read as scrollbars,
  track-and-thumb as sliders, inner outlines as text fields (`references/visual-design.md` §Chrome
  semantics).
- **One accent, one meaning:** the accent marks the primary action or the key state, never both.
- **Tokens, contrast floors, the greyscale guard and a second lighting built as a re-lighting are
  unchanged.** Most apps ship two lightings and follow the system appearance (Auto / On / Off); one
  lighting is a valid identity decision, recorded with its reason (`references/visual-design.md` §9).
  Draw the icon with your own renderer and judge it among the category's icons
  (`references/visual-design.md` §Icon, launch screen and store art).

**Contrasting answers.** Each example below is one project's answer, derived from its own research.
Do not reuse a motif unless your own identity derives it.
- *Example (expense-splitter trial):* the research found that the category tells "owes" from "is
  owed" mainly by red and green. The identity made position carry it instead: each group has one
  level line, members who are owed sit above it, members who owe sit below it, and settling brings
  everyone onto the line. Owing is not an error, so neither side is red.
- *Example (habit-tracker trial):* kept days are glazed tiles, drawn from the audience's own tile
  tradition, that join into a frieze. A missed day is bare, unglazed tile, never red.
- *Hypothetical (a transit timetable):* the hero is the next departure, set large in tabular
  figures. The screen is still at rest by decision, and it moves only when the countdown changes.

The flat look (hairlines, one accent, tabular figures, no shadows) is the default of money and
productivity apps. A direction that lands on it must pass the distinctness check like any other
(`references/kickoff.md` §Identity).

### 2.2 The seven questions and two edge checks, checked in an app

The questions, each with a game reading and an app reading, are in `references/visual-design.md`
§The quality bar; refer to them by name, never by number. This table adds how to check each one in
an app and the app failure it catches (a translation: the checks are new; each failure is the app
form of one the source hit). Answer them in writing for every screen in the slice, across the look
matrix.

| Question | Check in an app | The app failure it catches |
|---|---|---|
| **Alive at rest?** | Leave the screen open while a fake remote change lands; filmstrip it. A tool that chose stillness has the decision in DESIGN. | a changed item swapped in place; a sync mark that never goes away |
| **Does touch have weight?** | Filmstrip at 60 fps: the frame after touch-down already differs. | a press that shows only on release; a swipe action that snaps |
| **Do results arrive?** | Filmstrip: the destination changes in the landing frame, not the commit frame; with motion off it settles at once to the true value. | a count that updates before the item gets there; a list that re-sorts under the finger |
| **Is every surface from the one material system?** | Screenshot every second-ring surface (sheets, toasts, pickers, errors, empty states, permission primers); list each platform default and the decision that allows it. | a system date picker or alert beside designed controls |
| **Does each screen arrive?** | Filmstrip a push, a tab switch and a cold open, with motion on and reduced. | rows popping in one by one as data arrives |
| **Does it read at its emptiest?** | Render and read the seed fixtures of §15. | a dashboard that reads as broken with zero records |
| **Does the thing arrive before its container?** | Filmstrip a cold open with a 2 s fake network. | an empty card frame painted first; decorative grey bars read as a skeleton |
| **E1: change while moving** | Tests: a sync update mid-animation, two taps 30 ms apart, backgrounding mid-transition (§4 rule 1, §6.4). | an action applied twice; a stale animation finishing over new data |
| **E2: a stuck user sees the way out** | Walk each flow's failure branch on the smallest phone at 2× text. | an error with no remedy; a loader with no exit |

### 2.3 App extras A1–A4 (Proposed)

- **A1. Does every total open into its parts?** A balance, a count or a score taps through to the
  records that make it, to the cent. *Why (expense-splitter trial):* in the review coding, a header
  total that disagreed with the expense view was a named complaint against the category leader.
  Derived totals (§5) make this rule cheap to keep.
- **A2. Does any pixel shame a miss?** A day not done gets no red, no cross, no "0" and no
  animation, and rest days look different from misses. The habit-tracker trial added this question
  to its own bar (§11).
- **A3. Does it survive interruption?** Background, kill and relaunch mid-flow: no typed input is
  lost and no action is applied twice (§4, §7).
- **A4. Does every status word match the code?** "Saved", "synced", "sent", "deleted" and "offline"
  appear only when the code made them true (`references/ux-and-accessibility.md` §Copy precision).

**Escape hatch:** put the screen beside the category leader's at the same size; name the one element
they polished that you left plain.

## 3. Feel, translated

*Translation.* Motion numbers, springs and sequencing rules are in `references/motion-and-feel.md`.
How much bounce, overshoot or sound a product has is an identity slot, set in the feel brief
(`references/kickoff.md` §Identity). Order and causality are universal.

| Game mechanism (proven) | App equivalent |
|---|---|
| Ambient life, in the measure the identity sets | Live state: a fresh item's highlight decays; a counter changed elsewhere ticks once; a breathing element only where the product has a hero and the identity wants it |
| Touch has weight | Press, drag and swipe physics from one motion table. Departures never overshoot; arrivals overshoot only as far as the feel brief allows, which is often not at all on data and money |
| Rewards travel from where they are announced to where they are kept | Completions travel: task → done list, file → folder, payment → history. The destination updates on landing |
| Celebration timeline: achievement → payment → exits, exits last and together | Confirmation sequence: the result, then its side effects, then the next actions, last and together |
| The display lags the model; the save never waits for the show | Commit and persist at once; only the visual transfer runs behind (server writes: §6.4) |
| Tap-to-skip; next action live within 300 ms | Any decorative sequence skips on tap; the next action is live within 300 ms |
| Refusals: one feedback per reason, or silent on purpose | Validation and blocked actions: one calm, specific answer per reason (§4) |
| A sound identity decided in the sound brief | A small cue family whose kind follows the sound brief, often off by default; never a sound before its visual cause |

The rule that matters most in apps comes from the "display lags the model" lesson. When a header
showed the new balance before the reward flew to it, the effect was that "nothing ever arrived
anywhere". In an app, the same fault is a counter that updates before the item animates to it, or a
list that re-sorts under the finger. If the motion is skipped (reduce motion, a screen reader),
settle at once: never withhold the true value.

## 4. Flows and forms

Standard form practice is assumed and checked in the look matrix on the smallest phone at 2× text:
the keyboard never covers the active field or the primary action, every step has an on-screen exit
(loading included), and the words for every state (empty, typing, each error, submitting, failed,
succeeded) are in the plan before building. What follows is what the evidence adds.

1. **One accepted tap per action: set the in-flight flag synchronously, before the first await.**
   Clear it only when the answer has landed (success, refusal or timeout). A flag set after any
   await leaves a window in which a second tap passes the check. *Incidents (proven):* in review, a
   double tap on a hint helper spent two hints. A fully watched rewarded video paid nothing when its
   screen was popped mid-video; the fix set the in-flight flag before the await and granted before
   any "still on screen" check. *Test:* two taps 30 ms apart, against a fake that answers after 2 s,
   apply once and charge once. The server's idempotency key (§6.3) is a second line of defence, not
   a substitute.
2. **A pending step blocks leaving through real state.** *Incident (proven):* Back still worked
   while a full-screen ad was about to show, because the flag lived outside the framework's state
   and system Back ignores input shields. The busy state refuses Back and outside taps until the
   answer lands (`references/ux-and-accessibility.md` §States).
3. **Submitting is a busy state, not a disabled one.** Keep the button at full contrast with a busy
   mark, and block input separately. *Incident (proven):* disabled styling dimmed the busy dots to
   38% white and they all but vanished. The answer is one quiet line under the control, never a
   dialog.
4. **Never lose input.** Persist drafts on change (debounced, e.g. 500 ms) and when the app leaves
   the foreground, restore them after process death, and keep every field after a failed submit. An
   interrupted gesture (a system gesture, an incoming call) discards the half-made gesture, never
   typed data. *Incident (proven):* a cancelled pointer submitted half-drawn input until cancel was
   made to discard. *Test:* type, background, kill the process, relaunch; the draft is intact and
   nothing was submitted.
5. **Validate on leave and on submit, and once a field shows an error, re-check on every change**
   (translation). The error appears when the user is done with the field and clears on the
   keystroke that fixes it. *Test:* enter an invalid value and leave (the error shows), then type
   the fixing character (the error is gone in that frame). Answer at the field, in words that name
   the remedy ("Use 8 or more characters", not "Invalid"), with an icon as well as colour. *Why:* the
   source recorded the opposite failure. A stuck state was announced in the tone of a validation
   error, a slim red banner, at the moment the user most wanted help.
6. **An overlay takes no taps until it is readable (about 0.3 of its arrival) and latches on the
   first accepted exit** (`references/ux-and-accessibility.md` §Controls that tell the truth).
   *Incident (proven):* a results panel live from frame 0 took the tap of the finger that finished
   the last move. In apps the likely case (translation) is a confirmation sheet that takes the tap of
   the finger that opened it.
7. **Decide, for each destructive action, between undo and confirm** (translation). Prefer undo for
   reversible local actions: a one-tap bar for about 5 s that restores the record exactly. Confirm
   only what cannot be undone (deleting an account, leaving a shared group, sending money), and name
   the consequence in the confirmation.

## 5. Your own data: one user, local and synced

*Proven* in the source products, which synced progress and purchases across one user's devices.
The mechanics and tests live in `references/architecture.md`: §4 persistence (one strict versioned
document; read before write, and no writes for the session after a failed read; quarantine, never
overwrite), §5 multi-device sync (per-install grow-only ledgers, a join whose laws are tested) and §6
clocks (adversarial in both directions). Two rules matter most for apps:
- **Decide whether each field belongs to the user or to the device** before choosing where it lives.
  "Asked for a review once" is a user fact and syncs, so a restored profile is not asked again. "The
  tracking primer was shown on this phone" is a device fact.
- **Store facts; derive counts.** A streak computed from the days done can be merged, repaired and
  re-decided; a stored counter drifts.

For data shared between people, or a server that can refuse a change, see §6.

## 6. Data shared between people, and servers that decide

*Trial and Proposed.* The source products never had several people writing to one record, or a
server that could refuse a change. These rules apply the proven principles to that case: store facts
and derive; a join with tested laws; bound every call; record before the irreversible step. The money
probe in §6.8 ran in a trial.

**6.1 Name the authority for each kind of data, in DECISIONS.** One product often has all four
shapes, so decide per record, not per app.

| Shape | Example | Who decides | How copies merge |
|---|---|---|---|
| One device | habit check-ins kept on the phone | the device | nothing to merge |
| One user, several devices | progress, purchases, settings that follow the user | the join | per-install ledger with tested laws (§5) |
| Shared between people, works offline | a group's expenses, a shared shopping list | the operation log | union by operation id; state derived |
| Server-authoritative | a booking, a payment, stock, a seat, an invite | the server | the server's answer replaces the local guess |

**6.2 Store operations, not documents.**
- Each user action becomes one immutable operation: `{opId, actor, device, clock, kind, payload}`.
- State (balances, lists, totals) is a pure function of the log and is never stored as truth.
- An edit is a new operation that names the one it replaces; a delete is a tombstone.
- Merging two copies is a set union by `opId`. That is commutative, associative and idempotent by
  construction; test the laws anyway (`references/architecture.md` §5.3).
- Order operations by a clock that does not trust the wall clock alone (a Lamport counter or a hybrid
  logical clock), with ties broken by device id.
- *Why (expense-splitter trial):* last-writer-wins documents silently erase a friend's concurrent
  change, and the trial rejected them for that reason.
- If re-deriving gets slow, add a verified snapshot (the derived state at one operation, checked
  against a full re-derivation in tests), never a stored truth. *Trial plan:* a snapshot is added
  only if re-deriving one group takes over 50 ms on the low-end reference phone.

**6.3 Every mutating request carries an idempotency key.**
- Mint the key when the user acts, store it with the operation before the first send, and reuse it
  on every retry.
- The server keeps a unique constraint on the key and answers a repeat with the original result.
- At-least-once delivery plus idempotent apply is the only "exactly once" a network gives.
- *Test:* deliver every operation 1–3 times, in random order, with random delays. The final state is
  identical to a single clean delivery.

**6.4 Optimistic UI, reconciled: the model still commits first.** The commit-first rule
(`references/architecture.md` §3.2) holds. The action commits to the local log, and the screen shows
it at once, quietly marked as pending. Then one of three things happens:
- **accepted:** the pending mark clears and nothing else moves;
- **refused:** the change reverts visibly, with one calm line naming the reason ("This list was
  deleted on another phone"). Never a silent snap-back (a silent refusal reads as broken), and never
  a modal;
- **no answer within the bound:** the action stays pending and the queue retries it (§7). The screen
  never claims it was saved to the server.

Decide for each action whether it is **optimistic** or **pending**, and keep the list in
ARCHITECTURE:
- **optimistic:** reversible and low-stakes, such as adding an item, editing text, ticking a box;
- **pending:** irreversible, scarce or leaving the app, such as paying, booking, sending, deleting an
  account, accepting an invite. A pending action uses the busy state (§4 rule 3) and shows its result
  only after the server answers.

*Test:* run against a fake server that refuses 1 in 5 operations, and that delays, reorders and
duplicates them. After the queue drains, every device's screen equals the server's state.

**6.5 Decide conflict rules per field, in a table in ARCHITECTURE.** Never inherit the backend's
default.

| Field kind | Rule (choose one and record it) |
|---|---|
| Free text (a title, a note) | the later by (clock, device) wins on screen; the losing version stays one tap away |
| Membership, tags, set items | union with tombstones; decide add-wins or remove-wins |
| Counters | a per-actor ledger, never a stored total (`references/architecture.md` §5.2) |
| Money amounts | never merged arithmetically; the record is the unit, and both versions are kept |
| The order of a list | by content or a fractional index, never by array position |
| Edit against delete | either the edit restores the record, or the record stays deleted and says by whom |

Show conflicts rather than hide them. *Trial plan:* when two people edit one expense at once, both
versions are kept. The later one shows, marked "edited on two phones", with both one tap away.

**6.6 Access, invites, and people who are not users.**
- **Access rules live on the server.** A check in the client cannot protect a server-issued token.
  *Trial (kit review):* a plan to enforce invite expiry "in the core" was caught; the backend's access
  rules enforce it.
- **Invites expire and can be revoked.** *Trial plan:* 14 days (Proposed); any member may revoke.
- **Removing a member is a decision about their history.** Either their name stays on past records
  as a plain label, unlinked from any account, or it is erased. Record which.
- **Data about people who never installed the app** (a group member's name, a contact) needs a
  privacy answer before Gate 0. It goes on the owner's legal list
  (`references/working-with-the-owner.md`).
- **End-to-end tests with several devices run against a local or fake backend, never production.**
  *Trial (kit review):* a planned two-device test would have written to the real backend
  (`references/release-and-store.md` §Test builds never touch production backends).

**6.7 Money: integer minor units and deterministic arithmetic** (*trial*).
- **Amounts are integers in the currency's minor units, with the currency attached.**
  `{amount: 1234, currency: "EUR"}` is €12.34. Never use a float or a formatted string in the core,
  the store or on the wire. Minor-unit exponents differ by currency (0 for JPY, 2 for USD, 3 for
  KWD); read them from a table, never assume 2.
- **Split by the largest-remainder method, with ties broken by a stable id,** so every device
  computes the same cents. €10.00 among three people is 3.34 / 3.33 / 3.33, and the lowest id gets the
  extra cent.
- **Derive balances from the log** (§6.2). The settlement plan is a pure function of the balances,
  with every tie broken by a stable id.
- **Multi-currency** (Proposed; not probed in the trial): keep each record's original amount and
  currency, and convert at a rate stored on the record, so history never shifts when rates move.
- *Why:* floats (0.1 + 0.2 ≠ 0.3), rounding each share separately (which loses or invents cents), and
  tie-breaks that depend on object key order all let two phones show different cents for one
  expense. Friends who see different numbers stop trusting the product.

**6.8 Prove conservation with a probe, then prove the probe.** *Example (expense-splitter trial;
verified in that run, not shipped):* at kickoff, a throwaway money core was tested. It used
largest-remainder allocation, balances derived from the log, and a greedy plan in which the largest
debtor pays the largest creditor.

| Test | Result |
|---|---|
| Literal spec: 10.00 among 3; 0.01 between 2; 2:1:1 of 10.00 | 3.34 / 3.33 / 3.33; 0.01 / 0.00; 5.00 / 2.50 / 2.50 |
| 10,000 random groups (2–13 members, 1–30 expenses, every split kind): each allocation sums to its total, balances sum to exactly 0, and the plan clears everyone in at most n − 1 payments | pass in 386 ms; at most 12 payments seen |
| The same log, shuffled, gives identical balances and plan | pass |
| 50 members × 5,000 expenses | 20.8 ms on a laptop |

Then two mutation proofs ran in an isolated copy (`references/verification.md` §Mutation proofs):
- **Removing the remainder step** was killed by all four tests.
- **Removing the id tie-break** was killed **only** by the literal-spec test. The "determinism"
  test shuffled the order of expenses, but the order that really differs between two phones is the
  **member key order inside one split**. The test measured something next to the claim, and the gap
  would have shipped.

*Lesson* (`references/traps.md` T-38b): a determinism test must permute every input whose order can
differ between devices (record order, key order, arrival order, device of origin). It must also be
seen to fail with the tie-break removed.

Greedy settlement gives at most n − 1 payments, not always the minimum (finding the minimum is
NP-hard in general); the trial recorded accepting it as a decision: short and explainable.

## 7. The offline queue

*Proposed.* It builds on the proven write discipline in `references/architecture.md` §4.3.
- **The local operation log is the queue.** An operation is written locally before the screen says
  it is done, and the screen never waits for the network.
- **Send in order per device, at least once, with the idempotency key** (§6.3). Bound each call
  (e.g. 10 s), back off retries with jitter (e.g. 1, 2, 4 s … capped at 60 s), and send again on
  resume and on reconnect.
- **The queue survives process death.** *Test:* kill the app mid-send and relaunch; the operation is
  sent and applied exactly once.
- **A refused operation is reconciled (§6.4), never retried for ever.** A permanent refusal (no
  access, a failed validation) leaves the queue at once with its reason; only transient failures
  retry.
- **Say what is waiting.** Write "3 changes will upload when you're online" only if the code does
  exactly that. A status shows the pending count. Nothing says "synced" before the server has
  acknowledged.
- **Offline reads show the last known state with its age** ("Updated 2 h ago") once it is older than
  the data's normal freshness.

## 8. Accounts, deletion and export

*Proposed, with dated facts.* None of the source products had accounts (their sync used the
platform's own cloud), so nothing here shipped there. The expense-splitter trial planned the flow
below and marked the store rules Unverified.

1. **Defer the account until the user has seen what it is for.** The core works without an account
   wherever the data allows. Offer sign-in at the moment it pays: a second device, a backup, sharing.
   *Trial plan:* friends join a group from an invite link with one tap and no password; sign-in
   appears only for a second device or a backup.
2. **Choose sign-in methods from the audience and the platform rules** (dated block below): the
   platform's own sign-in, an email magic link, or a password. Every extra provider is one more
   deletion and token-revocation path to build and test.
3. **Sign-out clears user facts from the device and keeps device facts** (§5). It never deletes
   server data, and it never leaves the previous user's data visible to the next user.
4. **Deletion starts in the app, at most three taps from Settings, and does what it says.**
   - One confirmation names what is deleted, what stays and why ("Your name stays on past shared
     expenses as plain text; it is no longer linked to you"). It also says whether a store
     subscription continues: deleting the account never cancels it, so link to the store's
     subscription page.
   - It is deletion, not deactivation. It completes on the server within a stated time, and the app
     signs out at once and continues as a fresh install.
   - Third-party sign-in tokens are revoked wherever the provider requires it.
   - Shared records that belong to other people follow the §6.6 decision.
   - The privacy policy says the same thing.
   - *Test:* create an account, populate it, delete it. The server then holds no record linked to
     the account, and a second device signed in as that account is signed out on its next contact.
5. **Export is complete and in an open format** (JSON or CSV): every record the user created, with
   a round-trip test (export, import into a fresh install, identical derived state). Keep the export
   of the user's own records free (Proposed). A paid report built from the data (charts, formatted
   PDFs) is a different product. *Trial plan (habit tracker):* data loss drew 20 of 402 low-star
   reviews in the category, the angriest ones, so export is free from the first release.

> **Dated facts (as of 2026-10 — re-verify before relying):**
> - **Apple** (App Review Guidelines 5.1.1(v), in force since 30 June 2022): an app that supports
>   account creation must let the user start deleting the account inside the app.
> - **Sign in with Apple:** an app that uses it should revoke the user's tokens through Apple's REST
>   API on deletion.
> - **Apple guideline 4.8** sets which sign-in options must accompany a third-party login.
> - **Google Play** (account deletion policy): an app that lets users create an account must offer
>   an in-app path to request deletion, plus a web link where deletion can be requested without
>   reinstalling. The link is declared in the Data safety form.
>
> None of this was verified in a shipped project here. Read the current guideline text and console
> forms before Phase 4. The review gate and release checklist item are in
> `references/release-and-store.md` §7.

## 9. Empty, loading, error and offline

Each of these is a designed screen with a picture (or the hero in a matching state), one truthful
line and one action, and its words are written in the plan before building.

- **Empty invites; it never scolds.** First run ("Add your first …") differs from cleared-everything
  ("All done"). Never show a record of failure before the user has started.
- **Loading shows what you already have first** (cached content, the last known state). When nothing
  is cached and the wait is real, show one designed loading state, and let the content replace it in
  one movement, never into an empty frame. Nothing decorative may look like a skeleton: grey bars
  under a headline were read as "loading".
- **Every wait is bounded.** After the bound, show one quiet retry line, in a live region. A hung
  loader with no exit is a trap.
- **Errors name the true remedy:** an offline game told players to check their connection. Offline
  is a state, not an error: say what works now and what will happen later, promising only what the
  queue does (§7). Unavailable features keep their place and say why in one line
  (`references/ux-and-accessibility.md` §States).

## 10. Notifications, permission prompts and widgets

**Prompts and notifications** (*proven* for prompts; *trial* where marked):
- **Ask only at a safe moment** (`references/ux-and-accessibility.md` §System prompts at safe
  moments): never at cold launch, mid-task or over a confirmation.
- **Ask after the user has seen the value** the permission serves, through a one-button primer whose
  copy is true for every user, then the system prompt. *Trial plan (expense splitter):* the
  notification permission is asked after the first friend joins the user's group, the first moment a
  notification could carry news.
- **Record "asked" deliberately**, as a user fact or a device fact (some systems ask per device), at
  the moment that makes the safe failure happen. An offer is recorded when shown (under-offering is
  safe); a primer that must precede the system prompt is recorded when answered.
- **Notify only about something real:** something another person did that involves the user, or a
  reminder the user scheduled. Never send re-engagement pushes. Never remind about something already
  done. *Trial (habit tracker):* 33 of 402 low-star reviews in the category complained of wrong
  reminders, chiefly for a habit already done, so a habit kept today is never reminded that day.
- **Notification text is true, specific and never shaming** ("You missed 3 days" scolds; say what is
  waiting instead), and the tap opens the screen it names.
- **Plan local reminders with a pure planner.** It returns the next occurrences after now, skipping
  items already done, capped below the platform's limit. Rebuild the plan on launch, resume,
  completion and edit. If reminders stop when the app goes unopened, the copy says so ("Reminders for
  the coming days are refreshed whenever you open the app").

**Widgets and other OS surfaces** (*trial and Proposed*) are drawn by the operating system, in
another process, on a refresh budget. The project's own renderer cannot draw them live, which breaks
both "everything from our renderer" and the usual look loop.
- **Decide by a probe on a device:**
  - (a) render a still from your own drawing code and show it as an image (one look, stale between
    refreshes); or
  - (b) build a native view per platform from DESIGN's tokens (live, but a second implementation to
    keep in the identity).
- **Keep widgets out of the vertical slice** unless the probe has proved refresh on a device.
- **A widget shows only what stays true until its next refresh** ("3 kept today, as of 9:40"), never a
  live claim it cannot keep.
- **Run the look loop on device screenshots of the home screen:** light, dark, tinted, every offered
  size.
- *Trial (habit tracker):* in the category's reviews, widgets drew 73 loves and 32 "widgets broken"
  complaints. The trial's research review moved widgets out of the slice, behind a Phase 3
  reliability probe.

> **Dated facts (as of 2026-10 — re-verify before relying):**
> - **iOS** keeps at most 64 pending local notifications per app. A frequently viewed widget
>   typically gets 40–70 refreshes a day, and the budget is not guaranteed.
> - **Android:** notifications need a runtime permission from Android 13. Exact alarms need a
>   permission that most apps do not get by default from Android 14, so prefer inexact scheduling
>   and say so. App widgets' `updatePeriodMillis` is never honoured more often than every 30 minutes.

## 11. Consistency without pressure

*Trial*, built on the proven streak mechanics in `references/domain-games.md` §8.2 Streaks without
shame. Use it when consistency is the product: habits, learning, fitness, journaling.

1. **Store the days; derive every run and count** (`references/architecture.md` §4.1). Decide each
   day once, in the zone the phone is in now, and only after that local day has ended.
2. **Show runs, not a countdown to failure.** *Trial plan (habit tracker):* each habit shows "kept
   this month" and "longest run"; there is no "current streak" counter that drops to 0.
3. **A miss is neutral:** no red, no cross, no animation, no sound. Rest days (not scheduled) look
   different from misses, and an N-per-week goal is judged by the whole week.
4. **If a streak counter exists, give it one forgiveness mechanic,** held in advance and spent
   automatically (the tested game version: `references/domain-games.md` §8.2). *Why:* "streak freeze
   doesn't work" was a named complaint in the source genre, and "streak rules feel unfair" was a
   coded complaint in the habit trial's category.
5. **Allow honest repair.** The user may check in or undo any of the last few days (trial: 7,
   Proposed); older days are read-only.
6. **Never show a record of failure before the user started.** Days before the first use are neutral
   (`references/ux-and-accessibility.md` §States).
7. **Ban shaming words** in UI, notification and store text: "streak broken", "you failed", "don't
   break the chain", "missed!" as a shout (the trial's list). The copy test enforces the list.
8. **Test day boundaries in several zones.** *Trial (habit tracker):* the probe's naive day count was
   wrong on 476 steps in New York and 420 in London, and on 0 in Tehran, so a test run in one zone
   proves nothing. Run DST days and several zones in child processes (`references/architecture.md`
   §6.3), plus travel, a clock set back, a simulated year, and N-per-week weeks. Calendar and week
   start follow the UI language (`references/ux-and-accessibility.md` §Localisation, RTL and
   calendars).

## 12. Settings and onboarding

**Settings** (*proven*). Group them by what the user is trying to do, and use Auto / On / Off for
every "follow the system" setting (copy rules: `references/ux-and-accessibility.md` §Copy precision).
A setting takes effect visibly, at once: a theme change crossfades the whole screen. A setting with
no effect is hidden until it does something. Growth needs a compaction decision, rendered at 1× and
2× text on the smallest phone before a new row lands (`references/visual-design.md` §Layout). User
facts sync and device facts stay (§5); account, export and deletion live here (§8).

**Onboarding.** The rules are in `references/ux-and-accessibility.md` §Onboarding that teaches by
doing: straight into the core action, one idea in about three actions, never a "Got it" button,
unlock at the moment of use, long-press re-explains. The app deltas:
- **The first screen is the core action on the user's own first item,** not a feature tour or a
  sign-up wall. Its completion on day 0 is the activation metric (§14).
- **In shared apps, most users arrive through an invite, not the store page.** The invite path is
  the main onboarding: it lands on the shared thing with the user's place in it (Proposed: the
  group, showing the joiner's share), and it teaches there.
- **Teach in every entry path:** deep link, widget, notification, share target, invite.
- **Defer accounts and permissions** until their value is visible (§8, §10).

## 13. Perceived performance

- **The first frame is the launch screen,** drawn by the app's own code, so the handover changes
  nothing (`references/visual-design.md` §Icon, launch screen and store art).
- **Respond on the frame of touch:** drag input uses raw pointer events, not recognisers that wait
  for slop. Commit at once and animate after; skip within 300 ms (`references/motion-and-feel.md`).
- **Warm what the first interaction needs** (fonts, shaders, first-use sounds, the first screen's
  data) before it is needed, with a bound, and show cached data first (§9).
- **Profile on a real low-tier device,** never only on a simulator or emulator
  (`references/performance.md` §Real-device profiling).

## 14. Market health

*Proposed.* Kickoff never invents launch metrics. Set them here before Phase 5, from the category's
current data, and check them after release. The method (a fixed window, a staged rollout, a target
and an investigate line per metric; one metric below its line means fix and re-stage, two mean hold
the launch) and a game's worked numbers are in `references/domain-games.md` §13 Market health at
launch. The app metrics and numbers below are Proposed starting values, not measurements: replace
them with the category's current benchmarks (dated).

| Metric | Definition | Target | Investigate below |
|---|---|---|---|
| Crash-free sessions | sessions without a fatal crash | ≥ 99.5% | 99% |
| Activation | installs that complete the first core action on day 0 (a first habit kept, a first expense recorded) | ≥ 60% | 40% |
| Onboarding completion | first runs that reach the end of the first lesson | ≥ 80% | 65% |
| D1 / D7 / D30 return (daily-use apps) | activated users who open the app on that day | 30 / 15 / 8% | 20 / 8 / 4% |
| Return at the next trigger (episodic apps) | activated users who come back within 30 days | ≥ 25% | 12% |
| Permission primer acceptance | primers answered Continue, then allowed | ≥ 50% | 30% (usually: asked before value) |
| Rating trend | the mean of the 200 most recent written reviews (all of them at launch) against the store's average | gap ≤ 0.3 stars | gap ≥ 0.6 stars, or widening week on week |
| New complaint themes | new 1–3★ reviews coded with the kickoff's themes | no new theme above 10% | a new theme at ≥ 10% |

*Why the rating row compares two means (habit-tracker trial, verified by its review pull):* the
category's store averages hid steep declines. Against the mean of the 200 most recent written
reviews, the leaders went 4.81 → 3.60, 4.60 → 2.62 and 4.59 → 3.46; the healthiest went 4.84 → 4.59.
Written reviews skew lower than silent ratings, so a small gap is normal; a widening one is the
signal.

- **A rate needs a denominator.** Fix where attempts start and end, and log each opportunity with
  its outcome, before any analytics destination exists (`references/monetization-and-privacy.md` §8,
  rule 3, with the event vocabulary and consent; logging from the state layer:
  `references/architecture.md` §3.4).
- **An app with no analytics SDK** (a privacy decision) uses only what the store consoles report,
  and says so in this table. Never add an SDK to measure something without changing the privacy
  claim, the label and the consent flow in the same slice.
- **Re-run the kickoff's review-coding script on your own reviews** weekly during the launch window.

> **Dated facts (as of 2026-10 — re-verify before relying):**
> - **Play Console's Android vitals bad-behaviour thresholds:** a user-perceived crash rate of 1.09%
>   and a user-perceived ANR rate of 0.47% of daily users overall, and 8% on any single device model.
>   Above them, the store may reduce the app's visibility.
> - **The App Store's phased release** applies only to updates: over 7 days it reaches 1, 2, 5, 10,
>   20, 50 and 100% of users with automatic updates on. A first version therefore reaches everyone
>   at once. Play's staged rollout takes any percentage.

## 15. The same verification bar

*Proven* discipline, unchanged for apps (`references/verification.md` §7 and §8):
- **Drive every core flow end to end through the real app root,** with real gestures, motion on and
  off.
- **Treat seed data and fixtures like generated content:** deterministic, versioned, rendered and
  read. Include the empty account, one item, a thousand items, the longest name, right-to-left text
  (`references/ux-and-accessibility.md` §Localisation, RTL and calendars) and the largest text size.
- **Prove persistence on the real store** (three launches across processes; a marker survives), and
  cold-launch the real entry point on a device: no component test runs it.
- **Test shared and server data against a fake server** that refuses, delays, reorders and
  duplicates (§6.4), and never against production (§6.6).
- **The look matrix, the look loop and the accessibility audit are unchanged**
  (`references/visual-design.md` §The look loop).

**App slice done:**
- [ ] The seven questions and two edge checks, checked as in §2.2, plus A1–A4, answered "yes" in
      writing for every screen in the slice.
- [ ] Every state in §9 rendered and looked at, with its planned words.
- [ ] Every form keeps input through backgrounding, failure and process death, and two quick taps
      apply once (tests).
- [ ] Own-device sync tested with two simulated devices and a hostile clock. Shared data tested with
      the fake server. Every determinism test seen to fail with its tie-break removed.
- [ ] If accounts exist: deletion and export tested end to end on a non-production backend.
- [ ] Every claim in the UI maps to code that makes it true.
- [ ] The category-leader comparison done, and its one finding written down.
