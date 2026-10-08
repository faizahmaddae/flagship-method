# Working with the owner

How to split decisions with the person who commissions and approves the work: what they keep, how
to ask, how to report, where permission stops, and how to hand back everything only they can do.
The aim is an owner who intervenes rarely, never loses control of anything irreversible, and is
never surprised.

**Read when:** before any message to the owner; when an answer has not arrived; before any
download, purchase, login, account or console action; when the owner overrides you, interrupts you,
reports a bug, or asks "is it worth it?"; at every milestone; when preparing the device-check and
END-OF-PROJECT lists. Owner profiling and the first questions are in `references/kickoff.md` §3–4.

## Contents
1. Decision rights · 2. How to ask, and answers that have not arrived · 3. Message tiers · 4. Gates,
from the owner's side · 5. When to ask: the timing table · 6. Overrides and "is it worth it?" ·
7. What you cannot perceive: judging tools and fallbacks · 8. The owner's own tools · 9. Permission
boundaries · 10. Mistakes, side effects, interrupts and reported bugs · 11. Memory notes and
standing preferences · 12. The device-check list · 13. The END-OF-PROJECT list · 14. Templates ·
15. Traps

---

## 1. Decision rights

**The method carries the work; the owner steps in only where the decision is theirs.** Example
(shipped puzzle game): the owner sent about a dozen short messages over two-plus days for a complete
product. Those were "start", the gate answers, two file downloads, a verdict on the sounds, their
own ad package plus one hard requirement, one account authorisation, and "what's left?". Every other
choice, about 120 of them, was decided from evidence and recorded.

| Area | The owner keeps | The builder decides (from evidence, recorded in DECISIONS) |
|---|---|---|
| Irreversible public steps | any upload, test tracks included, only on their explicit request for that upload; submission for review, publishing, production deploys and public posts only after their own device test and explicit approval | everything up to the lever: release prep, verified builds, store copy, screenshots, review notes |
| Money | every purchase, paid asset, hire or subscription (a yes per exact item and price) | researched shortlists with costs and licences; "nothing bought yet" |
| Accounts | creating accounts, accepting terms, agreements, tax, bank, account-level settings, logins | console work inside an explicit, named authorisation (§9) |
| Legal identity | developer name and the country the accounts are held in, support email, policy contact, trademark filing, domains, age-rating answers | drafts, research and a recommendation for each; eligibility facts (§9 item 9) |
| Keys and secrets | signing keys, certificates, passwords, production ids | never creates or commits them; ships a gitignored template |
| Product scope | platforms, features in or out, whether ads or a tracking prompt exist, hard requirements | a recommendation with evidence; builds any override to the full bar (§6) |
| Device feel | how the finished thing feels in the hand and sounds to the ear | everything measurable; judging tools for the rest (§7) |
| Everything else | — | design, UX, motion, sound design, copy (truth-checked), architecture, libraries, content, difficulty, ad cadence within policy, test strategy, order of work |

Developer-owners may co-decide engineering or other domains. Use the per-domain matrix from
`references/kickoff.md` §3, and keep it recorded. Delegate decisions explicitly into every agent
brief ("decide X; record it in DECISIONS with reasoning"), and make every builder report list its
decisions so the lead can log them (`references/orchestration.md`). Example: the night launch image,
whether to push the remove-ads offer, a replayed level's ad behaviour and hint-pack sizes were all
decided by agents from evidence and recorded. None of them was asked.

## 2. How to ask, and answers that have not arrived

**Before asking anything:**
- [ ] Does research, the genre or the design doc already answer it? Then decide, record it, and
      continue. Split mixed questions (`references/kickoff.md` §4).
- [ ] Is it owner-only by §1? If not, decide.
- [ ] Is now the moment it is needed (§5)? If you are asking early, mark it "no rush, nothing is
      blocked".
- [ ] Have you batched every question for this moment into one message?

**Shape of every question:** the owner's language, numbered, one line each, ending "(My
recommendation: X, because Y.)"; jargon explained inline ("ATT, the iPhone 'allow tracking'
window"); permanence flagged ("this id can't change after the first upload"); what you do on each
branch ("if you prefer that one, tell me and I'll download that single file"). Make each item
decidable at a glance (yes/no, an amount, pick one). Why: the owner answered a five-item list in one
line ("1. yes 2. later 3. … 5. yes, go for it"), and that only works when every item can be answered
in a word.

