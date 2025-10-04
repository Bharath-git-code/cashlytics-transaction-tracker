#!/bin/bash
# Cashlytics APK Builder - WSL Setup Script
# Run this script in WSL Ubuntu to set up your build environment

echo "🚀 Setting up Cashlytics APK Build Environment in WSL..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install essential build tools
echo "🔧 Installing build tools..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    zip \
    unzip \
    openjdk-8-jdk \
    wget \
    curl \
    build-essential \
    ccache \
    zlib1g-dev \
    libncurses5:i386 \
    libstdc++6:i386 \
    zlib1g:i386 \
    ant \
    autoconf \
    libtool \
    pkg-config \
    libffi-dev \
    libssl-dev

# Set JAVA_HOME
echo "☕ Setting up Java environment..."
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64' >> ~/.bashrc

# Install Python packages
echo "🐍 Installing Python build tools..."
pip3 install --upgrade pip
pip3 install buildozer cython

# Create project directory
echo "📁 Setting up project directory..."
mkdir -p ~/cashlytics
cd ~/cashlytics

echo "✅ WSL setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Copy your Cashlytics project files to ~/cashlytics/"
echo "2. Run: cd ~/cashlytics && buildozer android debug"
echo ""
echo "💡 To copy files from Windows:"
echo "   cp -r /mnt/c/Users/z004nrhb/OneDrive\\ -\\ Siemens\\ AG/D_drive_files/Sourcecode/personal_project/* ~/cashlytics/"