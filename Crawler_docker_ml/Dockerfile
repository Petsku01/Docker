FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY ml_web_crawler.py .

# Create output directory
RUN mkdir -p /app/output && \
    chmod 755 /app/output

# Run as non-root
RUN useradd -m -u 1000 crawler && \
    chown -R crawler:crawler /app

USER crawler

CMD ["python", "-u", "ml_web_crawler.py"]
