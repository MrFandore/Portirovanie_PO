import java.util.function.IntUnaryOperator;

public class ComplexMath {
    public static int complex_math(int n, int x, int y) {
        // базовые операции
        int add = x + y;
        int sub = x - y;
        int mul = x * y;

        // защита от деления на ноль
        double div = y != 0 ? (double) x / y : 0;

        // степень
        double power = Math.pow(x, 2) + Math.pow(y, 3);

        // факториал
        IntUnaryOperator factorial = new IntUnaryOperator() {
            public int applyAsInt(int k) {
                if (k <= 1)
                    return 1;
                return k * applyAsInt(k - 1);
            }
        };
        int fact = factorial.applyAsInt(n);

        // фибоначчи
        IntUnaryOperator fibonacci = new IntUnaryOperator() {
            public int applyAsInt(int k) {
                if (k <= 1)
                    return k;
                return applyAsInt(k - 1) + applyAsInt(k - 2);
            }
        };
        int fib = fibonacci.applyAsInt(n);

        // итоговая формула
        double result = add + sub + mul + div + power + fact + fib;

        return (int) result;
    }

    public static void main(String[] args) {
        System.out.println(complex_math(5, 3, 2));
    }
}