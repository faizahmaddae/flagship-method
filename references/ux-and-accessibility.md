# UX and accessibility

The interaction rules that keep a product easy, honest and calm whatever its word budget, the
accessibility work that was built as a feature and audited by tests rather than ticked off, and
localisation into other scripts, directions and calendars. Every rule comes from a fault found in a
past product, its review or a trial run of this method.

**Read when:** designing any screen, flow, state, onboarding, offer, system prompt or piece of copy;
before calling any screen done; when writing the per-screen plan in `docs/<slug>/DESIGN.md`; when a
second language, a right-to-left script or a non-Gregorian calendar is in scope.

**Contents:** Part A, UX: 1 Word budget · 2 Copy precision · 3 Onboarding that teaches by doing ·
4 States · 5 Stuck users · 6 Controls that tell the truth · 7 Honest offer UI · 8 System prompts at
safe moments. Part B, accessibility: 9 Semantics · 10 Touch targets, measured · 11 Live regions ·
12 The core loop by screen reader (real-time play) · 13 Text scaling by tier · 14 Layout switches by
measured fit, and masking traps · 15 Flashing and photosensitivity · 16 Reduce motion · 17 Colour
assist · 18 The audit. Part C: 19 Localisation, RTL and calendars

The look of these screens follows `references/visual-design.md`; their motion follows
`references/motion-and-feel.md`; the identity they express is the project's own
(`references/kickoff.md` §Identity).

---

## Part A: UX

## 1. Word budget: decide it, then plan every word

The word budget is an identity decision (`references/kickoff.md` §7.4, Voice), never a default.
Example (shipped puzzle game): nearly wordless, for a global casual audience and a working surface
that carries state; the category lesson was "every pixel either shows state or is the single
action". Example (contrast): a budgeting, reading or productivity app is word- and number-dense, the
words and figures are the product, and the budget limits chrome words, never content. The budget
also sets the cost of every extra language (section 19).

For every budget:
1. **Plan the exact words for every state before building**, in the screen's plan in DESIGN.md
   (`references/visual-design.md` §13). An unplanned state gets improvised copy, and improvised copy
   is where over-claims creep in.
2. **Put state on the thing it describes** (a count on a button's badge, the next target on the
   hero), not in a label beside it.
3. **Pictures keep their size and speak their words.** A badge, a board digit or an icon does not
   scale with text size; its label goes to the screen reader (section 13).
4. **No pointing-hand tutorials and no coach marks over chrome** (section 3).

With a nearly wordless budget, also:
5. **The working surface and the hero are the interface**; state lives on them, not in labels round
   them (e.g. the next target shown on the mascot).
6. **One screen carries the words** (usually Settings). Elsewhere, words appear only where a picture
   cannot carry the meaning: the reason for a state, the truth of an offer, a setting's name.

## 2. Copy precision

Every sentence the product shows is a claim about the code. Rules, each from a real fault:

1. **Never over-claim.** Status wording describes the arrangement, never a completion the app cannot
   know. Cloud backup that uploads on the operating system's schedule is never "synced"; it is "Your
   progress syncs with your account". Where the app cannot know at all (a system backup it does not
   control), say nothing rather than promise. Wording that might under-claim is acceptable.
2. **Words follow the event they name.** A line naming a reward rose before the gift was opened;
   it now rises after the reward lands.
3. **Copy must match behaviour exactly.** A payout row labelled "without help" paid players who had
   used help; a coach line described the hint's old behaviour. Map each claim to the code that makes
   it true (store copy: `references/release-and-store.md`).
4. **Error copy names the true remedy.** An offline game told players to check their connection.
5. **One word, one meaning, across the product.** "Auto" means "follow the phone" in every setting
   (Auto / On / Off). The spoken label starts with the visible word and the explanation goes in the
   hint, so voice control's "Tap Auto" works.
6. **A navigation label is a promise about its destination.** Test it by the screen reached.
7. **Counts come first.** "2 bonus words" is a count; "bonus 2" or "bonus #2" reads as an ordinal
   (the second bonus). One word must not mean two numbering systems on adjacent surfaces.
8. **Show "+N" only when N > 0.** "+0 reads as a taunt."
9. **Show only what the save actually holds.** "Total play time is not tracked, so not shown."
10. **Answers to a purchase or a link are one quiet line under the row, never a dialog:** buying,
    pending, failed, cancelled, restored, nothing found, restore failed.
11. **Refusals at the moment of need are calm, not validation errors.** A stuck state "announced in
    the language of a validation error" (a slim red banner) arrived exactly when the user most
    valued help.
12. **After success, the card becomes its thanks** ("Thanks!", one line, OK), not the question with
    a thanks appended.
13. **Keep phrase atoms together** with no-break spaces ("1 more hint", "a day").
14. **Banned words are per project and asserted absent by a test** on every offer and status string,
    in every language. A word is banned because it would be false in this product: "no ads" and
    "free" were banned in an ad-funded game; a product with truly no ads may say so once the copy
    checker maps the claim to code (`references/release-and-store.md` §5.3).

