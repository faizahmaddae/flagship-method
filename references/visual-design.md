# Visual design

How to turn a project's identity into a look that is coherent, measurable and premium: art direction
written as checkable rules, one surface system (and one light, if the style uses light), tokens,
contrast by numbers, layout measured on real content, one lighting or a second as a re-lighting, an
engineered hero, the look loop that catches what tests cannot, and the quality bar every screen passes.

**Read when:** before any visual, UI, icon, store-art or theme work; when writing the art-direction
part of `docs/<slug>/DESIGN.md`; before calling any screen done.

**Contents:** 1 Identity first · 2 Art direction as checkable rules · 3 One surface system ·
4 Design tokens · 5 Colour and contrast · 6 Chrome semantics · 7 Typography · 8 Layout ·
9 Lightings: one, or dark mode as a re-lighting · 10 The hero element · 11 Icon, launch screen and
store art · 12 No AI-generated art · 13 The look loop (13.1 holds the look matrix) · 14 The quality
bar: seven questions and two edge checks · 15 The failure catalogue

---

## 1. Identity first

The method transfers; the look does not. Every project derives its own identity first, from its
promise, its audience and a teardown of its category (`references/kickoff.md` §Identity). Nothing
below is a default style. Where a clay material, a dog mascot, a candy-like ribbon or park palettes
appear, they are a labelled worked example of a method, chosen by one product for its own reasons.
App examples come from trial runs of this method and are labelled as such.

Identity work produces, in `docs/<slug>/DESIGN.md`, before any screen is built:

- [ ] A style name of two or three words, and 5–7 rules a reviewer can pass or fail from a render.
- [ ] One surface system (section 3): a lit material with one key light, or a flat, line or
      emissive recipe.
- [ ] A palette *structure* that every theme fills in the same way.
- [ ] A type pair, and a hero element with a job.
- [ ] A "Decisions at a glance" table (`assets/templates/DESIGN.md`) that carries the rejections so
      they are not relitigated. Choose each technology by whether the builder can author, diff and
      test it as text, and record its verdict (`references/kickoff.md` §5.4, Track D).
- [ ] A category teardown (method: `references/kickoff.md` §5.4); it sets the art budget. In the
      shipped puzzle game the charm leader's appeal came from "one character asset, a cozy palette
      and a glow on success, not detailed scenery", so first art time went to the hero and the board.

**Adapt to the owner** (`references/kickoff.md` §3): a non-technical owner gets an identity decided
from evidence and judges only how the finished thing feels; a developer-owner gets 2–3 rendered
directions with your recommendation. Never programmer art "to check direction".

**Write an honest judgement of your own art** after each art checkpoint: what reads well, what falls
short of the benchmark, how close code can get. Name plan B (an artist, a rigging tool) and its cost
before you need it; keep the art's input a plain parameter object so a new renderer touches one
file. Example (shipped puzzle game): "charming and competent soft-vector art"; it "does not reach
the 3D-rendered look of the leader's icon. Code can get close, but not all the way."

---

## 2. Art direction as checkable rules

A mood ("warm, friendly, premium") cannot be reviewed. A rule can. Write each principle so that a
reviewer looking at one render can say pass or fail. The slots every art direction fills:

| Slot | Checkable form |
|---|---|
| Light (if the style has one) | One key light, a direction in degrees; where gloss sits; where shadows fall and how far |
| Surface | One recipe function every surface calls (section 3) |
| Edges | Where edges come from (rim, thickness, outline, hairline, nothing); when an outline is allowed |
| Corners | Radius as a ratio of the object's size; which shapes are fully rounded |
| Palette structure | The named slots every theme fills (section 5) |
| Readability | Which information is always the highest-contrast thing, with floors as numbers |
| Hierarchy | What may be louder than what (section 6, rule 6) |
| Signals | How state and mistakes are shown (shape, motion, colour) and what is never used |

