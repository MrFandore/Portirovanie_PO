import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import threading
from collections import Counter


class ModernAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Биба Читалка")
        self.root.geometry("800x600")
        self.root.configure(bg="#2b2b2b")

        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Настройка цветов темы
        bg_color = "#2b2b2b"
        accent_color = "#3d3d3d"
        text_color = "#ffffff"
        highlight = "#4a90e2"

        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabel", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

        # Стилизация вкладок
        self.style.configure("TNotebook", background=bg_color, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=accent_color, foreground=text_color, padding=[15, 5])
        self.style.map("TNotebook.Tab", background=[("selected", highlight)])

        # Стилизация кнопки
        self.style.configure("Accent.TButton", padding=10, font=("Segoe UI", 10, "bold"))

    def setup_ui(self):
        # Верхняя панель управления
        header_frame = ttk.Frame(self.root, padding=20)
        header_frame.pack(fill="x")

        ttk.Label(header_frame, text="Прикол читалка", style="Header.TLabel").pack(side="left")

        self.btn_open = ttk.Button(header_frame, text="Открыть файл", style="Accent.TButton",
                                   command=self.start_analysis_thread)
        self.btn_open.pack(side="right")

        # Основная область с вкладками
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        # Вкладка 1: Консоль анализа
        self.tab_log = ttk.Frame(self.tabs, padding=15)
        self.tabs.add(self.tab_log, text="  ОТЧЕТ  ")

        self.result_text = tk.Text(
            self.tab_log, bg="#1e1e1e", fg="#dcdcdc",
            font=("Consolas", 11), padx=15, pady=15,
            borderwidth=0, insertbackground="white"
        )
        self.result_text.pack(expand=True, fill="both")

        # Вкладка 2: Топ слов
        self.tab_stats = ttk.Frame(self.tabs, padding=15)
        self.tabs.add(self.tab_stats, text="  ЧАСТОТНЫЙ СЛОВАРЬ  ")

        # Список с кастомным скроллбаром
        stats_container = ttk.Frame(self.tab_stats)
        stats_container.pack(expand=True, fill="both")

        self.stats_list = tk.Listbox(
            stats_container, bg="#1e1e1e", fg="#4a90e2",
            font=("Segoe UI", 11), borderwidth=0, highlightthickness=0
        )
        self.stats_list.pack(side="left", expand=True, fill="both")

        scrollbar = ttk.Scrollbar(stats_container, orient="vertical", command=self.stats_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.stats_list.config(yscrollcommand=scrollbar.set)

        # Прогресс-бар в самом низу
        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", side="bottom")

    def log(self, message, is_header=False):
        self.result_text.config(state="normal")
        if is_header:
            self.result_text.insert(tk.END, f"\n{message.upper()}\n" + "=" * 40 + "\n", "header")
        else:
            self.result_text.insert(tk.END, f"• {message}\n")
        self.result_text.config(state="disabled")
        self.result_text.see(tk.END)

    def start_analysis_thread(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.result_text.config(state="normal")
            self.result_text.delete('1.0', tk.END)
            self.stats_list.delete(0, tk.END)
            threading.Thread(target=self.heavy_processing, args=(file_path,), daemon=True).start()

    def heavy_processing(self, file_path):
        try:
            self.root.after(0, lambda: self.progress.config(value=10))
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read()

            self.root.after(0, lambda: self.log(f"Анализ файла: {file_path.split('/')[-1]}", True))

            # Логика анализа
            words = re.findall(r'\w+', data.lower())
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', data)
            sentences = re.split(r'[.!?]+', data)

            self.root.after(0, lambda: self.progress.config(value=50))

            # Вывод данных
            self.root.after(0, lambda: self.log(f"Всего слов: {len(words)}"))
            self.root.after(0, lambda: self.log(f"Найдено email: {len(emails)}"))
            if emails: self.root.after(0, lambda: self.log(f"Пример: {emails[0]}"))

            # Частотка
            common = Counter(words).most_common(50)
            self.root.after(0, self.update_stats_ui, common)

            self.root.after(0, lambda: self.progress.config(value=100))
            self.root.after(0, lambda: messagebox.showinfo("Готово", "Данные успешно обработаны"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка доступа: {str(e)}"))

    def update_stats_ui(self, stats):
        for i, (word, count) in enumerate(stats, 1):
            self.stats_list.insert(tk.END, f" {i:02d}. {word.ljust(20)} | Повторов: {count}")
            if i % 2 == 0:
                self.stats_list.itemconfig(i - 1, bg="#252525")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernAnalyzer(root)
    root.mainloop()