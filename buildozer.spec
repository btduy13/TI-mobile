[app]

# (str) Title of your application
title = Tape Inventory

# (str) Package name
package.name = tapeinventory

# (str) Package domain (needed for android/ios packaging)
package.domain = org.tapeinventory

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,db,json

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,src/*

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_patterns = buildozer.spec,*.pyc,*.pyo,.git/*,bin/*,venv/*

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy==2.2.1,kivymd==1.1.1,sqlalchemy==2.0.23,pillow==10.1.0,python-dateutil==2.8.2,requests==2.31.0,plyer==2.1.0,sqlite3worker==1.1.7,psycopg2-binary==2.9.9

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations
# Valid options are: landscape, portrait, portrait-reverse or landscape-reverse
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
android.skip_update = False

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (list) Android application meta-data to set (key=value format)
android.meta_data = android.max_aspect=2.1

# (list) Android library project to add (will be added in the
# project.properties automatically.)
android.library_references =

# (list) Android shared libraries which will be added to AndroidManifest.xml using <uses-library> tag
android.uses_library =

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Android additional libraries to copy into libs/armeabi
android.copy_libs = 1

# (str) Android app theme, default is ok for Kivy-based app
android.apptheme = @android:style/Theme.NoTitleBar

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# In past, was `android.arch` as three arch linked into one binary
# If you want to build for multiple archs, use android.archs
android.archs = arm64-v8a

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
bin_dir = ./bin 