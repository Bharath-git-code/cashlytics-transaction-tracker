# Cashlytics APK Builder for Google Colab
# Copy each section below into separate Colab cells

# ============= CELL 1: Setup Environment =============
print("🔄 Setting up build environment...")

# Install system dependencies
!apt-get update -qq
!apt-get install -y -qq openjdk-8-jdk git zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Set Java 8 as default
import os
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64'
os.environ['PATH'] = f"/usr/lib/jvm/java-8-openjdk-amd64/bin:{os.environ['PATH']}"

# Install Python build tools
!pip install -q cython==0.29.36 buildozer==1.5.0 colorama

print("✅ Build environment ready!")

# ============= CELL 2: Download Project =============
print("📥 Downloading your project...")

# Clone the repository
!git clone https://github.com/Bharath-git-code/cashlytics-transaction-tracker.git
%cd cashlytics-transaction-tracker

print("✅ Project downloaded!")

# ============= CELL 3: Configure Android =============
print("🔧 Configuring Android SDK...")

# Create Android licenses directory and accept licenses
!mkdir -p /root/.android/licenses
!echo "8933bad161af4178b1185d1a37fbf41ea5269c55" > /root/.android/licenses/android-sdk-license
!echo "d56f5187479451eabf01fb78af6dfcb131a6481e" >> /root/.android/licenses/android-sdk-license
!echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" >> /root/.android/licenses/android-sdk-license
!echo "d975f751698a77b662f1254ddbeed3901e976f5a" > /root/.android/licenses/google-gdk-license

print("✅ Android licenses configured!")

# ============= CELL 4: Prepare Build =============
print("📋 Preparing build configuration...")

# Use stable config and clean previous builds
!cp buildozer-stable.spec buildozer.spec
!rm -rf .buildozer bin

print("✅ Configuration ready!")

# ============= CELL 5: Build APK =============
print("🚀 Building your APK...")
print("⏰ This takes 10-15 minutes - please wait!")

# Set environment and build
import os
os.environ['BUILDOZER_LOG_LEVEL'] = '1'
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64'

!buildozer android debug

print("🎉 Build completed!")

# ============= CELL 6: Download APK =============
print("🔍 Finding your APK...")

import os
from google.colab import files

# Find and download APK
for root, dirs, filenames in os.walk('.'):
    for filename in filenames:
        if filename.endswith('.apk'):
            apk_path = os.path.join(root, filename)
            print(f"📱 Found: {filename}")
            
            # Copy to simple name and download
            !cp "{apk_path}" "cashlytics-app.apk"
            files.download("cashlytics-app.apk")
            print("✅ APK downloaded!")
            break