#!/usr/bin/env python3
"""
Simple APK Builder for Cashlytics
This script attempts to build the APK using buildozer with proper error handling
"""

import subprocess
import sys
import os
import platform

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"Command: {cmd}")
        print(f"Error: {e}")
        print(f"Output: {e.output}")
        return False

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python
    print(f"Python version: {sys.version}")
    
    # Check if buildozer is installed
    try:
        import buildozer
        print("✅ Buildozer is installed")
    except ImportError:
        print("❌ Buildozer not found. Installing...")
        if not run_command("pip install buildozer", "Installing buildozer"):
            return False
    
    # Check if buildozer.spec exists
    if not os.path.exists("buildozer.spec"):
        print("❌ buildozer.spec not found")
        return False
    print("✅ buildozer.spec found")
    
    return True

def main():
    """Main build function"""
    print("🚀 Cashlytics APK Builder")
    print("=" * 50)
    
    # Check OS
    if platform.system() == "Windows":
        print("⚠️  Building on Windows. Consider using WSL, Docker, or GitHub Actions for better compatibility.")
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed")
        return False
    
    # Clean previous builds
    if os.path.exists("bin"):
        print("🧹 Cleaning previous builds...")
        run_command("rm -rf bin", "Cleaning bin directory")
    
    if os.path.exists(".buildozer"):
        print("🧹 Cleaning buildozer cache...")
        run_command("rm -rf .buildozer", "Cleaning buildozer cache")
    
    # Build APK
    print("🔨 Building APK...")
    if run_command("buildozer android debug", "Building APK"):
        print("🎉 APK built successfully!")
        
        # Find and list APK files
        if os.path.exists("bin"):
            apk_files = [f for f in os.listdir("bin") if f.endswith(".apk")]
            if apk_files:
                print("📱 APK files created:")
                for apk in apk_files:
                    apk_path = os.path.join("bin", apk)
                    size_mb = os.path.getsize(apk_path) / (1024 * 1024)
                    print(f"   • {apk} ({size_mb:.1f} MB)")
            else:
                print("⚠️  No APK files found in bin directory")
        return True
    else:
        print("❌ APK build failed")
        print("\n💡 Troubleshooting suggestions:")
        print("1. Try using WSL: wsl -d rancher-desktop")
        print("2. Use Docker: docker run -v $(pwd):/app kivy/buildozer")
        print("3. Use GitHub Actions (recommended)")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)