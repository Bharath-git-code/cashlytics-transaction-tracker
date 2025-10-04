# Alternative build script using python-for-android directly
# This is more advanced but gives you more control

# Install p4a
# pip install python-for-android

# Build APK directly
# p4a apk --name=Cashlytics --package=org.personal.cashlytics --version=0.1 \
#     --requirements=python3,kivy==2.3.0,kivymd==1.2.0,sqlite3,pillow \
#     --permission INTERNET --permission WRITE_EXTERNAL_STORAGE \
#     --icon=assets/icons/logo.png \
#     --orientation=portrait \
#     --arch=arm64-v8a --arch=armeabi-v7a \
#     --release \
#     main.py
