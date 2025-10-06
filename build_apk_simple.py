#!/usr/bin/env python3
"""
Simple APK Builder for Cashlytics
Builds APK using the clean buildozer.spec configuration
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
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"Command: {cmd}")
        print(f"Return code: {e.returncode}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python
    print(f"✅ Python version: {sys.version}")
    
    # Check if buildozer is installed
    try:
        result = subprocess.run("buildozer --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Buildozer is installed")
        else:
            print("❌ Buildozer not working properly. Installing...")
            if not run_command("pip install buildozer", "Installing buildozer"):
                return False
    except Exception:
        print("❌ Buildozer not found. Installing...")
        if not run_command("pip install buildozer", "Installing buildozer"):
            return False
    
    # Check if buildozer.spec exists
    if not os.path.exists("buildozer.spec"):
        print("❌ buildozer.spec not found")
        return False
    print("✅ buildozer.spec found")
    
    # Check main.py
    if not os.path.exists("main.py"):
        print("❌ main.py not found")
        return False
    print("✅ main.py found")
    
    return True

def clean_build():
    """Clean previous builds"""
    print("🧹 Cleaning previous builds...")
    
    if os.path.exists("bin"):
        run_command("rmdir /s /q bin" if platform.system() == "Windows" else "rm -rf bin", "Removing bin directory")
    
    if os.path.exists(".buildozer"):
        run_command("rmdir /s /q .buildozer" if platform.system() == "Windows" else "rm -rf .buildozer", "Removing .buildozer directory")

def build_apk():
    """Build the APK"""
    print("🔨 Building APK...")
    
    # Use buildozer to build debug APK
    if run_command("buildozer android debug", "Building APK with buildozer"):
        print("🎉 APK built successfully!")
        
        # Find and list APK files
        if os.path.exists("bin"):
            apk_files = [f for f in os.listdir("bin") if f.endswith(".apk")]
            if apk_files:
                print("📱 APK files created:")
                for apk in apk_files:
                    apk_path = os.path.join("bin", apk)
                    if os.path.exists(apk_path):
                        size_mb = os.path.getsize(apk_path) / (1024 * 1024)
                        print(f"   • {apk} ({size_mb:.1f} MB)")
                        print(f"   📁 Full path: {os.path.abspath(apk_path)}")
            else:
                print("⚠️ No APK files found in bin directory")
        else:
            print("⚠️ bin directory not created")
        return True
    else:
        print("❌ APK build failed")
        return False

def main():
    """Main build function"""
    print("🚀 Cashlytics APK Builder")
    print("=" * 50)
    
    # Check OS
    print(f"💻 Operating System: {platform.system()}")
    if platform.system() == "Windows":
        print("⚠️ Building on Windows. For best results, consider using WSL or Docker.")
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed")
        return False
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Build APK (keep existing cache)")
    print("2. Clean build (remove cache and build fresh)")
    print("3. Just install buildozer")
    
    try:
        choice = input("Enter choice (1-3): ").strip()
    except KeyboardInterrupt:
        print("\n❌ Build cancelled by user")
        return False
    
    if choice == "1":
        return build_apk()
    elif choice == "2":
        clean_build()
        return build_apk()
    elif choice == "3":
        return run_command("pip install buildozer cython", "Installing buildozer and cython")
    else:
        print("❌ Invalid choice")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Build completed successfully!")
            print("📱 Your APK is ready for installation on Android devices.")
        else:
            print("\n❌ Build failed. Check the error messages above.")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Build interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)