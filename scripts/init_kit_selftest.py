#!/usr/bin/env python3
"""init_kit_selftest.py: the cases behind `python3 init_kit.py --selftest`. Standard library only.

init_kit.py loads this file by path and calls run(<the init_kit module>). The cases use fake templates
in a temp folder, so they never depend on the shipped ones; every expectation is a literal written
here. Then, unless FLAGSHIP_INIT_KIT_SELFTEST_CHILD is set, it lints the shipped templates in every
kind and flag combination, and proves each core feature's cases by mutation: the feature is removed in
a temp copy of init_kit.py, and the copy's selftest must fail at the named case.
"""

from __future__ import annotations

import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Dict, List, Optional, Sequence, Tuple

K: ModuleType  # the init_kit module under test, set by run()

FAKE_TEMPLATES = {
    "CLAUDE.md": (
        "# {{PROJECT_NAME}} — {{ONE_LINE}}\nOwner: {{OWNER}} ({{OWNER_LANGUAGE}})\n"
        "Stack: {{STACK}} on {{PLATFORMS}}\nDocs: docs/{{SLUG}}/\nRule: {{CORE_RULE}}\nDated {{DATE}}\n"
        "<!-- kind:game -->\nJudge the player by the rules.\n<!-- /kind:game -->\n"
        "<!-- kind:app -->\nNever lose the user's data.\n<!-- /kind:app -->\n"
        "<!-- if:monetization -->\n7. docs/{{SLUG}}/MONETIZATION.md\n<!-- /if:monetization -->\n"
        "<!-- if:release -->\n8. docs/{{SLUG}}/RELEASE.md\n<!-- /if:release -->\n"
        "Mode: <!-- kind:game -->play<!-- /kind:game --><!-- kind:app -->use<!-- /kind:app --> it.\nEnd\n"
    ),
    "project-skill/SKILL.md.template":
        "---\nname: {{SLUG}}-builder\ndescription: >-\n  Builds {{PROJECT_NAME}}.\n---\n# Builder\n[TODO: bans]\n",
    "PROGRESS.md": "# PROGRESS — {{PROJECT_NAME}}\nUpdated {{DATE}}\n[TODO: the exact next step]\n",
    "PLAN.md": "# PLAN\nGate with {{OWNER}}\n",
    "MONETIZATION.md": "# MONETIZATION — {{PROJECT_NAME}}\n",
    "RELEASE.md": "# RELEASE\n",
    "_AUTHORING.md": "notes for the template author; never copied\n",
}
FULL_ARGS = ["--kind", "game", "--name", "Demo Game", "--slug", "demo", "--one-line", "A tiny puzzle",
             "--owner", "Sam", "--language", "فارسی", "--stack", "Flutter", "--platforms", "iOS, Android",
             "--date", "2026-10-08"]
EXPECTED_FILES = {"CLAUDE.md", ".claude/skills/demo-builder/SKILL.md", "docs/demo/PROGRESS.md",
                  "docs/demo/PLAN.md", "docs/demo/MONETIZATION.md", "docs/demo/research/README.md",
                  "docs/demo/research/.gitignore", "docs/demo/reference/README.md"}
HEAD = ("# Demo Game — A tiny puzzle\nOwner: Sam (فارسی)\nStack: Flutter on iOS, Android\nDocs: docs/demo/\n"
        "Rule: [TODO: CORE_RULE]\nDated 2026-10-08\n")
EXPECTED_GAME = HEAD + "Judge the player by the rules.\n7. docs/demo/MONETIZATION.md\nMode: play it.\nEnd\n"
EXPECTED_APP = HEAD + "Never lose the user's data.\nMode: use it.\nEnd\n"
MUTANTS = (  # (feature, code to find in init_kit.py, its replacement, a FAIL it must cause)
    ("marker", 'f"[TODO: {name}]"', 'f"TODO({name})"', "unfilled placeholder becomes [TODO: NAME]"),
    ("slug default", '"-", ascii_name.lower()', '"_", ascii_name.lower()', "slug derived with hyphens"),
    ("slug check", r'r"^[a-z0-9]+(-[a-z0-9]+)*$"', r'r"^[a-z0-9_-]+$"', "--slug my_app refused"),
    ("block choice", "return name == kind", "return True", "--kind app keeps only the app blocks"),
    ("block balance", "if stack:  # unclosed", "if False:", "an unclosed block is refused, file:line named"),
    ("retrofit", "root = stage_dir", "root = dest", "retrofit exits 0 and stages"),
    ("check", "return 1 if failed else 0", "return 0", "--check exits 1 while markers remain"),
    ("folders", 'f"docs/{slug}/{sub}" not in planned', "False", "writes exactly the expected files"),
)


