#!/bin/bash

cat << EOF
========================================
Super Ubuntu Docker Container Usage
========================================

ENVIRONMENT VARIABLES:
  ENABLE_SSH=true         Start SSH server (port 22)
  ENABLE_CODE_SERVER=true Start code-server (port 8080)

VOLUMES:
  /home/user/data         Persistent data storage
  /home/user/.ssh         SSH keys

PORTS:
  22    SSH server
  8080  Code-server (VS Code)
  80    Available for web services

EXAMPLES:
  # Basic interactive shell
  docker run -it -v \$(pwd)/data:/home/user/data super-ubuntu

  # With SSH enabled
  docker run -d -p 2222:22 -e ENABLE_SSH=true -v \$(pwd)/data:/home/user/data super-ubuntu

  # With code-server enabled
  docker run -d -p 8080:8080 -e ENABLE_CODE_SERVER=true -v \$(pwd)/data:/home/user/data super-ubuntu

  # Full setup with both services
  docker run -d \\
    -p 2222:22 \\
    -p 8080:8080 \\
    -e ENABLE_SSH=true \\
    -e ENABLE_CODE_SERVER=true \\
    -v \$(pwd)/data:/home/user/data \\
    -v \$(pwd)/ssh_keys:/home/user/.ssh \\
    --name dev-container \\
    super-ubuntu

EOF
