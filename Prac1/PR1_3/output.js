javascript
function complex_math(n, x, y) {
    // базовые операции
    let add = x + y;
    let sub = x - y;
    let mul = x * y;

    // защита от деления на ноль
    let div = y !== 0 ? x / y : 0;

    // степень
    let power = Math.pow(x, 2) + Math.pow(y, 3);

    // факториал
    function factorial(k) {
        if (k <= 1) {
            return 1;
        }
        return k * factorial(k - 1);
    }

    let fact = factorial(n);

    // фибоначчи
    function fibonacci(k) {
        if (k <= 1) {
            return k;
        }
        return fibonacci(k - 1) + fibonacci(k - 2);
    }

    let fib = fibonacci(n);

    // итоговая формула
    let result = add + sub + mul + div + power + fact + fib;

    return result;
}