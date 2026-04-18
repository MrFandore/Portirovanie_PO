import os
import sys

def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_docx(file_path):
    from docx import Document
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def read_pdf(file_path):
    import PyPDF2
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = []
        for page in reader.pages:
            text.append(page.extract_text())
    return '\n'.join(text)

def read_doc(file_path):
    return None

def read_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        return read_txt(file_path)
    elif ext == '.docx':
        return read_docx(file_path)
    elif ext == '.pdf':
        return read_pdf(file_path)
    elif ext == '.doc':
        raise NotImplementedError("Формат .doc не поддерживается напрямую. Пожалуйста, конвертируйте файл в .docx или .txt.")
    else:
        raise ValueError(f"Неподдерживаемый формат: {ext}")

def analyze_text(text):
    """
    Анализирует текст и возвращает статистику:
    - количество символов (с пробелами)
    - количество слов
    - количество предложений (по . ! ?)
    """
    char_count = len(text)
    word_count = len(text.split())
    sentence_endings = {'.', '!', '?'}
    sentence_count = 0
    for char in text:
        if char in sentence_endings:
            sentence_count += 1
    if text and text[-1] not in sentence_endings:
        sentence_count += 1
    if sentence_count < 1:
        sentence_count = 1
    return {
        "characters": char_count,
        "words": word_count,
        "sentences": sentence_count
    }

def main():
    if len(sys.argv) < 2:
        print("Использование: python text_processor.py <путь_к_файлу>")
        print("Поддерживаемые форматы: .txt, .docx, .pdf")
        return

    file_path = sys.argv[1]
    try:
        text = read_file(file_path)
        stats = analyze_text(text)
        print(f"Файл: {file_path}")
        print(f"Символов: {stats['characters']}")
        print(f"Слов: {stats['words']}")
        print(f"Предложений: {stats['sentences']}")
        # Показываем первые 200 символов текста
        print("\n--- Первые 200 символов текста ---")
        print(text[:200] + ("..." if len(text) > 200 else ""))
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()