def _files(root: Path) -> Dict[str, str]:
    """Every file under root: relative path -> sha256."""
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def _call(argv: Sequence[str]) -> Tuple[int, str, str]:
    """Runs main in-process. A crash becomes rc -1, so a case fails by assertion, not by traceback."""
    o, e = io.StringIO(), io.StringIO()
    try:
        rc = K.main(list(argv), out=o, err=e)
    except SystemExit as ex:  # argparse
        return (ex.code if isinstance(ex.code, int) else 1), o.getvalue(), e.getvalue()
    except Exception as ex:  # noqa: BLE001 - the selftest must report, not die
        return -1, o.getvalue(), e.getvalue() + f"\nCRASH: {type(ex).__name__}: {ex}"
    return rc, o.getvalue(), e.getvalue()


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def run(kit: ModuleType) -> int:
    global K
    K = kit
    failures: List[str] = []
    count = 0

    def case(label: str, ok: bool, detail: str = "") -> None:
        nonlocal count
        count += 1
        if ok:
            print(f"  ok  {label}")
        else:
            failures.append(label)
            print(f"FAIL  {label}: {detail[:600]}")

    with tempfile.TemporaryDirectory(prefix="init_kit_selftest_") as tmp_name:
        tmp = Path(tmp_name)

        def templates(name: str, files: Dict[str, str]) -> List[str]:
            d = tmp / name
            for rel, text in files.items():
                (d / rel).parent.mkdir(parents=True, exist_ok=True)
                (d / rel).write_text(text, encoding="utf-8")
            return ["--templates", str(d)]

        def fresh(name: str) -> Path:
            d = tmp / name
            d.mkdir()
            return d

        t = templates("tpl", FAKE_TEMPLATES)
        skill_tpl = {"project-skill/SKILL.md.template": FAKE_TEMPLATES["project-skill/SKILL.md.template"]}

        # 1. Full run, kind game, with monetization: exact files, blocks resolved, values filled.
        p1 = fresh("p1")
        rc, out, err = _call(FULL_ARGS + t + ["--dest", str(p1), "--with-monetization"])
        case("full run exits 0", rc == 0, f"rc={rc} err={err!r}")
        got = set(_files(p1))
        case("writes exactly the expected files", got == EXPECTED_FILES,
             f"missing={sorted(EXPECTED_FILES - got)} extra={sorted(got - EXPECTED_FILES)}")
        case("--kind game keeps game and monetization blocks, drops the rest", _read(p1 / "CLAUDE.md") ==
             EXPECTED_GAME, repr(_read(p1 / "CLAUDE.md")))
        case("SKILL.md.template becomes the <slug>-builder SKILL.md",
             _read(p1 / ".claude/skills/demo-builder/SKILL.md").startswith("---\nname: demo-builder\n"),
             _read(p1 / ".claude/skills/demo-builder/SKILL.md")[:80])
        texts = {rel: _read(p1 / rel) for rel in got}
        case("no {{…}} or block marker left", not [r for r, x in texts.items() if "{{" in x or "<!--" in x])
        case("unfilled placeholder becomes [TODO: NAME]", "Rule: [TODO: CORE_RULE]\n" in texts.get("CLAUDE.md", "")
             and "CLAUDE.md:5  [TODO: CORE_RULE]" in out, out[-600:])
        case("marker report counts every TODO marker per file", "TODO markers to fill: 3 in 3 files" in out
             and "  docs/demo/PROGRESS.md  1" in out, out[-400:])
        case("research/ and reference/ READMEs carry no marker",
             all(x and K.MARKER not in x for r, x in texts.items() if r.endswith("/README.md")), str(sorted(got)))
        case("research/.gitignore keeps raw/ out of git", "\nraw/\n" in texts.get("docs/demo/research/.gitignore", ""),
             repr(texts.get("docs/demo/research/.gitignore")))
        case("RELEASE.md skipped without --with-release", not (p1 / "docs/demo/RELEASE.md").exists())
        case("underscore template note never copied", not any("_AUTHORING" in r for r in got))
        nxt = [ln.strip() for ln in out.splitlines() if "--check --dest" in ln]
        case("Next names the --check command", len(nxt) == 1 and K.MARKER not in nxt[0], out[-300:])
        case("a one-line without a full stop is warned about", "has no closing full stop" in out, out[-300:])
        stops = []
        for i, one in enumerate(("A tiny puzzle.", 'It says "done."', "یک پازل کوچک؟")):
            argv = list(FULL_ARGS)
            argv[argv.index("A tiny puzzle")] = one
            stops.append(_call(argv + t + ["--dest", str(fresh(f"p_stop{i}")), "--dry-run"]))
        case("a one-line that ends a sentence is not warned about",
             all(rc == 0 and "full stop" not in o for rc, o, _ in stops), str([o[-200:] for _, o, _ in stops]))

        # 2. --check: lists markers by file:line, exit 1; clean after filling; never matches its own line.
        rc, out, _ = _call(["--check", "--dest", str(p1), "--slug", "demo"])
        case("--check exits 1 while markers remain", rc == 1 and "3 TODO markers left" in out, f"rc={rc} {out!r}")
        case("--check names file:line", "CLAUDE.md:5: Rule: [TODO: CORE_RULE]" in out
             and "docs/demo/PROGRESS.md:3:" in out, out)
        for rel in got:
            if not rel.endswith("README.md"):
                (p1 / rel).write_text(_read(p1 / rel).replace(K.MARKER, "[DONE"), encoding="utf-8")
        with open(p1 / "docs/demo/PROGRESS.md", "a", encoding="utf-8") as fh:
            fh.write("How to verify: " + (nxt[0] if nxt else "") + "   # lists any TODO marker\n")
        rc, out, _ = _call(["--check", "--dest", str(p1), "--slug", "demo"])
        case("--check exits 0 once filled, its own command line included", rc == 0 and "no TODO markers" in out,
             f"rc={rc} {out!r}")
        (p1 / "docs/demo/PLAN.md").write_text("cell [TODO]\n", encoding="utf-8")
        rc, out, _ = _call(["--check", "--dest", str(p1), "--slug", "demo"])
        case("--check catches a bare marker too", rc == 1 and "docs/demo/PLAN.md:1:" in out, out)
        rc, out, _ = _call(["--check", "--dest", str(fresh("nokit")), "--slug", "demo"])
        case("--check with no kit exits 2 (never a vacuous pass)", rc == 2 and "missing" in out, f"rc={rc} {out!r}")
        rc, _, err = _call(["--check", "--dest", str(p1)])
        case("--check without --slug refused", rc == 1 and "needs --slug" in err, f"rc={rc} {err!r}")
        bad_fm = templates("tpl_fm", {**FAKE_TEMPLATES, "project-skill/SKILL.md.template":
                                      "---\nname: {{SLUG}}-builder\ndescription: use <it>\n---\n"})
        p_fm = fresh("p_fm")
        _call(FULL_ARGS + bad_fm + ["--dest", str(p_fm)])
        rc, out, _ = _call(["--check", "--dest", str(p_fm), "--slug", "demo"])
        case("--check reports angle brackets in the builder description", rc == 1 and "'<' or '>'" in out, out)

        # 3. Kind app without the optional docs.
        p2 = fresh("p2")
        rc, out, err = _call([a if a != "game" else "app" for a in FULL_ARGS] + t + ["--dest", str(p2)])
        case("--kind app keeps only the app blocks", rc == 0 and _read(p2 / "CLAUDE.md") == EXPECTED_APP,
             f"rc={rc} {err!r} {_read(p2 / 'CLAUDE.md')!r}")
        rc, _, err = _call(FULL_ARGS[2:] + t + ["--dest", str(fresh("p_nokind"))])
        case("missing --kind refused", rc == 1 and "--kind is required" in err, f"rc={rc} {err!r}")
        rc, _, err = _call(["--kind", "tool"] + FULL_ARGS[2:] + t + ["--dest", str(fresh("p_badkind"))])
        case("unknown --kind refused", rc == 1 and "game or app" in err, f"rc={rc} {err!r}")

        # 4. Blocks: every malformed shape is refused with file:line, and nothing is written.
        bad_blocks = {
            "an unclosed block is refused, file:line named": ("a\n<!-- kind:game -->\nb\n", "CLAUDE.md:2:"),
            "a close without an open is refused": ("a\n<!-- /if:release -->\n", "never opened"),
            "crossed blocks are refused": ("<!-- kind:app -->\n<!-- if:release -->\n<!-- /kind:app -->\n"
                                           "<!-- /if:release -->\n", "must nest"),
            "an unknown block name is refused": ("<!-- if:ads -->x<!-- /if:ads -->\n", "unknown block if:ads"),
            "a malformed marker is refused": ("<!-- kind: game -->x<!-- /kind -->\n", "malformed block marker"),
            "a bare close marker is refused": ("x\n<!-- /kind -->\n", "malformed block marker"),
            "kind inside another kind is refused": ("<!-- kind:game --><!-- kind:app -->x<!-- /kind:app -->"
                                                    "<!-- /kind:game -->\n", "inside kind:game"),
        }
        for i, (label, (claude, want)) in enumerate(bad_blocks.items()):
            pb = fresh(f"pb{i}")
            rc, _, err = _call(FULL_ARGS + templates(f"tb{i}", {"CLAUDE.md": claude, **skill_tpl})
                               + ["--dest", str(pb)])
            case(label, rc == 1 and want in err and not any(pb.iterdir()), f"rc={rc} {err!r}")
        nested = templates("tn", {"CLAUDE.md": "<!-- kind:app -->\nA\n<!-- if:release -->\nR\n"
                                               "<!-- /if:release -->\n<!-- /kind:app -->\nZ\n", **skill_tpl})
        pn = fresh("pn")
        rc, _, _ = _call(["--kind", "app", "--name", "N", "--with-release", "--dest", str(pn)] + nested)
        case("nested if: inside kind: works", rc == 0 and _read(pn / "CLAUDE.md") == "A\nR\nZ\n",
             repr(_read(pn / "CLAUDE.md")))

        # 5. Refusals and retrofit staging.
        before = _files(p2)
        rc, out, err = _call([a if a != "game" else "app" for a in FULL_ARGS] + t + ["--dest", str(p2)])
        case("second run refuses with exit 2", rc == 2 and "\n  CLAUDE.md\n" in err, f"rc={rc} {err!r}")
        case("refusal points to --retrofit, never to deleting", "--retrofit" in err and "delete" not in err, err)
        case("refusal changes no byte", _files(p2) == before)
        p4 = fresh("p4")
        (p4 / "docs").write_text("a file, not a folder\n", encoding="utf-8")
        rc, _, err = _call(FULL_ARGS + t + ["--dest", str(p4)])
        case("a file blocking a folder refuses", rc == 2 and "blocked: docs is a file" in err, f"rc={rc} {err!r}")

        pr = fresh("pr")
        (pr / "CLAUDE.md").write_bytes(b"# existing\n")
        rc, out, err = _call(FULL_ARGS + t + ["--dest", str(pr), "--retrofit"])
        staged = set(_files(pr / K.STAGE_DEFAULT)) if (pr / K.STAGE_DEFAULT).is_dir() else set()
        case("retrofit exits 0 and stages", rc == 0 and staged == (EXPECTED_FILES - {"docs/demo/MONETIZATION.md"})
             | {K.MERGE_NOTE}, f"rc={rc} {err!r} {sorted(staged)}")
        case("retrofit leaves CLAUDE.md byte-identical and writes nothing outside the stage",
             (pr / "CLAUDE.md").read_bytes() == b"# existing\n"
             and {r for r in _files(pr) if not r.startswith(K.STAGE_DEFAULT + "/")} == {"CLAUDE.md"}, str(_files(pr)))
        note = _read(pr / K.STAGE_DEFAULT / K.MERGE_NOTE)
        case("MERGE.md says what to merge and what to move", "- `CLAUDE.md`: merge `.flagship-kit/CLAUDE.md`"
             in note and "`.flagship-kit/docs/demo/PLAN.md` to `docs/demo/PLAN.md`" in note and K.MARKER not in note,
             note[:500])
        case("retrofit output marks the conflict", "CLAUDE.md  (exists in the project: merge by hand)" in out, out)
        before = _files(pr)
        rc, _, err = _call(FULL_ARGS + t + ["--dest", str(pr), "--retrofit"])
        case("a second retrofit refuses: the stage is full", rc == 2 and "already holds" in err
             and _files(pr) == before, f"rc={rc} {err!r}")
        side = tmp / "side_stage"
        rc, _, _ = _call(FULL_ARGS + t + ["--dest", str(pr), "--retrofit", "--stage", str(side)])
        case("--stage DIR stages there", rc == 0 and (side / "CLAUDE.md").is_file() and _files(pr) == before)
        p_clean = fresh("p_clean")
        rc, _, _ = _call(FULL_ARGS + t + ["--dest", str(p_clean), "--retrofit"])
        case("retrofit with no conflict writes in place", rc == 0 and (p_clean / "CLAUDE.md").is_file()
             and not (p_clean / K.STAGE_DEFAULT).exists())
        rc, _, err = _call(FULL_ARGS + t + ["--dest", str(fresh("p_st")), "--stage", str(tmp / "s2")])
        case("--stage without --retrofit refused", rc == 1 and "--stage needs --retrofit" in err, err)
        p_rd = fresh("p_rd")
        (p_rd / "CLAUDE.md").write_bytes(b"x\n")
        rc, out, _ = _call(FULL_ARGS + t + ["--dest", str(p_rd), "--retrofit", "--dry-run"])
        case("retrofit dry run stages nothing", rc == 0 and "would stage" in out and set(_files(p_rd)) == {"CLAUDE.md"})

        # 6. Dry run, slugs, missing values, literal values.
        p5 = fresh("p5")
        rc, out, _ = _call(FULL_ARGS + t + ["--dest", str(p5), "--dry-run", "--with-release"])
        case("dry run writes nothing and lists the plan", rc == 0 and not any(p5.iterdir())
             and "would write 8 files" in out and "docs/demo/RELEASE.md" in out, out)
        p6 = fresh("p6")
        rc, out, err = _call(["--kind", "app", "--name", "My Cool App!", "--date", "2026-10-08",
                              "--dest", str(p6)] + t)
        case("slug derived with hyphens", rc == 0 and (p6 / ".claude/skills/my-cool-app-builder/SKILL.md").exists(),
             f"rc={rc} {err!r} {sorted(_files(p6))}")
        case("missing values become [TODO: NAME], listed", "Owner: [TODO: OWNER] ([TODO: OWNER_LANGUAGE])"
             in _read(p6 / "CLAUDE.md") and "docs/my-cool-app/PLAN.md:2  [TODO: OWNER]" in out, out[-500:])
        rc, out, _ = _call(["--kind", "app", "--name", "Café Noir", "--dry-run", "--dest", str(fresh("p6b"))] + t)
        case("accents fold into the slug", rc == 0 and "docs/cafe-noir/PLAN.md" in out, out)
        for i, (slug_arg, ok_rc) in enumerate((("my_app", 1), ("calm--ledger", 1), ("-calm", 1),
                                               ("Calm", 1), ("2048-clone", 0))):
            rc, _, err = _call(["--kind", "app", "--name", "X", f"--slug={slug_arg}", "--dry-run",
                                "--dest", str(fresh(f"ps{i}"))] + t)
            case(f"--slug {slug_arg} {'refused' if ok_rc else 'accepted'}", rc == ok_rc, f"rc={rc} {err!r}")
        rc, _, err = _call(["--kind", "app", "--name", "شمسه", "--dest", str(fresh("p_fa"))] + t)
        case("a name with no latin letters asks for --slug", rc == 1 and "pass --slug" in err, err)
        p7 = fresh("p7")
        argv7 = list(FULL_ARGS)
        argv7[argv7.index("A tiny puzzle")] = "uses {{SLUG}} and <!-- kind:app --> literally"
        _call(argv7 + t + ["--dest", str(p7)])
        case("values are inserted literally, never scanned again",
             "— uses {{SLUG}} and <!-- kind:app --> literally\n" in _read(p7 / "CLAUDE.md"), _read(p7 / "CLAUDE.md"))

        # 7. Bad input fails for its own reason, exit 1.
        rc, _, err = _call(FULL_ARGS[:-2] + t)
        case("missing --dest refused", rc == 1 and "--dest is required" in err, f"rc={rc} {err!r}")
        rc, _, err = _call(FULL_ARGS + t + ["--dest", str(K.skill_root()), "--dry-run"])
        case("--dest inside the skill folder refused", rc == 1 and "inside the flagship-method skill" in err, err)
        rc, _, err = _call(["--kind", "app", "--slug", "demo", "--dest", str(fresh("p9"))] + t)
        case("missing --name refused", rc == 1 and "--name is required" in err, f"rc={rc} {err!r}")
        rc, _, err = _call(["--kind", "app", "--name", "X", "--one-line", "two\nlines", "--dest", str(fresh("p10"))] + t)
        case("multi-line value refused", rc == 1 and "must be one line" in err, f"rc={rc} {err!r}")
        rc, _, err = _call(["--kind", "app", "--name", "X", "--dest", str(tmp / "nowhere")] + t)
        case("missing --dest folder refused", rc == 1 and "not an existing folder" in err, f"rc={rc} {err!r}")
        rc, _, err = _call(["--kind", "app", "--name", "X", "--templates", str(tmp / "none"), "--dest", str(fresh("p11"))])
        case("missing templates refused", rc == 1 and "templates folder not found" in err, f"rc={rc} {err!r}")
        old = templates("old", {"CLAUDE.md": "x\n", "project-skill/SKILL.md": "---\n"})
        rc, _, err = _call(["--kind", "app", "--name", "X", "--dest", str(fresh("p12"))] + old)
        case("a builder template named SKILL.md is refused", rc == 1 and "rename it to SKILL.md.template" in err, err)
        rc, _, err = _call(["--kind", "app", "--name", "X", "--date", "8/10/2026", "--dest", str(fresh("p13"))] + t)
        case("bad date refused", rc == 1 and "is not YYYY-MM-DD" in err, f"rc={rc} {err!r}")
        rc, _, err = _call(["--kind", "app", "--name", "X", "--force", "--dest", str(fresh("p14"))] + t)
        case("--force refused: there is none", rc == 2 and "there is no --force" in err, f"rc={rc} {err!r}")
        many = templates("many", {"CLAUDE.md": "{{CORE_RULE}}\n" * 45, **skill_tpl})
        rc, out, _ = _call(["--kind", "app", "--name", "X", "--dest", str(fresh("p_many"))] + many)
        case("many markers are summarised, the list stops at 40", rc == 0 and "(45): CORE_RULE x45" in out
             and "CLAUDE.md:40  [TODO: CORE_RULE]" in out and "CLAUDE.md:41  [TODO" not in out
             and "... and 5 more" in out, out[-300:])

        # 8. The environment variable selects templates; the CLI works under python3 -I.
        p15 = fresh("p15")
        saved = os.environ.get(K.ENV_TEMPLATES)
        os.environ[K.ENV_TEMPLATES] = t[1]
        try:
            rc, _, err = _call(FULL_ARGS + ["--dest", str(p15)])
        finally:
            if saved is None:
                os.environ.pop(K.ENV_TEMPLATES, None)
            else:
                os.environ[K.ENV_TEMPLATES] = saved
        case(f"${K.ENV_TEMPLATES} selects the templates", rc == 0 and (p15 / "CLAUDE.md").exists(), f"rc={rc} {err!r}")
        p16 = fresh("p16")
        proc = subprocess.run([sys.executable, "-I", str(Path(K.__file__).resolve())] + FULL_ARGS + t
                              + ["--dest", str(p16)], capture_output=True, text=True, encoding="utf-8")
        case("CLI run under python3 -I writes the kit", proc.returncode == 0
             and set(_files(p16)) == EXPECTED_FILES - {"docs/demo/MONETIZATION.md"}, proc.stderr[-300:])

        if not os.environ.get(K.ENV_CHILD):
            _lint_shipped(case)
            _mutation_proofs(case, tmp)

    print(f"init_kit selftest: {count} cases, {len(failures)} failure(s)")
    return 1 if failures else 0


