# Games: core loop, proven content, difficulty, fairness, mascot, economy

What is specific to games: a loop the player learns by playing, content that is proven and
read like a player, difficulty that is measured, fairness promises, daily rituals, a character with
a brain, and an economy only if the loop needs one. The examples come from three shipped puzzle
games (a path puzzle, a word game and a sort puzzle). They show methods, not a genre or a style to
copy; each game derives its own identity (`references/kickoff.md` §Identity). §14 translates the
method for real-time and action games (Proposed).

**Read when:** at kickoff for a game (§1–§2 only; a real-time game also reads §14); then when you
design or build a game's core loop, simulation, content generator, difficulty curve, tutorial,
hints, daily mode, streaks, rewards, mascot or economy, or when the owner says it "looks like an
app, not a game".

## Contents
1. Is it a game yet?
2. Core loop
3. Proven content
4. Read content as a player
5. Difficulty, measured
6. Tutorials that teach by doing
7. Fairness: free recovery, hints, skips
8. Daily puzzles and streaks
9. Rewards inside the story
10. Economy: a currency or not
11. Mascot: a character with a brain
12. Replay, modes and retention without dark patterns
13. Market health at launch
14. Real-time and action games (Proposed)
15. Game slice checklist

---

## 1. Is it a game yet?

Run the quality bar (`references/visual-design.md` §The quality bar: seven questions and two edge
checks) on every screen, using each question's game reading; it holds for games as written,
escape hatch included. Games add three extras, labelled G1–G3, each drawn from a fault found in a
review of a shipped game. Answer them in writing per slice, beside the quality bar's answers.

- **G1. Does a run of successes build?** The fifth success in a row must not land like the first
  (`references/motion-and-feel.md` §7, rule 8).
- **G2. Does the hero react to every event, and never contradict it?** A mascot never smiles at a
  mistake (§11).
- **G3. Is the settled payoff frame worth staring at?** Players look at it for seconds after the
  show; give it material, a hero and life (`references/motion-and-feel.md` §7, rule 11).

**What "not good enough" looked like in games.** The general catalogue (static screens, boxes
that open onto nothing, unstyled buttons, validation-red stuck states, dead buttons) and the four
classes that cover nearly all of it are in `references/visual-design.md` §The failure catalogue;
hunt for all four on every screen and mode. These rows are game-only:

| Reported | What it was |
|---|---|
| Win "has no excitement"; coins "do not look important" | panel, stars and a static "+N" all landed together in 520 ms (the fix: `references/motion-and-feel.md` §7, rule 4) |
| Content that betrays the promise | a guaranteed level needed a word no living speaker uses; the obvious word went to "bonus" (§4) |
| "Off the played path it lies" | a farmable endless mode, fixed seeds, dead ad wiring: hardened only where someone played (§3.6, §12.2) |

## 2. Core loop

1. **State the rule in one sentence a player can learn by playing.** A category winner's lesson:
   "every pixel either shows game state or is the single action". Decide what the payoff state is,
   the frame the player looks at after a win (G3); the solved board becoming a picture worth keeping
   was one project's answer, not a motif to reuse unless your own identity derives it.
2. **List every event the loop can produce** and give each a rules result, an event, and a feedback
   row (motion, sound, haptic, hero reaction), or mark it silent on purpose.
3. **One typed object is both the refusal and the event.** The rules return a reason; the UI reacts
   to that same object, so feedback cannot drift from the rules. Fix the order reasons are checked
   in. *Example (shipped puzzle game):* `pathComplete → notAdjacent → wall → occupied → outOfOrder →
   endTooEarly`.

   | Reason | Feedback |
   |---|---|
   | wall | stretch and snap back, the wall rustles, a material bonk, the hero winces |
   | occupied (own path) | snap back, the hero shakes its head |
   | out of order | the target wobbles; the correct next target pings |
   | end reached too early | a wave across the empty cells; the hero tilts its head with a "?" |
   | not adjacent | silent: a fast swipe stops at the last legal step |
   | already complete | silent |
4. **Make the end rule explicit.** Reaching the goal with work missing is refused with its own
   reason and reaction; it neither succeeds nor fails silently.
5. **Judge by the rules, never against the stored answer.** Accept any valid result; the stored
   solution only feeds hints. *Why:* "a valid alternative was marked wrong" is a named genre
   complaint, and a rules judge stays correct even if a uniqueness bug ships. Test with a hand-built
   non-unique board that accepts both solutions.
6. **Undo can never fabricate success.** Undo steps back through whole states; no redo; a new move
   drops the undone branch; leaving a completed state starts a fresh history; undo never emits
   "solved". *Incident:* otherwise Replay then Undo credited a solve with a near-zero time.
