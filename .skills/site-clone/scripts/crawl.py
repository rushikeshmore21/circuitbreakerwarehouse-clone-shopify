"""Polite, read-only page scan. Records what each page is made of so the
rebuild can match it: titles, meta, canonical, headings, structured data,
forms (field names only; nothing is submitted), images without alt text,
links and third-party script hosts.

    # sample 5 pages of every address pattern from a URL list
    python crawl.py https://example.com --urls urls.txt --sample-per-pattern 5 --out scan/crawl

    # no URL list: follow links from the home page, up to 200 pages
    python crawl.py https://example.com --max-pages 200 --out scan/crawl

    # only show how the URL list groups into patterns (no requests)
    python crawl.py https://example.com --urls urls.txt --patterns-only

Writes <out>.jsonl (one record per page), <out>.csv (summary) and
<out>-patterns.txt. Defaults: 1 request per second, robots.txt respected,
same host only, GET only.
"""
import argparse
import csv
import json
import random
import re
import sys
import time
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _http import UA, Polite  # noqa: E402
import _patterns  # noqa: E402

SKIP_EXT = re.compile(r"\.(jpe?g|png|gif|webp|avif|svg|ico|pdf|zip|gz|mp4|webm|mp3|css|js|woff2?|ttf|eot|xml|txt)(\?|$)", re.I)
# Never fetch addresses that change state, even with GET (logout, add to cart, delete...).
UNSAFE = re.compile(r"(logout|log-out|signout|sign-out|add-to-cart|addtocart|add_to_cart|remove|delete|empty|unsubscribe|wp-admin|/admin)", re.I)


