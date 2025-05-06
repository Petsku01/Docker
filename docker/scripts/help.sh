#!/bin/bash
# loacation: scripts/help.sh
# remember to make it executable chmod +x scripts/help.sh

echo "Super Ubuntu Docker Container Usage:"
echo "-----------------------------------"
echo "Environment Variables:"
echo "  ENABLE_SSH=true         Start SSH server (port 22)"
echo "  ENABLE_CODE_SERVER=true Start code-server (port 8080)"
echo "Volumes:"
echo "  /home/user/data         Persistent data storage"
echo "  /home/user/.ssh         SSH keys"
echo "Commands:"
echo "  help                    Show this message"
echo "  /home/user/scripts/*.sh Run custom scripts"
echo "Examples:"
echo "  docker run -it -v \$(pwd)/data:/home/user/data super-ubuntu"
echo "  docker run -d -p 2222:22 -e ENABLE_SSH=true super-ubuntu"
echo "  docker run -d -p 8080:8080 -e ENABLE_CODE_SERVER=true super-ubuntu"