7. **Refuse every pressable thing in every wrong state** (Undo through a win overlay once unsorted a
   won board). When a new mechanic lands, re-read every tool and power-up: each reaches into state.
   And a control must visibly do something when right (a hint once spent a charge and changed no
   pixel).
8. **Cap content size as a written decision** in one notation (for example "rows×cols, at most
   9×7"), enforced by the generator and by the fit rule on the smallest phone.
9. **Keep the hero off the play surface** on puzzle and board surfaces, where it would hide play
   under the finger: beside or above the board, carrying one piece of live state (§11). A
   controlled avatar is exempt: it is the play (§14).

## 3. Proven content

Pipeline mechanics (offline generation, three independent proofs, parity by work counters, load-time
validation, bounded solvers): `references/architecture.md` §10. The game rules on top:

1. **Never ship an item that cannot be completed.** The app's own engine re-proves every shipped
   puzzle in CI: exactly one solution (if the genre promises uniqueness) and every rule holds.
   Tutorials and hand-made levels pass the same verifier.
2. **Two builder commands:** `selftest` (solver, grader, generator, every guard) and `verify`
   (re-prove the shipped packs), both run in the baseline every session.
3. **Deduplicate by every symmetry and by the underlying solution**: on a square grid all 8
   symmetries × reversal, size in the key, and also by solution route across all packs (route
   collisions are real at 7×7).
4. **Look for generator bias and randomise it away.** One path-move set never changed the
   checkerboard colour of the path's head, so cell 1 was always on the same colour (fix: reverse
   paths at random); midpoint clue insertion clumped clues. **Pruning that is not monotone repeats
   until nothing changes** (whether one wall matters depends on the others).
5. **Bench the hardest size first** and commit the output; set the size cap (§2.8) where both the
   solver and the experience stay good.
6. **"Played through" means automated real-gesture play** of every shipped item through the app's
   real root (a solver-driven UI test drew every level and daily by finger), **plus** a human play on
   a device at the gate.

## 4. Read content as a player

Statistics pass while content reads badly. **Render contact sheets per difficulty bucket
(`scripts/contact_sheet.py`) and read them as a player.** Acceptance criterion: "the generator's
review output has been *read*; boards from every bucket look like real puzzles".

1. **Turn every look complaint into a generator rule**, regenerate, re-check determinism, re-prove.
   *Example (shipped puzzle game):* "read as boards, the first build showed number soup, clumps and
   walls that did nothing". Rules added: refuse 2×2 blocks of clues; refuse straight runs of 4+
   clues (level 12 "read as a barcode"; runs hit ~3% of boards; 4 levels and 56 dailies were
   regenerated); place clues within the middle half of the widest gap, on the cell farthest from
   existing clues (~a third fewer touching clues); remove decorative walls while uniqueness and grade
   hold, keeping at least max(3, placed/3); lower early clue density (0.40 → 0.28 per cell, not
   0.45 → 0.33).
2. **Difficulty never comes from worse content**; it comes from size, length or count.
   *Example (word game):* never rarer vocabulary. Cut quality tiers by absolute frequency, not rank
   (rank 15,000 was ~5 uses in 42M tokens: noise); ask what the bottom of each tier looks like; keep
   a must-include list for every filter; "rare in writing" is not "not a word".
3. **Content that betrays the game's promise is a blocker** (a "guaranteed" level needing a word
   nobody uses while the obvious one goes to "bonus").
4. **Recompute shipped metrics from the final item** at the precision you publish, never from values
   rounded mid-pipeline.

## 5. Difficulty, measured

1. **Grade every puzzle by how a solver had to solve it**: tiers 0–2 pure logic, 3 one-step
   "what-if" trials, 4 deeper guessing. **For casual logic, ship nothing above one-step what-if**:
   the builder rejects tier 4, a test asserts it on the shipped pack, and "expert" slots become hard
   (tier 3 with many trials). *Why:* "unsolvable / needs guessing" was a named complaint (37 reviews);
   a calm game must feel fair.
2. **Where players can get stuck, keep an instrument**: the random-playout dead-end rate per level
   (300–500 playouts). *Incident (sort puzzle):* levels 1–17 were stuck 0% of the time, "not too
   easy, unlosable"; the obvious knob (more tangle) moved dead-ends 0 → 8%, removing a spare moved
   them to 36–64%; a "HARD" ribbon sat on a level a random walk always wins. "Retuning without it is
   guessing." Deal for a target rather than filtering for it: a shuffle essentially never produces
   gentle boards.
