@echo off
echo Building APK using Docker...

REM Build Docker image
docker build -f Dockerfile.local -t cashlytics-builder .

REM Run container and build APK
docker run --rm -v %cd%\bin:/app/bin cashlytics-builder

echo APK should be in bin\ folder
pause