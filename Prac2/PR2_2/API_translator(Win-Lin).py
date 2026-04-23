import requests
import re
import os
import subprocess
import tempfile
from typing import Optional

class WinToLinuxTranslator:
    def __init__(
            self,
            model: str = "qwen3-coder:30b",
            ollama_url: str = "http://127.0.0.1:11434/api/generate",
            verify_compile: bool = True
    ):
        self.model = model
        self.ollama_url = ollama_url
        self.verify_compile = verify_compile
        self.max_attempts = 3
        self.temperature = 0.1
        self.num_ctx = 16384

    def _build_prompt(self, source_code: str, error_feedback: Optional[str] = None) -> str:
        prompt = """Ты — эксперт по портированию C/C++ кода с Windows на Linux (POSIX).

        ЗАДАЧА:
        Переписать код так, чтобы он компилировался и работал на Linux.

        ====================
        ПРАВИЛА
        ====================

        1. ЗАМЕНЯЙ WINDOWS API:
        - Sleep → usleep/nanosleep
        - CreateThread → pthread_create
        - VirtualAlloc → mmap
        - HANDLE → pthread_t / int
        - DWORD → uint32_t
        - LPVOID → void*

        2. РАЗРЕШАЕТСЯ:
        - менять реализацию
        - добавлять код
        - переписывать API вызовы

        3. НЕЛЬЗЯ:
        - ломать логику программы
        - удалять функциональность

        4. ИСПОЛЬЗУЙ:
        <unistd.h>, <pthread.h>, <sys/mman.h>, <signal.h>

        ====================
        КРИТИЧНО
        ====================
        - Код ДОЛЖЕН компилироваться
        - Не пропускай строки
        - Не оставляй TODO

        ====================
        ВЫВОД
        ====================
        ТОЛЬКО КОД
        БЕЗ ``` И БЕЗ ПОЯСНЕНИЙ
        """

        if error_feedback:
            prompt += f"\n\nКРИТИЧЕСКАЯ ОШИБКА КОМПИЛЯЦИИ:\n{error_feedback}\nИсправь этот код, чтобы g++ его принял."

        prompt += f"\n\nWindows код:\n{source_code}\n\nLinux код:"
        return prompt

    def _check_compilation(self, code: str) -> Optional[str]:
        if not self.verify_compile:
            return None
        
        with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False) as tmp:
            tmp.write(code.encode('utf-8'))
            tmp_path = tmp.name

        try:
            result = subprocess.run(
                ["g++", "-fsyntax-only", "-pthread", tmp_path],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                return result.stderr
            return None
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def _call_llm(self, prompt: str) -> str:
        payload = {
            "model": self.model, "prompt": prompt, "stream": False,
            "options": {"temperature": self.temperature, "num_ctx": self.num_ctx}
        }
        response = requests.post(self.ollama_url, json=payload, timeout=180)
        response.raise_for_status()
        return response.json().get("response", "").strip()

    def _extract_code(self, text: str) -> str:
        text = re.sub(r"```[\w]*", "", text)
        return text.replace("```", "").strip()

    def translate(self, source_code: str) -> str:
        last_error = None

        for attempt in range(self.max_attempts):
            print(f"  ↳ Попытка {attempt + 1}")

            prompt = self._build_prompt(source_code, last_error)
            raw = self._call_llm(prompt)
            code = self._extract_code(raw)

            if not code or len(code) < 20:
                last_error = "LLM вернул пустой или слишком короткий код."
                continue

            # Проверка компиляции
            compile_error = self._check_compilation(code)
            if compile_error:
                print(f"Ошибка компиляции на попытке {attempt + 1}")
                last_error = compile_error
                continue

            if self.verify_compile:
                print(f"Код успешно прошел проверку g++")
            return code

        raise RuntimeError(f"Не удалось получить корректный код после {self.max_attempts} попыток.")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    input_dir = os.path.join(base_dir, "InputCode")
    output_dir = os.path.join(base_dir, "OutputCode")

    if not os.path.exists(input_dir):
        print(f"Папка InputCode не найдена: {input_dir}")
        return

    os.makedirs(output_dir, exist_ok=True)

    files = [
        f for f in os.listdir(input_dir)
        if os.path.isfile(os.path.join(input_dir, f))
    ]

    if not files:
        print("Папка InputCode пустая")
        return

    translator = WinToLinuxTranslator()

    print(f"Найдено файлов: {len(files)}")

    for filename in files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        print(f"\n[*] Обработка: {filename}")

        try:
            with open(input_path, "r", encoding="utf-8") as f:
                source = f.read()

            result = translator.translate(source)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result)

            print(f"Сохранено: {output_path}")

        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()