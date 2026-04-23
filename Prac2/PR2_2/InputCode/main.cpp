#include <windows.h>
#include <iostream>
#include <vector>

int main() {
    // Путь к файлу (LPCSTR - Long Pointer to Constant STRing)
    LPCSTR fileName = "data.txt";

    // 1. Создание/Открытие файла
    HANDLE hFile = CreateFileA(
        fileName,               // Имя файла
        GENERIC_READ,           // Режим доступа: только чтение
        FILE_SHARE_READ,        // Совместный доступ
        NULL,                   // Атрибуты безопасности
        OPEN_EXISTING,          // Открыть только если файл существует
        FILE_ATTRIBUTE_NORMAL,  // Стандартные атрибуты
        NULL                    // Шаблонный файл
    );

    if (hFile == INVALID_HANDLE_VALUE) {
        std::cerr << "Ошибка CreateFile. Код: " << GetLastError() << std::endl;
        return 1;
    }

    // Подготовка переменных для чтения
    const DWORD BUFFER_SIZE = 1024;
    char buffer[BUFFER_SIZE];
    DWORD bytesRead = 0;

    // 2. Чтение файла
    BOOL result = ReadFile(
        hFile,                  // Хэндл файла
        buffer,                 // Буфер для данных
        BUFFER_SIZE - 1,        // Сколько байт прочитать
        &bytesRead,             // Сколько байт прочитано по факту
        NULL                    // Структура для асинхронного ввода-вывода
    );

    if (result) {
        buffer[bytesRead] = '\0'; // Терминирующий ноль для строки
        std::cout << "Прочитано байт: " << bytesRead << std::endl;
        std::cout << "Данные: " << buffer << std::endl;
    } else {
        std::cerr << "Ошибка ReadFile. Код: " << GetLastError() << std::endl;
    }

    // 3. Закрытие хэндла
    CloseHandle(hFile);

    return 0;
}