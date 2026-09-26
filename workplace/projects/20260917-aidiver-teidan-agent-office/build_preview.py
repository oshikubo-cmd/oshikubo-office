# -*- coding: utf-8 -*-
"""原稿_ver1.md から読みやすいプレビューHTMLを生成する。

使い方: python build_preview.py
原稿を直したら実行し直せば preview.html が更新される。
"""
import os
import re
import html

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "原稿_ver1.md")
OUT = os.path.join(HERE, "preview.html")

CSS = """
:root{ --fs:19px; }
*{box-sizing:border-box;}
body{
  margin:0; padding:0 0 80px;
  background:#eceff1;
  font-family:"Yu Gothic","YuGothic","Hiragino Kaku Gothic ProN","Meiryo",sans-serif;
  color:#1b1f23;
}
.nav{
  position:sticky; top:0; z-index:10;
  background:#23272b; color:#fff;
  padding:10px 20px; display:flex; gap:18px; align-items:center; flex-wrap:wrap;
  font-size:14px;
}
.nav a{color:#cfd8dc; text-decoration:none;}
.nav a:hover{color:#fff;}
.nav .sp{flex:1;}
.nav button{
  background:#3a4148; color:#fff; border:1px solid #555; border-radius:4px;
  padding:4px 11px; font-size:14px; cursor:pointer; font-family:inherit;
}
.nav button:hover{background:#4a5158;}
.doc{
  background:#fff; max-width:860px; margin:26px auto; padding:60px 70px;
  box-shadow:0 2px 10px rgba(0,0,0,.18);
  font-size:var(--fs); line-height:2.0;
}
h1{font-size:1.55em; line-height:1.55; margin:0 0 .5em; letter-spacing:.01em;}
.sub{font-size:.82em; color:#546e7a; margin:0 0 2em; line-height:1.7;}
h2{
  font-size:1.2em; line-height:1.6; margin:2.4em 0 .9em;
  padding-left:.6em; border-left:5px solid #1565c0;
}
h3{font-size:1.0em; margin:2em 0 .6em; color:#37474f;}
p{margin:0 0 1.25em;}
.lead{
  background:#f4f7f9; border:1px solid #dde4e8; border-radius:6px;
  padding:1.2em 1.4em; margin:0 0 2em; font-size:.97em;
}
.quote{
  margin:0 0 1.35em; padding:.7em 0 .7em 1.1em;
  border-left:4px solid #b0bec5; background:#fafcfd;
}
.fig{
  margin:1.6em 0; padding:.85em 1.1em;
  border:1px dashed #90a4ae; border-radius:6px;
  background:#f7f9fa; color:#455a64; font-size:.78em; line-height:1.85;
}
.fig img{display:block; width:100%; height:auto; margin:.7em 0 .5em; border-radius:3px;}
.pagebreak{
  margin:3em 0 2.4em; padding:.7em 0; text-align:center;
  border-top:2px solid #cfd8dc; border-bottom:2px solid #cfd8dc;
  color:#607d8b; font-size:.78em; letter-spacing:.3em;
}
table{border-collapse:collapse; width:100%; margin:1.2em 0 1.6em; font-size:.8em; line-height:1.7;}
th,td{border:1px solid #cfd8dc; padding:.5em .7em; text-align:left; vertical-align:top;}
th{background:#eceff1;}
ul,ol{margin:0 0 1.25em; padding-left:1.5em;}
li{margin:.3em 0;}
code{background:#eceff1; padding:.12em .4em; border-radius:3px; font-size:.85em;}
hr{border:0; border-top:1px solid #dde4e8; margin:2.5em 0;}
.memo{background:#fbfbfa; border:1px solid #e0e0e0; border-radius:6px;
      padding:1.6em 1.8em; margin-top:3em; font-size:.84em; line-height:1.85; color:#37474f;}
.memo h2{font-size:1.1em; border-left-color:#90a4ae; margin-top:1.4em;}
.memo h3{font-size:.98em;}
@media(max-width:900px){ .doc{padding:34px 22px; margin:12px;} }
"""

JS = """
(function(){
  var root = document.documentElement;
  var KEY = 'teidan-preview-fs';
  function get(){
    try{ return parseInt(localStorage.getItem(KEY), 10) || 19; }catch(e){ return 19; }
  }
  function set(px){
    px = Math.max(14, Math.min(30, px));
    root.style.setProperty('--fs', px + 'px');
    document.getElementById('fsval').textContent = px + 'px';
    try{ localStorage.setItem(KEY, px); }catch(e){}
  }
  window.addEventListener('DOMContentLoaded', function(){
    set(get());
    document.getElementById('fsdown').onclick = function(){ set(get() - 1); };
    document.getElementById('fsup').onclick   = function(){ set(get() + 1); };
  });
})();
"""


