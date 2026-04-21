#include <iostream>
#include <cmath>

int factorial(int k) {
    if (k <= 1) {
        return 1;
    }
    return k * factorial(k - 1);
}

int fibonacci(int k) {
    if (k <= 1) {
        return k;
    }
    return fibonacci(k - 1) + fibonacci(k - 2);
}

double complex_math(int n, double x, double y) {
    // базовые операции
    double add = x + y;
    double sub = x - y;
    double mul = x * y;

    // защита от деления на ноль
    double div = (y != 0) ? (x / y) : 0;

    // степень
    double power = pow(x, 2) + pow(y, 3);

    // факториал
    int fact = factorial(n);

    // фибоначчи
    int fib = fibonacci(n);

    // итоговая формула
    double result = add + sub + mul + div + power + fact + fib;

    return result;
}

int main() {
    int n = 5;
    double x = 3.0, y = 2.0;
    std::cout << complex_math(n, x, y) << std::endl;
    return 0;
}