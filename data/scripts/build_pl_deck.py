# -*- coding: utf-8 -*-
"""2026年度PL分析・構造転換提言 経営会議資料（社外秘）"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
import os

OUT = r"C:\Users\020168\Documents\cowork_root\02_社内資料・データ\経営・マネジメント\PL資料\202605\2026PL分析_構造転換提言.pptx"

# ---- palette (Midnight Executive) ----
NAVY = RGBColor(0x1E, 0x27, 0x61)
NAVY2 = RGBColor(0x2B, 0x35, 0x73)
ICE = RGBColor(0xE9, 0xEE, 0xF9)
ICE2 = RGBColor(0xF4, 0xF7, 0xFC)
STEEL = RGBColor(0x5B, 0x6B, 0x8C)
INK = RGBColor(0x22, 0x26, 0x33)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED = RGBColor(0xC0, 0x39, 0x2B)
GREEN = RGBColor(0x1E, 0x8E, 0x6A)
AMBER = RGBColor(0xC9, 0x82, 0x1B)
LINEC = RGBColor(0xD4, 0xDB, 0xE8)

FONT = "Yu Gothic UI"
FONTB = "Yu Gothic UI"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = 13.333, 7.5


def slide(bg=WHITE):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = bg
    return s


def box(s, x, y, w, h, fill=None, line=None, lw=1.0, shape=MSO_SHAPE.RECTANGLE, radius=None):
    sp = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(lw)
    sp.shadow.inherit = False
    return sp


def txt(s, text, x, y, w, h, size=14, color=INK, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, font=FONT, spacing=1.0, italic=False, wrap=True):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    lines = text if isinstance(text, list) else [text]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if spacing: p.line_spacing = spacing
        runs = ln if isinstance(ln, list) else [(ln, {})]
        for t, o in runs:
            r = p.add_run(); r.text = t
            r.font.name = o.get("font", font)
            r.font.size = Pt(o.get("size", size))
            r.font.bold = o.get("bold", bold)
            r.font.italic = o.get("italic", italic)
            r.font.color.rgb = o.get("color", color)
    return tb


def eyebrow(s, n, label):
    txt(s, f"{n:02d}", 0.6, 0.34, 0.7, 0.4, size=13, color=STEEL, bold=True)
    txt(s, label, 1.25, 0.34, 11.4, 0.4, size=12.5, color=STEEL, bold=True)


def title(s, t, color=NAVY):
    txt(s, t, 0.6, 0.62, 12.1, 0.85, size=29, color=color, bold=True, font=FONTB)


def footer(s, page, dark=False):
    c = RGBColor(0xB9, 0xC2, 0xD6) if dark else STEEL
    txt(s, "社外秘 / 社内検討用", 0.6, 7.06, 4.0, 0.33, size=9, color=c)
    txt(s, "翔泳社 2026年度PL分析・構造転換提言（2026/6/19）", 5.0, 7.06, 6.4, 0.33, size=9, color=c, align=PP_ALIGN.RIGHT)
    txt(s, str(page), 12.5, 7.06, 0.4, 0.33, size=9, color=c, align=PP_ALIGN.RIGHT)


def style_table(tbl, header_fill=NAVY, header_color=WHITE, hsize=11, bsize=10.5,
                body_fill=WHITE, alt_fill=ICE2, font=FONT):
    for ci, cell in enumerate(tbl.rows[0].cells):
        cell.fill.solid(); cell.fill.fore_color.rgb = header_fill
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER if ci > 0 else PP_ALIGN.LEFT
            for r in p.runs:
                r.font.bold = True; r.font.size = Pt(hsize); r.font.color.rgb = header_color; r.font.name = font
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_top = Pt(2); cell.margin_bottom = Pt(2)
    for ri in range(1, len(tbl.rows)):
        for ci, cell in enumerate(tbl.rows[ri].cells):
            cell.fill.solid(); cell.fill.fore_color.rgb = body_fill if ri % 2 == 1 else alt_fill
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_top = Pt(1); cell.margin_bottom = Pt(1)
            cell.margin_left = Pt(5)
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER
                for r in p.runs:
                    r.font.size = Pt(bsize); r.font.name = font
                    if r.font.color.type is None:
                        r.font.color.rgb = INK


def add_table(s, data, x, y, w, h, colw=None, **kw):
    rows, cols = len(data), len(data[0])
    gt = s.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = gt.table
    if colw:
        tot = sum(colw)
        for i, cw in enumerate(colw):
            tbl.columns[i].width = Emu(int(Inches(w) * cw / tot))
    for ri, row in enumerate(data):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            cell.text = ""
            p = cell.text_frame.paragraphs[0]
            if isinstance(val, tuple):
                r = p.add_run(); r.text = val[0]
                r.font.color.rgb = val[1]
                if len(val) > 2 and val[2]: r.font.bold = True
            else:
                r = p.add_run(); r.text = str(val)
    style_table(tbl, **kw)
    return tbl


# ============ Slide 1 : 表紙 ============
s = slide(NAVY)
box(s, 0, 0, SW, 0.16, fill=RGBColor(0x4A, 0x5C, 0x9E))
txt(s, "社外秘", 11.55, 0.5, 1.2, 0.42, size=11, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
box(s, 11.5, 0.48, 1.25, 0.46, fill=AMBER)
txt(s, "社外秘", 11.5, 0.5, 1.25, 0.42, size=11, color=NAVY, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, "2026年度 経営会議資料", 0.9, 2.25, 11, 0.5, size=15, color=RGBColor(0xCA,0xDC,0xFC), bold=True)
txt(s, ["2026年度 PL分析と", "事業構造転換の提言"], 0.9, 2.75, 11.6, 1.9, size=42, color=WHITE, bold=True, font=FONTB, spacing=1.05)
txt(s, "全社・部門別の業績と見通し ／ 競合比較 ／ 出版部門の構造転換（人件費・直接原価）",
    0.9, 4.85, 11.6, 0.5, size=14, color=RGBColor(0xCA,0xDC,0xFC))
box(s, 0.9, 5.55, 3.2, 0.04, fill=RGBColor(0x4A,0x5C,0x9E))
txt(s, ["データ：4-5月実績＋6/16時点メディア上期読み（2026PL_翔泳社.xlsx／メディア_読み報告.xlsx）",
        "作成：analyst　2026年6月19日"],
    0.9, 5.75, 11.6, 0.8, size=11, color=RGBColor(0x9F,0xAD,0xCC), spacing=1.2)

# ============ Slide 2 : エグゼクティブサマリー ============
s = slide()
eyebrow(s, 1, "EXECUTIVE SUMMARY")
title(s, "結論：利益エンジン（メディア）が減速、出版は構造的赤字体質")
cards = [
    ("01", "全社は赤字スタート", RED,
     "4-5月の売上達成率は75.6%。営業利益は予算+85百万に対し実績▲33百万。ほぼ全部門が予算比76%前後で着地。"),
    ("02", "利益の89%がメディア依存", NAVY,
     "全社営業利益318百万のうちメディアが283百万（89%）。出版は薄利1.5%。メディアが減速すると全社利益が直撃される構造。"),
    ("03", "メディアは想定成長せず", AMBER,
     "上期読み662百万＝前年並み（±0%）。予算比▲58。主因は主力Web媒体（MarkeZine/EZ/CodeZine）の未達。AIdiverは投資フェーズで計画内。イベントは+18で堅調。"),
    ("04", "出版は固定費が重い", RED,
     "人件費37%＋直接費32%＝売上の約69%。売上が予算比76%に沈むと即赤字（4-5月OP▲23百万）。"),
]
cx, cy, cw, ch, gap = 0.6, 1.7, 5.95, 1.5, 0.25
for i, (n, head, col, body) in enumerate(cards):
    x = cx + (i % 2) * (cw + gap)
    y = cy + (i // 2) * (ch + gap)
    box(s, x, y, cw, ch, fill=ICE2, line=LINEC, lw=0.75)
    box(s, x, y, 0.09, ch, fill=col)
    txt(s, n, x + 0.28, y + 0.16, 0.8, 0.4, size=15, color=col, bold=True)
    txt(s, head, x + 0.95, y + 0.16, cw - 1.1, 0.4, size=14.5, color=INK, bold=True)
    txt(s, body, x + 0.28, y + 0.62, cw - 0.55, ch - 0.7, size=11.5, color=STEEL, spacing=1.08)
box(s, 0.6, 4.95, 12.13, 1.5, fill=NAVY)
txt(s, "提言の柱", 0.95, 5.12, 3, 0.4, size=13, color=RGBColor(0xCA,0xDC,0xFC), bold=True)
txt(s, [
    [("メディア：", {"bold": True, "color": WHITE}), ("ウェブをリード型・AIパッケージ・会員活用へ転換（AIdiver）。イベントは成長エンジンとして協賛枠を早期確定。", {"color": RGBColor(0xE3,0xE9,0xF7)})],
    [("出版：", {"bold": True, "color": WHITE}), ("原価・在庫改革（Phase0）で率5%超 → 人員を成長部門へ再配置（Phase1）→ 残る余剰のみ人員圧縮（Phase2／最終手段）。", {"color": RGBColor(0xE3,0xE9,0xF7)})],
    [("全社：", {"bold": True, "color": WHITE}), ("AIを軸に出版×メディア×イベントを統合。検索流入減のヘッジは会員基盤（KGI10万人）。", {"color": RGBColor(0xE3,0xE9,0xF7)})],
], 0.95, 5.5, 11.5, 0.9, size=11.5, spacing=1.12)
footer(s, 2)

# ============ Slide 3 : 全社の結果と利益構造 ============
s = slide()
eyebrow(s, 2, "GROUP RESULTS")
title(s, "全社：売上は予算比76%、利益はメディアに一極集中")
txt(s, "通期予算の構造（百万円）", 0.6, 1.65, 6, 0.35, size=13, color=NAVY, bold=True)
add_table(s, [
    ["部門", "売上予算", "営業利益", "利益率", "OP寄与"],
    ["出版", "2,288", ("35", RED), "1.5%", "11%"],
    ["メディア", "1,518", ("283", GREEN), "18.7%", ("89%", NAVY, True)],
    [("全社", INK, True), ("3,806", INK, True), ("318", INK, True), ("8.4%", INK, True), "100%"],
], 0.6, 2.05, 6.5, 1.7, colw=[1.6, 1.4, 1.2, 1.0, 1.0])
txt(s, "4-5月実績（純売上・百万円）", 0.6, 4.0, 6, 0.35, size=13, color=NAVY, bold=True)
add_table(s, [
    ["", "売上予算", "売上実績", "達成率", "OP実績"],
    ["出版", "445", "339", "76.2%", ("▲23", RED)],
    ["メディア", "185", "137", "74.0%", ("▲10", RED)],
    [("全社", INK, True), ("629", INK, True), ("475", INK, True), ("75.6%", RED, True), ("▲33", RED, True)],
], 0.6, 4.4, 6.5, 1.7, colw=[1.6, 1.4, 1.4, 1.1, 1.1])
# doughnut: OP contribution
chart_data = CategoryChartData()
chart_data.categories = ["メディア", "出版"]
chart_data.add_series("OP寄与", (283, 35))
gframe = s.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(7.5), Inches(1.9), Inches(5.2), Inches(4.3), chart_data)
ch = gframe.chart
ch.has_legend = True; ch.legend.position = XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout = False
ch.legend.font.size = Pt(11); ch.legend.font.name = FONT
ch.has_title = True; ch.chart_title.text_frame.text = "営業利益の寄与（通期予算）"
ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(13)
ch.chart_title.text_frame.paragraphs[0].runs[0].font.name = FONT
plot = ch.plots[0]
plot.has_data_labels = True
plot.data_labels.number_format = '0"%"'; plot.data_labels.number_format_is_linked = False
plot.data_labels.show_percentage = True; plot.data_labels.show_value = False
plot.data_labels.font.size = Pt(13); plot.data_labels.font.bold = True; plot.data_labels.font.color.rgb = WHITE
pts = plot.series[0].points
pts[0].format.fill.solid(); pts[0].format.fill.fore_color.rgb = NAVY
pts[1].format.fill.solid(); pts[1].format.fill.fore_color.rgb = RGBColor(0xB6, 0xC0, 0xD8)
txt(s, "メディアが全社営業利益の89%を稼ぐ＝メディアの減速がそのまま全社利益のリスク。",
    7.5, 6.05, 5.2, 0.6, size=11, color=STEEL, align=PP_ALIGN.CENTER, spacing=1.05)
footer(s, 3)

# ============ Slide 4 : メディア事業 上期読み ============
s = slide()
eyebrow(s, 3, "MEDIA — 1H FORECAST")
title(s, "メディア：不振は主力Web媒体の未達。AIdiverは投資フェーズで計画内")
# clustered column
cd = CategoryChartData()
cd.categories = ["イベント", "ウェブ", "書籍"]
cd.add_series("予算", (320, 396, 5))
cd.add_series("読み", (338, 319, 6))
cd.add_series("前年実績", (323, 338, 1))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.6), Inches(1.75), Inches(7.0), Inches(4.6), cd)
c = gf.chart
c.has_title = True; c.chart_title.text_frame.text = "メディア上期（4-9月）売上 比較（百万円）"
c.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(13); c.chart_title.text_frame.paragraphs[0].runs[0].font.name = FONT
c.has_legend = True; c.legend.position = XL_LEGEND_POSITION.TOP; c.legend.include_in_layout = False
c.legend.font.size = Pt(11); c.legend.font.name = FONT
c.series[0].format.fill.solid(); c.series[0].format.fill.fore_color.rgb = RGBColor(0xB6,0xC0,0xD8)
c.series[1].format.fill.solid(); c.series[1].format.fill.fore_color.rgb = NAVY
c.series[2].format.fill.solid(); c.series[2].format.fill.fore_color.rgb = RGBColor(0x9A,0xB8,0xA8)
ca = c.value_axis; ca.has_major_gridlines = True
ca.major_gridlines.format.line.color.rgb = LINEC
c.category_axis.tick_labels.font.size = Pt(11); c.category_axis.tick_labels.font.name = FONT
c.value_axis.tick_labels.font.size = Pt(9); c.value_axis.tick_labels.font.name = FONT
# right insight panel
px = 7.85
box(s, px, 1.85, 4.9, 4.5, fill=ICE2, line=LINEC, lw=0.75)
txt(s, "読み取りどころ", px + 0.3, 2.05, 4.3, 0.4, size=13, color=NAVY, bold=True)
rows = [
    ("Web内訳（4-5月実績）", "未達は主力媒体：MarkeZine 77%（5月62%に失速）／EnterpriseZine 62%／CodeZine 78%／Biz/Zine 18%。▲77の主因はここ。", RED),
    ("AIdiver", "売上は僅少だが粗利赤字は“予算どおりの投資フェーズ”。▲77への影響は約▲2百万のみ。FY25は2-3月に予算比438-787%の実績も。継続投資の対象。", GREEN),
    ("Biz/Zine", "達成率18%・粗利赤字が継続。メディア内の再構築/統廃合の検討候補。", AMBER),
]
yy = 2.5
for label, body, col in rows:
    box(s, px + 0.3, yy + 0.05, 0.12, 1.1, fill=col)
    txt(s, label, px + 0.55, yy, 4.0, 0.35, size=12.5, color=INK, bold=True)
    txt(s, body, px + 0.55, yy + 0.34, 4.05, 1.0, size=10.6, color=STEEL, spacing=1.06)
    yy += 1.3
footer(s, 4)

# ============ Slide 5 : メディア媒体別 4-5月実績 ============
s = slide()
eyebrow(s, 4, "MEDIA — BY PRODUCT (APR-MAY)")
title(s, "媒体別：未達は主力Web媒体に集中、AIdiverは投資フェーズ")
add_table(s, [
    ["媒体", "売上予算", "売上実績", "達成率", "粗利実績", "評価"],
    ["MarkeZine", "60.0", "46.0", "77%", ("+23.4", GREEN), "最大媒体。5月62%に失速＝要回復筆頭"],
    ["CodeZine", "34.8", "27.1", "78%", ("+14.4", GREEN), "Devsumi系イベントが収益柱"],
    ["EnterpriseZine", "30.0", "18.7", ("62%", RED), ("+9.4", GREEN), "4月43%・変動大"],
    ["HRzine", "6.3", "8.3", ("132%", GREEN), ("+4.2", GREEN), "予算超で好調"],
    ["Biz/Zine", "7.7", "1.4", ("18%", RED), ("▲3.2", RED), "構造赤字。再構築/統廃合候補"],
    ["AIdiver", "3.6", "1.6", "44%", ("▲2.0", AMBER), "投資フェーズ（予算上も赤字）・絶対僅少"],
], 0.6, 1.7, 12.13, 2.9, colw=[1.8, 1.05, 1.05, 0.9, 1.05, 3.6])
txt(s, "単位：百万円（4-5月合計・EnterpriseZineはOEM除く）。出典：プロダクトPL（社外取締役会資料）", 0.6, 4.7, 12, 0.3, size=9, color=STEEL)
box(s, 0.6, 5.05, 5.95, 1.5, fill=ICE2, line=LINEC, lw=0.75)
box(s, 0.6, 5.05, 0.09, 1.5, fill=RED)
txt(s, "▲77の主因＝主力Web媒体", 0.85, 5.2, 5.5, 0.35, size=12.5, color=INK, bold=True)
txt(s, "ウェブ上期▲77の内訳は MarkeZine▲14／EnterpriseZine▲11／CodeZine▲7.6／Biz/Zine▲6.3。広告収益が立つ既存媒体の未達で、検索流入減・タイアップ単価の頭打ちと整合。", 0.85, 5.54, 5.5, 0.95, size=10.3, color=STEEL, spacing=1.04)
box(s, 6.78, 5.05, 5.95, 1.5, fill=NAVY)
txt(s, "AIdiverは“計画どおりの投資”", 7.03, 5.2, 5.5, 0.35, size=12.5, color=RGBColor(0xCA,0xDC,0xFC), bold=True)
txt(s, "粗利予算がそもそも赤字＝投資フェーズ。▲77への影響は約▲2百万のみ。FY25は2-3月に予算比438-787%（粗利率60%）の実績も。削減でなく会員・AX Dayでの収益化が筋。", 7.03, 5.54, 5.5, 0.95, size=10.3, color=RGBColor(0xE3,0xE9,0xF7), spacing=1.04)
footer(s, 5)

# ============ Slide 6 : 競合比較 ============
s = slide()
eyebrow(s, 5, "COMPETITIVE BENCHMARK")
title(s, "競合比較：規模では戦わない。専門領域×イベント×AI媒体で勝つ")
add_table(s, [
    ["社・媒体", "売上規模", "営業利益", "メディア/IT内訳", "出典"],
    [("翔泳社メディア事業（自社）", NAVY, True), "15.2億(予算)", ("2.83億(18.7%)", GREEN), "イベント/ウェブ/書籍", "社内PL"],
    ["アイティメディア(2148)", "81.0億", ("20.3億(25%)", GREEN), "BtoB31.6億／イベント牽引", "決算短信"],
    ["インプレスHD(9479)", "143.9億", ("▲2.37億(赤字)", RED), "IT区分60.0億", "IR"],
    ["日経BP（非上場）", "361億", "非開示", "日経クロステック等", "会社情報"],
    ["宣伝会議（非上場）", "約25.8億", "非開示", "MarkeZine領域の外部競合※", "官報"],
    ["Qiita（CodeZine競合）", "非開示", "—", "会員120万/月間UU600万", "walkerplus"],
], 0.6, 1.7, 12.13, 2.55, colw=[2.7, 1.5, 1.7, 2.6, 1.1],
   header_fill=NAVY)
txt(s, "※MarkeZine/MarkeZine Dayは翔泳社の自社媒体。外部競合として宣伝会議を調査。数値は2026/6/19取得・直近通期。", 0.6, 4.32, 12, 0.3, size=9, color=STEEL)  # noqa
# market + implication two columns
box(s, 0.6, 4.75, 5.9, 1.95, fill=ICE2, line=LINEC, lw=0.75)
txt(s, "市場トレンド（出典付き）", 0.85, 4.92, 5.4, 0.35, size=12.5, color=NAVY, bold=True)
txt(s, [
    [("ネット広告費 +10.8%", {"bold": True, "color": INK}), ("（構成比初の50.2%／電通）。ただし伸びは動画・運用型中心。", {"color": STEEL})],
    [("イベント・展示 +11.2%", {"bold": True, "color": INK}), ("（電通）。リアル＋ウェビナーのハイブリッドが潮流。", {"color": STEEL})],
    [("AI Overviews表示時クリック率 8%", {"bold": True, "color": RED}), ("（非表示時15%／Pew）。検索流入は構造的縮小。", {"color": STEEL})],
], 0.85, 5.3, 5.45, 1.3, size=10.8, spacing=1.1)
box(s, 6.83, 4.75, 5.9, 1.95, fill=NAVY)
txt(s, "示唆", 7.08, 4.92, 5.4, 0.35, size=12.5, color=RGBColor(0xCA,0xDC,0xFC), bold=True)
txt(s, [
    [("・ ", {"color": WHITE}), ("ウェブ不振は自社固有でなく業界構造（検索流入半減）。", {"color": RGBColor(0xE3,0xE9,0xF7)})],
    [("・ ", {"color": WHITE}), ("イベント重心は市場と整合。最大手も「イベント牽引」で25%黒字。", {"color": RGBColor(0xE3,0xE9,0xF7)})],
    [("・ ", {"color": WHITE}), ("AI媒体は最大手も売上を単独開示せず＝空白。AIdiver先行の好機。", {"color": RGBColor(0xE3,0xE9,0xF7)})],
    [("・ ", {"color": WHITE}), ("検索減のヘッジは会員・コミュニティ化（KGI10万人）。", {"color": RGBColor(0xE3,0xE9,0xF7)})],
], 7.08, 5.3, 5.45, 1.3, size=10.8, spacing=1.08)
footer(s, 6)

# ============ Slide 6 : 出版の構造問題 ============
s = slide()
eyebrow(s, 6, "PUBLISHING — COST STRUCTURE")
title(s, "出版：人件費37%＋直接費32%が売上の約7割を占める")
# 100% stacked bar (horizontal)
cd = CategoryChartData()
cd.categories = ["出版コスト構造（売上比）"]
segs = [("直接費", 32.3, RGBColor(0x3C,0x4A,0x8A)),
        ("人件費", 37.0, NAVY),
        ("販売印税", 8.8, RGBColor(0x6B,0x7B,0xB0)),
        ("その他原価・販管・SEHI等", 20.4, RGBColor(0xB6,0xC0,0xD8)),
        ("営業利益", 1.5, GREEN)]
for name, val, _ in segs:
    cd.add_series(name, (val,))
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED_100, Inches(0.6), Inches(1.75), Inches(12.1), Inches(1.9), cd)
c = gf.chart
c.has_title = False
c.has_legend = True; c.legend.position = XL_LEGEND_POSITION.BOTTOM; c.legend.include_in_layout = False
c.legend.font.size = Pt(11); c.legend.font.name = FONT
for i, (_, _, col) in enumerate(segs):
    c.series[i].format.fill.solid(); c.series[i].format.fill.fore_color.rgb = col
c.category_axis.tick_labels.font.size = Pt(10); c.category_axis.tick_labels.font.name = FONT
c.value_axis.has_major_gridlines = False
c.value_axis.visible = False
# detail callouts
txt(s, "構造の問題", 0.6, 3.95, 6, 0.35, size=13, color=NAVY, bold=True)
txt(s, [
    [("人件費 847百万（37.0%）", {"bold": True, "color": NAVY, "size": 13}), ("　原価394＋販管453。最大の固定費。", {"color": STEEL})],
    [("直接費 739百万（32.3%）", {"bold": True, "color": NAVY, "size": 13}), ("　印刷・用紙・製本・外注。部数設計に依存。", {"color": STEEL})],
    [("→ 売上が予算比76%に沈むと即赤字（4-5月 営業利益 ▲23百万）。", {"bold": True, "color": RED})],
], 0.6, 4.35, 7.4, 1.7, size=11.5, spacing=1.3)
# stat callouts right
box(s, 8.3, 3.95, 4.43, 2.4, fill=ICE2, line=LINEC, lw=0.75)
txt(s, "47%", 8.6, 4.15, 3.8, 0.7, size=34, color=NAVY, bold=True)
txt(s, "売上総利益率（通期予算）。一方で販管・固定費が利益を消す。", 8.6, 4.9, 3.85, 0.5, size=10.5, color=STEEL, spacing=1.05)
txt(s, "1.5%", 8.6, 5.45, 3.8, 0.6, size=30, color=RED, bold=True)
txt(s, "出版の営業利益率。人員規模は人件費ベースで全社の約6割（概算90名）。", 8.6, 6.0, 3.85, 0.5, size=10.5, color=STEEL, spacing=1.05)
footer(s, 7)

# ============ Slide 7 : 構造転換 Phase 0/1/2 ============
s = slide()
eyebrow(s, 7, "PUBLISHING — TRANSFORMATION")
title(s, "出版の構造転換：「純減」より「成長部門への再配置」を優先")
phases = [
    ("PHASE 0", "原価・在庫改革（即時／人員影響なし）", GREEN,
     ["初版部数の最適化・POD/電子先行（直接費▲5%）",
      "印刷・用紙・製本の再交渉（直接費▲2-3%）",
      "滞留在庫の処分で保管料▲20-30%",
      "効果の低い販促の停止"],
     "営業利益 +80〜100百万（率5%超）"),
    ("PHASE 1", "再配置による構造転換（3-6ヶ月）", NAVY,
     ["取次依存→直販（SEshop）シフト",
      "校閲・制作・販売管理など重複機能を集約・外注化",
      "出版編集の余剰を成長テーマ（AI）へ",
      "メディア/AIdiver/イベント/直販へ配置転換"],
     "固定費を成長セグメントの売上に紐付け直し利益化"),
    ("PHASE 2", "人員圧縮（最終手段／要・法務・労使）", RED,
     ["Phase0+1後も残る構造的余剰のみ対象",
      "希望退職・早期退職を検討",
      "整理解雇の4要件・手続きの遵守が前提",
      "下表の3パターンで試算"],
     "下表参照（10/15/20名）"),
]
cx, cw, gap = 0.6, 3.97, 0.11
for i, (tag, head, col, items, eff) in enumerate(phases):
    x = cx + i * (cw + gap)
    box(s, x, 1.7, cw, 3.0, fill=WHITE, line=LINEC, lw=1.0)
    box(s, x, 1.7, cw, 0.5, fill=col)
    txt(s, tag, x + 0.2, 1.78, cw - 0.4, 0.36, size=13, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, head, x + 0.2, 2.32, cw - 0.4, 0.62, size=11.5, color=INK, bold=True, spacing=1.05)
    txt(s, [[("• ", {"color": col, "bold": True}), (it, {"color": STEEL})] for it in items],
        x + 0.2, 3.0, cw - 0.4, 1.25, size=10.3, spacing=1.18)
    box(s, x + 0.2, 4.25, cw - 0.4, 0.36, fill=ICE)
    txt(s, eff, x + 0.2, 4.27, cw - 0.4, 0.33, size=10, color=NAVY, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
# phase2 table
txt(s, "Phase 2 人員圧縮シナリオ（平均給与530万円前提。会社負担＝総額人件費は給与の約1.3-1.5倍）", 0.6, 4.85, 12.1, 0.32, size=11.5, color=NAVY, bold=True)
add_table(s, [
    ["削減人数", "給与ベース節減", "総額人件費ベース節減", "出版営業利益の着地（現状35百万）"],
    ["10名", "53百万", "74百万", ("約90〜110百万", GREEN)],
    ["15名", "80百万", "111百万", ("約120〜150百万", GREEN)],
    ["20名", "106百万", "148百万", ("約150〜180百万（率6〜8%）", GREEN, True)],
], 0.6, 5.2, 12.13, 1.5, colw=[1.4, 1.8, 2.0, 3.4])
footer(s, 8)

# ============ Slide 8 : 改善アクション総括 ============
s = slide()
eyebrow(s, 8, "ACTION PLAN")
title(s, "改善アクション総括（優先順位）")
add_table(s, [
    ["優先", "領域", "アクション", "ねらい・効果"],
    [("★1", RED, True), "メディア（主力Web）", "MarkeZine/CodeZine/EZの広告回復・リード型/AIパッケージ化", "未達の主因（▲77）の回復"],
    [("★2", RED, True), "メディア", "イベント協賛枠の早期確定（9月+68百万ほか）", "成長エンジン・読みを“確定”に"],
    [("★3", AMBER, True), "メディア", "Biz/Zineの再構築/統廃合を検討", "構造赤字（達成率18%）の解消"],
    [("★4", GREEN, True), "AIdiver", "投資継続。会員・AX Dayで収益化、短期広告でなくKPIで評価", "KGI10万人・将来の収益源"],
    [("★5", NAVY, True), "出版", "Phase0：原価・在庫・販促改革", "人員に手をつけず +80〜100百万"],
    [("★6", NAVY, True), "出版", "取次→直販シフト・機能集約・成長部門へ再配置", "薄利構造の是正・固定費の利益化"],
    [("★7", AMBER, True), "出版", "Phase2：希望/早期退職（最終手段）", "10名で+74前後（要・法務/労使）"],
    [("★8", NAVY, True), "全社", "AI軸で出版×メディア×イベントを統合", "成長テーマへの集中・KGI10万人"],
], 0.6, 1.65, 12.13, 3.75, colw=[0.85, 2.1, 5.0, 4.0], bsize=10)
box(s, 0.6, 5.62, 12.13, 0.92, fill=NAVY)
txt(s, "推奨ストーリー", 0.9, 5.74, 3, 0.32, size=11.5, color=RGBColor(0xCA,0xDC,0xFC), bold=True)
txt(s, "メディアは主力Webの回復＋イベント拡大＋Biz/Zine再構築（AIdiverは投資継続）。出版はPhase0→成長部門へ再配置→残余のみPhase2。"
       "「リストラ」ではなく「成長部門への再配置を伴う構造転換」として説明できる。",
    0.9, 6.06, 11.5, 0.45, size=11, color=WHITE, spacing=1.05)
footer(s, 9)

# ============ Slide 9 : 結び ============
s = slide(NAVY)
box(s, 0, 0, SW, 0.16, fill=RGBColor(0x4A,0x5C,0x9E))
txt(s, "結び", 0.9, 2.0, 11, 0.5, size=15, color=RGBColor(0xCA,0xDC,0xFC), bold=True)
txt(s, ["コスト削減で終わらせず、", "AI軸の事業統合で成長へ転換する"], 0.9, 2.5, 11.6, 1.7, size=36, color=WHITE, bold=True, spacing=1.05)
txt(s, [
    [("・ ", {"color": AMBER, "bold": True}), ("出版の編集力とリソースを、伸びるAI領域（書籍・記事・イベント・法人研修）へ集中。", {"color": RGBColor(0xE3,0xE9,0xF7)})],
    [("・ ", {"color": AMBER, "bold": True}), ("取次・検索流入という縮小チャネルから、SEshop直販＋AIdiver会員という直接顧客基盤へ。", {"color": RGBColor(0xE3,0xE9,0xF7)})],
    [("・ ", {"color": AMBER, "bold": True}), ("AIdiver会員10万人（KGI）が、メディア事業の防衛と成長の両方を支える。", {"color": RGBColor(0xE3,0xE9,0xF7)})],
], 0.9, 4.5, 11.6, 1.6, size=14, spacing=1.35)
footer(s, 10, dark=True)

prs.save(OUT)
print("SAVED:", OUT)
print("slides:", len(prs.slides._sldIdLst))
