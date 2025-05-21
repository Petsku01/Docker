package com.example.calculator;

public class ComplexNumber {
    private final double real;
    private final double imaginary;

    public ComplexNumber(double real, double imaginary) {
        if (Double.isNaN(real) || Double.isInfinite(real) || Double.isNaN(imaginary) || Double.isInfinite(imaginary)) {
            throw new IllegalArgumentException("Real or imaginary part cannot be NaN or infinite");
        }
        this.real = real;
        this.imaginary = imaginary;
    }

    public double getReal() {
        return real;
    }

    public double getImaginary() {
        return imaginary;
    }

    @Override
    public String toString() {
        if (imaginary == 0) {
            return String.format("%.2f", real);
        }
        if (imaginary > 0) {
            return String.format("%.2f + %.2fi", real, imaginary);
        }
        return String.format("%.2f - %.2fi", real, -imaginary);
    }
}