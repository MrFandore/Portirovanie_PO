def complex_math(n, x, y):
    # базовые операции
    add = x + y
    sub = x - y
    mul = x * y

    # защита от деления на ноль
    div = x / y if y != 0 else 0

    # степень
    power = x ** 2 + y ** 3

    # факториал
    def factorial(k):
        if k <= 1:
            return 1
        return k * factorial(k - 1)

    fact = factorial(n)

    # фибоначчи
    def fibonacci(k):
        if k <= 1:
            return k
        return fibonacci(k - 1) + fibonacci(k - 2)

    fib = fibonacci(n)

    # итоговая формула
    result = add + sub + mul + div + power + fact + fib

    return result

