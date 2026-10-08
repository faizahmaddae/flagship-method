# Kickoff: from a request to a reviewed kit

Turn the owner's request into a written goal with the owner's own success test, evidence from
parallel research, an identity that belongs to this project alone, a doc kit a fresh model can build
from, and an adversarial review of that kit. Kickoff ends at Gate 0, the owner's go.

**Read when:** the repo has no `docs/<slug>/` kit, or the owner has just described something new.
Read this file in full at kickoff. A project adopting the method mid-way follows
`references/planning-and-slices.md` §Retrofit, which runs these steps in compressed form.

## Contents
1. The kickoff on one page · 2. Capture the real goal · 3. Read the owner: commissioner or
developer-owner · 4. The first questions: split the question, never wait · 5. Research in parallel
tracks · 6. Review the research adversarially · 7. Identity · 8. Write the kit · 9. Review the kit
adversarially · 10. Gate 0 · 11. Kickoff checklist · 12. Templates · 13. Traps

---

## 1. The kickoff on one page

1. Capture the goal (§2) and read the owner (§3) from what they have already written.
2. Send one short question block at once (§4), holding only what the owner alone can answer.
   Research starts in the same moment, on your recommended answers recorded as **ASSUMED** (§4
   item 3). No track waits for an answer.
3. Run five research tracks (§5). Each writes a sourced report and keeps its scripts and counts.
4. Review the research adversarially (§6) and record the tally.
5. Derive the identity (§7): render candidates, pick, write the identity brief.
6. Write the kit (§8) with `scripts/init_kit.py` and `references/project-kit.md`.
7. Review the kit adversarially (§9); fix the docs before any code.
8. Hold Gate 0 (§10): the owner's go, and every ASSUMED answer on a permanent thing confirmed.

**Time.** In the shipped puzzle game the tracks, the kit and its review took about one day of agent
time, and the game was store-ready four days after research began. The review alone changed the ad
cadence, a store subtitle and the reward design before any product code existed. For a small
project, shrink the tracks (§5.7); never skip them.

| Kickoff output | Lives in |
|---|---|
| Goal sheet, owner's success test | the "Goal" section at the top of `docs/<slug>/PLAN.md`; one line in the root `CLAUDE.md` |
| First question block, exactly as sent and dated | PLAN, "First question block (as sent)", under the Goal |
| Owner profile and decision rights | `DECISIONS.md` #2, "Decision rights" (the §3 matrix) |
| Owner answers; ASSUMED answers | DECISIONS entries (an ASSUMED one's title ends **ASSUMED**), plus the ASSUMED answers table under PROGRESS "Open questions" |
| Standing owner preferences | the "Standing owner preferences" section of `PROGRESS.md`; a memory note too, only in this project's own memory (`references/working-with-the-owner.md` §11) |
| Track reports, scripts, derived counts, probes | `docs/<slug>/research/`, summarised in `RESEARCH.md` (raw data: §5) |
| Identity brief | `DESIGN.md`'s "Identity brief" section, then its Quality bar; the art-direction rules go to DESIGN §2.1 |
| Questions keyed by moment; messages drafted but not yet sent (the Gate 0 message) | `PROGRESS.md` "Open questions": the When / Ask timing table (`references/working-with-the-owner.md` §5) and the "Messages drafted, not yet sent" line |

## 2. Capture the real goal

1. **Write the goal in the owner's words first, then yours.** Keep the verbatim text (original
   language plus translation). The owner's phrases outlive every paraphrase and become tests.
   Example: "if it has a reward, where is it?" (a predecessor game) and "do you want to play the next
   level?" (the shipped game) were each used word for word as acceptance questions.
2. **Separate four kinds of success; each has different judges at different times.** *The owner's
   judgement* is how the finished thing feels in the hand, asked at the first owner gate as **one
   question** in their language; fix it now so the plan builds toward it, fitted to how the product
   is used (a game, a daily-use app, an episodic tool; wordings in `references/planning-and-slices.md`
   §3). *Product truth* (valid content, enforced rules, true store text) is proven by guards
   (`references/verification.md`). *The craft bar* is "The quality bar: seven questions and two edge
   checks" (`references/visual-design.md`), with `references/motion-and-feel.md`. *Market health*
   is set per product type later (`references/domain-games.md` §13, `references/domain-apps.md`
   §14); never invent launch metrics at kickoff.
