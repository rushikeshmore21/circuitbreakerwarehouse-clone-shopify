"""Group URLs into address patterns (page types) without knowing the platform.

A path segment that appears often at the same depth ("products", "category-s")
is kept as is; anything else becomes {x}, keeping its file extension and a
one-letter platform marker like Volusion's "-p" / "-s". Query values become
{v}. Examples:
    /Square-D-EDB34125-p/edb34125.htm  ->  /{x}-p/{x}.htm
    /products/blue-shirt               ->  /products/{x}
    /Articles.asp?ID=242               ->  /Articles.asp?ID={v}
"""
import re
from collections import Counter
from urllib.parse import parse_qsl, urlsplit

_MARK = re.compile(r"^(.+?)(-[a-z])(\.[a-z0-9]{2,5})?$", re.I)
_EXT = re.compile(r"^(.+?)(\.[a-z0-9]{2,5})$", re.I)


def _segments(url):
    p = urlsplit(url)
    return [s for s in p.path.split("/")], p.query


def build(urls, min_count=5):
    """Return a function url -> pattern string, trained on this URL list."""
    seen = Counter()
    for u in urls:
        segs, _ = _segments(u)
        for i, s in enumerate(segs):
            seen[(i, s.lower())] += 1
    total = max(len(urls), 1)

    def generalize(i, seg):
        if seg == "":
            return ""
        n = seen[(i, seg.lower())]
        # Frequent, but not a value that is unique per page (e.g. the only segment).
        if n >= min_count and n < total * 0.98 or n == total and total > 1:
            return seg
        if seg.isdigit():
            return "{n}"
        m = _MARK.match(seg)
        if m:
            return "{x}" + m.group(2) + (m.group(3) or "")
        m = _EXT.match(seg)
        if m:
            return "{x}" + m.group(2)
        return "{x}"

    def pattern(url):
        segs, query = _segments(url)
        path = "/".join(generalize(i, s) for i, s in enumerate(segs)) or "/"
        if query:
            keys = sorted({k for k, _ in parse_qsl(query, keep_blank_values=True)})
            path += "?" + "&".join(f"{k}={{v}}" for k in keys)
        return path

    return pattern


def group(urls, min_count=5):
    pat = build(urls, min_count)
    groups = {}
    for u in urls:
        groups.setdefault(pat(u), []).append(u)
    return dict(sorted(groups.items(), key=lambda kv: -len(kv[1])))