class PageParser(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.title, self.in_title = "", False
        self.meta, self.links, self.canonical, self.lang = {}, [], "", ""
        self.headings, self._h = [], None
        self.imgs, self.imgs_no_alt = 0, 0
        self.scripts, self.forms, self._form = [], [], None
        self.jsonld, self._ld, self.itemtypes = [], None, set()
        self.text_len = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link" and "canonical" in (a.get("rel") or "").lower():
            self.canonical = urljoin(self.base, a.get("href", ""))
        elif tag == "a" and a.get("href"):
            self.links.append(urljoin(self.base, a["href"]))
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._h = [tag, ""]
        elif tag == "img":
            self.imgs += 1
            if "alt" not in a:
                self.imgs_no_alt += 1
        elif tag == "script":
            if a.get("src"):
                self.scripts.append(urljoin(self.base, a["src"]))
            if (a.get("type") or "").lower() == "application/ld+json":
                self._ld = ""
        elif tag == "form":
            self._form = {"action": urljoin(self.base, a.get("action", "")), "method": (a.get("method") or "get").lower(),
                          "id": a.get("id", ""), "fields": []}
        elif tag in ("input", "select", "textarea") and self._form is not None:
            if (a.get("type") or "").lower() not in ("hidden", "submit", "button"):
                self._form["fields"].append(f"{a.get('name', '?')}:{a.get('type', tag)}")
        if a.get("itemtype"):
            self.itemtypes.add(a["itemtype"].rsplit("/", 1)[-1])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif self._h and tag == self._h[0]:
            self.headings.append((self._h[0], " ".join(self._h[1].split())[:120]))
            self._h = None
        elif tag == "script" and self._ld is not None:
            self.jsonld.append(self._ld)
            self._ld = None
        elif tag == "form" and self._form is not None:
            self.forms.append(self._form)
            self._form = None

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self._h:
            self._h[1] += data
        if self._ld is not None:
            self._ld += data
        else:
            self.text_len += len(data.strip())


def ld_types(blocks):
    types = set()

    def walk(o):
        if isinstance(o, dict):
            t = o.get("@type")
            if isinstance(t, str):
                types.add(t)
            elif isinstance(t, list):
                types.update(x for x in t if isinstance(x, str))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    for b in blocks:
        try:
            walk(json.loads(b))
        except ValueError:
            types.add("(invalid JSON-LD)")
    return sorted(types)


def scan(polite, url, host):
    t0 = time.monotonic()
    r, hops = polite.get(url), []
    while r.status in (301, 302, 303, 307, 308) and len(hops) < 5:
        hops.append(f"{r.status}>{r.location}")
        if urlsplit(r.location).netloc != host:
            break
        r = polite.get(r.location)
    rec = {"url": url, "status": r.status, "final_url": r.url, "redirects": hops, "error": r.error,
           "ms": int((time.monotonic() - t0) * 1000), "bytes": len(r.body),
           "content_type": r.headers.get("content-type", "")}
    looks_html = r.body[:300].lstrip().lower().startswith((b"<!doctype html", b"<html"))
    if r.status != 200 or not ("html" in rec["content_type"] or looks_html):
        return rec, []
    p = PageParser(r.url)
    try:
        p.feed(r.text)
    except Exception as e:  # noqa: BLE001
        rec["parse_error"] = str(e)[:100]
    script_hosts = sorted({urlsplit(s).netloc for s in p.scripts if urlsplit(s).netloc and urlsplit(s).netloc != host})
    internal = [urldefrag(u)[0] for u in p.links if urlsplit(u).netloc == host]
    rec.update({
        "title": " ".join(p.title.split()),
        "meta_description": p.meta.get("description", ""),
        "meta_robots": p.meta.get("robots", ""),
        "canonical": p.canonical,
        "og_url": p.meta.get("og:url", ""),
        "lang": p.lang,
        "h1": [t for h, t in p.headings if h == "h1"],
        "headings": p.headings[:40],
        "jsonld_types": ld_types(p.jsonld),
        "microdata_types": sorted(p.itemtypes),
        "forms": p.forms,
        "images": p.imgs,
        "images_no_alt": p.imgs_no_alt,
        "internal_links": len(set(internal)),
        "external_links": len({u for u in p.links if urlsplit(u).netloc not in ("", host)}),
        "script_hosts": script_hosts,
        "text_chars": p.text_len,
        "meta_keywords": bool(p.meta.get("keywords")),
    })
    return rec, internal


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site")
    ap.add_argument("--urls", help="file with one URL per line (e.g. from sitemap_urls.py)")
    ap.add_argument("--sample-per-pattern", type=int, default=0, help="pages per address pattern (0 = all)")
    ap.add_argument("--max-pages", type=int, default=200)
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between requests (default 1)")
    ap.add_argument("--ignore-robots", action="store_true", help="only for the owner's own site, with their OK")
    ap.add_argument("--patterns-only", action="store_true")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", default="crawl")
    a = ap.parse_args()

    host = urlsplit(a.site).netloc
    random.seed(a.seed)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    queue, follow = [], True
    if a.urls:
        listed = [u.strip() for u in Path(a.urls).read_text(encoding="utf-8").splitlines() if u.strip()]
        groups = _patterns.group(listed)
        lines = [f"{len(v):7}  {p}   e.g. {v[0]}" for p, v in groups.items()]
        Path(f"{out}-patterns.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{len(listed)} URLs in {len(groups)} patterns -> {out}-patterns.txt")
        if a.patterns_only:
            print("\n".join(lines[:40]))
            return
        for _, v in groups.items():
            pick = v if not a.sample_per_pattern else random.sample(v, min(a.sample_per_pattern, len(v)))
            queue.extend(pick)
        follow = False
    else:
        queue = [a.site]

    polite = Polite(a.site, delay=a.delay, respect_robots=not a.ignore_robots, user_agent=UA)
    seen, records, skipped = set(), [], Counter()
    with open(f"{out}.jsonl", "w", encoding="utf-8") as jf:
        while queue and len(records) < a.max_pages:
            url = queue.pop(0)
            if url in seen:
                continue
            seen.add(url)
            if urlsplit(url).netloc != host or SKIP_EXT.search(url):
                skipped["other host or file"] += 1
                continue
            if UNSAFE.search(url):
                skipped["state-changing address"] += 1
                continue
            if not polite.allowed(url):
                skipped["robots.txt"] += 1
                continue
            rec, links = scan(polite, url, host)
            records.append(rec)
            jf.write(json.dumps(rec) + "\n")
            jf.flush()
            print(f"[{len(records)}] {rec['status']} {rec['ms']}ms {url}", flush=True)
            if rec["status"] in (429, 503):
                print("Server is pushing back (429/503). Stopping; try later with a longer --delay.")
                break
            if follow:
                queue.extend(u for u in links if u not in seen)

    cols = ["url", "status", "ms", "title", "meta_description", "canonical", "meta_robots", "h1", "jsonld_types",
            "microdata_types", "forms", "images", "images_no_alt", "script_hosts", "redirects"]
    with open(f"{out}.csv", "w", newline="", encoding="utf-8") as cf:
        w = csv.writer(cf)
        w.writerow(cols)
        for r in records:
            w.writerow([
                "|".join(x if isinstance(x, str) else json.dumps(x) for x in v) if isinstance(v, list) else v
                for v in (r.get(c, "") for c in cols)
            ])

    ok = [r for r in records if r["status"] == 200 and "title" in r]
    titles = Counter(r["title"] for r in ok)
    print(f"\n{len(records)} pages fetched, skipped: {dict(skipped) or 'none'}")
    print(f"  no title: {sum(1 for r in ok if not r['title'])}   duplicate titles: {sum(n for n in titles.values() if n > 1)}")
    print(f"  no meta description: {sum(1 for r in ok if not r['meta_description'])}")
    print(f"  H1 count != 1: {sum(1 for r in ok if len(r['h1']) != 1)}")
    print(f"  no canonical: {sum(1 for r in ok if not r['canonical'])}")
    print(f"  images without alt: {sum(r['images_no_alt'] for r in ok)} on {sum(1 for r in ok if r['images_no_alt'])} pages")
    print(f"  structured data types seen: {sorted({t for r in ok for t in r['jsonld_types'] + r['microdata_types']})}")
    print(f"  third-party script hosts: {sorted({h for r in ok for h in r['script_hosts']})}")
    print(f"-> {out}.jsonl, {out}.csv")


if __name__ == "__main__":
    main()
