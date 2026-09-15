# -*- coding: utf-8 -*-
"""Inside AIdiver 動画出演依頼書ビルダー。

スキル aidiver-interview-request の書式関数と固定法務文言を再利用し、
動画版（NVIDIA井﨑様前例）のセクション順で組む。

Usage:
    python build_video_req.py <output.docx>
"""
import sys
import importlib.util
from docx import Document
from docx.shared import Pt, Mm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SKILL = (
    r"C:\Users\020168\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin"
    r"\43fa4d1d-1676-423f-a3c9-71b48e4232a1\4d501c8a-9dda-4aa3-9dae-636ecfd67e4f"
    r"\skills\aidiver-interview-request\scripts\build_request.py"
)
spec = importlib.util.spec_from_file_location("br", SKILL)
br = importlib.util.module_from_spec(spec)
spec.loader.exec_module(br)
para, MINCHO = br.para, br.MINCHO

D = {}

D["宛名"] = "OpenAI Japan合同会社\n執行役員 GTMパートナーシップ　水嶋 ディノ様"

D["取材希望日時"] = (
    "10月～11月\n"
    "（30分リハーサル＋60分撮影＋予備30分：合計約120分前後）\n"
    "※日程はご都合最優先で調整いたします。"
)

D["動画シリーズ概要"] = (
    "・動画シリーズ名：Inside AIdiver\n"
    "・シリーズのタグライン：最前線の声でAIの“今”をアップデート。\n"
    "・動画尺：20〜30分 前後の動画が1本 or 2本\n"
    "・撮影場所：弊社オフィス（四谷三丁目駅 周辺）\n"
    "https://www.shoeisha.co.jp/about#access\n"
    "・撮影時間：120分\n"
    "・掲載時期：撮影後、最短1ヵ月以降となります。\n"
    "AI業界の最前線に直接切り込み、意思決定の背景や具体的なフロー、実情など\n"
    "企業におけるAIの今を徹底深掘りするインタビュー形式の企画シリーズとなります。\n"
    "視聴後すぐに活用できるノウハウで、皆さまの明日の一手を後押しするようなコンテンツをお届けしていきます。\n"
    "\n"
    "※基本的には1本想定。尺などの都合により2本になるケースもあり。"
)

D["取材テーマ"] = (
    "OpenAIが描く、人とAIの協働\n"
    "─ GPT-6 Astraは、企業の仕事と人の役割をどう作り変えるのか"
)

D["取材趣旨"] = (
    "9月8日のMarkeZine Day 2026 Autumnでは、基調セッション「AIエージェント時代のマーケティング変革」に"
    "ご登壇いただき、誠にありがとうございました。今回はあらためて、AIdiverの主要読者である"
    "CAIO・CDO・CIOクラスの意思決定層に向けて、動画シリーズ『Inside AIdiver』にご出演いただきたく"
    "ご相談申し上げます。\n"
    "本企画でフォーカスしたいのは、9月3日に発表されたGPT-6 Astraです。"
    "「コンピューターでできることなら、Astraがあなたに代わって実行する。しかも、速く。」"
    "──依頼を受けて成果物をつくるところまで進めるモデルの登場は、"
    "企業が業務プロセスと人の役割を引き直す段階に入ったことを意味すると捉えております。\n"
    "一方で日本企業の多くは、どこまでをAIに任せ、どこを人が確認するのか、"
    "その線引きを組織のルールとして決めきれていません。日本市場の実装現場をご覧になっている水嶋様に、"
    "OpenAIが人とAIの協働をどう描いているのかを伺えればと考えております。\n"
    "何卒ご協力をいただければ幸いです。"
)

D["媒体概要"] = (
    "・AIdiver： https://aidiver.jp/\n"
    "IT技術書やビジネス書などの専門書籍や『CodeZine』『MarkeZine』『EnterpriseZine』などのWebメディアを"
    "運営する出版社、株式会社翔泳社が2025年9月にローンチしたAI情報専門メディア。『AIdiver』のミッションは、"
    "劇的に進化するAI時代において、ビジネスパーソン・企業がAIを味方につけ、AX（AI Transformation）を実行し、"
    "次の10年を切り拓くための羅針盤となること。CAIO、CDO、CIOなどAI戦略の策定、AXを推進する意思決定層、"
    "DX推進部門／IT部門の部課長・リーダー、次のCAIO／CDO／CIO候補など、AIファーストで戦略の策定、"
    "AX推進を意思決定する層をターゲットとする。20年のメディア運営ノウハウをベースとし、"
    "既存10メディアと連携しつつ多角的な情報を提供。\n"
    "\n"
    "・AIdiver【AI専門メディア】：YouTube、X、Instagram\n"
    "2025年11月に配信開始したAI情報専門メディアAIdiverのYouTubeアカウント。\n"
    "https://www.youtube.com/@AIdiver_jp"
)

