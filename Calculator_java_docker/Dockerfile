# Stage 1: Build Stage (use Alpine for lighter builder)
FROM maven:3.9.9-eclipse-temurin-17-alpine AS builder

# Set working directory
WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .

# Download dependencies (cached if pom unchanged)
RUN mvn dependency:go-offline -B

# Copy source and build the layered JAR
COPY src ./src
RUN mvn clean package -DskipTests

# Extract layers from the JAR
RUN mkdir -p target/extracted && \
    java -Djarmode=layertools -jar target/*.jar extract --destination target/extracted

# Stage 2: Runtime Stage (lightweight Alpine JRE)
FROM eclipse-temurin:17-jre-alpine

# Create non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser:appgroup

# Set working directory
WORKDIR /app

# Copy extracted layers (dependencies first for caching)
COPY --from=builder --chown=appuser:appgroup /app/target/extracted/dependencies/ ./
COPY --from=builder --chown=appuser:appgroup /app/target/extracted/spring-boot-loader/ ./
COPY --from=builder --chown=appuser:appgroup /app/target/extracted/snapshot-dependencies/ ./
COPY --from=builder --chown=appuser:appgroup /app/target/extracted/application/ ./

# Run with explicit launcher (faster than fat JAR)
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]

# Health check to monitor application
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

EXPOSE 8080