3. **Ask what the owner rejected before, and why.** A past rejection is their real bar, stated as a
   failure. Record it as a standing fact in the router ("the owner rejected a previous project on
   output quality") and turn each reason into a checkable question. Example (predecessor game): "it
   looks like an app, not a game" came back on three builds in a row, for a different reason each
   time; each reason became one quality-bar question, so none of them is hypothetical.
4. **"Not good enough" is rarely one big flaw;** it is four recurring classes: wrong order or
   timing, platform defaults beside designed surfaces, unscreenshotted edges, and UI or store text
   the code does not make true. Bar them from day one (`references/visual-design.md`).
5. **Pin the constraints that change the plan:** platforms and device scope (phone only? portrait?),
   regions, UI languages, scripts and calendars, the money model, the budget for paid assets or
   specialists (often zero), accounts that already exist, the country the owner's store accounts
   would be held in (§5.5), the owner's own packages and release procedures, sister projects,
   permanent bans ("no AI-generated art"), and any deadline (it becomes PLAN's calendar line:
   `references/planning-and-slices.md` §1).
6. **Name the release lever:** the irreversible public step (store submission, publish, production
   deploy). The owner holds it, and every upload; they pull it only after their own device test. It
   shapes every gate (`references/working-with-the-owner.md` §1).
7. **Fill the one-page goal sheet (§12.1).** An empty field becomes a research question or an owner
   question, never a guess.

## 3. Read the owner: commissioner or developer-owner

**Classify per domain, not per person.** Example (shipped puzzle game): the owner maintained their
own ads wrapper package, release procedures and developer accounts, so they were a developer; they
also said repeatedly that they had no game-design experience and wanted the builder to decide.
Treating them as a developer who co-decides design would have handed them choices they could not
judge; treating them as non-technical would have ignored their package and their release routine.

| Signal | Points to |
|---|---|
| Describes outcomes and feelings ("premium", "must not look weak"), says "you decide" | commissioner in that domain |
| Asks "is it worth it?" or "what does this do?" | commissioner there; answer with cost and benefit |
| Names packages with versions, links repos, has a release routine | developer-owner for engineering and release |
| Offers their own library or tool | developer-owner; study it before adopting (`references/working-with-the-owner.md` §8) |
| Strong views on one area (art, sound, copy) | co-decides that area; show finished samples, not options |
| Answers numbered lists in one terse line | wants decidable questions; keep them that way |

Fill this matrix at kickoff and record it as a DECISIONS entry:

| Domain | Delegates | Co-decides | Decides |
|---|---|---|---|
| Product scope and hard requirements | | | ✓ (default) |
| Look, feel, sound, UX | ✓ (default) | if they ask to | |
| Engineering, stack, architecture | ✓ (commissioner) | developer-owner, on request | |
| Money, accounts, legal identity, keys, release | | | ✓ (always) |

**Commissioner:** decide design and engineering from evidence and record why; ask only owner-only
items, few of them; explain every technical term in plain words the first time; show only finished
work; build judging tools for what they must judge.

**Developer-owner:** follow their conventions (naming, account structure, release procedure, their
packages once studied). Report engineering choices as "decided X because Y; say if you object", not
as questions. Where they co-decide, give a recommendation with evidence and a finished sample. Never
lower the bar because they are technical: they still get the device-check list, and owner-only items
stay theirs.

**Unclear:** ask once, in the first question block: "Which of these do you want to decide yourself?
(My recommendation: you decide money, accounts and release; I decide design and engineering from
evidence and record every decision.)"

## 4. The first questions: split the question, never wait

1. **Split every question before asking it.** What research, the genre or the platform can answer
   goes to a research track; only the remainder goes to the owner. Owner-only: taste in a *finished*
   thing, risk appetite, budget, legal identity, accounts and where they are held, facts about their
   own market or language, product scope, release control. Handing the owner a design decision is
   not deference; it is offloading, and it gets worse answers than research. Example (word game):
   "Should function words count as answers?" had been settled by the genre leaders years earlier, a
   five-minute search. "Is this word familiar to native speakers?" was the owner's, as one; the
   builder made a sample and asked.
2. **Ask few.** At kickoff, no more than five: numbered, one line each, in the owner's language,
   jargon explained inline, anything permanent flagged, each ending "(My recommendation: X,
   because Y.)" Format: `references/working-with-the-owner.md` §14.1.
3. **Questions never block research.** Send the block at once, marked "no rush, nothing is
   blocked". Work proceeds on your recommended answers, each recorded in DECISIONS with status
   **ASSUMED** and superseded by a new entry when the real answer arrives (convention:
   `references/working-with-the-owner.md` §2). Nothing permanent may rest on an ASSUMED answer. If
   answers never arrive, Gate 0 is where the ASSUMED answers on permanent things (name, ids, the
   account holder) must be confirmed (§10). Give every research worker each owner answer, each
   ASSUMED answer marked as such, and every fixed constraint; if a worker lacked one, void its
   affected notes. Example (shipped puzzle game): readers could not see who would make the signing
   key or test on devices, guessed, and the brief had to say "ignore their items 3 and 4"
   (`references/traps.md` T-17b).
4. **Ask taste questions with a sample** (a render, a sound, a sentence), never an abstract option
   list.

| Typical kickoff question | Who answers | Note |
|---|---|---|
| Which platforms and regions first? | owner, given research | Track A brings revenue per user by country |
| In which country, and in whose name, will the store accounts be held? | owner | slow and permanent: first block (§5.5) |
| Which UI languages? | owner; research brings the scripts, calendars and digits each needs | `references/ux-and-accessibility.md` §Localisation |
| Ads, purchases, subscription, paid, or none? | owner decides *whether*; research says *how* | `references/monetization-and-privacy.md` |
| App: used daily, or episodically (when something happens)? | research (review coding); the owner confirms | it picks the gate question (`references/planning-and-slices.md` §3) |
| App: accounts? Data on one device, one user's devices, shared between people, or server-held? | owner decides scope; research brings the obligations | `references/domain-apps.md` §1 |
| Which visual style? | identity step (§7) | the owner judges a finished render later |
| Engine, state library, packages? | research probes (§5.3) | unless a developer-owner co-decides |
| Is the name free? | research (§5.5) | the owner confirms at Gate 0 |
| Budget for paid assets or specialists? | owner | one money question with a researched quote |
| Who makes signing keys and tests on device? | owner | default: the owner, at the end |
| How much content, how many screens? | research plus the plan | never the owner's homework |

## 5. Research in parallel tracks

**Rules for every track.**
- **Research is evidence, not the plan;** decisions come after §6.
- **Tag every factual statement:** **Verified** (URL with date, local SDK or package source by
  file:line, or a run you did), **Proposed** (a choice with reasons; numbers are starting values to
  tune on a device) or **Unverified** (marked where it appears). Close each report with a "Not
  verified" list.
- **Primary sources first:** the installed package or SDK source, the platform's own docs
  (fetched, dated) and store pages; blogs and SEO pages are unverified. Example (shipped puzzle
  game): local source reads caught a plugin asserting the opposite of a flag the research brief
  recommended, a store restore that stamped pending purchases "restored", and an article's claim
  about an ad SDK's tracking domains that the SDK's own manifest disproved; each would have shipped
  a bug. Rank evidence by study design (`references/monetization-and-privacy.md` §1).
- **Probe, don't estimate:** every load-bearing technical claim gets throwaway code run under tests,
  with numbers, hardware, concurrency, and "what it did not prove".
