#!/bin/bash
set -e

if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose not found"
    echo "Install: sudo apt install docker-compose-plugin (Linux) or brew install docker-compose (Mac)"
    exit 1
fi

mkdir -p output
chmod 755 output
docker-compose up --build
```

## 2. activate-crawler.ps1 (Windows PowerShell)
```powershell
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Error "Docker Compose not found. Install Docker Desktop."
    exit 1
}

if (-not (Test-Path output)) {
    New-Item -ItemType Directory -Path output | Out-Null
}

docker-compose up --build
```
