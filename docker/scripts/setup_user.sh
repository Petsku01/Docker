#!/bin/bash
# location should be: scripts/setup_user.sh

# Create non-root käyttäjä
useradd -m -s /bin/zsh user
usermod -aG sudo user
echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/user