D["質問事項"] = [
    {
        "見出し": "■現在地：GPT-6 Astraが変えた前提",
        "質問": [
            "「コンピューターでできることなら、Astraがあなたに代わって実行する。しかも、速く。」"
            "──2026年9月3日のGPT-6 Astraの発表に際して、御社はこのメッセージを掲げられました。"
            "依頼を受けて複数のツールを使い、成果物をつくるところまで進める。"
            "これまでのAI活用と何が非連続に変わったと捉えていらっしゃいますか。",

            "ChatGPTの週間アクティブユーザーは10億人を超え、OpenAI製品を利用する企業も200万社を超えました。"
            "これだけの規模で使われている中で、成果につながる企業とそうでない企業を分ける差は、"
            "どこに見えてきているのでしょうか。",

            "エージェントが成果物まで作り切ることが前提になると、"
            "これまで「AI導入プロジェクト」と呼んでいたものの中身が変わってくるように思います。"
            "企業はいま、ツールを導入しているのではなく何を設計していると考えるべきなのでしょうか。",
        ],
    },
    {
        "見出し": "■実践：人とAIの協働を、組織としてどう設計するか",
        "質問": [
            "どこまでをAIに任せ、どこを人が確認するか。この線引きを個々の工夫に委ねている企業がまだ多いように見えます。"
            "組織のルールとして決めるとすれば、何を基準に線を引けばよいのでしょうか。",

            "その線引きは、業種や企業によっても変わってくるように思います。"
            "OpenAIから見て、いまどのような業種・企業で活用が進んでいるとお感じでしょうか。"
            "差し支えのない範囲で具体的な事例を挙げていただきつつ、"
            "うまく進んでいる企業に共通する進め方があれば伺いたいです。",

            "仕事の目的や背景、制約、顧客の声、過去の判断といった文脈をAIが参照できる状態に整えることは、"
            "現場の努力だけでは限界があります。この「AIが参照できる状態をつくる」責任は、"
            "組織の誰が担うべき仕事なのでしょうか。",

            "AI導入のROIがシビアに問われはじめています。"
            "AIによってどんな成果が出せたのかから逆算するのが理想だと思いますが、"
            "OpenAIとしてはAIに対するROIをどのようにとらえていらっしゃいますか。",
        ],
    },
    {
        "見出し": "■未来像：AGIという使命と、日本企業への提言",
        "質問": [
            "御社の使命は「AGIが人類全体に恩恵をもたらすようにすること」です。"
            "AGIという言葉は抽象的に受け取られがちですが、企業の仕事という文脈に置き換えると、"
            "それは何が実現された状態を指すのでしょうか。",

            "エージェントが仕事を終わらせてくれるようになった先で、"
            "企業の組織や職種はどう変わっていくとお考えでしょうか。"
            "人に残る仕事は、量ではなく質が変わるのだとすれば、それはどのような質なのでしょうか。",

            "最後に、AIdiver読者である日本企業のCAIO・CDO・CIOクラスの意思決定層に向けてメッセージをお願いします。"
            "人とAIの協働を本気で設計するために「最優先で取り組むべきこと」を挙げるとすれば、何でしょうか。",
        ],
    },
]


def build(out):
    doc = Document()
    s = doc.sections[0]
    s.page_width, s.page_height = Mm(210), Mm(297)
    s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Mm(25)
    st = doc.styles['Normal']
    st.font.name = MINCHO
    st.font.size = Pt(10.5)
    rPr = st.element.get_or_add_rPr()
    rf = rPr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rPr.insert(0, rf)
    for k in ('w:eastAsia', 'w:ascii', 'w:hAnsi'):
        rf.set(qn(k), MINCHO)

    para(doc, D["宛名"], size=12, bold=True, space_after=8)
    para(doc, "取材依頼書", align='center', size=14, bold=True, space_after=10)
    para(doc, "株式会社翔泳社 AIdiver編集部 編集長", align='right', space_after=2)
    para(doc, "押久保 剛", align='right', space_after=14)

    para(doc, "●取材希望日時", bold=True, space_after=2)
    para(doc, D["取材希望日時"], space_after=10)

    para(doc, "●動画シリーズの概要", bold=True, space_after=2)
    para(doc, D["動画シリーズ概要"], space_after=10)

    para(doc, "●取材テーマ", bold=True, space_after=2)
    para(doc, D["取材テーマ"], space_after=10)

    para(doc, "●取材趣旨", bold=True, space_after=2)
    para(doc, D["取材趣旨"], space_after=10)

    nq = sum(len(c["質問"]) for c in D["質問事項"])
    para(doc, f"●質問項目案（全{nq}問・3部構成）", bold=True, space_after=4)
    for c in D["質問事項"]:
        para(doc, c["見出し"], bold=True, space_after=4)
        for q in c["質問"]:
            para(doc, f"・{q}", space_after=4)
        para(doc, "", space_after=4)
    para(doc, "※当日の流れや時間配分により、質問の順序・表現を一部調整させていただく場合がございます。",
         space_after=10)

    para(doc, "● 掲載先・媒体概要", bold=True, space_after=2)
    para(doc, D["媒体概要"], space_after=10)

    para(doc, br.FIXED_PRE_REVIEW, space_after=6)
    para(doc, br.FIXED_POST_REVIEW, space_after=4)
    doc.save(out)
    print("Wrote:", out, "| 質問数:", nq)


if __name__ == "__main__":
    build(sys.argv[1])
