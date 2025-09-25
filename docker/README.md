# Ubuntu Docker Container

A feature-rich Ubuntu 22.04 development container with pre-installed tools and services.

## Features

- Ubuntu 22.04 LTS base
- Zsh shell with oh-my-zsh
- Development tools: git, python3, nodejs, npm, awscli
- Code-server (VS Code in browser)
- SSH server
- Non-root user with sudo access
- Persistent data volumes

## Quick Start

### Build the image:
```bash
chmod +x build.sh
./build.sh
```

### Run interactively:
```bash
docker run -it -v $(pwd)/data:/home/user/data super-ubuntu
```

### Run with docker-compose:
```bash
docker-compose up -d
```

### Access services:
- SSH: `ssh -p 2222 user@localhost`
- Code-server: http://localhost:8080
- Web services: http://localhost:8000

## Directory Structure

```
docker/
├── Dockerfile           # Main container definition
├── entrypoint.sh       # Container startup script
├── docker-compose.yml  # Compose configuration
├── build.sh           # Build helper script
├── config/            # Configuration files
│   ├── motd          # Welcome message
│   ├── sshd_config   # SSH configuration
│   └── zshrc         # Zsh configuration
├── scripts/          # Initialization scripts
│   ├── help.sh       # Help information
│   └── example.sh    # Example startup script
├── data/             # Persistent data (mounted)
└── ssh_keys/         # SSH keys (mounted)
```

## Environment Variables

- `ENABLE_SSH=true` - Enable SSH server
- `ENABLE_CODE_SERVER=true` - Enable code-server

## Volumes

- `/home/user/data` - Persistent data storage
- `/home/user/.ssh` - SSH configuration and keys

## Notes

- Default user is `user` with sudo access (no password required)
- SSH requires key-based authentication (no password login)
- Code-server runs without authentication by default (secure it for production)