3. **Finer classes inside buckets**, trials relative to size N: E; M1 ≤ N/12; M2 N/12–N/6;
   H1 N/6–N/4; H2 N/4–N/3; H3 ≥ N/3.
4. **Order per item, pairwise, never on aggregates.** A section's "big" level must beat *each*
   regular in its section: bigger, or the same size with a class range entirely above. A relief
   level is the reverse. Never order broad classes by rank. *Incidents:* aggregates let big levels be
   out-trialled by same-size regulars; Friday and Saturday dailies tied or beat Sunday in 82 weeks of
   the first build. Now every Sunday is strictly harder than every other day of its week, checked on
   the shipped stats in both languages.
5. **Rhythm:** each wall followed by one breather, never two; first real resistance by about
   level 8; each section opens with a relief and ends with a big level.
6. **Labels tell the truth the data supports.** A label repeated for 180 levels carries no
   information.
7. **Freeze authored chapters** as deals chosen by percentile, with the design intent restated in a
   test ("level 60 is meant to be a wall"); the tool refuses generator relaxations that silently
   break a request.
8. **When a literal rule becomes impossible, redefine it as a checkable rule and record it.**
   "One size up" cannot hold at the size cap, so "harder" became "a class entirely above". If you
   show par, keep it ≥ the solver's own path and ≤ optimum + 6.

## 6. Tutorials that teach by doing

1. **First launch goes straight into play.** A map with one node explains nothing.
2. **Hand-design the first levels, one rule each, in about three moves**, so lesson and level end
   together. *Example (shipped puzzle game):* three 4×4 boards: fill every cell (going straight from
   1 to 2 is refused); numbers in order (1 surrounded by 3, 4, 5); drag back (stepping onto 2
   strands a corner).
3. **Find tiny tutorial boards by exhaustive enumeration**, check each lesson's teaching property
   mechanically, choose by eye, re-check in the selftest. 4×4 has only 552 directed routes;
   enumeration also proved no 3×3 board with only 1 and 2 has a unique solution, so that idea died.
