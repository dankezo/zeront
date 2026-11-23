#!/bin/sh
# Package the Zeront extension into dist/zeront-extension-v<version>.zip
# The zip root IS the extension root (manifest.json at top level).
set -e
cd "$(dirname "$0")"
VER=$(python3 -c "import json; print(json.load(open('manifest.json'))['version'])")
mkdir -p ../dist
OUT="../dist/zeront-extension-v${VER}.zip"
rm -f "$OUT"
zip -qr "$OUT" manifest.json src icons -x '*.DS_Store*'
echo "built $OUT"
unzip -l "$OUT" | head -20
