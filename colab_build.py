# Cashlytics APK Builder - Google Colab
# Upload this notebook to Google Colab to build your APK online

# Cell 1: Setup environment
!apt-get update
!apt-get install -y openjdk-8-jdk git zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

import os
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64'

!pip install cython==0.29.36 buildozer==1.5.0

# Cell 2: Clone your repository
!git clone https://github.com/Bharath-git-code/cashlytics-transaction-tracker.git
%cd cashlytics-transaction-tracker

# Cell 3: Accept Android licenses
!mkdir -p /root/.android/licenses
!echo "8933bad161af4178b1185d1a37fbf41ea5269c55" > /root/.android/licenses/android-sdk-license
!echo "d56f5187479451eabf01fb78af6dfcb131a6481e" >> /root/.android/licenses/android-sdk-license
!echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" >> /root/.android/licenses/android-sdk-license

# Cell 4: Use stable config and build
!cp buildozer-stable.spec buildozer.spec
!buildozer android debug

# Cell 5: Download APK
from google.colab import files
import os

# Find APK file
for root, dirs, filenames in os.walk('.'):
    for filename in filenames:
        if filename.endswith('.apk'):
            apk_path = os.path.join(root, filename)
            print(f"Found APK: {apk_path}")
            files.download(apk_path)
            break