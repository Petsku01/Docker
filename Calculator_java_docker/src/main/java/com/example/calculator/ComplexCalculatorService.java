package com.example.calculator;

import org.springframework.stereotype.Service;

@Service
public class ComplexCalculatorService {

    private void checkNotNull(ComplexNumber num, String paramName) {
        if (num == null) {
            throw new IllegalArgumentException(paramName + " cannot be null");
        }
    }

    private void checkResult(double real, double imaginary) {
        if (Double.isNaN(real) || Double.isInfinite(real) || Double.isNaN(imaginary) || Double.isInfinite(imaginary)) {
            throw new ArithmeticException("Result is NaN or infinite");
        }
    }

    public ComplexNumber add(ComplexNumber a, ComplexNumber b) {
        checkNotNull(a, "First number");
        checkNotNull(b, "Second number");
        double real = a.getReal() + b.getReal();
        double imaginary = a.getImaginary() + b.getImaginary();
        checkResult(real, imaginary);
        return new ComplexNumber(real, imaginary);
    }

    public ComplexNumber subtract(ComplexNumber a, ComplexNumber b) {
        checkNotNull(a, "First number");
        checkNotNull(b, "Second number");
        double real = a.getReal() - b.getReal();
        double imaginary = a.getImaginary() - b.getImaginary();
        checkResult(real, imaginary);
        return new ComplexNumber(real, imaginary);
    }

    public ComplexNumber multiply(ComplexNumber a, ComplexNumber b) {
        checkNotNull(a, "First number");
        checkNotNull(b, "Second number");
        double real = a.getReal() * b.getReal() - a.getImaginary() * b.getImaginary();
        double imaginary = a.getReal() * b.getImaginary() + a.getImaginary() * b.getReal();
        checkResult(real, imaginary);
        return new ComplexNumber(real, imaginary);
    }

    public ComplexNumber divide(ComplexNumber a, ComplexNumber b) {
        checkNotNull(a, "First number");
        checkNotNull(b, "Second number");
        double denominator = b.getReal() * b.getReal() + b.getImaginary() * b.getImaginary();
        if (denominator == 0) {
            throw new ArithmeticException("Division by zero");
        }
        double real = (a.getReal() * b.getReal() + a.getImaginary() * b.getImaginary()) / denominator;
        double imaginary = (a.getImaginary() * b.getReal() - a.getReal() * b.getImaginary()) / denominator;
        checkResult(real, imaginary);
        return new ComplexNumber(real, imaginary);
    }

    public double modulus(ComplexNumber a) {
        checkNotNull(a, "Number");
        double result = Math.sqrt(a.getReal() * a.getReal() + a.getImaginary() * a.getImaginary());
        if (Double.isNaN(result) || Double.isInfinite(result)) {
            throw new ArithmeticException("Modulus is NaN or infinite");
        }
        return result;
    }
}