## 3. Onboarding that teaches by doing

The first minutes are designed, not sampled.

1. **First launch goes straight into the core action.** A map with one node, or a welcome carousel,
   explains nothing.
2. **The first item teaches one idea in about three actions**, and the lesson and the item end
   together.
3. **Hand-design the first items, one rule each, in order.** Example (shipped puzzle game): item 1
   "fill every cell", item 2 "numbers in order", item 3 "drag back to undo". They pass through the
   same verifier as all other content.
4. **Let arrivals teach.** Example (shipped puzzle game): targets drop in in number order, 60 ms
   apart with rising blips, "so the arrival itself teaches the order".
5. **Show, on the working surface:** a ghost finger tracing on the board, a staged reveal. No big
   pointing hand.
6. **Never ask the user to dismiss the lesson.** "Asking them to press Got it is asking them to agree
   that they were taught." The coach is dismissible by tap through the same path as doing it.
7. **Coach cards point at the control they name**, positioned from the control's measured location,
   not arithmetic.
8. **Unlock tools at the moment they become useful** (e.g. at items 2, 4, 7, 10), keyed to the
   furthest progress so replays keep them.
9. **Long-press re-explains a tool, even when it is disabled,** and the user is told the gesture
   exists.
10. **Teach in every entry mode**, not only the main one; a user who arrives through a daily or a
    deep link meets the same first-run teaching.
11. **Let experienced users skip ahead**, with a smaller control than the primary one and a card that
    names where the skip lands and what unlocks (Stay / Skip; a tap outside means Stay).
12. **System prompts wait until after onboarding** (section 8).
13. **Count it.** Once analytics exist, tutorial completion is a launch metric (event rules:
    `references/monetization-and-privacy.md` §Analytics and crash reporting).

## 4. States

Design every state as a screen, with its words, picture and one action. "Whatever state you happened
to screenshot is not the state that ships."

