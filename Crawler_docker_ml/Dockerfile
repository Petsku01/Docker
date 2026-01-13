# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Cache deps
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: Runtime (distroless for security - 2026 trend)
FROM gcr.io/distroless/python3-debian12

WORKDIR /app

COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Non-root (built-in in distroless)
USER nonroot

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "ml_web_crawler_fixed.py"]
