# DESIGN — {{PROJECT_NAME}}: art direction, UI, motion, sound

**Read this before any visual, UI, animation or sound work.** It is the creative contract: PLAN says
*when*, ARCHITECTURE says *where*, DECISIONS says *why*, and this says *what it must be like*.
Values marked *Proposed* are starting points to tune on a phone. Record each change here with the
reason.

<!-- flagship-method template. The identity in this doc is THIS project's own, derived at kickoff
from its audience, its category and its competitors' gaps (flagship-method references/kickoff.md
§Identity). Nothing from the skill's examples is a default style or motif. Content:
references/visual-design.md and references/motion-and-feel.md. Conventions:
references/project-kit.md §8. Each fact has one home: the sections below point to the identity brief
instead of restating it. A slot only a later phase can fill (a device-tuned number, an as-built
note) gets one line instead of a guess: "Written in Phase <n.m>; decided so far: <…>"
(references/project-kit.md §12). -->

## Identity brief (from kickoff)

<!-- Copied from the kickoff's identity brief (flagship-method references/kickoff.md §7.4 defines
every field) and kept current. Every line is testable or names a decision; the art-direction rules
themselves live in §2.1. -->

**Name and statement:** "[TODO: two or three words]". [TODO: one paragraph: the audience, their
context, and the combination sentence.]