def _lint_shipped(case) -> None:
    """The shipped templates render cleanly for every kind and flag combination."""
    tpl = K.default_templates()
    case("shipped templates folder exists", tpl.is_dir(), str(tpl))
    if not tpl.is_dir():
        return
    values: Dict[str, Optional[str]] = {
        "PROJECT_NAME": "Lint Probe", "SLUG": "lint-probe", "ONE_LINE": "A probe: it checks the kit.",
        "OWNER": "Sam", "OWNER_LANGUAGE": "English", "STACK": "Stack X (v1)", "PLATFORMS": "iPhone, Android",
        "DATE": "2026-01-01"}
    seen: Dict[Tuple[str, bool], Dict[str, str]] = {}
    for kind in K.KINDS:
        for on in (False, True):
            label = f"kind {kind}, optional docs {'on' if on else 'off'}"
            try:
                rendered, todo = K.render_kit(tpl, "lint-probe", kind, {"monetization": on, "release": on}, values)
            except K.KitError as e:
                case(f"shipped templates render ({label})", False, str(e))
                continue
            case(f"shipped templates render ({label})", True)
            texts = {rel: data.decode("utf-8", "replace") for rel, data in rendered}
            seen[(kind, on)] = texts
            unknown = sorted({name for _, _, name in todo})
            case(f"shipped templates use only the known placeholders ({label})", not unknown, str(unknown))
            legacy = sorted(rel for rel, x in texts.items() if re.search(r"TODO\([A-Z]", x))
            case(f"shipped templates use only the [TODO: …] marker ({label})", not legacy, str(legacy))
            probs = K.frontmatter_problems(texts.get(".claude/skills/lint-probe-builder/SKILL.md", ""), "lint-probe")
            case(f"shipped builder frontmatter is valid ({label})", not probs, str(probs))
            named = [d for d in ("MONETIZATION.md", "RELEASE.md") if d in texts.get("CLAUDE.md", "")]
            case(f"the router names optional docs only when written ({label})",
                 named == (["MONETIZATION.md", "RELEASE.md"] if on else []), str(named))
    if ("game", False) in seen and ("app", False) in seen:
        case("shipped kind:game and kind:app renders differ", seen[("game", False)] != seen[("app", False)])


