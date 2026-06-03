from pathlib import Path
import re

pattern = re.compile(r'href=(["\'])([^"\']*archive\.html)\1', re.IGNORECASE)

for file in Path(".").rglob("*.html"):
    parts = file.parts

    lang = None
    for p in parts:
        if p in ["ua", "ru", "de", "es", "ar"]:
            lang = p
            break

    if not lang:
        continue

    html = file.read_text(encoding="utf-8", errors="ignore")
    correct = f"https://deeppressanalysis.com/{lang}/archive.html"

    for m in pattern.finditer(html):
        old = m.group(2)
        if old != correct:
            print(file)
            print("  БЫЛО: ", old)
            print("  БУДЕТ:", correct)
            print()
