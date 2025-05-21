# Docker Container Test

This project creates a Docker container based on Ubuntu 20.04 that runs a Bash script to perform various tasks, including system info logging, API calls, file creation, Python script execution, and Git operations.

## Directory Structure

- `Dockerfile`: Defines the container setup, including Ubuntu image and tool installations.
- `script.sh`: Main Bash script that orchestrates tasks like logging, the API calls, file operations, Python execution, and Git initialization.
- `process.py`: Python script that processes API data and creates a siple JSON file.
- `requirements.txt`: Lists Python dependencies (empty for now).
- `README.md`: This file, providing  overview and instructions.

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your system.

## Setup

1. Clone or create the project directory:
   ```bash
   mkdir my-container
   cd my-container
   ```
2. Create the files (`Dockerfile`, `script.sh`, `process.py`, `requirements.txt`, `README.md`) with the provided contents.
3. Ensure `script.sh` is executable:
   ```bash
   chmod +x script.sh
   ```

## Building the Container

Build the Docker image:
```bash
docker build -t my-container .
```

## Running the Container

Run the container to execute the tasks:
```bash
docker run my-container
```

This will:
- Display system information (kernel, CPU).
- Fetch and parse data from a public API.
- Create and display a sample text file.
- Run a Python script to process data and create a JSON file.
- Initialize a Git repository and commit a `.gitignore` file.
- Log all operations with timestamps (e.g., "2025-05-21 08:35:05 EEST") to files in `logs/`.

## Inspecting the Container

To explore the container's filesystem:
```bash
docker run -it my-container /bin/bash
```
Navigate to `/app` to see generated files and directories (`logs/`, `data/`, `.git/`, `.gitignore`).

## Output

The container creates:
- `logs/`: Contains `system.log`, `api.log`, `file_ops.log`, `python.log`, `git.log`.
- `data/`: Contains `sample.txt` and `output.json`.
- `.git/` and `.gitignore`: From Git initialization.

## Notes

- The container uses Ubuntu 20.04 and installs `curl`, `jq`, `nano`, `git`, `python3`, and `pip3`.
- Logs include timestamps for tracking execution time.
- The image is optimized by cleaning up apt lists.

For issues or enhancements, please review the script outputs in the `logs/` directory.