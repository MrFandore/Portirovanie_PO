import concurrent.futures
import time
import math


def is_prime(n):
    """Функция проверки числа на простоту — требует много ресурсов."""
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    # Проверяем делители до корня из n
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def count_primes_in_range(start, end):
    """Считает количество простых чисел в заданном диапазоне."""
    count = 0
    for i in range(start, end):
        if is_prime(i):
            count += 1
    return count


def main():
    # Настройки задачи
    total_limit = 5_000_000  # Ищем простые числа до 5 миллионов
    num_workers = 4  # Количество параллельных процессов

    # Разделяем задачу на части (диапазоны)
    step = total_limit // num_workers
    ranges = [(i, i + step) for i in range(0, total_limit, step)]

    print(f"Задача: найти количество простых чисел до {total_limit}")
    print(f"Разделение на {num_workers} диапазона(ов)...")

    # --- 1. Последовательное выполнение ---
    print("\nЗапуск последовательно...")
    start_time = time.time()
    seq_result = count_primes_in_range(0, total_limit)
    seq_duration = time.time() - start_time
    print(f"Результат: {seq_result}, Время: {seq_duration:.2f} сек.")

    # --- 2. Параллельное выполнение ---
    print(f"\nЗапуск параллельно на {num_workers} ядрах...")
    start_time = time.time()

    # Используем ProcessPoolExecutor для распределения задач
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Передаем каждый диапазон в отдельный процесс
        futures = [executor.submit(count_primes_in_range, r[0], r[1]) for r in ranges]

        # Собираем результаты по мере готовности
        par_result = sum(f.result() for f in futures)

    par_duration = time.time() - start_time
    print(f"Результат: {par_result}, Время: {par_duration:.2f} сек.")

    # Итог
    speedup = seq_duration / par_duration
    print(f"\nУскорение: в {speedup:.2f} раза")


if __name__ == "__main__":
    main()