- **Empty, one, full.** Check every indicator at zero, one and full (the quality bar's "Does it read
  at its emptiest?", `references/visual-design.md` §The quality bar). A progress bar that drew
  nothing at 0% met every new user.
- **Empty states invite; they never scold.** A new user opening a weekly view on a Thursday saw
  Monday to Wednesday marked missed and "0 day streak". Days before the first use are a neutral
  "before start" state, like future days; zero reads "Start a streak", never "0 day streak"; stats at
  zero read "Nothing yet" in the product's voice.
- **Never show a record of failure before the user has started.**
- **Busy:** the row in progress stays at full ink; every other control is dimmed and announced as
  dimmed; back and outside taps are refused so the answer always lands.
- **Quiet (unavailable):** keep the same card and say why in one truthful line, plus what happens
  next. Example (shipped puzzle game): "No video is ready right now." / "That's all the videos for
  today." then "Each new day brings one more hint." (true for every user).
- **Live while open, frozen once committed.** An offer reflects live availability until the user
  commits; then it holds that state through the flow. A rewarded video going up made the SDK report
  "not ready", so the card turned quiet under the video and slid away saying "No video is ready right
  now." with the reward.
- **Leaving the app:** a link that opens the browser says so ("Opens in your browser"), ignores
  double taps, and after a 5 s bound shows one quiet retry line ("The page didn't open. Please try
  again.") in a live region.
- **A way back everywhere.** Every pushed screen has an on-screen Back (some platforms have no system
  back on plain routes). A hung loader with no exit is a trap; chrome must exist off the happy path.

## 5. Stuck users

This is the quality bar's edge check E2, "a stuck user sees the way out"
(`references/visual-design.md` §The quality bar). Helpers must be visible at exactly the moment they
matter. In an app that means every error names its remedy, undo is one tap after any destructive or
bulk action, and every flow shows its exit at every step, loading included.

1. **Nudge after idle, in steps.** Example (word game): 20 s idle lights the free helper; 25 s later,
   the paid one. Light only a helper that can be pressed.
2. **Undo and restart are always one visible tap.** Never hidden, never priced: that is the line
   between a hint economy and a dark pattern.
3. **The stuck moment offers the most generous option first.** A priced button the user cannot press
   is a taunt; show it only when affordable, and say where the currency comes from when it is not.
4. **A harmless miss answers with direction, not an error.** A touch that missed the start pulses the
   start silently ("start here"); no error sound or buzz.
5. **Every refusal gets exactly one feedback, or is silent on purpose.** List every reason input can
   be refused and give each a row. Example (shipped puzzle game):

   | Reason | Feedback |
   |---|---|
   | blocked by a wall | bump motion + soft sound |
   | target out of order | target wobbles, next target pings |
   | finishing too early | wave over the unfinished part, "?" |
   | not adjacent (fast swipe) | silent: the swipe stops at the last legal step |

6. **A silent refusal reads as broken.** A dead button tapped at zero coins left the screen
   pixel-identical before and after; users read it as a bug, not a "no".

## 6. Controls that tell the truth

- **A control that does nothing is a bug.** A music toggle with no music shipped; hide a control
  until it is real.
- **A control must visibly do something when it works.** A hint spent a charge and changed no pixel.
- **A refused control looks and sounds refused,** and is announced as dimmed. Its label stays
  legible: a label at 0.5 alpha measured 2.4:1, and "refused" is the state a user reads.
- **Busy is not disabled.** A pill with disabled styling dimmed its busy dots to 38% white on green
  and they all but vanished. Keep the busy control at full contrast and block input separately.
- **Anything pressable is refused in every wrong state.** Undo pressed through a win overlay unsorted
  a won board.
- **An overlay takes no taps until it is readable** (about 0.3 of its arrival), and latches on the
  first accepted exit. A results panel live from frame 0 took the tap of the finger that finished
  the last move; one fading out still accepted taps for 1.2 s and skipped levels. Change while
  moving: `references/motion-and-feel.md` §Sequencing.
- **Every button makes the same press sound and press motion**, asserted per control
  (`references/motion-and-feel.md`).

## 7. Honest offer UI

An offer is a calm card, the same shape everywhere:

- one picture (a vignette that explains the offer without words);
- a title and one truthful line of what it does;
- one primary action and a quiet "Not now".

Rules:
1. **Prices come from the store**, never typed into the app; the price pill scales to fit any
   currency.
2. **An unprompted offer appears once, on a calm screen, after real exposure;** never at cold launch,
   over a task or over a celebration, and never to someone who already owns it (the ad-funded game
   skipped anyone who had bought anything). Afterwards it lives in Settings and at the paid feature
   itself. A paywall is this same card at the moment a user reaches a paid feature, never a wall
   mid-task or before first value (`references/monetization-and-privacy.md` §Subscriptions and
   paywalls).
3. **No pressure devices:** no timers, countdowns, crossed-out prices or other products' names, and
   none of the project's banned words (typically "sale", "bonus", "double", and "free" wherever the
   user pays with money, attention or data); asserted absent by test.
4. **States are written in full** (offer, busy, each failure, thanks) before building.

Monetisation policy, ad rules and purchase plumbing live in `references/monetization-and-privacy.md`.

## 8. System prompts at safe moments

System prompts (tracking, consent forms, age sheets, notification permission, rating requests,
upsells) appear only at a named safe moment, never at cold launch, mid-task or over a celebration.

- **Safe** means, for example: the app is resumed; no sheet, show or ceremony is up; no task screen
  is active; and either home has been idle for 800 ms after returning from a task in this process,
  or a settled result panel has held for 1.2 s.
- **Check and take in one step.** Each presenter re-checks after the current frame and takes the
  moment atomically, so two presenters can never both take it.
- **Hold the moment through network-bound UI.** A form fetched over the network appears 0.5–3 s after
  the call; hold the moment with an invisible touch-absorbing layer hidden from screen readers until
  the form appears (5 s at most).
- **A pre-permission primer has exactly one button** ("Continue"): no close, no "Allow", no
  incentive, no picture of the system alert, copy true for every user; tested to have exactly one
  button and none of the banned words.
- **Ask for a permission after the user has seen its value** (a reminder permission after the first
  habit or task exists, not on first launch).
- **Rating requests** come once, on a settled success after enough wins, never while a share sheet is
  up, and well away from ads in both directions. Request the review directly at that moment, never
  behind an availability pre-check (`references/traps.md` T-135a).

Gate mechanics, record-at-show vs record-at-answer, the rating prompt's distance from ads, and the
platform rules: `references/monetization-and-privacy.md` (§Showing a full-screen ad safely,
§Record-at-show vs record-at-answer, §Consent and the tracking prompt).

---

## Part B: Accessibility, built and audited

Accessibility is a built feature with automated audits in CI, plus a human pass with the real screen
reader on each platform. Each audit below exists because a version without it passed while a user
could not use the product.

## 9. Semantics

- [ ] **Every tappable thing has a label, a role and a ≥ 44 pt target** (section 10).
- [ ] **Each screen names itself with one heading.**
- [ ] **Reading order is stated per screen in DESIGN.md**: top bar → heading → content → thumb-zone
      actions. Set it explicitly: platforms sort by position, so a full-screen scroll's items came
      before a top bar painted over them.
- [ ] **Long lists read from the most relevant item:** the next item, then back, then ahead. On a
      progress map, up to eleven "not open yet" items came first, and moving focus to them scrolled
      the map away.
- [ ] **Composite controls are one node** whose label includes the count or says in words what a
      visual badge means ("Hint, 3 left"; a play mark = "a short video earns this").
- [ ] **Every choice speaks the word it shows first** ("Motion: Auto"); the explanation goes in the
      hint.
- [ ] **Decoration is excluded:** decorative painters, the mascot when it carries nothing, glyphs set
      inline in text.
- [ ] **Content behind an overlay is hidden from the screen reader.** A dim stops fingers, not screen
      readers; test it on the live semantics tree.
- [ ] **Animated or withheld values are not withheld from screen readers:** under a screen reader
      (or reduce motion), a balance settles at once. "A balance quietly wrong is worse than
      undramatic."

(Flutter node merging, sort keys and exclusion: `references/stack-flutter.md` §Accessibility audit
that hit-tests.)

## 10. Touch targets, measured

1. **≥ 44 pt of real touch everywhere;** round icon buttons 48 pt visible. Dense working grids may go
   to ≥ 40 pt only with a nearest-item hit test (within 0.6 × cell, ≥ 48 pt effective).
2. **Measure the touch, not the semantics rectangle:** a point 1 pt inside the central 44 pt of each
   tappable node must reach that node's own handler. A semantics wrapper larger than its gesture
   detector passed a size rule; so did a control excluded from semantics.
3. **Walk the render tree for tap handlers without a semantics node.** The audit found the mascot
   announced as a button with no touch at all, and a full-screen outside-tap handler with no node.
4. **Walk targets over every viewport and text size.** A layout shrink took purchase buttons to 36 pt.
5. **Keep an explicit semantic tap path** when direct manipulation commits on pointer-down.
6. **Prices stay ≥ 11 pt even in compact mode.**

## 11. Live regions

1. **Every action whose result is only visual is announced.** A screen-reader user spent a hint and
   heard nothing change but the button's count.
2. **Use a polite live region keyed per occurrence** (a serial number), so each announcement is new
   even when its words repeat.
3. **Never start an announcement with a word a control owns.** Voice control's "Hint" must find one
   control, not a sentence.
4. **Order the words by what the user needs next.** Example (shipped puzzle game): "Trail found,
   cut back 2 steps: 3 steps to target 4. First, row 2, column 3."
5. **Completion is a live heading** placed so it is read before the time and the buttons
   ("Solved, <place>, <number>").
6. **Status lines that update while a sheet is open are live regions.**

## 12. The core loop by screen reader

The core loop must be usable with a screen reader alone, without the gesture (time-critical play:
the last subsection). In the word game the whole play surface exposed zero semantics while every
piece of chrome was labelled.

- **Expose every item of the working surface with full context:** its position, its value, its
  role in the rule, its neighbours or obstacles, and its state. Example (shipped puzzle game): "Row
  1, column 2, number 2, next", "walls above and left", "path end".
- **Items are buttons while the task is live.** An accessibility tap performs the core action on
  that item (in the example: extends, cuts back or starts the path); the action hint ("Extends the
  path") appears only where the action is legal.
- **Each accessibility tap is its own contact**, so a refused item reacts every time.
- **The semantics layer paints nothing** and rebuilds only when the state changes.
- **A drawn hero is one node that reads its state in words**, with a full path beside it. Example
  (expense-splitting app, a trial run): the balance diagram's label reads each member's balance
  ("<name> gets back 86 euros 40"), and the expense list below is the complete screen-reader path.
- **Test it:** complete a whole item (a game) or the core flow, such as add, edit, complete and undo
  (an app), using semantic actions only, in CI.

### Real-time play (Proposed)

No shipped project of this method had time-critical play; this translation comes from a trial run
of a real-time arcade game, to be proved in the project. When the core loop is time-critical (dodge,
aim, rhythm), a screen reader cannot carry play: there is no discrete item to expose and no time to
hear it. Faking a semantics layer for it is the wrong answer. Instead:

1. **Every non-play surface meets the full rule above:** onboarding, menus, store, settings and
   results; the semantic-actions test runs over those flows. Play itself is one labelled region
   whose result is announced when the run ends.
2. **Play gets an accessibility route, decided in DESIGN.md with a reason:**
   - assists that change the task (slower speed, a larger hitbox), each a separate labelled option,
     with the score marked as assisted; never folded into the Motion switch (section 16);
   - audio and haptic cues for hazards, so play does not rest on sight alone;
   - a one-touch control scheme.
   Test each assist like any rule: its effect on the task, and the assisted mark wherever the
   score appears.
3. **The store's accessibility declarations say exactly what is supported** (dated block in section
   18). A screen-reader claim needs every common task, play included, to be completable with it.

Loop, input and difficulty for real-time games: `references/domain-games.md` §Real-time and action
games.

## 13. Text scaling by tier

Classify every piece of text and give its tier a cap:

| Tier | Follows system size up to | Behaviour when it grows |
|---|---|---|
| Reading text (paragraphs, captions, list names) | 2× | wraps; layouts restack; names wrap to two lines rather than an ellipsis |
| Headings and titles | 1.5× | at 2× a title took three 52 pt lines and pushed the panel off |
| Prices | 1.3× | the pill grows to fit |
| Button labels | 1.2× | past the cap, scale down to fit inside the control rather than clip |
| Chips | 1.15× | |
| Pictures of numbers (badges, board digits) | 1× | keep their size; speak their words |

- Images inside a sheet shrink as text grows (132 → 96 pt) so the words keep their room.
- A screen that exists to be read gets no cap: "a Stats screen exists to be read … it is a scroll
  view".
- A compact mode triggered by large text must not hand those users the smallest text.
- Captions wrap under their counts instead of shrinking.

## 14. Layout switches by measured fit, and masking traps

Decide compact vs stacked by measuring whether the actual words fit as drawn, at the actual scale,
never by a text-scale threshold or a fixed panel width.

- A scale threshold broke "Haptics" into "Haptic / s" at 1.3× on a 360 pt phone; a fixed 316 pt
  panel width wasted a row that measuring would have saved.
- Measure the title plus its trailing control against the row; measure the widest word against the
  room left beside an icon disc and drop the disc when it does not fit ("purchases", 172 pt, broke
  mid-word in 134 pt at 2×).
- Restack rather than shrink: stat tiles stand one per row once a half-width tile can no longer hold
  its longest caption (at 2× on a 360 pt phone a half tile had ~130 pt).
- **Pin actions outside the scroll.** A card's buttons stay at its foot; the words scroll. At 2×,
  purchase rows and Done fell "below a hard cut with no sign of more". Assert the buttons are whole
  on the card: "nothing clipped" alone passed with a button scrolled away. Stop the card short of
  the top (72 pt) so Back stays visible.
- **Edge fades:** fade only at an edge the content continues past, over 44 pt, with a 12 pt fully
  clear band at the very edge. Under a plain ramp, letter tops cut by the edge stayed at 1–23% alpha
  and read as smudges. Keep the same component structure whether or not it scrolls, so scroll
  state survives.
- **A glyph beside wrapping text rides inline** in the paragraph (excluded from semantics); in its
  own column it drifted to the card's edge when the text wrapped.
- Check every reading paragraph, not one per screen, in every language: a 2× look at the shortest
  copy only missed the long-copy overflow.

**Masking traps:** checks that pass while the user sees broken text.

| Trap | Mechanism | Guard |
|---|---|---|
| A scale-to-fit wrapper above reading text (fine for a capped button label, never above a paragraph) | the text drew at 0.52 of its laid-out size at 2×, and both the overflow and the scaling suites passed | assert drawn height ÷ laid-out height = 1 ± 0.01 for every reading paragraph |
| Scale-to-fit round a number and its caption | the number shrinks when the caption grows | wrap the caption instead |
| No-wrap text with a fade on overflow | fails silently at large text; an overflow check cannot see it | minimum intrinsic width ≤ the box |
| "Tiles per row" counted by line tops | wrapping fools it | compare left edges (start edges in right-to-left) |
| A node cut by a screen or list edge | reports only its visible part to size checks | skip nodes touching a boundary |
| A scaled-down audit of one paragraph | other paragraphs overflow | audit every paragraph at 1×, ~1.3× and 2× on both reference phones |

(Flutter: the scale-to-fit wrapper is `FittedBox`; see `references/stack-flutter.md` §Text-scale
matrix.)

## 15. Flashing and photosensitivity

Flashing can trigger seizures in people with photosensitive epilepsy, so the flash limit is
structure, not personality: no identity, beat or celebration overrides it. No shipped product of
this method came near the limit (their calm feel briefs had no full-screen flash). A trial run of a
dark neon arcade game is where hit flashes, strobing hazards and beat-synced pulses piled up, and it
had to invent this rule; the guard is Proposed until a project proves it.

1. **Nothing flashes more than 3 times in any 1-second window** unless it stays below the general
   and red flash thresholds (dated block). A flash is a pair of opposing changes: one pulse up and
   back is one flash, and a hazard strobing at 5 Hz is five. A change whose darker state is at or
   above 0.8 relative luminance does not count; changes against a dark base, the usual neon case, do.
2. **Judge the area on a phone, not a monitor.** The threshold is a share of the visual field and a
   phone is held close: at 30 cm the area limit is about 5.4 cm², roughly 6% of a 6.1-inch screen,
   and about 2.4 cm² at 20 cm (computed from the dated figures). Treat any region over about 5% of
   the screen as in scope, less for an audience that holds the phone closer.
3. **Cap full-screen luminance swings** (a hit flash, lightning, a background pulsing on the beat)
   below 0.1 relative luminance (10% of white), so they are not flashes at all. Let a hit read
   through hit-stop, shake or a shine on what was hit. A larger swing is a recorded decision and
   still counts toward rule 1.
4. **Red flashes count at any luminance:** a change to and from a saturated red is a red flash even
   when brightness barely moves, so a red pulse or strobe is held to rule 1.
5. **Motion Off removes every flash** (section 16). A warning screen at launch never replaces the
   limit.
6. **Guard it by frame analysis of the busiest moment** (the biggest combo, the finale, the fastest
   stage):
   - record losslessly at the device frame rate with Motion On, on the smallest and largest phones;
   - per frame, linearise as in the contrast method (`references/visual-design.md` §5.2) and average
     relative luminance over windows of the threshold area, sliding by a quarter window (a flash
     straddling two fixed windows is diluted in both and missed); track saturated-red transitions
     per window too;
   - count opposing changes of ≥ 0.1 whose darker side is below 0.8, per window, in a sliding 1 s
     span; fail above 3, naming the time and the window;
   - controls: a threshold-sized white square strobing at 4 Hz on black must fail, and the same at
     3 Hz must pass; with Motion Off, the same moment counts zero flashes.
   What it does not prove: certification by a dedicated flash analyser (as broadcasters use), or
   content the recording missed.

## 16. Reduce motion

Follow the platform setting plus an in-app **Motion** setting: Auto (follows the platform's reduce
motion) / On / Off, the same vocabulary as every "follow the system" setting. Motion Off removes
presentation motion: transitions, shake, hit-stop, flashes, parallax, camera moves, ambient life,
celebratory shows. None of it is scheduled, not even "faster". Motion that is the task (a real-time
simulation, a video, a live map) continues. Outcomes are identical for the same input, proved by a
test; pressed states still show; the setting is re-read at the moment of each action. Assists that
change the task (slower speed) are separate, labelled options, never the Motion switch (section 12).
The canonical rule and its details: `references/motion-and-feel.md` §Reduce motion.

## 17. Colour assist

No state is carried by hue alone, guarded in greyscale (`references/visual-design.md` §5.5). On top of
that, an optional colour-assist setting:

- adds patterns in a fixed order where any four in a row differ (e.g. stripes, dots, chevrons that
  point the way, waves), so neighbours always differ;
- anchors each mark to a position, not to path length, so new input never moves existing marks;
- draws each mark as a light face over a dark under-edge, so it reads in greyscale on every colour
  ("a white-only mark fell to 1.8:1 on amber in greyscale, a dark-only one to 1.6:1 on plum");
- strengthens rims (≥ 4.9:1 on every palette);
- leaves the settled, shared output byte-identical with assist on or off, so share images need no
  special case.

Where colours name things (a sorting game's items), give each colour a second channel (distinct
silhouette marks) and a distinct spoken name, tested for collisions in every shipped language.

## 18. The audit

Automated, per screen, in CI, in every supported direction:
- [ ] Every tap handler on screen has a semantics node over it (render-tree walk).
- [ ] A hit test 1 pt inside the central 44 pt of each node reaches its own handler.
- [ ] One heading per screen; the reading order matches DESIGN.md.
- [ ] Each transient event produces a live-region announcement that starts with no control's name.
- [ ] The core loop, or for real-time play every non-play flow, completes using semantic actions
      only (section 12).
- [ ] Every reading paragraph across the look matrix's phone and text axes
      (`references/visual-design.md` §13.1): no truncation, clipping or overflow; drawn ÷ laid-out
      height = 1 ± 0.01; pinned buttons whole.
- [ ] Greyscale guard over compared states; contrast floors in every lighting the product ships.
- [ ] Motion Off: no presentation motion scheduled, motion that is the task continues, outcomes
      identical for the same input.
- [ ] Flashing: the frame analysis of the busiest moment passes and its controls fail as expected;
      the Motion Off recording counts zero flashes (section 15).

By a human, before each owner gate: use the core loop (for real-time play, every non-play flow, and
play through its accessibility route) with the platform screen reader on each platform, with large
text on, in every lighting the product ships, and in each script direction.

> **Dated facts (as of 2026-10 — re-verify before relying):**
> - Apple's guidance is 44×44 pt touch targets; Android's is 48×48 dp. WCAG 2.2: 2.5.8 target size
>   minimum 24×24 CSS px (AA); 2.5.3 the accessible name contains the visible label. Android 16
>   deprecates the old one-shot announcement call (`announceForAccessibility`) and was observed to
>   ignore it; live regions worked on both platforms.
> - WCAG 2.2 2.3.1 (Level A): nothing flashes more than three times in any one-second period, unless
>   the flashing is below the general flash and red flash thresholds. A general flash is a pair of
>   opposing changes in relative luminance of 10% or more of the maximum (1.0) where the darker
>   state is below 0.80. A red flash is a pair of opposing transitions involving a saturated red
>   (one state with R/(R+G+B) ≥ 0.8, and a difference above 0.2 in the CIE 1976 UCS chromaticity
>   diagram). Flashing is below the thresholds if no more than three of either kind occur in any
>   second, or if the combined area of concurrent flashes is at most 0.006 steradians (25% of any
>   10° visual field; 341 × 256 px at 1024 × 768 on a monitor). 2.3.2 (AAA): no more than three
>   flashes in any second, at any size. W3C notes that a viewer closer than the assumed distance is
>   affected by smaller areas.
> - Apple's App Store shows per-device accessibility labels (Accessibility Nutrition Labels) on its
>   26 OS releases: VoiceOver, Voice Control, Larger Text, Dark Interface, Differentiate Without
>   Color Alone, Sufficient Contrast, Reduced Motion, Captions, Audio Descriptions. A feature may be
>   marked supported only if every common task can be completed with it: the primary function, plus
>   first launch, login, purchase and settings. Voluntary at first; Apple says it will become
>   required for submissions, with no date given. Check whether the other stores you ship to ask
>   for anything similar.

---

## Part C: Localisation, RTL and calendars

## 19. Localisation, RTL and calendars

Where this comes from: a word game shipped in Persian, a sorting game shipped in three languages
including right-to-left ones, and a habit-tracker kickoff in Persian and English (a trial run of this
method) whose probes found the calendar and time-zone faults below. Decide the launch languages at
kickoff. A right-to-left language planned for launch is built and rendered from the first slice:
retrofitting right-to-left breaks layouts, and an owner who speaks the language judges that build
first.

### 19.1 One locale policy, from the UI language

1. **One pure function maps the UI language** to direction, digits, calendar, first weekday, number
   and date formats, and plural rules. Never derive these from the device region: an English UI on a
   phone set to an Iranian region would otherwise mix Saturday-first weeks with Latin digits (a review
   finding in the habit-tracker trial). Guard it with a table test over every language × setting.
2. Example (habit-tracker trial): Persian → right to left, Persian digits, Solar Hijri, Saturday
   first; English → left to right, Latin digits, Gregorian, Monday first. A separate setting may
   switch the calendar (some Persian speakers prefer Gregorian); digits stay with the language.
3. **The UI language follows the phone** when the app supports it, else a default; a setting
   overrides it (Auto, then each language named in its own script).
4. **Stored data is language-neutral:** dates as ISO `YYYY-MM-DD` Gregorian, numbers as numbers,
   text as typed. Calendars and digit shapes exist only at display.

### 19.2 Mirroring: what flips and what never does

- **Flips with reading direction:** the order of items in a row, start and end alignment and
  padding, back and forward arrows, list chevrons, a sheet or page entering from the start edge,
  and progress through a sequence (a slider, a progress bar, step dots). Example (habit-tracker
  trial): a week row reads right to left, so the month record's day order follows it.
- **Never flips:** the digits inside a number (they read left to right in every script), media
  playback controls and their timeline, clocks and circular gauges, photos and logos, and a game's
  working surface (a puzzle board's geometry is not text). Example (sorting game): a test asserts
  every item's horizontal position is identical in both directions.
- **Glyphs:** mirror only directional ones, and before mirroring one, check what its mirror means in
  your own icon set. A circular arrow is a rotation, not a direction: in the sorting game, undo and
  restart were one circular glyph drawn in opposite directions, so mirroring undo (as generic
  checklists advise) would have put two identical live buttons side by side.
- **Write layout in start and end, never left and right,** so one layout serves both directions.

### 19.3 Bidi: mixed-direction strings

1. **A sign is bidi-neutral.** "+۱۵" drew as "۱۵+" in a right-to-left run. Set a signed figure in a
   left-to-right isolate and verify by glyph boxes (the sign's box lies left of the digits), not by
   squinting.
2. **Isolate every interpolated value** whose direction may differ from its sentence (names, amounts
   with currency, Latin product words, links, codes) with first-strong isolates (U+2068 … U+2069) or
   the framework's bidi formatter. Without isolation a Latin name inside a Persian sentence can carry
   the number or punctuation after it to the wrong side.
3. **A text field takes its direction from its first strong character**, or from the UI when empty,
   and aligns to match.
4. **Render mixed strings in tests**, in both UI directions, with names in the other script.

### 19.4 Digits, separators and numbers

1. **Digits follow the policy everywhere,** including pictures of numbers (badges, board digits, day
   tiles). Persian digits (U+06F0–U+06F9), Arabic-Indic digits (U+0660–U+0669) and Latin digits are
   three different sets of code points; a numeric input accepts all three and normalises before
   parsing, because users type whatever their keyboard gives.
2. **Format numbers, dates and currencies with the platform's locale formatter** (CLDR data); never
   build separators by hand.
3. **A middle dot cannot separate numbers where zero is a dot** (Persian ۰, Arabic ٠). In the word
   game a map label "… · ۱" read as "۱۰"; in the habit-tracker trial the chosen font also drew U+00B7
   as a box, and the first look caught it. Use the language's comma (Persian "،") or a line break. A
   comma between two digit runs can read as a decimal separator: use a dash.
4. **Prices come from the store already localised** (section 7). Price test fakes use strings nobody
   would type ("5,49 €"), so a hard-coded price cannot pass.

### 19.5 Whole sentences and plurals

1. **Compose whole sentences per language;** never join fragments (`'$a, $b and $c'`). Word order,
   agreement and dual forms differ, so a translator writes each sentence whole.
2. **Use the platform's plural or message format** with every category each language has. Arabic
   has six (zero, one, two, few, many, other); English has two; a Persian noun stays singular after
   a number.
3. **Test every counted message at 0, 1, 2, 3, 11 and 100** in every language: those six values reach
   all six Arabic categories.

### 19.6 Fonts and shaping per script

1. **Bundle a family that covers every shipped script and digit set,** with a verified licence per
   family (`references/visual-design.md` §7). One family designed for both scripts keeps weights
   matched; otherwise pair faces at matched size and weight, judged side by side.
2. **A coverage test:** every code point used in the string tables, the store copy and generated
   content exists in the bundled fonts' character maps. A tofu test renders two glyphs per script
   and asserts their pixels differ.
3. **Arabic-script text needs shaping:** letters change form by position and join. Draw text through
   the platform's text layout engine; a painter, canvas or engine path that places glyphs one by one
   draws isolated, unjoined letters.
4. **Persian spelling uses the zero-width non-joiner** (U+200C, as in "می‌شود"): never strip it in
   normalisation, search keys or truncation, and never cut text inside a grapheme cluster.
5. **Letter-spacing is 0 for joined scripts,** and optical placement differs per script ("uses
   descender space"): `references/visual-design.md` §7.
6. **Arabic-script faces often need more line height** than Latin ones; line heights tuned on Latin
   clip or crowd them. Check every reading paragraph in each script at 2× (section 18).

### 19.7 Calendars, days and time zones

1. **A calendar conversion is a core algorithm:** prove it over every day against an independent
   implementation, plus a continuity check (consecutive Gregorian days map to consecutive local
   days). Example (habit-tracker trial): its own Solar Hijri conversion matched a reference library
   on all 182,621 days from 1800 to 2299, but only after the all-days probe found that the first
   version had 98 continuity breaks, each at Gregorian 1 January: dates before the Persian new year
   used the previous year's leap flag. Every known-date check had passed. Known dates are a sanity
   check; the all-days parity is the proof. Keep the reference library as a test-only oracle.
2. **Compute a day index from the local calendar date** (UTC midnight of the local year, month and
   day, counted in days from an epoch), never as hours since a local epoch divided by 24. Example
   (same trial; a probe that walks every hour of a year and checks the index steps by exactly 1 at
   local midnight): the naive form was wrong 476 times in New York and 420 in London, and 0 times
   in Tehran, Kabul and Lord Howe. A suite run only in the owner's zone would never have seen it.
3. **Run day-boundary tests in child processes under several `TZ` values:** a zone with daylight
   saving whose epoch falls in its lower-offset season (New York, London), one without it (Tehran),
   one with a 30-minute shift (Lord Howe) and one with a non-hour offset (Kabul, +4:30).
4. **Decide and record what a day means:** store each event's local date and its UTC offset at that
   moment; derive kept, missed and streak counts from events, never store them; a day becomes
   "missed" only after its local date has ended in the phone's current zone; travel and a clock set
   back never move an event's date (`references/architecture.md` §Clocks).
5. **Daylight-saving days have 23 or 25 hours,** and some local times do not exist (02:30 on a
   spring-forward night where clocks jump at 02:00). Test schedules and reminders over those days.
6. **The week starts where the policy says** (Saturday in Persian, Monday in much of Europe, Sunday
   in the US); weekly views, "this week" stats and week-based streaks all read it.

### 19.8 Layout in every direction

1. **The look matrix has a locale and direction axis** (`references/visual-design.md` §13.1): every
   screen in each direction, at 2× text, with each language's longest copy, not the English.
2. **A rendered-tree test** pumps every screen in the right-to-left language and fails on any visible
   Latin letter or Latin digit outside user text. Example (sorting game): a localisation pass that
   replaced literal text widgets shipped with 509 green tests and still missed 95 strings built in
   getters, switch expressions and helpers; the rendered-tree test found them and covers future
   screens for free.
3. **Before translations exist, a pseudo-locale build** (every string lengthened and wrapped in
   markers) shows hard-coded strings and clipped layouts. A standard technique; the source projects
   used the rendered-tree test instead.
4. **Assert mirroring where it matters:** the working surface's positions equal in both directions;
   chrome's start and end swap.

### 19.9 Translation workflow

1. **String tables of whole sentences, keyed by meaning,** each with a context note: where it shows,
   its room at 1× and 2×, and what each placeholder holds.
2. **No machine-only copy in the product or the store listing.** A fluent reader reviews every string
   in place, on the rendered screens, not in a spreadsheet. If the owner speaks a launch language,
   the owner judges that build. The habit-tracker trial wrote it into its bar: a build that "reads
   as translated" fails, as programmer art does.
3. **Banned-word and claim tests run over every language's strings** (section 2, rule 14).
4. **Store listings are localised per language,** with screenshots captured from the localised build
   (`references/release-and-store.md` §Screenshots).
5. **Language names in the switcher are written in their own script.**

**Checklist:**
- [ ] Locale policy table test over every language × setting.
- [ ] Calendar parity over every day against an independent implementation, plus continuity.
- [ ] Day-index tests under at least four `TZ` values, as in 19.7.
- [ ] Right-to-left rendered-tree test: no visible Latin outside user text; the working surface
      unmirrored.
- [ ] Counted messages at 0, 1, 2, 3, 11 and 100 in every language.
- [ ] Font coverage over every string; a tofu test per script.
- [ ] Look matrix renders in each direction at 2× with the longest copy, with three looks.
- [ ] Every string reviewed in place by a fluent reader; store listing per language.

> **Dated facts (as of 2026-10 — re-verify before relying):** Apple's Human Interface Guidelines
> ("Right to left") and Material Design ("Bidirectionality") list what to flip (progress indicators
> and sliders among them) and what to keep (media playback controls and the digits of a number among
> them); re-read both before a right-to-left slice. Iran has observed no daylight saving since 2022
> (time zone database), so Tehran tests exercise no transition. CLDR gives Arabic six plural
> categories and English two.
