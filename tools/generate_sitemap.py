#!/usr/bin/env python3
"""Regenerate the public sitemap from deployable HTML pages."""

from pathlib import Path
from xml.etree import ElementTree as ET


BASE_URL = "https://academy-tools-jade.vercel.app"
PUBLIC_DIR = Path(__file__).resolve().parents[1] / "public"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
EXCLUDED = {"lab-verification.html"}


def public_url(page: Path) -> str:
    route = page.relative_to(PUBLIC_DIR).as_posix()
    route = route.removesuffix(".html")
    if route == "index":
        route = ""
    elif route.endswith("/index"):
        route = route[: -len("/index")]
    return BASE_URL + (f"/{route}" if route else "/")


def main() -> None:
    ET.register_namespace("", SITEMAP_NS)
    root = ET.Element(f"{{{SITEMAP_NS}}}urlset")
    pages = sorted(
        page for page in PUBLIC_DIR.rglob("*.html") if page.name not in EXCLUDED
    )
    for page in pages:
        item = ET.SubElement(root, f"{{{SITEMAP_NS}}}url")
        ET.SubElement(item, f"{{{SITEMAP_NS}}}loc").text = public_url(page)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(PUBLIC_DIR / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    print(f"Wrote {len(pages)} URLs to {PUBLIC_DIR / 'sitemap.xml'}")


if __name__ == "__main__":
    main()
