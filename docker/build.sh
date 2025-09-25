#!/bin/bash

echo "Building Super Ubuntu Docker Image..."
docker build -t super-ubuntu:latest .

echo ""
echo "Build complete! Run with:"
echo "  docker run -it super-ubuntu"
echo "  docker-compose up -d"
echo ""
echo "For help:"
echo "  docker run -it super-ubuntu help"
