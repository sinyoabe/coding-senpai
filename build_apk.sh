#!/bin/bash
HTML_INPUT_PATH="$1"
OUTPUT_APK_PATH="$2"

BUILD_DIR="/tmp/cordova_builder"
rm -rf "$BUILD_DIR"

cordova create "$BUILD_DIR" com.sinyoabe.codingsenpai CodingSenpaiApp
cd "$BUILD_DIR"
cordova platform add android
cp "$HTML_INPUT_PATH" "$BUILD_DIR/www/index.html"
cordova build android --no-telemetry

APK_GEN=$(find "$BUILD_DIR/platforms/android/app/build/outputs/apk/debug" -name "*.apk" | head -n 1)

if [ -f "$APK_GEN" ]; then
    cp "$APK_GEN" "$OUTPUT_APK_PATH"
    echo "SUCCESS"
else
    echo "FAILED"
fi
