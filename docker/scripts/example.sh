#!/bin/bash
# location: scripts/example.sh
# remember to chmod +x scripts/example.sh

echo "Running example script as $(whoami)..."
echo "Node version: $(node --version)"
echo "Python version: $(python3 --version)"
echo "Saving output to /home/user/data/output.txt"
echo "Hello from $(date)" > /home/user/data/output.txt