4. **Teach on the board, not with a pointing hand or coach marks.** A translucent fingertip draws
   the first moves until the first touch; it ignores input and screen readers; it returns after ~6 s
   idle only while the board is untouched (over a drawn path it would act out a route on top of the
   player's); with motion off it is a static hint; "seen" is marked by the first touch, not the
   visit. **Let arrivals teach**: targets drop in in order (in the shipped game, with rising notes).
5. **Never ask to be dismissed**: "asking them to press Got it is asking them to agree that they
   were taught". Doing the thing dismisses it, and so does a tap.
6. **Unlock tools when they become useful** (for example levels 2, 4, 7, 10), keyed to the frontier
   so replays keep them. Coach cards point at the control they name, measured from its real
   position; a long-press on a tool re-explains it, even disabled. Teach the first run in **every**
   entry mode.
7. **Measure it**: tutorial completion ≥ 90% (dated block, §13).

## 7. Fairness: free recovery, hints, skips

1. **Turn the genre's top complaints into "always free" guarantees**, written into DECISIONS and the
   project rules: "The player can always, for free and without limit: retrace, undo, restart." No
   lives, energy, timers or paid clearing. *Why (2026 review research):* the largest clone was rated
   2.5 with "no way back without clearing, clearing costs coins, 10 free puzzles a day"; lives drew
   28 complaints; every competitor advertised "no timer". "Selling a way past a wall requires first
   building the wall."
2. **Lives, energy or timers are justified only when the design's tension really is scarcity or
   time** (a speed mode the player opts into; an arcade run where losing is the game, §14). Never
   as a gate in front of content, never to sell. Record the decision, keep a calm path, and never
   pause a timed mode with the content visible behind a see-through scrim.
3. **Stage hints, and make them worth more than competitors' hints.** First undo whatever is wrong,
   then show the whole route to the next goal (a competitor's "only highlights the next number" was
   criticised). A free unlimited hint is an answer key: give a daily trickle. The hint must visibly
   change the board and be announced to screen readers (dots at 35% opacity measured 1.2–1.7:1 and
   vanished outdoors and in store shots; they became opaque with a ≥ 3:1 ring). Play the hero's
   "thinking" beat before the reveal; a second hint on the same state spends nothing.
4. **Nudge a stuck player**: after 20 s idle light the free helper, after 25 s more the paid one,
   and only ever a helper that can be pressed.
5. **A stuck state is a dialog, not a red banner.** The primary action is the most generous option;
   a priced button appears only when affordable ("a priced button you can't press is a taunt"); undo
   and restart are always one visible tap, and restart is never hidden: the no-dark-patterns line.
6. **Offer "skip ahead", not a difficulty slider.** Skipped content stays playable; a skip that
   unlocks things grants them fully (withholding needs "a second 'open but not rewarded' state, two
   rules for one fact"); the skip control is smaller than Play; the confirmation names where it
   lands, what stays open and what unlocks, with **Stay** and **Skip** (a tap outside = Stay). "Play
   never stops while a level is left": after the furthest skip, Next goes to the lowest skipped
   level.

## 8. Daily puzzles and streaks

### 8.1 Daily puzzles

1. **Three promises, tested:** a daily always counts; its archive is never removed; no interstitial
   follows it (protect the ritual). *Why:* a competitor's uncredited daily was a top complaint, and
   removing past months drew anger.
2. **Difficulty rises through the week**, Sunday strictly hardest (§5.4). Put the day-0 epoch on a
   Monday so `day % 7` is the weekday, and ship whole weeks so a wrap keeps weekday difficulty
   (*example:* five years of dailies bundled).
3. **Clock rules** (general: `references/architecture.md` §6): the day index from the local Y/M/D
   as a midnight-UTC date (DST-proof); sample the clock once per transaction; a clock before the
   epoch shows no daily and never crashes (refuse day ≤ 0); refresh at local midnight and on resume;
   decide each day once; be generous to backward clocks offline but clamp re-payment
   (`lastPaidDay < today`).

### 8.2 Streaks without shame

These rules hold for any product that counts consecutive days, games and apps alike. Apps where
consistency itself is the product (no game streak): `references/domain-apps.md` §11 Consistency
without pressure.

1. **Compute the streak from stored facts** (on-time days, covered days, last settled day), never a
   stored counter: facts can be merged, repaired and re-decided. Across devices the facts merge by
   an order-independent join, and a fresh install's empty record is not a decision
   (`references/architecture.md` §5: it once wiped another device's 13-day streak).
2. **One streak-protection mechanic, held in advance, spent automatically.** *Example (shipped
   puzzle game):* +1 token per 7-day streak (and +1 per week from an opt-in video), at most 2 held;
   two missed days are covered only if 2 are held. *Why:* "streak freeze doesn't work" is a named
   complaint. Test: always credited; one miss with and without a token; two misses with 2 and with
   1; earning at 7 days; the cap; the archive across a simulated year; DST and time zones.
3. **Never show a record of failure before the user started.** Days before the first played day
   are neutral, like future days; at zero show "Start a streak", never "0 day streak" (the incident
   and the general empty-state rule: `references/ux-and-accessibility.md` §States).
4. **A miss is neutral, never a shame state.** No red day, no alarm colour, no loss message, no
   animation on a missed day; show what was kept. The stuck-state lesson applies: help announced
   "in the language of a validation error" read as punishment.
5. **A streak is alive, not merely non-zero.** One day is not a streak. Show it on the screen where
   time is spent; never advertise a broken streak a week later.

## 9. Rewards inside the story

1. **Prefer rewards that live inside the game's own story** over a coin economy: the payoff state,
   progress, cosmetics the hero wears, the streak. *Example (shipped puzzle game):* no stars, coins
   or purse; progress stored the best solve time.
2. **Consider turning the player's achievement into an event**, so the plan they made becomes
   something that happens. *Example (shipped puzzle game; one project's answer, do not reuse the
   motif unless your own identity derives it):* the mascot runs the drawn route, each milestone's
   chime replays, and the solved board becomes a card that doubles as the share image. A racing
   game might replay the best lap as a ghost; a builder game might time-lapse the build.
3. **A container opens before its contents are known**: locked → strain → the lock breaks → the
   lid → light → items leave one at a time → amounts count → exits last; contents illegible until
   the lid opens. *Worked beats (2 s):* 0–6% a locked shudder; 6–16% the shackle snaps off; 10–30%
   the lid throws back, light out; 30–72% items leave one at a time; 72–100% the light settles. Lid
   ~24° (5° is a shrug, 50° means the lid came off). Show **totals owned** with a +N badge, not
   "Item +2"; copy says where it went ("ADDED TO YOUR KIT"), not accounting ("BOOSTS BANKED"). Exits
   live from frame 1 as a skip: a reveal seen eight times must not trap anyone. "A container whose
   contents are known before it opens is not a chest; it is a decoration on a receipt."
4. **An unlock show names the gift after it lands.** A cosmetic arcs onto the hero and is drawn in
   the hero's own layers, as it will be worn (a coat once flew across the hero's eyes).
5. Reward travel, counters, timelines and confetti: `references/motion-and-feel.md` §7.

## 10. Economy: a currency or not

**Default: no currency unless the core loop needs one.** *Why (shipped puzzle game):* "a coin economy
is a separate game system that this calm puzzle does not need, and nothing here needs to be bought
with it"; the "double your reward" and purse beats were cut. Ads and purchases:
`references/monetization-and-privacy.md`.

**A currency is justified only if every box holds:**
- [ ] The loop creates real demand for its sinks without manufactured friction. Tools that resolve
      genuine stuck states qualify; a wall built to sell its removal does not.
- [ ] Earning tracks getting better: "no sequence of taps that mints coins without the player getting
      better". Pay only for first clears and improvements.
- [ ] Every line of its copy can stay true, and its balance is pinned by tests.
- [ ] It is not just a wrapper around ads ("double your coins" videos).

**If you have one** (rules from a sort puzzle with coins): show "+N" only when N > 0 ("+0 reads as a
taunt"); put the price on the button at the moment of need, and make an unaffordable tap say where
the currency comes from; model the economy at several play levels and compare each change against
what **shipped**, not the branch's drafts; check each door's traffic (a feature behind a button 4% of
players press does nothing); keep constants in one file with bounds pinned in tests; prevent farming
everywhere (fixed seeds, replays, endless modes); keep copy exactly true (a "without help" payout row
once paid players who had used help).

**Rejected, with reasons:** consumable coin packs and saved-game services (resented; unrestorable
without a server); leaderboards and accounts (a backend, reopened privacy forms, and fake
leaderboards are a named complaint); encrypting a single-player save (any shipped key is
extractable; nobody to cheat against); fetched remote economy config where the service is blocked in
your markets (keep numbers compile-time, move them little per release).

**Hint economy** *(example, shipped puzzle game)*: 3 free at the start, +1 free per day, +1 per
opt-in video (at most 2 per level, 30 per day), and two packs priced from the genre's per-unit
prices, the larger called "Best value" only with a real margin (`references/monetization-and-privacy.md`
§5).

## 11. Mascot: a character with a brain

A mascot is optional; its species, shape and voice come from the project's identity. If you have
one, give it a job. Its art spec (proportions in units of its height, a silhouette test at the
smallest size, parts that grow out of the body, pose and accessory sheets) is in
`references/visual-design.md`.

1. **It carries game information**: one piece of live state (*example:* the next target on a tag it
   wears) and a reaction to every event; it never contradicts the event. A replay of the
   achievement is a further job if your identity derives one (§9.2).
2. **A pure, deterministic brain driven by events and a clock.** It publishes a plain pose value a
   painter draws, so the renderer can be swapped behind a one-file seam. Moods: idle, attentive,
   react, celebrate, think, sleep; exactly one reaction per event type; variety from fixed seeds; it
   needs frames only while something can change, never with motion off.
   *Example reaction table (shipped puzzle game):*

   | Event | Reaction |
   |---|---|
   | into a wall | wince, 220 ms |
   | onto its own path | "no-no" head shake, twice in 260 ms |
   | out of order | looks at the right target for 700 ms; its tag flashes |
   | ended too early | head tilt and a "?", 900 ms |
   | milestone collected | licks its lips 100 ms after, for 360 ms; tag flips to the next number in 180 ms |
   | hint | three sniffs over 900 ms; sound peaks on the head dips (150/450/750 ms) |
   | solved | leaps in and runs the route; two happy hops of 320 ms at the end |
3. **Attentive while the player acts**: it leans in, and its head and eyes follow the input point
   (`spring(180, 0.1)`). *Example (animal mascot):* an idle tail wag at 0.9 Hz rising to 2.2 Hz
   while the player acts. Find your character's own sign of attention the same way.
4. **It sleeps only on the home screen, after 30 s idle, never during play**: a mascot dozing
   while the player thinks "reads as boredom". On home any touch counts: on the mascot it perks
   up, elsewhere it looks at the finger; returning to the screen perks it and restarts its idle clock.
5. **Locomotion advances by distance, never by time.** Sliding feet are the classic tell of cheap
   animation.
   - `gait += distance / cycleLength`, so planted feet stay planted; a test reads the *painted* foot
     positions in every facing.
   - **Cap cadence at 6 Hz** (≥ 10 frames per cycle at 60 Hz). At run speed, one cycle per cell meant
     30–40 Hz legs, and "they alias backwards". *Policy that worked:* one cycle per cell up to
     6 cells/s; above that the stride fades and a stylised dash fades in, full dash from 12 cells/s.
   - *Trot starting values (example, a four-legged mascot; H = its height):* diagonal pairs half a
     cycle apart; legs ±25°; foot lift 0.06 H mid-swing; body bob 0.03 H at twice gait frequency,
     head counter-bob at half that; ears trail the speed; tail 3 Hz.
   - **Facing has hysteresis**: corners are cut on a curve 0.3 cell wide so facing switches as the
     tangent crosses 45°; a leg shorter than 80 ms keeps the previous facing; each turn gets a 60 ms
     squash.
6. **Lay it out by its resting box** (one that holds every resting pose: 1.16 × 1.045 of one
   mascot's height) and let leaps overflow upward into empty space, never sized by full paint bounds.
7. **Checkpoint before wiring**: render the pose sheet and a walk sheet (8 frames × 4 facings), look
   three times, compare at the same size with the category's benchmark character, write an honest
   paragraph on where it falls short, and follow a failure path written in advance (one plan B: a
   rigging animator driving the same pose inputs through the one-file seam).

## 12. Replay, modes and retention without dark patterns

1. **Replays keep unlocks and never re-credit.** A solve time is valid only for a first clear; carry
   `first` or `replay` on the analytics event.
2. **Fixed seeds are exploits.** Never seed a "fresh" mode with a constant: an endless mode and a
   duel served seed 1 forever, farmable and spoiled.
3. **Every mode needs a number that says where you are**, on the screen where time is spent (an
   endless mode with no round number "blurred into one").
4. **Retention that respects the player:** a daily ritual with a forgiving streak (§8); collection
   inside the story (§9); unlock shows; a share image of the payoff; the next level always one tap
   away (*example:* the Play button shows the next level's number, matching the number on the
   mascot's tag); stats only for what the save holds ("total play time is not shown: it is not
   tracked").
5. **Never:** lives, energy or timers the player did not choose; paid clearing or daily caps on play;
   fake leaderboards; AI-generated art anywhere the player looks (`references/visual-design.md`); an
   upsell pushed more than once; a record of failure before the player starts; and, if ad-funded,
   ads mid-task, at level start or on a reward screen (`references/monetization-and-privacy.md`).
6. **The owner's feel-gate question** is asked in their language after they play the vertical
   slice. Its one wording for games (with the real unit named: level, board, round, run), the
   delivery route and what follows a "no" live in `references/planning-and-slices.md` §3 Owner
   gates; copy the wording from there into the PLAN goal sheet.

## 13. Market health at launch

Set launch metrics per genre once the game exists, never at kickoff. The method: a fixed window, a
staged rollout, each metric with a target and an investigate line; below one investigate line, fix
and re-stage; below two, hold the launch. Event rules: `references/monetization-and-privacy.md`
§Analytics. The app equivalent, with app metrics: `references/domain-apps.md` §14 Market health.

> **Dated facts (as of 2026-10 — re-verify before relying):** one sort puzzle's launch-health
> targets (14-day window; staged rollout 10 → 50 → 100%, ~48 h per step), each with an investigate
> line: crash-free sessions ≥ 99.5% (< 99%); tutorial completion ≥ 90% (< 80%); reached level 10 on
> day 0 ≥ 45% (< 30%); D1 ≥ 30% (< 22%); D7 ≥ 12% (< 8%); median session ≥ 6 min (< 3 min). They
> were set from 2026 genre data; re-derive them for yours. Review-complaint counts in this file
> come from 2026 store reviews of puzzle competitors.

## 14. Real-time and action games (Proposed)

**Proposed, translated.** Sections 1–13 were proven on turn-based puzzles. A game where the player
steers something against time (a dodger, a runner, a shooter, a platformer) keeps the method and
its order, honesty and fairness rules, but reads several rules differently. These readings are
translated from the proven method and one trial build; no shipped game has proved them yet. Every
number below is a starting value: confirm it on a device and record it in DESIGN or DECISIONS.

| Turn-based rule | Real-time reading |
|---|---|
| The hero stays off the play surface (§2.9) | The controlled avatar is on it; the thumb never covers it (§14.2) |
| A typed refusal per illegal move (§2.3) | A typed outcome per collision or death, each with a feedback row and a cause visible on its frame |
| Retrace, undo and restart are free (§7.1) | Retry is free, instant and a numbered promise (§14.2) |
| Every shipped item is proven solvable (§3) | Every pattern is survivable at its maximum speed (§14.3) |
| Difficulty by solver tier and dead-end rate (§5) | Difficulty by a human-like bot: survival-time and deaths-per-minute curves (§14.3) |
| Ads after N cleared levels | Ads by active-play minutes, never by attempts (§14.5) |
| "Does touch have weight?" (game reading) | The avatar never lags input; weight lives in secondary motion (`references/visual-design.md` §The quality bar) |

Decide the genre's feel slots in the feel brief (`references/kickoff.md` §7.4): input latency,
avatar smoothing (default none), hitbox ratio, time-to-retry and hit-stop.

### 14.1 The loop: one fixed-step simulation

1. **The simulation is pure and fixed-step:** `step(state, input) → state` with a constant step
   (trial starting value: 1/120 s), no clock, no framework imports, and randomness only from a
   seeded stream held in the state (`references/architecture.md` §1.1, §9). One ticker adds real
   elapsed time to an accumulator and runs whole steps; the renderer draws the last two states
   interpolated by the leftover fraction. Per-frame state never enters the app's store, which holds
   menus, results and settings (`references/architecture.md` §3.3).
2. **Cap the catch-up after a hitch.** A stall (a garbage collection, the notification shade, a slow
   frame) would otherwise run dozens of steps at once and move the avatar into a hazard it never
   showed. Run at most a bounded number of steps per frame (trial starting value: 250 ms worth) and
   drop the rest, so the world slows for a moment instead. Leaving the app pauses the run; it comes
   back paused with the avatar visible, and play resumes on a touch.
3. **Sweep collisions.** Test the path each object travelled during the step, not only where it
   ended: a swept shape, or sub-steps in which nothing moves more than half the smallest collider.
   *Why:* at speed, a hazard passes straight through a thin avatar between two steps. Test the
   fastest hazard against the thinnest pose.
4. **Prove determinism.** The same seed plus the same input log (inputs stamped by step number,
   never by wall time) gives the same final-state hash with the renderer at 30, 60 and 120 Hz and
   with an injected hitch. Keep input logs of real deaths as regression tests: a replay is the bug
   report. If replays must match across platforms, keep math-library calls (sin, pow) out of the
   state or use fixed point; their results can differ between platforms.
5. **Whether an engine pays** is a Track C decision (`references/kickoff.md` §5.3), taken on the
   stack playbook's criteria (Flutter: `references/stack-flutter.md` §15 Game loop and engine verdict).

### 14.2 Control, fairness and retry

1. **The avatar follows the input with zero positional smoothing.** Read raw pointer events; no
   lerp and no spring on position. Weight and juice go into secondary motion: tilt, squash, trail,
   glow, camera. *Why (a trial build's review research):* "controls" was a recurring complaint
   about the genre's leaders, even inside 4–5★ reviews; positional lag reads as unfairness.
2. **The thumb never covers the avatar.** Use relative control (the avatar moves by the finger's
   movement, not to the finger) or a fixed offset; the feel brief decides which.
3. **A latency budget, measured on a device.** Film finger and screen together in 240 fps slow
   motion (one video frame ≈ 4 ms) on the owner's phone, count frames from finger to avatar, and
   record the number, device and date. The app's own share stays within one simulation step:
   input read before a frame is built moves the avatar in that frame, and nothing smooths or queues
   it (interpolation costs at most one step, ~8 ms at 1/120 s). Until measured, it sits on Device
   checks.
4. **The hitbox is constant and smaller than the art** (trial starting value: 0.55 × the avatar's
   silhouette), the same in every animation pose; a hazard's hitbox is never larger than its art.
   Look at a filmstrip of near misses and deaths with hitboxes drawn: every death shows contact on
   its frame, every near miss a visible gap. A death without a visible cause is a bug.
5. **Time-to-retry is a numbered promise** (trial starting value: ≤ 400 ms from death to a
   controllable avatar, one tap, no menu), proved by a UI test like the 300 ms next-action rule
   (`references/motion-and-feel.md` §5). The death beat (hit-stop, a personality slot; trial:
   80 ms) is skipped by the retry tap.
6. **The fairness promises still hold** (§7): no lives or energy the player did not choose;
   difficulty comes from speed, density and pattern, never from worse fairness (a larger hitbox,
   added latency, a hazard that enters with no warning).

### 14.3 Proven patterns, measured difficulty

1. **"Proven content" means every pattern is survivable at the highest speed it can appear at.** A
   search over the real simulation (the avatar's real speed limit and hitbox, no reaction delay)
   proves each wave, chunk or segment, and every allowed pairing at their seams, where impossible
   combinations hide. The app's engine re-proves the shipped set in CI (§3.1); a generator emits
   only proven patterns.
2. **Measure difficulty with a human-like bot:** a reaction delay in the human range (starting
   value ~220 ms, varied per run) and positional jitter, over thousands of seeded runs. Publish
   survival-time and deaths-per-minute curves per speed step and per pattern. A pattern that kills
   the bot far more often than its neighbours is a spike to review; one the zero-delay prover
   cannot pass is a content bug.
3. **Calibrate the bot against people** before tuning on its curves: compare the owner's and
   testers' first-session survival times with the bot's at the same settings, and again against
   real players after launch (§13).
4. **Rhythm and labels carry over** (§5.5, §5.6): each wall followed by a breather; labels only the
   data supports.

### 14.4 Motion, flashes and accessibility

- **Motion Off keeps the simulation moving** and removes presentation: shake, hit-stop, flashes,
  parallax, camera moves (`references/motion-and-feel.md` §10). Assists that change the task
  (slower speed, a more forgiving hitbox) are separate, labelled options, with the score marked.
- **Hit flashes, strobing hazards and music-synced pulses obey the flash-safety rule**
  (`references/ux-and-accessibility.md` §15), checked by a test over recorded frames of the
  busiest moment.
- **The screen reader covers every non-play surface;** play gets an accessibility route decided in
  DESIGN (assists, audio and haptic hazard cues, one-touch control):
  `references/ux-and-accessibility.md` §12.
- **Shake and haptics on every hit** are capped in amplitude and rate like any repeating cue
  (`references/motion-and-feel.md` §7, §13).

### 14.5 Ads, attempts and retention

1. **Count ad cadence in cumulative active-play minutes, never in attempts** (trial starting
   values: the first after ≥ 6 min of play, then ≥ 4 min apart). Never after consecutive short runs
   (trial: two under 20 s), never on a new-best result (a reward screen), never at a run's start.
   *Why (a trial build's review research):* "an ad every 2–4 attempts" was a repeated low-review
   complaint about a category leader; counting attempts punishes exactly the short runs a skill
   game is made of. Policy shape: `references/monetization-and-privacy.md` §2; the run-based slots:
   `assets/templates/MONETIZATION.md`. An allowed ad sits between a result and the next run, so the
   retry promise is measured on runs without one, and the cadence keeps those the norm.
2. **A run is an attempt** for analytics: it starts when control begins and ends at death, quit or backgrounding. The run
   itself pauses (§14.1); its resume opens a new attempt tagged resumed (`references/monetization-and-privacy.md` §8).
3. **Every mode shows where you are** (§12.3): the current run's time or score, and the best.

## 15. Game slice checklist

- [ ] The quality bar (game reading) and G1–G3 are answered in writing for every screen in the
      slice.
- [ ] The rule fits one sentence; every event has a rules result, an event and a feedback row (or
      deliberate silence); refusals are typed, ordered, mapped one to one.
- [ ] Judged by the rules (a non-unique test board accepts both solutions); undo cannot fabricate a
      solve.
- [ ] Every shipped item is re-proved in CI by the app's engine, tutorials included; deduplication
      covers symmetries and solutions.
- [ ] Contact sheets of every bucket were **read**; each look complaint became a generator rule and
      a regeneration.
- [ ] Difficulty graded by solver tier, capped where the genre needs it, ordered pairwise per item;
      a dead-end instrument where players can get stuck; labels true.
- [ ] Tutorials teach by doing on the board, are found by enumeration, and never ask to be dismissed.
- [ ] Retrace, undo and restart are free and unlimited; any life, timer or currency has a recorded
      justification. Hints undo what is wrong first, read at ≥ 3:1, are announced, and are limited.
- [ ] Dailies always credited, archive kept; the streak computed from facts, misses neutral,
      nothing shown before the start, protection tests pass; clock rules hold in both directions.
- [ ] Rewards live inside the story; containers open before contents; nothing animates that did not
      change.
- [ ] If there is a mascot: it carries live state, reacts to every event, never contradicts one,
      sleeps only on home; planted feet are tested.
- [ ] Every item played through by real gestures in a test; the owner played the slice on a device
      and answered the gate question (`references/planning-and-slices.md` §3).
- [ ] Real-time game (§14), in place of the puzzle-only items above: a pure fixed-step simulation
      with interpolation, swept collisions and a capped catch-up; the same seed and input log hash
      identically at 30, 60 and 120 Hz; zero positional smoothing, a device-measured latency, a
      constant hitbox smaller than the art; the time-to-retry promise tested; every pattern proved
      survivable at its maximum speed; bot curves read and calibrated; Motion Off keeps the
      simulation; flashes within the flash-safety rule; ad cadence in active-play minutes.
