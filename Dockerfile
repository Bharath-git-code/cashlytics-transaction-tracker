# Dockerfile for building Kivy APK
FROM kivy/buildozer:latest

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ANDROID_HOME=/opt/android
ENV ANDROID_SDK_ROOT=/opt/android
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

# Install additional Python packages if needed
RUN pip install kivymd

# Accept Android SDK licenses
RUN yes | $ANDROID_HOME/tools/bin/sdkmanager --licenses

# Build the APK
CMD ["buildozer", "android", "debug"]