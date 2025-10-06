[app]

# (str) Title of your application
title = Cashlytics

# (str) Package name
package.name = cashlytics

# (str) Package domain (e.g., org.example)
package.domain = com.cashlytics

# (str) Source directory of your application (usually the current directory)
source.dir = .

# (list) File extensions to include in the package
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) Directories to exclude from the package
source.exclude_dirs = tests,bin,buildozer,.venv,.git,__pycache__

# (str) Application version (manual or captured from a file)
version = 1.0

# (list) Python modules or extensions required by your application
# These can be recipes from python-for-android or pure-Python packages.
requirements = python3,kivy,kivymd,sqlite3,pillow

# (str) Path to your application's presplash image (optional)
# presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Path to your application's icon (optional)
icon.filename = %(source.dir)s/assets/icons/logo.png

# (str) Orientation of the application (portrait, landscape, sensor landscape, all)
orientation = portrait

# (bool) Fullscreen mode (True/False)
fullscreen = False

# (int) Target Android API level
android.api = 33

# (int) Minimum Android API level supported by your APK
android.minapi = 21

# (str) Android NDK directory (leave empty to auto-download)
# android.ndk_dir =

# (str) Android SDK directory (leave empty to auto-download)
# android.sdk_dir =

# (str) Kivy version to use (e.g., 'master' for latest development version)
# You can also specify a specific version number like '2.2.1'
# android.kivy_version = 2.3.0

# (str) Python-for-android branch to use (e.g., 'develop' for latest)
# android.p4a_branch = master

# (list) Permissions required by your application (e.g., INTERNET, CAMERA)
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (bool) Enable/disable debug mode for the APK
android.debug = True

# (list) Java classes to add as activities to the manifest
# android.add_activities =

# (str) Background color of the presplash screen (e.g., '#FFFFFF' for white)
android.presplash_color = #2196F3

# (bool) Enable/disable logcat filtering during build
log_level = 2

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin