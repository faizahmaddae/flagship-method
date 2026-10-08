# Architecture

How to shape the code so rules stay testable in milliseconds, SDKs stay replaceable, saves never lose
a user's progress, and every generated thing (content, platform folders) can be rebuilt and re-proved.
Stack-neutral; Flutter specifics live in `references/stack-flutter.md`.

**Read when:** writing `docs/<slug>/ARCHITECTURE.md` at kickoff, scaffolding Phase 0, putting a guard
over an existing codebase (§2.5), adding a dependency or a layer, touching saves, sync, clocks,
timeouts or startup, or building a content pipeline or setup script.

## Contents
1. The shape: pure core, ports, adapters, one composition root
2. The layer contract, enforced by a test that reads the doc (2.5: legacy code under a ratchet)
3. State: immutable values, commit first, events to sinks
4. Persistence: one strict versioned document; write-ahead records
5. Multi-device sync for one person: per-install ledgers and a join with algebra
6. Clocks: designed for both directions
7. Async boundaries: timeouts chosen by their fallback, ordering
8. Startup: nothing before the first frame throws or waits unbounded
9. Determinism everywhere
10. Offline content pipelines, proven three times
11. Generated platform folders: an idempotent setup script
12. Config and secrets hygiene; debug switches proven dead in release

Incidents sit inline beside the rule they caused; the cross-project catalogue is `references/traps.md`.

## 1. The shape: pure core, ports, adapters, one composition root

### 1.1 Keep a pure core

The core holds the domain: rules, solver or validators, the save model and its decoder, policies, the
event vocabulary, the ports and the null objects. It imports only the language's standard library: no
UI framework, no state library, no plugin, no file or network API.
- *Why:* the same core runs in unit tests in milliseconds, inside offline tools (the content verifier
  re-uses it), and under property tests with thousands of random operations.
- Parsers take a string or bytes, never an asset loader; services load bytes and hand them over.
- **Policies take every input explicitly, including "now":** `mayShowAd({cleared, lastShownAt, now,
  ...})` returns OK or a named refusal, checked in a fixed order. With no clock inside, every rule is a
  test with a number in it.

### 1.2 Ports in the core, adapters in services

Everything from outside (save store, content source, sound, haptics, ads, purchases, analytics, review
prompt, share sheet, link opener, cloud mirror, age signals) is a core interface speaking the *app's*
language ("a level ended", not "is a cap active").
- **Results are closed types** the compiler forces callers to handle:
  `SaveRead = Found | Missing | Corrupt | TooNew(version) | Unavailable`;
  `RewardedOutcome {unavailable, dismissed, earned}`;
  `PurchaseOutcome {purchased, pending, cancelled, failed, unavailable}`.
- **The contract is written on the port:** never throws, idempotent, every platform call bounded in
  the implementation ("a channel with no handler never answers").
- **Building a service touches nothing on the platform;** connect lazily in `start()`. *Incident:*
  reading a purchase SDK's singleton connected to the store at once; under the test runner the channel
  had no handler and threw later, failing a test *after it had completed*.
- **Put a backend seam inside each service** (a tiny interface over the plugin) so the service is
  tested with recording fakes, and test the thin adapters under the seam against the real hooks, with
  mutations. *Incident:* 4 of 10 adapter mutations survived until the adapters had their own tests.

### 1.3 Choose each port's default deliberately

| Port kind | Default when not wired | Why |
|---|---|---|
| Required (save store, content, sound, haptics, clocks) | **throws, naming itself**: "`<port>` is not wired: the composition root (or the test) must override it" | A silent no-op hides a wiring bug until a user finds it |
| Absence is safe and intended (ads, purchases, analytics, cloud, link opener, age signals) | **null object in the core**: never shows, never sells, sends nothing; records calls for tests | Every screen harness reaches these; "a build without a store has sold nothing" |

The null object lives in the core because the state layer may not import services.

### 1.4 One composition root

Only the root files (entry point, app shell) construct services, pick real or null implementations per
platform, and override the port providers. Nothing below imports the root. A service that must show UI
(a pre-permission primer) receives a presenter as a constructor callback from the root. Write a
**composition test**: with a platform that never answers, the app still becomes usable, memory-only,
within the timeouts.

### 1.5 One SDK, one file

Every SDK with side effects (ads, billing, analytics, crash reporting, cloud, age signals, URL
launching, share) is imported by exactly one service file. A test lists every importer and compares it
to that exact list. Screens read state, never the SDK; no test ever starts an SDK, by construction.
- **One-file exceptions** (a wrapper lacks an API, so one file must touch the base SDK) are written in
  the architecture doc with the exact file, URI and list of imported names, guarded by their own test,
  and given an exit condition ("narrow it when upstream adds X"). Any other file, alias, extra name or
  export fails.
  *Example (shipped puzzle game):* the list grew three times, each in a dated entry with its exit.
- **Justify every dependency in the manifest:** `# <purpose> (DECISIONS #n). <version>, checked
  <date>: <transitive deps, UI-kit imports, privacy manifest, min OS>. Only <file> imports it.`

### 1.6 One home per vocabulary; variants are data

- Cue names, analytics event names, product ids, URLs and economy constants each live in one
  dependency-free core file. Mappings (theme → material → sound) are pure core functions, so a restyle
  cannot keep the old sound unnoticed.
- When layering forces a rule to exist twice (two languages, generator vs app, doc vs code, store
  config vs product ids), a test holds the copies equal. *Incident:* a beat window read 600–1300 ms in
  the sound generator and 450–1350 ms in the app.
- Every theme or brand variant is one value of the same structure (palette, backdrop, styles, sound
  material); drawing code asks the structure, never `if (theme == X)`. Dark variants are twins plus one
  numeric field. A registry names every variant's stubs up front, so parallel lanes fill stubs and never
  edit a shared file (`references/orchestration.md`); one test paints every registered variant against
  its written contract (where it may paint, max reach, light direction, low-quality form).

## 2. The layer contract, enforced by a test that reads the doc

### 2.1 Write the contract as an allow-list table

Put it in `docs/<slug>/ARCHITECTURE.md` §1 (full doc shape: `assets/templates/ARCHITECTURE.md`). Open
the doc with its precedence rule: *"If a change doesn't fit this shape, either the change is in the
wrong place or this document needs updating first. Decide which before writing code."*

| Directory | Holds | Internal imports allowed | External imports allowed |
|---|---|---|---|
| `src/core/` | rules, save model, policies, ports, null objects, events | `src/core/` | standard library only |
| `src/state/` | reactive store: notifiers, providers | core, state | the state library |
| `src/services/` | port implementations | core, services | each SDK in exactly one file |
| `src/theme/` | tokens, palettes, type, the surface recipe | theme | drawing API only |
| `src/render/` | painters; engine types wrapped in own types | core, render, theme | drawing API, not the widget layer |
| `src/motion/` | choreography, one ticker each | core, render, theme | no timers, no state, no services |
| `src/widgets/`, `src/screens/` | UI | all but services and root | UI toolkit, not raw engine types |
| root files | composition root | everything | everything except the banned UI kit |

*Example (shipped puzzle game):* the motion layer could not import async primitives (its only clock is
a ticker; the widget owns any timer), and widgets could not name engine picture or shader types, so
those were wrapped in render-layer classes. Flutter rows: `references/stack-flutter.md` §Layers.

### 2.2 Enforce it literally with a lexer, never a regex

The guard tokenises every source file (comments, nested comments, every string form, interpolation)
and reads import and export directives.
- A directory with no row fails; nested directories belong to their top directory; a file directly
  under the source root, other than the root files, fails.
- Exports count as imports; every URI of a conditional import counts; a file that shares another
  file's imports (a Dart `part`, an include) must stay in that file's directory, or it smuggles those
  imports across layers.
- URIs that leave the source root, are absolute, use another scheme or are malformed fail everywhere.
- Unreadable input (unterminated string, missing terminator, interpolated URI) is a **violation naming
  the line**: the guard will not guess.
- Message: `path:line  import 'uri'  breaks RULE: <why + what is allowed>`.
- *Why a lexer:* a sister project's regex guard was wrong both ways (a comment satisfied it; a doc
  comment tripped it). Must-catch and must-ignore lists, anti-vacuity, mutation proofs:
  `references/verification.md`.

### 2.3 Parse the doc in the test

Keep the human table in the doc and an encoded copy in test support; a test parses the markdown table
and fails until both are identical.
- The parser understands exactly the forms the table uses ("as `x/`", "plus …", "everything",
  "everything except X", "nothing"); anything else parses, then fails the comparison. Normalise
  spellings; assert the expected rows were found before comparing.
- The failure names the fix: "change ARCHITECTURE.md §1 and the encoded rules together".
- One-file exceptions live in a bullet list with a fixed prefix, parsed the same way.
- *Incident:* the first run showed the doc, read literally, forbade what the code needed (a layer could
  not import its own directory; services could not use file I/O). The doc was amended first.

### 2.4 Amend inline, dated

Format: `Amended YYYY-MM-DD (phase/slice; DECISIONS #n): <what was added, why, guarded by <test>>`.
Every widening is tied to a decision, so nobody relitigates it.

### 2.5 Adopting the guard over existing code: a ratchet

A codebase that predates the method has no layers. "Describe what is" then gives a table where
everything is allowed, and "a directory with no row fails" leaves legacy folders (`models/`,
`utils/`, a globals file) nowhere to stand. The adoption order and the quarantine for red tests live in
`references/planning-and-slices.md` §Retrofit; this is the guard's part.
1. **Write the target table first:** the layers you are moving to. New directories get target rows
   only, and a target directory may not import legacy code.
2. **Admit what exists as legacy rows,** each marked `LEGACY (expires: <slice>)`. Fill each legacy
   row's allowed cells with exactly what that directory imports today, read by the guard's own lexer,
   never guessed. A UI kit imported by most legacy files is one legacy cell ("plus the UI kit"), not
   forty one-file exceptions. Each mutable global gets its own row and the slice that removes it.
3. **Freeze the inventory.** At adoption, commit the legacy rows and their imported names as a
   baseline fixture stamped with the adoption commit. The guard then fails on:
   - any import no row allows (a new file, a new import in a legacy file, a new `show` name);
   - any legacy row or name that is not in the baseline, so adding one fails and removing one is free;
   - an expired row, whose slice PROGRESS lists as done.

   It never fails on a recorded, unexpired row.
4. **See it fail three ways** before trusting it: plant a new import in a legacy file, plant a legacy
   import in a target directory, and mark a legacy row's slice done.
5. **Migrate by strangler.** Each slice moves one screen or module onto the target layers, deletes its
   legacy rows in the same commit, and shows before and after looks. Never let two layers own one
   piece of state at once. (Flutter, leaving Material or another state library:
   `references/stack-flutter.md` §2 and §3.)

*Example (a retrofitted word game):* the UI kit sat in 6 of 9 source files and mutable globals in 5,
and the adopter had to invent legacy rows, five exceptions with exit phases and a list that only
shrinks. This section is that shape, made explicit.

## 3. State: immutable values, commit first, events to sinks

### 3.1 Immutable values with value equality

Every change makes a new value; a no-op returns the *identical* instance (tests assert identity); lists
are stored unmodifiable; cross-field invariants are asserted in constructors ("the clock runs exactly
when the board is neither paused nor solved").
- *Why:* reactive stores filter updates by `==`; a mutated-then-reassigned list silently does not
  notify, and a record holding a list never equals a fresh copy.
- Decode stored data strictly by type (`is int`: `1.0 == 1` on some runtimes).
- Turn off automatic retries where a failed load must fall back at once (a save; a bundled asset that
  failed once will fail again). Flutter: `references/stack-flutter.md` §State.

### 3.2 The model commits first; the picture catches up

1. Commit the intent synchronously: compute next, `state = next`, persist side effects.
2. Derive events with **pure core functions of (before, after)**; deliver them asynchronously.
3. The presentation draws the committed truth (`sync(state)`) plus a short animated tail, and plays
   one-off cues per event. Each event carries its own data; no sink reads "latest state" to interpret
   an event.
- *Why:* a fast swipe commits several steps before the first event arrives; an event-driven picture
  would lag or skip. Committing first makes outcomes identical with motion off.
- Make the refusal and the event one type (`Blocked(reason, cell)`, reasons checked in a fixed
  precedence), so feedback is exactly what the rules returned.
- Time *reactions* to the visual contact, not to the commit: `references/motion-and-feel.md`.
- When a server is the authority, the model still commits first, locally, and then reconciles with
  the server's answer (optimistic or pending per action, idempotency keys, visible rollback):
  `references/domain-apps.md` §6 (rule 6.4).

### 3.3 Per-frame values never enter the reactive store

Finger positions, springs, poses, particles and animation clocks live in objects owned by the UI
component that draws them, exposed as listenables the painter reads. Values that screens report *from
inside a frame* (a panel settled, a route on top, a "safe moment" for a popup) are plain observable
objects held by a provider, updated after the frame, never during build or dispose.
- *Incident:* a provider whose state changed inside a frame made the state library rebuild its root
  scope; the frame-budget test caught it (`references/performance.md` §2).
- Watch narrow slices; watch the route through a leaf component so a screen never rebuilds when a route
  comes or goes.

### 3.4 A closed event vocabulary, consumed by sinks

The core defines a sealed set of domain events (`StepCommitted`, `Blocked(reason)`, `Collected(n)`,
`Retracted`, `Solved`, `SessionStarted`). Sound, haptics, analytics, accessibility announcements and
choreography subscribe to it; domain logic calls none of them. Analytics events are a table of closed
values with bounded payloads (no ids, timestamps or free text); record opportunities with their
outcome, since a rate needs a denominator. Buffer early events until the sink attaches; chain error
handlers, never replace them. Where attempts start and end, the event table and consent:
`references/monetization-and-privacy.md` §8 (rule 3).

### 3.5 One source of truth per rule and per derived value

A rule two consumers need lives below both. A derived value states which source answers when (the live
session while playing, the profile after banking). Freeze what a panel displays when it opens and pay
exactly that; store a "per item" rule with that item's save, not in screen state.
- *Incidents:* a counter read after banking showed "170" behind a panel announcing "+20"; a "one free
  hint per board" flag kept in screen state reset on reopen.
- Judge the user by the rules, never by comparison with a stored answer (`references/domain-games.md`).

## 4. Persistence: one strict versioned document; write-ahead records

### 4.1 Shape

- One JSON document per group of fields that share invariants, stored as **one string under one key**:
  a single key-value write is the only atomicity a key-value store gives; two keys let a crash leave
  half a profile. Settings and progress are separate documents (corrupt settings never reset progress).
- Facts about the *person* (progress, purchases, "already asked for a rating") go in the synced
  document; facts about *this device* (motion switch, when the OS primer was shown) go in settings.
- Store facts, compute derived values (a streak from on-time days, never a stored counter). Never
  persist constants (prices, caps).
- Integer `v` from 1. Strict decoder: unknown keys, wrong types and newer versions are errors (or carry
  unknown keys through untouched; never drop them silently).

### 4.2 The read outcomes are different failures with opposite handling

| Outcome | Detect | Do | Writes this session |
|---|---|---|---|
| Found | parses, `v` ≤ current, validates | upgrade in memory, use | allowed |
| Missing | no key | fresh profile | allowed, after the read finished |
| Too new | `v` > current, **checked before validating** (a newer schema can look like nonsense) | keep it untouched; run fresh in memory; ask for an update if visible | **refused** |
| Corrupt | not parseable, no integer `v`, fails validation | copy the raw string to a quarantine key (never over an existing quarantine), then fresh | only if the copy succeeded |
| Unavailable | read threw or timed out | fresh in memory | **refused**: one unsaved session costs less than overwriting a real save |

### 4.3 Write discipline

- [ ] No write before the read completes (it could clobber a save never looked at).
- [ ] Callers fire and forget; writes are **serialised through a queue** and encoded at submit time,
      so a slow old write never lands after a newer one.
- [ ] Before writing, decode the string back and run the validator the next launch runs; cap the
      writer to the reader's limits.
- [ ] Remember failed writes; an unchanged commit after one writes again instead of answering
      "saved". *Incident:* a purchase grant answered "saved" while it lived only in memory, and the
      store transaction was finished.
- [ ] Persist on real exit paths (lifecycle away, Back, completion), not on every pause (banking time
      in `pause()` wrote the save on every level open).
- [ ] A checksum may give tamper evidence; a mismatch never deletes progress.
- [ ] Reset carries purchases across explicitly, field by field.
- [ ] Key names are permanent from the first upload; confirm them with the owner
      (`references/working-with-the-owner.md`).

### 4.4 Versioning

- Bump once per change set: `v(n+1) = v(n) + <fields>`. The newest reader reads **every** older version
  exactly, back-filling new fields conservatively (an old save that had asked for a rating reads as
  "asked at the level cleared then", so the margin is never cut short).
- Two fields added in parallel lanes get two versions; the later lane treats the earlier one as old.
- Build the "too new" test as `current + 1`, never from the current document (a hand-built "newer"
  fixture stopped failing at the next bump).
- A new required field with no reader for the old version turns every save into "corrupt": a silent
  restart for every user.
- **Property test:** 2,000–5,000 random operations with clocks moving both ways; the reader accepts
  every written state. *Example (shipped puzzle game):* saves and settings each went v1 → v6, no loss.

> **Dated facts (as of 2026-10 — re-verify before relying):** Android Auto Backup silently backs up
> nothing once app data exceeds its 25 MB quota (an ad SDK's WebView cache did it in a sibling app).
> Write backup rules that include only the save file; leave consent strings and analytics ids out.
> Setup: `references/release-and-store.md`.

### 4.5 Write-ahead records for events the process may not survive

This is the home of the pattern; it fits any irreversible side effect with an external owner (a
full-screen ad, a purchase, a sent message, a payment request).
1. Write a provisional record **before** handing off to the SDK, and await that write, bounded (e.g.
   ≤ 1 s).
2. Hand off.
3. Settle or withdraw the record with compare-and-set: withdraw only if the stored value is still
   exactly what step 1 wrote, so a later change is never undone.
- *Incident:* an impression written after `await show()` was lost when the user killed the app under
  the ad, and the next ad came a level early.
- Purchases: grant, save, **then** finish the transaction; "saved" means the write's answer; a crash in
  between re-delivers, and the saved purchase id prevents double counting.
- Prove it with a held show and a fresh container built over the last saved document.
- The ad-specific form (hand-off and settle, session counts): `references/monetization-and-privacy.md`
  §3.

## 5. Multi-device sync for one person: per-install ledgers and a join with algebra

This section covers **one person's own devices** syncing through a last-writer-wins cloud store, which
is what the source projects shipped. Data shared between several people, or held by a server that may
refuse a change (operation logs with idempotency keys, per-field conflict rules, access enforced on the
server, money in integer minor units), is a different problem: `references/domain-apps.md` §6, with
the offline queue in §7.

### 5.1 Counters cannot be merged from their values

Max hands back spent items; sum doubles what both devices share; a three-way merge against a "last
synced copy" loses an update whenever the cloud store is last-writer-wins and keeps the other device's
write.

### 5.2 Keep a per-install grow-only ledger inside the same document

Each install owns one line of numbers that only grow (`itemsIn`, `itemsOut`, `playMs`); only that
install writes its line. Totals are derived: `held = base + Σ_installs(in − out)`. Copies of a line
join by their larger numbers, so a grant counts once however often it is merged. The ledger shares the
counters' atomic document (two keys would let a crash double or cancel another device's grants). An
`absorb` step records this install's residual changes into its own line, so feature code never
changes: `merged = absorb(join(absorb(local), remote))`.

### 5.3 Make the join a semilattice and test its laws

The laws (commutative, associative, idempotent) are tested over random histories. Per field: union
for sets, min for best times, later for dates, "either" for once-true flags, the ledger for counters.
Order every list **by content alone**. *Incident:* ordering ids "by nearness to the end of each list"
was not associative; random two-device tests showed devices that never agreed, an endless ping-pong
of writes.

### 5.4 Flow rules

- Start after the first frame; read before write; run only while the local save may be written.
- Never write a fresh profile over a remote copy (a device that has not downloaded its copy must not
  replace it with nothing); write back only when the result differs.
- A remote copy from a newer build halts sync for the session; an unreadable one is quarantined before
  it may be replaced; the merged result passes the strict check before it is saved.
- **"Nothing to decide" is not a decision.** *Incident:* a fresh install settled "nothing to decide up
  to yesterday", and counting that in the join wiped another device's 13-day streak. Test both orders:
  act then merge, merge then act.
- **A listener must not hear its own writes:** ignore changes made during your own sync; schedule one
  more only if local data moved meanwhile. Debounce (e.g. 5 s after the last change), flush on leaving
  the foreground, sync on resume. Bound every call (e.g. 3 s); a failure leaves the local save alone.
- Never save a clock clamp produced by a merge (§6.4). Record every accepted anomaly with the side it
  errs on ("a token in the user's favour").

### 5.5 Test with randomized multi-replica models

Join laws over ~24 random histories; several 400-step two-device histories through a
last-writer-wins store model against a simple model (identical at the end, every count exact); a
skewed-clock case pinning zero extra writes.

> **Dated facts (as of 2026-10 — re-verify before relying):** Apple's iCloud key-value store refuses
> keys over 64 bytes and values over 1 MB, discards writes made before the initial download, and keeps
> the last write per key. Whether its identity token is nil with iCloud Drive off was unverified, so it
> chose only a status line, never whether to sync. Never gate a feature on an unverified signal; put
> it on the device-test list.

## 6. Clocks: designed for both directions

### 6.1 Inject clocks; no component reads the system clock itself

- **Monotonic** for durations (solve times, holds). Changing the device clock never changes a time.
- **Wall clock** for calendar days, gaps that must span sleep, and stamps that survive a reboot. A
  monotonic stopwatch stops while a phone sleeps, so "a session ends after ≥ 30 min away" uses the wall
  clock.
- Tests drive fake clocks by hand (a real stopwatch does not advance under fake time).

### 6.2 For every time rule, write down what happens when

- [ ] the clock goes back;
- [ ] the clock went forward, the app ran, and it came back;
- [ ] the app stayed suspended for days (a resume is often the first moment of a later day: grant
      day-based rewards on resume too);
- [ ] two devices disagree by more than the slack.

### 6.3 Dates

Build dates from the local Y/M/D as midnight UTC (DST-proof); index days from an epoch and handle
negative indexes (a helper silently did nothing near the epoch). Test DST zones in child processes with
`TZ` set, asserting each zone's offsets: a naive local-midnight count fails only where the epoch sits in
the lower-offset season. Decide each day once. Daily grants: the first call records the day, later
days add one, missed days are not paid, a clock set back pays nothing. Calendars other than the
Gregorian, week starts and locale digits: `references/ux-and-accessibility.md` §Localisation.

### 6.4 Clamp future stamps on read; save the clamp only where bookkeeping runs

Read a stamp more than a slack (e.g. 1 min) ahead as now, and save it as now at launch or in the day's
bookkeeping, so gaps (150 s between ads, an hourly cap) hold from the moment the skew was noticed; an
unsaved clamp refuses forever. Never save a clamp produced by a merge. *Incident:* two devices a minute
apart wrote on every change and stacked made-up "ad just shown" stamps until the hourly cap stopped all
ads.
- Prefer proof-based rollbacks: a first on-time completion of a day *before* the last decided day can
  only happen if later days were decided on a clock that ran ahead, so undo those decisions.

## 7. Async boundaries: timeouts chosen by their fallback, ordering

### 7.1 Bound every await that crosses to the platform, plugin or network

Do so even where docs say the call throws: a channel with no handler never answers, and a crash SDK's
init on an emulator never answered rather than throwing.
- A timeout abandons the *wait*, not the call; the late answer still arrives. Mark state before
  awaiting (mark a loop as playing before awaiting its start, or a late answer leaves it unstoppable).
- A `dispose()` that awaits in-flight loads hangs forever if a channel never answers.
- Do not bound reads nothing waits on: the bound would only discard a slow true answer.

### 7.2 Choose each timeout by what its fallback does

Never time out into the unsafe side. This table is the home of the rule; other references cite it.

| Call (example, shipped puzzle game) | Bound | Fallback | Why that side is safe |
|---|---|---|---|
| Open the save store at launch | 3 s | in-memory store, writes refused | playing without remembering beats overwriting |
| Preload shaders | 2 s overall | designed fallback; a late one adopted when it lands | no flash of the fallback in the common case |
| Analytics / crash SDK init | 5 s, never awaited | quiet no-op, events queued | telemetry never sits on the critical path |
| Record an ad before showing it | ≤ 1 s | show after the bound | the count must survive a kill under the ad |
| Entitlement check at launch | 2 s window | "unknown" = maybe a buyer: no interstitials; re-ask on resume | never show ads to someone who paid |
| Age signal before ads start | **none on the decision**; each underlying call bounded | ads wait | a timeout to "adult" would show tracking prompts to a late-answering minor |

*Incident behind the last row:* ads waited 20 s for an age answer, then proceeded as adult while the
age sheet could take 2 min.

### 7.3 Ordering

- **Number overlapping fire-and-forget reads; apply only the newest.** A bound alone does not fix
  ordering (a slow consent read overwrote a newer one).
- **Check and take in one synchronous step.** Two presenters awaiting the same "safe moment" both took
  it; every await between check and take is a gap.
- **A gate checked before a network call is stale when the result appears.** Hold the moment (absorb
  touches, bounded, e.g. ≤ 5 s) until a fetch-then-show call reports its end; re-check at show time.
- Timer holds restart from zero after the app returns from the background. A timer can fire between a
  tap and the next rebuild: read live state in the callback.
- **Record facts when they become true:** a primer's date at the user's answer, not at the push (a
  kill would skip the explanation); an ad at hand-off (§4.5).

## 8. Startup: nothing before the first frame throws or waits unbounded

- [ ] Every await before the first frame has a timeout and a fallback (§7.2); fire-and-forget work is
      never awaited.
- [ ] A tiny bounded settings read before the first frame is fine (the first screen must know whether
      to animate), but every failure path still reaches the first frame.
- [ ] Anything needing navigation or a sheet (consent, age check, sync) runs after the first frame;
      SDKs with UI start at a calm moment, never on cold launch.
- [ ] A timeout's fallback must match the awaited future's run-time type. *Incident:* a function
      declared to return nothing but written without `async`, as `=> waitForAll(…)`, really returned
      a future of a list. Its "do nothing" fallback threw a type error inside the entry point, and the
      app sat on its launch screen forever. Await such calls inside your own `async` function whose
      declared type is "nothing", then time out that function (Flutter:
      `references/stack-flutter.md` §10).
- [ ] **Run the entry point itself** on a device or simulator: no UI test runs it
      (`references/verification.md` §Cold launch; time budget: `references/performance.md` §9).

## 9. Determinism everywhere

Same inputs, same bytes: it makes pixel tests, recorded pictures, reviews and rebuilds possible.
- [ ] Generators are pure functions of (spec, seed). Structure seeds so slots never collide
      (*example:* item seed = `id × 100000 + attempt`; daily seed = `yyyymmdd × 1000 + attempt`). The
      output records the generator version, bumped whenever output can change.
- [ ] Parallel generation assembles in slot order, never completion order; worker functions are
      module-level (spawned processes import them).
- [ ] No per-process salted string hashes for seeds; use a stable hash such as CRC32.
- [ ] Painters derive variety from `hash(index, salt)`, never a random source at paint time; character
      behaviour comes from one seeded source; a burst counter in the seed makes repeats differ.
- [ ] A second run is byte-identical for content packs, platform setup, icons, store screenshots and
      the sound pack, checked by `cmp` or a tree hash in a test.

## 10. Offline content pipelines, proven three times

For any shipped data you must never get wrong: levels, puzzles, datasets, translations, price tables.
Game-specific rules (difficulty curves, tutorials): `references/domain-games.md`.

1. **Generate offline.** Generation time explodes with size (median 0.37 s at one size, 19.6 s two
   sizes up, with long tails): fine offline, wrong on a device.
2. **Freeze the data contract before lanes split:** a `format` version plus the generator version,
   changed on both sides at once. The doc's annotated example says it is illustrative and points to
   real fixtures; it spells out what trips people (1-based vs 0-based ids, cell indexing, what each
   stat counts). Look items up by their own index, never a shared `id` field.
3. **Prove every shipped item three times:** the builder verifies, rejects, deduplicates, enforces
   ordering, re-verifies and writes atomically (temp file + rename); an independent verifier with its
   own decoder re-proves from the shipped file; the app's own engine re-proves every item in CI,
   reading the asset as the app receives it. *Example (shipped puzzle game):* 2,027 boards re-proved
   by the app in ~0.7 s; generator selftest ~21 s; independent verify ~12 s.
4. **Parity by work counters, not answers.** Two implementations must report identical search-node
   counts on a fixture: same moves, same order, same pruning. A weaker pruning rule still counts
   answers right. Generate the fixture with the production solver and test its coverage (≥ 150 items;
   every size, square and non-square; ≥ 100 unique, ≥ 20 non-unique, ≥ 20 unsolvable; deep searches;
   node-limit aborts; one case per pruning rule).
5. **Keep the research prototype as the reference,** imported only by a selftest proving the
   production copy equal to it.
6. **Re-implement rules independently in tests** (canonical keys, ordering, symmetry images); a shared
   helper means a shared bug passes both.
7. **Check per item, never on aggregates** (aggregates let "big" levels be easier than same-size
   regulars). Include non-square cases in geometry tests (a wrong transpose stride passed on squares).
8. **Bound the solver:** a memory rule, a step cap, a background worker; distinguish "proved
   impossible" from "gave up".
9. **Validate at load, strictly:** check each entry's stored invariants; reject the whole pack on a
   failure.
10. **Print a human-readable review** (renderings per bucket, the curve table) and read it.
11. **Guard the foot-guns:** refuse partial builds into the shipped directory; one generator version
    across packs; recompute published metrics from the final item; one failure lists every offender
    (a count plus the first 25, labelled).
12. **Cap parallel workers inside one test process.** A test timeout cannot interrupt synchronous
    work, so busy workers can starve the test runner until its timeout never fires. Measure the
    limit on your machine and cap below it (measured numbers: `references/traps.md` §11, T-114).

## 11. Generated platform folders: an idempotent setup script

Platform folders (e.g. `android/`, `ios/`) are generated and gitignored; one script rebuilds them from
committed sources and verifies every edit. Which edits (signing, manifests, entitlements, privacy
files) and the release checks: `references/release-and-store.md`.

- [ ] **Never run the scaffolder over the repo.** Scaffold into a temp directory; copy out only the
      generated folders. (A bare scaffold overwrote the entry point, manifest, lint config, README and
      ignore file, several of which encoded decisions.) Checksum hand-written files before and after;
      grep the final tree for the temp path.
- [ ] **Validate every input before deleting anything:** a failure leaves the previous tree whole (a
      test asserts the order). Unknown inputs, half sets and configs that set nothing usable fail.
- [ ] **Each edit has a `check_*` that runs right after it, and every check runs again on the final
      tree.** "A sed that matched nothing looks exactly like one that worked", and a later step can
      undo an earlier one. A sister project shipped a stock icon, a wrong-language label and a
      debug-signed bundle that way.
- [ ] Edit by structure, not by old value (`label="[^"]*"`, not `label="oldname"`, which stopped
      matching after a rename); read back with a real parser.
- [ ] Query project files by their object graph: effective settings per configuration (inheritance),
      build-phase membership rather than file presence (a privacy file was in the project, not the app).
- [ ] Nothing a regeneration can delete lives only in generated folders (a console tool's config
      vanished quietly: the app built, ran, and stopped reporting).
- [ ] Patch tools expose `install | verify | verify-absent | selftest`; the selftest installs twice
      (identical tree hash) and removes each edit to see its check fail, comparing with literal values,
      never the installer's own constants.
- [ ] **Run the whole script twice: byte-identical trees.** Avoid steps that write random ids: a
      build-tool step that also ran a dependency installer rewrote the native project with random
      object ids, so two runs gave two trees (Flutter's case and its replacement:
      `references/stack-flutter.md` §12). IDE edits that cannot be made idempotent stay manual and
      documented.
- [ ] Steps keyed to an input run only when it exists; an unported step is a stub that fails once its
      input appears.
- [ ] Read env files as data (line by line, first wins, trim CR and spaces), never `source` them: a
      trailing CR carried into a platform plist made an SDK throw at launch.
- [ ] Know which of the toolchain's own commands write to tracked files (a dependency fetch that
      rewrites the lint config, generated registrants), and keep `git status --short` in the baseline
      check (Flutter: `references/stack-flutter.md` §1).

