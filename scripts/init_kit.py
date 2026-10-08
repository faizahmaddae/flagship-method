#!/usr/bin/env python3
"""init_kit.py: scaffold the flagship-method doc kit into a project, or check a kit for unfilled
TODO markers. Standard library only (Python 3.8+).

<skill-dir> is the folder that holds the flagship-method SKILL.md, for example
~/.claude/skills/flagship-method. Run the script from anywhere, always pass --dest (the project
root), and never point --dest at the skill folder itself.

Scaffold: a dry run first, then the same command without --dry-run.

    python3 <skill-dir>/scripts/init_kit.py --dest <project-root> --kind app|game \\
        --name "Calm Ledger" --slug calm-ledger --one-line "What it is, in one sentence." \\
        --owner "Sam" --language "English" --stack "Flutter 3.x" --platforms "iPhone, Android phones" \\
        [--with-monetization] [--with-release] --dry-run

Check: lists every remaining TODO marker as file:line and exits 1 while any remain.

    python3 <skill-dir>/scripts/init_kit.py --check --dest <project-root> --slug calm-ledger

Existing project: if any kit file already exists, add --retrofit. The whole kit is then staged in
<project-root>/.flagship-kit/ (or in --stage DIR, which always stages) with a MERGE.md listing what
to merge by hand and what to move into place. No existing file is ever touched.

What it writes (relative to --dest, or to the staging folder):
    CLAUDE.md                                <- templates/CLAUDE.md
    .claude/skills/<slug>-builder/SKILL.md   <- templates/project-skill/SKILL.md.template
    docs/<slug>/<file>                       <- every other template; MONETIZATION.md only with
                                                --with-monetization, RELEASE.md only with --with-release
    docs/<slug>/research/README.md, docs/<slug>/reference/README.md   (unless a template gives them)
    docs/<slug>/research/.gitignore           (raw/: raw third-party text stays out of git)
A trailing ".template" is dropped from every name. Template files or folders whose name starts with
"." or "_" are notes for the template author and are never copied. Templates come from --templates,
else $FLAGSHIP_TEMPLATES, else ../assets/templates next to this script.

Blocks, in every template, may span lines; the markers are removed:
    <!-- kind:game --> ... <!-- /kind:game -->            kept only with --kind game
    <!-- kind:app --> ... <!-- /kind:app -->              kept only with --kind app
    <!-- if:monetization --> ... <!-- /if:monetization --> kept only with --with-monetization
    <!-- if:release --> ... <!-- /if:release -->          kept only with --with-release
An unbalanced, crossed, unknown or malformed marker is an error naming file:line; nothing is written.

Placeholders {{PROJECT_NAME}} {{SLUG}} {{ONE_LINE}} {{OWNER}} {{OWNER_LANGUAGE}} {{STACK}}
{{PLATFORMS}} {{DATE}} are filled from the flags (blocks first, then placeholders). Any other {{NAME}},
or a known one whose flag was not given, becomes the marker [TODO: NAME], listed with file and line.
Values are inserted literally and never scanned again.

Exit codes. Scaffold: 0 written, staged, or a clean dry run; 1 bad input or bad templates; 2 a kit
file exists (without --retrofit) or the staging folder already holds kit files. Check: 0 no marker
left; 1 markers or builder-frontmatter problems remain (or bad input); 2 no complete kit found.
There is deliberately no --force.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import os
import re
import shlex
import sys
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Sequence, TextIO, Tuple

KNOWN = ("PROJECT_NAME", "SLUG", "ONE_LINE", "OWNER", "OWNER_LANGUAGE", "STACK", "PLATFORMS", "DATE")
PLACEHOLDER = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")
SLUG_OK = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SLUG_MAX = 40
SUFFIX = ".template"
BUILDER_TEMPLATE = "project-skill/SKILL.md" + SUFFIX
REQUIRED_TEMPLATES = ("CLAUDE.md", BUILDER_TEMPLATE)
ENV_TEMPLATES = "FLAGSHIP_TEMPLATES"
ENV_CHILD = "FLAGSHIP_INIT_KIT_SELFTEST_CHILD"  # set in mutant copies
STAGE_DEFAULT = ".flagship-kit"
MERGE_NOTE = "MERGE.md"
MARKER = "[TODO"
TODO_LIST_MAX = 40
SENTENCE_END = ".!?…。؟"  # checked after any closing quote or bracket
KINDS = ("game", "app")
FLAGS = ("monetization", "release")
BLOCK = re.compile(r"<!--[ \t]*(/?)(kind|if):([a-z0-9-]+)[ \t]*-->")
BLOCK_LOOSE = re.compile(r"<!--\s*/?\s*(?:kind|if)\s*(?::|-->)")
EXTRA_FILES = (
    ("research/README.md",
     "# Research\n\nThe evidence behind RESEARCH.md: one dated report per research track, the scripts that\n"
     "produced every number, and the derived counts. Correct a report with a dated Errata block at its\n"
     "top, never silently. Raw third-party text (store reviews) goes in research/raw/, which the\n"
     ".gitignore here keeps out of git, unless its licence and privacy allow committing it.\n"),
    ("research/.gitignore",
     "# Raw third-party text (store reviews, forum posts) stays local. Remove this rule only after a\n"
     "# DECISIONS entry records that its licence and the authors' privacy allow committing it.\n"
     "raw/\n"),
    ("reference/README.md",
     "# Reference\n\nReference renders, identity probes and small tests that pin a library's real behaviour:\n"
     "API demos, not code to copy. Competitor screenshots never go in the repository.\n"),
)


class KitError(Exception):
    """Bad input or bad templates: exit 1 with this message."""


def default_templates() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "templates"


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def derive_slug(name: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    return slug[:SLUG_MAX].strip("-")


def check_slug(slug: str) -> None:
    if not slug:
        raise KitError("no slug could be derived from --name (it has no latin letters or digits): "
                       "pass --slug, e.g. --slug calm-ledger")
    if len(slug) > SLUG_MAX or not SLUG_OK.match(slug):
        raise KitError(f"slug {slug!r} is not usable: lowercase latin letters and digits, words joined by "
                       f"single hyphens, at most {SLUG_MAX} characters (e.g. calm-ledger)")


def _line(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def plan(templates: Path, slug: str, flags: Dict[str, bool]) -> List[Tuple[Path, str]]:
    """Every (template file, destination relative path) this run would render, sorted."""
    if not templates.is_dir():
        raise KitError(f"templates folder not found: {templates}")
    for need in REQUIRED_TEMPLATES:
        if not (templates / need).is_file():
            hint = ""
            if need == BUILDER_TEMPLATE and (templates / "project-skill" / "SKILL.md").is_file():
                hint = " (found project-skill/SKILL.md: rename it to SKILL.md.template)"
            raise KitError(f"templates folder is incomplete: {templates / need} is missing{hint}")
    out: List[Tuple[Path, str]] = []
    for src in sorted(p for p in templates.rglob("*") if p.is_file()):
        rel = src.relative_to(templates).as_posix()
        if any(part.startswith((".", "_")) for part in rel.split("/")):
            continue
        if src.name == "SKILL.md":
            raise KitError(f"template {rel} must be named SKILL.md.template: a second file named "
                           "SKILL.md inside the skill makes skill validators reject it")
        name = rel[:-len(SUFFIX)] if rel.endswith(SUFFIX) else rel
        if name == "CLAUDE.md":
            dest = "CLAUDE.md"
        elif name.startswith("project-skill/"):
            dest = f".claude/skills/{slug}-builder/" + name[len("project-skill/"):]
        elif name == "MONETIZATION.md" and not flags["monetization"]:
            continue
        elif name == "RELEASE.md" and not flags["release"]:
            continue
        else:
            dest = f"docs/{slug}/{name}"
        out.append((src, dest))
    return out


def _keeps(tag: str, name: str, kind: str, flags: Dict[str, bool]) -> bool:
    if tag == "kind":
        return name == kind
    return flags[name]


def _marker_spans(text: str, tokens: Sequence["re.Match[str]"]) -> List[Tuple[int, int]]:
    """Where each marker is cut. A line holding only markers and blanks goes entirely."""
    spans = [(m.start(), m.end()) for m in tokens]
    by_line: Dict[int, List[int]] = {}
    for i, m in enumerate(tokens):
        by_line.setdefault(text.rfind("\n", 0, m.start()) + 1, []).append(i)
    for start, idx in by_line.items():
        nl = text.find("\n", start)
        end = len(text) if nl < 0 else nl + 1
        rest = BLOCK.sub("", text[start:end])
        if rest.strip():
            continue
        for k, i in enumerate(idx):
            s = start if k == 0 else tokens[i].start()
            e = tokens[idx[k + 1]].start() if k + 1 < len(idx) else end
            spans[i] = (s, e)
    return spans


def apply_blocks(text: str, rel: str, kind: str, flags: Dict[str, bool]) -> str:
    """Keeps or drops every kind:/if: block; raises KitError on any bad marker."""
    tokens = list(BLOCK.finditer(text))
    strict = {m.start() for m in tokens}
    for m in BLOCK_LOOSE.finditer(text):
        if m.start() not in strict:
            end = text.find("-->", m.start())
            bad = text[m.start():end + 3 if end >= 0 else m.end()]
            raise KitError(f"{rel}:{_line(text, m.start())}: malformed block marker {bad[:60]!r} "
                           "(write <!-- kind:game --> ... <!-- /kind:game -->, no spaces around ':')")
    for m in tokens:
        tag, name = m.group(2), m.group(3)
        if name not in (KINDS if tag == "kind" else FLAGS):
            allowed = ", ".join(f"{tag}:{n}" for n in (KINDS if tag == "kind" else FLAGS))
            raise KitError(f"{rel}:{_line(text, m.start())}: unknown block {tag}:{name} (known: {allowed})")
    out: List[str] = []
    stack: List[Tuple[str, str, int, bool]] = []
    pos = 0
    for m, (s, e) in zip(tokens, _marker_spans(text, tokens)):
        if all(keep for _, _, _, keep in stack):
            out.append(text[pos:s])
        closing, tag, name, line = m.group(1) == "/", m.group(2), m.group(3), _line(text, m.start())
        if closing:
            if not stack:
                raise KitError(f"{rel}:{line}: <!-- /{tag}:{name} --> closes a block that was never opened")
            otag, oname, oline, _ = stack[-1]
            if (otag, oname) != (tag, name):
                raise KitError(f"{rel}:{line}: <!-- /{tag}:{name} --> arrives while {otag}:{oname} "
                               f"(opened at line {oline}) is still open; blocks must nest")
            stack.pop()
        else:
            for otag, oname, oline, _ in stack:
                if otag == "kind" and tag == "kind":
                    raise KitError(f"{rel}:{line}: kind:{name} inside kind:{oname} (line {oline}) "
                                   "is never kept as intended; close one kind block before the next")
                if (otag, oname) == (tag, name):
                    raise KitError(f"{rel}:{line}: {tag}:{name} opened again inside itself (line {oline})")
            stack.append((tag, name, line, _keeps(tag, name, kind, flags)))
        pos = e
    if stack:  # unclosed
        tag, name, line, _ = stack[-1]
        raise KitError(f"{rel}:{line}: <!-- {tag}:{name} --> is never closed")
    out.append(text[pos:])
    return "".join(out)


def fill(text: str, values: Dict[str, Optional[str]]) -> Tuple[str, List[Tuple[int, str]]]:
    """Text with placeholders replaced, and the (line, NAME) of every one left as a TODO marker."""
    unresolved: List[Tuple[int, str]] = []
    pieces: List[str] = []
    last = 0
    for m in PLACEHOLDER.finditer(text):
        name = m.group(1)
        value = values.get(name)
        pieces.append(text[last:m.start()])
        if value:
            pieces.append(value)
        else:
            pieces.append(f"[TODO: {name}]")
            unresolved.append((_line(text, m.start()), name))
        last = m.end()
    pieces.append(text[last:])
    return "".join(pieces), unresolved


def render_kit(templates: Path, slug: str, kind: str, flags: Dict[str, bool],
               values: Dict[str, Optional[str]]) -> Tuple[List[Tuple[str, bytes]], List[Tuple[str, int, str]]]:
    rendered: List[Tuple[str, bytes]] = []
    todo: List[Tuple[str, int, str]] = []
    for src, rel in plan(templates, slug, flags):
        raw = src.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            rendered.append((rel, raw))  # not text: copied byte for byte
            continue
        filled, left = fill(apply_blocks(text, rel, kind, flags), values)
        rendered.append((rel, filled.encode("utf-8")))
        todo.extend((rel, line, name) for line, name in left)
    planned = {rel for rel, _ in rendered}
    for sub, body in EXTRA_FILES:
        if f"docs/{slug}/{sub}" not in planned:
            rendered.append((f"docs/{slug}/{sub}", body.encode("utf-8")))
    rendered.sort(key=lambda item: item[0])
    return rendered, todo


def markers(text: str) -> List[Tuple[int, int, str]]:
    """(line, count, line text) for every line holding a TODO marker."""
    return [(n, line.count(MARKER), line.strip())
            for n, line in enumerate(text.splitlines(), 1) if MARKER in line]


def frontmatter_problems(text: str, slug: str) -> List[str]:
    """What a skill validator would reject in the builder skill's frontmatter."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ["no frontmatter: the first line must be ---"]
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return ["the frontmatter is never closed with ---"]
    fm, name, desc, problems = lines[1:end], None, None, []
    i = 0
    while i < len(fm):
        m = re.match(r"^(name|description):[ \t]*(.*)$", fm[i])
        i += 1
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if key == "name":
            name = val.strip("'\"")
        elif val in (">", ">-", ">+", "|", "|-", "|+"):
            parts = []
            while i < len(fm) and (fm[i][:1] in (" ", "\t") or not fm[i].strip()):
                parts.append(fm[i].strip())
                i += 1
            desc = " ".join(p for p in parts if p)
        else:
            if val[:1] not in ("'", '"') and (": " in val or " #" in val):
                problems.append("the description is a plain YAML scalar containing ': ' or ' #'; "
                                "use a folded block (description: >-)")
            desc = val.strip("'\"")
    if name != f"{slug}-builder":
        problems.append(f"name is {name!r}; it must be {slug + '-builder'!r}, the folder's name")
    if not desc:
        problems.append("the description is missing or empty")
    else:
        if len(desc) > 1024:
            problems.append(f"the description is {len(desc)} characters; the limit is 1024")
        if "<" in desc or ">" in desc:
            problems.append("the description contains '<' or '>'; skill validators reject angle brackets")
    return problems


