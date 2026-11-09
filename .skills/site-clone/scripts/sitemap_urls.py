"""List every address in a site's sitemap(s).

    python sitemap_urls.py https://example.com --out urls.txt
    python sitemap_urls.py https://example.com/sitemap_index.xml --out urls.txt

Finds sitemaps from robots.txt (or /sitemap.xml), follows sitemap indexes,
handles .gz files, and writes one URL per line. Read-only and slow on
purpose (--delay seconds between requests, default 1).
"""
import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _http import Polite  # noqa: E402

LOC = re.compile(r"<loc>\s*(?:<!\[CDATA\[)?\s*([^<\s\]]+)", re.I)


def find_sitemaps(polite, base):
    parts = urlsplit(base)
    root = f"{parts.scheme}://{parts.netloc}"
    if parts.path.lower().endswith((".xml", ".xml.gz")):
        return [base]
    r = polite.get(root + "/robots.txt")
    found = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", r.text) if r.status == 200 else []
    if found:
        return found
    # No Sitemap line in robots.txt: try the usual locations, first one that answers wins.
    for path in ("/sitemap.xml", "/sitemap_index.xml", "/wp-sitemap.xml", "/sitemap.xml.gz"):
        if fetch(polite, root + path).status == 200:
            return [root + path]
    return [root + "/sitemap.xml"]


def fetch(polite, url, hops=3):
    """GET that follows a few redirects (sitemaps often move, e.g. WordPress /sitemap.xml)."""
    r = polite.get(url)
    while r.status in (301, 302, 303, 307, 308) and r.location and hops:
        r = polite.get(r.location)
        hops -= 1
    return r


def expand(polite, start, max_sitemaps):
    seen, urls, queue = set(), [], list(start)
    while queue and len(seen) < max_sitemaps:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        r = fetch(polite, sm)
        if r.status != 200:
            print(f"  skip {sm}: HTTP {r.status} {r.error}", file=sys.stderr)
            continue
        body = r.text
        locs = LOC.findall(body)
        if "<sitemapindex" in body[:2000].lower():
            queue.extend(locs)
            print(f"  index {sm}: {len(locs)} sitemaps", file=sys.stderr)
        else:
            urls.extend(locs)
            print(f"  {sm}: {len(locs)} urls", file=sys.stderr)
    return urls, sorted(seen)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site", help="site root or a sitemap URL")
    ap.add_argument("--out", default="urls.txt")
    ap.add_argument("--delay", type=float, default=1.0)
    ap.add_argument("--max-sitemaps", type=int, default=500)
    a = ap.parse_args()

    # Sitemaps are meant for crawlers, so robots.txt rules don't apply to them.
    polite = Polite(a.site, delay=a.delay, respect_robots=False)
    urls, maps = expand(polite, find_sitemaps(polite, a.site), a.max_sitemaps)
    unique = list(dict.fromkeys(u.strip() for u in urls))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text("\n".join(unique) + "\n", encoding="utf-8")
    print(f"{len(unique)} unique URLs from {len(maps)} sitemap(s) -> {a.out}")


if __name__ == "__main__":
    main()
