# Monetization and privacy

How to choose how a product earns from the category's evidence, build that model without becoming
what its reviews hate, and make every consent prompt, privacy declaration, analytics event and age
rule true and provable. The ad, Remove Ads and consumable rules shipped through store review in one
free, ad-funded casual game; the subscription, feature-unlock and paid-upfront rules are Proposed.
Every store, ad-network, privacy or legal specific sits in a dated block: re-verify it (§11).

**Read when:** choosing a business model; touching ads, rewarded videos, purchases, subscriptions,
paywalls, consent or the tracking prompt; filling a privacy label or data-safety form; adding
analytics; deciding the audience or answering anything about minors. Release mechanics, store copy,
account deletion and the age-rating questionnaire are in `references/release-and-store.md`.

## Contents
1. Choose the model from evidence
2. Interstitials: one pure policy function (ads only)
3. Showing a full-screen ad safely (ads only)
4. Rewarded videos: opt-in cards that tell the truth (ads only)
5. Purchases: what to sell, entitlements, subscriptions, plumbing (5.6 Entitlement: one pure
   function; 5.7 Subscriptions and paywalls)
6. Consent and the tracking prompt
7. Privacy declarations
8. Analytics and crash reporting
9. Audience and age signals
10. Legal questions and real backends
11. Where to verify volatile facts
12. Checklists

---

## 1. Choose the model from evidence

Whether the product earns money at all is the owner's decision; how it earns is decided from
evidence (`references/kickoff.md` §4). Decide before any money code, record the choice as the first
section of `docs/<slug>/MONETIZATION.md` ("Model") and in DECISIONS, and read only the sections of
this file your model needs.

**1.1 The decision table.** Each row's "demands" column is work you take on in full; a mixed model
takes on every row it mixes.

| Model | Fits when the evidence shows | What it demands | Status here |
|---|---|---|---|
| Ads + a one-time Remove Ads | a free casual product in short units; ad-funded rivals; "wants to pay" among the complaints | §2–§4 in full; consent, tracking prompt, audience and age (§6, §9); the ad SDK's privacy load (§7); buyers never see breaks (§5.4) | Proven: one shipped ad-funded puzzle game |
| One-time unlock | "one-time purchase" praised; extras worth paying for once; no per-user server cost | a complete free core; a list of what the unlock adds and never covers; Restore; §5.6 | Remove Ads proven; feature unlocks Proposed |
| Consumables | natural scarcity (hints, boosts) where more is a convenience | a free path that never runs dry; dedupe; the no-server gap recorded (§5.1); never sell a way past a wall you built | Proven, gap recorded |
| Subscription | ongoing value or ongoing cost (sync, a server, new content, scanning) | §5.7 in full; a receipt-truth decision; often accounts and in-app deletion (`references/domain-apps.md` §8) | Proposed |
| Paid upfront | a premium tool or a known audience; reviews punish in-app purchases | a store page that sells without a trial; no purchase plumbing; a price-tier decision; store-handled refunds | Proposed |
| None | a portfolio, open-source or companion product | the privacy answers (§7) and analytics rules (§8) if any data leaves the device; a "data not collected" claim guarded by a dependency check | — |

