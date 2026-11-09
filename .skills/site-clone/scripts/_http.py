"""Small shared HTTP helpers for the site-clone scripts. Standard library only.

Every request is a GET (or HEAD), identifies itself, and never follows a
redirect silently, so callers see exactly what the server answered.
"""
import gzip
import time
import urllib.error
import urllib.request
import urllib.robotparser
from urllib.parse import urljoin, urlsplit

UA = "site-clone-scan/1.0 (read-only)"


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


_opener = urllib.request.build_opener(_NoRedirect)


class Response:
    def __init__(self, url, status, headers, body, error=""):
        self.url = url
        self.status = status
        self.headers = headers or {}
        self.body = body or b""
        self.error = error

    @property
    def text(self):
        enc = "utf-8"
        ctype = self.headers.get("content-type", "")
        if "charset=" in ctype:
            enc = ctype.split("charset=")[-1].split(";")[0].strip() or enc
        try:
            return self.body.decode(enc, errors="replace")
        except LookupError:
            return self.body.decode("utf-8", errors="replace")

    @property
    def location(self):
        loc = self.headers.get("location")
        return urljoin(self.url, loc) if loc else ""


def get(url, timeout=30, method="GET", max_bytes=5_000_000, user_agent=UA):
    """One request, no redirect following. Returns a Response (status 0 on network error)."""
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip",
    })
    try:
        r = _opener.open(req, timeout=timeout)
        status, headers, raw = r.status, r.headers, r.read(max_bytes)
    except urllib.error.HTTPError as e:
        status, headers = e.code, e.headers
        try:
            raw = e.read(max_bytes)
        except Exception:  # noqa: BLE001
            raw = b""
    except Exception as e:  # noqa: BLE001
        return Response(url, 0, {}, b"", error=str(e)[:200])
    hdrs = {k.lower(): v for k, v in headers.items()} if headers else {}
    if hdrs.get("content-encoding") == "gzip" or raw[:2] == b"\x1f\x8b":
        try:
            raw = gzip.decompress(raw)
        except OSError:
            pass
    return Response(url, status, hdrs, raw)


class Polite:
    """Rate limiter plus robots.txt check for one host."""

    def __init__(self, base, delay=1.0, respect_robots=True, user_agent=UA):
        self.delay = delay
        self.user_agent = user_agent
        self._last = 0.0
        self.robots = None
        if respect_robots:
            parts = urlsplit(base)
            rp = urllib.robotparser.RobotFileParser()
            r = get(f"{parts.scheme}://{parts.netloc}/robots.txt", user_agent=user_agent)
            rp.parse(r.text.splitlines() if r.status == 200 else [])
            self.robots = rp

    def allowed(self, url):
        return self.robots is None or self.robots.can_fetch(self.user_agent, url)

    def wait(self):
        gap = time.monotonic() - self._last
        if gap < self.delay:
            time.sleep(self.delay - gap)
        self._last = time.monotonic()

    def get(self, url, **kw):
        self.wait()
        return get(url, user_agent=self.user_agent, **kw)
