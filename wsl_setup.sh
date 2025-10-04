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

# Install Android SDK and accept licenses
echo "📱 Setting up Android SDK..."
mkdir -p ~/.android
echo "y" | sudo apt install -y android-sdk

# Download and install Android SDK command line tools
echo "⬇️ Installing Android SDK command line tools..."
cd /tmp
wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
unzip commandlinetools-linux-9477386_latest.zip
sudo mkdir -p /opt/android-sdk/cmdline-tools
sudo mv cmdline-tools /opt/android-sdk/cmdline-tools/latest
sudo chown -R $USER:$USER /opt/android-sdk

# Set Android environment variables
echo "🔧 Setting Android environment variables..."
export ANDROID_HOME=/opt/android-sdk
export ANDROID_SDK_ROOT=/opt/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools
echo 'export ANDROID_HOME=/opt/android-sdk' >> ~/.bashrc
echo 'export ANDROID_SDK_ROOT=/opt/android-sdk' >> ~/.bashrc
echo 'export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools' >> ~/.bashrc

# Accept Android SDK licenses
echo "📜 Accepting Android SDK licenses..."
yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses

# Install required SDK components
echo "📦 Installing Android SDK components..."
$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.2" "ndk;25.2.9519653"

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