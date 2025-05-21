# Complex Number Calculator

This is a Spring Boot application that provides a command-line interface (CLI) for performing complex number calculations, including addition, subtraction, multiplication, division, and modulus. The application is containerized using Docker for easy deployment and runs on Java 17 with Maven as the build tool.

## Features
- **Operations**: Supports addition, subtraction, multiplication, division, and modulus of complex numbers.
- **Input Validation**: Handles invalid inputs (e.g., empty strings, incorrect formats, NaN/Infinity) with user-friendly error messages.
- **Retry Limit**: Limits retries to 5 for invalid inputs to prevent infinite loops.
- **Operation Confirmation**: Prompts for confirmation before executing operations to reduce errors.
- **Logging**: Logs operations and errors to the console for debugging.
- **Dockerized**: Runs in a Docker container with a multi-stage build for easy setup.

## Project Structure
```
complex-calculator/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/calculator/
│   │   │       ├── CalculatorApplication.java
│   │   │       ├── ComplexNumber.java
│   │   │       ├── ComplexCalculatorService.java
│   │   │       └── CalculatorCommandLineRunner.java
│   │   └── resources/
│   │       └── application.properties
│   └── test/
├── Dockerfile
├── pom.xml
└── README.md
```

- **CalculatorApplication.java**: Main Spring Boot application entry point.
- **ComplexNumber.java**: Represents a complex number with real and imaginary parts.
- **ComplexCalculatorService.java**: Implements complex number operations with validation.
- **CalculatorCommandLineRunner.java**: Provides the CLI for user interaction.
- **application.properties**: Configures logging and Spring Boot settings.
- **Dockerfile**: Defines the multi-stage build for creating the Docker image.
- **pom.xml**: Maven configuration for dependencies and build settings.

## Prerequisites
- **Docker**: Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) and ensure it is running.
- No local Java or Maven installation is required, as the Dockerfile handles the build.

## Setup Instructions (Windows)
1. **Create the Project Directory**:
   - Create a folder named `complex-calculator` (e.g., `C:\Projects\complex-calculator`).
     ```cmd
     mkdir C:\Projects\complex-calculator
     cd C:\Projects\complex-calculator
     ```

2. **Create the Directory Structure**:
   - Create the following directories:
     ```cmd
     mkdir src\main\java\com\example\calculator
     mkdir src\main\resources
     mkdir src\test
     ```
   - Alternatively, use File Explorer to create:
     - `src\main\java\com\example\calculator`
     - `src\main\resources`
     - `src\test`

3. **Create the Files**:
   - Copy the content of each file from the provided artifacts into the respective locations using a text editor (e.g., Notepad, VS Code):
     - `src\main\java\com\example\calculator\CalculatorApplication.java`
     - `src\main\java\com\example\calculator\ComplexNumber.java`
     - `src\main\java\com\example\calculator\ComplexCalculatorService.java`
     - `src\main\java\com\example\calculator\CalculatorCommandLineRunner.java`
     - `src\main\resources\application.properties`
     - `Dockerfile` (in the root `complex-calculator` folder)
     - `pom.xml` (in the root `complex-calculator` folder)
   - Ensure files are saved with UTF-8 encoding and the correct extensions (`.java`, `.xml`, `.properties`, no extension for `Dockerfile`).

## Build and Run
1. **Build the Docker Image**:
   - Open a command prompt or PowerShell in the `complex-calculator` directory:
     ```cmd
     cd C:\Projects\complex-calculator
     docker build -t complex-calculator:latest .
     ```
   - This uses a multi-stage Dockerfile to build the application with Maven and package it into a lightweight OpenJDK 17 image.

2. **Run the Docker Container**:
   - Start the container in interactive mode:
     ```cmd
     docker run -it --name calculator-container complex-calculator:latest
     ```
   - The `-it` flag enables the CLI for input/output.

3. **Using the Calculator**:
   - The CLI prompts for:
     - First complex number (format: `real imaginary`, e.g., `3 4` for `3 + 4i`).
     - Operation (`add`, `subtract`, `multiply`, `divide`, `modulus`).
     - Second complex number (if not `modulus`).
     - Confirmation (`y` to proceed, `n` to cancel).
   - Enter `exit` to stop.
   - Example interaction:
     ```
     Complex Number Calculator (format: a + bi or a - bi)
     Operations: add, subtract, multiply, divide, modulus
     Enter 'exit' to quit

     Enter first complex number (real imaginary): 3 4
     Enter operation (add, subtract, multiply, divide, modulus): add
     Enter second complex number (real imaginary): 1 2
     Confirm operation: add (3.00 + 4.00i, 1.00 + 2.00i)? (y/n): y
     Result: 4.00 + 6.00i

     Enter first complex number (real imaginary): 5 0
     Enter operation (add, subtract, multiply, divide, modulus): modulus
     Modulus: 5.00

     Enter first complex number (real imaginary): exit
     Calculator stopped.
     ```

4. **View Logs** (if needed):
   - If running in detached mode (`-d` instead of `-it`), view logs:
     ```cmd
     docker logs calculator-container
     ```

5. **Stop and Remove the Container**:
   - Stop:
     ```cmd
     docker stop calculator-container
     ```
   - Remove:
     ```cmd
     docker rm calculator-container
     ```

## Configuration
- **Logging**: Logs are written to the console (visible via `docker logs`). To enable detailed logs, edit `application.properties`:
  ```
  logging.level.com.example.calculator=DEBUG
  ```
- **Retry Limit**: The application limits retries to 5 for invalid inputs. Modify `MAX_RETRIES` in `CalculatorCommandLineRunner.java` to change this.

## Extending the Application
- **Add Operations**: Extend `ComplexCalculatorService.java` to include operations like conjugate or polar form conversion.
- **Unit Tests**: Add tests in `src/test/java/com/example/calculator/` using JUnit (included via `spring-boot-starter-test`).
- **REST API**: Add `spring-boot-starter-web` to `pom.xml` and create a controller to expose operations via HTTP.
- **Docker Enhancements**: Add a `HEALTHCHECK` instruction in the `Dockerfile` or use Docker Compose for multi-container setups.

## Troubleshooting
- **Docker Build Fails**: Ensure Docker Desktop is running and you have an internet connection for downloading Maven dependencies.
- **Invalid Input Errors**: The application handles empty inputs, invalid formats, and NaN/Infinity values. Check error messages for guidance.
- **Logs**: Use `docker logs calculator-container` or set `logging.level.com.example.calculator=DEBUG` for detailed output.

## License
This project is unlicensed and provided as-is for educational purposes.