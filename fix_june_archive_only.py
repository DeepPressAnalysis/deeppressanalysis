from pathlib import Path
import re
import shutil
from datetime import datetime

TARGETS = {
    "es": "https://deeppressanalysis.com/es/archive.html",
    "ar": "https://deeppressanalysis.com/ar/archive.html",
    "ua": "https://deeppressanalysis.com/ua/archive.html",
    "ru": "https://deeppressanalysis.com/ru/archive.html",
    "de": "https://deeppressanalysis.com/de/archive.html",
}

DATES = ["010626", "020626", "030626"]

backup_dir = Path("_backup_june_archive_fix_" + datetime.now().strftime("%Y%m%d_%H%M%S"))

# Меняет только ссылку-кнопку архива class="btn-text"
a_tag_pattern = re.compile(
    r'<a\b(?P<attrs>[^>]*class=["\'][^"\']*\bbtn-text\b[^"\']*["\'][^>]*)>(?P<text>.*?)</a>',
    re.IGNORECASE | re.DOTALL
)

href_pattern = re.compile(r'href=(["\'])(.*?)\1', re.IGNORECASE)

archive_words = [
    "archive",
    "archiv",
    "архив",
    "archivo",
    "архів",
    "الأرشيف",
]

changed_files = 0
changed_links = 0

for lang, correct_url in TARGETS.items():
    for date in DATES:
        file = Path(lang) / f"{date}.html"

        if not file.exists():
            print(f"SKIP, файла нет: {file}")
            continue

        old_html = file.read_text(encoding="utf-8", errors="ignore")

        def replace_link(match):
            global changed_links

            text_clean = re.sub(r"<[^>]+>", "", match.group("text")).strip().lower()
            attrs = match.group("attrs")

            if not any(word in text_clean for word in archive_words):
                return match.group(0)

            href_match = href_pattern.search(attrs)
            if not href_match:
                return match.group(0)

            old_href = href_match.group(2)

            if old_href == correct_url:
                return match.group(0)

            quote = href_match.group(1)
            new_attrs = href_pattern.sub(f'href={quote}{correct_url}{quote}', attrs, count=1)

            print(f"FIX: {file}")
            print(f"  БЫЛО:  {old_href}")
            print(f"  СТАЛО: {correct_url}")

            changed_links += 1
            return f'<a{new_attrs}>{match.group("text")}</a>'

        new_html = a_tag_pattern.sub(replace_link, old_html)

        if new_html != old_html:
            backup_file = backup_dir / file
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, backup_file)
            file.write_text(new_html, encoding="utf-8")
            changed_files += 1

print("")
print(f"ГОТОВО. Изменено файлов: {changed_files}")
print(f"Изменено ссылок: {changed_links}")
print(f"Бэкап измененных файлов: {backup_dir}")
