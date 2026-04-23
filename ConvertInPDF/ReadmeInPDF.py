import markdown
import pdfkit
import chardet
import os
from pathlib import Path
from bs4 import BeautifulSoup


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def fix_image_paths(html_content, base_dir):
    """Заменяет относительные пути в img src на абсолютные (file://)"""
    soup = BeautifulSoup(html_content, 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src')
        if not src:
            continue
        # Если путь уже абсолютный (http, https, file://, или начинается с диска C:\) — не трогаем
        if src.startswith(('http://', 'https://', 'file://', 'data:')):
            continue
        if os.path.isabs(src) and os.path.exists(src):
            # Абсолютный путь в стиле Windows, например C:\folder\image.png
            abs_path = src
        else:
            # Относительный путь — склеиваем с базовой директорией
            abs_path = os.path.normpath(os.path.join(base_dir, src))
        if os.path.exists(abs_path):
            # Превращаем в file:// URL для Windows
            abs_path_url = Path(abs_path).as_uri()
            img['src'] = abs_path_url
        else:
            print(f"⚠️ Предупреждение: файл не найден - {abs_path}")
    return str(soup)


def convert_md_to_pdf_with_images(md_path, pdf_path):
    base_dir = os.path.dirname(os.path.abspath(md_path))
    encoding = detect_encoding(md_path)
    print(f"Кодировка файла: {encoding}")

    with open(md_path, 'r', encoding=encoding) as f:
        md_content = f.read()

    # Конвертируем Markdown -> HTML
    html_content = markdown.markdown(md_content, extensions=['extra', 'toc'])

    # Исправляем пути к изображениям
    html_with_abs_images = fix_image_paths(html_content, base_dir)

    # Оборачиваем в полноценный HTML
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>README</title>
    <style>
        body {{ font-family: Arial, sans-serif; font-size: 12pt; margin: 20mm; }}
        img {{ max-width: 100%; height: auto; }}
        pre, code {{ font-family: Consolas, monospace; background-color: #f5f5f5; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; }}
    </style>
</head>
<body>
{html_with_abs_images}
</body>
</html>"""

    options = {
        'encoding': 'UTF-8',
        'enable-local-file-access': None,  # разрешаем локальные файлы
        'page-size': 'A4',
        'margin-top': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '15mm',
        'margin-right': '15mm',
    }

    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

    try:
        pdfkit.from_string(full_html, pdf_path, options=options, configuration=config)
        print(f"✅ PDF создан: {pdf_path}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("Проверьте, что wkhtmltopdf установлен по указанному пути.")


if __name__ == "__main__":
    convert_md_to_pdf_with_images('../Prac1/README.md', '../PDF_Otcheti/Отчет_1.pdf')