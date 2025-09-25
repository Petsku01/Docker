# ML Web Crawler

A Dockerized web crawler that uses machine learning to identify and follow suspicious URLs.

## Features
- Machine learning-based URL classification using Logistic Regression
- TF-IDF and statistical feature extraction
- Scrapy-based web crawling with politeness settings
- Docker containerization for easy deployment
- CSV output of suspicious URLs with confidence scores

## Prerequisites
- Docker and Docker Compose
- 500MB disk space
- Internet connection

## Quick Start

### Linux/Mac
```bash
chmod +x activate-crawler.sh
./activate-crawler.sh
```

### Windows PowerShell
```powershell
.\activate-crawler.ps1
```

### Windows Command Prompt
```batch
activate-crawler.bat
```

## Configuration

Edit `docker-compose.yml` to customize:
- `START_URLS`: Comma-separated seed URLs
- `MAX_URLS`: Maximum URLs to crawl (default: 50)
- `OUTPUT_FILE`: Output CSV path

## Output
Results are saved to `output/crawled_urls.csv` with:
- URL
- Classification (Suspicious/Safe)
- Confidence score
- Timestamp

## Architecture
- **Python 3.11** with Scrapy framework
- **scikit-learn** for ML classification
- **Docker** for containerization
- Non-root container execution for security

## Limitations
- Demo dataset (10 URLs) - extend for production
- Basic feature set - can be enhanced
- No JavaScript rendering support

## Development

Build image:
```bash
docker build -t ml-web-crawler .
```

Run without Docker Compose:
```bash
docker run -v $(pwd)/output:/app/output \
  -e START_URLS="https://example.com" \
  ml-web-crawler
