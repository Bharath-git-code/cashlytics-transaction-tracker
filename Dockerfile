# Dockerfile for building Kivy APK with proper Android SDK setup
FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    openjdk-8-jdk \
    git \
    zip \
    unzip \
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
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV ANDROID_HOME=/opt/android-sdk
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# Install Android SDK command line tools
RUN mkdir -p /opt/android-sdk/cmdline-tools && \
    cd /tmp && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip && \
    unzip -q commandlinetools-linux-9477386_latest.zip && \
    mv cmdline-tools /opt/android-sdk/cmdline-tools/latest && \
    rm commandlinetools-linux-9477386_latest.zip

# Accept licenses and install SDK components
RUN yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses && \
    $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.2" "ndk;25.2.9519653"

# Install Python dependencies
RUN pip3 install --upgrade pip && \
    pip3 install buildozer cython

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Build APK
CMD ["buildozer", "android", "debug"]