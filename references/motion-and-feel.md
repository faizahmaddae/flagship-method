# Motion and feel

How to specify, build and verify motion, input feel, haptics and sound, so that touch has weight,
every event lands in the right order, and the sound plays well on a phone speaker. Rules about order,
causality and honesty hold for every product. Rules about personality (overshoot, bounce, ambient
amount, shake, the kind of sound) are slots that each project's feel and sound briefs fill
(`references/kickoff.md` §Identity); the numbers here are tuned starting values and worked examples.

**Read when:** you are about to animate anything, wire a gesture, add a haptic, choose or generate a
sound, choreograph a reward, show or transition, or review a build that "feels flat" or "looks like
an app".

## Contents
1. Derive the feel, then freeze it
2. Write motion as a spec
3. House physics: a starting set
4. Motion grammar
5. Model first, picture second
6. Sequencing: causes, order, overlap
7. Rewards and payoffs
8. Shows as pure timelines
9. Ambient life
10. Reduce motion: presentation off, the task kept
11. Input feel: grid and drag input
12. Haptics
13. Cue scheduling
14. Sound identity and system
15. Mastering for the phone speaker
16. Sound in step with motion
17. Sound plumbing, generation, licences and the owner's ears
18. Verifying feel: definition of done

---

## 1. Derive the feel, then freeze it

Most "it feels cheap" faults were not wrong numbers but correct frames in the wrong order, at the
wrong time, or while something else changed. A code critic once confirmed every duration and curve
in a game's motion table was implemented faithfully; all the faults were in the rules *around* the
table. Spend the effort on §4–§8, and settle the numbers once.

1. **Start from the feel and sound briefs.** Their contents are defined in one place,
   `references/kickoff.md` §7.4 The identity brief; this file executes them. Before tuning, sort
   every number you are about to set into one of two kinds:

   | Kind | What it covers | Who decides |
   |---|---|---|
   | **Structure** (universal) | effects after causes (§6.1–§6.2), content before container (§6.4), no double exposure (§6.6), never block input (§5.4), Motion Off removes presentation motion and schedules none of it while motion that is the task continues, outcomes identical (§10), every flash within the flash-safety rule (§7.6), departures never more energetic than arrivals (§4.1) | this file; violating one is a bug |
   | **Personality** (a slot) | overshoot on arrival (§4.9), refusal shape (§4.10), spring bounce, ambient amount (§9.1), screen-shake budget (§7.6), hit-stop length (`references/domain-games.md` §14.2), refusal haptic weight (§12.2), the kind of sound system (§14.2) | the brief; the numbers here are one project's answers |

   *Example (shipped puzzle game, "a cozy, tactile toy"):* arrivals overshoot, one impact per level
   with one screen shake, input plays a ladder of soft plucks. *Example (hypothetical banking app,
   "steady, exact, quiet"):* nothing on data or money overshoots, no shake, ambient motion only on
   values that change, one quiet confirmation sound, off by default. The process transfers; the
   numbers may not.
2. **Tune by watching builds on a phone, then freeze the values in one constants file**, each with
   its unit and source. Forbid re-deriving values per feature. *Why:* in a word game the owner asked
   twice for a 120–180 ms press; the one 90 ms press was the only beat that did not match the tile
   the game is played on. Unifying to 130 ms fixed it.
3. **Label each number "set from renders" or "set on a device"** (render-set numbers are the first
   to revisit on a phone), and record each tuned change with its reason ("0.09 → 0.07 because the
   cap showed as a sliver"). "Make it feel better" becomes an edit someone can review.

## 2. Write motion as a spec

**Event table.** One row per interaction, all four channels, exact numbers, so that motion, sound
and haptics are designed together and nothing is left to the implementer's taste. *Example (shipped
puzzle game):*

```
| Event          | Visual                                  | Timing                                     | Sound              | Haptic                  |
| Cell committed | segment grows 0→full; width 1.15→1.0;   | grow 110 ms easeOutCubic; width            | step-ladder pluck, | selection tick,         |
|                | stamp pops, then fades                  | spring(220, 0.3); stamp 1.35→1.0 160 ms    | ≥ 45 ms apart      | ≤ 1 per 35 ms           |
|                |                                         | easeOutBack, then opacity 0.55→0.18 600 ms |                    |                         |
| Into a wall    | end stretches, snaps back; wall rustles | spring(240, 0.4); rustle 180 ms            | material bonk      | light, once per contact |
```

**Timeline table** `| Time (ms) | What happens |` for anything with more than one beat (for
example: 0 the milestone pops and chimes; 60–180 its colour changes; 0–520 a token flies; 520–760
it lands and the counter changes). Shows carry the same table in code (§8).

- Give durations in ms and name curves (easeOutCubic, easeOutBack, easeInCubic, easeInOutSine).
- Write springs as `spring(settle duration, bounce)`, bounce 0 = critically damped. Check that your
  framework has this constructor, or map it to stiffness and damping. Schedule as if a spring
  settles at 4× its duration: "a bouncy spring's tail is invisible long before it is mathematically
  done".
- **Drive all motion by elapsed time, never by frame count.** Phones run at 60, 90 and 120 Hz.
- Every table gets a **motion-off** note (§10) and a row per refusal (§11). Keep "Plan" and "As
  built" side by side in the motion-spec section of `assets/templates/DESIGN.md`.

## 3. House physics: a starting set

Set by watching builds of two calm puzzle games and confirmed on devices. Use them to **start**
tuning, not as your identity; a fast arcade game or a sober utility moves away from them by §1.
Every easeOutBack below is a **playful-feel starting value**: a sober identity keeps the duration
and swaps in easeOutCubic or a critically damped spring (§4.9).

