# Stage 1: Build Stage
# Use Maven 3.8.6 with OpenJDK 17 as the base image for building the Java application
FROM maven:3.8.6-openjdk-17 AS builder

# Set the working directory inside the container to /app for all subsequent commands
WORKDIR /app

# Copy the Maven configuration file (pom.xml) from the local project to the /app directory
COPY pom.xml .

# Copy the source code directory (src) from the local project to /app/src in the container
COPY src ./src

# Run Maven to clean previous build artifacts, compile the code, and package it into a JAR file
# The -DskipTests flag skips unit tests to speed up the build process
RUN mvn clean package -DskipTests

# Stage 2: Runtme Stage
# Use OpenJDK 17 JRE slim image as the base image for running the application
# The slim version includes only the Java Runtime Environment (JRE) to minimize image size
FROM openjdk:17-jre-slim

# Set the working directory inside the runtime container to /app
WORKDIR /app

# Copy the JAR file generated in the build stage from /app/target/ to /app/app.jar
# The --from=builder flag references the builder stage defined above
COPY --from=builder /app/target/complex-calculator-0.0.1-SNAPSHOT.jar app.jar

# Define the command to run the JAR file when the container starts
# The exec form ["java", "-jar", "app.jar"] runs the command directly for better performance
ENTRYPOINT ["java", "-jar", "app.jar"]
