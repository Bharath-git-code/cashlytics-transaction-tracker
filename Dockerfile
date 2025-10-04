# Dockerfile for building Kivy APK
FROM kivy/buildozer:latest

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Build APK
CMD ["buildozer", "android", "debug"]