| Motion class | Starting value | Curve / note |
|---|---|---|
| Press (every control) | to 0.94 scale in 130 ms; spring back on release | easeOut. **One press duration**: if a control seems to need another, it belongs to a different tier. |
| Tile / key press | down 130 ms, up 210 ms | release slower than press |
| Screen entrance | 620 ms as **one** movement: opacity over the first 55%, lift 28 pt → 0, scale 0.94 → 1 | lift easeOutCubic, scale easeOutBack; row stagger 0.09–0.11 of the timeline |
| Route transition | 240 ms in / 190 ms out; fade + 0.94 scale | easeOutCubic; never scale a full scene (§6.6) |
| Sheet / dialog | 260 ms / 220 ms | slide opaque; only the dim fades |
| Counter pop / landing pop | 380 ms / 1.25 → 1.0 in 240 ms | easeOutBack |
| Reward flight | 520 ms on an arc of height 0.25 × distance | easeInCubic: accelerates into the slot |
| Count-up / spark burst | 420–700 ms / 420 ms | easeOutCubic / out easeOutCubic, fade easeInQuad |
| Praise line | 1150 ms: pop over 0–26%, lift away over 70–100% | easeOutBack in, easeInCubic out |
| Grow vs retract | grow 110 ms, pull back 90 ms; multi-step reel-in 18 ms/segment, cap 260 ms | easeOutCubic vs easeInCubic |
| Theme crossfade | 600 ms | easeOutCubic |
| Idle "continue here" nudge | after 1.5 s idle, a pulse on a 1.6 s loop | |
| Screen shake | the source's budget: one per level, 4 px, 120 ms, on the completion impact | a slot (§7.6); never during input |
| Shows / ambient loops | completion ~1.9 s; container reveal 1.8–3.0 s; unlock ~3.0 s / 2.6–6 s periods | shows tap-to-skip (§5); ambient §9 |

## 4. Motion grammar

**Structure (universal).** These rules are about order and honesty; they hold whatever the
identity. Violating one is a bug, not a matter of taste.

1. **Departures never overshoot, and are never more energetic than arrivals.** Exits use
   easeInCubic or a plain fade.
2. **Leaving is faster than arriving**; retraction is faster than growth (90 vs 110 ms).
3. **Never exit by reversing the arrival.** *Incident:* an exit played the arrival timeline
   backwards; stars un-popped through a reversed easeOutBack, rays fired again, confetti rose. Write
   a dedicated exit, and clamp painters at their end state while it runs.
4. **Nothing jumps in one frame**, except a deliberate cut (a change while covered, §6.6; reduce
   motion, §10).
5. **Retarget from the current position and velocity.** When a spring's target changes, start a new
   simulation from where the value is and how fast it moves, never from rest. When an override
   ends, spring back from the moment it ended, not from this frame, so the motion is identical at
   any frame rate.
6. **One side owns the easing.** Eased twice = snap, then crawl. Simulate eased timelines frame by
   frame: a "pop" keyed to an eased input once lasted a single frame.
7. **Cap the cycle rate of anything that must read as repeating motion** (legs, wheels, wings) at
   6 Hz, ≥ 10 frames per cycle at 60 Hz; below ~8 frames per cycle it strobes backwards. Character
   locomotion: `references/domain-games.md` §Mascot.
8. **Key tweens per entity.** A tween animates from the last value it showed, so a new entity must
   start settled. *Incidents:* a chapter's progress road ran 0.8 → 0 when the chapter changed;
   counters popped on every level change.

**Personality (slots the feel brief fills).** Decide these once, record them in DESIGN, and apply
them everywhere; a value chosen per feature is the drift §1.2 forbids.

9. **Overshoot on arrival.** If the identity uses overshoot, arrivals carry it and departures never
   do (rule 1). *Example (shipped puzzle game, a toy):* every arrival on easeOutBack; things that
   arrived long ago "breathe" on a half-sine with no overshoot. *Example (hypothetical banking
   app):* arrivals on easeOutCubic or a critically damped spring (bounce 0); nothing carrying data
   or money overshoots, because a number that bounces past its value reads as wrong for a moment.
10. **Refusal shape.** A refusal always decays and ends; a constant wobble reads as broken. The
    shape is personality: a damped sine (*example:* two swings decaying as (1−t)² over 320 ms), a
    resistive stretch (§11.6), or, for a sober tool, a static mark and a one-line reason.

## 5. Model first, picture second

State rules (commit first, events to sinks) live in `references/architecture.md` §3. For motion:

1. **A move counts the instant it is legal; the picture catches up** from a "before" snapshot. No
   outcome depends on an animation. *Rejected:* animate-then-commit, because every other system
   must then reason about half-applied state.
2. **New input during an animation hurries the in-flight one home** (~4× speed, floor 70 ms, cap
   200 ms), then starts. **Never queue**: a queue shows results before their animations and the
   model drifts ahead. **Never teleport**: snapping deleted a piece hovering 200 pt from its slot in
   one frame and dropped 3 of its 4 landing cues.
3. **Give each animation an id** (a completion for a stale one is a silent no-op), and **freeze
   presentation facts on the event at commit time** (did this complete the level? did the target
   fill?); never ask the live model later what an old animation achieved. Status overlays (won,
   stuck) wait for the animation to finish, so they never appear over something in mid-air.
4. **Never block input with an animation.** Only *named* sequences may hold input (the completion
   run), each tap-to-skip after a short guard (~300 ms), landing the final state with **the next
   action live within 300 ms, proved by a UI test**. Any other input block needs its own DECISIONS
   entry (*example:* a consent-form hold during which nothing animates, at most 5 s).
5. **Panel buttons take touches once readable** (~0.3 of the arrival, or half shown; the primary was
   live ~80 ms into its rise). A tap anywhere during the beats completes them. The first accepted
   exit sets a latch synchronously and disables every exit from that frame; one route change at a
   time. Test: tap where the button *will* appear, within 200 ms. *Incident:* buttons live from
   frame 0 caught the finger that finished the last move, and for ~1.2 s after Continue the fading
   panel still took taps: Replay was overridden by the stale chain, levels were skipped,
   interstitials doubled.
