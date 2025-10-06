# 📱 Build Cashlytics APK

This guide provides **3 different ways** to build your Cashlytics APK, from easiest to most advanced.

## 🏆 Method 1: Google Colab (RECOMMENDED - Easiest)

**Why this is best:** Free, no setup required, works in your browser

1. **Open Google Colab**: https://colab.research.google.com/
2. **Upload** the `Cashlytics_APK_Builder.ipynb` file (from this repository)
3. **Run all cells** in order (Runtime → Run all)
4. **Wait 10-15 minutes** for the build to complete
5. **Download** the APK from the Files panel

## 🚀 Method 2: GitHub Actions (Automated)

**Why this is good:** Automated, no manual work, builds on every push

1. **Push code** to GitHub (already set up!)
2. **Go to**: https://github.com/Bharath-git-code/cashlytics-transaction-tracker/actions
3. **Click** on the latest workflow run
4. **Download** the APK from "Artifacts" section

Available workflows:
- `build-apk-reliable.yml` - Most stable build
- `build-apk.yml` - Standard build
- `build-apk-docker.yml` - Docker-based build

## 🖥️ Method 3: Local Build (Advanced)

**Requirements:** WSL or Linux environment

### Using WSL (Windows):
```bash
# Copy project to WSL
wsl -d rancher-desktop mkdir -p /tmp/cashlytics
wsl -d rancher-desktop cp -r /mnt/c/path/to/project/* /tmp/cashlytics/

# Enter WSL and build
wsl -d rancher-desktop
cd /tmp/cashlytics
./build_cashlytics.sh setup  # First time only
./build_cashlytics.sh build
```

### Using Docker:
```bash
docker pull kivy/buildozer:latest
docker run --rm -v $(pwd):/app kivy/buildozer:latest buildozer android debug
```

## 📋 buildozer.spec Configuration

Your app is configured with:
- **App Name**: Cashlytics
- **Package**: com.cashlytics.cashlytics
- **Version**: 1.0
- **Target Android API**: 33
- **Minimum Android API**: 21
- **Requirements**: kivy, kivymd, sqlite3, pillow

## 🔧 Troubleshooting

### Build Fails?
1. Try **Google Colab** method (most reliable)
2. Check GitHub Actions logs for specific errors
3. Ensure all required files are present: `main.py`, `buildozer.spec`, `requirements.txt`

### APK Won't Install?
1. Enable "Install from unknown sources" in Android settings
2. Make sure you downloaded the `.apk` file (not `.aab`)
3. Check Android version compatibility (minimum Android 5.0)

## 📱 Installation

1. **Download** the APK file
2. **Transfer** to your Android device
3. **Enable** "Install from unknown sources"
4. **Tap** the APK file to install
5. **Enjoy** your personal finance tracker!

---

## 🎯 Quick Start (Recommended)

**Fastest way to get your APK:**

1. Open: https://colab.research.google.com/
2. Upload: `Cashlytics_APK_Builder.ipynb`
3. Run all cells
4. Download APK
5. Install on Android

**Total time:** ~15 minutes ⏱️