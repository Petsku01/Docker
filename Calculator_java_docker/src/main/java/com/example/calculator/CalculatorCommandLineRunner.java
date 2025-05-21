package com.example.calculator;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.Scanner;

@Component
public class CalculatorCommandLineRunner implements CommandLineRunner {
    private static final Logger logger = LoggerFactory.getLogger(CalculatorCommandLineRunner.class);
    private final ComplexCalculatorService calculatorService;
    private static final int MAX_RETRIES = 5;

    @Autowired
    public CalculatorCommandLineRunner(ComplexCalculatorService calculatorService) {
        this.calculatorService = calculatorService;
    }

    @Override
    public void run(String... args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Complex Number Calculator (format: a + bi or a - bi)");
        System.out.println("Operations: add, subtract, multiply, divide, modulus");
        System.out.println("Enter 'exit' to quit");
        int retryCount = 0;

        while (true) {
            try {
                System.out.print("\nEnter first complex number (real imaginary): ");
                String input = readLine(scanner);
                if (input.equalsIgnoreCase("exit")) {
                    break;
                }
                ComplexNumber num1 = parseComplexNumber(input);

                System.out.print("Enter operation (add, subtract, multiply, divide, modulus): ");
                String operation = readLine(scanner).toLowerCase();

                if (operation.equals("modulus")) {
                    double result = calculatorService.modulus(num1);
                    System.out.printf("Modulus: %.2f%n", result);
                    logger.info("Modulus of {} = {}", num1, result);
                    retryCount = 0;
                    continue;
                }

                System.out.print("Enter second complex number (real imaginary): ");
                ComplexNumber num2 = parseComplexNumber(readLine(scanner));

                System.out.printf("Confirm operation: %s (%s, %s)? (y/n): ", operation, num1, num2);
                String confirmation = readLine(scanner).trim().toLowerCase();
                if (!confirmation.equals("y")) {
                    System.out.println("Operation cancelled.");
                    retryCount = 0;
                    continue;
                }

                ComplexNumber result;
                switch (operation) {
                    case "add":
                        result = calculatorService.add(num1, num2);
                        System.out.println("Result: " + result);
                        logger.info("Add: {} + {} = {}", num1, num2, result);
                        break;
                    case "subtract":
                        result = calculatorService.subtract(num1, num2);
                        System.out.println("Result: " + result);
                        logger.info("Subtract: {} - {} = {}", num1, num2, result);
                        break;
                    case "multiply":
                        result = calculatorService.multiply(num1, num2);
                        System.out.println("Result: " + result);
                        logger.info("Multiply: {} * {} = {}", num1, num2, result);
                        break;
                    case "divide":
                        result = calculatorService.divide(num1, num2);
                        System.out.println("Result: " + result);
                        logger.info("Divide: {} / {} = {}", num1, num2, result);
                        break;
                    default:
                        System.out.println("Invalid operation. Use: add, subtract, multiply, divide, modulus");
                        continue;
                }
                retryCount = 0;
            } catch (IOException e) {
                System.out.println("Error reading input: " + e.getMessage() + ". Please try again.");
                logger.error("I/O Error: {}", e.getMessage());
                if (++retryCount >= MAX_RETRIES) {
                    System.out.println("Too many failed attempts. Exiting.");
                    break;
                }
                continue;
            } catch (Exception e) {
                System.out.println("Error: " + e.getMessage() + ". Please try again.");
                logger.error("Error: {}", e.getMessage());
                if (++retryCount >= MAX_RETRIES) {
                    System.out.println("Too many failed attempts. Exiting.");
                    break;
                }
                continue;
            }
        }
        scanner.close();
        System.out.println("Calculator stopped.");
    }

    private String readLine(Scanner scanner) throws IOException {
        if (!scanner.hasNextLine()) {
            throw new IOException("Input stream closed");
        }
        return scanner.nextLine().trim();
    }

    private ComplexNumber parseComplexNumber(String input) {
        if (input.isEmpty()) {
            throw new IllegalArgumentException("Input cannot be empty");
        }
        String[] parts = input.split("\\s+");
        if (parts.length != 2) {
            throw new IllegalArgumentException("Invalid format. Use: real imaginary");
        }
        try {
            double real = Double.parseDouble(parts[0]);
            double imaginary = Double.parseDouble(parts[1]);
            return new ComplexNumber(real, imaginary);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("Invalid number format");
        }
    }
}