**1.2 Code the competitors' reviews into counts before deciding anything.** The method (pull ~500
recent written reviews per app, one regex per theme, read every 1–3★ by hand) is in
`references/kickoff.md` §5.1 (item 4). For money, build three tables: complaints (1–3★), loves
(4–5★), and complaints inside 4–5★. Record incidental facts too ("the level where reviewers say ads
began", "ads started right after the rating prompt", "charged for the year on day one").

**1.3 Turn each count into a rule.** End the report with "design openings" (complaint + count + the
rule it implies) and "traits we must match" (love + count); they become decisions almost 1:1.
- Example (shipped puzzle game): 2,811 reviews, 1,188 negative. Ad frequency 376 (32%), lying "no
  ads" claims 229, trapping ads 187, wants to pay 102, mid-level ads 67, lives 28, no undo 24. Even
  4–5★ reviews held 82 ad-frequency complaints. Reviewers' "ads began at level…" medians were 14–45.
  These counts set every number in §2.
- Example (habit-tracker kickoff, not shipped): in 1,200 coded reviews, subscription, price and
  billing made 130 of 402 negatives, and "one-time purchase" was praised 43 times in 4–5★. That
  kickoff chose a complete free core plus one honest unlock, not another subscription.

**1.4 Rank evidence by design:** randomised long-run > survey > observational > vendor case study. A
long-run field experiment found ad-load sensitivity **3× larger** than a one-month test showed,
driven mainly by ads per hour. A survey found one disruptive ad raises churn 6–7%, and quit rates
**triple** when an ad lands on a reward or end screen. "Rewarded watchers retain 3.5–5× better" is
correlational (engaged players self-select). Review counts show what angers people, not what earns.

**1.5 The proven ad-funded conclusion is one genre's, not a law.** For a free, ad-funded casual
product: money = retention × opt-in rewarded, and interstitials are a late, light supplement. Do the
arithmetic with your own eCPMs, or ~2/3 of published averages (benchmarks are seasonal peaks),
labelled "sanity check only". It supports one conclusion: protect retention before adding load.

**1.6 Research is evidence, not the plan;** an adversarial review sits between them. Example: research
proposed the first interstitial at level 8 / 6 min; the decision became 20 / 8 min.

**1.7 A "Not used" list is a decision too.** Example (shipped puzzle game): banners (layout jumps
mid-task cause wrong taps), app-open ads, rewarded interstitials, lives/energy ("selling a way past
a wall requires first building the wall"), a soft currency, coins to clear a board, "double your
reward". Configure an ad SDK with only the formats you use and test "exactly N formats"; never call
a "test config" helper that enables every format.

**1.8 No currency unless the core loop needs one.** A coin economy is a second game system with its
own balance, farming exploits and copy to keep true. For a calm product, rewards inside the product
(progress, cosmetics, a streak) do the job. Economy design: `references/domain-games.md`.

**1.9 Copy words follow the model.** The banned list is per project: "no ads" and "free" were banned
in the shipped game because they would have been false there. A product with truly no ads, or a
core that is truly free, may say so once the copy checker maps the phrase to code
(`references/release-and-store.md` §5.3).

**1.10 Write `docs/<slug>/MONETIZATION.md` as policy-as-constants:** "Model" first, then only the
sections the model uses, privacy and analytics always; literal numbers, each citing a decision; an
"As built" block per slice; the "Not used" list. Template: `assets/templates/MONETIZATION.md`.

> **Dated facts (as of 2026-10 — re-verify before relying):** an earlier game's own iOS eCPMs were
> rewarded $11.31 vs interstitial $5.62 (2.0×), rewarded = 69% of ad revenue. The US was ~58% of iOS
> game ad revenue (Q2 2026 benchmark). Sanity arithmetic, US iOS player, 3 interstitials + 1
> rewarded per day: ≈ $0.03/day, ≈ $0.15 over 5 active days.

## 2. Interstitials: one pure policy function

Sections 2–4 apply only when the model includes ads. The values are the shipped game's, derived
from its own review counts; yours come from your own evidence. **A run-based game** (Proposed) counts
cadence in cumulative active-play minutes, never in attempts, exempts consecutive short runs and never
shows on a new-best result (`references/domain-games.md` §14.5; `assets/templates/MONETIZATION.md`).

**Shape:** `policy(ask) → Allowed | Refused(reason)`. Every input is explicit (where Next leads,
units completed, active time, wall clock, persisted ledger, in-memory session, purchase flags); no
clock inside; refusals in a **fixed order**, naming the first rule that refuses. "Is an ad loaded?"
and "is the app in the foreground?" are the caller's questions, not policy.

| # | Refusal | Example rule | Why |
|---|---|---|---|
| 1 | daily / special show / campaign end | never before a ritual, an unlock show or the ending | reward-screen ads triple quits; protect the habit |
| 2 | `buyer` | anyone who bought anything | a payer who still sees breaks writes a 1★ |
| 3 | `entitlementUnknown` | the store has not yet said whether Remove Ads is owned | §5.4 |
| 4 | `rewardedThisUnit` | a rewarded video was watched on this board | the user already gave an ad |
| 5 | `tooFewUnits` | < 20 levels cleared | competitors began at 14–45; the free opening sells the game |
| 6 | `tooLittlePlay` | < 8 min total active play | protects fast players |
| 7 | `nearRatingPrompt` | within 3 cleared levels after the rating prompt | "ads started right after the rating prompt" |
| 8 | `unitGap` | < 3 cleared since **any** full-screen ad | rewarded counts too |
| 9 | `timeGap` | < 150 s since any full-screen ad | |
| 10 | `sessionCap` | ≥ 4 this session | |
| 11 | `hourCap` | ≥ 6 in a sliding hour | users respond to ads per hour |

**Definitions are part of the policy;** write them next to the numbers:
- "Level N cleared" = N distinct main levels solved; skips, replays and dailies never count.
- "Total play" = active time on task, capped per board (10 min), paused in background and under a
  rewarded card, so a board left open on the table does not bring the first ad closer.
- "Session" = foreground use not broken by ≥ 30 min away or a process death.
- A ledger stamp > ~1 min in the future counts as "now": a clock that ran ahead holds the gaps for
  their normal length, never until the clock catches up.
- A failed show is not a shown ad.

**Placement:** only after the completion sequence finished or was skipped **and** the user tapped
Next. Never at launch, resume, unit start or mid-task; never on a reward screen, straight after a
rewarded grant, before an unlock show or after the daily.

**Prove it:**
- [ ] One test per rule with **every other rule satisfied**, asserting the doc's literal number.
  Each term of a compound rule ("20 levels AND 8 minutes") gets its own scenario: reviews deleted
  half a compound rule and the suite stayed green until each term had a test.
- [ ] Exactly **one call site** shows an interstitial (the Next of a completed unit). Every other
  surface (start, home, resume, launch, shows) has a test asserting **zero** show calls.
- [ ] The verdict is the handler's first synchronous statement, before any early return or await.
- [ ] A by-finger playthrough, motion on and off, proves the first ad lands where the doc says.
  Example: at 30 s per board, Next on level 20 shows nothing; the first ad waits for 8 min of play.

> **Dated facts (as of 2026-10 — re-verify before relying):** AdMob policy disallows interstitials on
> app load or exit, back-to-back, more than one per two user actions, or unexpectedly during play;
> Google Play disallows ads at level start. Mirror your caps as frequency caps in the network
> console, block sensitive categories, and keep the ads' content ceiling (example: PG) consistent
> with the store age rating (`references/release-and-store.md` §7). Leave the child-directed and
> under-age tags unset for an adult audience; Google has deprecated them (removal expected ~H1 2027).

## 3. Showing a full-screen ad safely

1. **Count the ad when it is handed to the SDK (write-ahead), not when it closes.** `handOff(kind)`
   commits the impression to the save and awaits the write (bounded, 1 s); then show; then
   `settle(handOff, shown:)`. Shown → move the stamp to the close time. Not shown → withdraw it only
   with compare-and-set. The in-memory session counts only ads really shown. The pattern, its
   incident (an impression lost when the app was swiped away under the ad) and its proof (a held
   show, then a fresh container over the last saved document): `references/architecture.md` §4.5.
2. **Bound every wait on the SDK and classify the exit:** `notShown | failed | dismissed | earned`;
   `earned` only if the reward callback fired. Subscribe to the ad's state **before** calling show (a
   failure can arrive inside the call). End the wait on the first return to foreground + 2 s, or at
   a 90 s cap, and then treat it as shown (it was handed over).
   *Why:* the wrapper's `show()` resolved at hand-off, not at close, with no watchdog; a lost dismiss
   would leave a dead Next on a completed board. Reading any exit as "dismissed" counted failures
   as impressions.
3. **No exit while an ad is on its way.** From the tap that commits to an ad until the next screen
   opens, refuse Back (system and on-screen) through the framework's state mechanism, not a plain
   flag. At show time, check **in the screen and in the service** that the app is resumed and this
   screen is the top route. Never defer a skipped ad to "later".
   *Why:* Home pressed during a 570 ms out-transition fired the show while paused (ad-on-resume
   breaks policy). With motion off, a flag set outside the state update left Back live; the ad went
   up over the home screen and the next level never opened. Give fakes a **pre-show gate** so the
   window between ask and present is testable. (Flutter: `references/stack-flutter.md` §14.)
4. **Audio around ads.** Stop loops before a full-screen ad. When the user's sound is off, mute the
   ad just before each show, once it has loaded (SDK init has finished by then). Re-apply your audio
   session after **every** full-screen ad, shown or not, and record on a device what video ads do
   with the silent switch. *Why:* reviewers complain about ads playing through silent mode, and an
   SDK may leave the iOS session in playback, after which your cues ignore the silent switch and stop
   other apps' music. Sound design: `references/motion-and-feel.md`.
5. **Keep the rating prompt and ads apart both ways, with its own counter:** no interstitial within
   N cleared units after the prompt, no prompt within N after an interstitial. Keep
   `lastInterstitialAtUnit` separate from `lastFullScreenAt`. *Why:* a shared counter starved the
   prompt for everyone who used rewarded hints. Call the platform's review request directly at the
   settled moment: an availability pre-check made a slow services call that lost the user's only
   prompt after the turn had been saved (`references/traps.md` T-135a). Nothing may branch on
   whether the prompt appeared (stores do not say), and "asked" is keyed by app version, pinned in a
   test against the build's version.

## 4. Rewarded videos: opt-in cards that tell the truth

1. **A video plays only after an explicit tap ("Watch a video")** on a card that states exactly what
   it gives. Never the word "ad" on the trigger; a play mark is enough.
2. **The trigger is live only when a video is loaded and the caps allow.** Otherwise it is dimmed,
   and a tap opens the card's quiet state with the reason ("No video is ready right now." / "No more
   videos on this level." / "That's all the videos for today.") plus the free path ("Each new day
   brings one more hint."). Derive the offer as rules first, then readiness. "Not ready" is not
   "unavailable" (an SDK can have a quiet period after a video). A marker that opens "no video right
   now" is an advert for nothing.
3. **The card freezes once the user answers.** From the tap on Watch, and from the start of any
   close, it holds what it showed. *Why:* the SDK drops its ready flag as the video goes up; a card
   following live state slid away saying "No video is ready right now" at the moment of the reward.
   The tests passed only because the fake stayed "loaded" through its own show: make fakes drop
   readiness at show and emit a change, like the real SDK.
4. **Pause everything the video would distort.** Stop the task clock and play-time accrual from the
   card's arrival to its departure. *Why:* on iOS a full-screen ad may leave the app "resumed", so
   ad time inflated best times and brought the first interstitial closer; on Android the ad activity
   backgrounds the app, and a naive resume handler restarted the clock mid-video.
5. **Pay on the reward callback, not on display.** Set the in-flight flag **before** the await;
   grant and record before any "is the screen still mounted" check. *Why (earlier game):* a fully
   watched ad paid nothing when its screen was popped mid-video, and skipped the cooldown.
6. **Cap, and keep a free path.** Example: 2 videos per item ever, 30 per calendar day; rewarded
   only at the zero state (a hint at 0 hints) plus a weekly streak-saver (max 2 held); free grants
   without video (3 at start, +1/day).
7. **Scope rules precisely.** "Never mid-task" is about interstitials; a user-initiated rewarded
   card mid-task is allowed. Say so in the decision text, because the literal rule forbade it.
   Offers appear only at calm moments, never during a reveal or a celebration.

## 5. Purchases: what to sell, entitlements, subscriptions, plumbing

### 5.1 What to sell
- **One-time unlock.** Example (shipped puzzle game): a lifetime non-consumable "Remove Ads" that
  removes interstitials only. Rewarded stays: removing it would silently take a feature the payer
  chose. For a feature unlock (Proposed): the free core stays complete, the unlock only adds, and
  the doc lists what it never covers (the user's own data, history, export). Always offer
  **Restore**.
- **Subscriptions to remove ads were resented in that genre** (rivals' $35–70/yr and $6.99/wk
  plans). That is a genre finding about ad removal, not a verdict on subscriptions (§5.7). **No way
  to pay** was itself a top complaint in three competitors.
- **Consumable packs only if you accept the no-server gap:** a corrupt save loses unspent bought
  items. One earlier game refused consumables for this; the shipped game sold them with the gap
  recorded as a decision.
- **Paid upfront (Proposed):** no in-app purchase plumbing, but the store page must sell the product
  without a trial (`references/release-and-store.md` §6), and every claim on it is the whole
  purchase decision.
- Price from the genre's per-unit prices; "Best value" only with a real margin. Example: 10 for
  $1.99 vs 40 for $4.99 is 37.5% cheaper per unit and qualified; a 17% gap did not.
- Product ids are as permanent as the app id; decide them with the owner before the first upload.

### 5.2 Truthful scope and placement
- **The copy says exactly what the purchase gives and what it does not.** Example: "Removes the
  breaks between levels. Optional videos for hints stay." Never "no ads", "ad-free" or "removes all
  ads" when only breaks go; no "bonus", "sale", countdowns or crossed-out prices. One constant, run
  through the project's banned list (`references/release-and-store.md` §5.3). *Why:* 229 counted
  complaints called a "no ads" claim a lie (76 of one competitor's 95 low reviews).
- **List it only once the user has met what it changes** (example: 3 interstitials seen). **Push it
  once:** a card the first time they return to an idle home screen after that; never over the task,
  a results panel or a reward show; never to a buyer. Afterwards it lives only in settings. Bought
  from the card → a "Thanks!" state. Offer-card UI rules: `references/ux-and-accessibility.md` §7.
- **Record the push when it goes up,** so a kill never brings it back: under-offering is the safe side.

### 5.3 Record-at-show vs record-at-answer
For every one-time event, decide when it is recorded by **which failure is harmless**. A lost upsell
is harmless: record at show. A system tracking alert without its primer is a review problem: record
the primer at the **answer** (§6.4). Write the choice in DECISIONS.

### 5.4 Any purchase ends interstitials; "unknown" counts as a buyer
A buyer of **anything** never sees an interstitial. At launch, silently ask the store what the
account owns; refuse interstitials until it answers (`entitlementUnknown`). Re-ask on every resume
and when the purchase sheet opens while unknown. Never move "owned" back within a run.
*Why:* after a reinstall or on a new phone, an owner saw ads until they tapped Restore. Trap: a
parental-controls phone reports "cannot make payments" for good; a gate that stopped there never got
an answer, so that phone never saw an interstitial. Ask something that **can** answer on that device
(on iOS the current-entitlements query needs no permission to pay). Record the accepted gaps: a
store that never answers = no interstitials (lost revenue, the safe side); a consumable-only buyer on
a new device until the cloud copy arrives.

### 5.5 Purchase plumbing (each rule closed a real defect; it applies to every model)
1. **Grant from the purchase stream,** never from the buy call's return; grant a delivery even when
   nothing awaits it.
2. **Save the grant, then finish the transaction** (the write-ahead shape,
   `references/architecture.md` §4.5). Wait for the write's answer, not the commit. A failed save
   leaves the transaction unfinished so the store redelivers it; a failed write is remembered, so an
   unchanged commit after it writes again.
3. **Dedupe by purchase id** (store token or transaction id; keep the last ~32).
4. **Pending grants nothing,** even when a restore labels it otherwise; read the platform's own
   purchase state. *Why:* a slow-card payment, later declined, was granted Remove Ads for good.
5. **A cancel can arrive as a fake purchase with an empty product id.** Treat a cancel or error
   without a product id as the answer to the flow in flight. *Why:* the card froze 10 minutes, then
   said "failed" for a plain cancel.
6. **Bound every call.** Example: 15 s per call, 10 min per purchase, 10 s to finish, 60 s per sync,
   2 s after restore. **Building the service touches no platform channel** (on one platform, merely
   reading the plugin instance connected to the store).
7. **Prices come only from the store's localized strings.** Fakes price in strings nobody would type
   ("5,49 €", "2,29 €") so a hard-coded "$4.99" fails.
8. **Fakes prove the bounds.** A fake that answers at once proves no timeout: give it a hold per
   call. Build fakes in the plugin's own shapes, per platform.
9. **Words are parameters.** Example (earlier game): a reused widget carried a "QA" badge onto the
   only paid control.

> **Dated facts (as of 2026-10 — re-verify before relying):** rules 4 and 5 were seen through the
> Flutter purchase plugin family (StoreKit 2 by default; Play Billing Library 8, "compliant until
> 2027-08-31"); other wrappers may differ. Its exact shapes (the empty-id cancel, pending purchases
> restored as "restored", consume rules per platform, restored transactions with nothing to
> complete): `references/stack-flutter.md` §14. Play refunds a purchase not acknowledged within 3 days
> (license-tester purchases: 3 minutes). App Store product ids can never be changed or reused, and
> the type is fixed once created; the first IAPs are submitted with an app version; the Paid Apps
> Agreement, tax and banking must be active even for sandbox. Play product creation reportedly stays
> locked until an AAB with billing is on a test track. Genre prices (casual puzzle): lifetime unlocks
> at $3.99–4.99 praised; $5.99–9.99 drew "too expensive".

### 5.6 Entitlement: one pure function
§5.4 is the proven instance; generalise it for any unlock or subscription (the general form is
Proposed). One function decides, every gate reads it, and nothing else asks the store.

**Shape:** `entitlement(lastDefinite, storeAnswer, now) → Entitled(until) | NotEntitled | Unknown`,
then derived gates such as `mayShowAds`, `mayPushPaywall`, `mayUsePaidFeature`.
1. **Only a definite store answer moves the state.** A timeout, an error, "cannot make payments" or
   no network gives `Unknown`, never `NotEntitled`.
2. **Cache the last definite answer with its expiry** (for a subscription, the store's expiry plus
   its grace period). Refresh at launch, on every resume and when a paywall or purchase sheet opens;
   bound each refresh (example: a 2 s launch window, 15 s per call). Store dates come from the
   store's transaction, never from the device clock alone.
3. **`Unknown` counts as entitled for every gate that could harm a payer:** no ads, no paywall
   pushed, no paid feature locked, nothing the user made hidden. A paying user locked out on a slow
   store writes the 1★; a non-payer who keeps a feature a little longer costs almost nothing. Record
   that gap as accepted. `Unknown` never triggers a "welcome" celebration or a one-time bonus.
4. **Within a run, `Entitled` moves back only on a definite answer** (expired after grace, refunded,
   revoked), never on a timeout.
5. **What a lapsed user keeps is part of the function:** everything they made stays readable and
   exportable; only paid features lock again.

**Prove it:** a table test per row (cache × answer × now → result and every gate); a property test
over random answer sequences (no `Entitled → NotEntitled` without a definite answer); held fakes for
every bound; the clock moved both ways; fakes for each store state (active, grace, billing retry or
hold, expired, refunded or revoked, pending, no answer) in each platform plugin's own shapes.

### 5.7 Subscriptions and paywalls
> **Status: Proposed.** No source project shipped a subscription. These rules translate the shipped
> purchase, offer and safe-moment rules, two kickoff research runs' review evidence, and store
> policy. Mark the project's choices Proposed until a device test and a review prove them.

Each rule's bold name is a row of the MONETIZATION template's Subscription table
(`assets/templates/MONETIZATION.md`), so the doc is filled rule by rule.

1. **What it sells: define the free floor from complaint evidence, before the paywall.** Code the
   category's reviews for paywall, limit and billing themes (§1.2). The floor keeps the user's own
   data and the core loop: creating, viewing, history, export and account deletion never sit behind
   the paywall. Write it as a table (Action | Limit) with a test per row asserting that no limit
   applies. Example (expense-splitter kickoff): the category leader's free-tier caps and gated
   arithmetic led its recent 1–3★ reviews (paywall or price 17, limits 9, of 56), so recording,
   every split kind, balances and settling stayed free with no count, cooldown or prompt.
2. **Where the paywall may appear, and how often unasked: policy-as-constants,** enumerated like
   interstitial call sites (§2). It appears when the user taps a paid feature or opens it from
   settings, plus at most one unasked offer at a calm moment after demonstrated value (example:
   after use on 7 different days), recorded at show (§5.3). Never at first launch before value,
   never mid-task, never over a success state or a reward, never on resume, never to a subscriber,
   never while entitlement is `Unknown`. Safe-moment mechanics: `references/ux-and-accessibility.md`
   §8. Every other surface has a test asserting zero paywall presentations.
3. **Trial and renewal disclosure, on the screen that holds the button:** the billed price per
   period as the most prominent price; any calculated price ("per month" for a yearly plan) smaller;
   the trial length; the date of the first charge; that it renews until cancelled; how to cancel;
   links to the terms and the privacy policy. Strings come from the store's localized product data.
   Show a trial only to accounts the store says are eligible. *Why:* "charged the full year on day
   one" was a counted billing complaint. Remind before a trial converts: an in-app line in its last
   days, and an opt-in notification.
4. **Restore, manage and cancellation are always reachable:** a Restore row and a "Manage
   subscription" row that opens the store's own management page. Cancelling says plainly what ends
   and when ("Your plan stays on until 12 March"); no guilt screens, no maze, no fake cancel flow of
   your own.
5. **Grace period, billing retry and lapse never punish first.** During the store's grace period
   keep access and show one calm line linking to the store's payment settings. On hold or expiry,
   lock the paid features only; the floor and the user's data stay. Never delete anything on lapse.
6. **A price increase respects existing subscribers.** Never raise a price silently; announce it
   in-app first; a subscriber who declines keeps access to the end of the period they paid for.
   Whether existing subscribers keep their price is a decision for the owner, recorded. Moving a
   paid app to subscriptions never takes away what users already paid for.
7. **The entitlement rule: decide where its truth lives:** the store's signed on-device transactions
   (no server), your server validating with the store's server APIs and notifications, or a
   subscription vendor (a fee or revenue share: the owner's decision). Whichever, the app's gates
   read §5.6.
8. **Group or family entitlement is the owner's decision.** Does one purchase cover a family (the
   store's family sharing), or a shared group in a multi-user app? Record it; the store switch can
   be irreversible.
9. **Periods follow the evidence.** Weekly plans drew resentment in one genre (§5.1). Show each
   period's full price; never default-select the most expensive plan without saying so.
10. **Test with the stores' sandbox renewal clocks:** renew, lapse, grace, hold, restore on a second
    device, refund. Each passing case says what the sandbox could not prove (real billing retries).

> **Dated facts (as of 2026-10 — re-verify before relying):** App Review Guideline 3.1.2: ongoing
> value, a period of at least 7 days, available on all the user's devices; switching an app to
> subscriptions must not take away primary functionality users already paid for; describe what the
> user gets before asking (3.1.2(c)). Apple requires working terms-of-use (EULA) and privacy-policy
> links in the purchase flow and the metadata; reviewers reject paywalls where a free trial or a
> calculated price outshines the billed amount. Introductory offers: one per subscription group per
> account; check eligibility through the store API. Apple: configurable billing grace period,
> billing retry up to 60 days; Play: configurable grace period and account hold. Price increases:
> Apple allows a no-consent increase at most once a year within caps (US$5 and 50% per period;
> US$50 and 50% for yearly), otherwise the subscriber must accept or lapses; Play has its own opt-in
> and notice-only paths. Play's subscriptions policy requires clear price, period, trial and
> cancellation terms and an easy way to manage or cancel. California's automatic-renewal law
> (amended, effective 2025-07-01) requires clear terms, affirmative consent and online cancellation;
> the FTC's federal click-to-cancel rule was vacated in July 2025. Apple's Family Sharing is a
> per-product switch that cannot be turned off once on.

## 6. Consent and the tracking prompt

1. **Exactly one owner of the tracking prompt.** Either the consent SDK drives it (which depends on a
   console setting your build cannot check) or the app does (then the console explainer must be OFF;
   both on asks twice). Prefer the owner your build can verify: client-driven lets the primer meet
   the design bar and be tested with a fake SDK. *Why (earlier game):* a build was rejected because
   the console checkbox was unticked: the label declared tracking and the reviewer never saw a
   prompt. If the SDK drives it, that checkbox goes on the release checklist.
2. **Your own primer:** one screen, **one "Continue" button**, no close, no "Allow", no incentive, no
   picture of the system alert; copy true for every user.
   - Example: title "A quick word about ads"; the body says ads appear between some levels and the
     system will next ask about this device's identifier; it ends "Either answer is fine. The game
     plays the same either way."
   - A **buyer variant** ("offers optional videos for extra hints"). A skeptic caught "shows a short
     ad between some levels" as false for a Remove Ads owner after reinstall, and "you'll see the
     same number of ads" as unkeepable (fill varies).
   - An honest purpose string. Example: "This identifier will be used to deliver personalized ads
     to you. Declining still shows ads, just less relevant ones." Never gate a feature on the answer.
3. **When:** after onboarding (example: after the 4th solved level, ~3 minutes in; never inside the
   tutorial), **never on a cold launch's home screen**, and only at a **safe moment checked at
   presentation time**. The general gate is in `references/ux-and-accessibility.md` §8.
   Consent-specific traps:
   - Consent SDKs **re-run a failed flow on their own timer** (one did every 10 s), so gating only
     the start call let consent UI land mid-task.
   - The form is fetched over the network (0.5–3 s) inside one native call, so a moment checked
     before the call is stale when the form appears. **Hold** the moment (an invisible,
     touch-absorbing overlay hidden from screen readers) until the flow reports its end, max **5 s**.
   - Holds are cancelled on backgrounding and restarted on return. Two presenters can take one
     moment: check and take it in one synchronous step, and re-check after the frame.
   - Remember "privacy options required" across launches, so the settings row exists before
     consent runs this session.
4. **A primer can never hang consent.** It completes on Continue, on its route being removed by any
   means, or on a 10-minute timeout; its route refuses system back. "Not determined after a request"
   means "ask on a later launch", never "denied". At most once a week. Record its date at the
   **answer** (or timeout), never at the push. *Why:* the SDK awaited the primer with no timeout, so
   unrelated navigation replacing its route would have left every ad load waiting for the life of
   the process; recording at push meant a user who killed the app under the primer met the bare
   system alert next launch. Test: replace the primer's route → start completes, request count 1.
5. **Tell the reviewer when the prompt appears** (after play, so they may never reach it): a
   review-notes constant the release verifier prints and cross-checks
   (`references/release-and-store.md` §5.9).
6. **Wire the consent start.** An unwired start looks exactly like "no fill" (earlier game).

> **Dated facts (as of 2026-10 — re-verify before relying):** App Review Guidelines 5.1.1(iv) and
> 5.1.2(i) govern tracking requests and primers. The ATT purpose string is required (the app is
> terminated without it); the request is one-time. iOS 27.0/27.1 can return "not determined"
> without showing the alert for some accounts. iOS 27.2 redesigns ATT in the EU (a full-page sheet in
> DE/FR/IT/PL/RO, re-asked yearly). Google's documented order: consent info update every launch →
> form if required → initialise ads once requests are allowed; for unconsented EEA users UMP shows
> GDPR then ATT. UMP's "consent changed" callback also fires at the end of the first flow. IAB TCF
> v2.3 mandatory since 2026-03-01 (missing disclosed vendors → Limited Ads, error 1.4); US-state
> messages via GPP.

## 7. Privacy declarations

1. **Your privacy manifest declares your code's truth, not the whole app's.** SDKs ship their own.
   Yours says your code does not track, lists no tracking domains, and lists your analytics'
   collected types (not linked) once wired, never before. A guard accepts **exactly the reviewed
   literal shapes**; anything else is a decision, not drift:
   - `(tracking false, domains [])` ships; `(true, [one reviewed measurement domain])` is a reviewed
     fallback.
   - `(true, [])` refused: it came back as **Invalid Binary hours after upload** (earlier game).
   - Any ad-serving domain refused: listed tracking domains are **blocked for every user who declines
     tracking**, so they would get no ads.
   - `(false, [domains])` refused as contradictory; wrong types refused ("a typo is a valid plist
     that declares nothing").

   Type-tag booleans before comparing (in Python `False == 0`, so `<integer>0` passes for
   `<false/>`). One testable module, a fixture per rule, a selftest that fails on an unused fixture;
   run it after each setup edit, on the final tree and on the built app. A string that setup writes
   and the guard requires (the purpose string) is single-sourced from the guard.
2. **The store's privacy label is the union per data type across every SDK.** The form asks "linked?"
   and "used for tracking?" **once per data type**, and purposes add up. Build one table (Data type |
   Linked | Tracking | Purposes | Declared by) in `docs/<slug>/store/PRIVACY_ANSWERS.md`
   (`references/release-and-store.md` §7) from **every** manifest in the built bundle (ads, consent,
   crash, transport, tracking plugin, yours) plus SDKs without one. A type the ad SDK declares
   *linked* cannot be re-entered as *not linked* for analytics. Over-declaring a purpose is allowed;
   under-declaring is not. A **script compares the table with every manifest in the generated tree**
   (linked/tracking at least as strong, every purpose present). Also write "Not collected: answer
   No", "what the product page will show", "without SDK X, what changes". Compare with the IDE's
   privacy report from the signed archive before submitting. *Why:* an early draft omitted the ad
   SDK's not-linked diagnostics.
3. **Data-safety forms follow the store's definitions.** Ad SDK data is collected **and shared**; a
   service provider acting for you (crash, analytics) is collected, not shared. "Optional" = No if
   the user cannot stop it in-app (consent changes personalisation, not collection). With no account
   and no server, the deletion question is No (explain in the policy); with accounts, the deletion
   path and web link are required (`references/release-and-store.md` §7). Data the user's own cloud
   backup holds for them never reaches you, so it is not "collected" (re-read the definition when
   filling). On every legal form, **read back each selection before the commit button**. Example
   (earlier game): a resized window nearly answered "collects no data" for an ad-funded app.
4. **The privacy policy is mapped statement by statement to code.** Each statement has a phrase that
   must appear on the page and a needle in the code (or an `ext:` row for an outside fact such as a
   retention period). The app links to it where users look for privacy (beside ad choices and
   Restore), in the system browser: https only, bounded, never throws, a quiet failure line. **One
   constant holds the URL**; a check fails if any doc names another. **Publishing the page is a
   release blocker**: until then the in-app row opens a 404. Sections (example, ad-funded game): In
   short · Who we are · What stays on the device · Cloud copy · Backup · Ads · Analytics · Crash
   reports · Purchases · Age signals · What we do not do · Children · Legal bases · Retention · Your
   choices · Where processed · Changes · Contact. An app with accounts adds account data, deletion
   and export. If the kinds of data collected change after launch, update the page and notify the
   stores **before** releasing.
5. **Scope backups.** Back up only the save file. Exclude consent strings (a new phone asks again) and
   analytics/installation ids (two phones must never share an analytics identity). Claim backup in
   store text only after verifying it on a device.
6. **app-ads.txt lives at the root of the developer website named in both listings;** one file per
   domain serves every app.

> **Dated facts (as of 2026-10 — re-verify before relying):** Apple has required privacy manifests
> for privacy-impacting SDKs since 2025-02-12; the literal-shape rules above are community practice,
> unverified by Apple. App Review 5.1.1(i) and Play both require an in-app privacy-policy link for
> data-collecting apps. Android Auto Backup covers the whole data dir and **backs up nothing,
> silently, above 25 MB** (ad SDK WebView caches crossed it in an earlier game). app-ads.txt line:
> `google.com, pub-<publisher id>, DIRECT, f08c47fec0942fa0`; crawling takes up to 24 h; new AdMob
> apps serve limited ads until verified (since January 2025). Under a Texas law, a change in the
> kinds of data collected is a "significant change" needing store notice.

## 8. Analytics and crash reporting

1. **A closed vocabulary.** Event names are constants; values are closed (an int in a range, a word
   from a set, a size string); no free text, ids, dates or anything personal. Encode the vendor's
   limits as a rules object with tests. Log from the state layer only (`references/architecture.md`
   §3); never reuse a name the SDK logs itself.
2. **Never log** consent answers, tracking answers, age, revenue (the stores have it) or screen views.
3. **Fix where attempts start and end before any analytics destination exists.** "A wrong first
   funnel is worse than no funnel": every difficulty, retention and conversion reading is built on
   these boundaries.
   - An attempt starts when a unit opens (a level, or a run when control begins; in an app, a core
     flow such as "add an expense") and carries `first` (never completed before) and `replay`
     (opened from a completed state).
     *Why:* three solves of one level (61 s first, 3 s on replay, 4 s reopened) logged identically,
     which would average the level to 23 s. Tune difficulty from first attempts only.
   - It ends exactly once: completed; quit (closed for good without completing, with progress %);
     or backgrounded. Backgrounding is the platform's paused or hidden state, never "inactive",
     which a system sheet, the notification shade or a permission alert also cause. A resume starts
     a new attempt tagged as resumed. (Flutter lifecycle states: `references/stack-flutter.md` §11.)
   - Record opportunities with their outcome, not only impressions ("offered → result", "eligible →
     shown"): a rate needs a denominator. Carry the confounders that change behaviour (purchase
     state, an offered rescue).
   - Buffer events until the SDK is ready; when the buffer is full drop the **newest**, so the launch
     event survives.
   - Example (shipped puzzle game): `level_start` (first, replay) · `level_solve` (time_s ≤ 86400,
     hints, undos, restarts, first, replay) · `level_quit` (progress %) · `rewarded_offered` /
     `rewarded_result`. App translation: `flow_start` · `flow_complete` · `flow_abandon`.
4. **Keep ads and analytics apart.** Analytics never reads the advertising id; the ad consent types
   stay denied on the analytics path (this keeps "our code does not track" true). Analytics storage
   follows consent status: not required → granted; required and unanswered → denied; obtained → left
   to the consent SDK; unknown → untouched. Collect in release builds only.
5. **Test the adapter, not just the port.** Fakes at the seam hide the adapter beneath: run the real
   adapter against a strict stand-in that fails on any unexpected call (analytics granting ad
   storage, collection on in debug).
6. **Register custom dimensions and metrics before launch** (they never backfill): an owner console
   task for the end-of-project list.
7. **Crash reporting** never blocks or throws before the first frame: bound its init, run without it
   when unconfigured. Framework errors are **non-fatal** (filing them as fatal wrecks the crash-free
   figure). Validate the config's shape: a malformed config killed an app natively at launch, where
   no try could catch it. Flutter: `references/stack-flutter.md` §13 (handlers) and §14 (init bound,
   config-shape check).
8. **State what leaves the device before consent** (crash reports with session data and an
   installation id; identifier-free consent-mode pings), name the legal basis you recommend, and put
   the question to the owner (§10). *Why:* gating crash reports on consent would lose every EEA crash
   from the first sessions, the launches most likely to crash.

> **Dated facts (as of 2026-10 — re-verify before relying):** GA4: event names ≤ 40 chars
> `[A-Za-z][A-Za-z0-9_]*`, no reserved prefixes, ≤ 25 params, string values ≤ 100, no booleans (send
> 0/1: the Flutter plugin asserts String-or-number only in debug builds, so a bool reaches the native
> SDK unchecked in release; what it does there is unverified). Custom definitions never backfill;
> default data retention is 2 months; ads personalisation defaults to allowed in all regions (Google
> Signals and ads personalisation are owner settings to turn off). Native consent-mode defaults: all
> four types denied. Crashlytics uploads a crash on the *next* launch.

## 9. Audience and age signals

1. **The audience is a decision slot:** decide it at kickoff from the model and the look, record it,
   and code the store art and copy to it. The content rating says what the content suits; the
   declared target audience says who it is made for. They differ without contradiction.
   - *Adults (18+) target, general-audience content.* Example (shipped puzzle game): ad-funded with a
     cute character, so the target audience was adults only, to stay out of family-program
     obligations, while the content stayed rated for everyone. It kept the character's charm but
     **adult-coded** store art and copy ("logic", "brain game", "for adults", a refined palette, no
     toddler type; the copy guard banned kids/children/toddler/baby/preschool). A **fallback icon and
     first screenshot** (product-led, character out of frame) were ready before launch, and an
     outside viewer judged both: "what kind of app, who is it for?" (One first icon read too young
     and was replaced.) Never add a child age group to "fix" a store flag: it brings the whole family
     policy with it.
   - *Teens and adults:* age signals (rule 2) decide each user's restrictions.
   - *Children or families:* the family programs apply in full (dated block). Choose it only when the
     product is made for children, and plan to the strictest store's rules from the start.

   Icon craft: `references/visual-design.md`. Age-rating questionnaire:
   `references/release-and-store.md` §7.
2. **Age signals: restrict, never store, never time out to "adult".**
   - Ask the platform's age signal once per launch, after the first frame, inside the safe-moment
     hold, and only where the platform says age features apply (a sheet for every adult would be the
     wrong product).
   - Under 18, declined where a law asks, or "verification required" → every ad request
     non-personalised, the network's age-restricted treatment set before SDK init, and **no tracking
     primer or request at all**. Errors, unsupported OS or "not shared" → the adult default.
   - Keep nothing: memory only, never saved, never logged.
   - **Bound each store call, but let the ads wait for the answer with no overall timeout:** a silent
     port then costs one launch without ads, nothing worse. Why a timeout to "adult" is the unsafe
     side (it gave a late-answering minor the tracking request and personalised ads):
     `references/architecture.md` §7.2.
   - Ship a debug-only mock so the owner can run the minor path on a device, proven dead in release
     (`references/release-and-store.md` §1.4).

> **Dated facts (as of 2026-10 — re-verify before relying; laws move monthly):** Texas SB 2420 in
> force, merits appeal pending (verify age through the store signal, use it only for age protection,
> delete it). Brazil's Digital ECA since 2026-03-17 (no profiling-based ads to minors). Louisiana
> 2027-07-01; Utah 2027-05-06; Alabama and California 2027-01-01. COPPA 2025 amendments: compliance
> from 2026-04-22. Apple's Declared Age Range needs iOS 26+, its eligibility check 26.2+ (reported
> unreliable in some regions); Play Age Signals is a beta API. Apple's Kids category forbids
> third-party ads and analytics (permanent once approved); Play Families restricts ads to certified
> non-personalised demand. A cute animated character is an FTC child-directed factor.

## 10. Legal questions and real backends

- **Legal choices go to the owner with a recommendation; never decide them silently.** Give the
  question, the options, what each changes in code and forms, your recommendation and why, and "not
  legal advice; a lawyer decides". Typical: the legal basis for crash reports before consent, the
  data-retention setting, target audience, trademark clearance, data users enter about other people.
  Batch them into the end-of-project list (`references/working-with-the-owner.md`).
- **Test builds must not write to real backends; when they did, say so.** Crash-mapping and symbol
  uploads, error probes, and recordings on a simulator signed in to a cloud account all reach
  production. Gate them (`references/release-and-store.md` §1.5) and tell the owner about any test
  data already in their accounts. Never change account or console settings, log in, or tap a live
  ad yourself: list the exact menu path and value for the owner.

## 11. Where to verify volatile facts

Rules in plain text are durable. Every number about a store, an SDK or a law sits in a dated block.
Before relying on one, re-read the source below and update the date in `docs/<slug>/RESEARCH.md`.
When a re-check proves an earlier entry wrong, supersede it with a new DECISIONS entry; never edit
history. (Example: a state law recorded as "in force 2026-07-01" actually started 2027-07-01, and
another law's injunction status flipped twice in one year.)

| Topic | Verify against |
|---|---|
| Ad placement rules | the ad network's program policies and interstitial guidance; the store's ads policy |
| SDK behaviour (callbacks, readiness, retries) | the **installed** SDK/plugin source in the package cache, cited file:line |
| Purchase and subscription behaviour | each platform implementation of the purchase plugin, read separately; the stores' subscription docs |
| Paywall and subscription rules | the App Review Guidelines (quote the number), Play's payments and subscriptions policies, the law of each sales region |
| Tracking prompt and primers | the platform's interface guidelines and App Review Guidelines (quote the number) |
| Privacy manifests and labels | platform docs, every manifest in the **built** tree, the IDE's privacy report |
| Data-safety forms | the store's help definitions plus each SDK vendor's disclosure page |
| Analytics limits | the analytics vendor's event and parameter limits page |
| Age laws and signals | the statute's status that day (docket, attorney-general page); the platform age API docs |

Treat blogs and SEO articles as unverified. Example (shipped puzzle game): an article claimed the ad
SDK lists tracking domains, and the SDK's own manifest disproved it. A research brief recommended a
purchase flag that the iOS plugin asserts against. Reading the source caught both.

## 12. Checklists

**Model**
- [ ] Model chosen from coded review counts and ranked evidence; MONETIZATION opens with "Model";
  the decision table's "demands" column copied into PLAN; "Not used" list written.
- [ ] Banned words set per project from what would be false here; audience decided and recorded.

**Before any full-screen ad shows**
- [ ] Completion sequence ended or skipped AND the user tapped Next; never launch, resume, unit
  start, mid-task, a reward screen, after a rewarded grant or the daily, before an unlock show.
- [ ] First ad needs BOTH progress and active time; gaps on BOTH axes since ANY full-screen ad;
  session and hourly caps.
- [ ] Never for a buyer of anything; never while entitlement is unknown.
- [ ] Resumed and top route, checked at show time in screen AND service; Back refused while pending.
- [ ] Impression written ahead; compare-and-set withdraw; bounded wait; failure ≠ impression.
- [ ] Rating-prompt margin both ways; review request called directly; muted when sound is off;
  audio session re-applied after.
- [ ] Console caps mirror the code; ads' content ceiling consistent with the age rating.

**Rewarded and purchases**
- [ ] Opt-in card naming what it gives; no "ad" on the trigger; live only when loaded and within
  caps; quiet state says why; frozen from the tap; clock paused; pays on the callback.
- [ ] Grant from the stream; save then finish; dedupe by id; pending grants nothing; empty-id cancel.
- [ ] Every call bounded; construction touches no channel; prices from the store; fakes hold per
  call and use odd locale prices.
- [ ] Restore present; one pure entitlement function; unknown never harms a payer; accepted gaps
  written; offer copy scoped and offered once.

**Subscriptions (Proposed)**
- [ ] Free floor table from complaint evidence, a test per row; data, history, export and deletion
  free; a lapsed user keeps what they made.
- [ ] Paywall call sites enumerated; zero elsewhere; never first launch, mid-task, over a success,
  to a subscriber or while unknown.
- [ ] Billed price most prominent; trial length, first-charge date, renewal, cancel path, terms and
  privacy links on the button's screen; trial shown only to eligible accounts.
- [ ] Restore and Manage rows; grace keeps access; price changes announced; family/group decided.
- [ ] Sandbox renewal, lapse, grace, restore on a second device; dated block re-verified.

**Consent, tracking prompt and age**
- [ ] One prompt owner, console state matching; reviewer note says when it appears.
- [ ] Primer: one Continue; no close/Allow/incentive/alert image; buyer variant; honest purpose string.
- [ ] After onboarding; never cold launch; gate checked at presentation; network form held ≤ 5 s;
  holds restart after background.
- [ ] Primer completes on Continue/removal/timeout; not-determined = later; weekly max; date at answer.
- [ ] Ads wait for the age answer; minor → no tracking request, non-personalised, age treatment;
  nothing about age stored or logged.

**Privacy forms and analytics**
- [ ] Own manifest = own code's truth; literal-shape guard; no ad domains as tracking domains.
- [ ] Label = union per type over every manifest, script-checked; IDE privacy report compared.
- [ ] Data safety per the store's definitions; vendor pages re-read; selections read back.
- [ ] Policy mapped to code; in-app link; one URL constant; published before review.
- [ ] Analytics: attempt boundaries fixed first; closed vocabulary; no PII; first/replay flags;
  opportunities with outcomes; definitions registered before launch.
