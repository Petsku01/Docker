#!/bin/bash

set -e

export HOME=/home/user
export SHELL=/bin/zsh

# MOTD
[ -f /etc/motd ] && cat /etc/motd

# Setup dirs
mkdir -p /home/user/data /home/user/.ssh
chown -R user:user /home/user/data /home/user/.ssh
chmod 700 /home/user/.ssh
chmod 750 /home/user/data

# Start SSH if enabled
if [ "$ENABLE_SSH" = "true" ]; then
  /usr/sbin/sshd -D &
fi

# Start code-server if enabled
if [ "$ENABLE_CODE_SERVER" = "true" ]; then
  su - user -c "code-server --bind-addr 0.0.0.0:8080 --auth password --user-data-dir /home/user/data &"  
fi

# Run scripts
if [ -d /home/user/scripts ]; then
  for script in /home/user/scripts/*.sh; do
    [ -x "$script" ] && su - user -c "$script" || echo "Warning: $script failed"
  done
fi

# Help handling
if [ "$1" = "help" ]; then
  su - user -c "/home/user/scripts/help.sh"
  exit 0
fi

# Exec command or shell
if [ $# -gt 0 ]; then
  exec su - user -c "$*"
else
  exec su - user