- **Keep the evidence, within licence and privacy.** Scratch disappears, so copy the evidence into
  `docs/<slug>/research/` and `docs/<slug>/reference/`, with an old→new path table in `RESEARCH.md`.
  Always keep probes, scripts, query dates and parameters, derived counts and renders. Raw
  third-party text (review bodies, forum posts) enters the repo only if its licence and privacy
  allow, author names dropped; otherwise it stays in a local, gitignored `docs/<slug>/research/raw/`,
  with the gap stated under "Not verified". Competitor screenshots and icons never enter the repo.
  (The rule's home: `references/project-kit.md` §11, "What may be committed".)

### 5.1 Track A: market and competitors
1. **Competitor table** of 10–15 products, plain baseline clones included: seller, release and
   update dates, rating count, average, price and in-app items, size, date viewed.
2. **Open with "Corrections to the brief":** test every premise in the request against data and list
   each wrong one with the datum that refutes it. Example (shipped puzzle game): a 471K-rating
   "path" competitor was a different genre; "a cute theme is worth about 20×" was confounded by a
   publisher running several 400K-rating games and buying heavy ad traffic; another leader's volume
   came partly from play-to-earn cash-out traffic. Acting on the second would have over-invested in
   theme and under-invested in the store page.
3. **Store average vs the mean of recent written reviews.** Averages hide anger: 4.66 → 3.39,
   4.81 → 3.67, 4.63 → 3.38 in that market. The gap is the opening.
4. **Code the reviews with a reproducible script.** Fetch up to ~500 recent written reviews per app
   with a small project script (endpoints and limits: dated block below; add other countries for
   tiny apps), de-duplicating and keeping rating, date, version and country. Code them with
   `scripts/code_reviews.py` (`--help` gives the input format): one regex per theme (optional "must
   also mention X" prefix), counted per app × theme for complaints (1–3★), loves (4–5★) and
   complaints inside 4–5★. Read every 1–3★ review by hand too, and say that counts are approximate
   (a review can hit several themes). Paraphrase, never quote. Keep the fetch script, the theme
   file and the counts; raw text follows the rule above. Example: 2,811 reviews (1,188 negative) set
   the whole ad and UX policy (numbers in `references/monetization-and-privacy.md` §1).
5. **Incidental facts:** the level at which reviewers say ads began (medians of 14–45 there), "ads
   started right after the rating prompt".
6. **Close with two lists.** *Design openings* (complaint theme + count + the rule it implies) and
   *traits we must match* (love theme + count), plus other gaps (accessibility, touch accuracy,
   motion sickness). They became decisions almost one to one.
7. **If the product itself is undecided,** add a one-page "why this product" table: retention proof
   from a large player, incumbents' rating counts, adjacent genres' counts, the theme gap, revenue
   per user by country, and fit with the team's strengths. Example: 84–86% next-day return at the
   original daily puzzle that introduced the rule, a largest clone of 461 ratings, adjacent logic
   games past 100M installs, no themed version found.

For an app with no reviewable rivals, code support forums, community threads and the closest tools'
reviews the same way.

> **Dated facts (as of 2026-10 — re-verify before relying):** the App Store's public customer-review
> RSS feed served recent reviews in about 10 pages (~500 per app per country); the iTunes Search and
> Lookup API returned rating counts, averages, dates and sizes without a key; Google Play's public
> pages showed install bands and ratings and had to be parsed. The keyless Search API throttled
> after roughly 6–20 rapid calls: either HTTP 403, or HTTP 200 with an **empty body** and no error
> (a naive parser crashes or records "no results"); a retry 20 s later was still empty. Space calls
> ≥ 3 s, back off on a 403 or an empty body, and record the item as "not screened" (Unverified),
> never as "no match". Check each endpoint and its limits before writing the script.

### 5.2 Track B: core feasibility
Name the one technical thing the product cannot exist without (a generator of uniquely solvable
puzzles, a sync engine, an on-device model, a real-time renderer), then probe it under tests and
measure. Example (shipped puzzle game): the generator prototype made 1,078 of 1,078 unique puzzles
from 4×4 to 10×10; the 7×7 median was 0.078 s, the 10×10 median 19.6 s with a 283 s maximum.
"Generate offline, prove every item in CI" became a measured conclusion, and the board-size cap
followed. Deliver measured numbers, the probe's location, a recommendation and "did not prove".
Content pipelines: `references/architecture.md`.

### 5.3 Track C: stack and packages
Resolve versions on this machine and read the local source of every dependency you will lean on. Pin
the state library's real behaviour with small passing tests (example: 17 probe tests exposed
equality-filtered notifications and a silent default of ten automatic retries before any product
code existed). Grep dependencies for imports of the big UI kit. Measure engine versus no engine
(example: +0.38 MB, so the decision rested on the render loop, accessibility and an upcoming
breaking release, not on size). Confirm renderer and shader features under the test runner on each
platform. Output: a dependency manifest with exact versions and a verified/not-verified list. Stack
detail: `references/stack-flutter.md`, `references/stack-other.md`.

### 5.4 Track D: look, feel and sound
1. **Tear down 3–5 winners and the plain baseline:** name, rating count, date viewed, palette,
   shapes and depth, character, UI chrome, motion, then a one-paragraph **Lesson** each. List what
   all share. State confounds plainly ("charm probably matters; marketing confounds the
   comparison"). List what you could not verify: store pages show no sound or feel, and some
   originals sit behind a login.
2. **Render a probe headless to PNG** before any app exists: the hero at its smallest real size
   (e.g. 48 pt), a full screen at a reference phone size, and the payoff state, with the product's
   fonts loaded (without them non-Latin text renders as boxes). Flutter: a self-contained scratch
   probe package with a complete render-to-PNG test (`references/stack-flutter.md` §0). React
   Native, native, web, or any stack that cannot render headless before the scaffold exists: SVG or
   HTML drawn from the same data, rendered to PNG by headless Chrome and labelled "not the real
   stack" (`references/stack-other.md` §0). Make the real-stack render harness the first item of
   Phase 0, and re-render the chosen identity there. Example: the probe caught a trail that
   recoloured itself on every move and a reward hidden under the thing that earned it.
3. **Choose technologies the builder can create, diff and test as text:** code-drawn vectors and
   painters over bitmap tools and visual editors; sound synthesised by a versioned script over
   sample libraries whenever licensing is unclear. Record each candidate in the DESIGN technology
   verdict format (`assets/templates/DESIGN.md` §3): Verdict · Verified (version, licence, paints
   under the test runner) · The catch · Allowed uses · Plan B. Example (shipped puzzle game):
   painters for everything; shaders for backgrounds only, verified to paint under tests, with a
   gradient fallback (shader image filters did not run under tests, so no core visual may depend on
   them); a rigging runtime rejected because its files are authored in a visual editor the builder
   cannot operate (kept as plan B behind a one-file pose seam); animation-JSON players rejected
   (third-party animations did not match the style; hand-written JSON was slower than a painter and
   could not be tested); sprite atlases only from images generated at runtime; no game engine for a
   UI without physics (a second loop beside the UI framework's).
4. **Plan sourcing:** what is drawn in code, synthesised, recorded, licensed or commissioned. Verify
   each licence's text; log URL, author, licence and sha256. CC BY needs credit; paid licences
   forbid redistributing sources (keep bought sources out of public repos); keep an "avoid" list of
   stores whose terms exclude apps or end with the subscription. Bundle fonts under a verified
   licence; never rely on system fonts.
5. **AI-generated images: mood boards at most,** never in the product, the icon or store art
   (reasons and the dated legal fact: `references/visual-design.md` §12).

> **Dated facts (as of 2026-10 — re-verify before relying):** a large CC0 sound library required a
> login to download. Several popular stock-audio subscriptions excluded apps and games from their
> standard licence or stopped new uses after cancellation. A popular rigging tool's runtime was
> MIT-licensed, but exporting its files needed a paid plan from 2025-10.

### 5.5 Track E: money, legal, region and name
1. **Money:** evidence for the model ranked by study design, plus the owner's first-party numbers
   from sibling apps if any (`references/monetization-and-privacy.md`).
2. **Audience and age are a decision slot.** Decide them from the product and the money model, and
   record why. Kids and family categories bring obligations on ads and analytics, and a cute
   character can count as child-directed (dated block below). Example (shipped puzzle game,
   ad-funded, with a cute mascot): an adult (18+) store target audience, adult-coded store art and
   copy, and a fallback icon ready, to stay out of family-program obligations. A product made for
   children makes the opposite choice and builds to those obligations. Rules, age signals and the
   fallback icon: `references/monetization-and-privacy.md` §Audience.
3. **Owner-region constraints are a compliance check.** Before anything permanent, establish with
   sources whether the owner can hold a developer account in each target store and receive payouts
   (country of residence, payment and tax requirements); whether sanctions or export rules restrict
   the owner, the target users' countries, or a service the product depends on; and which local
   stores matter in the target markets. Ask the owner-only part (the country and the name the
   accounts will be held in) in the first question block. Record the facts and leave the decision
   to the owner, with "check the program terms, and a qualified adviser where sanctions apply". Never
   suggest a way around eligibility or sanctions rules. Example (word game for one regional
   market): the owner reported that a hosted remote-configuration service was filtered in the main
   audience's country; anything such a service serves needs a built-in default that works when it
   is unreachable.
4. **Name screening, before anything makes a name permanent.** Check each candidate against the
   trademark registries of the main markets (live marks, class-filtered), both stores in several
   countries, and domains. Verdict per name: *Recommended*, *Good fallback* or *Weaker*, with "this
   search is not legal advice; get a clearance opinion". Keep the scripts; a name the store search
   refused to answer for is "not screened", never "free". Don't name a mascot in store text until
   cleared. Example: the working name was a registered mark with a live app; a candidate one letter
   from a registered game mark was rejected; the genre's reference product name was a freshly
   registered mark of a large company, so it was banned from every player-facing text.
5. **Mechanics are free; expression is not.** Generate your own content; never copy the reference
   product's levels, names, palette, shapes or sounds.

> **Dated facts (as of 2026-10 — re-verify before relying):** screening used the USPTO trademark
> search, TMview (EU and national offices), store search APIs per country (US, GB, CA, AU, DE, JP;
> rate limits in §5.1) and whois for .com/.app/.net/.io; USPTO filing cost $350 per class (from
> 2025-01-18). The US Copyright Office treats game rules and methods as unprotected; *Tetris v. Xio*
> (2012) held that copying audiovisual expression infringes; *Spry Fox v. 6waves* settled with the
> copyright transferred. Apple's Kids category barred third-party ads and analytics, Play Families
> restricted ad SDKs, and the FTC counted animated characters as one child-directed factor. Both big
> stores' developer programs restricted accounts and payouts by country of residence and sanctions;
> in some markets Android apps were distributed mainly through local stores. Read each program's
> current terms.

### 5.6 Running the tracks
**In parallel:** one worker per track. Each brief carries the goal sheet, the owner's answers so
far (ASSUMED ones marked), today's date, "search for recent facts, cite URLs with dates, mark
anything unverified", the local paths to read, the output path, and "keep scripts and counts; probes
in scratch; do not touch the project tree" (lanes and brief shapes: `references/orchestration.md`).
**Solo fallback:** run A → B → C → D → E in order (A first: its corrections change the other tracks'
questions), saving each report before starting the next.

### 5.7 Scaling down
Keep all five tracks for a small app and shrink each: A, five competitors × 100 reviews; B, one
probe; C, a version check plus one behaviour test; D, three winners and one render; E, a name
screen, a region check and a policy check. Never drop name screening, the "Not verified" lists, or
the scripts and derived counts.

## 6. Review the research adversarially

1. **Run skeptics with distinct lenses** before anything becomes a decision. Each reads the reports
   and local sources, edits nothing, and returns only defects with evidence. **FACTS AND SOURCES:**
   every number traced, confounds named, dates present, no secondary source passed off as primary.
   **USER HARM AND POLICY:** each recommendation against the complaint counts and platform rules.
   **FEASIBILITY AND CONSISTENCY:** buildable and verifiable with the real tools; no two tracks
   contradict each other.
2. **Write each defect** as failure path, fix, and the test that would fail without the fix (§12.3).
   Fold every confirmed defect into a numbered decision.
3. **Record the tally** in the DECISIONS header ("N findings, M confirmed, all addressed") and tag
   rules born from a finding inline ("(skeptic H3)").
4. **Reports are evidence: never edit them silently.** Head each one "kept as evidence; DECISIONS
   wins where they differ". When a review finds a factual error in a report (a wrong number, a
   missing tag), add an **Errata** block at the top of that report (date, finding id, the
   correction) and record the resulting decision in DECISIONS; leave the body as written.

Example (shipped puzzle game): one combined review of the research and the kit drafted from it
raised 82 findings, 71 confirmed, all addressed. It moved the first interstitial from level 8 / 6
min to level 20 / 8 min, removed a store subtitle that reused a competitor's title, and dropped a
"double the reward" idea that contradicted the no-currency decision. General review protocol:
`references/verification.md`.

## 7. Identity

Every project finds its own identity. This skill transfers the bar and the method, never a look.
Rules about **order, causality and honesty** are universal (effects after causes, content before its
container, input never blocked); rules about **personality** are slots decided here. A finance app,
a meditation app and a word game should each end somewhere different.

**How to read the examples.** Each slot below shows two contrasting answers: the shipped puzzle
game's, and a hypothetical product from another domain. Neither is a default. The structural
motifs among them (a route replayed at the finish, the finished board as a picture, a tonal ladder
resolving at the finale, a mascot, the "quiet ledger" look) are **one project's answer; do not
reuse the motif unless your own identity derives it.** If your product sits near an example, add
that example to your distinctness check (§7.3): a direction that matches it fails.

### 7.1 Inputs
1. **Audience and context of use:** who, the age band and its legal consequences (§5.5), when and
   where, and Track A's love themes. Example: "a brain workout that feels just right", "relaxing at
   bedtime" (the puzzle genre); "I finally see where the money went" (hypothetical budgeting app).
2. **Category conventions:** what every winner shares, to match, never to copy. Example (puzzle
   genre): one palette applied strictly; one light direction or none; a single hero element; every
   state change felt, never a snap; a beautiful payoff state; no clutter.
3. **Gaps:** what competitors leave plain or get wrong. Example: the clones had no character, no
   theme, a flat grey UI and a generic icon.
4. **The owner:** what they liked and rejected, and their permanent bans.
5. **Languages and scripts:** direction, digits and calendar shape the layout and the type from
   the first render (`references/ux-and-accessibility.md` §Localisation).
6. **Production means:** what this team can produce to the bar (code-drawn art, synthesised sound, a
   budget for one commission; §5.4 item 3). An identity you cannot produce at the bar is not an
   identity.
7. **The domain file:** for an app, read `references/domain-apps.md` §Identity for utilities first;
   for a game with a character, `references/domain-games.md` §Mascot.

### 7.2 Steps
1. **Write the combination sentence.** Example (shipped puzzle game): "the charm leader's
   character, the minimalist leader's discipline, a third game's 'the solved puzzle becomes a
   picture', and the polish benchmark's character reacting above the board". Hypothetical
   (budgeting app): "the bank apps' trust, a paper notebook's calm, and the one tool reviewers
   praise for never showing a red number".
2. **Name 2–3 candidate directions (two or three words each) and render each** (§5.4 item 2).
   Decide every primary element by rendering its alternatives side by side, and record why each
   loser lost. Example: for the path, a leash read as a tangle, paw prints read as dirt at that size
   and showed no corners, a glow read as neon (wrong for a calm theme); a thick ribbon won.
3. **Run the leak check.** List every motif you are drawing on from this skill's examples or from
   a competitor (the motifs named above, a gate wording, a sound scheme, a material recipe). For
   each, write the reason this project's own inputs (§7.1) derive it; with no reason, drop it.
4. **Score the directions with §7.3.** A direction failing any row is out, or is fixed and
   re-scored.
5. **Write the identity brief** (§7.4; template §12.4).
6. **Judge your own probe against the benchmark and pre-plan the escalation.** Example: "the mascot
   reads as charming, competent soft-vector art; it does not reach the leader's 3D look." Plan B had
   a trigger: if the hero failed three looks on any of three criteria (it reads at 48 pt; its walk
   reads as a trot with no sliding; it would not look amateur beside a polished commercial
   character), the owner would get one money question (hire an animator, at a researched quote). It
   passed; nothing was spent.

### 7.3 Identity scorecard
| Criterion | Test |
|---|---|
| Distinct | At icon and thumbnail size beside five genre screens, a stranger points to ours; no palette-and-shape pairing shared with a competitor; it matches no example in this skill |
| Fits the audience | Matches the users' context and the audience decision (§5.5); an outsider reads the intended age |
| Carries information | The hero element has a job: it shows live state or reacts to input (replaying the user's achievement is one option among several) |
| Producible to the bar | The probe already reads as finished at its smallest real size, with the means you have |
| Survives conditions | Every lighting the product ships (a second lighting re-lit, never inverted), greyscale (no hue-only signal), smallest phone, 2× text, every script direction, and Motion Off: presentation motion removed, motion that *is* the task kept, outcomes identical for the same input (`references/motion-and-feel.md` §10) |
| Legally clear | No borrowed names, content or look; every licence logged |
| Store-safe | Store art and copy fit the intended age rating |
| Extensible | Rules hold for ten times the content; new themes swap colours inside the same structure |

### 7.4 The identity brief
Each slot: what to decide, then two contrasting examples.

- **Name and statement:** two or three words, plus one paragraph (audience, context, the
  combination sentence). *Shipped puzzle game:* "soft clay diorama". *Hypothetical budgeting app:*
  "quiet ledger".
- **Art-direction rules:** 5–8 numbered rules, each testable by a reviewer with a number or a
  yes/no; they go to DESIGN §2.1. *Shipped puzzle game:* one key light at −45°, one material recipe
  for every object, no black outlines, a corner radius of 22% of the cell, numbers ≥ 7:1 (rules and
  recipe in full: `references/visual-design.md` §2 and §3.1). *Hypothetical budgeting app:* no
  shadows and one hairline weight; amounts in tabular figures at ≥ 7:1; one accent colour, reserved
  for money arriving; motion only on values that change; every empty state shows the next action.
- **Lightings:** one (dark-only or light-only: ignore the system appearance; the look matrix drops
  the lighting axis) or two (follow the system), with a reason (`references/visual-design.md` §9).
  *Shipped puzzle game:* two, a day scene and a night scene re-lit on one structure.
  *Hypothetical neon arcade game:* dark only, because its one idea is light against the dark.
- **Hero:** what it is, proportions in units of its own height, a silhouette test at its smallest
  size, and its job. *Shipped puzzle game:* a mascot watching from beside the board; it reads at
  48 pt and reacts to each move. *Hypothetical budgeting app:* the month's remaining balance, a
  single tabular figure that reads at widget size and shows live state.
- **Feel brief** (this list is the one definition; `references/motion-and-feel.md` says how to
  execute it): the motion personality in three words · what is frequent, what is rare, and the one
  impact · what success and "no" feel like · what it must never feel like (a slot machine, a
  settings dialog, a toddler's toy) · the signature moment people will remember or share · the
  personality slots, each decided with a reason: overshoot on arrival (how much, or none), refusal
  shape, spring bounce, ambient motion (how much, or none), shake budget, refusal haptic weight ·
  starting values to tune on a device: press duration, spring settle, ambient ceiling · for a game
  with a controlled avatar (Proposed): the input-latency budget, avatar smoothing (default none),
  the hitbox as a ratio of the art, time-to-retry, hit-stop (`references/domain-games.md`, "Real-time
  and action games"). (Tap to skip within 300 ms is not a slot; it is universal.)
  *Shipped puzzle game:* "calm, tactile, rewarding"; drawing a cell is frequent, solving is rare,
  one shake per level is the impact; arrivals overshoot, departures never; when the board is
  solved, the mascot runs the player's own route (a motif). *Hypothetical budgeting app:* "steady,
  exact, quiet"; entering an amount is frequent, closing a month is rare, and there is no impact,
  only one soft confirmation when the month balances; no overshoot on numbers; no ambient motion;
  never a slot machine. *Hypothetical dodging game:* no avatar smoothing, a hitbox 0.55 of the
  silhouette, a retry within 400 ms, an 80 ms hit-stop, latency measured on a device.
- **Sound brief** (the one definition; execution and mastering: `references/motion-and-feel.md`
  §Sound identity): the sound world, drawn from the product's world (materials, instruments, voice)
  · the kind of sound system: tonal, textural/foley or minimal (sound off by default is a valid
  identity) · if tonal, one tonal family · what success, refusal and the one impact sound like ·
  the loudness ladder (three tiers) · what is synthesised, recorded or licensed · the phone speaker
  as the playback reference · whether it mixes with the user's music and obeys the silent switch ·
  music on or off by default.
  *Shipped puzzle game:* acoustic toy instruments in one pentatonic scale; each step plays the
  next note of a ladder that resets at each milestone, and the milestones form a melody the finale
  replays (a motif). *Hypothetical hiking log:* foley only (boots on gravel for a saved waypoint, a
  canvas flap for a closed day), no melody. *Hypothetical budgeting app:* off by default; one soft
  paper tick for a saved entry.
- **Voice:** the word budget, the tone, and the banned words. *Shipped puzzle game:* nearly
  wordless, for a global casual audience whose board carries the state. *Hypothetical budgeting
  app:* word- and number-dense, plain full sentences. **Banned words are per project:** other
  products' names always, plus any claim the code does not make true. The puzzle game banned "no
  ads" and "free" because both would have been false there; a product with truly no ads may say so
  if the copy checker maps the claim to code. Approved exceptions have one home that the copy guard
  reads (store rules: `references/release-and-store.md`).
- **What we will not be:** 5–10 "never" lines, each with its reason. *Shipped puzzle game:* not a
  kids' app; no black outlines; no platform-default controls; not the reference product's palette
  or shapes; no lives or timers; no AI-generated art; no clutter on the home screen. *Hypothetical
  budgeting app:* never red for a normal expense; no confetti; no streak pressure; no chart before
  there is data to chart.
- **The edge:** the 2–4 things that set it apart. *Shipped puzzle game:* the character, the path's
  material, the solve run, an honest ad policy. *Hypothetical budgeting app:* entry in two taps,
  calm at the month's end, an export the user owns.
- **Rejected directions, plan B and reference renders:** the candidates that lost, with the look
  that decided each (§7.2 step 2); the plan-B trigger and its one money question (§7.2 step 6); the
  files that prove the identity, re-rendered at every look.

The brief becomes `DESIGN.md`'s "Identity brief" section, followed by its Quality bar. The owner
meets the identity as a finished render, not as a choice between sketches, unless they co-decide
the look (§3).

## 8. Write the kit

1. **Scaffold with `scripts/init_kit.py`, dry run first.** `<skill-dir>` is the folder holding this
   skill's `SKILL.md` (for example `~/.claude/skills/flagship-method`). Always pass `--dest`; never
   run the script from inside the skill folder.

   ```bash
   python3 <skill-dir>/scripts/init_kit.py --dest <project-root> --kind app|game \
     --name "…" --slug … --one-line "…" --owner "…" --language "…" --stack "…" \
     --platforms "…" [--with-monetization] [--with-release] --dry-run
   ```

   Then run the same command without `--dry-run`. It creates the root `CLAUDE.md` router, the
   builder skill at `.claude/skills/<slug>-builder/`, and `docs/<slug>/` (with `research/` and
   `reference/`) from `assets/templates/`.
   - `--kind` (required) selects the game or app template blocks. Add `--with-monetization` for a
     product that earns money or collects data, `--with-release` for one that ships to a store or
     to production (`references/project-kit.md` §2). `--owner` takes the owner's name, or "the
     owner".
   - `--slug` is strict kebab-case (`my-app`), picked from the working name. The slug is internal:
     renaming the product later never requires renaming the slug, so scaffolding before the name
     screen finishes is safe.
   - It never overwrites: if any target exists it lists them, writes nothing and exits 2. On an
     existing project, add `--retrofit`: the kit goes to a staging folder for a merge by hand
     (`references/planning-and-slices.md` §Retrofit).
2. **Fill in this order** (per `references/project-kit.md`): `RESEARCH.md` (summary, path table) →
   `DECISIONS.md` (numbered, evidence-cited, #2 the decision rights, owner answers verbatim, ASSUMED
   ones marked) → `DESIGN.md` (identity brief first) → `ARCHITECTURE.md` → `MONETIZATION.md` and
   `RELEASE.md` if scaffolded (what is decided now; the rest when their phase starts,
   `references/project-kit.md` §12) → `PLAN.md` (the Goal and the first question block as sent,
   phases, a Phase 2 owner gate, runnable acceptance criteria; `references/planning-and-slices.md`)
   → the builder skill (invariants; inherited traps from `references/traps.md`, converted) →
   `CLAUDE.md` → `PROGRESS.md` (its eleven sections: under Open questions the timing table, the
   "Messages drafted, not yet sent" line and the ASSUMED answers; Device checks; Standing owner
   preferences; an empty END-OF-PROJECT list).
3. **Owner-specific values become numbered decisions, not hard-coded rules:** UI language, art bans,
   ad thresholds, device scope, content caps, each citing its reason.
4. **Find what is left** with
   `python3 <skill-dir>/scripts/init_kit.py --check --dest <project-root> --slug <slug>`: it lists
   every remaining `[TODO` marker by file:line and exits 1 while any remain. Use it instead of a
   grep.
5. **Done when a fresh model with no memory could start Phase 0 from the docs alone:** every
   decision cites evidence, every acceptance criterion is runnable, no topic lives in two docs,
   volatile facts are dated, every owner answer is recorded, and `--check` exits 0. In every doc, a
   slot only a later phase can fill reads "Written in Phase <n.m>; decided so far: …", and one that
   does not apply reads "none: <reason> (DECISIONS #n)" (`references/project-kit.md` §12).

## 9. Review the kit adversarially

Three lenses, in parallel or in sequence (solo: a fresh pass per lens, writing its findings before
starting the next).
- **TRUTH:** every claim traces to a report or is marked Unverified; numbers agree across docs;
  notation is defined once ("sizes are rows×cols everywhere"); volatile facts are dated.
- **BUILDABILITY:** a smaller model could build Phases 0–2 from the kit; every acceptance criterion
  runs with the real tools (a plan once required profile-mode runs on a simulator that only runs
  debug builds, found only after building; catch it here); every layer rule has a guard specified
  (seeing it fail is the Phase 0 exit); every "never" is testable. Run the kit health checklist
  (`references/project-kit.md` §Kit health checklist) and `--check` inside this lens.
- **PRODUCT AND POLICY:** monetization, privacy, audience, region, store copy and identity hold
  against the complaint evidence, platform policy, the owner's answers and the "will not be" list.

Fix the docs before Phase 0. Record the tally in the DECISIONS header beside the research review's,
and record refuted findings "so nobody re-finds them".

## 10. Gate 0

Gate 0 settles go or no-go, the scope of the first owner gate, the name (provisional or final), the
permanent ids, the account holder, and who holds the release lever.

1. **Send one message in the owner's language** (§12.5): the product in one line; the identity in
   one sentence (plus one render only if it already reads as finished); what the first owner gate
   will show and the feel question you will ask then; the name with its screening verdict; the
   permanent ids, flagged as permanent; the ASSUMED answers that need confirming; only the questions
   needed now; and the upload sentence, word for word (`references/working-with-the-owner.md` §4
   item 5).
2. **Confirm every ASSUMED answer that touches something permanent:** the name, the bundle or
   package id, product ids, whose developer account and in which country, a paid vendor. Reversible
   ASSUMED answers may stay ASSUMED until their phase.
3. **Gate 0 never blocks reversible work.** Ids become permanent only at the first upload. If an
   answer lags, scaffold under the working name and slug (§8), mark ids "provisional until the owner
   confirms", and schedule the confirmation before the first store record. Example (shipped puzzle
   game): name and package id were confirmed in the prerequisites for the first device build, not
   before scaffolding.
4. **Record the answers verbatim with dates** in DECISIONS, superseding the ASSUMED entries and
   noting which plan rules they relax; record standing preferences per
   `references/working-with-the-owner.md` §11. **On a go,** start Phase 0
   (`references/planning-and-slices.md`).

## 11. Kickoff checklist

- [ ] Goal sheet written; owner's verbatim text kept; the gate question fixed for the product type;
      past rejections recorded as a standing fact and turned into checkable questions.
- [ ] Decision-rights matrix filled per domain and recorded.
- [ ] First question block sent at once: ≤ 5 owner-only items in their language, each with a
      recommendation recorded as ASSUMED; every research worker had them, marked.
- [ ] A: competitor table, corrections to the brief, coding script and counts, openings, must-match.
- [ ] B: core probe with measured numbers and "did not prove". C: versions resolved locally;
      library behaviour pinned by tests; engine choice measured.
- [ ] D: winners' teardown with lessons; render probe; technology verdicts; sourcing plan with
      licences logged.
- [ ] E: money evidence ranked; audience decided; region and account eligibility checked; name
      screened; policies dated.
- [ ] Every report tagged Verified/Proposed/Unverified, with a "Not verified" list; scripts, counts
      and probes in the repo (old→new path table); raw text per the raw-data rule; no screenshots.
- [ ] Research review: ≥ 3 lenses, tally recorded, defects folded into decisions, errata where due.
- [ ] Identity: combination sentence, rendered candidates, leak check, scorecard, brief, plan B.
- [ ] Kit scaffolded with `scripts/init_kit.py`, filled per `references/project-kit.md`, `--check`
      clean; kit review run (three lenses, docs fixed, tally recorded).
- [ ] Gate 0 sent; ASSUMED answers on permanent things confirmed; answers recorded verbatim with
      dates; standing preferences saved.

## 12. Templates

### 12.1 Goal sheet
```
# Goal — {{PROJECT_NAME}} ({{DATE}})
One line: <what it is, for whom>
Owner's words (verbatim, original + translation): "<...>"
For whom, and when/where they use it: <...>  Use pattern: <game | daily | episodic, trigger: ...>
Platforms, device scope, regions, UI languages and scripts: {{PLATFORMS}}; <...>
Owner's country for store accounts and payouts (or ASSUMED): <...>
Money model (or none): <...>
The owner's gate question (their language; wording per planning-and-slices §3): "<one sentence>"
Rejected before, and why (verbatim): "<...>" → bar questions: <named, e.g. "Does touch have
  weight?", or this project's own question added to DESIGN>
Hard constraints and permanent bans: <...>    Deadline (→ PLAN's calendar line): <date | none>
Existing accounts, packages, procedures, sister projects: <...>
Release lever: <step>, held by the owner; every upload only on their request for that upload;
  nothing to review or the public before their device test and approval.
Research will answer: <...>    Only the owner can answer: <...> (→ first question block)
```

### 12.2 Research track report
```
# <Track>: <topic> (written <date>)
> Repo note: kept as evidence. DECISIONS wins where they differ. Moved paths: see RESEARCH.md.
> Errata (added only after review): <date> · <finding id> · <correction>
Status legend: Verified (URL+date | local source file:line | a run) · Proposed · Unverified
0. Corrections to the brief (numbered; the datum that refutes each)
1. Decisions at a glance (what this track recommends, one line each)
2..n. Evidence (tables with counts; measured numbers with hardware and concurrency)
n+1. Proposal, with rejected alternatives and why
n+2. Design openings and must-match traits (market) | proved / found / did not prove (probes)
Not verified · Sources (URL, date queried, version read) · Files (scripts, counts, renders; raw data
location and any gap)
```
The `RESEARCH.md` summary is templated in `assets/templates/RESEARCH.md`.

### 12.3 Skeptic report
```
Verdict: <holds | holds with defects | does not hold>
A. Claims confirmed (file:line or URL+date)   B. Factual corrections
C. Defects, High/Medium/Low: failure path · required fix · the test that fails without the fix
D. Gaps against the house rules and owner answers   E. Cheaper alternatives   F. Unverified
RISKS: one line each
```

### 12.4 Identity brief
```
## Identity: "<two or three words>"
Statement: <audience, context, the combination sentence>
Leak check: <each borrowed motif → the reason our inputs derive it, or "dropped">
Art-direction rules (each testable; they go to DESIGN §2.1): 1. <light/depth, with numbers, or
"no light"> 2. <surface system> 3. <edges/outlines> 4. <shape, e.g. radius as % of unit>
5. <palette structure> 6. <readability floors> [7–8. ...]
Lightings: <one: dark-only | light-only; or two: follow the system> because <...> (DECISIONS #n)
Hero: <what>; proportions in its own height; silhouette test at <size>; its job: <...>
Feel: <3 words>; frequent <...> / rare <...> / the one impact <... or none>; success feels <...>;
  "no" feels <...>; never feels like <...>; signature moment: <...>;
  overshoot <amount | none>, refusal shape <...>, bounce <...>, ambient <amount | none>,
  shake budget <...>, refusal haptic weight <... | none>;
  start values: press <ms>, settle <ms>, ambient ceiling <...>;
  controlled avatar only: latency <ms, on device>, smoothing <none>, hitbox <ratio>, retry <ms>,
  hit-stop <ms | none>
Sound: world <...>; kind <tonal | textural/foley | minimal>; tonal family <... | n/a>;
  success / refusal / impact sound <...>; ladder quiet/medium/loud; synth/recorded/licensed;
  phone-speaker reference; mixes with music <y/n>, obeys silent switch <y/n>, music default <on/off>
Voice: <word budget, tone>; banned words: <names; claims the code does not make true>;
  approved exceptions: <file the copy guard reads>
We will not be: - <never X, because Y>   (5–10 lines)
Edge: <2–4 items>   Reference renders: <files>   Rejected directions and why: <...>
Plan B: trigger <checkpoint fails on any of a, b, c after three looks> → <one money question>
```

### 12.5 Gate 0 message (write it in the owner's language)
```
<Project> is ready to start. Nothing is uploaded unless you ask for that specific upload, and
nothing goes to review or the public before you have tested it on your device and approved.
- What: <one line>. Look and feel: <one sentence> [<render, only if finished>].
- First thing you'll judge: <the gate slice>. I'll ask you one question then: "<feel question>".
- Name: <name> (screening: <verdict>; not legal advice).
- Ids: <ids>, permanent from the first upload. Accounts: <whose, which country>.
- I went ahead on these recommendations; please confirm or change: <ASSUMED items>.
For you (no rush unless marked):
1. <question>. (My recommendation: <X>, because <Y>.)
If you say "start", I begin under the working name; the ids stay provisional until you confirm.
```

## 13. Traps

These cost the most when missed; each came from an incident (T-n: `references/traps.md`).
1. **The brief taken as fact** (a misread genre, a confounded multiplier). *Fix:* §5.1 item 2.
2. **Research recommendations shipped as decisions.** *Fix:* adversarial review first (§6).
3. **Design questions sent to a commissioner.** *Fix:* split the question (§4).
4. **Research waiting for the owner, or a recommendation silently treated as an answer.** *Fix:*
   ASSUMED entries; nothing permanent rests on them (§4, §10; T-17e).
5. **The source game's look or motifs reused as a default.** *Fix:* the leak check (§7.2 step 3).
6. **Gate 0 blocking reversible work.** *Fix:* provisional ids (§10; T-17c).
7. **Programmer art at Gate 0.** *Fix:* a render only if it already reads as finished (T-12).
8. **An empty API response read as "no match".** *Fix:* back off; "not screened" (§5.1; T-157b).
9. **Raw third-party text in a public repo,** or **a report corrected silently.** *Fix:* the
   raw-data rule (§5); an Errata block plus a DECISIONS entry (§6).
