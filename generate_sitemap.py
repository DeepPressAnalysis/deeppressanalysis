
import os
import datetime
import xml.etree.ElementTree as ET

BASE_URL = "https://deeppressanalysis.com"

# Папки и файлы, которые не надо включать
EXCLUDE_DIRS = {".git", ".github", "assets", "img", "images", "cloud", "cloude", "node_modules"}
EXCLUDE_FILES = {"404.html"}

def collect_urls():
    urls = []

    for root, dirs, files in os.walk("."):
        # отфильтровываем папки
        dirs[:] = [d for d in dirs
                   if d not in EXCLUDE_DIRS and not d.startswith(".")]

        for fname in files:
            if not fname.endswith(".html"):
                continue
            if fname in EXCLUDE_FILES:
                continue

            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, ".").replace(os.sep, "/")

            # корневой index.html → https://deeppressanalysis.com/
            if rel_path == "index.html":
                loc = f"{BASE_URL}/"
            else:
                loc = f"{BASE_URL}/{rel_path}"

            mtime = os.path.getmtime(full_path)
            lastmod = datetime.date.fromtimestamp(mtime).isoformat()

            urls.append((loc, lastmod))

    urls.sort(key=lambda x: x[0])
    return urls


def build_sitemap(urls, outfile="sitemap.xml"):
    urlset = ET.Element(
        "urlset",
        attrib={"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    )

    for loc, lastmod in urls:
        url_el = ET.SubElement(urlset, "url")

        loc_el = ET.SubElement(url_el, "loc")
        loc_el.text = loc

        lastmod_el = ET.SubElement(url_el, "lastmod")
        lastmod_el.text = lastmod

    tree = ET.ElementTree(urlset)
    try:
        ET.indent(tree, space="  ", level=0)  # Python 3.9+
    except AttributeError:
        # если старая версия Python — просто без красивых отступов
        pass

    tree.write(outfile, encoding="utf-8", xml_declaration=True)
    print(f"Saved {outfile} with {len(urls)} URLs")


if __name__ == "__main__":
    urls = collect_urls()
    build_sitemap(urls)
