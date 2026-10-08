# flagship-method

A Claude Code skill that carries a field-tested way of building a premium, store-ready mobile game or
app, from the first idea to the upload. It was distilled from three mobile games built by an AI
builder for a demanding owner. One of them went from research to store-ready in a few days of agent
sessions, with every level proven by a solver, every guard seen to fail, and every screen looked at
before anyone called it done. The skill holds what made the difference: how the goal is understood,
how research and decisions are recorded, how work is sliced and verified, how visuals are judged by
rendering and looking, and how nothing outward happens unless the owner asks for it: no upload without their
request for that specific upload, and nothing to review or the public before their own device
test and approval.

It transfers a **method and a bar**, not a look. Every project derives its own identity: art
direction, motion, sound and voice, from its own audience and competitors. Examples from past
projects appear only to show a method at work. The method is stack-neutral, with a deep Flutter
playbook and a translation table for SwiftUI, Jetpack Compose, React Native and the web. It works with
one Claude session, or with many agents in parallel when the tools allow.

## What is inside

```
flagship-method/
├── SKILL.md                  the operating method, lifecycle, quality bar and routing table
├── README.md                 this file
├── references/               read on demand, routed from SKILL.md
│   ├── kickoff.md            goal → owner interview → research → identity → kit → Gate 0
│   ├── working-with-the-owner.md
│   ├── project-kit.md        the per-project docs: what each one decides and how to keep it alive
│   ├── planning-and-slices.md  phases, gates, slices, definition of done, handoff, retrofit
│   ├── orchestration.md      multi-agent lanes, reviewers, fixers; the solo fallback
│   ├── architecture.md       pure core, ports, enforced layers, saves, clocks, timeouts, pipelines
│   ├── performance.md        frame budgets, repaint isolation, quality tiers, device profiling
│   ├── verification.md       guards that are proven to guard; tests; adversarial review
│   ├── visual-design.md      identity as rules, colour, type, layout, lightings, icon, look loop
│   ├── motion-and-feel.md    motion specs, input feel, haptics, sound
│   ├── ux-and-accessibility.md   UX rules, accessibility, localisation, RTL and calendars
│   ├── monetization-and-privacy.md   choosing the model, ads, purchases, subscriptions; dated
│   ├── release-and-store.md  setup scripts, release verifiers, store copy, screenshots, upload gate
│   ├── traps.md              the trap catalogue: mechanism → fix → guard
│   ├── domain-games.md       games: content, difficulty, tutorials, daily, mascot, economy
│   ├── domain-apps.md        non-game apps: the same bar for flows, forms, data, sync and accounts
│   ├── stack-flutter.md      the Flutter playbook
│   └── stack-other.md        SwiftUI / Compose / React Native / web equivalents
├── assets/templates/         the doc kit copied into a project (the builder skill is SKILL.md.template)
└── scripts/
    ├── init_kit.py           scaffolds the kit, checks it for unfilled TODO markers (standard library)
    ├── init_kit_selftest.py  the cases behind `init_kit.py --selftest`
    ├── contact_sheet.py      tiles rendered PNGs into a labelled sheet or filmstrip (needs Pillow)
    └── code_reviews.py       counts review themes per app for the research step (standard library)
```

## Install

Pick one place:

- **For all your projects:** copy the folder to `~/.claude/skills/flagship-method/`.
- **For one project (and its collaborators):** copy it to `<project>/.claude/skills/flagship-method/`
  and commit it.

Then start a new Claude Code session and ask "Which skills can you use?". `flagship-method` should
be listed. Claude also picks it up by itself when you describe a new app or game.

**Python.** The scripts need Python 3.8 or newer. `init_kit.py` and `code_reviews.py` use only the
standard library. `contact_sheet.py` needs Pillow; install it into a virtual environment once:

```bash
python3 -m venv ~/.venvs/flagship && ~/.venvs/flagship/bin/pip install pillow
```

