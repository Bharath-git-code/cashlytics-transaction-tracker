#!/bin/bash
# Android SDK Troubleshooting Script for Cashlytics
# Run this script to diagnose and fix Android SDK issues

echo "🔍 Cashlytics Android SDK Troubleshooting Script"
echo "=================================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if we're in the right directory
if [ ! -f "buildozer.spec" ]; then
    echo "❌ buildozer.spec not found. Please run this script from your project directory."
    exit 1
fi

echo "✅ Found buildozer.spec"

# Check if buildozer is installed
if ! command_exists buildozer; then
    echo "❌ Buildozer not installed. Installing..."
    pip3 install buildozer cython
else
    echo "✅ Buildozer is installed"
    buildozer --version
fi

# Check Android SDK setup
echo ""
echo "🔍 Checking Android SDK setup..."

if [ -n "$ANDROID_HOME" ]; then
    echo "✅ ANDROID_HOME set to: $ANDROID_HOME"
    
    if [ -d "$ANDROID_HOME" ]; then
        echo "✅ Android SDK directory exists"
        
        # Check for build tools
        if [ -d "$ANDROID_HOME/build-tools" ]; then
            echo "✅ Build tools directory found"
            echo "📋 Available build tools versions:"
            ls -1 "$ANDROID_HOME/build-tools/" | head -5
        else
            echo "❌ Build tools directory not found"
        fi
        
        # Check for command line tools
        if [ -f "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" ]; then
            echo "✅ SDK Manager found"
            
            echo "📋 Installed SDK components:"
            $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --list_installed | head -10
            
            echo ""
            echo "🔧 Accepting Android SDK licenses..."
            yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses
            
        elif [ -f "$ANDROID_HOME/tools/bin/sdkmanager" ]; then
            echo "✅ SDK Manager found (legacy location)"
            
            echo "📋 Installed SDK components:"
            $ANDROID_HOME/tools/bin/sdkmanager --list_installed | head -10
            
            echo ""
            echo "🔧 Accepting Android SDK licenses..."
            yes | $ANDROID_HOME/tools/bin/sdkmanager --licenses
            
        else
            echo "❌ SDK Manager not found"
        fi
        
    else
        echo "❌ Android SDK directory does not exist: $ANDROID_HOME"
    fi
else
    echo "⚠️  ANDROID_HOME not set"
fi

# Check buildozer configuration
echo ""
echo "🔍 Checking buildozer configuration..."

# Extract Android API and build tools from buildozer.spec
api_level=$(grep "^android.api" buildozer.spec | cut -d'=' -f2 | tr -d ' ')
build_tools=$(grep "^android.build_tools" buildozer.spec | cut -d'=' -f2 | tr -d ' ')
ndk_version=$(grep "^android.ndk" buildozer.spec | cut -d'=' -f2 | tr -d ' ')

echo "📋 Buildozer configuration:"
echo "  Android API: $api_level"
echo "  Build Tools: $build_tools"
echo "  NDK Version: $ndk_version"

# Check if buildozer has created its own Android SDK
buildozer_sdk="$HOME/.buildozer/android/platform/android-sdk"
if [ -d "$buildozer_sdk" ]; then
    echo "✅ Buildozer Android SDK found at: $buildozer_sdk"
    
    if [ -d "$buildozer_sdk/build-tools" ]; then
        echo "✅ Buildozer build tools found"
        echo "📋 Available versions:"
        ls -1 "$buildozer_sdk/build-tools/" | head -5
    fi
    
    # Try to accept licenses for buildozer SDK
    if [ -f "$buildozer_sdk/cmdline-tools/latest/bin/sdkmanager" ]; then
        echo "🔧 Accepting licenses for buildozer SDK..."
        export ANDROID_HOME="$buildozer_sdk"
        yes | $buildozer_sdk/cmdline-tools/latest/bin/sdkmanager --licenses
    elif [ -f "$buildozer_sdk/tools/bin/sdkmanager" ]; then
        echo "🔧 Accepting licenses for buildozer SDK (legacy)..."
        export ANDROID_HOME="$buildozer_sdk"
        yes | $buildozer_sdk/tools/bin/sdkmanager --licenses
    fi
else
    echo "⚠️  Buildozer Android SDK not found"
fi

# Offer to clean and rebuild
echo ""
echo "🧹 Cleanup Options:"
echo "1. Clean buildozer cache (recommended if build fails)"
echo "2. Clean and rebuild everything"
echo "3. Continue with current setup"
echo ""
read -p "Choose option (1-3): " choice

case $choice in
    1)
        echo "🧹 Cleaning buildozer cache..."
        buildozer android clean
        ;;
    2)
        echo "🧹 Cleaning everything..."
        rm -rf .buildozer
        buildozer android clean
        ;;
    3)
        echo "✅ Continuing with current setup"
        ;;
    *)
        echo "✅ No cleanup performed"
        ;;
esac

# Test build
echo ""
echo "🚀 Ready to build APK!"
echo ""
echo "💡 Recommended next steps:"
echo "1. Run: buildozer android debug"
echo "2. If build fails with license errors, run this script again"
echo "3. Check build logs in .buildozer/android/platform/build-*/logs/"
echo ""
echo "🐳 Alternative: Use Docker build with:"
echo "   docker build -t cashlytics-builder ."
echo "   docker run --rm -v \"\$(pwd):/app\" cashlytics-builder"