#!/usr/bin/env python3
"""code_reviews.py: code store reviews into themes, per app (the research review matrix).
Standard library only (Python 3.8+). It reads reviews you already pulled; it fetches nothing.

    python3 code_reviews.py REVIEWS... --themes themes.json [--csv counts.csv] [--summary-csv apps.csv]
        [--store store.json] [--recent 500] [--uncoded uncoded_low.txt]
    python3 code_reviews.py --selftest

REVIEWS are JSON files (a list of objects, or {"reviews": [...]}) or CSV files with a header row.
Fields: app, rating (1-5), date (YYYY-MM-DD, a time after it is fine), body (also read from text,
content or review), title (optional). Optional: id (the de-duplication key), version, country. Rows
repeated across pages or files are dropped: by (app, id) when id is given, else by (app, rating, date,
title, body); the number dropped is reported. A bad row is an error naming file and row; nothing is
guessed.

THEMES is JSON. Every regex is case-insensitive and searched in title + " " + body:
    {"complaints": {"crashes": "crash|freez|lost (my )?progress",
                    "wants to pay": {"also": "\\\\bads?\\\\b", "any": "pay|purchase|buy"},
                    "ads too often": {"also": ["\\\\bads?\\\\b", "advert"], "any": ["every level", "too many"]}},
     "loves":      {"relaxing": ["relax", "calm", "bed ?time"]},
     "negative_cue": ["\\\\bbut\\\\b", "wish", "n't\\\\b", "annoy", "except"]}
A theme is one regex, or a list of regexes (any one hits). The optional "must also mention X" prefix is
the object form {"also": X, "any": theme}: the review counts only if it also matches an "also" regex
(X is one regex or a list), e.g. "wants to pay" only in reviews that also mention ads. A flat map
{"theme": regex} with no complaints/loves key is used for both complaints and loves. negative_cue
(optional) applies to complaints inside 4-5 stars only: a 5-star review that names a theme is usually
praise, so it counts there only with a cue.

It prints a per-app summary and three theme x app tables (markdown): complaints in 1-3 star reviews,
loves in 4-5 star reviews, complaints inside 4-5 star reviews. Column headers carry each base (n).
--csv writes view,theme,app,count,base (app ALL = every app). --store adds each app's store average
(JSON {"app": 4.7} or {"app": {"average": 4.7, "ratings": 120000}}, or CSV app,average[,ratings]) next
to the mean of its most recent --recent written reviews; averages hide anger, and the gap is the
opening. --uncoded writes the 1-3 star reviews that no complaint theme caught: read them (read every
1-3 star review by hand anyway) and grow the themes from what they say.

Counts are approximate: one review can hit several themes and regexes miss paraphrases. Paraphrase
reviews in docs; never quote them in product or store text. Keep raw review text out of the repository
unless its licence and privacy allow; this script, the themes file and the derived counts always stay.
Exit codes: 0 done; 1 bad input (unreadable file, bad row, bad theme or regex).
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Tuple

BODY_KEYS = ("body", "text", "content", "review")
VIEWS = (
    ("complaints_1_3", "Complaints in 1-3 star reviews"),
    ("loves_4_5", "Loves in 4-5 star reviews"),
    ("complaints_in_4_5", "Complaints inside 4-5 star reviews"),
)
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}")


class InputError(Exception):
    """Bad input: exit 1 with this message."""


Review = Dict[str, object]
Matcher = Callable[[str], bool]


def _rows(path: Path) -> List[Dict[str, object]]:
    try:
        raw = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as e:
        raise InputError(f"cannot read {path}: {e}")
    if path.suffix.lower() == ".csv":
        return [dict(r) for r in csv.DictReader(io.StringIO(raw))]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise InputError(f"{path} is not JSON: {e}")
    if isinstance(data, dict):
        data = data.get("reviews")
    if not isinstance(data, list) or not all(isinstance(r, dict) for r in data):
        raise InputError(f"{path}: expected a list of review objects, or {{\"reviews\": [...]}}")
    return data


def load_reviews(paths: Sequence[Path]) -> Tuple[List[Review], int]:
    """Every valid review, de-duplicated, and the number of duplicates dropped."""
    reviews: List[Review] = []
    problems: List[str] = []
    for path in paths:
        for n, row in enumerate(_rows(path), 1):
            r = {str(k).strip().lower(): v for k, v in row.items() if k is not None}
            where = f"{path.name} row {n}"
            app = str(r.get("app") or "").strip()
            body = next((str(r[k]) for k in BODY_KEYS if r.get(k) not in (None, "")), "")
            date = str(r.get("date") or "").strip()
            try:
                rating = float(str(r.get("rating", "")).strip())
            except ValueError:
                rating = 0.0
            if not app:
                problems.append(f"{where}: no app")
            elif rating not in (1.0, 2.0, 3.0, 4.0, 5.0):
                problems.append(f"{where}: rating {r.get('rating')!r} is not 1-5")
            elif not DATE.match(date):
                problems.append(f"{where}: date {date!r} is not YYYY-MM-DD")
            else:
                reviews.append({"app": app, "rating": int(rating), "date": date[:10], "body": body,
                                "title": str(r.get("title") or ""), "id": str(r.get("id") or "")})
    if problems:
        more = f"\n  ... and {len(problems) - 20} more" if len(problems) > 20 else ""
        raise InputError("bad review rows:\n  " + "\n  ".join(problems[:20]) + more)
    seen = set()
    unique: List[Review] = []
    for rv in reviews:
        key = (rv["app"], rv["id"]) if rv["id"] else (rv["app"], rv["rating"], rv["date"], rv["title"], rv["body"])
        if key not in seen:
            seen.add(key)
            unique.append(rv)
    return unique, len(reviews) - len(unique)


def _compile(where: str, patterns: object) -> List["re.Pattern[str]"]:
    if isinstance(patterns, str):
        patterns = [patterns]
    if not isinstance(patterns, list) or not patterns or not all(isinstance(p, str) for p in patterns):
        raise InputError(f"theme {where}: expected one regex string or a non-empty list of them")
    out = []
    for p in patterns:
        try:
            out.append(re.compile(p, re.IGNORECASE))
        except re.error as e:
            raise InputError(f"theme {where}: bad regex {p!r}: {e}")
    return out


def _theme(name: str, spec: object) -> Matcher:
    if isinstance(spec, dict):
        unknown = set(spec) - {"any", "also"}
        if unknown or "any" not in spec:
            raise InputError(f"theme {name!r}: an object theme takes 'any' (required) and 'also' "
                             "(the 'must also mention' regexes) only")
        any_rx = _compile(f"{name!r} any", spec["any"])
        also_rx = _compile(f"{name!r} also", spec["also"]) if "also" in spec else []
    else:
        any_rx, also_rx = _compile(repr(name), spec), []
    return lambda text: any(rx.search(text) for rx in any_rx) and (
        not also_rx or any(rx.search(text) for rx in also_rx))


def load_themes(path: Path) -> Tuple[Dict[str, Matcher], Dict[str, Matcher], Optional[Matcher]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        raise InputError(f"cannot read the themes file {path}: {e}")
    if not isinstance(data, dict) or not data:
        raise InputError(f"{path}: expected a JSON object of themes")
    if "complaints" in data or "loves" in data:
        extra = set(data) - {"complaints", "loves", "negative_cue"}
        if extra:
            raise InputError(f"{path}: unknown top-level keys {sorted(extra)} "
                             "(expected complaints, loves, negative_cue)")
        groups = [data.get("complaints") or {}, data.get("loves") or {}]
    else:
        groups = [data, data]
    for g in groups:
        if not isinstance(g, dict):
            raise InputError(f"{path}: complaints and loves must be objects of theme -> regexes")
    complaints = {name: _theme(name, spec) for name, spec in groups[0].items()}
    loves = {name: _theme(name, spec) for name, spec in groups[1].items()}
    cue_rx = _compile("negative_cue", data["negative_cue"]) if "negative_cue" in data else None
    cue = (lambda text: any(rx.search(text) for rx in cue_rx)) if cue_rx else None
    return complaints, loves, cue


def load_store(path: Path) -> Dict[str, Tuple[float, Optional[int]]]:
    rows: List[Tuple[str, object, object]] = []
    if path.suffix.lower() == ".csv":
        for r in _rows(path):
            r = {str(k).strip().lower(): v for k, v in r.items() if k is not None}
            rows.append((str(r.get("app") or "").strip(), r.get("average"), r.get("ratings")))
    else:
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
            raise InputError(f"cannot read the store file {path}: {e}")
        if not isinstance(data, dict):
            raise InputError(f"{path}: expected {{\"app\": average}} or {{\"app\": {{\"average\": x, \"ratings\": n}}}}")
        for app, v in data.items():
            rows.append((app, v.get("average"), v.get("ratings")) if isinstance(v, dict) else (app, v, None))
    out: Dict[str, Tuple[float, Optional[int]]] = {}
    for app, avg, count in rows:
        try:
            out[app] = (float(str(avg)), int(float(str(count))) if count not in (None, "") else None)
        except ValueError:
            raise InputError(f"{path}: app {app!r} has average {avg!r} / ratings {count!r}; expected numbers")
    return out


def code(reviews: Sequence[Review], complaints: Dict[str, Matcher], loves: Dict[str, Matcher],
         cue: Optional[Matcher]) -> Tuple[Dict[str, Dict[str, Dict[str, int]]], Dict[str, Dict[str, int]]]:
    """counts[view][theme][app] and base[view][app]; app "ALL" sums every app."""
    picks = {"complaints_1_3": (complaints, lambda r, t: r["rating"] <= 3),
             "loves_4_5": (loves, lambda r, t: r["rating"] >= 4),
             "complaints_in_4_5": (complaints, lambda r, t: r["rating"] >= 4 and (cue is None or cue(t)))}
    counts: Dict[str, Dict[str, Dict[str, int]]] = {}
    base: Dict[str, Dict[str, int]] = {}
    for view, (themes, pick) in picks.items():
        counts[view] = {name: {} for name in themes}
        base[view] = {}
        for rv in reviews:
            text = f"{rv['title']} {rv['body']}"
            in_view = rv["rating"] <= 3 if view == "complaints_1_3" else rv["rating"] >= 4
            if in_view:
                for app in (rv["app"], "ALL"):
                    base[view][app] = base[view].get(app, 0) + 1
            if not pick(rv, text):
                continue
            for name, hit in themes.items():
                if hit(text):
                    for app in (rv["app"], "ALL"):
                        counts[view][name][app] = counts[view][name].get(app, 0) + 1
    return counts, base


def uncoded(reviews: Sequence[Review], complaints: Dict[str, Matcher]) -> List[Review]:
    return [rv for rv in reviews if rv["rating"] <= 3
            and not any(hit(f"{rv['title']} {rv['body']}") for hit in complaints.values())]


def summary(reviews: Sequence[Review], apps: Sequence[str], recent: int, store: Dict[str, Tuple[float, Optional[int]]],
            missed: Sequence[Review]) -> List[Dict[str, object]]:
    rows = []
    for app in apps:
        mine = [rv for rv in reviews if rv["app"] == app]
        latest = sorted(mine, key=lambda rv: rv["date"], reverse=True)[:recent]
        mean = round(sum(rv["rating"] for rv in latest) / len(latest), 2)
        avg, ratings = store.get(app, (None, None))
        rows.append({
            "app": app, "reviews": len(mine), "low_1_3": sum(1 for rv in mine if rv["rating"] <= 3),
            "high_4_5": sum(1 for rv in mine if rv["rating"] >= 4),
            "first": min(rv["date"] for rv in mine), "last": max(rv["date"] for rv in mine),
            "recent_n": len(latest), "recent_mean": mean, "store_average": avg, "store_ratings": ratings,
            "gap": None if avg is None else round(avg - mean, 2),
            "uncoded_1_3": sum(1 for rv in missed if rv["app"] == app)})
    return rows


def _fmt(v: object) -> str:
    return "-" if v is None else str(v)


def _cell(v: object) -> str:
    """A markdown table cell: a '|' in an app or theme name would split the column."""
    return str(v).replace("|", "\\|")


def report(counts, base, rows, apps: Sequence[str], dropped: int, out) -> None:
    total = sum(r["reviews"] for r in rows)
    print(f"{total} reviews from {len(apps)} apps after dropping {dropped} duplicates. Counts are "
          "approximate (one review can hit several themes).\n", file=out)
    print("| App | Reviews | 1-3 star | 4-5 star | Dates | Mean of recent | Store average | Gap | "
          "Uncoded 1-3 star |\n|---|---:|---:|---:|---|---:|---:|---:|---:|", file=out)
    for r in rows:
        store = "-" if r["store_average"] is None else (
            f"{r['store_average']}" + (f" ({r['store_ratings']} ratings)" if r["store_ratings"] else ""))
        print(f"| {_cell(r['app'])} | {r['reviews']} | {r['low_1_3']} | {r['high_4_5']} | {r['first']}..{r['last']} | "
              f"{r['recent_mean']} (n={r['recent_n']}) | {store} | {_fmt(r['gap'])} | {r['uncoded_1_3']} |",
              file=out)
    cols = list(apps) + ["ALL"]
    for view, heading in VIEWS:
        print(f"\n### {heading}\n", file=out)
        print("| Theme | " + " | ".join(f"{_cell(a)} (n={base[view].get(a, 0)})" for a in cols) + " |", file=out)
        print("|---|" + "---:|" * len(cols), file=out)
        ranked = sorted(counts[view].items(), key=lambda kv: (-kv[1].get("ALL", 0), kv[0]))
        for name, per in ranked:
            print(f"| {_cell(name)} | " + " | ".join(str(per.get(a, 0)) for a in cols) + " |", file=out)


def main(argv: Optional[Sequence[str]] = None, out=sys.stdout, err=sys.stderr) -> int:
    p = argparse.ArgumentParser(prog="code_reviews.py", formatter_class=argparse.RawDescriptionHelpFormatter,
                                description=(__doc__ or "").split("\n\n")[0],
                                epilog=(__doc__ or "").split("\n\n", 1)[-1])
    p.add_argument("reviews", nargs="*", help="review files: .json or .csv")
    p.add_argument("--themes", help="themes JSON: complaints / loves / negative_cue, or a flat theme map "
                                    "(format below)")
    p.add_argument("--csv", help="write view,theme,app,count,base rows here")
    p.add_argument("--summary-csv", dest="summary_csv", help="write the per-app summary here")
    p.add_argument("--store", help="store averages: JSON or CSV (app, average[, ratings])")
    p.add_argument("--recent", type=int, default=500, help="reviews per app in the recent mean (default 500)")
    p.add_argument("--uncoded", help="write the 1-3 star reviews no complaint theme caught (local reading only)")
    p.add_argument("--selftest", action="store_true", help="prove this script works, in a temp folder")
    args = p.parse_args(argv)
    if args.selftest:
        return selftest()
    try:
        if not args.reviews or not args.themes:
            raise InputError("give at least one review file and --themes")
        if args.recent < 1:
            raise InputError("--recent must be at least 1")
        reviews, dropped = load_reviews([Path(x) for x in args.reviews])
        if not reviews:
            raise InputError("no reviews in the input")
        complaints, loves, cue = load_themes(Path(args.themes))
        store = load_store(Path(args.store)) if args.store else {}
    except InputError as e:
        print(f"code_reviews: {e}", file=err)
        return 1
    apps = sorted({str(rv["app"]) for rv in reviews})
    unknown = sorted(set(store) - set(apps))
    if unknown:
        print(f"code_reviews: note: store averages for apps with no reviews: {unknown}", file=err)
    counts, base = code(reviews, complaints, loves, cue)
    missed = uncoded(reviews, complaints)
    rows = summary(reviews, apps, args.recent, store, missed)
    report(counts, base, rows, apps, dropped, out)
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["view", "theme", "app", "count", "base"])
            for view, _ in VIEWS:
                for name, per in counts[view].items():
                    for app in list(apps) + ["ALL"]:
                        w.writerow([view, name, app, per.get(app, 0), base[view].get(app, 0)])
    if args.summary_csv:
        with open(args.summary_csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    if args.uncoded:
        with open(args.uncoded, "w", encoding="utf-8") as fh:
            for rv in sorted(missed, key=lambda rv: (rv["app"], rv["date"])):
                fh.write(f"--- {rv['app']} | {rv['rating']} star | {rv['date']}\n{rv['title']}\n{rv['body']}\n\n")
    return 0


# --------------------------------------------------------------------------------------------
# Selftest: a tiny review set in a temp folder; every expected count is a literal written here.

REVIEWS = [
    {"app": "Alpha", "id": "a1", "rating": 1, "date": "2026-09-01", "title": "Too many ads", "body": "ads every level"},
    {"app": "Alpha", "id": "a2", "rating": 2, "date": "2026-09-02", "title": "", "body": "crashes too many times"},
    {"app": "Alpha", "id": "a3", "rating": 5, "date": "2026-09-03", "title": "Love it", "body": "so relaxing at bedtime"},
    {"app": "Alpha", "id": "a4", "rating": 5, "date": "2026-09-04", "title": "Great",
     "body": "relaxing, but too many ads lately"},
    {"app": "Alpha", "id": "a5", "rating": 4, "date": "2026-09-05T10:00:00Z", "title": "Fine", "body": "the ads are fine"},
    {"app": "Alpha", "id": "a6", "rating": 1, "date": "2026-08-01", "title": "meh", "body": "I just do not like it"},
    {"app": "Alpha", "id": "a1", "rating": 1, "date": "2026-09-01", "title": "Too many ads", "body": "ads every level"},
    {"app": "Beta", "rating": 3, "date": "2026-09-10", "title": "Ads", "body": "advert after advert"},
    {"app": "Beta", "rating": 3, "date": "2026-09-10", "title": "Ads", "body": "advert after advert"},
    {"app": "Beta", "rating": 5, "date": "2026-09-11", "title": "calm", "body": "calm puzzles"},
]
THEMES = {  # "crashes" is one regex; "ads too often" has a "must also mention" prefix given as one regex
    "complaints": {"ads": ["\\bads?\\b", "advert"], "crashes": "crash|freez",
                   "ads too often": {"also": "\\bads?\\b|advert", "any": ["too many", "every level", "after"]}},
    "loves": {"relaxing": ["relax", "calm"]},
    "negative_cue": ["\\bbut\\b", "n't\\b"],
}


def selftest() -> int:
    failures: List[str] = []
    count = 0

    def case(label: str, ok: bool, detail: str = "") -> None:
        nonlocal count
        count += 1
        if ok:
            print(f"  ok  {label}")
        else:
            failures.append(label)
            print(f"FAIL  {label}: {detail[:500]}")

    def call(argv: Sequence[str]) -> Tuple[int, str, str]:
        o, e = io.StringIO(), io.StringIO()
        try:
            rc = main(list(argv), out=o, err=e)
        except Exception as ex:  # noqa: BLE001 - report, never die
            return -1, o.getvalue(), f"CRASH {type(ex).__name__}: {ex}"
        return rc, o.getvalue(), e.getvalue()

    def rows_of(path: Path) -> List[List[str]]:
        return list(csv.reader(path.open(encoding="utf-8"))) if path.is_file() else []

    with tempfile.TemporaryDirectory(prefix="code_reviews_selftest_") as tmp_name:
        tmp = Path(tmp_name)
        rj, th, st = tmp / "reviews.json", tmp / "themes.json", tmp / "store.json"
        rj.write_text(json.dumps(REVIEWS), encoding="utf-8")
        th.write_text(json.dumps(THEMES), encoding="utf-8")
        st.write_text(json.dumps({"Alpha": 4.6, "Beta": {"average": 4.8, "ratings": 1200}}), encoding="utf-8")
        counts_csv, apps_csv, low = tmp / "counts.csv", tmp / "apps.csv", tmp / "low.txt"
        rc, out, err = call([str(rj), "--themes", str(th), "--store", str(st), "--csv", str(counts_csv),
                             "--summary-csv", str(apps_csv), "--uncoded", str(low)])
        case("a full run exits 0", rc == 0, f"rc={rc} {err!r}")
        case("duplicates dropped by id, and by content without id", "8 reviews from 2 apps after dropping 2" in out, out)
        rows = rows_of(counts_csv)
        want = [
            ["complaints_1_3", "ads", "Alpha", "1", "3"], ["complaints_1_3", "ads", "Beta", "1", "1"],
            ["complaints_1_3", "crashes", "Alpha", "1", "3"], ["complaints_1_3", "ads too often", "ALL", "2", "4"],
            ["loves_4_5", "relaxing", "Alpha", "2", "3"], ["loves_4_5", "relaxing", "Beta", "1", "1"],
            ["complaints_in_4_5", "ads", "Alpha", "1", "3"], ["complaints_in_4_5", "ads too often", "Alpha", "1", "3"],
        ]
        case("the CSV holds the expected counts and bases", all(w in rows for w in want),
             str([w for w in want if w not in rows]))
        case("a 4-5 star review without a negative cue is not a complaint there",
             ["complaints_in_4_5", "ads", "ALL", "1", "4"] in rows, str([r for r in rows if r[0] == "complaints_in_4_5"]))
        case("'also' needs both patterns (a crash 'too many times' is not about ads)",
             ["complaints_1_3", "ads too often", "Alpha", "1", "3"] in rows, str([r for r in rows if "often" in r[1]]))
        case("a theme given as one regex counts like a list",
             ["complaints_1_3", "crashes", "ALL", "1", "4"] in rows, str([r for r in rows if r[1] == "crashes"]))
        case("the tables carry their bases", "| Theme | Alpha (n=3) | Beta (n=1) | ALL (n=4) |" in out, out)
        summ = {r[0]: r for r in rows_of(apps_csv)[1:]}
        hdr = rows_of(apps_csv)[0] if apps_csv.is_file() else []
        col = {name: i for i, name in enumerate(hdr)}
        a = summ.get("Alpha", [])
        ok = bool(a) and a[col["recent_mean"]] == "3.0" and a[col["gap"]] == "1.6" and a[col["uncoded_1_3"]] == "1"
        case("store average vs recent mean, and the gap", ok, str(a))
        case("the store rating count is shown", "4.8 (1200 ratings)" in out, out)
        case("uncoded 1-3 star reviews are written to read", "I just do not like it" in low.read_text(encoding="utf-8")
             if low.is_file() else False)
        rc, out, _ = call([str(rj), "--themes", str(th), "--recent", "2"])
        case("--recent N averages only the newest N", "| Alpha | 6 | 3 | 3 | 2026-08-01..2026-09-05 | 4.5 (n=2) |" in out, out)

        # CSV input with the 'text' alias reads the same; a flat theme map counts both ways.
        rc_path = tmp / "reviews.csv"
        with rc_path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["app", "rating", "title", "text", "date", "id"])
            for r in REVIEWS:
                w.writerow([r["app"], r["rating"], r["title"], r["body"], r["date"], r.get("id", "")])
        flat = tmp / "flat.json"
        flat.write_text(json.dumps({"relaxing": ["relax", "calm"]}), encoding="utf-8")
        flat_csv = tmp / "flat.csv"
        rc, out, err = call([str(rc_path), "--themes", str(flat), "--csv", str(flat_csv)])
        frows = rows_of(flat_csv)
        case("CSV input and a flat theme map", rc == 0 and ["loves_4_5", "relaxing", "ALL", "3", "4"] in frows
             and ["complaints_1_3", "relaxing", "ALL", "0", "4"] in frows, f"rc={rc} {err!r} {frows[:4]}")

        # Bad input fails for its own reason, exit 1.
        bad_rx = tmp / "bad_rx.json"
        bad_rx.write_text(json.dumps({"complaints": {"broken": ["(unclosed"]}}), encoding="utf-8")
        rc, _, err = call([str(rj), "--themes", str(bad_rx)])
        case("a bad regex names its theme", rc == 1 and "'broken'" in err and "bad regex" in err, err)
        bad_rows = tmp / "bad_rows.json"
        bad_rows.write_text(json.dumps([{"app": "A", "rating": "five", "date": "2026-01-01", "body": "x"},
                                        {"rating": 3, "date": "2026-01-01", "body": "x"},
                                        {"app": "A", "rating": 3, "date": "01/02/2026", "body": "x"}]), encoding="utf-8")
        rc, _, err = call([str(bad_rows), "--themes", str(th)])
        case("bad rows are named, nothing guessed", rc == 1 and "row 1: rating 'five'" in err and "row 2: no app" in err
             and "row 3: date" in err, err)
        bad_top = tmp / "bad_top.json"
        bad_top.write_text(json.dumps({"complaints": {}, "lovez": {}}), encoding="utf-8")
        rc, _, err = call([str(rj), "--themes", str(bad_top)])
        case("a misspelt top-level key is refused", rc == 1 and "lovez" in err, err)
        rc, _, err = call([str(tmp / "missing.json"), "--themes", str(th)])
        case("a missing review file is refused", rc == 1 and "cannot read" in err, err)

        # The command line itself works in an isolated interpreter.
        proc = subprocess.run([sys.executable, "-I", str(Path(__file__).resolve()), str(rj), "--themes", str(th)],
                              capture_output=True, text=True, encoding="utf-8")
        case("CLI run under python3 -I", proc.returncode == 0 and "### Loves in 4-5 star reviews" in proc.stdout,
             proc.stderr[-300:])
        proc = subprocess.run([sys.executable, "-I", str(Path(__file__).resolve()), "--help"],
                              capture_output=True, text=True, encoding="utf-8")
        case("--help gives the input format", proc.returncode == 0 and "Fields: app, rating" in proc.stdout
             and 'must also mention X" prefix' in proc.stdout and "negative_cue" in proc.stdout, proc.stdout[-300:])

    print(f"code_reviews selftest: {count} cases, {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
