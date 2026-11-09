"""Check old addresses against a new site: does each one reach the right page,
in one hop, ending in 200?

    # redirect map: CSV with old_url and new_url columns (status column optional)
    python check_urls.py redirect-map.csv --base http://localhost:8081 --out results

    # plain list of old addresses (e.g. the old sitemap): each must end in 200
    python check_urls.py urls.txt --base http://localhost:8080 --out results

--base swaps the scheme and host of every address for the test site, so a
map written for https://www.example.com can be checked on localhost or
staging. Failures are retried one at a time at the end, because a busy
local server times out under parallel load; only failures that fail again
are reported as failures.

Writes <out>.csv (one row per address) and <out>-summary.txt.
"""
import argparse
import csv
import re
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _http import get  # noqa: E402

CANON = re.compile(r"""<link[^>]+rel=["']canonical["'][^>]*>""", re.I)
HREF = re.compile(r"""href=["']([^"']+)""", re.I)


def rebase(url, base):
    if not base or not url:
        return url
    b, u = urlsplit(base), urlsplit(url)
    if not u.netloc:
        return urlunsplit((b.scheme, b.netloc, u.path or "/", u.query, ""))
    return urlunsplit((b.scheme, b.netloc, u.path, u.query, ""))


def norm(url):
    u = urlsplit(url)
    return urlunsplit((u.scheme.lower(), u.netloc.lower(), u.path, u.query, ""))


def check(row, base, timeout, want_canonical):
    start = rebase(row["old_url"], base)
    expected = rebase(row.get("new_url", ""), base)
    want_status = row.get("status", "").strip()
    hops, cur, first_status, first_loc = [], start, None, ""
    for _ in range(6):
        r = get(cur, timeout=timeout)
        if first_status is None:
            first_status, first_loc = r.status, r.location
        if r.status in (301, 302, 303, 307, 308) and r.location:
            hops.append(f"{r.status}")
            # Keep the test on the test site, but leave real off-site redirects alone.
            same_site = urlsplit(r.location).netloc in (urlsplit(start).netloc, urlsplit(row["old_url"]).netloc)
            cur = rebase(r.location, base) if base and same_site else r.location
            continue
        break
    final_status = r.status
    canonical = ""
    if want_canonical and final_status == 200:
        m = CANON.search(r.text)
        if m:
            h = HREF.search(m.group(0))
            canonical = rebase(h.group(1), base) if h else ""

    problems = []
    if final_status == 0:
        problems.append("network error: " + r.error[:60])
    elif final_status != 200:
        problems.append(f"ends in {final_status}")
    if len(hops) > 1:
        problems.append(f"{len(hops)} hops")
    if want_status in ("301", "302", "308", "307") and not hops:
        problems.append(f"expected {want_status}, got {first_status}")
    if want_status == "200" and hops:
        problems.append("expected 200, got a redirect")
    if want_status and want_status not in ("200",) and hops and hops[0] != want_status:
        problems.append(f"expected {want_status}, got {hops[0]}")
    if expected and norm(cur) != norm(expected):
        problems.append("wrong target")
    if want_canonical and final_status == 200 and canonical and norm(canonical) != norm(cur):
        problems.append("canonical points elsewhere")
    return {
        "old_url": row["old_url"], "tested_url": start, "first_status": first_status, "first_location": first_loc,
        "hops": len(hops), "final_url": cur, "final_status": final_status, "expected": expected,
        "canonical": canonical, "result": "pass" if not problems else "FAIL", "problems": "; ".join(problems),
        "type": row.get("old_type", ""),
    }


def load(path):
    p = Path(path)
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix.lower() == ".csv":
        rows = list(csv.DictReader(text.splitlines()))
        if rows and "old_url" not in rows[0]:
            first = list(rows[0].keys())[0]
            rows = [{"old_url": r[first], **r} for r in rows]
        return rows
    return [{"old_url": ln.strip()} for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="CSV (old_url,new_url[,status,old_type]) or a text file of URLs")
    ap.add_argument("--base", default="", help="test site, e.g. http://localhost:8081")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--timeout", type=float, default=60)
    ap.add_argument("--no-canonical", action="store_true", help="skip the canonical tag check")
    ap.add_argument("--only-failed", help="previous results CSV: recheck only its FAIL rows")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default="url-check")
    a = ap.parse_args()

    if a.base and urlsplit(a.base).hostname not in ("localhost", "127.0.0.1", "::1") and not urlsplit(a.base).hostname.endswith((".test", ".localhost")):
        print(f"Note: checking against {a.base}. Keep --workers low on a shared or production server.")

    rows = load(a.input)
    if a.only_failed:
        failed = {r["old_url"] for r in csv.DictReader(open(a.only_failed, encoding="utf-8")) if r.get("result") == "FAIL"}
        rows = [r for r in rows if r["old_url"] in failed]
    if a.limit:
        rows = rows[: a.limit]
    print(f"Checking {len(rows)} addresses with {a.workers} workers")

    t0 = time.monotonic()
    results = [None] * len(rows)
    with ThreadPoolExecutor(a.workers) as ex:
        futs = {ex.submit(check, r, a.base, a.timeout, not a.no_canonical): i for i, r in enumerate(rows)}
        for n, f in enumerate(as_completed(futs), 1):
            results[futs[f]] = f.result()
            if n % 500 == 0 or n == len(rows):
                bad = sum(1 for x in results if x and x["result"] == "FAIL")
                print(f"  {n}/{len(rows)} done, {bad} failing so far, {time.monotonic() - t0:.0f}s", flush=True)

    retry = [i for i, x in enumerate(results) if x["result"] == "FAIL"]
    if retry:
        print(f"Retrying {len(retry)} failures one at a time")
        for i in retry:
            again = check(rows[i], a.base, a.timeout, not a.no_canonical)
            if again["result"] == "pass":
                again["problems"] = "passed on retry (first try: " + results[i]["problems"] + ")"
            results[i] = again

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(f"{out}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()) if results else ["old_url"])
        w.writeheader()
        w.writerows(results)

    fails = [r for r in results if r["result"] == "FAIL"]
    by_type = Counter((r["type"] or "-", r["result"]) for r in results)
    chains = sum(1 for r in results if r["hops"] > 1)
    lines = [
        f"Address check against {a.base or '(addresses as written)'}  {time.strftime('%Y-%m-%d %H:%M')}",
        f"Tested: {len(results)}   Passed: {len(results) - len(fails)}   Failed: {len(fails)}",
        f"Redirect chains (more than one hop): {chains}",
        f"Passed only on retry: {sum(1 for r in results if r['problems'].startswith('passed on retry'))}",
        "By type:",
        *[f"  {t:12} {by_type[(t, 'pass')]:7} passed  {by_type[(t, 'FAIL')]:5} failed" for t in sorted({t for t, _ in by_type})],
        "Problems:",
        *[f"  {n:6}  {p}" for p, n in Counter(p for r in fails for p in r["problems"].split("; ")).most_common()],
        "First failures:",
        *[f"  {r['old_url']} -> {r['final_url']} ({r['problems']})" for r in fails[:30]],
    ]
    Path(f"{out}-summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:4 + len({t for t, _ in by_type}) + 1]))
    print(f"-> {out}.csv, {out}-summary.txt")


if __name__ == "__main__":
    main()
