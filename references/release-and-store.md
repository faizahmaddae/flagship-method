# Release and store

How to build an artefact you can prove is the right one, prove that it starts and plays, make
every word and picture on the store page true, and hand the upload to the owner. Every gate here
exists because a build that passed every other check was rejected, crashed or lied.

**Read when:** the owner asks for a build (§0 first); Phase 5 (release prep); writing or changing
store text, screenshots or the preview video; adding anything that changes what the built artefact
must contain (ids, permissions, entitlements, SDKs); adding accounts (deletion is a review gate,
§7); before anything is uploaded anywhere. Money and privacy rules are in
`references/monetization-and-privacy.md`.

## Contents
0. The upload gate (read first): uploads, submission, permanent ids, the owner's list, eligibility
1. Release engineering
2. The static artefact verifier
3. The run gate
4. `RELEASE.md` and what a pass does not prove
5. Store copy that cannot lie (the `store/` folder, claim table, per-project banned list)
6. Screenshots and the preview video
7. Ratings, audience, accounts and the compliance docs
8. Platform traps that silently break a release
9. The release checklist

---

## 0. The upload gate (read first)

1. **No upload of any kind unless the owner explicitly asks for that specific upload; no submission
   before their device test and approval.**
   - An owner gate build (Phase 2 and later) reaches the owner by a non-public route by default: a
     cable or developer install, a locally built package they install, or a simulator recording if
     they have no device (`references/planning-and-slices.md` §3).
   - Any upload, an internal test track included, happens only when the owner explicitly asks for
     that specific upload. One request covers that one build, not the next.
   - Submission for review, external testing or the public happens only after the owner has tested
     the build on their own device and approved that submission explicitly in chat.

   Your release work ends at verified artefacts and the facts the owner needs to decide. Uploads,
   console entries, store records, purchases, account settings and logins belong to the owner. A
   tool that *can* upload is not permission to upload (`references/working-with-the-owner.md` §9).
2. **Version numbers belong to the owner.** Never invent one, never reuse one, never bump one
   because "it was next". Ask, and record the answer in PROGRESS.
3. **Permanent identifiers are confirmed before the first upload:** app/bundle id, product ids,
   content epochs (a daily-content start date re-maps every player's archive if it moves), display
   name. Record each in DECISIONS with "permanent from the first upload".
4. **The name is cleared before the first upload makes it permanent.** The screening method is in
   `references/kickoff.md` §5.5. At release, re-run the store searches (a new app may have appeared
   since kickoff), confirm the owner has the clearance opinion they chose to get, and recommend
   claiming the store record early. Store text never names a character whose name is not cleared.
5. **The owner's end-of-project list.** Its format, timing, order constraints (dated) and language
   rules live in `references/working-with-the-owner.md` §13. These are the release and money items
   it usually needs; give each its exact ids, console menu path and what happens if it is skipped:
   - [ ] Ad network app + unit ids into the gitignored env file. Console: tracking-explainer state
     matching the prompt owner, privacy messages (GDPR, US states), content ceiling, child tags,
     caps mirrored, floors, blocked categories.
   - [ ] app-ads.txt on the developer website named in both listings.
   - [ ] Privacy label and data-safety answers pasted from the answers file; App Review notes.
   - [ ] Upload keystore; distribution profile regenerated **after** enabling capabilities.
   - [ ] IAP and subscription records: agreements, tax and banking first; ids exact and permanent;
     type; localisation; review screenshot; terms (EULA) link for subscriptions; sandbox and license
     testers (including a slow-card tester).
   - [ ] If the product has accounts: the web deletion link entered in the data-safety form; the
     reviewer's demo account (§7).
   - [ ] Listing texts, privacy-policy publication (before review), age-rating questionnaires.
   - [ ] Analytics property settings (signals off, ads personalisation off, custom definitions
     before launch, one forced release crash to prove reporting).
   - [ ] A device test script, runnable as written: every consent/tracking/ads/IAP path, kill under
     the primer, Home-and-back mid-flow, airplane mode at launch, reinstall + restore; where they
     exist, a subscription's renewal and lapse in the sandbox and an account deletion end to end.
   - [ ] An outside viewer's icon check; small confirmations (support email, developer name,
     retention setting); test data the tools may have left in the owner's accounts.
6. **Store eligibility was checked at kickoff; re-confirm it before the first upload.** Whether the
   owner can hold a developer account in each store, receive payouts and sell in their country is a
   compliance check in `references/kickoff.md` §5.5 (Track E). If a store is out of reach, the
   release plan names the route the owner chose (for example a local store) as a DECISIONS entry;
   never suggest a way around sanctions or eligibility rules.

## 1. Release engineering

