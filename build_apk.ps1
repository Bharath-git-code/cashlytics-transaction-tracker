# Cashlytics APK Builder - Windows PowerShell Script
# Run this script in PowerShell to build your APK using Docker

Write-Host "🚀 Building Cashlytics APK using Docker..." -ForegroundColor Green

# Check if Docker is running
try {
    docker version | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Build Docker image
Write-Host "🔨 Building Docker image..." -ForegroundColor Yellow
docker build -t cashlytics-builder .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed" -ForegroundColor Red
    exit 1
}

# Create bin directory if it doesn't exist
if (!(Test-Path "bin")) {
    New-Item -ItemType Directory -Path "bin"
}

# Run Docker container to build APK
Write-Host "📱 Building APK..." -ForegroundColor Yellow
docker run --rm -v "${PWD}:/app" cashlytics-builder

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ APK build completed successfully!" -ForegroundColor Green
    Write-Host "📦 Your APK is available in the bin/ directory" -ForegroundColor Cyan
    
    # List generated APK files
    if (Test-Path "bin/*.apk") {
        Write-Host "📋 Generated APK files:" -ForegroundColor Yellow
        Get-ChildItem "bin/*.apk" | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor White }
    }
} else {
    Write-Host "❌ APK build failed. Check the logs above for details." -ForegroundColor Red
    Write-Host "💡 Try running: docker run --rm -it -v `"${PWD}:/app`" cashlytics-builder bash" -ForegroundColor Yellow
    Write-Host "   Then run: buildozer android debug" -ForegroundColor Yellow
}

Write-Host "`n🔍 For troubleshooting, see BUILD_APK.md" -ForegroundColor Cyan