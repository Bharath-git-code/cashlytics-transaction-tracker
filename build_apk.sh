#!/bin/bash

# Build APK using Docker
echo "Building APK using Docker..."

# Build Docker image
docker build -t cashlytics-builder .

# Run container to build APK
docker run --rm -v "$(pwd)":/app cashlytics-builder

echo "APK build complete! Check the bin/ directory for the APK file."