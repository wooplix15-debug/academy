"""Run after regenerating pages to restore the shared animation assets."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = '<link rel="stylesheet" href="/site-motion.css?v=20261012">'
JS = '<script src="/site-motion.js?v=20261012" defer></script>'

def apply():
    changed = 0
    for page in (ROOT / "public").rglob("*.html"):
        text = page.read_text()
        result = text
        if "/site-motion.css" not in result:
            result = result.replace("</head>", CSS + "</head>", 1)
        if "/site-motion.js" not in result:
            result = result.replace("</body>", JS + "</body>", 1)
        if result != text:
            page.write_text(result)
            changed += 1
    print(f"Shared motion added to {changed} pages")

if __name__ == "__main__":
    apply()
