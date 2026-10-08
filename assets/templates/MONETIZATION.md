# MONETIZATION — {{PROJECT_NAME}}

<!-- if:monetization -->
This is the money and data policy, written as constants. The evidence is in `research/[TODO: file]`,
and the decisions behind it are DECISIONS #[TODO: n]. **Read before touching money, purchases, ads,
analytics, consent or privacy decisions.**

<!-- flagship-method template (optional doc). Rules and their reasons:
flagship-method references/monetization-and-privacy.md (start with "Choose the model from
evidence"). Every rule in a table here becomes a named constant in the pure core, with one test per
rule that fails without it, using this doc's literal numbers. Store rules, SDK behaviour, privacy
law and prices are volatile: keep them in dated blocks and re-verify.
All three model sections (Ads, Subscription, Purchases) are scaffolded; the Model decides which
stay (see the instruction under the Model table). A product with no money but with analytics or
crash reports keeps the Model ("none"), Not used, and every section from "The SDKs" down. A slot
only a later phase can fill gets one line instead of a guess: "Written in Phase <n.m>; decided so
far: <…>" (references/project-kit.md §12). -->

## Model

| Question | Decision |
|---|---|
| Model | [TODO: ads (with Remove Ads?) / one-time unlock / consumables / subscription / paid upfront / none] |
| Evidence | [TODO: complaint and love counts from research, ranked by design strength] |
| What stays free | [TODO: everything the core needs; a user's own data, history and export are never paywalled] |
| What the money buys | [TODO: exactly what, and what it does NOT do] |
| Decided in | DECISIONS #[TODO: n] |

**Principle:** [TODO: the money model and its evidence in one or two sentences, with numbers.]

<!-- Now delete each model section below that the Model has none of: Ads, Subscription, Purchases.
List each one under "Not used" with the reason. Until you do, the TODO check keeps listing its
markers. -->

## Ads

<!-- Delete this section if the Model has no ads. Never mid-unit, at launch or resume, or on a
reward or success screen; the first one comes late. -->

### Interstitials

<!-- Every slot is written in this product's unit of play: a level, a run, a round or a task. Count
cadence in completed units and active-play minutes, never in attempts (the rules and the shipped
policy function: flagship-method references/monetization-and-privacy.md §2).
Example (shipped puzzle game, unit = level): first after 20 levels cleared and 8 minutes of active
play; then at least 3 levels and 150 s after any full-screen ad, rewarded included; at most 4 a
session and 6 in a sliding hour; only after the completion sequence has ended and the player tapped
Continue.
Example (run-based arcade game, Proposed in a trial design, not shipped; unit = run): first after 6
minutes of cumulative active play; then at least 4 active-play minutes apart, never counted in
attempts; never after two consecutive runs under 20 s; never on a new-best result; only on the
results screen once the player chose to leave or retry.
Example (app, unit = task): only at a natural pause after a completed task; never mid-entry or
between a user and their own data. -->

| Rule | Value |
|---|---|
| Unit of play | [TODO: level / run / round / task, and exactly when one counts as completed] |
| Where | [TODO: only at a natural pause after a completed unit has ended (or been skipped) and the user chose to go on. Never at launch or resume, at the start of a unit, mid-unit, on a reward or success screen, on a new-best result, or straight after a rewarded grant.] |
| First one | [TODO: not before <N units> **and** <M minutes> of active play, whichever comes later; a run-based game counts active-play minutes only] |
| Gap | [TODO: at least <n units> **and** <s seconds> (or <m active-play minutes>) since any full-screen ad, rewarded included; never counted in attempts] |
| Short units | [TODO: e.g. never after two consecutive runs under <s> seconds; or "none: units are long (DECISIONS #n)"] |
| Caps | [TODO: per session; per sliding hour] |
| Never | [TODO: for anyone who bought anything, or while that is unknown; after a rewarded ad in the same unit] |
| Rating prompt | [TODO: when it is asked, and the margin from any full-screen ad, in both directions] |
| Definitions | [TODO: what counts as a completed unit, active play, a session, a shown ad] |

**As built** (slice [TODO: n.m]; DECISIONS #[TODO: n]): [TODO: the pure policy function, its inputs,
its named refusals in order, and the tests. A shown ad is written to the save as it is handed to the
SDK.]

### Rewarded (opt-in only)

| Placement | Reward | Limit |
|---|---|---|
| [TODO: where the offer card appears] | [TODO: exactly what it gives] | [TODO: per item ever; per day] |

The card says exactly what it gives and holds its content from the tap until it closes. The trigger
is live only when a video is loaded and the caps allow it.

## Subscription

<!-- Delete this section if the Model has no subscription. Rules and dated store facts:
flagship-method references/monetization-and-privacy.md §5.6 (entitlement) and §5.7 (subscriptions
and paywalls). -->

**The free floor** (from the complaint evidence; a test per row asserts that no limit applies):

| Action | Limit |
|---|---|
| [TODO: e.g. create, view, history, export, delete the account] | none |

| Rule | Value |
|---|---|
| What it sells | [TODO: the paid features; never the core, a user's own data, history or export] |
| Periods | [TODO: e.g. monthly and yearly] |
| Where the paywall may appear | [TODO: only at a calm moment after the user has seen the value, e.g. on tapping a paid feature. Never on first launch, mid-task, at resume or over a success state.] |
| How often it appears unasked | [TODO: e.g. never; or once, recorded when shown] |
| Trial | [TODO: only with the price, the period and the first charge date on the same screen] |
| Renewal disclosure | [TODO: price, period, auto-renewal and how to cancel, where the user subscribes] |
| Restore and manage | [TODO: where the Restore row and the "Manage subscription" row (the store's own page) live; the answer as one quiet line] |
| Grace period and billing retry | [TODO: what the user keeps while the store retries a failed payment] |
| Price increase | [TODO: how existing subscribers are asked or told, per store rules; what happens if they decline] |
| Cancellation and lapse | [TODO: what a lapsed subscriber keeps (everything they made); the copy says so] |
| Group or family | [TODO: does one purchase unlock for a family or a group? An owner decision.] |
| Where entitlement truth lives | [TODO: the store's signed on-device transactions; your server checking with the store; or a subscription vendor (a fee: an owner decision)] |

**The entitlement rule:** one pure function from the store's answers to entitled / not entitled /
unknown, with a test per case. The cached answer refreshes within [TODO: a bound, e.g. at launch
and on resume, each call bounded]. While the answer is unknown, the user is treated as subscribed
for anything whose loss would harm a payer: a slow store never locks a paying user out.

> **Dated facts (as of {{DATE}} — re-verify before relying):** [TODO: each store's rules on
> subscriptions, trials, price increases and cancellation, by guideline number.]

## Purchases

<!-- Delete this section if the Model sells nothing through the store (it covers one-time unlocks,
consumables and the subscription's products). -->

| Product id (permanent) | Type | Price | Gives |
|---|---|---|---|
| [TODO: id] | [TODO: non-consumable / consumable / auto-renewing subscription] | [TODO: store tier] | [TODO: what it gives, and what it does NOT] |

- Restore purchases: [TODO: where it lives].
- Grant, save, then finish the transaction. A pending purchase grants nothing.
- Prices only from the store's localized strings.
- Every claim about what a purchase gives matches the code exactly ("ad-free" only if every ad goes).

## Not used

<!-- And why, e.g.: banners; app-open ads; a currency; lives or energy; "double your reward";
subscriptions; weekly plans; limits on the free core. -->

- [TODO: each model, format or mechanic not used, and why]

## The SDKs

> **Dated facts (as of {{DATE}} — re-verify before relying):** [TODO: SDK names and exact versions,
> read in source; the file that imports each; console settings that mirror the caps; or "none".]

## Consent and the tracking prompt

[TODO: whether any SDK needs consent or a tracking prompt. If yes: who owns the prompt; the primer
(one Continue, no incentive); when it may appear (a safe moment, never on cold launch); what happens
for minors or unknown age. If no: say so, and name the guard that keeps it true.]

## Analytics, crash reports and privacy decisions

[TODO: what is collected and why, or "nothing", with the guard that keeps that claim true (e.g. a
dependency test that fails if a collecting SDK appears). Where an attempt starts and ends, fixed
before any destination exists: it starts when a unit opens, tagged first or replay, and ends once:
completed, quit (with progress), or backgrounded (paused or hidden, never "inactive"); a resume
starts a new attempt, tagged (flagship-method references/monetization-and-privacy.md §8).]

| Event | When (once) | Parameters (closed values) |
|---|---|---|
| [TODO: event, or "none"] | [TODO: when] | [TODO: parameters] |

<!-- The stores' privacy forms are answered from this section and every SDK's disclosure, checked
against the privacy manifests in the built artefact. Every statement in the privacy policy is
mapped to code. -->
<!-- if:release -->
The answers themselves live in `docs/{{SLUG}}/store/PRIVACY_ANSWERS.md` (RELEASE).
<!-- /if:release -->

## Audience, age and backup

[TODO: the audience and rating choice, and why (an ad-funded product with a friendly character
needs this decided early); how age signals are mapped; what restricted users get; what is stored
about age (ideally nothing); a timeout never falls back to "adult". The fallback store art (icon
and first screenshot) if an outside viewer reads the audience differently. Backup: what the
platform backs up (the save only) and how a reinstall restores progress and purchases.]

## Listing decisions

[TODO: this project's banned-word list for every surface (or where it lives), each word with its
reason; the claims policy; the name and keyword strategy.]
<!-- if:release -->
The store texts, the claim table and the length table live in `docs/{{SLUG}}/store/` (RELEASE §8).
<!-- /if:release -->

## Arithmetic (a sanity check only)

[TODO: revenue per active user from your own measured numbers if you have any, otherwise about 2/3
of benchmark averages; or "no money". End with what protects retention.]
<!-- /if:monetization -->