**Leak check:** [TODO: each motif borrowed from a competitor or an example → the reason this
project's own inputs derive it, or "dropped".]

**Lightings:** [TODO: one (dark-only or light-only; the system appearance is ignored and the look
matrix drops the lighting axis) or two (following the system), with the reason (DECISIONS #n).]

**Hero:** [TODO: what it is; proportions in units of its own height; the silhouette test at its
smallest real size; its job (shows live state, reacts to input, or another job the identity
derives).]

**Feel brief:** [TODO: the motion personality in three words; what is frequent, what is rare, and
what the one impact is (or none); what success and "no" feel like; what it must never feel like;
the signature moment; the personality slots, each decided with a reason and each may be "none":
overshoot, refusal shape, bounce, ambient amount, shake budget, refusal haptic weight; starting
values to tune on a device: press, settle, the ambient ceiling.] Tap to skip within 300 ms is
universal, not a slot.
<!-- kind:game -->

**Feel brief, controlled-avatar slots** (Proposed): [TODO: if the player steers an avatar in real
time, the input-latency budget (measured on a device), avatar smoothing (default none), the hitbox
as a ratio of the art, time-to-retry as a numbered promise, and hit-stop (or none); otherwise "no
controlled avatar" (flagship-method references/domain-games.md, "Real-time and action games").]
<!-- /kind:game -->

**Sound brief:** [TODO: the sound world, drawn from the product's world; the kind of sound system:
tonal, textural/foley or minimal (silence by default is also a decision); what success, refusal and
the one impact sound like; the loudness ladder; synthesised, recorded or licensed; the phone speaker
as the reference listener; whether it mixes with the user's audio and obeys the silent switch; music
on or off by default.]

**Voice:** [TODO: the word budget, the tone, and this project's banned words, each with its reason;
the one file of approved exceptions that the copy guard reads.]

**What we will not be:**
- [TODO: "never X, because Y": 5–10 lines.]

**The edge:** [TODO: the 2–4 things that set it apart.]

**Rejected directions, and why:** [TODO: the candidates that lost, with the look that decided it.]

**Plan B:** [TODO: the trigger ("the <checkpoint> fails after three looks on any of a, b, c") → one
money question to the owner (DECISIONS #n).]

**Reference renders** in `docs/{{SLUG}}/reference/`: [TODO: file — what it shows.]

## Quality bar (read before any visual work)

How it looks and feels is what {{OWNER}} judges. [TODO: the owner's own words about the bar, and
what was rejected before, if anything.] So:

1. **Answer the quality bar on every screen, in writing.** Canonical text, the reasons and each
   question's game and app reading: flagship-method references/visual-design.md §The quality bar.
   Each "Here:" is this project's reading, set by the identity brief:
   1. **Alive at rest?** In the measure the identity sets; stillness may be a decision, never a
      default. Here: [TODO: what is alive at rest, or why stillness is the decision.]
   2. **Does touch have weight?** An immediate response with physical character suited to the
      identity; never a one-frame snap. Here: [TODO: the press and release character.]
   3. **Do results arrive?** Earned or completed things travel to where they are kept; the
      destination changes only when they land. Here: [TODO: what travels, from where to where.]
   4. **Is every surface from the one material system?** Second-ring surfaces included: toasts,
      toggles, errors, loading. In a flat style the "material" is the surface system: fills, rules,
      elevation, type. Here: [TODO: the surface system, in one line.]
   5. **Does each screen arrive?** One overlapping movement, never pop, never queue; a
      reduced-motion variant exists. Here: [TODO: how screens arrive.]
   6. **Does it read at its emptiest?** Zero, one and full. Here: [TODO: the emptiest state of each
      core screen.]
   7. **Does the thing arrive before its container?** Checked on a filmstrip. Here: [TODO: the
      sequences to filmstrip.]
   - **E1, change while moving:** input during an animation hurries it home; never queue, never
     teleport. Here: [TODO: the animations input can interrupt.]
   - **E2, the stuck user** sees the way out. Here: [TODO: where a user can get stuck, and the way
     out.]
<!-- kind:game -->
   - **Game extras** (flagship-method references/domain-games.md §1), answered per slice:
     **G1,** does a run of successes build? **G2,** does the hero react to every event and never
     contradict it? **G3,** is the settled payoff frame worth staring at? Here: [TODO: this
     project's reading of each.]
<!-- /kind:game -->
<!-- kind:app -->
   - **App extras** (Proposed; flagship-method references/domain-apps.md §2, with the app checks
     for each question): **A1,** does every total open into its parts? **A2,** does any pixel shame
     a miss? **A3,** does it survive interruption? **A4,** does every status word match the code?
     Here: [TODO: the ones that apply, in this project's words.]
<!-- /kind:app -->
   - **This project's own questions,** added as the owner, reviews or play-tests find them:
     [TODO: the first ones, or "none yet".]
2. **Look at what you made.** Render every renderer and screen to PNG across the look matrix
   (flagship-method references/visual-design.md §13.1), and check the important ones on a
   simulator. **Budget three looks per visual change.** Write down what each look found.
3. **Compare against the winners, screen by screen** (§1). Name the one element they polished that
   we left plain.
4. **Only final-quality work reaches {{OWNER}}.** Never a programmer-art build, not even "to check
   direction".

How to read the labels below:
- **Verified:** checked on the web (URL and date), in the installed SDK source (version), or by a
  render.
- **Proposed:** a design choice with its reasons; the numbers are starting values to tune on a phone.
- **Unverified:** not yet confirmed, and marked where it appears.

---

## 0. Decisions at a glance

<!-- Answers a new session's first questions without reading the whole doc. Include the rejections
("not X, not Y") so they are not relitigated. -->

| Question | Decision |
|---|---|
| Name, hero, lightings, feel, sound, voice | The Identity brief above (not restated here) |
| UI languages and direction | PLAN "Goal" (not restated here); what mirrors per language: §2.7 |
| Primary visual | [TODO: the thing the user acts on, and what was rejected] |
| Drawing and animation technology | [TODO: and what was rejected, with the reason (§3)] |
| Backgrounds | [TODO: what sits behind the working surface, or "none", as a decision] |
| Art provenance | [TODO: hand-built / licensed / commissioned; the AI-art rule, as decided with {{OWNER}}] |
| State and per-frame values | [TODO: per-frame values never go through the state store] |

## 1. What the winners do

<!-- 3–5 category winners plus the plain baseline clones. Per competitor: name, ratings count and
stars, rank, release date, date viewed; palette; shapes and depth; character; UI chrome; motion (if
known); then a one-paragraph **Lesson**. Correct the brief where the evidence disagrees, and state
confounds. List what you could not verify in §8. -->

**What they all share:** [TODO: the traits every winner has.]

**Our combination:** the combination sentence in the Identity brief's statement (one home; not
restated here).

## 2. Art direction (the style named in the Identity brief)

### 2.1 Principles (rules a reviewer can pass or fail from a render)
1. [TODO: light and depth, with numbers, if the style uses light.]
2. [TODO: the surface system: one recipe every surface is drawn from.]
3. [TODO: edges and outlines; shape (e.g. radius as a % of the unit); palette structure;
   readability floors: 5–8 rules in all, each with a number or a yes/no.]

### 2.2 Global tokens

<!-- If a test parses this table, say so here: "Parsed by <test>: contrast figures within ±0.01." -->

| Token | Hex | Use | Contrast check (ratio, against which surface or stop) |
|---|---|---|---|
| [TODO: name] | [TODO: #rrggbb] | [TODO: use] | [TODO: ratio vs surface] |

### 2.3 Theme palettes (every theme fills the same structure, in every lighting the product ships)

| Theme | [TODO: the structure's columns, e.g. background, surface top / low / edge, accent, ambient motion] | Lowest measured contrast |
|---|---|---|
| [TODO: theme] | [TODO: values] | [TODO: ratio] |

### 2.3a The second lighting, if any
[TODO: the second lighting as a re-lighting of the same structure, whichever lighting is primary,
never an inversion; or "none: single lighting (DECISIONS #n)".]

### 2.4 Typography
[TODO: the type pair, sizes, weights; a font for every script the UI uses, with its licence;
reading text follows the system text size to 2×.]

### 2.5 The hero element
[TODO: proportions, poses or states, and an honest judgement against the benchmark, with plan B and
its cost.]

### 2.6 Secondary elements and interface pieces
[TODO: the one surface system applied to every surface, the second ring included: toasts, errors,
toggles, loading.]

### 2.7 Accessibility and languages, as built
[TODO: contrast floors per theme and lighting (reading text and functional strokes); no hue-only
signal; ≥ 44 pt real touch; reading order; live regions; flash safety (nothing flashes more than three times in
any one second above the general and red flash thresholds; ux §15); for each UI language and direction, what mirrors and what never does
(flagship-method references/ux-and-accessibility.md). If the core loop is time-critical: every
other surface works by screen reader alone, and play gets its own route: assists that mark the
score, audio and haptic hazard cues, one-touch control (references/ux-and-accessibility.md §12).]

## 3. Technology verdicts

<!-- One row per candidate drawing, animation, sound or rendering technology. Prefer what the builder
can create, diff and test as text (code-drawn shapes over files made in a visual editor; synthesised
sound over sample libraries whose licence is unclear): flagship-method references/kickoff.md §5.4.
Put prices and plan terms in a dated block. Then the recommended stack. -->

| Technology | Verdict | Verified (version, licence, renders under the test runner) | The catch | Allowed uses | Plan B |
|---|---|---|---|---|---|
| [TODO: candidate] | [TODO: use / reject / plan B only] | [TODO: how it was verified] | [TODO: the catch] | [TODO: uses] | [TODO: fallback] |

## 4. Motion spec

<!-- Keep "Plan" and "As built" side by side for every table. Numbers are *Proposed* until tuned on a
device; label each "set from renders" or "set on a device", and record old → new and why. A value
only a device can set reads "Written in Phase <n.m>; decided so far: <…>" until then.
Event table: | Event | Visual | Timing (ms) | Sound | Haptic |, one row per interaction, refusals
included. Timeline for anything with more than one beat: | Time (ms) | What happens |.
For every sequence: its Motion Off path and the skip (the next action live within 300 ms). Motion
Off removes presentation motion (transitions, shake, hit-stop, flashes, parallax, camera moves,
ambient life, celebratory shows); motion that IS the task (a real-time simulation, a video, a live
map) continues; outcomes are identical for the same input. Assists that change the task are
separate, labelled options, never the Motion switch (flagship-method references/motion-and-feel.md
§10). -->

**Personality slots** (flagship-method references/motion-and-feel.md §1): overshoot, refusal shape,
bounce, ambient amount, shake budget and refusal haptic weight take the values the feel brief
decided, each a named constant in 4.1; the kind of sound system is in §5. **Structure holds for
every identity:** effects after causes, content before container, no double exposure, never block
input, Motion Off removes presentation motion and changes no outcome, every flash within the flash-safety rule
(ux §15), departures never more energetic than arrivals.

### 4.1 House physics (one constants file)

| Name | Value | Set from (renders / device) | History (old → new, why, device) |
|---|---|---|---|
| [TODO: e.g. press] | [TODO: value with unit] | [TODO: renders / device] | [TODO: or "first value"] |

## 5. Sound and haptics

<!-- Sound list: | id | when | character | level (quiet / medium / loud) | min gap |. If a test parses
it, say how ("rows starting with a backticked id are cue rows; a later row wins"), and make sure no
other table here starts its rows that way.
Measured cue table, through a phone-speaker model:
| cue | built as | length | loudest 50 ms: full / 250 Hz / 350 Hz (dBFS) |.
One beat map per choreographed show: | ms | the show | the sound |.
A silent product writes "none: silent by default (DECISIONS #n)" and keeps the haptics table. -->

### 5.1 Haptics

| Moment | Haptic | Limit |
|---|---|---|
| [TODO: e.g. frequent step] | [TODO: e.g. selection tick] | [TODO: e.g. ≤ 1 per 35 ms] |

## 6. Screens and layout

Reference phone sizes: [TODO: e.g. a small and a standard phone]. Fit rule: [TODO: computed fit,
measured text, no threshold-based switches].

<!-- One entry per screen or effect:

N. **<Screen name>** (<phase/slice>; DECISIONS #..).
   **Plan (written before building):** layout; the exact words for every state; what is NOT on it;
   motion and sound cues; semantics; text-size behaviour; acceptance renders by file name.
   **As built (three looks; <render folder>).** Look 1: <what was wrong>. Look 2: <what changed>.
   Look 3: <accepted / what changed>. Guarded in <test> (<what it asserts>).
   **Fixer pass (<date>):** <finding>; <fix>; <negative control>.

Hard details get numbered versions with what each read as (v1 … vN, the shipped one marked). -->

## 7. What the probe proved, found and did not prove

- **Proved** (by running): [TODO: what ran, with numbers.]
- **Found by looking at the renders** (would have shipped otherwise): [TODO: the faults the looks
  found.]
- **Not proved** (needs a device or a human): [TODO: each becomes an acceptance item in PLAN.]

## 8. Unverified, and open questions

- [TODO: each claim no tool here confirmed, and what would confirm it.]

## Sources

<!-- URL, date queried, SDK version read. -->
