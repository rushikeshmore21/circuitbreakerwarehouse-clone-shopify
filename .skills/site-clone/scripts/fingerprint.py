"""First look at a site: platform signals, server/CDN headers, third-party
hosts, robots.txt rules and the shape of its sitemap.

    python fingerprint.py https://example.com --out fingerprint.json

About five GET requests in total. The platform guess is a hint; confirm it
by looking at the pages.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _http import Polite  # noqa: E402
import _patterns  # noqa: E402
from sitemap_urls import expand, find_sitemaps  # noqa: E402

SIGNALS = {
    "Volusion": [r"/v/vspfiles/", r"-p/[^\"'/]+\.htm", r"volusion"],
    "Shopify": [r"cdn\.shopify\.com", r"Shopify\.theme", r"myshopify\.com"],
    "BigCommerce": [r"bigcommerce\.com", r"stencil-utils", r"cdn11\.bigcommerce"],
    "WordPress": [r"/wp-content/", r"/wp-includes/", r"wp-json", r'generator" content="WordPress'],
    "WooCommerce": [r"woocommerce", r"wc-ajax", r"wc_add_to_cart_params"],
    "Magento": [r"Magento_", r"mage/cookies", r"static/version\d+"],
    "Wix": [r"static\.wixstatic\.com", r"wix-warmup-data", r"X-Wix-"],
    "Squarespace": [r"static1\.squarespace\.com", r"Squarespace\.", r"squarespace-cdn"],
    "Webflow": [r"website-files\.com", r"data-wf-site", r"webflow\.js"],
    "Drupal": [r"/sites/default/files", r"Drupal\.settings", r"drupal\.js"],
    "Joomla": [r"/media/jui/", r'generator" content="Joomla'],
    "PrestaShop": [r"prestashop", r"id_product="],
    "OpenCart": [r"route=product/", r"catalog/view/theme"],
    "Next.js": [r"/_next/static/", r"__NEXT_DATA__"],
    "Gatsby": [r"___gatsby", r"/page-data/"],
    "Nuxt": [r"/_nuxt/", r"__NUXT__"],
}
HEADER_HINTS = ["server", "x-powered-by", "x-generator", "cf-ray", "x-vercel-id", "x-nf-request-id",
                "x-shopify-stage", "x-wix-request-id", "x-cache", "via", "x-served-by", "set-cookie",
                "strict-transport-security", "content-security-policy"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site")
    ap.add_argument("--out", default="fingerprint.json")
    ap.add_argument("--delay", type=float, default=1.0)
    ap.add_argument("--no-sitemap", action="store_true", help="skip reading the sitemap")
    a = ap.parse_args()

    parts = urlsplit(a.site)
    root = f"{parts.scheme}://{parts.netloc}"
    polite = Polite(root, delay=a.delay, respect_robots=False)

    home = polite.get(root + "/")
    hops = []
    while home.status in (301, 302, 303, 307, 308) and len(hops) < 5:
        hops.append(f"{home.status} {home.location}")
        home = polite.get(home.location)
    html = home.text
    blob = html + "\n" + "\n".join(f"{k}: {v}" for k, v in home.headers.items())

    scores = {name: sum(1 for p in pats if re.search(p, blob, re.I)) for name, pats in SIGNALS.items()}
    platform = [n for n, s in sorted(scores.items(), key=lambda kv: -kv[1]) if s]

    hosts = Counter()
    for u in re.findall(r"""(?:src|href)=["'](https?://[^"'\s>]+)""", html, re.I):
        h = urlsplit(u).netloc.lower()
        if h and h != parts.netloc.lower():
            hosts[h] += 1
    gen = re.search(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)', html, re.I)

    robots = polite.get(root + "/robots.txt")
    robots_lines = [ln for ln in robots.text.splitlines() if ln.strip() and not ln.startswith("#")] if robots.status == 200 else []

    sitemap = {}
    if not a.no_sitemap:
        urls, maps = expand(polite, find_sitemaps(polite, root), 50)
        groups = _patterns.group(urls)
        sitemap = {
            "sitemaps_read": maps,
            "url_count": len(urls),
            "patterns": [{"pattern": p, "count": len(v), "examples": v[:3]} for p, v in list(groups.items())[:40]],
        }

    report = {
        "site": root,
        "home_status": home.status,
        "home_redirects": hops,
        "home_bytes": len(home.body),
        "platform_guess": platform[:3],
        "platform_scores": {k: v for k, v in scores.items() if v},
        "generator_meta": gen.group(1) if gen else "",
        "headers": {k: v for k, v in home.headers.items() if k in HEADER_HINTS},
        "third_party_hosts": hosts.most_common(40),
        "robots_txt": robots_lines[:80],
        "sitemap": sitemap,
    }
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(report, indent=1), encoding="utf-8")

    print(f"Site: {root}  home HTTP {home.status}{'  via ' + ' > '.join(hops) if hops else ''}")
    print(f"Platform guess: {', '.join(platform[:3]) or 'unknown'}  {report['generator_meta']}")
    for k, v in report["headers"].items():
        if k != "set-cookie":
            print(f"  {k}: {v[:100]}")
    print(f"Third-party hosts on home: {len(hosts)}")
    for h, n in hosts.most_common(12):
        print(f"  {n:3}  {h}")
    if sitemap:
        print(f"Sitemap: {sitemap['url_count']} URLs in {len(sitemap['sitemaps_read'])} file(s)")
        for p in sitemap["patterns"][:15]:
            print(f"  {p['count']:7}  {p['pattern']}")
    print(f"-> {a.out}")


if __name__ == "__main__":
    main()
