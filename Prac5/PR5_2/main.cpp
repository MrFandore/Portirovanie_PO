#include <iostream>
#include "mylib/mylib.h"

int main() {
    int result = add(3, 4);
    std::cout << "Result: " << result << std::endl;

    print_message("Hello from main!");

    return 0;
}