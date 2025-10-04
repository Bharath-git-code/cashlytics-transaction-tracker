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

- Ensure all dependencies are in requirements.txt
- Check buildozer.spec for correct package name and version
- For Windows users, Docker or GitHub Actions are recommended
- Linux users can use buildozer directly

## APK Location

After successful build, find your APK at:
`bin/cashlytics-0.1-arm64-v8a-debug.apk`
