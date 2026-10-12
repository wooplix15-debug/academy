#!/usr/bin/env python3
"""Set canonical and Open Graph URLs for all pages in public/.

Run with the current Vercel origin, or pass a new primary origin when the
custom domain is connected, for example: python tools/sync_site_urls.py https://vivekpandey.ai
"""

from pathlib import Path
import re
import sys


DEFAULT_ORIGIN = "https://academy-tools-jade.vercel.app"
PUBLIC_DIR = Path(__file__).resolve().parents[1] / "public"
CANONICAL_RE = re.compile(r'<link\s+rel=["\']canonical["\'][^>]*>', re.I)
OG_URL_RE = re.compile(r'<meta\s+property=["\']og:url["\'][^>]*>', re.I)


def route_for(page: Path) -> str:
    route = page.relative_to(PUBLIC_DIR).as_posix().removesuffix(".html")
    if route == "index":
        route = ""
    elif route.endswith("/index"):
        route = route[: -len("/index")]
    return "/" + route if route else "/"


def replace_or_insert(text: str, pattern: re.Pattern[str], tag: str) -> str:
    if pattern.search(text):
        return pattern.sub(tag, text, count=1)
    return text.replace("</head>", f"  {tag}\n</head>", 1)


def main() -> None:
    origin = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else DEFAULT_ORIGIN
    if not origin.startswith("https://"):
        raise SystemExit("Use an https:// site origin.")

    pages = sorted(PUBLIC_DIR.rglob("*.html"))
    for page in pages:
        text = page.read_text(encoding="utf-8")
        route = route_for(page)
        page_url = origin + route
        text = text.replace(DEFAULT_ORIGIN, origin)
        head, marker, body = text.partition("</head>")
        if not marker:
            continue
        head = replace_or_insert(
            head,
            CANONICAL_RE,
            f'<link rel="canonical" href="{page_url}">',
        )
        head = replace_or_insert(
            head,
            OG_URL_RE,
            f'<meta property="og:url" content="{page_url}">',
        )
        page.write_text(head + marker + body, encoding="utf-8")
    print(f"Updated canonical and Open Graph URLs in {len(pages)} pages for {origin}")


if __name__ == "__main__":
    main()