def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


def figure_block(text):
    """［写真: ...］ / ［図版...］ を枠で表示し、実ファイルがあれば埋め込む。

    単体で開いても崩れないよう、画像は data URI で埋め込む。
    """
    body = inline(text)
    m = re.search(r"`images/([^`]+)`", text)
    img = ""
    if m:
        path = os.path.join(HERE, "images", m.group(1))
        if os.path.exists(path):
            import base64
            with open(path, "rb") as fh:
                b64 = base64.b64encode(fh.read()).decode("ascii")
            ext = os.path.splitext(path)[1].lower()
            mime = "image/png" if ext == ".png" else "image/jpeg"
            img = '<img src="data:%s;base64,%s" alt="">' % (mime, b64)
    return '<div class="fig">%s%s</div>' % (body, img)


def main():
    with open(SRC, encoding="utf-8") as f:
        lines = f.read().split("\n")

    out = []
    title = ""
    subtitle = ""
    in_memo = False
    in_table = False
    table_rows = []
    i = 0
    n = len(lines)

    def flush_table():
        nonlocal in_table, table_rows
        if not in_table:
            return
        out.append("<table>")
        for r, row in enumerate(table_rows):
            if re.match(r"^\s*\|?[\s:|-]+\|?\s*$", row):
                continue
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            tag = "th" if r == 0 else "td"
            out.append("<tr>" + "".join("<%s>%s</%s>" % (tag, inline(c), tag) for c in cells) + "</tr>")
        out.append("</table>")
        in_table = False
        table_rows = []

    while i < n:
        raw = lines[i]
        s = raw.strip()
        i += 1

        if s.startswith("|"):
            in_table = True
            table_rows.append(s)
            continue
        flush_table()

        if not s:
            continue
        if s == "---":
            continue

        if s.startswith("# ") and not title:
            title = s[2:].strip()
            continue
        if s.startswith("サブタイトル:"):
            subtitle = s
            continue
        # page markers: "# P1" etc
        m = re.match(r"^#\s*P(\d)\s*$", s)
        if m:
            out.append('<div class="pagebreak" id="p%s">%s ページ目</div>' % (m.group(1), m.group(1)))
            continue
        if s == "次のページ":
            continue
        if s.startswith("## "):
            h = s[3:].strip()
            if h in ("リード", "目次"):
                out.append('<h2>%s</h2>' % inline(h))
                continue
            if h == "執筆メモ（編集用・記事には含めない）":
                out.append('<div class="memo"><h2>%s</h2>' % inline(h))
                in_memo = True
                continue
            out.append('<h2>%s</h2>' % inline(h))
            continue
        if s.startswith("### "):
            out.append('<h3>%s</h3>' % inline(s[4:].strip()))
            continue
        if s.startswith("［") or s.startswith("["):
            out.append(figure_block(s))
            continue
        if s.startswith("> "):
            out.append('<div class="lead"><p>%s</p></div>' % inline(s[2:].strip()))
            continue
        if re.match(r"^[-*]\s+", s):
            items = [re.sub(r"^[-*]\s+", "", s)]
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(re.sub(r"^[-*]\s+", "", lines[i].strip()))
                i += 1
            out.append("<ul>" + "".join("<li>%s</li>" % inline(x) for x in items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s+", s):
            items = [re.sub(r"^\d+\.\s+", "", s)]
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            out.append("<ol>" + "".join("<li>%s</li>" % inline(x) for x in items) + "</ol>")
            continue
        # speaker quote
        if s.startswith("「") and re.search(r"（[^（）]+氏）\s*$", s):
            out.append('<div class="quote">%s</div>' % inline(s))
            continue
        out.append("<p>%s</p>" % inline(s))

    flush_table()
    if in_memo:
        out.append("</div>")

    doc = "\n".join(out)
    page = """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s｜原稿プレビュー</title>
<style>%(css)s</style>
<script>%(js)s</script>
</head><body>
<div class="nav">
  <a href="#p1">1ページ目</a><a href="#p2">2ページ目</a><a href="#p3">3ページ目</a>
  <span class="sp"></span>
  <span>文字サイズ</span>
  <button id="fsdown" type="button">A−</button>
  <span id="fsval">19px</span>
  <button id="fsup" type="button">A＋</button>
</div>
<div class="doc">
<h1>%(title)s</h1>
<p class="sub">%(sub)s</p>
%(doc)s
</div>
</body></html>""" % {
        "title": html.escape(title),
        "sub": inline(subtitle),
        "css": CSS,
        "js": JS,
        "doc": doc,
    }

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print(OUT, os.path.getsize(OUT) // 1024, "KB")


if __name__ == "__main__":
    main()
