package com.example.calculator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

// Marks this class as the entry point for a Spring Boot application
// Enables auto-configuration, component scanning, and Spring Boot features
@SpringBootApplication
public class CalculatorApplication {
    // Main method serving as the entry point for the Java application
    public static void main(String[] args) {
        // Launches the Spring Boot application using the current class as the configuration source
        SpringApplication.run(CalculatorApplication.class, args);
    }
}
