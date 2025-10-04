# APK Build Instructions

## Method 1: GitHub Actions (Recommended for Windows)

1. Push your code to GitHub repository
2. Go to Actions tab and run "Build APK" workflow
3. Download APK from artifacts

## Method 2: Docker (Local Build)

```bash
# Install Docker Desktop first
docker build -t cashlytics-builder .
docker run --rm -v "${PWD}:/app" cashlytics-builder
```

## Method 3: WSL2 (Most Control)

```bash
# In WSL2 Ubuntu terminal
sudo apt update
sudo apt install -y python3-pip build-essential git python3 python3-dev
pip3 install buildozer cython
buildozer android debug
```

## Method 4: Buildozer on Linux

```bash
buildozer android debug
```

## Output

Your APK will be created in:

- `bin/` directory (local builds)
- GitHub Actions artifacts (GitHub builds)

## Troubleshooting

### Android SDK License Issues

If you get license acceptance errors:

1. **GitHub Actions**: The workflow now automatically accepts licenses
2. **Docker**: Use the updated Dockerfile which handles SDK setup
3. **WSL2**: Run `./wsl_setup.sh` which accepts licenses automatically
4. **Manual License Accept**:
   ```bash
   yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses
   ```

### Build Tools Not Found

If you get "build-tools folder not found" or "Aidl not found":

1. Ensure Android SDK is properly installed
2. Check that `buildozer.spec` has correct versions:
   - `android.api = 33`
   - `android.build_tools = 33.0.2`
   - `android.ndk = 25b`
3. Verify environment variables:
   ```bash
   export ANDROID_HOME=/path/to/android-sdk
   export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools
   ```

### Common Fixes

- Clean buildozer cache: `buildozer android clean`
- Update buildozer: `pip install --upgrade buildozer`
- Ensure all dependencies are in requirements.txt
- Check buildozer.spec for correct package name and version
- For Windows users, Docker or GitHub Actions are recommended
- Linux users can use buildozer directly after running `./wsl_setup.sh`

## APK Location

After successful build, find your APK at:
`bin/cashlytics-0.1-arm64-v8a-debug.apk`