Then run `contact_sheet.py` with `~/.venvs/flagship/bin/python`. Two reasons not to use plain
`pip install`. First, Homebrew's Python and most Linux distributions' Pythons refuse a system-wide
`pip install` ("externally-managed-environment", PEP 668). Second, the commands here run the scripts
with `python3 -I`. Isolated mode ignores `PYTHON*` environment variables and puts neither the script's
folder nor the user site folder on the import path, so a stray module cannot hijack a run. Under `-I`
a `pip install --user` Pillow is invisible. A virtual environment's own packages are not "user site",
so `-I` still sees them.

Check all three scripts after installing (each prints its cases and ends with `0 failure(s)`):

```bash
python3 -I ~/.claude/skills/flagship-method/scripts/init_kit.py --selftest
python3 -I ~/.claude/skills/flagship-method/scripts/code_reviews.py --selftest
~/.venvs/flagship/bin/python -I ~/.claude/skills/flagship-method/scripts/contact_sheet.py --selftest
```

The `init_kit.py` selftest also renders the shipped templates in every combination and proves that its
own checks fail when a feature is removed from a copy of the script.

**Share it with a friend** as a zip:

```bash
cd ~/.claude/skills && zip -r flagship-method.zip flagship-method -x '*.DS_Store' '*__pycache__*'
```

