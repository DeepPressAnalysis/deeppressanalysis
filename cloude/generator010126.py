from datetime import date, timedelta

BASE_URL = "https://deeppressanalysis.com"

LANGS = ["ru", "ar", "en", "de", "ua", "hi"]

YEAR = 2026
MONTH = 1

XDEFAULT_LANG = "en"


def ddmmyy(d):
    return f"{d.day:02d}{d.month:02d}{str(d.year)[-2:]}"


def url(lang, d):
    return f"{BASE_URL}/{lang}/{ddmmyy(d)}.html"


def month_range(year, month):
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(year, month + 1, 1) - timedelta(days=1)
    return start, end


start, end = month_range(YEAR, MONTH)

lines = [
    "<?xml version='1.0' encoding='utf-8'?>",
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
    '        xmlns:xhtml="http://www.w3.org/1999/xhtml">'
]

d = start
while d <= end:
    for loc_lang in LANGS:
        lines.append("  <url>")
        lines.append(f"    <loc>{url(loc_lang, d)}</loc>")
        lines.append(f"    <lastmod>{d.isoformat()}</lastmod>")

        for l in LANGS:
            hre = "uk" if l == "ua" else l
            lines.append(
                f'    <xhtml:link rel="alternate" hreflang="{hre}" href="{url(l, d)}"/>'
            )

        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url(XDEFAULT_LANG, d)}"/>'
        )

        lines.append("  </url>")
    d += timedelta(days=1)

lines.append("</urlset>")

filename = f"sitemap-{YEAR}-{MONTH:02d}.xml"
with open(filename, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("DONE:", filename)
