import random

def generate_large_file(filename, count):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for i in range(count):
                num = random.uniform(-1000, 1000)
                f.write(f"{round(num, 2)} ")
                if (i + 1) % 10 == 0:
                    f.write("\n")

        print(f"Успешно создано {count} чисел в файле {filename}")
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")

generate_large_file('numbers.txt', 1000000)