def conflicts(root: Path, targets: Sequence[str]) -> List[str]:
    """Targets that exist already, or whose parent path is blocked by a file."""
    found: List[str] = []
    for rel in targets:
        path = root / rel
        if os.path.lexists(path):
            found.append(rel)
            continue
        parent = path.parent
        while parent != root and parent != parent.parent:
            if os.path.lexists(parent) and not parent.is_dir():
                found.append(f"{rel} (blocked: {parent.relative_to(root).as_posix()} is a file)")
                break
            parent = parent.parent
    return found


def check_command(dest: Path, slug: str) -> str:
    script = shlex.quote(str(Path(__file__).resolve()))
    return f"python3 {script} --check --dest {shlex.quote(str(dest))} --slug {slug}"


def _usage() -> str:
    """The Scaffold / Check / Existing project part of the module docstring (empty under -OO)."""
    doc = __doc__ or ""
    start, end = doc.find("Scaffold:"), doc.find("What it writes")
    return doc[start:end].rstrip() if 0 <= start < end else ""


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="init_kit.py", formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Scaffold the flagship-method doc kit into a project (never overwrites), or check a "
                    "kit for unfilled TODO markers.\n<skill-dir> is the folder holding the flagship-method "
                    "SKILL.md, e.g. ~/.claude/skills/flagship-method.",
        epilog=_usage())
    p.add_argument("--dest", help="the project root to write into or check (required; never the skill folder)")
    p.add_argument("--kind", help="game or app (required to scaffold): selects the templates' kind blocks")
    p.add_argument("--name", help="the project's working name as people say it, e.g. 'Calm Ledger'")
    p.add_argument("--slug", help="internal id for docs/<slug>/ and <slug>-builder: lowercase words joined "
                                  "by hyphens (default: from --name). Renaming the product later does not "
                                  "require renaming the slug.")
    p.add_argument("--one-line", dest="one_line", help="what it is, in one sentence ending with a full stop "
                                                       "(the templates start a new sentence after it)")
    p.add_argument("--owner", help="the owner's name as they want it written, or \"the owner\"")
    p.add_argument("--language", help="the language the owner is asked questions in, e.g. 'English'")
    p.add_argument("--stack", help="e.g. 'Flutter 3.x, Riverpod 3' or 'React Native with Expo'")
    p.add_argument("--platforms", help="e.g. 'iPhone (portrait), Android phones'")
    p.add_argument("--with-monetization", action="store_true",
                   help="write MONETIZATION.md and keep if:monetization blocks (it earns money or collects data)")
    p.add_argument("--with-release", action="store_true",
                   help="write RELEASE.md and keep if:release blocks (it ships to a store or production)")
    p.add_argument("--retrofit", action="store_true",
                   help=f"existing project: if any kit file exists, stage the whole kit in <dest>/{STAGE_DEFAULT}/")
    p.add_argument("--stage", help="with --retrofit: stage the kit in this folder instead (always stages)")
    p.add_argument("--check", action="store_true",
                   help="list remaining TODO markers by file:line (needs --dest and --slug); exit 1 if any")
    p.add_argument("--date", help="YYYY-MM-DD for {{DATE}} (default: today)")
    p.add_argument("--templates", help=f"template folder (default: ${ENV_TEMPLATES}, else ../assets/templates)")
    p.add_argument("--dry-run", action="store_true", help="print the plan and the markers; write nothing")
    p.add_argument("--force", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--selftest", action="store_true", help="prove this script works, in a temp folder")
    return p


def main(argv: Optional[Sequence[str]] = None, out: TextIO = sys.stdout, err: TextIO = sys.stderr) -> int:
    args = build_parser().parse_args(argv)
    if args.selftest:
        return selftest()
    if args.force:
        print("init_kit: there is no --force; init_kit never overwrites. For an existing project use "
              "--retrofit, which stages the kit for a hand merge.", file=err)
        return 2
    try:
        return _check(args, out) if args.check else _run(args, out, err)
    except KitError as e:
        print(f"init_kit: {e}", file=err)
        return 1


def _dest(args: argparse.Namespace) -> Path:
    if not args.dest:
        raise KitError("--dest is required: the project root (init_kit never guesses it)")
    dest = Path(args.dest).expanduser().resolve()
    if not dest.is_dir():
        raise KitError(f"--dest is not an existing folder: {dest}")
    return dest


def _check(args: argparse.Namespace, out: TextIO) -> int:
    dest = _dest(args)
    if not args.slug:
        raise KitError("--check needs --slug (the kit's docs/<slug>/ folder name)")
    check_slug(args.slug)
    slug = args.slug
    builder = f".claude/skills/{slug}-builder"
    roots = ("CLAUDE.md", builder, f"docs/{slug}")
    missing = [r for r in roots if not (dest / r).exists()]
    if missing:
        print(f"init_kit --check: no complete kit for slug {slug!r} under {dest}; missing: "
              f"{', '.join(missing)}. Point --dest at the folder that holds the kit.", file=out)
        return 2
    files = [dest / "CLAUDE.md"] + sorted(p for r in roots[1:] for p in (dest / r).rglob("*") if p.is_file())
    hits: List[Tuple[str, int, int, str]] = []
    scanned = 0
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # binary or unreadable: no markers to find
        scanned += 1
        rel = f.relative_to(dest).as_posix()
        hits.extend((rel, n, c, line) for n, c, line in markers(text))
    skill_md = dest / builder / "SKILL.md"
    problems = frontmatter_problems(skill_md.read_text(encoding="utf-8"), slug) if skill_md.is_file() \
        else ["SKILL.md is missing"]
    if hits:
        total = sum(c for _, _, c, _ in hits)
        per: Dict[str, int] = {}
        for rel, _, c, _ in hits:
            per[rel] = per.get(rel, 0) + c
        print(f"init_kit --check: {total} TODO markers left in {len(per)} files under {dest}", file=out)
        for rel, n, _, line in hits:
            print(f"{rel}:{n}: {line[:100]}", file=out)
        print("Per file: " + ", ".join(f"{rel} {c}" for rel, c in sorted(per.items(), key=lambda x: -x[1])),
              file=out)
    for problem in problems:
        print(f"{builder}/SKILL.md frontmatter: {problem}", file=out)
    failed = bool(hits or problems)
    if not failed:
        print(f"init_kit --check: no TODO markers left ({scanned} files scanned in CLAUDE.md, {builder}/ "
              f"and docs/{slug}/); builder frontmatter valid", file=out)
    return 1 if failed else 0


def _run(args: argparse.Namespace, out: TextIO, err: TextIO) -> int:
    if args.stage and not args.retrofit:
        raise KitError("--stage needs --retrofit")
    dest = _dest(args)
    root_of_skill = skill_root()
    if dest == root_of_skill or root_of_skill in dest.parents:
        raise KitError(f"--dest {dest} is inside the flagship-method skill folder; pass --dest <project root>")
    if not args.kind:
        raise KitError("--kind is required: game or app (it selects the templates' kind:game or kind:app blocks)")
    if args.kind not in KINDS:
        raise KitError(f"--kind must be game or app, not {args.kind!r}")
    if not args.name or not args.name.strip():
        raise KitError("--name is required (the project's working name as people say it)")
    slug = args.slug if args.slug is not None else derive_slug(args.name)
    check_slug(slug)
    date = args.date or _dt.date.today().isoformat()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        raise KitError(f"--date {date!r} is not YYYY-MM-DD")
    values: Dict[str, Optional[str]] = {
        "PROJECT_NAME": args.name, "SLUG": slug, "ONE_LINE": args.one_line, "OWNER": args.owner,
        "OWNER_LANGUAGE": args.language, "STACK": args.stack, "PLATFORMS": args.platforms, "DATE": date,
    }
    for key, value in list(values.items()):
        if value is None:
            continue
        if "\n" in value or "\r" in value:
            raise KitError(f"the value for {{{{{key}}}}} must be one line")
        values[key] = value.strip() or None

    templates = Path(args.templates or os.environ.get(ENV_TEMPLATES) or default_templates()).resolve()
    flags = {"monetization": args.with_monetization, "release": args.with_release}
    rendered, todo = render_kit(templates, slug, args.kind, flags, values)
    existing = conflicts(dest, [rel for rel, _ in rendered])
    if existing and not args.retrofit:
        print(f"init_kit: refusing to overwrite. These already exist under {dest}:", file=err)
        for rel in existing:
            print(f"  {rel}", file=err)
        print(f"Nothing was written. To adopt the kit in an existing project, rerun with --retrofit: the "
              f"whole kit is staged in {dest / STAGE_DEFAULT} with merge instructions, and no existing "
              "file is touched.", file=err)
        return 2

    root, writes = dest, list(rendered)
    exist_rels = {e.split(" (blocked")[0] for e in existing}
    staging = bool(args.stage) or bool(existing)
    if staging:
        stage_dir = Path(args.stage).expanduser().resolve() if args.stage else dest / STAGE_DEFAULT
        if os.path.lexists(stage_dir) and not stage_dir.is_dir():
            raise KitError(f"the staging path is a file, not a folder: {stage_dir}")
        root = stage_dir
        note = merge_note(args.name, slug, rendered, exist_rels, dest, stage_dir, date)
        writes.append((MERGE_NOTE, note.encode("utf-8")))
        held = conflicts(root, [rel for rel, _ in writes])
        if held:
            print(f"init_kit: the staging folder {root} already holds kit files:", file=err)
            for rel in held:
                print(f"  {rel}", file=err)
            print("Nothing was written. Finish or move that staged kit first, or pass --stage <another "
                  "folder>.", file=err)
            return 2

    if not args.dry_run:
        written: List[str] = []
        for rel, data in writes:
            path = root / rel
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                with open(path, "xb") as fh:  # "x": fail rather than overwrite, even in a race
                    fh.write(data)
            except OSError as e:
                print(f"init_kit: stopped at {rel}: {e}", file=err)
                if written:
                    print("Already written by this run (yours to keep or delete):", file=err)
                    for done in written:
                        print(f"  {done}", file=err)
                return 2 if isinstance(e, FileExistsError) else 1
            written.append(rel)

    if staging:
        verb = "would stage" if args.dry_run else "staged"
        n = len(existing)
        why = f"{n} kit file{'s' if n != 1 else ''} already in the project" if n else "--stage given"
        print(f"init_kit: {verb} {len(writes)} files into {root} ({why}); nothing outside it is touched",
              file=out)
        for rel, _ in writes:
            tag = ("these instructions" if rel == MERGE_NOTE else
                   "exists in the project: merge by hand" if rel in exist_rels else "new: move into place")
            print(f"  {rel}  ({tag})", file=out)
    else:
        verb = "would write" if args.dry_run else "wrote"
        print(f"init_kit: {verb} {len(writes)} files into {root}", file=out)
        for rel, _ in writes:
            print(f"  {rel}", file=out)
    if todo:
        tally: Dict[str, int] = {}
        for _, _, name in todo:
            tally[name] = tally.get(name, 0) + 1
        summary = ", ".join(f"{name} x{n}" for name, n in sorted(tally.items()))
        print(f"Values not given, left as TODO markers ({len(todo)}): {summary}", file=out)
        for rel, line, name in todo[:TODO_LIST_MAX]:
            print(f"  {rel}:{line}  [TODO: {name}]", file=out)
        if len(todo) > TODO_LIST_MAX:
            print(f"  ... and {len(todo) - TODO_LIST_MAX} more (--check lists every marker)", file=out)
    per = [(rel, sum(c for _, c, _ in markers(data.decode("utf-8", "replace")))) for rel, data in rendered]
    per = sorted(((rel, c) for rel, c in per if c), key=lambda x: (-x[1], x[0]))
    print(f"TODO markers to fill: {sum(c for _, c in per)} in {len(per)} files", file=out)
    for rel, c in per:
        print(f"  {rel}  {c}", file=out)
    one_line = values["ONE_LINE"]
    if one_line and one_line.rstrip("\"')]»”’")[-1:] not in tuple(SENTENCE_END):
        print(f"warning: --one-line {one_line!r} has no closing full stop; the templates start a new sentence "
              "right after it", file=out)
    builder = f".claude/skills/{slug}-builder/SKILL.md"
    for rel, data in rendered:
        if rel == builder:
            for problem in frontmatter_problems(data.decode("utf-8", "replace"), slug):
                print(f"warning: {builder} frontmatter: {problem}", file=out)
    if args.dry_run:
        print("Dry run: nothing was written. Run the same command without --dry-run.", file=out)
    elif staging:
        print(f"Next: follow {root / MERGE_NOTE}, delete the staging folder, then run", file=out)
        print(f"  {check_command(dest, slug)}", file=out)
    else:
        print("Next: fill the kit from the kickoff (flagship-method references/kickoff.md, \"Write the "
              "kit\"), then run", file=out)
        print(f"  {check_command(dest, slug)}", file=out)
        print("until it reports none left; then the kit review (references/kickoff.md, \"Review the kit\"; "
              "checklist: references/project-kit.md, \"Kit health checklist\").", file=out)
    return 0


def merge_note(name: str, slug: str, rendered: Sequence[Tuple[str, bytes]], existing: set,
               dest: Path, stage: Path, date: str) -> str:
    try:
        shown = stage.relative_to(dest).as_posix()
    except ValueError:
        shown = str(stage)
    lines = [
        f"# Merging the flagship-method kit into {name}", "",
        f"init_kit.py staged this kit on {date}. Nothing outside this folder was written or changed.",
        "The retrofit order (run and render the project as found; the goal sheet and the owner questions;",
        "research; identity; this merge; the kit review; Gate 0; the adoption baseline) is in the",
        "flagship-method skill: references/planning-and-slices.md, section Retrofit.", "",
        "## Already in the project: merge by hand", "",
        "Keep everything that is true about the project and add the kit sections it lacks, written from",
        "the project's real state, not the template's assumptions. Never delete the owner's content",
        "without asking. Record each merge choice in DECISIONS.", "",
    ]
    lines += [f"- `{rel}`: merge `{shown}/{rel}` into it." for rel, _ in rendered if rel in existing] or ["- none"]
    lines += ["", "## Not in the project yet: move into place", ""]
    lines += [f"- `{shown}/{rel}` to `{rel}`" for rel, _ in rendered if rel not in existing] or ["- none"]
    lines += ["", "## Then", "", "1. Delete this folder; never commit it.",
              f"2. Run `{check_command(dest, slug)}` until it reports none left.", ""]
    return "\n".join(lines)


def selftest() -> int:
    """Runs the cases in init_kit_selftest.py next to this file (loaded by path, so -I is fine)."""
    path = Path(__file__).resolve().with_name("init_kit_selftest.py")
    if not path.is_file():
        print(f"init_kit: the selftest needs {path.name} next to this script", file=sys.stderr)
        return 1
    sys.dont_write_bytecode = True  # leave no __pycache__ inside the installed skill
    spec = importlib.util.spec_from_file_location("init_kit_selftest", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module.run(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())
