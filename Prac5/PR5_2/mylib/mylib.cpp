#include <iostream>
#include "mylib.h"

int add(int a, int b) {
    return a + b;
}

void print_message(const char* msg) {
    std::cout << "Library says: " << msg << std::endl;
}