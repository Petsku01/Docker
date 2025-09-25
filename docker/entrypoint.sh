#!/bin/bash
set -e

# Set up environment
export HOME=/home/user
export SHELL=/bin/zsh

# Welcome message
[ -f /etc/motd ] && cat /etc/motd

# Ensure directories exist with correct permissions
mkdir -p /home/user/data /home/user/.ssh
chown -R user:user /home/user/data /home/user/.ssh
chmod 700 /home/user/.ssh

# Start SSH server if enabled
if [ "$ENABLE_SSH" = "true" ]; then
    echo "Starting SSH server..."
    /usr/sbin/sshd -D &
fi

# Start code-server if enabled
if [ "$ENABLE_CODE_SERVER" = "true" ]; then
    echo "Starting code-server on port 8080..."
    su - user -c "code-server --bind-addr 0.0.0.0:8080 --auth none /home/user/data" &
fi

# Run initialization scripts
if [ -d /home/user/scripts ]; then
    for script in /home/user/scripts/*.sh; do
        if [ -f "$script" ] && [ -x "$script" ]; then
            echo "Running $(basename $script)..."
            su - user -c "bash $script" || echo "Warning: $script failed"
        fi
    done
fi

# Display help if requested
if [ "$1" = "help" ]; then
    su - user -c "/home/user/scripts/help.sh"
    exit 0
fi

# Execute provided command or start shell
if [ $# -gt 0 ]; then
    exec su - user -c "$*"
else
    exec su - user
fi
