# GitHub Actions Workflows for APK Building

This project includes several GitHub Actions workflows for building the Cashlytics APK. Here's which one to use:

## 🚀 Recommended Workflow

### **"Build APK"** (`build-apk-recommended.yml`)

- ✅ **Use this one** - Most reliable
- 🏗️ **Native Ubuntu setup** (no Docker)
- 🔧 **Automatic license handling**
- 📱 **Builds APK successfully**
- 🎯 **Triggers automatically** on push to main/develop

## 📋 Other Workflows

### **"Build APK (Basic)"** (`build-apk-basic.yml`)

- 🔄 **Backup option** if main workflow fails
- 🏗️ Native Ubuntu with simpler setup
- 🛠️ Manual trigger only

### **"Debug Build Environment"** (`debug-build.yml`)

- 🔍 **Troubleshooting only**
- ✅ Tests environment setup
- 🛠️ Manual trigger only

### **"Build APK (Simple Docker)"** - DISABLED

- ❌ **Disabled** due to Docker compatibility issues
- 🐳 Had Java classpath problems with Android SDK

### **"Build APK (Docker Alternative)"** - DISABLED

- ❌ **Disabled** due to Docker compatibility issues
- 🐳 Had SDK licensing problems

## 🎯 How to Use

1. **Automatic builds**: Push code to `main` or `develop` branch
2. **Manual builds**: Go to Actions → "Build APK" → "Run workflow"
3. **Download APK**: Check the "cashlytics-apk" artifact after build completes

## 🛠️ Local Development

For local builds, use:

```bash
# Windows PowerShell
.\build_apk.ps1

# WSL2/Linux
./debug_android_sdk.sh  # For troubleshooting
buildozer android debug
```

The main "Build APK" workflow is the most reliable and handles all the Android SDK licensing automatically! 🚀
