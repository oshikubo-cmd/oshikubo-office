#!/usr/bin/env bash
# HTMLレポートを PNG（全体＋分割）と PDF に書き出す。
# 使い方: bash data/scripts/render_html_report.sh <input.html> <出力ベース名>
set -euo pipefail
SRC_FILE="$1"; BASE="${2:-report}"
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
OUT="$(cd "$(dirname "$SRC_FILE")" && pwd)"
URL="file:///$(cygpath -m "$SRC_FILE" 2>/dev/null || echo "$SRC_FILE")"

# 高さ20000pxの仮想ウィンドウで撮り、あとで余白をトリムする
"$CHROME" --headless --disable-gpu --hide-scrollbars --force-color-profile=srgb \
  --force-device-scale-factor=2 --window-size=1280,20000 --virtual-time-budget=15000 \
  --user-data-dir="$OUT/chrome-profile" --screenshot="$OUT/_raw.png" "$URL" >/dev/null 2>&1

"$CHROME" --headless --disable-gpu --virtual-time-budget=15000 \
  --user-data-dir="$OUT/chrome-profile" --no-pdf-header-footer \
  --print-to-pdf="$OUT/${BASE}.pdf" "$URL" >/dev/null 2>&1

python - "$OUT" "$BASE" <<'PY'
import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
out, base = sys.argv[1], sys.argv[2]
im = Image.open(f"{out}/_raw.png").convert("RGB")
W, H = im.size
bg = im.getpixel((5, H - 5))
def has(y):
    ext = im.crop((0, y, W, y + 1)).getextrema()
    return any(abs(a - c) > 6 or abs(b - c) > 6 for (a, b), c in zip(ext, bg))
last, step = 0, 200
for y in range(0, H, step):
    if has(y): last = y
for y in range(last, min(H, last + step + 5)):
    if has(y): last = y
bottom = min(H, last + 96)
im.crop((0, 0, W, bottom)).save(f"{out}/{base}_全体.png", optimize=True)
y = n = 0
while y < bottom - 200:
    h = min(3500, bottom - y); n += 1
    im.crop((0, y, W, y + h)).save(f"{out}/{base}_p{n}.png", optimize=True)
    y += h
print(f"PNG 全体 {W}x{bottom} / 分割 {n}枚 / PDF 出力完了")
PY
rm -f "$OUT/_raw.png"; rm -rf "$OUT/chrome-profile"