Example (shipped puzzle game, style "Soft Clay Diorama"; one product's answer, not a default):
(1) one key light at top-left (−45°): all gloss top-left, all shadows bottom-right, offset about
(+2, +4) pt, never mixed; (2) one material recipe for every object; (3) no black outlines: edges
come from the darker thick edge, dark lines only for facial features; (4) tile corner radius = 22%
of the cell, pills fully rounded; (5) every theme has the same palette structure, so code never
changes, only colours; (6) the numbers are always the highest-contrast thing.

Example (hypothetical dark-first audio app, "night console"; not built; same method, different
answer): (1) dark first, on a near-black from the accent's hue family, never #000; (2) no key light:
flat fills in three elevation steps, each lighter than the one below; (3) only live things glow (the
playing track, the record button, a level meter); (4) a glow fades to zero within 0.5 × its object's
size and never carries contrast: the shape holds ≥ 3:1 with the glow off; (5) tabular figures ≥ 7:1.

The puzzle game showed mistakes by motion (a stretch and snap-back, a wobble), not a red error
colour, because a red flash contradicts a calm product: a style decision with a reason. Write yours.

**Choose the primary visual by rendering alternatives.** Render 3–4 treatments of the product's main
visual element, pick by looking, and record why each loser lost. Example (shipped puzzle game): for
the drawn path, a rope "reads as a tangle" over 36–64 cells; dots do not show corners or connections
(which is why every genre peer uses a band); a glow reads sci-fi, wrong for a cozy style. The winner
was written as a numbered layer stack: width 0.50 × cell, round ends, shadow offset (0.03, 0.09) ×
cell at alpha 0.28, rim 0.07 × cell wider than the fill, gloss 0.26 × width toward the light.
Example (habit-tracker app, a trial run of this method): for the month view, a heat-map grid lost as
too close to a competitor, plain dots as generic, joined geometric tiles as busy (they read as a gift
ribbon), and a star with a centre hole because it read as a settings cog.

**Render the payoff and check it is visible.** At full width that ribbon hid half of every tile, so
the solved-state reward was invisible; the fix thins the ribbon to 0.32 of its width before the
reward shows. Whatever earned a reward must not cover it.

---

## 3. One surface system

### 3.1 One recipe, applied to every surface

The universal rule: **one surface system, every surface drawn from it, and one light direction if the
style uses light.** Encode it as one function (`surface(shape, colours, depth)`) that every drawing
routine ("painter") calls: panel, button, tile, badge, particle sprite, icon disc, character part.
Coherence comes from shared rules, not from matching colours by eye. The identity brief picks the
family; the recipe fixes different things in each:

| Family | The recipe fixes | What applies below |
|---|---|---|
| Lit material (clay, enamel, glass, paper with depth) | key light, contact shadow, thickness, face gradient, gloss | 3.2–3.4 |
| Flat system | fills, hairline weights, elevation steps, type | 3.3 (tinted dims), 3.4 |
| Line | one stroke family as fractions of size, caps and joins | 3.4; section 6 rule 7 |
| Emissive or dark-first | the dark base, what may glow, glow falloff, a bloom budget | 3.4 (glows), 3.5 |

For a flat style, "material" in the quality bar (section 14) means this surface system.

**Route the second ring through it too.** A word game's critique found "the primary play surfaces got
the treatment and the second-ring surfaces did not": a flat currency circle in a game of glazed
discs; error and loading screens "the last flat things left"; and three grey most-pressed buttons
beside a glazed board, which the owner said "make our whole game look like an app".

- [ ] Once the recipe exists, sweep the code for raw single-colour boxes and plain text on patterns:
      counters and currency, toggles, toasts, swatches, error and loading states, icon rings,
      settings rows, sheets, empty states.
- [ ] One drawing per object with N call sites (one coin drawing served balance, flight and price).

Example (shipped puzzle game, the lit clay recipe, bottom to top; one product's answer): (1) contact
shadow, blurred (sigma ~5 at a 44 pt object), alpha 0.25, shifted along the light by
`max(3, 0.75 × lip)`; (2) lip: the face shape shifted down 3–6 pt (8 for panels) in a darker colour,
the toy thickness; (3) face: a two-stop top-to-bottom gradient with explicit stops; (4) gloss: white
from alpha 0.45 at the top edge to 0 at 55% of the face height, clipped to the face. Example
(expense-splitting app, a trial run, flat): no drop shadows; cards are the surface colour on the
canvas with one 1 pt hairline at 25% of the secondary ink; radius 18 pt on cards, fully round on
buttons and tokens.

### 3.2 Light rules (lit styles)

- **Centralise the light** (direction, gloss depth and alpha, shadow alpha) in one place, with one
  shared shading function. In the word game nine hand copies of it had already drifted.
- **Mirrored drawings keep the light where it is on screen.** A character flipped to face left flips
  its light unless every lighting offset goes through a helper that un-mirrors it.
- **Offsets along a path point toward the light only.** A uniform-offset band on a polyline crossed
  the gloss at every corner and read as plaid.
- **Rim light lives on the lit edge, inside the silhouette.** A rim traced round the underside read
  as an outline; two inner rims (key light plus a second kick) met round every ear as a pale loop.
  Mask any second light by a ramp along its own direction.
- **A rim on a part lying over another part reads as a cut line:** clip it to outside the part below.
- **Highlights are drawn inside the face's clip.** A gloss drawn after the clip was released hung off
  narrow shapes; a test for "translucent white more than 2 px from anything opaque" catches it.
- **Long upright shapes are lit across their thickness**, not down their length.

### 3.3 Shadow colour and darkening (any style with shadows or dims)

- Tint every shadow with a near-black from the palette's own family. "A black shadow on a cream tile
  reads as dirt."
- Darken by interpolating toward a hue-matched dark, never by multiplying toward black or grey. A
  plain multiply turned cream legs grey on a green board; under a red ribbon a neutral shadow read
  grey, so that ribbon got its own warm-brown shadow. A dimmed scene gets a tinted veil, never grey.
- Derive shaded sides and variants in HSV from the base colour. Snow mixed toward grey read as steel.

### 3.4 Edges, translucency and glows

- **Outlines:** decide whether edges come from outlines at all. Where contrast forces one, keep it
  soft: at 0.85 strength it read as a black cartoon outline, at 0.6 as a soft rim.
- **Composite translucent passes once:** draw overlapping translucent layers opaque inside one layer
  bounded to the shape, then apply the alpha once, or joints double-darken. Touching parts of one
  object are one mass with one shadow and one lip ("two sausages touching read badly").
  (Flutter: `references/stack-flutter.md` §Painters.)
- **A glaze modulates; an opaque shade erases.** Texture over a gradient is translucent white or
  black at a few percent. In the word game, opaque "shades" sampled from the gradient erased it, and
  the weave still showed with strength at zero, so two builds of "tuning" controlled nothing. Only a
  before/after capture caught it.
- **Glows fade to zero on an oval inscribed in their box;** a clip turns overflow into a hard edge.
- **The cheap fallback still looks designed:** a low-quality mode bakes the expensive frame into an
  image rather than swapping in a cheaper style; a plain gradient fallback "read as programmer art"
  (`references/performance.md` §Quality tiers).

### 3.5 Emissive and dark-first styles (Proposed)

No shipped project of this method used one; these rules translate the lit-material ones, to be
proved in the identity probe. The base is a near-black from the palette's own family (3.3), never
#000. Only listed things glow: live, interactive or earned ones (a glowing decoration competes with
state, section 6 rule 6). Set a bloom budget (glowing things per screen, their share of its area) and
measure it on the render. A glow never carries contrast: with glows off, text holds ≥ 7:1 and marks
≥ 3:1. Draw each glow once per object (3.4). If a light variant ships, it re-lights the style
(section 9): a glow becomes a tinted fill or a rim, because a glow on white disappears. A bloom or
pulse budget never breaks the flash rule (`references/ux-and-accessibility.md` §Flashing and
photosensitivity): a pulse on a dark base is exactly where flashes come from.

---

## 4. Design tokens

In the word game 9 corner radii, 11 paddings and 3 border weights coexisted: "none of that is a bug
in any one widget and all of it together is why a screen made of well-drawn parts can still not look
designed". A tile's corner ratio was 0.18 on one surface and 0.16 on another, "close enough to look
like one intention, different enough to look slightly wrong".

1. **One scale per property** in one tokens file: radii, spacing, border weights, depth, icon sizes,
   type sizes. Durations and curves live in the motion table (`references/motion-and-feel.md`).
2. **Derived values come from functions, not literals:** `radius.tile(side)`, `depth.lip(size)`,
   `stroke.icon(side)`.
3. **Colour per object is a named tuple defined once:** `top / low / lip` for a lit material (face top
   stop, face low stop, thickness); `fill / pressed / edge` for a flat system.
4. **Each colour token carries its measured contrast** in its doc comment, so the decision stays
   visible and cannot silently regress: `ink = #4A3426` "Numbers, text, facial features.
   8.9–10.3:1 on every theme's darker tile stop."; `shadow = #2B1A10` "The tinted near-black every
   soft shadow uses. Never pure black."
5. **Readouts in a row share one frame shape** (height, radius, border, fill). Test the frame, not
   only the ink.
6. **Theme variation is one theme object with the same slots**; drawing code never branches on theme.

DESIGN.md keeps a token table (`| token | #hex | use | contrast vs which surface and stop |`) and a
theme table: one row per theme, same columns, including its lowest measured contrast.

---

## 5. Colour and contrast

### 5.1 Palette structure

- **Construct palettes so pairwise properties hold by construction**, then spend the remaining
  freedom on looks; never nudge hex values until a test goes green. Example (sorting game): every
  pair of item colours differs by 30° of hue *or* 1.5:1 contrast; 10 colours at 36°, not 12 at
  exactly 30° (no headroom); tints by a fixed HSV value, because accents start at different
  brightness. Example (expense-splitting app, a trial run): each member gets one of 8 hues at equal
  lightness plus an initial, and the hue never encodes who owes.
- **Both sides of a contrast pair come from the same source**, so they cannot drift per theme.
- **When a search across a whole range finds nothing, the question is wrong.** Find the distinction
  the user actually needs (e.g. "concealed differs from empty by ≥ 1.9:1").
- **Ask what a colour will sit on before reusing it.** Darker than its surroundings reads as a hole.
- **Colour along a growing sequence is indexed by the final total:** `i / (N − 1)`, with N taken from
  the geometry. Dividing by the count drawn so far recoloured the whole trail on every move.
- **Every themed area gets visual parity.** In the shipped puzzle game the first theme had no props
  or ambient life and "read as the plainest beside five that had both, on the store's first page".

### 5.2 Contrast method

1. **Measure against the darker gradient stop**, never the top or the average. Ink on a gold disc
   was 8.3:1 against its top stop and 5.81:1 against its darker stop.
2. **Compute with 8-bit colours**, as the display does (unrounded floats drifted up to ~0.016 from the
   design figures), then check the true minimum along the gradient.
3. **House bar** (this method's floors, stricter than the minimum standard on purpose):
   - text and numbers on working surfaces ≥ 7:1, in every lighting; secondary text ≥ 4.5:1;
   - functional non-text marks (a path's rim, a wall, a focus ring, a progress mark) ≥ 3:1;
   - a large label below 4.5:1 only by recorded decision. Example: white on the primary button at
     4.09:1, accepted because every primary label is ≥ 20 pt semibold.
4. **When a fill alone cannot reach the floor, add a rim that carries the contrast**, derived by a
   rule. Example: the path fills measured 1.35–5.24:1, "that is why the rim exists"; rim = fill mixed
   45% toward a dark target (55% in the theme that needed it), +7 points at night. A 38% draft gave
   one theme 2.54:1, found in review.
5. **When a pair falls short, decide explicitly and record it:** "keep the tokens, accept AA;
   measured 6.56:1 beside the digits; a render test holds ≥ 6:1 there".
6. **Tabulate every theme with its lowest measured ratio** in DESIGN.md, and **pin the floors in
   tests** per theme and lighting.

### 5.3 Measure the distinction the user makes

- **Measure "can the user tell X from Y", not "X against Z".** At night a player tells a wall from
  the empty gap between tiles. The first guard (≥ 3:1 across each wall slice) "was met by the gutter
  alone and passed with no walls". Its replacement compares each wall against the same board with no
  walls, keeps ≥ 0.85 of the day separation, and carries a control that paints no walls and fails
  (`references/verification.md`).
- **Structural parts in one colour family get a luminance floor between them** (≥ 1.5:1 was used). A
  pier derived from the tile colours "read as a hole in the wall".

### 5.4 Translucent cues

A translucent cue can fail everywhere at once: hint dots at 35% opacity measured 1.2–1.7:1 on every
theme's tiles and vanished outdoors, at thumbnail size and in a store screenshot. Compute each cue's
contrast composited over every real background (each theme and lighting, each state) before
hunting for a better scene; judge it there, never on transparency. Default to opaque with a rim ring
in a colour that already carries a palette rule (translucent member tokens in the expense-splitting
trial let the line behind cross their initials). A per-theme tint that saves one theme can sink
another: re-check every theme after any tint.

### 5.5 No hue-only signals

Every state a user compares (done/not done, next/open/collected, today/missed, on/off) differs in
shape, depth, size, mark or motion as well as hue. Guard it: render each compared state, convert to
luminance, assert the states still differ, on every theme and lighting. Example (shipped puzzle
game): open and collected targets differ by colour *and* a sticker mark; the next target is raised,
has a deeper lip, sits in a dashed ring and is 4% larger. The optional colour-assist setting is in
`references/ux-and-accessibility.md` §Colour assist.

> **Dated facts (as of 2026-10 — re-verify before relying):** WCAG 2.x: 1.4.3 text contrast 4.5:1
> (3:1 for large text), 1.4.6 enhanced 7:1, 1.4.11 non-text contrast 3:1. "Large text" is defined in
> web points (18 pt, or 14 pt bold); check how that maps to your platform's units before claiming it.

---

## 6. Chrome semantics

One visual language per meaning. If two meanings share a look, users guess.

1. **A border means pressable** (primary thick and filled, secondary thin and hollow). **A fill alone
   is a surface.** **A rule or line is a meter.**
2. **Never dress a readout as a button.** Example (sorting game): reward chips styled as buttons
   reading "Undo +2" made a chest "not feel like I received anything".
3. **One accent, one meaning.** If gold means money or reward, it is never a selection outline.
4. **One primary action per screen; at most one highlighted thing at a time.** "Too many things
   wearing the same clothes" reads as a menu of equals. On home, the primary action is the screen;
   everything else is a header button or a line, guarded by a fit test on the smallest phone.
5. **Never borrow shapes the platform owns.** Each misread in a past product: a lit vertical rail
   beside a list → scrollbar (use dots); a track with a thumb → slider (use checked milestones); a
   bright inner rounded rectangle round a word → text field (use a sunk darker band); rounded grey
   bars under a headline → loading skeleton; a gear in a game of stars → a star; a star with a centre
   hole → a settings cog (habit-tracker trial). Check an icon against what it sits next to, not
   against an icon set.
6. **The working surface may be finer than the background, never louder.** Example (word game): the
   background pattern went 0.64 → 0.34 → 0.22, an ornament 0.95 → 0.40 "so the letters lead", and a
   frame "with more incident than the puzzle it framed" became one fine rule and four corner marks.
   Fade per ink; never wrap a whole painter in opacity (it dims its lighting too).
7. **Icons are drawn, in one stroke grammar** (round caps and joins, one fill, one catch-light), in a
   unit square, coloured by the caller. Typed symbols fall back to whatever font the phone has. Set
   the stroke as a fraction of the side and compare each new icon beside its siblings. Example
   (shipped puzzle game): at the house stroke (0.115 of the side), one dense icon, a page with two
   lines of writing, read as a solid slab beside its siblings; its outline at 0.85× and its writing
   at 0.7× of the house stroke matched them.
8. **Unearned slots are holes, not dim versions:** earned and unearned differ in material (a filled
   object vs a dark socket with a lip), not only opacity. Three equal stars on a line read as a
   rating table; stand them on an arc, middle larger. Below ~8 px radius use flat fills: "a gradient
   across three pixels is a smudge".

---

## 7. Typography

- **At most two families:** a display face for titles and numbers, a body face. Bundle the files;
  never fetch fonts at runtime.
- **Ship static weight instances**, cut from the official variable font if needed: a static file
  draws its weight identically on every renderer and under the test runner. Pin upstream hashes;
  keep the licence (OFL requires it) and an attribution file, guarded by a test.
- **Font tests:** load the real fonts in any test that measures or rasterises text (a default test
  font draws boxes, so every measurement is wrong); a tofu test renders two glyphs and asserts their
  pixels differ; a weight test compares two weights (a family with only SemiBold draws w700 exactly
  like w600). (Flutter: `references/stack-flutter.md` §Fonts and icons.)
- **Size information to its container as a ratio** (board digits at 0.36 × cell), and **place ink,
  not boxes.** Centre digits by the font's digit height, not the line box; an icon's box
  centre is not its ink centre. For optical placement across scripts the variable is "uses descender
  space": two constants suffice, never one per string.
- **Measure text with the real text engine at the real scale**; layout decisions come from measured
  widths (`references/ux-and-accessibility.md` §Layout switches by measured fit).
- **Phrase atoms stay together:** no-break spaces in "1 more hint", "try again", "a day".
- **Words never stand straight on a variable scene** (sky, photo, pattern): put them on a panel or in
  a halo. "A title floating on a pattern reads as a settings screen"; text on a sky measured 1.0:1 at
  night.
- **Letter-spacing breaks joined scripts** (Arabic script and other connected scripts): route
  tracking through one function that returns 0 for them. Fonts per script, shaping, bidi, digits,
  separators and mirroring: `references/ux-and-accessibility.md` §Localisation, RTL and calendars.

---

## 8. Layout

1. **Fix two reference phones:** the smallest supported and a standard size (the shipped puzzle game
   used 360×780 and 390×844 pt, 16 pt side margins), plus the largest content; renders cover both.
2. **Size the primary element by a formula with explicit fallbacks**, and tabulate the results.
   Example: `cell = min(0.91·W / cols, (availH − pad) / rows)`, W = width − 32, availH = height after
   safe areas and every fixed chrome budget; the hero shrinks 140 → 96 pt before cells drop below
   42 pt; never wider than 480 pt. Screen and formula read the same chrome constant. Cap content size
   where it still fits the smallest phone. Example (expense-splitting trial): token spacing =
   (width − 2 × 24 pt gutter − token diameter) / (n − 1), at most 6 tokens plus a "+n" token.
3. **Shrink continuously, not at a threshold.** A hero that jumped 140 → 96 pt at a threshold sat
   44 pt apart on two boards one row apart.
4. **Distribute spare height by a stated ratio.** All of it above the controls "left ~110 pt of empty
   meadow under every board of 7 rows or fewer"; one third above the hero and two thirds above the
   controls fixed it.
5. **Actions in the thumb zone:** in-task actions at the bottom (60 pt pills), one primary. When a
   sheet's content scrolls, pin its buttons at the foot and fade the content at the edge.
6. **Avoid tangents:** a background horizon through a floating panel reads as a mistake. Pin the
   placement with a test on the target phones.
7. **Placement over variable content is measured over all content.** A completion badge (a stamp
   placed on the solved board's card) fixed in one corner hid the mascot on 10 levels and 99 daily
   puzzles. The fix lifts it just enough to clear every key cell by 0.12 × cell and takes the other
   corner when needed; its test runs over every level and daily on three phones, with eight mutations
   that each fail. Measure an occluder by painting it (a guessed reach was twice the real one), and
   claim only what the rule delivers.
8. **Reserve slots for conditional controls**, sized by measuring every variant, so nothing jumps; a
   dismissing banner never reflows content under a finger.
9. **Size by the resting box; let action poses overflow into known empty space** (usually up), not
   by full paint bounds. Decoration takes the leftover room (binary search) and drops below a minimum.
10. **Painters declare their bounds** and a test proves nothing paints outside: many canvases do not
    clip, so overflow silently covers neighbours (`references/verification.md`). Lay out in the
    visible face's frame (a face with a lip is not centred on its cell), not a box with shadow margins.
11. **Layout switches come from measured fit**, never text-scale thresholds
    (`references/ux-and-accessibility.md` §Layout switches by measured fit).
12. **The one wordy screen grows only by a compaction decision** with render acceptance ("nothing
    clips at 360×780 at 1×; at 2× the panel scrolls and never clips") and three looks.

---

## 9. Lightings: one, or dark mode as a re-lighting

How many lightings ship is an identity decision (`references/kickoff.md` §7.4): one (dark-only or
light-only) or two (follow the system), decided with a reason. If the product ships one lighting,
record it in DECISIONS, ignore the system appearance and drop the lighting axis; pin the app's
appearance at the platform level so the system parts it draws (status bar, keyboard) match. In a
neon arcade trial whose one idea was light against dark, a light variant would have deleted the
identity. What follows applies only when two lightings ship.

Then light and dark are two lightings of the same structure. Whichever is primary, the second is a
re-lighting with every floor recomputed, never an inversion: inverting breaks the material and the
information hierarchy. Example (shipped puzzle game, day-first): the brief was "a lamp-lit board in a
moonlit park".

1. **Hash the primary lighting's frames before writing any code for the second**, gate every part of
   it behind one flag, and keep the primary frames byte-identical. "24 day frames hashed before any
   night code was written still match byte for byte" made night a zero-risk addition
   (`references/verification.md` §6).
2. **For a day-first scene, keep the working surface bright and drop the surroundings.** Example:
   tiles kept ≥ 70% of day luminance, the scene dropped much further, rims strengthened by 7 points to
   hold 3:1. Re-measure every palette (night ink 7.78–8.37:1, rim 3.55–3.82:1). Chrome keeps its day
   tokens unless contrast demands a change. **For a dark-first identity (Proposed),** design dark
   first and derive light as its re-lit variant: elevation by luminance steps becomes elevation by
   shadow or hairline, glows become tinted fills or rims (3.5); re-measure every floor both ways.
3. **Anything drawn on the scene is a dark-mode bug waiting to happen.** Words go on a panel or in a
   halo. Ink sleep "z"s vanished on the night sky and a pale face vanished on snow, so scene glyphs
   became a pale face inside a thin dark outline, ≥ 3:1 on every night sky stop.
4. **Re-check empty against filled:** a cream empty slot was as light as a filled gold pip on the
   night sky; it became a dark hollow. **Re-measure functional separations** that are not text
   (section 5.3), and test every screen's text in both lightings.
5. **Characters in a lit style get a rim light inside the silhouette**, never an outline. Grade the
   foreground too (grass kept 93% luminance on dunes that fell to a third), and hide scene parts
   chrome covers.
6. **The switch is one whole-screen crossfade from a kept last frame**; motion off cuts; nested
   animated layers cut while the root fades (`references/motion-and-feel.md`). The launch screen
   gets a second-lighting variant (section 11). One setting vocabulary (Auto / On / Off for every
   "follow the system" setting); images that leave the app (share cards) use the primary lighting.

---

## 10. The hero element

One hero per screen. In a game it is often a mascot; in an app it may be the primary object (the
day, the balance, the document, the chart). Give it a job the identity derives: showing live state,
reacting to input, or another (replaying the user's route was one game's answer, not a default). The
mascot's role in play is in `references/domain-games.md`; this section engineers the hero as an asset.

1. **Specify it in proportions of its own height H** (or its own side), drawn in unit space with the
   origin at the ground point and scaled at paint time, so one drawing serves every size. Hairlines
   use `max(unitWidth, 0.8 / pixel)` so they never vanish small; bands sized in H stop growing past a
   reference size (they doubled on a 250 pt hero).
2. **Silhouette test at the smallest shipped size.** Example (shipped puzzle game): at 48 pt the
   animal and its head direction must read; ears hidden behind the head made it "read as a loaf of
   bread". Example (habit-tracker trial): the day tile at 18 pt, in greyscale, must still tell kept
   from missed from rest. Example (expense-splitting trial): in a 120 × 36 pt list row, the tilt of
   the members' tokens alone must say "uneven" or "all square".
3. **Drive it from a plain pose or state object** of named controls with ranges (for a character:
   squash, lift, head tilt and turn, ear lift, blink, mouth, smile −1..1, gait phase …; for an app
   object: its states and their sizes). Expressions are presets that blend. Clamp ranges that break
   the drawing (ear lift at 1.0 stuck out sideways, so the range was rescaled to make 1.0 the old 0.7).
4. **Render a pose sheet and a walk sheet** (e.g. 8 frames × 4 facings), or every state at every
   size, and take three looks before wiring the hero into the product.
5. **A reaction never contradicts its event.** A wince with a smile reads as laughing at the user;
   worried brows raise the inner ends (outer ends read as anger).
6. **Attached parts grow out of the body:** colour continuity across the seam, a thin fillet of the
   body's colour, no shadow at the root; never an outline. A flat chord at an ear's root read as "a
   card cut out"; a dome alone read as a pad stuck on.
7. **Accessories live in a fixed envelope**, in their own layers, never covering the information the
   hero carries; an accessory drawn alone is told the hero's size, not its own.
8. **Guard painted pixels across the extremes of the pose space**, not the default pose: e.g. seam
   colour difference < 20 RGB, darkening < 7 luminance, outline corner angle < 15° per pixel, over
   every pose corner × every lighting, each guard proven by a mutation (`references/verification.md`).
9. **Keep charm refined** (blush at full strength looked like a toddler's; it shipped at 45%), and
   **iterate hard details in numbered versions** (v1 … vN), recording what each rejected one read as.

Example (expense-splitting trial, its own answer): a level line with one token per member, above
it when owed, below when owing (height = sign × (27 + |balance| / max |balance| × 83) pt). Its job:
live state, a reaction (it tilts as a new expense lands), a replay (squaring up settles every token).

**Cue → misreading.** When a part misreads, find the cue that causes it and swap that cue. These
rows come from three products; find your own cues the same way.

Example (shipped puzzle game, a clothed four-legged mascot and its props):

| Cue | Read as | Swap |
|---|---|---|
| hem band + parallel highlight + long gloss | an inflatable | folds with lit ridges (cloth) |
| steel-blue shade, straight terminator | a metal tube | sky-blue shade with bounce light, curved terminator |
| a part lit with its own gradient | a ball stuck on | light it with the body's gradient |
| small repeated prints along a path | dirt | one stamp per unit that pops and fades to ~18% |
| puffs rising from the ear | a thought bubble | rise from the source to the nose |

Example (app objects and motifs, from two trial runs):

| Cue | Read as | Swap |
|---|---|---|
| spokes from a tile's centre to its edge midpoints | a gift ribbon | a motif inlaid inside the tile |
| a star with a centre hole | a settings cog | an inlaid star with no hole |
| chain-link joints between kept days | a chain ("don't break the chain", a pressure the identity rejected) | a flat band joint, only between truly consecutive days |
| a nonzero balance drawn on the zero line ("+12.10") | settled | keep it ≥ token radius + 6 pt off the line |

---

## 11. Icon, launch screen and store art

Draw the icon, launch screen and store art with the product's own renderer, so the store promises
exactly what ships, and guard each against drift. Screenshots and preview video are captured from the
real app, never redrawn (`references/release-and-store.md` §6).

**Icon:**
- [ ] Drawn from vector art at each size with a detail pass per size (a cloud only from 120 px up);
      never a downscaled 1024. Each file tested to equal a fresh render. Opaque; no sliver of a
      cropped part under any platform mask.
- [ ] Key features hold small (each eye ≥ 6 pixel rows at 120 px; nothing hairline at 40 px).
- [ ] Greyscale squint at ~29 px: a sky top with the luminance of the character's fur melted the
      head into the sky; the zenith was deepened.
- [ ] Judged at 1024 and 180/120/87/60/40 px, among the genre's icons, on light and dark wallpaper,
      in every mask, with the rubric below. A fallback icon is ready before review.

**Launch screen = the real first frame.** Render the first frame's backdrop with the app's own code,
install it as the launch image, and guard it by a pixel diff against a fresh render. A mark on the
launch screen must be drawn by the first frame at the same size and place, or left out: one "blinked
out at the first frame, then came back about a second later at twice the size". No ambient particles
in the launch image (the first frame has none). Add a variant for a second lighting. A returning
user whose look differs from the default gets a crossfade, not a cut on frame 2.

**Fix at the source, then regenerate.** A flaw a derived asset shows from the shared renderer is
fixed in the renderer (with its own looks and guards, in every view); then every derivative is
regenerated: icons (twice, byte-identical), screenshots, preview video. The icon's "flat-cut ears
read as a card cut-out at 1024"; the fix went into the character painter, and one pass forgot to
re-record the preview video. Track the regeneration as a pre-upload item.

**Youthful-reading rubric** (score any store art before shipping if the audience is adult), each
criterion High / Medium / Low: (1) subject: a portrait of a young animal says "pet app", the working
surface says the genre; (2) baby schema: head share, eye size and roundness, catch-light size, blush;
(3) numerals: a number on a cute character reads as a counting app, on the board as a puzzle;
(4) palette: primary blue, lime green and pink flowers read as a picture book; (5) typography: no
toddler lettering, ideally no words; (6) the page around it: name and captions coded for the real
audience. Anything High on 1–3 is too young. Example (shipped puzzle game): the first icon (mascot
~55% of the frame, eyes 11% of its width, a "1" on its tag) was High on 1–4; the replacement (the
product screen, mascot ~22%, eyes 8%) was Medium on 1–2 and Low on 3–6.

> **Dated facts (as of 2026-10 — re-verify before relying):** Android adaptive icons draw 108 dp
> layers, of which a 72 dp viewport shows and a 66 dp circle is the safe zone. Icon alpha and
> launch-screen caching: `references/release-and-store.md` §6 and §8.

---

## 12. No AI-generated art

Use no AI-generated images anywhere a user looks (product art, icon, store screenshots, ads); mood
boards only. AI art beside drawn art "looks like two different games"; players notice (about 9
low-star reviews of one top competitor objected to AI art in the game, about 5 to AI ad creatives);
provider output terms differ; and ownership is doubtful.

> **Dated facts (as of 2026-10 — re-verify before relying):** In the US, purely AI-generated images
> are not protected by copyright (*Thaler v. Perlmutter*, D.C. Cir., 2025-03-18; the Supreme Court
> declined to hear the appeal in 2026). Not legal advice; the owner decides with counsel.

---

## 13. The look loop

Never judge a visual change by reading code: "every visual step was wrong the first time and right
the second". The shipped puzzle game's first probe renders had four faults every test passed: a
self-recolouring trail (5.1), a loaf-of-bread mascot (10), a hidden payoff (2) and prints read as
dirt.

### 13.1 The loop

1. **Render to images headlessly:** a harness paints every painter and screen to PNG in a gitignored
   folder (`<preview>/out/<topic>/`), named by state and size (`sheet_text2_360x780.png`,
   `v2_icon_60.png`, `before_*`).
2. **Render the look matrix, not one state.** This is the canonical matrix; other files link here.
   - **Phones:** the smallest supported and a standard one (section 8). **Themes:** every theme, in
     every lighting the product ships (section 9). **Text:** 1×, ~1.3× and 2×, with the longest copy.
   - **Locales:** every supported locale and script direction
     (`references/ux-and-accessibility.md` §Localisation, RTL and calendars).
   - **States:** empty, one, full, busy, failed. **Motion:** Motion Off for anything that moves.
   - **Add the axes your product has:** first-run and returning user, quiet (unavailable) states, pose
     and parameter extremes, every generated variant; the automated matrix adds safe areas
     (`references/verification.md` §4).
3. **Open every image and look at it.** Write each fault down in words.
4. **Budget at least three looks per change**, each recorded: "Look 1: the title broke 'Remove /
   Ads' beside the price on a 360 pt phone. Look 2: … Look 3: accepted." Stop when a look changes
   nothing, and say "accepted".
5. **Play the moment on a device or simulator.** "Three of the worst bugs were invisible to every
   test and obvious in one played level." If the change is not visible in the screenshot, it is not
   done.
6. **Compare beside the category winner** at the same size, and name the one element they polished
   that you left plain. In the word game "that comparison has produced every breakthrough".
7. **Fix at the source painter**, then regenerate every derived asset (section 11).
8. **Record it** in DESIGN.md beside the plan written before building, as Plan / As built with each
   look and the guarding test (format: `references/project-kit.md`; `assets/templates/DESIGN.md`).

### 13.2 Instruments for what one still cannot show

- **Contact sheets for families.** Render all N generated variants (icons, emblems, textures,
  themes, levels, poses) onto one sheet and read it. It asserts nothing; it is still mandatory. On
  first run in the word game a motif came out as a gold diamond grid, a leaf as a torn blob (mirrored
  control points) and a turquoise-named emblem in pink: "every one of those passes a paint test".
  Tile PNGs with `scripts/contact_sheet.py`, run by the Pillow virtual environment the README sets
  up (`--cell 390x844` keeps phone screens tall; `--help`):
  `~/.venvs/flagship/bin/python -I <skill-dir>/scripts/contact_sheet.py out/icons/*.png --out out/sheet.png --title "look 2"`
- **Filmstrips for faults of order.** Most "not good enough" faults are correct in every frame and
  wrong in order or timing: a box drawn empty then filled, a reward before its cause, two copies of
  one character during a fade. Lay out frames at a fixed step side by side with the same script
  (`--filmstrip`); a platform's screenshot tool cannot see a 300 ms beat. Pick stills from it too:
  the event frame is often the worst (a goal frame put the character over the last number, "11"
  read "1", and froze a segment mid-transition as a hard wedge).
- **Before/after pairs.** A before/after capture is the test, not bookkeeping: a change that shows no
  difference controls nothing (section 3.4).

### 13.3 Real viewing conditions

- [ ] Shipped size, beside its real neighbours, composited on the real background. An arrowhead
      verified at 600 px was invisible at the 20–28 px it ships at; ratio rules (base ≥ 2.5× stroke,
      length ≥ 1.5× width) replaced fixed numbers.
- [ ] A 2× crop for edge cleanliness, but judge at hand size: a "collision" seen in a 2× crop was
      correct at hand size, and the "fixes" made the mark vanish.
- [ ] Icon sizes and masks; greyscale; 2× text; every lighting; outdoor brightness for subtle cues.
- [ ] Re-look every theme after a per-theme tweak; a fix in one theme can break another.
- [ ] Turn taste into a rule, then regenerate (a level that read as a barcode made the generator
      refuse straight runs of 4+).

---

## 14. The quality bar: seven questions and two edge checks

The canonical form: SKILL.md and the DESIGN template carry the short form, and every other file
refers to it by name. These came from builds an owner rejected as "an app, not a game"; each
question names one of the reasons, and every one has failed in a real build at least once.

Run them on every screen before calling it done, across the look matrix (13.1), and answer each in
writing for the slice. The identity brief decides *how much* (`references/kickoff.md` §7.4); each
question asks whether that decision was made and carried out.

1. **Alive at rest?** Is the screen alive at rest, in the measure the identity sets? Stillness may
   be a decision, never a default. A word game's reward screen froze after its show: "every pixel
   identical for as long as the player looked, on the one screen the game is played to reach".
   *Game:* one slow wandering background plus one focused beat, below notice (that game's ceiling).
   *App:* live state looks live and stale state says so; a sync mark shows only while syncing; one
   quiet ambient element, or none in a tool.
2. **Does touch have weight?** Every touch gets an immediate response with physical character suited
   to the identity: a spring for a toy, a crisp depress-and-settle for a tool. Never a one-frame snap
   with no response ("a state that snaps in one frame is a checkbox"). *Game (pieces, boards):* what
   the finger touches leads and lags, springs up and settles. *Game (a controlled avatar,
   Proposed):* the avatar never lags input; weight lives in secondary motion (tilt, trail, glow)
   (`references/domain-games.md` §Real-time and action games). *App:* press states respond on the
   frame of touch; drags follow from the first frame; a swipe resists, then commits or springs home.
3. **Do results arrive?** Earned or completed things travel from where they happen to where they are
   kept, and the destination changes only when they land. *Game:* a reward flies to its counter,
   which ticks on landing. *App:* a completed task travels to its list; a payment settles into the
   balance; a saved item goes visibly to where it now lives.
4. **Is every surface from the one material system?** Second-ring surfaces included: counters,
   toggles, toasts, errors, loading, settings rows, sheets. For flat styles, "material" means the
   project's surface system: fills, rules, elevation, type (section 3). *Game:* the second-ring
   sweep in 3.1. *App:* no platform-default control beside designed ones.
5. **Does each screen arrive?** One overlapping movement, never pop, never queue; a reduced-motion
   variant cuts to the same settled frame. *Game:* board, hero and controls rise in together.
   *App:* a list's rows rise as one movement, not one by one.
6. **Does it read at its emptiest?** Zero, one and full. A progress bar fine at 40% drew nothing at
   0%, the state every new chapter opens in. *Game:* a chapter at 0%, a counter at 0, a full row.
   *App:* zero items, one, a thousand; the longest name; first run and power user.
7. **Does the thing arrive before its container?** A box painted empty and then filled reads as a
   form loading; only a filmstrip (13.2) shows it. *Game:* the prize is there before the panel that
   frames it. *App:* content, or a placeholder of its real size, before the card frame.

**Two edge checks:**
- **E1: change while moving is handled.** Input during an animation hurries it home: the model
  commits at once and the old motion finishes fast; never queue, never teleport. The same holds when
  a setting or the app state changes mid-motion. Added after a review found 11 faults, all of this
  kind (`references/motion-and-feel.md` §Sequencing). *Game:* a tap during a long show skips to the
  settled state, the next action live within 300 ms. *App:* a sync update, a second tap or a trip to
  the background mid-transition.
- **E2: a stuck user sees the way out.** Helpers are visible at exactly the moment they matter
  (`references/ux-and-accessibility.md` §Stuck users). *Game:* undo and restart are one visible tap;
  an idle nudge lights the next helper. *App:* every error names its remedy; undo is one tap; every
  flow shows its exit.

**Extras** live in their domain files, never numbered after the seven: game extras G1–G3 in
`references/domain-games.md` §1, app extras A1–A4 in `references/domain-apps.md` §2 (which also
gives a check per app reading). A project adds its own in DESIGN.md. Example (habit-tracker trial):
"Does the Persian build read as made in Persian, not translated?"

**Escape hatch:** if a screen passes all seven and both edge checks and still feels plain, put it
beside the category winner's equivalent at the same size and name the one element they polished that
you left plain. Motion numbers behind 1, 2, 3, 5, 7 and E1: `references/motion-and-feel.md`.

**Per-screen visual acceptance:**
- [ ] The seven questions and two edge checks answered "yes" in writing across the look matrix;
      the largest content fits.
- [ ] Paint and bounds tests per painter; contrast floors per theme and lighting; greyscale guard.
- [ ] Accessibility audit green, text at ~1.3× and 2× clean (`references/ux-and-accessibility.md`);
      the reduced-motion path reaches the same end state (`references/motion-and-feel.md`).
- [ ] Three looks recorded in DESIGN.md; the winner comparison done and its finding written down.

---

## 15. The failure catalogue

What "not good enough" looked like in past products. Hunt for each pattern on every screen.

| Symptom as reported | What it really was |
|---|---|
| "Looks like an app, not a game" (three builds) | static screens; state that snaps; numbers that change instead of arriving; flat surfaces; screens that appear |
| "A title floating on a pattern reads as a settings screen" | hero content with no surface under it |
| Reward panel "reads like a weak app" after its animation shipped | the settled frame, stared at for seconds, was a dark rectangle, floating text and three flat glyphs: "a dialog wearing a drum roll" |
| "A box opens its mouth, nothing comes out" | the container opened onto its own front face; the reward was bookkeeping text |
| Menu "reads as a list" | two design decisions each carried to ~80% and stopped; an accent on its own colour, 19 RGB apart |
| Stuck state "in the language of a validation error" | a slim red banner at the moment the user most needed help |
| A refused tap "reads as broken" | a dead button tapped at zero: pixel-identical before and after |
| Hundreds of green tests caught none of the blockers | the faults lived in the seams (screen ↔ profile ↔ clock ↔ seed) that tests inject around |

Four classes cover nearly all of it:
1. **Correct frames, wrong order or time.** Every still looks right; the sequence reads cheap.
   Instruments: filmstrips, frame-by-frame value tests, the content-before-container question and
   the change-while-moving edge check (section 14).
2. **Flat default secondary surfaces** next to designed ones. Instrument: the material sweep (3.1).
3. **Edges nobody screenshotted:** empty states, off-path flows, second-ring screens, settings-off
   paths, transitions between screens. Instrument: the look matrix (13.1).
4. **The screen says something the code does not do:** a label promising a destination, copy
   describing old behaviour, a balance shown before its reward lands. Instrument: drive the real
   flow and read the result as a user would (`references/verification.md`;
   `references/ux-and-accessibility.md` §Copy precision).
