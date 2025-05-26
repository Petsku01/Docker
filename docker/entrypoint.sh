#!/bin/bash
# docker/entrypoint.sh

# Exit on error
set -e

# Set up environment
export HOME=/home/user
export SHELL=$(command -v zsh || command -v bash || echo /bin/sh)

# Welcome message
[ -f /etc/motd ] && cat /etc/motd

# Ensure directories exist
mkdir -p /home/user/data /home/user/.ssh || { echo "Failed to create directories"; exit 1; }
chown -R user:user /home/user/data /home/user/.ssh || { echo "Failed to set ownership"; exit 1; }
chmod 700 /home/user/.ssh || { echo "Failed to set permissions"; exit 1; }

# Verify user exists
id user >/dev/null 2>&1 || { echo "User 'user' not found"; exit 1; }

# Start SSH server if enabled
if [ -n "$ENABLE_SSH" ] && [ "$ENABLE_SSH" = "true" ]; then
    echo "Starting SSH server..."
    command -v sshd >/dev/null || { echo "SSHD not found"; exit 1; }
    /usr/sbin/sshd -D &
fi

# Start code-server if enabled
if [ -n "$ENABLE_CODE_SERVER" ] && [ "$ENABLE_CODE_SERVER" = "true" ]; then
    echo "Starting code-server on port 8080..."
    command -v code-server >/dev/null || { echo "code-server not found"; exit 1; }
    su - user -c "code-server --bind-addr 0.0.0.0:8080 --auth none /home/user/data &" || { echo "Failed to start code-server"; exit 1; }
fi

# Run initialization scripts
if [ -d /home/user/scripts ]; then
    for script in /home/user/scripts/*.sh; do
        if [ -f "$script" ] && [ -x "$script" ] && [ "$(basename "$script")" != "setup_user.sh" ] && [ "$(basename "$script")" != "install_code_server.sh" ]; then
            echo "Running $script..."
            su - user -c "bash $script" || echo "Warning: $script failed"
        fi
    done
fi

# Display help if requested
if [ "$1" = "help" ]; then
    [ -f /home/user/scripts/help.sh ] || { echo "Help script not found"; exit 1; }
    su - user -c "/home/user/scripts/help.sh"
    exit 0
fi

# Execute provided command or start shell
if [ $# -gt 0 ]; then
    exec su - user -c "$@"
else
    exec su - user -c "$SHELL"
fi