They unzip it into their own `~/.claude/skills/` (or a project's `.claude/skills/`) and run the checks
above. Nothing in the skill refers to your machine, your accounts or your projects.

## Start a new project

Open Claude Code in an empty folder (or a fresh repository) and say what you want, in any language:

> I want to build a calm daily word puzzle for adults, iPhone and Android. Use flagship-method.

What happens next:
1. **Understand.** Claude sends a short numbered list of questions in your language, each with its
   recommendation, and starts research at once on the recommended answers. If you would rather not
   decide design details, say so: it decides from evidence and records why.
2. **Research and identity.** Competitors, feasibility, money and legal facts, each tagged with its
   status and date; then an identity brief with rendered style probes for you to react to.
3. **The kit.** Project docs in `docs/<slug>/`, a router `CLAUDE.md`, and a project skill
   `.claude/skills/<slug>-builder/`. These now steer every later session, whichever model runs it.
4. **Gate 0.** You confirm the name, permanent ids and scope.
5. **Building in phases.** You see the first slice only at final quality, on your own device, and
   answer one question about how it feels.
6. **Release.**
   Nothing is uploaded unless you ask for that specific upload, and nothing goes to review or the public before you have tested it on your device and approved.
   Purchases, signing and account settings wait for your explicit request in the same way.

### Scaffold the kit by hand

Claude runs this during kickoff; you can run it too. `<skill-dir>` is the folder that holds this
skill's `SKILL.md`, for example `~/.claude/skills/flagship-method`. Run it from anywhere, always pass
`--dest` (the project root), and never point `--dest` at the skill folder. A dry run first:

```bash
python3 <skill-dir>/scripts/init_kit.py --dest <project-root> --kind app --name "Calm Ledger" \
  --slug calm-ledger --one-line "A shared expense ledger for small groups." --owner "Sam" \
  --language "English" --stack "Flutter 3.x" --platforms "iPhone, Android phones" \
  --with-monetization --with-release --dry-run
```

Then the same command without `--dry-run`.
- `--kind game` or `--kind app` (required) keeps the templates' game-only or app-only passages.
- `--with-monetization` adds MONETIZATION.md when the product earns money or collects data.
- `--with-release` adds RELEASE.md when it ships to a store or a production server.
- `--owner` takes the owner's name as they want it written, or simply "the owner".
- `--one-line` is one sentence ending with a full stop: the templates start a new sentence after it.
- The slug is internal, lowercase words joined by hyphens. Renaming the product later does not
  require renaming the slug.
- The script never overwrites a file. Any value you did not give, and every slot the templates leave
  for kickoff, is a `[TODO: …]` marker. List the ones still open, by file and line, with:

```bash
python3 <skill-dir>/scripts/init_kit.py --check --dest <project-root> --slug calm-ledger
```

It exits 1 while any marker remains, so it can sit in a project's verification commands.

## Adopt it in an existing project

In the project's folder, say:

> Adopt flagship-method for this project.

Claude follows the retrofit path (`references/planning-and-slices.md`, section Retrofit). It runs and
renders the project as found and sends its questions first. It writes the kit from the real state of
the project rather than from template assumptions, adds the missing guards first, and then continues
in verified slices.

Existing files are never overwritten. Without `--retrofit`, `init_kit.py` refuses when any kit file
exists (exit 2) and writes nothing. With `--retrofit`, if any kit file already exists, for example a
`CLAUDE.md`, the whole kit is staged in `<project-root>/.flagship-kit/` (or in `--stage <folder>`).
A `MERGE.md` there lists the files to merge by hand and the files to move into place. Merge, delete
the staging folder, then run `--check`.

## The research and look-loop helpers

- **Review themes** (`code_reviews.py`). Give it the competitor reviews you pulled (JSON or CSV:
  app, rating, date, title, body) and a themes file: one regex per theme, with an optional "must
  also mention X" filter (e.g. "wants to pay" only in reviews that also mention ads). It counts
  complaints in 1–3★, loves in 4–5★ and complaints inside 4–5★, per app and theme. It sets each
  store average beside the mean of the recent written reviews and writes a CSV. `--help` describes
  the file formats.

  ```bash
  R=docs/<slug>/research
  python3 -I <skill-dir>/scripts/code_reviews.py $R/raw/reviews.json --themes $R/themes.json \
    --store $R/store_averages.json --csv $R/theme_counts.csv --uncoded $R/raw/uncoded_low.txt
  ```

  The kit's `research/.gitignore` keeps `research/raw/` out of git. Remove that rule only when the
  reviews' licence and privacy allow committing them, and record why in DECISIONS. The themes file,
  the counts and the commands always stay in the repository.

- **Contact sheets and filmstrips** (`contact_sheet.py`). Tile renders to compare variants, or tile
  frames to judge order and timing. `--cell 390x844` gives phone-shaped cells. `--same-scale` keeps
  true relative sizes. `--bg checker` shows transparency. A missing input file is an error, never
  silently skipped.

  ```bash
  ~/.venvs/flagship/bin/python -I <skill-dir>/scripts/contact_sheet.py build/looks/home/ --cols 4 \
    --cell 390x844 --title "look 1" --out build/looks/home_1.png
  ```

## Update

- Replace the skill folder with the newer copy. If you edited your copy, keep the old one aside and
  merge by hand.
- Projects are not affected: each project's kit lives in that project. When a project learns a lesson
  worth keeping (a new trap, a better rubric), rewrite it without project names and add it to the
  matching file here (`references/traps.md` for traps). Then run the leak check; both commands must
  print nothing. Put your own product, mascot, people and company names in the first; the brackets
  stop each pattern from matching its own line here:

  ```bash
  grep -rniE '<product>|<mascot>|<owner>|<company>|/U[s]ers/|/h[o]me/[a-z]' ~/.claude/skills/flagship-method
  grep -rniwE 'h[e]|h[i]s|h[i]m|h[i]mself|s[h]e|h[e]r|h[e]rs|h[e]rself' ~/.claude/skills/flagship-method
  ```

  The second keeps the skill gender-neutral: "the owner", they/them; a mascot is "it".
- Facts marked **Dated** (package versions, store and ad rules, privacy law, platform behaviour) were
  checked around 2026-10. Re-verify them against the installed source or official docs before
  relying on them.

---

## راهنمای کوتاه فارسی

**این چیست؟** `flagship-method` یک «مهارت» (skill) برای Claude Code است: روش کار و معیار کیفیتی
که چند بازی موبایل با آن از ایده تا آمادگی انتشار ساخته شدند. این مهارت ظاهر هیچ پروژه‌ای را تکرار
نمی‌کند؛ هر پروژه هویت خودش (ظاهر، حرکت، صدا و لحن) را از مخاطب و رقبایش پیدا می‌کند.

**نصب**
1. پوشه‌ی `flagship-method` را در `~/.claude/skills/` کپی کنید تا در همه‌ی پروژه‌ها در دسترس باشد،
   یا در `.claude/skills/` داخل یک پروژه تا فقط همان پروژه از آن استفاده کند.
2. یک جلسه‌ی تازه‌ی Claude Code باز کنید و بپرسید «چه مهارت‌هایی داری؟». نام `flagship-method` باید
   در فهرست باشد.
3. اسکریپت‌ها به Python 3.8 یا بالاتر نیاز دارند. فقط `contact_sheet.py` به Pillow نیاز دارد. آن را
   یک بار در یک محیط مجازی نصب کنید:
   `python3 -m venv ~/.venvs/flagship && ~/.venvs/flagship/bin/pip install pillow`
   پایتونِ Homebrew و بیشتر توزیع‌های لینوکس نصب سراسری با `pip` را نمی‌پذیرند (PEP 668). اگر هم
   Pillow را با `--user` نصب کنید، اجرای `python3 -I` آن را نمی‌بیند.
4. برای فرستادن به یک دوست، پوشه را zip کنید. او آن را در `~/.claude/skills/` خودش باز می‌کند.

**شروع یک پروژه‌ی تازه**
- در یک پوشه‌ی خالی Claude Code را باز کنید و خواسته‌تان را بنویسید، مثلاً: «می‌خواهم یک اپ ساده
  برای ثبت عادت‌های روزانه بسازم. از flagship-method استفاده کن.»
- Claude چند سؤال کوتاه و شماره‌دار به زبان خودتان می‌پرسد و برای هر کدام پیشنهادش را هم می‌گوید.
  منتظر جواب نمی‌ماند و تحقیق را همان موقع شروع می‌کند. بعد هویت محصول را پیشنهاد می‌دهد و اسناد
  پروژه را در `docs/<slug>/` می‌نویسد.
- تصمیم‌های برگشت‌ناپذیر همیشه با خود شماست: نام، شناسه‌های دائمی، انتشار، پرداخت و حساب‌ها.
  هیچ چیزی آپلود نمی‌شود مگر اینکه خودتان همان آپلود را درخواست کنید، و هیچ نسخه‌ای برای بررسی یا عموم فرستاده نمی‌شود پیش از آنکه روی دستگاه خودتان تست و تأیید کنید.

**پروژه‌ی موجود:** در پوشه‌ی پروژه بنویسید: «روش flagship-method را روی این پروژه پیاده کن.» هیچ
فایل موجودی بازنویسی نمی‌شود. اگر بعضی از فایل‌های اسناد از قبل وجود داشته باشند، همه‌ی اسناد در
پوشه‌ی جداگانه‌ی `.flagship-kit/` آماده می‌شوند تا دستی ادغام شوند.

**سه اسکریپت**
- `init_kit.py`: اسناد پروژه را می‌سازد (اول با `--dry-run`) و با `--check` جاهای پرنشده را با شماره‌ی خط نشان می‌دهد.
- `contact_sheet.py`: تصویرهای رندرشده را در یک برگه یا نوار فیلم کنار هم می‌چیند تا با چشم مقایسه شوند.
- `code_reviews.py`: نظرهای کاربران رقبا در فروشگاه را موضوع‌به‌موضوع می‌شمارد: شکایت‌ها، آنچه کاربران دوست دارند، و فاصله‌ی امتیاز فروشگاه با میانگین نظرهای اخیر.
