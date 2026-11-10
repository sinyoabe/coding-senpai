#!/bin/bash
HTML_FILE="$1"
OUTPUT_APK="$2"

WORK_DIR="/tmp/native_apk_project"

# Bersihkan folder temp
rm -rf "$WORK_DIR"

# Inisialisasi Project Android Ringkas
npx --yes cordova create "$WORK_DIR" com.sinyoabe.codingsenpai "CodingSenpai"
cd "$WORK_DIR"

# Copy HTML pengguna ke dalam folder aplikasi
cp "$HTML_FILE" "$WORK_DIR/www/index.html"

# Tambahkan Platform Android & Build (Offline Support)
npx --yes cordova platform add android --save
npx --yes cordova build android --no-telemetry

# Cari hasil APK yang terbentuk
GENERATED_APK=$(find "$WORK_DIR/platforms/android/app/build/outputs/apk" -name "*.apk" | head -n 1)

if [ -f "$GENERATED_APK" ]; then
    cp "$GENERATED_APK" "$OUTPUT_APK"
    echo "BUILD_SUCCESS"
else
    echo "BUILD_FAILED"
fi