## 12. Config and secrets hygiene; debug switches proven dead in release

### 12.1 Secrets and production ids

- [ ] Production ids live only in a gitignored env file; a committed `.example` holds vendor samples.
- [ ] Setup and release scripts fail if the real file is tracked or not ignored.
- [ ] A test greps the repo (tracked plus untracked-not-ignored) for id-shaped strings and fails on any
      that look real (fake = vendor sample, a fixture like `1234567890123456`, or one repeated digit).
- [ ] Test-only fake configs carry a marker allowed only in the code that refuses it, tests and docs;
      release verification refuses the fake.
- [ ] Signing config lives outside generated folders; release verification catches a silent fallback
      to debug signing.
- [ ] When a forbidden value is compiled into every build (a library's test ids), check that every
      production value is *present* (`references/release-and-store.md`).

### 12.2 Debug switches

Enumerate every compile-time define and classify it (release value, debug-only, diagnostic). Compile a
probe three ways in child processes: debug with all debug defines (each must take effect, or the
release run proves nothing), release with the same defines (each must do nothing), release with none
(the shipped defaults). Name the probe so the normal test run skips it.
- *Why:* a store build with a leftover age-mock define would treat every adult as a teen; unit tests
  that pass `release: true` explicitly cannot see the shipped defaults.
- **A debug QA mode is dependency substitution, not progress mutation:** a debug-only launcher opens
  any state through the ordinary screens with an in-memory store, null ads and telemetry, and a
  persistent "SAVES OFF" badge. A test proves store bytes, write counts, ads and telemetry unchanged; a
  release-artefact string check proves it compiled away.
- Test builds send nothing to production backends (crash-mapping uploads only from builds signed with
  the real upload key).