def _mutation_proofs(case, tmp: Path) -> None:
    """Each core feature is removed in a copy of init_kit.py; the copy's selftest must catch it."""
    script = Path(K.__file__).resolve()
    source = script.read_text(encoding="utf-8")
    env = dict(os.environ, **{K.ENV_CHILD: "1"})

    def run_copy(name: str, text: str) -> Tuple[int, str]:
        folder = tmp / "mutants" / name / "scripts"
        folder.mkdir(parents=True)
        (folder / "init_kit.py").write_text(text, encoding="utf-8")
        shutil.copy(Path(__file__).resolve(), folder / "init_kit_selftest.py")
        try:
            proc = subprocess.run([sys.executable, "-I", str(folder / "init_kit.py"), "--selftest"],
                                  capture_output=True, text=True, encoding="utf-8", env=env, timeout=300)
        except subprocess.TimeoutExpired:
            return -1, "timed out after 300 s"
        return proc.returncode, proc.stdout + proc.stderr

    rc, out = run_copy("baseline", source)
    case("mutation control: an unchanged copy passes its selftest", rc == 0, out[-600:])
    for i, (feature, find, replace, label) in enumerate(MUTANTS):
        if source.count(find) != 1:
            case(f"mutant '{feature}' is caught", False, f"anchor found {source.count(find)} times: {find!r}")
            continue
        rc, out = run_copy(f"m{i}", source.replace(find, replace))
        case(f"mutant '{feature}' is caught by '{label}'", rc == 1 and f"FAIL  {label}" in out, out[-600:])
    shutil.rmtree(tmp / "mutants", ignore_errors=True)


if __name__ == "__main__":
    print("Run the selftest through the script: python3 init_kit.py --selftest", file=sys.stderr)
    sys.exit(2)
