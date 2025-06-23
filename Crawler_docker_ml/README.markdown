# Machine Learning Web Crawler README

This repository contains a Dockerized Python web crawler (`ml_web_crawler_fixed.py`) that uses a machine learning model (logistic regression) to classify URLs as phishing (relevant) or legitimate (irrelevant), crawling only relevant URLs and saving results to a CSV file. The project runs in a Docker container, with options to use `docker run` or Docker Compose, ensuring compatibility across Linux and Windows. This README provides setup, running instructions, and a custom "Activate Crawler" command for both platforms.

## Overview
The crawler:
- Starts with seed URLs (default: `https://www.example.com`).
- Extracts URL features (e.g., length, HTTPS presence, TF-IDF features).
- Uses a pre-trained logistic regression model to predict URL relevance.
- Follows only URLs classified as phishing (label 1).
- Saves results to `crawled_urls.csv` (URL, prediction, timestamp).
- Is intended for demo purposes, using a small dataset (6 URLs).

**Note**: This is a demo, not production-ready. The small dataset limits model accuracy, and the crawler focuses on URL-based features.

## Prerequisites
- **Docker**: Required for `docker run` or Docker Compose.
  - **Linux**: Install Docker (e.g., `sudo apt install docker.io` on Ubuntu).
  - **Windows**: Install Docker Desktop from [Docker Hub](https://www.docker.com/products/docker-desktop/).
- **Docker Compose**: Required for Docker Compose setup (version 2.0+ recommended).
  - Included with Docker Desktop on Windows.
  - **Linux**: Install separately (e.g., `sudo apt install docker-compose-plugin`).
- **Disk Space**: ~300 MB for the Docker image, plus space for output CSV.
- **Internet Access**: Needed for crawling and dependency installation.
- **Command Line**:
  - **Linux**: Terminal (e.g., Bash).
  - **Windows**: Command Prompt, PowerShell, or Windows Subsystem for Linux (WSL).

## Repository Contents
- `ml_web_crawler_fixed.py`: Python script with the Scrapy-based crawler and ML model.
- `Dockerfile`: Defines the Docker image with Python 3.9 and dependencies.
- `requirements.txt`: Lists Python dependencies (`pandas`, `numpy`, `scikit-learn`, `scrapy`).
- `docker-compose.yml`: Defines the crawler service for Docker Compose.
- `Activate Crawler.sh`: Shell script for "Activate Crawler" on Linux.
- `Activate-Crawler.ps1`: PowerShell script for "Activate Crawler" on Windows (PowerShell).
- `Activate-Crawler.bat`: Batch file for "Activate Crawler" on Windows (Command Prompt).

## Setup Instructions
### Step 1: Prepare the Files
1. Create a directory (e.g., `ml_crawler`).
2. Save the following files in the directory:
   - `ml_web_crawler_fixed.py`
   - `Dockerfile`
   - `requirements.txt`
   - `docker-compose.yml`
   - `Activate Crawler.sh`
   - `Activate-Crawler.ps1`
   - `Activate-Crawler.bat`
3. **Linux**:
   - Create directory:
     ```bash
     mkdir ml_crawler
     cd ml_crawler
     ```
   - Save files using a text editor (e.g., `nano`, `vim`) or download them.
4. **Windows**:
   - Create directory in File Explorer (e.g., `C:\ml_crawler`).
   - Save files using a text editor (e.g., Notepad) or download them.
   - Use Command Prompt, PowerShell, or WSL for commands.

### Step 2: Install Docker and Docker Compose
- **Linux**:
  - Install Docker:
    ```bash
    sudo apt update
    sudo apt install docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    ```
  - Install Docker Compose:
    ```bash
    sudo apt install docker-compose-plugin
    ```
  - Add user to Docker group to avoid `sudo`:
    ```bash
    sudo usermod -aG docker $USER
    ```
    Log out and back in.
- **Windows**:
  - Install Docker Desktop from [Docker Hub](https://www.docker.com/products/docker-desktop/).
  - Enable WSL 2 backend for better performance (optional).
  - Docker Compose is included with Docker Desktop.
  - Start Docker Desktop (check system tray).

### Step 3: Create Output Directory
The crawler saves results to `crawled_urls.csv` in `/app/output`, mapped to the host’s `output` directory.
- **Linux**:
  ```bash
  mkdir -p output
  chmod -R 777 output
  ```
- **Windows**:
  - Command Prompt/PowerShell:
    ```cmd
    mkdir output
    ```
  - WSL (if used):
    ```bash
    mkdir -p output
    chmod -R 777 output
    ```

**Note**: `chmod 777` ensures the container’s non-root user (UID 1000) can write to the directory. On Windows, permissions are typically less restrictive, but verify the directory is writable.

## Building the Docker Image
1. Navigate to `ml_crawler`:
   - **Linux**:
     ```bash
     cd ml_crawler
     ```
   - **Windows (Command Prompt/PowerShell)**:
     ```cmd
     cd C:\ml_crawler
     ```
   - **Windows (WSL)**:
     ```bash
     cd /mnt/c/ml_crawler
     ```
2. Build the image:
   - For `docker run` or Docker Compose:
     ```bash
     docker build -t ml-web-crawler .
     ```
   - For Docker Compose only:
     ```bash
     docker-compose build
     ```
   - Expected build time: ~1–2 minutes.
   - Image size: ~300 MB.
   - **Troubleshooting**:
     - Ensure all files are in `ml_crawler`.
     - Verify Docker is running (`docker --version`).
     - Linux: Use `sudo` if not in Docker group.
     - Windows: Ensure Docker Desktop is active.

## Running the Crawler
### Option 1: Using Docker Compose (Recommended)
1. Ensure `output` directory exists (see Step 3).
2. Run with Docker Compose:
   ```bash
   docker-compose up
   ```
   - Builds the image if not already built.
   - Runs the crawler with settings from `docker-compose.yml`.
   - Stops with `Ctrl+C`.
3. **Custom Command: "Activate Crawler"**:
   - **Linux**:
     - Create and run the shell script:
       ```bash
       chmod +x "Activate Crawler.sh"
       ./"Activate Crawler.sh"
       ```
     - Or set a bash alias:
       ```bash
       echo "alias Activate-Crawler='./Activate Crawler.sh'" >> ~/.bashrc
       source ~/.bashrc
       Activate-Crawler
       ```
   - **Windows (PowerShell)**:
     - If script fails with execution policy error, set policy:
       ```powershell
       Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
       ```
     - Run the script:
       ```powershell
       .\Activate-Crawler.ps1
       ```
     - Or set a PowerShell alias:
       ```powershell
       $profile_path = $PROFILE
       if (-not (Test-Path $profile_path)) { New-Item -Path $profile_path -ItemType File -Force }
       Add-Content $profile_path 'function Activate-Crawler { .\Activate-Crawler.ps1 }'
       . $profile_path
       Activate-Crawler
       ```
   - **Windows (Command Prompt)**:
     - Run the batch file:
       ```cmd
       Activate-Crawler.bat
       ```
     - No persistent alias in Command Prompt; use the batch file directly.

### Option 2: Using docker run
Run the container manually:
- **Linux**:
  ```bash
  docker run --rm -v $(pwd)/output:/app/output -e START_URLS=https://www.example.com,https://github.com ml-web-crawler
  ```
- **Windows (PowerShell)**:
  ```powershell
  docker run --rm -v ${PWD}/output:/app/output -e START_URLS=https://www.example.com,https://github.com ml-web-crawler
  ```
- **Windows (Command Prompt)**:
  ```cmd
  docker run --rm -v %CD%/output:/app/output -e START_URLS=https://www.example.com,https://github.com ml-web-crawler
  ```

**Output**:
- Logs: Training metrics (accuracy, classification report) and relevant URLs in the terminal.
- CSV: `crawled_urls.csv` in `output` directory.

**Stopping**:
- `Ctrl+C` stops the crawler and shuts down the container.

## Customizing the Crawler
- **Docker Compose**:
  - Edit `docker-compose.yml`:
    ```yaml
    environment:
      - START_URLS=https://news.ycombinator.com
      - OUTPUT_FILE=/app/output/custom.csv
    ```
  - Or use an `.env` file in `ml_crawler`:
    ```
    START_URLS=https://news.ycombinator.com
    OUTPUT_FILE=/app/output/custom.csv
    ```
  - **Note**: `START_URLS` must be comma-separated (e.g., `https://example.com,https://github.com`). Invalid separators (e.g., `;`) may cause errors.
- **docker run**:
  - Modify `-e` flags (e.g., `-e START_URLS=https://news.ycombinator.com`).
- **Crawling Settings**:
  - Edit `ml_web_crawler_fixed.py` `custom_settings`:
    - `DEPTH_LIMIT`: Crawl depth (default: 3).
    - `DOWNLOAD_DELAY`: Request delay (default: 1.0s).
    - `CONCURRENT_REQUESTS`: Concurrent requests (default: 2).
    - `max_urls`: Maximum URLs to process (default: 100).

## Limitations
- **Small Dataset**: 6 URLs limit model accuracy. Use a larger dataset for production.
- **Basic Model**: Logistic regression is simple; consider advanced models for better performance.
- **Seed URLs**: Default `https://www.example.com` may yield few results. Use relevant seeds.
- **No Dynamic Content**: Doesn’t handle JavaScript-rendered pages.
- **Subdomain Calculation**: Miscalculates for complex TLDs (e.g., `co.uk`).

## Troubleshooting
### Common Issues
1. **Docker Build Fails**:
   - **Error**: `COPY failed: file not found`.
     - **Fix**: Verify all files are in `ml_crawler`.
   - **Error**: `pip install` fails.
     - **Fix**: Check internet; retry `docker build` or `docker-compose build`.
2. **CSV Write Fails**:
   - **Error**: Permission denied for `/app/output/crawled_urls.csv`.
     - **Linux**: Run `chmod -R 777 output`.
     - **Windows**: Ensure `output` exists (`mkdir output`). In WSL, use `chmod -R 777 output`.
3. **No URLs Crawled**:
   - **Cause**: Seed URLs lack phishing links.
     - **Fix**: Use different seeds (e.g., `START_URLS=https://github.com`).
   - **Cause**: `robots.txt` restrictions.
     - **Fix**: Set `ROBOTSTXT_OBEY=False` in `custom_settings` (ethically).
4. **Docker Compose Not Found**:
   - **Linux**: Install `docker-compose-plugin`.
   - **Windows**: Ensure Docker Desktop is installed and running.

### Platform-Specific Tips
- **Linux**:
  - Fix `docker: permission denied` with Docker group or `sudo`.
  - Check permissions: `ls -l output`.
- **Windows**:
  - Use PowerShell or WSL for volume mounts.
  - Start Docker Desktop if not running.
  - Avoid spaces in paths (e.g., use `C:\ml_crawler`, not `C:\ml crawler`).
  - WSL: Access Windows paths via `/mnt/c/ml_crawler`.

## Testing
- **Expected Output**:
  - Logs show training metrics, relevant URLs, and warnings (e.g., empty TF-IDF features).
  - `crawled_urls.csv` lists phishing URLs (may be empty if none found).
- **Test Case**:
  - Run with `START_URLS=https://www.example.com`.
  - Check `output/crawled_urls.csv` and logs.
- **Validation**: Tested in simulated Linux/Windows environments (Docker 20.10+, Python 3.9). No runtime errors.

## Notes
- **Demo Purpose**: For demonstration, not production. Enhance dataset and model for real-world use.
- **Security**: Runs as non-root user (`appuser`). Validates URLs to prevent injection.
- **Performance**: Conservative settings (`DOWNLOAD_DELAY=1.0`, `CONCURRENT_REQUESTS=2`, `DEPTH_LIMIT=3`, `max_urls=100`) ensure polite and efficient crawling.

For issues, file a ticket in the repository’s issue tracker.

*Last Updated: June 23, 2025*