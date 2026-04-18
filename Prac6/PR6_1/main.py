import math
import os
import time
from decimal import Decimal, getcontext

# Tочность для сложных вычислений
getcontext().prec = 50

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0: return False
    return True


def run_comprehensive_analysis(input_path, output_path):
    start_time = time.perf_counter()
    metrics = {
        'count': 0,
        'errors': 0,
        'sum': 0.0,
        'min': float('inf'),
        'max': float('-inf'),
        'mean': 0.0,
        'm2': 0.0,
        'harmonic_sum': 0.0,
        'primes_count': 0
    }

    if not os.path.exists(input_path):
        print(f"Ошибка: Файл {input_path} не найден.")
        return

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Очистка от мусора
                clean_line = line.replace(',', ' ').replace(';', ' ').replace('(', ' ').replace(')', ' ')
                parts = clean_line.split()

                for part in parts:
                    try:
                        val = float(part)

                        #1.
                        metrics['count'] += 1
                        metrics['sum'] += val
                        if val < metrics['min']: metrics['min'] = val
                        if val > metrics['max']: metrics['max'] = val

                        #2.
                        delta = val - metrics['mean']
                        metrics['mean'] += delta / metrics['count']
                        delta2 = val - metrics['mean']
                        metrics['m2'] += delta * delta2

                        #3.
                        if val > 0:
                            metrics['harmonic_sum'] += 1.0 / val

                        if val.is_integer() and val > 0:
                            if is_prime(int(val)):
                                metrics['primes_count'] += 1

                    except ValueError:
                        metrics['errors'] += 1
                        continue

        n = metrics['count']
        if n == 0:
            print("Файл не содержит валидных числовых данных.")
            return

        variance = metrics['m2'] / n if n > 1 else 0
        std_dev = math.sqrt(variance)
        h_mean = n / metrics['harmonic_sum'] if metrics['harmonic_sum'] > 0 else "N/A (нужны только положительные числа)"

        execution_time = time.perf_counter() - start_time
        report = [
            "=========================================================",
            "           ОТЧЕТ О МАТЕМАТИЧЕСКОМ АНАЛИЗЕ               ",
            "=========================================================",
            f"Дата обработки:          {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Входной файл:            {input_path}",
            f"Время выполнения:        {execution_time:.6f} секунд",
            f"Всего чисел обработано:  {n}",
            f"Пропущено ошибок/текста: {metrics['errors']}",
            "---------------------------------------------------------",
            "1.",
            f"   - Сумма:              {metrics['sum']}",
            f"   - Минимум:            {metrics['min']}",
            f"   - Максимум:           {metrics['max']}",
            "---------------------------------------------------------",
            "2.",
            f"   - Среднее арифм.:     {metrics['mean']:.4f}",
            f"   - Дисперсия:          {variance:.4f}",
            f"   - Станд. отклонение:  {std_dev:.4f}",
            "---------------------------------------------------------",
            "3.",
            f"   - Среднее гармон.:    {h_mean}",
            f"   - Простых чисел:      {metrics['primes_count']}",
            f"   - Размах выборки:     {metrics['max'] - metrics['min']}",
            f"   - Коэфф. вариации:    {(std_dev / metrics['mean'] * 100) if metrics['mean'] != 0 else 0:.2f}%",
            "========================================================="
        ]
        final_text = "\n".join(report)
        print(final_text)

        with open(output_path, 'w', encoding='utf-8') as f_out:
            f_out.write(final_text)

        print(f"\n[INFO] Отчет успешно сохранен в файл: {output_path}")

    except Exception as e:
        print(f"Критический сбой программы: {e}")

if __name__ == "__main__":
    INPUT_FILE = 'numbers.txt'
    REPORT_FILE = 'report.txt'

    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, 'w') as f:
            f.write("10, 20.5; 7 (ошибка) 13 42 100")

    run_comprehensive_analysis(INPUT_FILE, REPORT_FILE)