### 1.1 Native projects come from a script
Platform folders are generated and patched by an idempotent setup script: inputs validated before
anything is deleted, every edit verified right after it and again on the final tree, two runs
byte-identical. Method: `references/architecture.md` §11; Flutter sketch: `references/stack-flutter.md`
§12. The release-relevant edits it writes **and verifies** (the shipped game's set):
- [ ] display name, bundle id, team id, version from the owner's numbers;
- [ ] orientation, device family, app category, platform lifecycle requirements, target SDK;
- [ ] export compliance, privacy manifest (literal shape), tracking purpose string, attribution ids;
- [ ] ad network app ids, crash/analytics config (shape-validated), entitlements;
- [ ] signing config copied in from outside the generated folders, shrinker keep rules referenced
  by the release build type, side-effect gates (§1.5);
- [ ] icons and launch screens (drawn icons re-derived on every regeneration).

### 1.2 Inputs exist before the build
Put an inputs table at the top of `docs/<slug>/RELEASE.md`:

| Input | Where | Without it |
|---|---|---|
| Production ad ids | gitignored env file (`.example` committed with vendor sample ids) | build carries sample ids; the verifier refuses |
| Upload signing key | gitignored properties + keystore, kept outside regenerated folders | release falls back to the debug key; refused |
| Distribution profile | owner's keychain, regenerated after capabilities are enabled | export fails or signs without entitlements; refused |
| Crash/analytics config | committed real pair, shape-validated | reports nothing, or a malformed key crashes natively at launch |

Example (earlier game): a regenerated platform folder deleted the keystore config, and every
release was silently debug-signed. Account-specific inputs live outside generated folders and are
copied in by a verified patch.

### 1.3 Production ids
Where ids live and how the repo is kept clean of them: `references/architecture.md` §12.1. For the
release itself:
- The helper that prints the release defines prints exactly the expected flags, warns per empty
  slot on stderr, lets the environment override the file, and refuses an application id placed in
  a unit slot (printing nothing).
- **Decide production per platform: both formats or neither.** An Android interstitial plus an iOS
  rewarded completes neither.
- A release built without ids runs with no ads, never with test ads.

### 1.4 Debug-only switches are proven dead in release
Debug-only switches (consent geography, age mocks, analytics-in-debug) exist so the owner can run
device checks whose real trigger is unreachable (a minor's account, an EEA location). Each is a
release risk: a store build with a leftover age mock set to "teen" would treat every adult as a teen.
Classify every compile-time define and prove each debug one dead by compiling a probe three ways
(`references/architecture.md` §12.2; Flutter commands: `references/stack-flutter.md` §13). The
release checklist requires that proof for the commit being shipped.

### 1.5 Test builds never touch production backends
Know which build steps talk to real services, and gate each on a real release signal:
- Crash-mapping uploads run only when the upload key exists. Prove it with the build tool's dry
  run: no upload task is listed on a machine without the keystore.
- Symbol uploads run only from archive builds. Run the installed phase both ways with a fake
  uploader.
- Error-injection probes run on a copy with the backend config removed.
- Recordings and screenshots use null cloud/analytics/ads services (§6 item 9).

*Why:* the crash plugin uploaded mapping files on every release build, debug-signed test builds
included. Two test mappings reached the real project, and a network error failed one build. An
error probe on a release build reported to the real crash dashboard. When test traffic did reach
production, tell the owner exactly what and where.

### 1.6 Symbols for this binary
Readable production crashes need symbols (iOS dSYMs, the Android mapping file) uploaded for **this**
binary. The upload script writes a stamp holding the binary's UUID, and the static verifier refuses
an artefact whose stamp is missing or belongs to another build.

> **Dated facts (as of 2026-10 — re-verify before relying):** Xcode's `ACTION` reads "archive" in
> `-showBuildSettings` but "install" inside a real archive. Gate symbol phases on
> `DEPLOYMENT_POSTPROCESSING == YES` instead. Gradle's `-m` dry run lists the tasks a build would
> run. The Crashlytics iOS pod adds no dSYM upload phase of its own, so a script uploads and stamps.

## 2. The static artefact verifier

**Principle:** a last script reads the **built** artefact (`.ipa`/`.app`/`.aab`/`.apk`), not the
source. Every check targets a failure that is invisible in a successful build. Each row below is a
real incident.

| Check | Incident it prevents |
|---|---|
| Signed for distribution (upload key / distribution certificate); not debuggable; no `get-task-allow` | debug-signed bundle |
| Real app ids: no vendor sample publisher, each platform exactly its own | sample ids shipped when the gitignored file was missing (three times) |
| **Every** production unit id compiled into the code binary (inverse check) | as above |
| Required permissions present in the **merged** manifest (ad id, billing) | billing arrives by manifest merge; without it the store won't sell |
| Tracking purpose string present and exactly the reviewed wording | the app is terminated when it asks without one |
| Privacy manifest in a reviewed literal shape (`references/monetization-and-privacy.md` §7) | Invalid Binary hours after upload |
| Ad-network attribution id list well formed, ≥ floor | zero ids makes networks bid down |
| Crash/analytics config present, for this bundle id, not a test fake | reports nothing |
| Symbol stamp matches this binary's UUID | raw addresses in every crash |
| Nothing test-only bundled (purchase test configs, fake config markers) | test store config shipped |
| Required entitlements in the **signature** | profile predated the capability, so signing stripped the keys |
| Artefact newer than the code | stale upload |
| Review-notes constants equal the code's constants | reviewer told the wrong moment |

**Rules for the verifier itself:**
1. **Invert the check when the bad value is always present.** Test ad ids from a library are
   compiled into every build, so "is the sample absent?" can never pass. Ask "is every production
   id present?" instead: extract id-shaped strings from the compiled binary and require each id from
   the env file.
2. **Staleness.** Fail if the artefact is older than the last commit touching sources, older than
   any modified, staged or untracked source file, or if sources were deleted since. Example: an
   artefact sat in the build folder for eleven hours while five commits changed the code, and
   stores accept stale uploads silently. The `.apk` next to an `.aab` is a different artefact.
3. **No silent skips.** Every "acceptable here" path is a named flag (`--allow-stale`,
   `--allow-sample-ads`) printed as "allowed explicitly". The default is fail.
4. **Print the review notes every run, and cross-check them.** The sentences you will paste for the
   reviewer (when the tracking prompt appears, when a dormant feature starts) are constants in the
   verifier, grepped against the source constants. A mismatch fails.
5. **Selftest with fabricated inputs and fake tools.** Every path the script reads can be overridden
   by an env var. External tools are fakes on PATH that print fixtures. A case runner is
   `run_case label want_rc want_substring env… args…`. **FAIL text goes to stderr, and the selftest
   matches stderr**, because otherwise an earlier step's FAIL hides a later check that was demoted
   to a plain echo. Each case must reach the step it tests. Case counts grew with every review
   (16 → 43), and each new case was a real gap.
6. **End with one unmistakable line**, such as "Ready to upload", and nothing else counts as a pass.
7. **Read binary formats with the right tool, never by eye** (dated block below).

> **Dated facts (as of 2026-10 — re-verify before relying):** Android: the merged manifest in an
> `.aab` is protobuf, so read it with bundletool (or aapt2 for an `.apk`). Signatures: keytool for an
> `.aab` (v1 JAR), apksigner for an `.apk` (v2/v3). iOS: entitlements with
> `codesign -d --entitlements - --xml`, provisioning with `security cms -D`. A simulator build's
> entitlements live in a binary section, not the code signature. Use `strings -a` on the compiled
> code binary. Google's SKAdNetwork list had ~50 ids, so use a verifier floor of 40. AdMob
> application ids use `~`, and a unit id (`/`) in that slot makes the SDK throw at launch.

## 3. The run gate

**Principle:** static checks and unit tests never start the shipped binary. Install **the exact
artefact that uploads**, start it, play it, and watch it stay alive.

*Why (word game):* a bundle passed every static check, then died at start under the code shrinker,
and the store rejected it with a photo of "keeps stopping". Tests run without the shrinker, analysis
reads source, and the artefact check reads certificates and manifests, so nothing had ever started it.
A sorting game hit the same fault with 605 tests green; its own launch gate caught it before upload.

**The gate:**
1. **Build from the upload artefact.** Example: make a universal APK from the `.aab`, signed with
   the upload key. Never test a stale sibling file.
2. **Fresh install.** Uninstall first: shrinker problems and migrations hide behind old data, and
   the reviewer has none. Read the version code back from the device to prove which artefact ran.
3. **Cold start**, and record the start-time figure.
4. **Prove the app's own code ran via the accessibility tree.** Wait (≤ 30 s) for a node only your
   UI framework publishes, such as the main button's label. The launch screen looks like the first
   frame, so **a screenshot cannot prove the runtime started**.
5. **Play N flows by accessibility label, not pixels.** Example: the first five levels by finger,
   the share sheet (native interop + file provider), a rewarded **test** video that must pay its
   reward, then Back to home. A design that is playable by screen reader doubles as the automation
   API. Dismiss one-time system cards as a user would.
6. **Health after every stage:**
   - the process is alive, and your activity is on top (the process id alone lies: a crashed
     process is kept warm);
   - the crash buffer is empty, and there are no runtime error lines from your pid;
   - **no app crash marker.** A release build with a crash reporter attached logs no findable line
     for a handled error, so make both crash handlers print a fixed marker
     (`<app>: uncaught error: <first line>`) and grep it.
7. **Static shrinker check:** every class the platform builds by name (activities, services,
   receivers, providers, startup initializers, component registrars, generated database
   implementations) must exist **with the no-argument constructor it calls**. Check that keep rules
   are both present and referenced by the release build type, since either half alone is the crash.
8. **Leave screenshots and logs per stage.** End with "Look at the screenshots before trusting it."
   Then look at them.
9. **Inability to run is a FAIL, never a skip.** No device, no tool, no artefact, several devices
   without a serial, no network for the ad stage: each FAIL names the fix.
10. **Prove the gate with a negative control.** Remove the keep rules: the static check must fail,
    the app must die at start, and the gate must fail on the missing button, the dead process and
    the crash buffer. A later reviewer found the gate's error-line check could not fire on a release
    build, which is why the marker line exists. A probe build then failed on exactly the two
    marker lines.
11. **Never tap a live ad.** With production ids the video is real. Register a test device, or run
    the gate with ads off on the production build and rely on the test-id run of the same commit.

**Run it on the device classes the reviewer uses,** including compatibility modes. Example: a store
reviewer opened a phone app on a tablet in phone-compatibility mode that nobody had launched.

**What it cannot do:** some release builds cannot be started by any tool you have (a release iOS
build needs a signed device install). Say so in RELEASE.md: that first launch is the owner's device
test. Procedure doctrine (cold launch, liveness, labels): `references/verification.md` §8.

> **Dated facts (as of 2026-10 — re-verify before relying):** since AGP 8, release builds run R8 in
> full mode by default. With keep rules removed, it kept `WorkDatabase_Impl` but dropped its
> constructor. A fresh emulator's Play services can kill the app once while updating a module (read
> the log, rerun). A fresh Android device shows a one-time "Viewing full screen… Got it" card that
> eats the first Back.
> Back on a share sheet can be swallowed while it slides in, so wait for the chooser on top.
> `uiautomator dump` can fail to see an idle window under ambient animation, so retry it. Grep logcat
> by pid and level. Simulator quirks: the first tap after launch was dropped 3 times out of 3;
> `print` in a debug build doesn't reach the launch console (write marks to a temp folder); a
> reinstall gives a fresh data container (an empty save there is not data loss).

## 4. `RELEASE.md` and what a pass does not prove

Template: `assets/templates/RELEASE.md`. Shape:
- **§0 Inputs** (the table in §1.2).
- **§1 Baseline green:** every selftest, analysis, the full test suite, the verifier's and the run
  gate's own selftests.
- **§2 Regenerate native projects; set the owner's version.**
- **§3 / §4 Per platform:** build with release defines → static verifier "Ready to upload" → run
  gate (or, where none can run, the privacy report from the signed archive compared with the label)
  → the review-notes line.
- **§5 What a passing run does NOT prove.** Write the blind spots of every gate next to it. Examples:
  - the release iOS build was never started by a tool;
  - purchases ran without a store account, so the billing connection merely did not crash;
  - interstitials begin after level 20, but the gate stops at level 6;
  - the preview check verifies the file's format, not what it shows.

  The owner's device test script covers exactly this list. General doctrine:
  `references/verification.md` §11.
- **§6 Reference numbers,** so regressions show: artefact sizes, one-device download size, cold start
  (first install vs warm), the privacy manifests found in the bundle. Example: universal APK 61.5 MB,
  AAB 63.6 MB, one-phone download ≈ 15 MB, iOS app 35.6 MB, cold start 3.7 s first install and
  0.9–1.4 s after.
- **§7 Side effects of a release build:** what talks to real services, and how each is gated (§1.5).
- **§8 The `store/` folder:** an index of `docs/<slug>/store/` (§5) and the commands that check it
  (the copy checker, the privacy-answers script).

## 5. Store copy that cannot lie

**The store folder.** `docs/<slug>/store/` is created in Phase 5 by the release work and owned by
RELEASE (`references/project-kit.md` lists it in the doc set and the precedence order). It holds
`text/<store>/` (every store text exactly as pasted, §5.1), `LISTING.md` (the claim and length
tables, the screenshot caption list, the decisions made in the copy), `RATINGS.md` and
`PRIVACY_ANSWERS.md` (§7). MONETIZATION keeps the decisions these files apply (the model, the offer
copy constants, the privacy-policy rules) and links here for the tables: each table has one home.

### 5.1 Every store text is a registered file
- Keep every store-visible text (name, subtitle, keywords, descriptions, promo text, what's new,
  IAP names and descriptions) as one file, exactly as pasted, in `docs/<slug>/store/text/<store>/`.
- Length = content without the final newline.
- A registry maps each path to its limit, platform and kind. **The set of files on disk must equal
  the registry**, so a new text cannot skip the checks.
- A length table in the listing doc must equal the files.
- Single-line fields have no leading or trailing whitespace.

### 5.2 The claim table: every claim maps to code
Rows: `| id | phrases as written (;; between) | code path:line | needle |`, or a named fact
computed from shipped data (`@levels_and_worlds_count`). A checker requires that:
- every phrase appears in some store text;
- every needle is in its file, and every fact holds;
- **every claim word in every store text lies inside a mapped phrase.** Claim words form a
  WATCHWORDS list: numbers, ×, ads, video, purchase, hints, daily, streak, offline, sync, cloud,
  undo, levels, share, accessibility words.

A new claim without a row, or a feature removed from the code, now fails the build. A `lines --write`
command refreshes line numbers. Example rows (shipped puzzle game):
- "every board has exactly one way to finish it" → the verifier function plus the CI test;
- "After level 20, a short ad may play between some levels, never in the middle of a puzzle" →
  `firstAfterSolved = 20`;
- "(hold up to 2)" → the cap constant.

*Why (earlier game):* the listing claimed "nothing leaves your phone" while the app ran analytics.

### 5.3 One banned list for every store surface
One list, with a reason per pattern, applied to copy, screenshot captions and sub-lines,
feature-graphic words, IAP names and descriptions, and the privacy policy (a policy subset).
*Why:* the screenshot test kept its own shorter list, and eight phrases slipped through: "No-ads",
"Removes all ads", the uncleared character name, "made for kids", "No timer", "Hand-built",
"Nothing leaves your phone", "On iPad". The copy checker now reads the caption source file directly.

**The list is per project.** A phrase is banned because it would be false or risky in *this*
product. The shipped game banned "no ads" and "free" because both would have been false there; a
product with truly no ads, or a core that is truly free, may say so once a claim-table row (§5.2)
maps the phrase to the code that keeps it true. Typical entries (shipped ad-funded game):
- competitor and reference-game names and marks;
- "no ads", "ad-free", "without ads", "zero ads", "removes all ads" (when only breaks are removed);
- "free" (even "free to play"), "#1", "number one", prices (pricing words in metadata: §5 dated
  block);
- child words (for an adult-coded app);
- "hand-made/crafted/built/picked" (when content is generated);
- privacy boasts: "private", "no tracking", "no data", "doesn't collect", "nothing leaves";
- "no timer(s)" (say "no countdown" if a time is recorded);
- "unlimited" (when capped);
- uncleared names.

Platform words per store: no Android/Play in App Store text, no iPhone/iCloud/Apple/iOS in Play text,
neither in shared texts, and never "iPad" for an iPhone-only app.

### 5.4 Wording precision
Prefer the exactly true phrase over the familiar one:
- "no countdown", not "no timers" (a solve time is recorded);
- "every board has exactly one way to finish it", not "hand-built" (levels are generated);
- "supported by ads; a short ad may play between some levels";
- "Remove Ads removes the breaks between levels, for good. Optional hint videos stay.";
- "undo and restart whenever you like", not "free to play";
- a generic noun ("walls", not one theme's name for them), and a role word for the character, not
  its uncleared name.

**A claim true for a new user can be false at a cap:** "every 7 days earns a save" became "(hold up
to 2)". Read every feature's limits before claiming its rate. Leave accessibility claims out until
they are verified on a device; visible settings may be claimed. Cloud sync is claimed only on the
store whose platform has it.

### 5.5 Dormant features: date every line
A feature not reachable on the review date is advertised only with its start date, described in
the review notes, and its screenshot is left out of earlier submissions. The checker refuses any text
naming the feature's words (daily, every day, streak, archive) without the date string. Short fields
that cannot carry the date drop the claim. After the start date, fields that need no review (promo
text) may drop the date. "A guard that only prints a note is not a guard."

### 5.6 Reasons in compliance docs get checks
Every "because…" in a compliance doc can go stale when a feature lands. Example: a ratings answer
"no web access: no links out" became false when the privacy-policy row shipped. The checker now
requires the answer to name the one fixed link while the code opens links. The privacy-policy URL
lives in one code constant, and every doc naming a URL of that family must name exactly it.

### 5.7 Selftest by copying and breaking
The copy checker's selftest copies the store docs, source, data and manifests to a temp dir per case.
It applies one edit, with an anchor that must exist or the selftest aborts, and requires that case's
specific failure. The unmodified copy must pass. Example mutations, each failing with its claim id:
- a cap raised from 2 to 3 under "hold up to 2";
- the first ad moved from level 20 to 10;
- a settings label renamed, or a product id removed;
- 199 levels shipped;
- a network client added under a no-network claim;
- "Hints never run out" added.

### 5.8 ASO patterns that held
- Title: `[short brand]: [genre phrase]`. Subtitle: a benefit plus a second keyword cluster.
- The keyword field never repeats a word from the name or subtitle: the store indexes them together,
  so a repeat only spends characters. The checker refuses one (dropping a repeat brought the field
  to 97/100).
- Use real autocomplete phrases. Note searched modifiers you cannot honestly use ("no ads" when you
  have ads).
- Never use a competitor's title, not even in the subtitle.
- Where the long description is indexed, use generic genre phrases naturally, without stuffing.
- Use the fields that change without review for timely lines; seasonal in-app events give free
  search surface.
- A small word budget makes listing localisation cheap; do the high-value markets first, and never
  ship a machine-only translation in a listing (`references/ux-and-accessibility.md` §Localisation).

### 5.9 Review notes
Write a note for anything a reviewer might not reach: a prompt that appears only after play, a
dormant feature, a hidden setting. Example: "The App Tracking Transparency request appears after
the 4th puzzle is solved (about 3 minutes), preceded by a one-screen explanation with a single
Continue button. The daily puzzle starts on <date>: before that date the home screen shows no
daily." The numbers in it are constants cross-checked by the verifier (§2).

> **Dated facts (as of 2026-10 — re-verify before relying):** App Store limits: name 30, subtitle
> 30, keywords 100, promotional text 170, description 4000, what's new 4000. Play: title 30, short
> description 80, full description 4000, release notes 500. IAP name 30, IAP description 45. App
> Review 2.3.1(a) covers accuracy and undescribed dormant features; 2.3.7 covers metadata (no
> pricing information or other apps' names in it). Apple indexes name, subtitle and keywords
> together; Play indexes the long description; App Store promotional text changes without review.
> Example fill (shipped puzzle game): name 27/30, subtitle 26/30, keywords 97/100, description
> 1916/4000, Play short 79/80.

## 6. Screenshots and the preview video

1. **Drive the real app; never redraw it.**
   - Capture from the real root with every external port faked. Drive it as a user would: input
     through the real state layer, real taps on real buttons, the real completion choreography.
   - Compose only the frame and the words around the capture.
   - *Why:* "the game doesn't look like its ads" was a counted complaint (58).
2. **Deterministic and byte-identical.**
   - Use a fake clock, and make every wait a fixed run of 16 ms frames. Never use "wait until
     settled", which ends wherever the last animation happened to end.
   - Enable ambient motion before the first build.
   - Two builds in separate processes must be byte-identical.
   - Capture at the target phone's logical size × device pixel ratio equal to the store size, with
     real safe-area insets. One capture feeds both stores, so both listings show the same build.
   - Keep outputs out of git, and rebuild after any visual change.
   - (Flutter capture mechanics: `references/stack-flutter.md` §14.)
3. **Frame in your own material, never a drawn phone.** The frame is built from the product's own
   visual language, derived for this project (`references/kickoff.md` §7,
   `references/visual-design.md`); one shipped game framed its shots in its own sculpted material,
   which is its identity, not a style to copy. Platform marketing guidelines forbid drawing their
   hardware, and drawn phones age badly.
4. **The first two shots carry the page.** Shoppers read two and swipe:
   - Shot 1 = the rule and the character (or the product's core) in one glance.
   - Shot 2 = the payoff, your edge.
   - Then feature shots, each a 2–6 word caption plus one line.
   - Example list (shipped puzzle game): "One path. Every square." (the rule) / the solve payoff /
     the daily (dated, left out before its start) / the campaign's size / dark mode / the hint /
     a rule variant / "No lives. No rush."
5. **One caption source.** Each entry holds: slug, caption, accent substring, sub-line, `shows`, and
   `truth` (the code that makes it true). A test holds it to the caption list in
   `docs/<slug>/store/LISTING.md` (same words, same order) and to the bundled fonts' glyphs: a "→"
   with no glyph renders as tofu. The copy checker reads the same source (§5.3). Render the set side
   by side as a shopper swipes it (`scripts/contact_sheet.py`), and look at it.
6. **Read every output back, and count.** Re-read each file's header: exact pixel size, **no alpha**
   (both stores refuse it), the expected count per folder, the fallback set and the contact sheet
   present. Measure the caption band against the store's text-area limit. *Why:* "a loop that keeps
   going after a failed file looks exactly like a loop that worked."
7. **Pick frames from a filmstrip; the event frame is often the worst.**
   - Tile a sequence (`scripts/contact_sheet.py`) and choose by eye.
   - *Why:* the "goal reached" frame put the character over the last number ("11" read as "1") and
     froze a segment mid-transition as a hard wedge. Mid-run was better.
   - Guard the pick with a pixel test: every number near the character keeps its numeral, compared
     with a frame of the same run where the character is far away.
8. **Compute a cue's contrast across every palette before hunting for a better scene.** Hint dots at
   35% opacity measured 1.2–1.7:1 on every theme's tiles, so no scene or framing could rescue the
   shot. The product's dots were redrawn opaque with a ≥ 3:1 rim. Fix the product, not the
   screenshot.
9. **Preview video from the real app.**
   - **Length and hook:** 15–30 s, with a satisfying completion in the **first 3 s** (it autoplays
     muted).
   - **A separate entry point** that differs from `main()` only in what keeps the footage clean:
     a null ads service (no primer over footage), no analytics (a recording is not a user), and a null
     cloud mirror. A simulator signed in to a cloud account otherwise writes the recording's progress
     to that account, so warn the owner it may hold test data. Seed a returning-user save (tutorials
     done, rating prompt already asked).
   - **Drive input** through the framework's own input pipeline from a script (Flutter entry point
     and input injection: `references/stack-flutter.md` §14).
   - **Warm up off camera.** The first heavy animation in a debug build stalled 158 ms while
     compiling (77 ms after warm-up). Record from a non-debug build where possible.
   - **Set up the device:** fresh install, a clean status bar, light mode.
   - **Cut** from timed marks the app writes to a temp folder.
   - **Encode, then read every number back** with `ffprobe` (size, orientation, fps, duration,
     codec, profile, audio channels, sample rate, **actual** audio bitrate). *Trap:* ffmpeg's built-in
     AAC encoder wrote "256 kbps" silence at ~2 kbps, which the store spec refuses, so use the
     platform encoder and check the file, not the flag. A test builds a passing file, then breaks it
     one way at a time (too short, landscape, 60 fps, mono, low bitrate, wrong codec).
   - **Choose a poster frame.**
10. **Keep a fallback set ready** in the same pipeline, tested: a product-led icon and first shot,
    character out of frame (`references/monetization-and-privacy.md` §9).

> **Dated facts (as of 2026-10 — re-verify before relying):** App Store 6.9" iPhone shots are
> 1260×2736, 1290×2796 or 1320×2868, 1–10 images, no alpha; smaller iPhones are scaled from them.
> Play: 2–8 per device type, and ≥ 3 portrait 9:16 at ≥ 1080×1920 for game recommendations; taglines
> ≤ 20% of the image; feature graphic 1024×500, no alpha. App preview: 886×1920 portrait, 15–30 s,
> 30 fps, H.264 high 10–12 Mbps, yuv420p, stereo AAC 256 kbps at 44.1/48 kHz, < 500 MB. Play's promo
> video takes only a YouTube link (unlisted, ads off, not age-restricted, a watch URL, not Shorts).
> The app icon must have no alpha channel at all (ITMS-90717).

## 7. Ratings, audience, accounts and the compliance docs

Keep three compliance docs in `docs/<slug>/store/`, each answering from the code:
- **`RATINGS.md`:** each questionnaire step as `Question | Answer | Why (the code)`, then the computed
  result, the recommendation with its guideline, the regional rating-board table, the expected
  outputs, target audience and family-policy implications, and a law table with dates and effects.
  - **Reconcile the computed rating with your ads' content ceiling.** If the questionnaire gives a
    lower rating than the ads may show, rate up, or lower the ceiling (lower fill). Example: the
    questionnaire computed 4+ while ads were capped at PG, so 9+ was recommended.
  - Answer from what the product is, not from words that sound alike: personal streaks are not
    contests, fixed-content packs are not loot boxes, a "relax" keyword is not a wellness claim.
  - The audience is a decision slot made at kickoff (`references/monetization-and-privacy.md` §9):
    the rating says what the content suits, the target audience who it is made for. Example: an
    ad-funded game with a cute character targeted adults while its content was rated for everyone.
- **`PRIVACY_ANSWERS.md`:**
  - SDKs that collect (what, from when);
  - the label per data type (linked, tracking, purposes, declared by);
  - not collected;
  - a product-page preview;
  - why the manifest and the label differ;
  - the data-safety table;
  - the other store declarations;
  - the policy-statement table.
- **`LISTING.md`:** the claim table (§5.2), the length table, the screenshot caption list (§6), and
  "decisions made in the copy".

Every stated reason in these docs is checked against the code (§5.6). Re-check the law table at
every release, and record a re-check with a date even when nothing changed.

**Accounts and deletion (when the product has accounts).** Review blocks an app that lets users
create an account but not delete it. The design (sign-in, deletion, export, shared records) and the
store rules with their dates live in `references/domain-apps.md` §8; this is the review and console
gate, checked on the release build:
- [ ] Deletion starts inside the app from account settings and deletes rather than deactivates;
  third-party sign-in tokens are revoked where the provider requires it.
- [ ] A web link lets a user request deletion without reinstalling; it is entered in the store's
  data-safety form.
- [ ] The privacy policy and `PRIVACY_ANSWERS.md` say what is deleted, what is kept and for how
  long, and what happens to records shared with other users.
- [ ] The review notes (§5.9) give the reviewer a working demo account.

> **Dated facts (as of 2026-10 — re-verify before relying):** App Review Guideline 5.1.1(v) requires
> in-app account deletion for apps that support account creation (since 2022-06-30); Google Play
> requires an in-app path plus a web deletion link declared in Data safety (details:
> `references/domain-apps.md` §8). Guideline 2.1 expects a demo account, or a full demo mode, for
> features behind a login.

## 8. Platform traps that silently break a release

Each of these built green and failed later. Keep a dated list in the project skill, and re-check it
at every SDK or OS bump.

> **Dated facts (as of 2026-10 — re-verify before relying):**
> - A portrait-locked universal iOS app is refused (ITMS-90474; iPad apps must support all
>   orientations). Ship iPhone-only when portrait-only. Read the *chosen* device family, not the
>   default: an earlier game shipped iPhone+iPad by default and drew iPad screenshots, then an
>   orientation rejection.
> - Android 16+ ignores `screenOrientation` on displays ≥ 600 dp for apps targeting API 36, unless
>   `android:appCategory="game"`; the opt-out goes away at API 37.
> - Play requires target API 36 for new apps and updates from 2026-08-31. iOS uploads have needed the
>   iOS 26 SDK since 2026-04-28, and the iOS 27 SDK is expected from April 2027. iOS 27 requires the
>   UIScene lifecycle, so the setup script verifies the scene delegate.
> - iOS export with no Apple ID in Xcode needs manual signing with a named App Store profile.
> - Entitlements (cloud key-value, age range) must be enabled on the App ID and the profiles
>   regenerated before a signed build; automatic signing strips them otherwise.
> - A free app with IAPs still picks a price tier and availability. Apple's age ratings are
>   4+/9+/13+/16+/18+, with new questionnaire items mandatory from September 2026. Guideline 2.5.18
>   requires ads to suit the age rating. Expected IARC outputs for a calm puzzle with IAPs: ESRB
>   Everyone, PEGI 3, "In-Game Purchases".
> - Android night-mode resources go through what the styles name; a night `styles.xml` outranks the
>   API-31 styles and drops the splash. iOS caches launch screens, so reboot or reinstall to see a
>   change.
> - Stack-specific build blockers (for example an ads plugin's iOS module-map patch):
>   `references/stack-flutter.md`.

## 9. The release checklist

- [ ] Owner's version numbers recorded; permanent identifiers confirmed; name cleared; store
  eligibility re-confirmed (§0.6).
- [ ] Inputs exist (ids, upload key, profile regenerated after capabilities, crash/analytics config).
- [ ] Baseline green, including every tool's selftest.
- [ ] Native projects regenerated by the script; two runs byte-identical.
- [ ] Debug-only defines proven dead in release; release defines print exactly the expected flags.
- [ ] Static verifier "Ready to upload" for each artefact; no "allowed explicitly" lines unexplained.
- [ ] Run gate passed on the bundle that uploads; screenshots looked at.
- [ ] Symbols uploaded for this binary; test builds sent nothing to production (or it was disclosed).
- [ ] Privacy report from the signed archive compared with the label; data-safety answers rechecked.
- [ ] Store copy checker green: limits, claim table, one banned list, dated dormant features.
- [ ] Screenshots and preview rebuilt from this commit; read back; contact sheet looked at.
- [ ] Review notes printed by the verifier and matching the code; law table re-checked with a date.
- [ ] If accounts exist: in-app deletion, web deletion link, policy wording and demo account (§7).
- [ ] If subscriptions exist: disclosure, terms and privacy links, Restore and Manage present
  (`references/monetization-and-privacy.md` §5.7).
- [ ] RELEASE.md §5 "what this does not prove" written; the owner's device test script covers it.
- [ ] No upload happened without the owner's explicit request for that specific upload.
- [ ] Owner tested on their device and approved this submission explicitly. Only then submit, or hand
  over the submission.
