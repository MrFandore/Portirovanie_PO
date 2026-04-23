#include <iostream>
#include <new>
#include <cstring> 

class SafeString {
private:
    char* data;
    size_t length;

public:
    // Конструктор
    SafeString(const char* str) : data(nullptr), length(0) {
        if (!str) {
            std::cerr << "Ошибка: передана пустая строка\n";
            return;
        }

        length = std::strlen(str);

        data = new(std::nothrow) char[length + 1];
        if (!data) {
            std::cerr << "Ошибка: не удалось выделить память\n";
            length = 0;
            return;
        }

        std::strcpy(data, str);
    }

    // Конструктор копирования
    SafeString(const SafeString& other) : data(nullptr), length(other.length) {
        if (!other.data) {
            return;
        }

        data = new(std::nothrow) char[length + 1];
        if (!data) {
            std::cerr << "Ошибка копирования: нет памяти\n";
            length = 0;
            return;
        }

        std::strcpy(data, other.data);
    }

    // Оператор присваивания
    SafeString& operator=(const SafeString& other) {
        if (this == &other) return *this;

        // Освобождаем старую память
        delete[] data;
        data = nullptr;

        length = other.length;

        if (!other.data) return *this;

        data = new(std::nothrow) char[length + 1];
        if (!data) {
            std::cerr << "Ошибка присваивания: нет памяти\n";
            length = 0;
            return *this;
        }

        std::strcpy(data, other.data);
        return *this;
    }

    // Деструктор
    ~SafeString() {
        delete[] data;
        data = nullptr;
    }

    void print() const {
        if (data)
            std::cout << data << std::endl;
        else
            std::cout << "(пусто)" << std::endl;
    }
};

// Функция, работающая с указателем
void processNumber(int* ptr) {
    if (!ptr) {
        std::cerr << "Ошибка: null указатель\n";
        return;
    }

    *ptr *= 2;
}

int main() {
    int* number = new(std::nothrow) int;

    if (!number) {
        std::cerr << "Ошибка: память не выделена\n";
        return 1;
    }

    *number = 10;
    processNumber(number);

    std::cout << "Результат: " << *number << std::endl;

    delete number;
    number = nullptr;

    // --- Работа с массивом ---
    int* arr = new(std::nothrow) int[5];

    if (!arr) {
        std::cerr << "Ошибка: не удалось выделить массив\n";
        return 1;
    }

    for (int i = 0; i < 5; ++i) {
        arr[i] = i * 10;
    }

    std::cout << "Массив: ";
    for (int i = 0; i < 5; ++i) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;

    delete[] arr;
    arr = nullptr;

    SafeString str1("Привет");
    SafeString str2 = str1;  // копирование
    SafeString str3("Мир");

    str3 = str1; // присваивание

    std::cout << "Строки:\n";
    str1.print();
    str2.print();
    str3.print();

    return 0;
}