6. **An animation that never runs must still settle** (zero-size layout, offscreen), or input
   wedges forever.

## 6. Sequencing: causes, order, overlap

1. **Effects follow causes.** Time a reaction to the *visual* contact, not the logical commit:
   compute contact time from the growth curve and delay pop, colour change and particles by it.
   *Incident:* a target popped at the commit, but the growing segment touched its edge ~35 ms later.
   Stamps likewise wait for their segment to grow in.
2. **Sound and impact land on the same frame; sound never comes first.** Timeline constants mark the
   *landing*, not the launch; derive landing times from the same function the painter calls, never
   a second copy of the formula. Accept platform latency on the late side; do not compensate by
   guessing. *Incident:* a cue 90–165 ms before the star landed: "sound before impact is uncanny in a
   way sound slightly after impact is not."
3. **Celebrations play in causal order, not size order.** Level-end before chapter-end. *Incident:*
   a chapter chest fired first "so the bigger moment isn't buried", and the reward arrived before the
   player knew they had finished the level. Write causal order on paper before choreographing.
4. **Content arrives before its container.** A box drawn empty then filled reads as a form loading.
   *Examples:* a completion stamp lands on the solved board before the card that frames it
   develops; a ledger box rises with its first row; a container is never shown empty between two
   contents.
5. **Overlap hand-offs; never leave dead time.** *Incident:* waiting for a 300 ms recede to finish
   left "300 ms of a darkened board doing nothing"; handing over 40 ms into it lands the next beat
   as the board comes to rest. In a level transition the exit ends as its last tile goes and the
   entry starts with its first tiles already popping (−40 ms).
6. **Never two copies of the same thing on screen.** *Incident:* a card fading in over the board it
   pictured, smaller and tilted, read as a double exposure; it now *develops in register* exactly
   over the board, then settles to its tilt.
   - **Never fade something that moves.** A layer is opaque while it moves, or still (or off screen)
     while it fades. Per-frame guard: "whenever 0 < opacity < 1, the layer is still or off screen".
   - Overlays leave by dropping away **opaque** (260 ms), not by fading over what they covered.
     Sheets slide opaque; only the dim fades.
   - Between screens sharing an element (a mascot, a header): fade the content over an opaque
     backdrop, then the backdrop. Never scale a full scene (a scaled backdrop doubles the horizon).
     Per-frame guard: "the shared element is gone, or the backdrop is opaque".
   - A whole-screen snapshot crossfade shows anything moving at the switch twice: start no motion
     with the switch, and fade fast-then-soft (easeOutCubic). Under an outer fade, inner elements cut
     (two crossfades for one change cost twice and blend twice).
   - A change made while a screen is covered, or in its first two frames after uncovering, is a
     **cut**, or two themes show at once.
7. **Words follow the event they name.** The line naming a reward rises after the reward lands (it
   once rose with the sign, naming the present before its bow was untied).
8. **Cap durations that scale with content, and test over the largest content.** *Example:* a run
   lasts `clamp(N × 45 ms, 1200, 2400)`; a reveal "ends by 1.85 s on every board", tested over the
   busiest content because at per-item pace a 22-item reveal ran 2.96 s. Bound staggers too,
   `delay = min(i × step, 1 − span)`; without it items past the 12th were never drawn.
9. **The app leaving mid-show settles it silently** to its end state, with no sound or haptic (they
   would land after the user has gone, audibly on Android). Cancel timer holds in the background and
   restart them on return; wall-clock timers fire overdue.
10. **Ask "what if it changes while it moves?"** of every animated element: the setting, the app
    state, the next input. One review found 11 faults, all of this kind; it is the change-while-moving
    edge check of the quality bar (`references/visual-design.md` §The quality bar).

## 7. Rewards and payoffs

In an app, read "reward" as a completion or confirmation: a done task travels to its list, a payment
settles into the balance (`references/domain-apps.md`). The order and honesty rules are the same.

1. **Rewards travel; counters change only when they land.** *Starting values:* 520 ms easeInCubic on
   a fixed arc of height 0.25 × distance, bulging toward the item's own side so flights from both
   halves swing outward instead of crossing; the item emerges small (0.45), swells to 1.5 in the
   first 22% (never covering the source digit) and shrinks into the slot; landing 1.25 → 1.0 over
   240 ms easeOutBack, with a land sound. A thrown object peaks at ~42% of its window and **lands at
   ~88%**, then fades; a single quadratic Bézier peaks only halfway to its control point and reads
   as "sitting in the box".
2. **Save immediately, display later.** Persist the reward the instant it is earned; show
   `readout = balance − pending` and release pending on landing. A force-quit mid-flight keeps the
   reward; only seeing it arrive is lost.
   - **Settle instantly, never withhold,** under reduce motion, with a screen reader, with a missing
     anchor, a zero payout, or the panel already gone. A balance quietly wrong is worse than an
     undramatic one.
   - Count from what the readout currently *shows* (an interrupted count restarting from its old
     value ran the digits backwards). Test by reading the *save* while the display lags.
   *Incident:* the header showed the new balance four centimetres above "+30", so "nothing ever
   arrived anywhere". The owner's words became the test: "the player should feel something was
   added".
3. **Animate only what actually moved; losses change at once** (only arrivals travel). Before
   animating a transfer, confirm the destination value changes on landing. *Incident:* a coin flying
   to the purse on a bonus word would have landed on a counter that does not change (bonuses paid at
   level end); the fix flew the word itself into a jar whose gauge rises.