**Money questions** shrink to one money question with a researched number ("May we hire an animator
for the character? About $X, quote from <source>."). Never phrase one as a design question.

**Taste questions** go with a finished sample: a render, a sound, a sentence. Never send a
commissioner a list of design options.

**Every number you tell the owner is computed or traced.** Example: "best value" on a pack was
checked before it shipped (12.5¢ against 19.9¢ per hint).

**Answers that have not arrived: ASSUMED.** Questions never block work. When an answer lags, or
the owner cannot be reached, adopt the recommendation you sent:
1. Record it in DECISIONS with status **ASSUMED**, quoting the question and the recommendation, and
   list it in PROGRESS's ASSUMED answers table (under "Open questions").
2. Build on it, but **nothing permanent may rest on an ASSUMED answer:** no store record, bundle or
   package id, product id, paid vendor, published text, or account created in anyone's name.
3. When the real answer arrives, add a new entry that confirms or supersedes the ASSUMED one, and
   re-check the decisions that cited it. Never edit the ASSUMED entry itself.
4. Gate 0 is the point where every ASSUMED answer on a permanent thing must be confirmed
   (`references/kickoff.md` §10).

## 3. Message tiers

**Status beats** go out between milestones. Each is one line: what just finished, with its evidence,
and the next action. Examples: "Green: 149 tests. Now looking at the renders myself (look 1)."
"Look 1: good overall; fault: the panel straddles the background horizon. Fixing." "Fresh data
container: the launch tool reinstalled the app, so the code lost no data." The owner can follow from
a phone without reading code.

**Milestone updates** go out at each committed slice, in plain, user-facing words (shape: §14.3):
what is committed (hash, test count, analyzer state); what changed for the user; the review (N real
problems found and fixed, the one to three that matter); what is still unchecked (needs a device or
an ear) and why; side effects on the owner's accounts; what is running now; questions; the gate
reassurance. Example review line: "Review: 10 real problems, all fixed. Two were serious, both on
Android: cancelling a purchase could freeze the card for 10 minutes, and unpaid 'pending' purchases
could be granted."

**Language:** questions, decisions, milestone updates and anything the owner must act on go in the
owner's language. Terse technical beats may stay in the working language if the owner reads it.
Keep technical identifiers (ids, file names, commands) verbatim.

## 4. Gates, from the owner's side

Phases and gate scheduling live in `references/planning-and-slices.md`. This section covers how the
gates meet the owner.

1. **Never show the owner programmer art**, not even in an internal test build. Run a polish pass
   before any build they touch: a real icon, a launch screen matching the first frame, no default
   fonts, dialogs, placeholder text or a white or black flash. Why: the owner had rejected a
   previous project on output quality, and a rough build anchors judgement low. Example: the first
   device build reached the owner only after a dedicated pass drew the icon with the product's own
   character renderer (plus a fallback icon) and matched the launch screen to the first frame. The
   tells are in `references/visual-design.md` ("The quality bar: seven questions and two edge
   checks", and the failure catalogue).
2. **Gate the first owner-facing build with one feel question**, never a checklist. Its wording
   depends on how the product is used (a game, a daily-use app, an episodic tool) and lives in
   `references/planning-and-slices.md` §3. Ask the practical prerequisites as a separate short list
   before the build. If the answer is no, ask what felt wrong, in their words; record it in
   DECISIONS; fix it; re-gate.
3. **Deliver the gate build by a non-public route by default:** a cable or developer install on the
   owner's phone, a locally built package they install, or a simulator recording if they have no
   device. **Any upload, an internal test track included, happens only when the owner explicitly
   asks for that specific upload.** Submission for review or to the public waits for their device
   test and explicit approval.
4. **Never present the release lever as the next step.** Example: a gate message ended with "once
   the icon and launch screen are ready, whenever you say, I'll build and upload". The owner
   corrected it: no upload until the game had been really tested and they approved. Write release
   steps as "when you approve: …", each paired with a non-public route ("I can install it on your
   phone by cable; that is not an upload").
5. **Record a release gate in three places:** the decision log, the progress handoff and a standing
   preference (§11). Put "do NOT upload, publish, push or contact any store or console" in every
   agent brief. Tell the owner the rule in one sentence, word for word everywhere (milestone
   updates, the gate message, the END-OF-PROJECT list), translated once into their language and
   then reused: **"Nothing is uploaded unless you ask for that specific upload, and nothing goes to
   review or the public before you have tested it on your device and approved."** A looser form
   ("nothing until you approve") is wrong both ways: it rules out a test-track upload the owner may
   ask for, and it implies that approval unlocks every later upload.
6. **Owner instructions supersede the plan.** Record each one as a new decision, and note which plan
   rules it relaxes. Example: "no upload before approval" replaced the plan's "nothing in Phase 3
   before a yes", because the owner wanted progress without exposure. If the owner prefers to do
   all device testing at the end, that is such an instruction: record it, keep building, and hold
   the gate questions for that session.
7. **Don't push hands-on chores early.** Offer the gate build once, by its route; never chase the
   owner to plug in a phone, create keys or run sandbox purchases. Collect those chores into the
   device-check list (§12) and the END-OF-PROJECT list (§13).

## 5. When to ask: the timing table

Schedule questions for when their answers are needed. Ask early, marked non-blocking, whenever the
answer is slow: accounts, purchases, legal steps, anything the owner must do by hand. Keep the table
in `PROGRESS.md`, check the next row before each phase, and batch that row into one message.
Example: the money-phase questions (tracking prompt yes/no, ad networks, who makes the signing key
and tests) went out while the previous slice was still building, marked "no rush, nothing is blocked
right now". The answers arrived before the phase started.

| When | Ask the owner |
|---|---|
| Kickoff, first block | owner-only items, including the country and the name the store accounts will be held in (slow and permanent) |
| Gate 0 | go; scope; name and ids (provisional is fine); confirm every ASSUMED answer on a permanent thing; who holds the release lever |
| Before the first device build (the feel gate) | which phone, and whether a cable or developer install on it is possible (the default route); confirm the name and permanent ids before any store record or upload; the store record early, because it is slow; a test group only if they want delivery by a test track |
| Start of the money phase | ads yes/no; tracking prompt yes/no; ad networks; who makes keys and tests on device |
| Only if a checkpoint fails | one money question with a researched quote |
| When a perception limit bites (§7) | judge this with the tool I built |
| End of project | the END-OF-PROJECT list, once (§13) |

## 6. Overrides and "is it worth it?"

**Accept an override, record it, and build it to the full bar.** Recommend clearly once. When the
owner overrides you on product scope, write "Owner decided X (date)" in DECISIONS. The next brief
treats it as a requirement, not an open question, and nobody relitigates it. Example: the builder
recommended "no tracking prompt for now" (a simpler privacy label, no early interruption, an
unproven revenue effect). The owner answered "we must have it". The next slices built a full flow:
a custom explainer screen, safe-moment gating, a backstop timer, review-notes text and policy tests.
None of it carried any further pushback.

**Answer "is it worth it?" in five parts:** the cost; the benefits, ranked; what it is *not* needed
for; its priority; a one-line verdict (§14.5). Write the answer in the owner's language, and record
it in DECISIONS. Example (registering the product's domain): the cost was small and yearly. The main
benefit was brand protection; the others were a professional support address and a landing page
later. It was not needed for the privacy page, which could live on the owner's existing site, or for
the ad-network verification file, which must sit on the developer site registered in the stores.
Verdict: "low priority, low cost: register it."

> **Dated facts (as of 2026-10 — re-verify before relying):** a .app-style domain cost about $15–20
> a year. The ad network's app-ads.txt had to be served from the developer website listed in the
> store records, not from a product domain.

## 7. What you cannot perceive: judging tools and fallbacks

**Name the limit in one sentence** ("I can't hear, so 'weak or not' needs a human ear"). Typical
limits: sound through a phone speaker; real-device touch latency and haptics; frame timing on real
hardware; whether art reads as childish to a stranger; naturalness in the owner's native language.
Measure the proxies you can (spectra through a phone-speaker high-pass, frame-budget tests,
filmstrips: `references/motion-and-feel.md`, `references/performance.md`). Never present a proxy as
the human verdict.

**Build the owner the smallest judging tool that records verdicts you can read back.** Example: a
private listening page with every cue grouped by product moment, buttons that play sequences (the
melody built over a level), Good/Weak plus a note per cue, an overall verdict, the instruction
"listen once on the phone speaker, once with headphones", and verdicts saved where the builder could
read them. When you change an item, add an A/B row. A re-processed sound came out about 3 dB louder
on a phone speaker than the first version, so the owner picked between them. For visual "does it
read as childish?" questions, give an outsider a written scorecard. For feel, use the device-check
list (§12).

**Research a licensed fallback in parallel, and buy nothing until the owner has judged.** The
shortlist has tiers (best value, biggest single upgrade, premium) with costs, licence terms checked
(worldwide commercial use in apps, one-time, no attribution), an "avoid" list with reasons, and the
honest note "nobody has listened to these". Example: the owner said the product "must not look weak
because of sound" and offered to buy packs. The page and a costed shortlist went out together. The
owner judged the set "not bad, suitable", so nothing was bought. The research stayed as the
documented fallback, and "re-judge on a real device" went onto the device list.

## 8. The owner's own tools

Evaluate a package or tool the owner offers as rigorously as a third-party one: read its source; run
its tests in a temporary copy; diff the published version against the owner's local source; check
transitive imports of big UI kits and dependency conflicts against your lockfile; read a sister
project's integration and its hard-won traps; check current platform facts; then have skeptics
attack the verdict. Write gaps up as an upstream request doc: a table (number, request, why,
workaround), then one section per request with file:line evidence and "once this lands, delete X".
Ship a contained one-file workaround for each gap. Never edit or publish the owner's package, and
ask before suggesting they release a new version.

Example (shipped puzzle game): four readers (the package with its 573 tests, the sister app's
integration, the project's rules, platform facts) fed a designer, and then two skeptics attacked the
result. The verdict was "suitable", yet the skeptics found three real defects in the *integration
plan*, none needing a package change: an explainer route could be removed and block ads for the
whole session; a system prompt could appear mid-task; an interstitial could fire while the app was
backgrounding. Eight upstream requests were written; none blocked shipping.

## 9. Permission boundaries

1. **Never log in, enter passwords or create accounts on third-party sites.** When a needed file
   sits behind a login, give the owner a table (purpose, file, link, size, licence) with a
   recommendation and a no-login alternative, stating its weakness. Process the file once they drop
   it locally: pin its sha256, keep it byte for byte as a source, and log its licence. Example: two
   CC0 recordings needed a login, so the owner downloaded them. The no-login alternative was weaker
   (it covered only one of the two sounds needed).
2. **Downloads:** show the name, source and size, and wait for a yes.
3. **Purchases:** get a yes for the exact item and price, even after the owner has said "I'll buy".
4. **Secrets and ids:** production ids and secrets never enter git. They live in a gitignored env
   file read line by line (never `source`d), beside a committed `.example` with the vendor's sample
   ids, and release verification refuses sample ids (`references/release-and-store.md`). Never
   create signing keys or certificates. Never commit fake config; exercise "config present" paths
   only in an isolated copy. Once real config exists, never touch it.
5. **Use broad account authorisation narrowly.** "Do all of it yourself, with the CLI or my browser"
   is not a blank cheque. List the existing projects and follow their naming and structure; reuse
   existing accounts (no new accounts, no new terms); act only on what was authorised; close the
   tabs you used; report what you "created / linked / downloaded / closed"; check results against a
   known-good sister project and verify end to end (events arriving in the vendor's debug view).
   Hold back any change that would disturb a running workflow (real config was held aside while a
   run was testing the no-config path).
6. **Stop at account-level settings.** If a step changes account-wide settings, or the permission
   system stops it, close without applying and leave nothing half-done. Give the owner the exact
   click path, and add "or tell me explicitly and I'll do it". Example: turning off an analytics
   property's ads-personalisation setting was blocked. The editor was closed unapplied, and the
   owner got "Admin → Data collection → … → Apply".
7. **Agents never commit, upload, publish, push or touch consoles.** The lead commits after its own
   verification. Only the owner uploads, or the lead on the owner's explicit request for that
   specific upload (`references/orchestration.md`).
8. **Competitor material is for internal comparison only.** Screenshots and icons may sit in scratch
   for side-by-side judging. They never enter the repo, the store assets or committed sheets. Raw
   review text follows the raw-data rule (`references/project-kit.md` §11).
9. **Region and eligibility are compliance facts.** Whether the owner can hold developer accounts
   and receive payouts in a store, whether sanctions or export rules touch the owner, the users or a
   service the product needs, and which local stores matter: research these with sources (dated,
   re-verified), and ask the owner in which country and in whose name the accounts will be held. The
   decision is the owner's, made with the program's terms and a qualified adviser where sanctions
   apply. Never suggest a way around eligibility or sanctions rules (another person's account or
   identity, a borrowed address, a masked location). Method: `references/kickoff.md` §5.5.

## 10. Mistakes, side effects, interrupts and reported bugs

**Report your own mistakes at once, in plain words:** what happened, what you did, and the blast
radius. Example: "I made a mistake: I passed a placeholder instead of lane C's report into the
relaunched workflow. I stopped it within a minute, before it changed anything, and relaunched it
with the file path."

**Report a plan correction** in one sentence of cause and one of replacement, and record it in
DECISIONS. Example: "Profile mode doesn't exist on the simulator, so frame timing moves to a device
log on your phone."

**Disclose side effects on real systems.** Whenever a workflow touched real services, add a "Side
effects on your accounts" line to the milestone update. Example: two deliberate probe crash reports
in the real crash project ("please ignore them"); symbol files uploaded by early test builds (since
gated to builds signed with the real key); a test save possibly left in the owner's cloud account.
Gate test builds so they never upload release artefacts.

**On an interrupt: stop, report the exact state, ask** (§14.6): what finished, what may have been
halted (and that you have not checked yet), what is uncommitted, the last commit hash, then "What
would you like to do?" Never resume on a guess. After "continue", establish the facts first: which
runs completed, where the others stopped, what partial work is in the tree, which notices are stale.
Resume with a finisher, not a rerun (`references/orchestration.md`). Tell the owner: "Nothing was
lost: the finished work is in the tree and the last commit is still <hash>." Then list what resumes
and what will not be redone.

**When the owner fears they broke something,** answer from their evidence (often a screenshot) in
four parts: what is running; what the item they saw actually was; why nothing is lost (verification
runs afterwards; runs can resume); the one control that *would* stop the work. Example: "The
'Finished' item was a small command an agent ran itself; its status is 'Completed'. Just don't press
the square button next to the main task; that stops the whole workflow, and even then it resumes
from that point."

**When the owner reports a bug from a photo or a short message, reproduce before you fix.** Never
fix on a guess.
1. **Reproduce it** on the build flavour and device class they used. Six investigators once agreed
   with high confidence on the cause of a store rejection and were wrong; one release build on a
   simulator settled it (`references/verification.md` §Cold launch).
2. **Separate tool behaviour from app behaviour** with a controlled variant. A path that missed its
   last cell on a simulator was the tool's lift-off injection, not the app; an apparently lost save
   was a launch tool reinstalling into a fresh data container (`references/traps.md` §Tooling).
3. **When two complaints arrive together, the specific one is usually the real one.** Example (sort
   game): "everything is too big" came with "the hint card won't go away". The card, dismissed only
   by a move and a quarter of a narrow screen tall, was the defect. A text-scale theory matched the
   photo but not the fact that a restart fixed it: the one-time card had been consumed.
4. **A render that resembles the photo is a hypothesis, not a diagnosis.** Ask what else changed
   between the two runs, and measure before blaming the visible code: an empty band blamed on
   layout code was, after 15 minutes of rect measurement, a fixed-height slot reserved for a note
   that could not appear after level 5.
5. **Fix the diagnosis, not the symptom,** with a guard that fails without the fix. Then reply in
   one message: what you reproduced, the cause, the fix and its guard, or "not reproduced yet; I
   need <the one thing>".

## 11. Memory notes and standing preferences

When the owner states a standing preference or boundary, record it in the "Standing owner
preferences" section of `PROGRESS.md` (and in the builder skill where it constrains building): the
rule, **Why:** (the owner's reason and the date) and **How to apply:** (what to do and not do). Also
save it as a memory note (template §14.9, with a one-line index) **only when the session's memory
belongs to this project.** A session launched from another repository, or a subagent, may carry
another project's memory; writing there files this owner's facts under the wrong project. Record
gates and authorisations in DECISIONS too. Worth recording: the release gate; the owner's language;
their own packages and how to treat them; the decision-rights matrix; permanent bans; every
authorisation granted (scope, date) and where you were rightly stopped.

Example (sanitised): "No upload unless the owner asks for that specific upload, and nothing to
review or the public before they have tested on a real device and explicitly approved. The owner
creates the signing key and does device testing themselves, at the end. **Why:** they want to test
the real product before anything reaches a store, and the key's password is theirs. **How to
apply:** do all other work, including release prep, but never upload unasked, never create the
key, and don't push them to plug in their phone early. Gather the device checks into a list they
can run at the end."

## 12. The device-check list

Every slice ends by listing what could not be verified without a real device or human senses ("Still
unchecked" in the milestone update). Collect these into one list in the "Device checks" section of
`PROGRESS.md`, grouped: core feel and the signature moment, haptics, touch latency; sound on the
speaker and on headphones; permission and consent prompts and when they appear; test ads (none
before the first-ad threshold, none at forbidden moments); sandbox purchases (each product, restore,
reinstall); sync between two devices; share, screen reader, a launch in every lighting the product
ships; every script direction and calendar the product supports; a frame log on a low-tier device.
Write each item so it can be run as written: steps, the expected result, and what a failure looks
like. Attach the release doc's "what this does not prove" (`references/release-and-store.md`).

## 13. The END-OF-PROJECT list

Keep one living list in `PROGRESS.md`, headed "END-OF-PROJECT LIST FOR <owner>". It holds every
account, store, legal, money and signing action only the owner can do. Add to it slice by slice.
Present it **once, at the end**, in the owner's language, grouped, with a recommendation on each
item. It lives in the repo so it survives sessions, and the store docs folder (`docs/<slug>/store/`,
created in Phase 5) links to it. The release and money items it usually needs are listed in
`references/release-and-store.md` §0 item 5.

**Shape (template §14.8):**
1. *Device testing first*, the most important group: it carries the "Device checks" list (§12).
2. *Decisions*, each with a recommendation and its consequence: the age-rating answer and why; the
   support email and developer name for the privacy policy ("until you publish it, the in-app link
   shows a 404"); legal defaults ("keep both as they are"); an outsider check of the icon, with the
   fallback icon if it reads as childish.
3. *Accounts and consoles*: each item gives the exact console path, ids and values, the file to edit
   and the command to run afterwards. The group ends with the release build per `RELEASE.md`.

**Order constraints:** say which item must come first; the owner's device test always precedes any
submission. **Fallbacks:** each item that can fail names its fallback. Close with the next step you
recommend ("device testing first"), the offer ("I can do <console items> in the browser if you
name each one explicitly. Agreements, tax and bank details are yours."), and last, the upload
sentence (§4 item 5), word for word: "Nothing is uploaded unless you ask for that specific upload,
and nothing goes to review or the public before you have tested it on your device and approved."

> **Dated facts (as of 2026-10 — re-verify before relying):** typical order constraints on the two
> big mobile stores:
> - agreements, tax and bank must be complete before paid products can be tested or sold;
> - products must exist with their exact ids before sandbox purchase tests;
> - capabilities must be enabled in the developer portal before the provisioning profile and the
>   release build;
> - the privacy policy must be live before review;
> - ad-network apps and units must be created, and their ids put in the gitignored env, before the
>   release build;
> - the signing key must exist before the release build.

## 14. Templates

Write every template in the owner's language. They are shown here in English.

### 14.1 Question block
```
For <owner> (no rush; nothing is blocked right now):
1. <Question, one line>. <Why it matters / "permanent after the first upload">.
   (My recommendation: <X>, because <Y>.)
2. <Action only you can do>: <exact place>, <exact values>. <What I do after you do it.>
3. May I <download/buy> <exact item: name, source, size or price>? (My recommendation: yes/no)
Until you answer, I'll go ahead on my recommendations; nothing permanent will depend on them.
```

### 14.2 Status beat
```
<Finished thing>: <evidence, e.g. "green: N tests" / "look 2: <fault> fixed">. Next: <action>.
```

### 14.3 Milestone update
```
<Slice> is committed (<hash>). <N> tests pass, analyze is clean. Nothing has been uploaded.
- <What changed for the user, plain words, 3–6 bullets>
- Review: <N> real problems, all fixed. The main ones: <1–2 lines>.
Still unchecked (needs a real device / your ear): <items, why>.
Side effects on your accounts: <if any; how to treat them>.
Running now: <next work, 3–6 bullets>.
For you: <question block, or "nothing needed">.
Nothing is uploaded unless you ask for that specific upload, and nothing goes to review or the
public before you have tested it on your device and approved.
```

### 14.4 First owner gate
```
Before the build (one short list): 1. <prerequisite> (My recommendation: …) 2. …
The build: <the non-public route, e.g. a direct install on your phone>.
  Nothing is uploaded unless you ask for that specific upload, and nothing goes to review or the
  public before you have tested it on your device and approved.
One question after you use it: "<the gate question for this product type
  (references/planning-and-slices.md §3)>"
If not, tell me in your own words what felt wrong; I'll record it, fix it, and send it again.
```

### 14.5 "Is it worth it?"
```
Cost: <money/time>. Benefits: 1. <main> 2. <...>. Not needed for: <...>.
Priority: <low/medium/high, urgent or not>. Verdict: <one line>.
```

### 14.6 Interrupt report
```
Stopped. Finished: <...>. Possibly halted (not yet checked): <...>.
Uncommitted: <... / nothing since <hash>>. What would you like to do?
```

### 14.7 Login-gated file request
```
| Use | File | Source (link) | Size | Licence |
My recommendation: download these and tell me. No-login alternative: <...> (weaker: <why>).
```

### 14.8 END-OF-PROJECT list (in PROGRESS; presented once)
```
## END-OF-PROJECT LIST FOR <OWNER> (when they judge it ready; nothing before)
Ask in <language>, at the end, in one go. The upload rule is decision #N.
1. Device testing (most important): <the "Device checks" list, runnable as written>
2. Decisions (each with my recommendation and consequence): <age rating>, <policy contact/name>,
   <legal defaults>, <icon outsider check → fallback>
3. Accounts and consoles (exact path · ids/values · file to edit · command after; order noted):
   <ad network apps/units → env file>, <console settings>, <ads verification file>,
   <agreements/tax/bank>, <products: exact ids, types, prices>, <portal capabilities>,
   <analytics links/settings>, <blocked settings with click paths>, <signing key>,
   <release build per RELEASE.md>
Next step I recommend: <device testing first>.
Offer: I can do <console items> in the browser if you name each one.
Agreements, tax and bank are yours.
Nothing is uploaded unless you ask for that specific upload, and nothing goes to review or the
public before you have tested it on your device and approved.
```

### 14.9 Memory note
```
---
name: <slug>
description: <one line>
metadata: { type: feedback | reference, modified: <date> }
---
<The rule or fact.>
**Why:** <owner's reason, date>.
**How to apply:** <do / don't>. Related: [[other-note]].
```

## 15. Traps

T-n numbers are entries in `references/traps.md`.
1. **Phrasing the publish step as the default continuation.** The owner had to correct it. *Fix:*
   "when you approve: …", a non-public test route, and the upload sentence word for word (§4;
   T-10).
2. **Asking what research could answer, or handing a commissioner design choices.** *Fix:* the
   before-asking checklist (§2; T-11).
3. **Questions asked the moment they block.** Slow answers then stall the work. *Fix:* the timing
   table; ask early, marked non-blocking (§5).
4. **Something permanent built on an ASSUMED answer** (an id, a store record, a paid vendor).
   *Fix:* ASSUMED entries never carry permanent things; confirm them at Gate 0 (§2; T-17e).
5. **Relitigating an override.** *Fix:* record "Owner decided X (date)"; build it to the bar (§6).
6. **Presenting a proxy as the human verdict** ("the sounds are fine" from a spectrogram). *Fix:* a
   judging tool, plus a device-list item (§7; T-13).
7. **Buying before the owner has judged the free option.** *Fix:* research the fallback; buy only on
   a yes to the exact item (§7, §9; T-15).
8. **Editing or publishing the owner's package.** *Fix:* upstream requests and local workarounds
   (§8; T-16).
9. **A blocked account-setting change left half-applied.** *Fix:* close it unapplied; hand over the
   click path (§9; T-17d).
10. **Changing repo state (adding real config) while a workflow tests the opposite state.** *Fix:*
    hold the change until the run ends (§9; T-17a).
11. **Treating store eligibility as a puzzle to route around.** *Fix:* state the rules with
    sources; the owner decides with a qualified adviser (§9).
12. **Test builds uploading release artefacts to real services.** *Fix:* gate uploads on real
    signing; disclose what landed (§10; T-14).
13. **Resuming on a guess after an interrupt, or reporting stale status.** *Fix:* re-derive state
    from git and the runs; then use a finisher (§10; T-7, T-9).
14. **Fixing an owner-reported bug from the photo alone.** *Fix:* reproduce, separate tool from
    app, measure, then fix with a guard (§10; T-157).
15. **Owner facts written into another project's memory.** *Fix:* PROGRESS "Standing owner
    preferences" always; a memory note only in this project's own memory (§11; T-17f).
16. **Owner-only chores scattered across messages.** *Fix:* one END-OF-PROJECT list, presented once
    (§13).
