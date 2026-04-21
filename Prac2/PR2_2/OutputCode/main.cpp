#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <iostream>
#include <vector>
#include <cstring>

int main() {
    // Путь к файлу
    const char* fileName = "data.txt";

    // 1. Создание/Открытие файла
    int fd = open(fileName, O_RDONLY);
    if (fd == -1) {
        std::cerr << "Ошибка open. Код: " << errno << std::endl;
        return 1;
    }

    // Подготовка переменных для чтения
    const size_t BUFFER_SIZE = 1024;
    char buffer[BUFFER_SIZE];
    ssize_t bytesRead = 0;

    // 2. Чтение файла
    bytesRead = read(fd, buffer, BUFFER_SIZE - 1);
    if (bytesRead >= 0) {
        buffer[bytesRead] = '\0'; // Терминирующий ноль для строки
        std::cout << "Прочитано байт: " << bytesRead << std::endl;
        std::cout << "Данные: " << buffer << std::endl;
    } else {
        std::cerr << "Ошибка read. Код: " << errno << std::endl;
    }

    // 3. Закрытие дескриптора
    close(fd);

    return 0;
}