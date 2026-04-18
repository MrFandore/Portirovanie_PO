import requests
import json
import sys
import re
import subprocess
import tempfile
import os
from typing import Tuple, Optional

class UniversalTranslator:
    def __init__(self, model: str = "qwen3-coder:30b", ollama_url: str = "http://localhost:11434/api/generate"):
        self.model = model
        self.ollama_url = ollama_url
        self.max_attempts = 3
        self.temperature = 0
        self.top_p = 0.1
        self.num_ctx = 8192

    def _build_prompt(self, source_code: str, source_lang: str, target_lang: str,
                      error_feedback: Optional[str] = None) -> str:
        prompt = f"""Ты — строгий компилятор и транслятор кода, а не помощник.

        Твоя задача: выполнить ПОСТРОЧНЫЙ перевод кода с {source_lang} на {target_lang}.

        ====================
        СТРОГИЕ ПРАВИЛА (ОБЯЗАТЕЛЬНЫ)
        ====================

        1. СОХРАНИ СТРУКТУРУ КОДА:
        - Не изменяй архитектуру
        - Не разбивай функции
        - Не объединяй функции
        - Не переименовывай функции, классы и переменные
        - Сохрани порядок строк максимально близко к оригиналу

        2. ЗАПРЕЩЕНО:
        - рефакторинг
        - оптимизация
        - “улучшения”
        - упрощение логики
        - добавление новой логики
        - удаление частей кода

        3. ДОПУСТИМО ТОЛЬКО:
        - замена синтаксиса {source_lang} → {target_lang}
        - добавление ОБЯЗАТЕЛЬНЫХ импортов
        - минимальные изменения для компиляции

        4. ОБРАБОТКА НЕСОВМЕСТИМОСТЕЙ:
        Если в {target_lang} нет прямого аналога:
        → реализуй максимально близкий эквивалент
        → НЕ меняй поведение программы

        5. РАБОТА С ИСКЛЮЧЕНИЯМИ:
        - Все исключения должны быть корректны для {target_lang}
        - Код должен компилироваться без ошибок

        6. КОД ДОЛЖЕН БЫТЬ:
        - полностью рабочим
        - самодостаточным
        - без пропусков

        ====================
        ФОРМАТ ВЫВОДА (КРИТИЧНО)
        ====================

        - Выведи ТОЛЬКО код
        - Без пояснений
        - Без комментариев (если их не было в исходнике)
        - Без markdown (никаких ```)
        - Без лишнего текста
        - Начни сразу с кода

        ====================
        САМОПРОВЕРКА ПЕРЕД ОТВЕТОМ
        ====================

        Перед выводом убедись:
        - код компилируется
        - нет пропущенных строк
        - нет "TODO", "FIXME", "..."
        - структура совпадает с оригиналом
        - логика не изменена

        ЕСЛИ структура или логика изменена → ответ неверный, исправь.

        ====================
        КОД ДЛЯ ПЕРЕВОДА
        ====================
        """

        if error_feedback:
            prompt += f"\n\nПредыдущая попытка вызвала ошибку:\n{error_feedback}\nПожалуйста, исправь код.\n"
        prompt += f"\nИсходный код ({source_lang}):\n```\n{source_code}\n```\n\nКод на {target_lang}:"
        return prompt

    def _call_llm(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": self.temperature}
        }
        response = requests.post(self.ollama_url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["response"].strip()

    def _extract_code(self, llm_response: str, target_lang: str) -> str:
        # Удаляем markdown-блоки
        patterns = [
            rf"```{target_lang.lower()}\s*(.*?)\s*```",
            r"```\s*(.*?)\s*```",
            r"`{3}.*?\n(.*?)`{3}",
        ]
        for pattern in patterns:
            match = re.search(pattern, llm_response, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return llm_response.strip()

    def _validate_syntax(self, code: str, target_lang: str) -> Tuple[bool, str]:
        lang = target_lang.lower()
        if lang in ("python", "py"):
            try:
                compile(code, "<string>", "exec")
                return True, ""
            except SyntaxError as e:
                return False, str(e)
        elif lang == "java":
            try:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
                    f.write(code)
                    temp_file = f.name
                try:
                    result = subprocess.run(['javac', temp_file], capture_output=True, text=True, timeout=15)
                    os.unlink(temp_file)
                    return result.returncode == 0, result.stderr
                except FileNotFoundError:
                    print("javac не найден. Установите JDK или проверка синтаксиса Java пропущена.")
                    return True, ""  # Пропускаем проверку
                except Exception as e:
                    return False, str(e)
            except Exception as e:
                return False, str(e)
        elif lang in ("c", "cpp"):
            compiler = 'gcc' if lang == 'c' else 'g++'
            try:
                with tempfile.NamedTemporaryFile(mode='w', suffix=('.c' if lang == 'c' else '.cpp'), delete=False) as f:
                    f.write(code)
                    temp_file = f.name
                try:
                    result = subprocess.run([compiler, '-fsyntax-only', temp_file], capture_output=True, text=True,
                                            timeout=15)
                    os.unlink(temp_file)
                    return result.returncode == 0, result.stderr
                except FileNotFoundError:
                    print(f"{compiler} не найден. Пропускаем проверку.")
                    return True, ""
                except Exception as e:
                    return False, str(e)
            except Exception as e:
                return False, str(e)
        elif lang in ("javascript", "js"):
            try:
                result = subprocess.run(['node', '--check', '-e', code], capture_output=True, text=True, timeout=15)
                return result.returncode == 0, result.stderr
            except FileNotFoundError:
                print("node не найден. Пропускаем проверку.")
                return True, ""
            except Exception as e:
                return False, str(e)
        else:
            return True, ""  # Для других языков не проверяем

    def translate(self, source_code: str, source_lang: str, target_lang: str) -> str:
        last_error = None
        current_code = source_code
        for attempt in range(self.max_attempts):
            prompt = self._build_prompt(current_code, source_lang, target_lang, last_error)
            try:
                raw_response = self._call_llm(prompt)
                translated = self._extract_code(raw_response, target_lang)
                valid, error_msg = self._validate_syntax(translated, target_lang)
                if valid:
                    print(f"Попытка {attempt + 1} успешна!")
                    return translated
                else:
                    print(f"Попытка {attempt + 1} не удалась. Ошибка:\n{error_msg[:200]}")
                    last_error = error_msg
                    current_code = translated
            except Exception as e:
                print(f"Ошибка вызова LLM: {e}")
                last_error = str(e)
        raise RuntimeError(f"Не удалось получить валидный код после {self.max_attempts} попыток.")


def main():
    if len(sys.argv) < 4:
        print("Использование: python universal_translator.py <исходный_язык> <целевой_язык> <файл>")
        print("Пример: python universal_translator.py python java sieve.py")
        sys.exit(1)

    source_lang, target_lang, file_path = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()

    translator = UniversalTranslator(model="qwen2.5-coder:7b")
    try:
        result = translator.translate(source_code, source_lang, target_lang)
        print("\n ----Переведенный код---- \n")
        print(result)
        output_file = f"output.{target_lang}"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"\nСохранено в {output_file}")
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()