4. **A reward timeline runs achievement → payment → exits**, one controller, every element an
   interval. *Worked intervals (1.9 s):* panel 0–27%; stars land 29–72% a quarter-second apart;
   payment 62–92% (row pops, number counts up from 0); buttons 80–100%. The exits arrive as **one**
   rise ("three staggered exits = a second drum roll after the drum roll"). The total lands *before*
   the buttons: "a figure still moving when the thumb arrives is a figure nobody saw land". "A
   number that arrives complete is a receipt; a number that runs up to itself is a prize."
   *Incident:* at 520 ms everything landed at once, "information delivered, nothing celebrated",
   and the exits were the first legible thing on screen.
5. **Unearned slots are holes, not dim copies** (how they look: `references/visual-design.md`
   §Chrome semantics). In motion: draw all slots from frame 1; an unearned slot never animates; the
   panel punches on each landing, harder each time.
6. **Small effects for frequent events, big ones for rare.** *Example (shipped puzzle game):* ~50
   per level got a tick, a pluck and a stamp; a milestone, a pop, particles and a flying token;
   completion, the full sequence. Confetti only for the rarest (a chapter, the daily), launched from
   what earned it ("every level throwing paper is every level being the same level"). No
   full-screen flash; a shine along what earned it instead.
   **Every flash obeys the flash-safety rule, whatever the identity.** It is structure, not
   personality: hit flashes, strobing hazards, bloom and music-synced pulses included. Its
   threshold, the guard over recorded frames of the busiest moment, and Motion Off removing every
   flash: `references/ux-and-accessibility.md` §15.
   **Budget screen shake in the feel brief**; many products have none. *Example (calm puzzle):* one
   per level, on the completion impact, never during input ("shake is impact, and a calm puzzle has
   one impact per level"). An action game may shake on every hit; then cap its amplitude and rate
   like any repeating cue (§13); Motion Off removes it (§10).
7. **Aggregate events closer than ~100 ms**: one swell over the run (to 1.035), a tick per landing,
   one pop on the last (1.10, 180 ms easeOutBack). Nine coins 42 ms apart turned per-landing bumps
   into a 24 Hz buzz. Never two cues at one instant: the stronger replaces the weaker.
8. **A run of successes must build.** The Nth success in a row lands differently: a pitch ladder
   per step, praise tiers by run length shown where the eye just was. Break the run on a refusal or
   paid help, not harmless repeats, and never on the completing action. *Incident:* "the fifth word
   in a row landed exactly like the first."
9. **Keep the payoff visible** (the rule and its incident: `references/visual-design.md` §Art
    direction). In motion: transform the element that would hide the reward *as* the reward
    appears, in the same beat, never after it.
10. **Index colour by the final total** (`references/visual-design.md` §Palette structure). Get it
    wrong (dividing by the count drawn so far) and the whole sequence recolours on every step, a
    flicker that only rendered frames showed: check growing sequences in a filmstrip.
11. **The settled frame is the reward screen.** The player stares at it for seconds after the show;
    give it material, a hero and ambient life. A panel ending as a dark rectangle with floating text
    read as "a dialog wearing a drum roll".

## 8. Shows as pure timelines

1. **Every show is a pure function `frameAt(t)` played by one clock** (completions, transitions,
   reward flights, unlocks), with the beat table in its doc comment:

   ```
   /// | ms      | beat                                                                  |
   /// | 0–260   | the completion stamp comes down: 2.2 → 1.0 easeInCubic, opaque by 30 ms |
   /// | 260     | impact: sound, heavy haptic, the one screen shake, a ring 220 ms       |
   /// | 300–360 | the card develops in register over the board it pictures               |
   ```

   *Why:* a frame is identical at 60 or 120 Hz; a skip just jumps the clock and lands on exactly
   the final frame; previews render any instant; tests assert beats by time; the sound generator
   reads the same constants (§16).
2. **Publish each part separately, only when it changes**, so a beat repaints only what moves
   (`references/performance.md`). **Expose motion geometry as pure public functions**
   (`positionAt`, `landingOf`) and assert on them: every sprite on screen, each ends within 12 pt of
   its target, each rises before it falls. Assert a hash's range and spread: a constant hash once
   passed every visual check while stacking 54 confetti pieces on one point.
3. **Look at shows as filmstrips** (`scripts/contact_sheet.py --filmstrip`, frames at fixed
   intervals). A 1 Hz screenshot cannot see a 300 ms beat, and an order fault is invisible in any
   still. Sample densely for bounds: a thrown thing wholly outside the box touches no edge at its
   peak.

## 9. Ambient life

1. **The feel brief sets the ambient amount; stillness may be a decision, never a default.** A
   screen identical a minute later reads as a document, so a still screen needs a recorded reason
   (a tool whose live state is its life: `references/domain-apps.md`). Where there is ambient life,
   keep it at the threshold of perception. *Ceiling (calm puzzle games):* one slow wandering
   background plus one focused beat; never add a second because you can. A plaque breathing over
   4.4 s is "only noticed by looking away and back"; turning a background up "is how a background
   stops being one" (rays held at 0.3).
2. **Starting numbers (calm games):** breathing 1.0 ↔ 1.012 on a 3.2 s sine; for a character, a
   120 ms blink every 2.5–6 s and a 200 ms twitch every 8–14 s (behaviour while the user acts:
   `references/domain-games.md` §Mascot); at most 24 particles per scene (9 for delicate ones),
   drawn behind the content.
3. **Deterministic:** variety from a fixed seed or index hash, never a random number at paint time.
4. **One process-wide switch, off unless the app's entry point turns it on.** Tests never run the
   entry point, so every "wait until settled" terminates; tests covering ambient motion turn it on
   explicitly. Also off under reduce motion and low quality, and then **removed, not frozen**:
   frozen particles read as dirt.
5. **Own clock, own layer**, running only while something can change. Complete whole cycles within a
   period and wrap time there; long-running float time loses precision and the wrap jumps.
6. **No screen freezes by accident after its show.** *Incident:* "every pixel identical for as long
   as the player looked, on the one screen the game is played to reach." Measure with lossless
   screenshots 14 s apart (once fixed, they differed over 33.8–46% of the panel), never video
   frames: ~10% of pixels change between identical h264 frames.

## 10. Reduce motion: presentation off, the task kept

1. **Follow the platform setting plus an in-app override** named for motion, not for reducing it:
   "Motion: Auto / On / Off" (Auto follows the platform's reduce-motion setting, the same word as
   every other follow-the-system setting; On plays motion; Off is the no-motion path of the
   canonical rule below), folded into one switch at the root that every element reads live.
2. **The canonical rule.** This is its one home; other files restate it in one sentence or link
   here:

   > Motion Off removes presentation motion: transitions, shake, hit-stop, flashes, parallax,
   > camera moves, ambient life, celebratory shows. Motion that IS the task (a real-time
   > simulation, a video, a live map) continues. Outcomes are identical for the same input. Assists
   > that change the task (slower speed) are separate, labelled options, never the Motion switch.

   For presentation motion, **Off means nothing is scheduled**: not faster, not simplified. No
   clocks, no controllers, zero-length transitions; states snap. A moving task still loses its
   presentation layer: a run's hazards keep moving while its camera stops shaking. *Why the split
   (a trial build of a real-time game):* the hazards' movement is the play. A switch that stopped
   it would make the game unplayable for every player with the platform's reduce-motion setting on
   (Auto follows it), and one that slowed it would change the outcome.
3. **Every outcome is identical for the same input, proved by a test**: progress, money, times,
   streaks, hints, navigation, and the same events, sounds and haptics. *Why:* off-is-off failed in
   more than six places in one critique (a whole mode never got the flag; a counter popped on every
   change; a toast's controller doubled as its display timer; a fix defaulted a new effect to
   "animate"), and the platform setting was never read: "for a vestibular trigger … it is a setting
   that did not work."
4. **Keep a static outcome signal.** A refused action must not be pixel-identical to a dropped
   touch: show a brief static mark on a timer, not an animation.
5. **Off removes the animation, not the state.** A pressed button still takes its pressed size, on
   the frame.
6. **Read the setting at the moment of the action.** Some frameworks fix a transition's duration
   when the route is created; turning motion off in Settings must make that screen's own Back
   instant.
7. **Delayed cues play immediately when there is no motion**, but never stack two loud cues on one
   frame ("two loud cues at once are worse than one"): drop the lesser.
8. **Every animated element takes the flag and documents its no-motion path** (for motion that is
   the task: "continues", its presentation layer removed); its default must never silently be
   "animate". Rewards settle at once (§7.2); ambient motion is removed (§9.4). Framework
   traps: `references/stack-flutter.md`.

## 11. Input feel: grid and drag input

*Starting values come from a grid game with drag input. For apps, the same rules govern swipes,
sliders, reorderable lists and drawing. Steering an avatar in real time follows other rules (zero
positional smoothing, a finger offset, a constant hitbox smaller than the art, a latency budget
measured on a device): `references/domain-games.md` §14 Real-time and action games.*

1. **The first touch responds on the frame.** For dragging and drawing, read raw pointer events:
   gesture recognisers wait for a "slop" distance before reporting a drag, and "that delay is felt"
   (Flutter's value: `references/stack-flutter.md`). Commit direct manipulation on pointer-down, not
   tap-up, with one active pointer.
2. **Hysteresis at boundaries:** commit a move only after the finger crosses the shared edge by a
   margin (0.12 × cell), so nothing flickers at the border.
3. **Fast and slow input end in the same state.** A fast swipe that skips cells walks toward the
   finger one legal step at a time: the axis with more cells to go first (ties: the axis the finger
   moved further), stopping at the first refusal, the loop capped at 2 × the cell count.
4. **A generous grab:** a touch finds the nearest valid handle within 0.6 × cell (ties to the more
   recent); touching an earlier part of the path cuts back to it and the drag continues.
5. **A harmless miss answers "start here", not an error:** pulse the place to start twice
   (2 × 300 ms), no error sound, no haptic. An idle pause mid-task (1.5 s) gets a "continue here"
   pulse.
6. **Touch has weight, even when refused.** Held against a wall, the end stretches with resistance
   `d′ = 0.22 · tanh(d / 0.22)` cells and snaps back with `spring(240, 0.4)`; measure *d* from the
   commit band so it grows from 0. If the stretch would hide under an overlying element, lean that
   element instead (≤ 0.07 × cell; at 0.09 a sliver of the layer below showed). A disabled button
   still presses and says why: a dead button tapped at zero coins was pixel-identical before and
   after, so it "reads as broken, not refused".
7. **A refusal fires once per contact.** A finger held against a wall keeps being refused, but the
   event, sound and haptic fire once; each *different* refusal in the contact fires once too. A
   contact ends when the finger lifts, returns inside the head's own square (not merely the commit
   band, so a finger wavering on the band never repeats), the path changes, or an accessibility
   action runs (each is its own contact).
8. **Map every refusal reason to exactly one feedback row, or mark it silent on purpose.** The
   refusal the rules return is the event the UI reacts to (`references/domain-games.md` §Core loop).
9. **Cancel discards.** When the system takes the gesture, nothing steps toward the cancel position;
   committed steps stay. Extra fingers are ignored. If the model changes under a held finger for
   another reason (Undo with a second finger, a new session), the drag ends and needs a fresh touch,
   or walking on from the new head would commit cells the player never drew.
10. **Decorative overlays never take touches** (tutorial ghosts, flights, fading snapshots).
11. **Targets ≥ 44 pt; the visible solid part is the target** (`references/ux-and-accessibility.md`).

## 12. Haptics

1. **One haptics table, fired by the same choreographer** that plays the event's motion and sound, so
   they never drift apart. The step gate exists because a fast swipe commits several cells in one
   frame, and a click per cell blurs into a buzz.

   | Moment | Haptic | Limit |
   |---|---|---|
   | frequent step (cell, letter, tick), step back | selection tick | ≤ 1 per 35 ms, shared gate |
   | multi-step undo / reel-in | light impact | once |
   | milestone | medium impact | — |
   | refusal | see rule 2 | once per contact |
   | completion | success notification | — |
   | the one impact, if the brief has one | heavy impact | — |

2. **Give a refusal the weight it needs to be noticed; decide per project and record it.** Where a
   refusal has no other strong signal it gets the **heaviest** haptic, because it is the only cue
   that anything happened (*example, sort puzzle:* a refused pour). Where motion and sound already
   carry it and it can repeat under a held finger, use light, once per contact (*example, shipped
   puzzle game:* a wall).
3. **The stronger haptic replaces the weaker**; never two at one instant (a move that completes a
   target gets medium *instead of* the move's light, never both).
4. **Never await, never throw.** Detach the call and swallow its error; a failing vibrator must not
   take a move down. No timer per click. Haptics obey their own setting, go silent when the app
   leaves (§6.9), and are unchanged by reduce motion.
5. **Accept silence where a device lacks a type.** No fallback pattern: "a different buzz on old
   phones would be a second design to tune".

## 13. Cue scheduling

1. **Rate-limit by skipping, never queuing.** One gate per cue family with a minimum gap; extras are
   skipped. Starting gaps: step 45 ms, milestone 60, count tick 40, hint dot 30, selection haptic 35.
2. **Set the gap below the visual stagger, allowing for frame quantisation.** Dots staggered 40 ms
   apart fire on frames that can be 33 ms apart at 60 Hz; a 40 ms gate dropped a third of them,
   unevenly. The gate became 30 ms.
3. **Make each counting step ≥ gate + one frame** (60 ms), so every change of the number is heard.
   Give a repeating top rung a second voice, so it does not cut itself off.
4. **Drop late cues.** A cue whose file was not ready within 150 ms is stale (out of step with the
   eye) and dropped, except in the first 100 ms after unmuting (the toggle's own confirmation must be
   heard). A frame returning from the background must not fire a pile of pops.
5. **Fire and forget:** "a platform round trip must never sit inside the frame that asked for the
   cue."

## 14. Sound identity and system

1. **Start from the sound brief** (its contents: `references/kickoff.md` §7.4 The identity brief).
   Turn it into the sound list in DESIGN, `| id | when | character | level | min gap |`, one row per
   moment the domain reports (rule 3), before generating a single cue.
2. **Decide the kind of sound system in the sound brief**; the rest of this file applies to all
   three kinds:
   - **tonal**: pitched cues in one scale or family, tied to the product's structure;
   - **textural or foley**: material sounds, filtered noise, recorded actions, no melody;
   - **minimal**: one press, one confirm, one soft refusal, often off by default (many tools).

   One proven method is a tonal, musical system; it is one project's answer, not a default.
   *Example (shipped puzzle game; do not reuse the motif unless your own identity derives it):* an
   acoustic set (kalimba, ukulele pluck, glockenspiel, woodblock, shaker) in one major pentatonic
   scale, so any overlap is consonant. Each cell drawn climbs one rung of a step ladder that resets
   at each numbered milestone and caps at 12 rungs (2 octaves); stepping back plays one rung lower
   at −4 dB from the same files. Milestone *k* plays scale degree *k*, so a level builds a melody,
   and the finale replays each milestone's chime. **Bound the range:** a plain one-degree climb
   would span 4.5 octaves by the 22nd milestone, so milestones became rising phrases, each a degree
   higher, within an octave and a fifth.
   *Example (word game, tonal):* a pitch ladder per letter traced; backing off steps down (the rung
   is the length, not a touch count); distinct degrees, not the octave twice.
   *Example (hypothetical dark sci-fi game, textural):* cues built from filtered noise bursts and
   metallic resonances; progress shown by brightness and density rather than pitch.
   *Example (hypothetical expense tool, minimal):* off by default; when on, three soft cues with
   bodies above 300 Hz (§15) and nothing for routine scrolling.
3. **The domain reports moments; sinks decide how they sound and feel.** The rules layer emits a
   closed set of moments and never names an asset. Adding a moment is deliberately multi-file (the
   moment, the mapping, the pack, the ordered-list tests): the cost is the point. Each refusal reason
   has its own cue. A null sink is normal, and a silent player is both test double and production
   fallback: "a game that won't start because it couldn't open audio is worse than a quiet one".
   Map themed variants by a pure function, theme → material → cue, held by a test so a restyled theme
   cannot keep an old sound.
4. **Build cues in layers, whatever the kind.** A cue with more than 90% of its energy in one band
   reads as a beep. *Incident:* a "well-formed, licence-clean" pack "was a beep": 21 of 22 cues
   failed that test, and a "shimmer" was an 825 Hz low-pass. Give every cue a body, a transient
   (air or strike) and its own decay, then soft saturation (creates harmonics) and a short reverb
   (so nothing happens at zero distance). *Example (acoustic tonal set):* the rebuild added a bell
   with stretched partials (each with its own decay and a detuned twin) and sparkle grains at
   1.7–5.3 kHz. Frequent cues are mono, close and small; stereo only for rare moments. On a phone,
   the body must sit where the speaker plays (§15).
5. **One loudness ladder, in one place.** Every cue names its rung; one global effects gain. A
   per-cue volume override is a second ladder: once one multiplied in, a three-step reward phrase got
   *quieter* across its steps. Starting rungs on the loudest 50 ms: quiet −21, medium −15, loud
   −11 dBFS, each with a peak ceiling. Normalise on loudness (K-weighted, BS.1770), never on peak;
   peak normalisation makes the mix an accident.
6. **Success grows in weight, not brightness, in every kind of set.** Each step of a success phrase
   is ~2 dB louder and heavier (more body) while energy above 2 kHz *falls*. *Incident:* steps with
   46–50% of their energy in 2–6 kHz (the ear canal's resonance) were "loud and painful", rebuilt
   to 30 → 28 → 16% above 2 kHz.
   *Tonal sets (example, two shipped games):* weight came from a chord and the octave below, and
   the last note landed on the octave; stacked fourths ending a minor seventh up "sound like a
   fourth star is still coming". A falling figure was reserved for failure or "time up", because
   every reward rose. A textural set resolves the same way with its own means (a denser, lower,
   longer final layer).
7. **Music is optional**, with its own switch; its default is a sound-brief decision (example,
   shipped puzzle game: off by default, because effects confirm what you did and music plays
   uninvited). Stop it in the background ("a puzzle game has no business playing under somebody's
   podcast"). Duck it under reward UI and restore it at an explicit "sequence ended" bookend, not a
   timer.
8. **Model the physics of continuous sounds** (pours, runs, rain): a pour loop's crest factor rose
   from 12.1 dB (plain noise) to 17.9 dB once built from bubble events. Write events modulo the loop
   length so the seam wraps (a crossfade plays transients twice; the seam's RMS jump fell 28% → 4%),
   and drive pitch from real state, clamped and throttled (~40 updates per pour, not 601).

## 15. Mastering for the phone speaker

The phone speaker is the reference listener, not headphones.

1. **Judge every cue through a phone-speaker model.** Measure the loudest 50 ms at full band, through
   a 250 Hz high-pass, and through a steep 350 Hz high-pass (optionally 500 Hz and 1 kHz, or two
   cascaded 2-pole high-passes at 700 Hz). Tabulate: `| cue | built as | length | full / 250 / 350 Hz
   dBFS |`.
2. **Guard it in tests:** quiet < medium < loud holds through every filter; no cue loses more than
   3 dB to the 250 Hz filter; no new cue keeps more than **2% of its energy under 250 Hz**. Pin the
   spectrum, not only the level: a body moved to 150 Hz changed no level enough for any level guard
   to see.
3. **Tonal bodies at 300 Hz and up.** *Incident:* mastered on full-band loudness, an impact with a
   118 Hz body dropped under the medium cues on a phone, and a footstep patter at 170–205 Hz almost
   vanished; rebuilt from 330 Hz, both held their rungs. A sub layer may add warmth on headphones but
   never carries the cue's level.
4. **Match families on the phone measure.** Cues built above 300 Hz play 1–6 dB louder on a phone
   than a lower-bodied reference at the same full-band level. Trim per-theme variants to sit just
   under the reference cue through both filters, so no theme is louder on a phone.
5. **Fix a sinking cue by high-passing it, never by turning it up.** *Incident:* a +2 dB trim made a
   recording the loudest medium cue on full band and the quietest on a phone; a 450 Hz high-pass and
   no trim made it 2.9–3.8 dB louder on the phone. A cue below its rung loses its sub.
6. **Budget the pack's size** and fail the build over it (one project: 9 MB).

## 16. Sound in step with motion

1. **One sound file per choreographed show, built to its beat map** (`| ms | the show | the sound |`).
   *Example (shipped puzzle game, a 3.1 s unlock):* hinges creak over 40–600 ms, gliding with the
   gate's speed; a "ta-DA" strum lands as the name rises (1220–1300 ms), 2.7 dB under the landing;
   the resolving chord, the file's loudest moment, lands with the gift on the hero at 2450 ms and
   rings out to 3100 ms.
2. **Share the beat constants and test them.** A test reads the generator's copy of the beats
   against the app's choreography constants, so changing a timing fails until the sound is rebuilt.
   *Incident:* a swell read 600–1300 ms in the generator and 450–1350 ms in the app.
3. **Model the framework's real easing curve.** A named curve may be a cubic Bézier, not the
   textbook polynomial; a sound placed "at 98% unrolled" with the polynomial came 20 ms early. Shape
   a sound to its motion curve (a paper rustle slows with the roll).
4. **Beat guards check the level and count each beat must carry**, and end the window before the
   next beat: "does something start near T" passed with the main strum removed.
5. **Define a skip's effect on sound.** A skip silences the sound while the show still has story to
   tell; from a `ringsOutFrom` time it only rings out. *Incident:* the expected tap on "Next" at
   ~2.7 s was itself a skip, and cutting the chord there stopped it near −10 dBFS. A stop that
   arrives while a play call is in flight wins (a per-file stop counter).
6. **Warm show files right after the first gesture's files**, so a show opened just after launch is
   not silent.

## 17. Sound plumbing, generation, licences and the owner's ears

**Plumbing** (Flutter specifics: `references/stack-flutter.md`):
1. **Policy out of the plugin.** Voice pools, rate limits, the cold-start window, mute and loops live
   in a player class over a narrow backend port; the platform adapter is thin, one call per method.
   *Incident:* an untested 590-line plugin file shipped 3 of 4 audio bugs.
2. **A pool of players per file**, sources set once, replay by stop + resume (re-setting a source
   re-prepares it); one dedicated player per loop.
3. **Lifecycle as desired-state reconciliation:** one sync point reads "setting AND foreground AND no
   suspension" and acts only on change. Suspension reasons (background, an ad) are independent;
   neither resumes over the other. Re-apply your audio session after every full-screen ad
   (`references/monetization-and-privacy.md` §3).
4. **Bound every platform await** (calls 1 s, loads 3 s) and give up on a voice that does not answer.
   **Sound off creates nothing**: no player made, configured or called while muted. **A missing or
   failed cue is silence, never an error**; remember failures for the session.
5. **Preload the first gesture's files before returning**; warm the rest one at a time in the
   background. Test bundle drift: every named cue exists, every shipped file is used.
6. **Every button presses audibly**, secondary and close controls included, asserted per control in
   tests. *Incident:* a Stay button, an archive's close and a re-tapped settings segment were silent.

**Generation.** Synthesise UI sounds in code with a versioned generator that builds identical bytes
on every machine, with a `selftest` that exits non-zero and a `preview <cue>` plotting waveform, dB
envelope, spectrogram (speaker floor marked) and the show's beats. Code-built sound can be diffed,
tested and rebuilt by the builder; record the choice as a technology verdict
(`references/kickoff.md` §5.4).
- *For an acoustic, tonal set (the source's choice):* modal synthesis for mallets; Karplus-Strong
  for plucks (with a fractional-delay allpass, or they play out of tune; test pitch against the
  intended note); FM or additive for bells; filtered noise for shakers.
- *For a textural set:* shaped and filtered noise, granular synthesis from a short source, or
  recorded foley run through the same scripted chain.
- *Every kind:* each cue gets its own seeded noise stream (with a shared one, changing one cue
  shifts every later cue), seeded by a stable hash (crc32), never a per-process salted one. DC
  hygiene: give resonators a zero at DC and remove the mean after fades. Record only what cannot be
  synthesised convincingly (animals, voices), under the licence rules below.

**Licences.** CC0, or paid with the licence text verified (worldwide commercial use in apps,
one-time, no attribution). Log every file with URL, author, licence and sha256; keep originals byte
for byte and process them by a scripted, deterministic chain. Never put paid sources in a public
repository. Avoid marketplaces whose licences exclude apps or are per-project or subscription. Buy
nothing without the owner; downloads behind a login are the owner's to do.

**The owner's ears.** The builder cannot hear: say so in one sentence and build the owner an
instrument (`references/working-with-the-owner.md`). A private listening page with every cue grouped
by moment, sequence buttons (ladders, melodies, A/B pairs), Good / Weak and a note per cue, an
overall verdict, the instruction "listen once on the phone speaker, once with headphones", and the
verdicts stored where you can read them back. Keep a researched, licence-checked paid fallback in
tiers (best value, biggest single upgrade), and buy nothing until the owner has judged. *Example:*
the owner judged a synthesised set "not bad, suitable"; nothing was bought, and "re-judge on a real
device" went on the device list.

> **Dated facts (as of 2026-10 — re-verify before relying):** iOS could not decode Ogg Vorbis, and
> looped MP3 clicked (encoder padding), so loops and predictable onsets used WAV; 22.05 kHz mono
> 16-bit WAV was fine for short cues (one project used 44.1 kHz for one-shots). A cross-platform
> audio player in use changed speed without changing pitch on iOS (pitch variants became separate
> files) and looped by seek(0) + resume, which is not gapless (loop seams sat in silence). The iOS
> "ambient" audio category mixes with the user's music and obeys the silent switch; full-screen ad
> SDKs may leave the session in "playback". Measured iPhone speakers were nearly silent below
> ~300 Hz. Android's "success notification" haptic needs API 30+ and is silent below it. Re-read the
> installed player's source and the platform docs before relying on any of these (stack specifics:
> `references/stack-flutter.md`, `references/stack-other.md`).

## 18. Verifying feel: definition of done

Feel is proved by tests that see *time*, and by looking. Test shapes and mutation proofs:
`references/verification.md`; frame budgets: `references/performance.md`.

- [ ] Every number lives in the constants file with unit and source, time-based; the design doc has
      the event tables and "as built" notes. Every personality value (overshoot, bounce, ambient
      amount, shake budget, hit-stop, refusal weight, sound kind) traces to the feel or sound
      brief. Departures never overshoot; no exit replays its arrival.
- [ ] Each named blocking sequence is tap-to-skip with **next action ≤ 300 ms (UI test)**; nothing
      else blocks input; a tap where a button *will* appear is handled; input during motion hurries
      the old animation home (no queue, no teleport).
- [ ] Effects follow their visual cause; sound lands on the impact frame, never before. Content
      before container; no dead time; never two copies on screen (per-frame guards).
- [ ] Rewards travel; the display lags, the save does not; instant under reduce motion or a screen
      reader; tested by reading the save mid-flight. Content-scaled durations are capped and tested
      over the largest content.
- [ ] Every show is a pure `frameAt(t)` with a beat table, looked at as a filmstrip.
- [ ] Motion Off removes presentation motion (transitions, shake, hit-stop, flashes, parallax,
      camera moves, ambient life, celebratory shows) and schedules none of it; motion that is the
      task continues; outcomes identical for the same input (test); assists are separate, labelled
      options, never the Motion switch (§10). Static outcome signals, pressed states shown.
      Ambient motion gated, deterministic, off in tests, removed rather than frozen. Leaving
      mid-show settles silently; late cues are dropped.
- [ ] Every flash within the flash-safety rule, guarded over recorded frames of the busiest
      moment (`references/ux-and-accessibility.md` §15).
- [ ] Input (grid and drag, §11; a controlled avatar instead meets `references/domain-games.md`
      §14.2: zero positional smoothing, device-measured latency, constant hitbox, the
      time-to-retry test): first touch on the frame, hysteresis, fast = slow, generous grab, refusals once per
      contact, cancel discards, every refusal mapped or deliberately silent. Haptics: one table,
      rate-limited, never awaited, stronger replaces weaker.
- [ ] Sound: one ladder; phone high-pass tiers and low-energy share tested; beats tested against
      code constants; skip semantics defined; sound off creates nothing; every button presses
      (test); licences logged.
- [ ] The moment was **played on a simulator or device**: "three of the worst bugs were invisible to
      every test and obvious in one played level".
- [ ] The owner has listened and judged the sound, or it is on the end-of-project list.

More traps of this kind: `references/traps.md`.
