@echo off
REM Build APK using Docker - Windows Batch Version

echo 🚀 Building Cashlytics APK using Docker...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker Desktop.
    exit /b 1
)

echo 📦 Building Docker image...
docker build -t cashlytics-builder .

echo 🔨 Building APK...
docker run --rm -v "%cd%:/app" cashlytics-builder

echo ✅ APK build complete!
echo 📱 Your APK should be in the bin/ directory