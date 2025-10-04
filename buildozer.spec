[app]

# (str) Title of your application
title = Cashlytics

# (str) Package name
package.name = cashlytics

# (str) Package domain (needed for android/ios packaging)
package.domain = org.personal.cashlytics

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt,db

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,screens/*

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.0,kivymd==1.2.0,sqlite3,pillow

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

#
# Android specific
#

# (bool) Indicate if you would like to use the bitmap font
android.add_gradle_repositories = google()

# (str) Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 33

# (str) Android build tools version
android.build_tools = 33.0.2

# (str) Android SDK directory (if not using default)
# android.sdk_path = /home/runner/android-sdk

# (str) Android NDK directory (if not using default)  
# android.ndk_path = /home/runner/android-sdk/ndk/23.2.8568313

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
android.activity_class_name = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Python Service
android.service_class_name = org.kivy.android.PythonService

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) Icon of the application
icon.filename = assets/icons/logo.png

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Adaptive icon of the application (used if Android API level is 26+ at runtime)
# icon.adaptive_foreground.filename = %(source.dir)s/data/icon_fg.png
# icon.adaptive_background.filename = %(source.dir)s/data/icon_bg.png

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin