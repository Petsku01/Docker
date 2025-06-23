# Use a slim Python 3.9 base image
FROM python:3.9-slim

# Create non-root user
RUN useradd -m appuser

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the crawler script
COPY ml_web_crawler_fixed.py .

# Create output directory and set permissions
RUN mkdir -p /app/output && chown appuser:appuser /app/output

# Switch to non-root user
USER appuser

# Set environment variable for output
ENV OUTPUT_FILE=/app/output/crawled_urls.csv

# Run the crawler
CMD ["python", "ml_web_crawler_fixed.py"]