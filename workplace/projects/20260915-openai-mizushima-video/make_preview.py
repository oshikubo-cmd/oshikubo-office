# -*- coding: utf-8 -*-
"""依頼書のHTMLプレビューを生成する。

build_video_req.py の D（本文データ）をそのまま読み込むので、
docxとプレビューの内容は常に一致する。

Usage:
    python make_preview.py [output.html]
"""
import html
import io
import sys
import importlib.util
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("bvr", HERE / "build_video_req.py")
bvr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bvr)
D = bvr.D


def esc(t):
    return html.escape(t).replace("\n", "<br>")


def main(out):
    nq = sum(len(c["質問"]) for c in D["質問事項"])
    parts = []
    A = parts.append

    A(f'<p class="to">{esc(D["宛名"])}</p>')
    A('<h1>取材依頼書</h1>')
    A('<p class="from">株式会社翔泳社 AIdiver編集部 編集長<br>押久保 剛</p>')

    for label, key in [("●取材希望日時", "取材希望日時"),
                       ("●動画シリーズの概要", "動画シリーズ概要"),
                       ("●取材テーマ", "取材テーマ"),
                       ("●取材趣旨", "取材趣旨")]:
        A(f'<p class="sec">{label}</p>')
        A(f'<p class="body">{esc(D[key])}</p>')

    A(f'<p class="sec">●質問項目案（全{nq}問・3部構成）</p>')
    for c in D["質問事項"]:
        A(f'<p class="cat">{esc(c["見出し"])}</p>')
        for q in c["質問"]:
            A(f'<p class="q">・{esc(q)}</p>')
    A('<p class="body note">※当日の流れや時間配分により、質問の順序・表現を一部調整させていただく場合がございます。</p>')

    A('<p class="sec">● 掲載先・媒体概要</p>')
    A(f'<p class="body">{esc(D["媒体概要"])}</p>')
    A(f'<p class="body">{esc(bvr.br.FIXED_PRE_REVIEW)}</p>')
    A(f'<p class="body">{esc(bvr.br.FIXED_POST_REVIEW)}</p>')

    doc = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>取材依頼書プレビュー｜OpenAI 水嶋様</title>
<style>
  :root { color-scheme: light; }
  body { margin:0; background:#6b6b6b; font-family:"MS Mincho","ＭＳ 明朝","Hiragino Mincho ProN",serif; }
  .bar { position:sticky; top:0; background:#2b2b2b; color:#eee; padding:8px 16px;
         font-family:system-ui,sans-serif; font-size:12px; letter-spacing:.02em; }
  .bar b { color:#fff; }
  .page { max-width:210mm; margin:16px auto 48px; background:#fff; padding:25mm;
          box-shadow:0 2px 16px rgba(0,0,0,.4); font-size:10.5pt; line-height:1.75; color:#000; }
  .to { font-size:12pt; font-weight:bold; margin:0 0 14px; }
  h1 { text-align:center; font-size:14pt; margin:0 0 18px; font-weight:bold; }
  .from { text-align:right; margin:0 0 28px; }
  .sec { font-weight:bold; margin:22px 0 4px; }
  .body { margin:0 0 6px; }
  .cat { font-weight:bold; margin:16px 0 6px; }
  .q { margin:0 0 8px; padding-left:1em; text-indent:-1em; }
  .note { margin-top:14px; }
  @media print { body{background:#fff} .bar{display:none} .page{box-shadow:none;margin:0} }
</style></head><body>
<div class="bar">プレビュー（HTML）｜正本は <b>【取材依頼書】OpenAI水嶋様_AIdiver.docx</b> ／ build_video_req.py の D から生成</div>
<div class="page">
""" + "\n".join(parts) + """
</div></body></html>
"""
    io.open(out, "w", encoding="utf-8", newline="\n").write(doc)
    print("Wrote:", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(HERE / "preview.html"))
