const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5

// palette
const INK = "20242C";      // near-black
const PAPER = "FFFFFF";
const SOFT = "5A6070";     // muted text
const BLUE = "1F4FA3";
const BLUESOFT = "E8EEF8";
const RED = "B0442C";
const REDSOFT = "F7ECE8";
const LINE = "D9D9D2";
const SURFACE = "F2F2EE";

const MINCHO = "Yu Mincho";
const GOTHIC = "Yu Gothic";

const W = 13.33, H = 7.5, MX = 0.7;
const CW = W - MX * 2;

function base(dark = false) {
  const s = pres.addSlide();
  s.background = { color: dark ? INK : PAPER };
  return s;
}

function header(s, no, title, sub) {
  s.addText(no, { x: MX, y: 0.42, w: CW, h: 0.3, fontFace: "Arial", fontSize: 10.5, bold: true, color: RED, charSpacing: 3, isTextBox: true, margin: 0 });
  s.addText(title, { x: MX, y: 0.72, w: CW, h: 0.75, fontFace: MINCHO, fontSize: 27, bold: true, color: INK, isTextBox: true, margin: 0 });
  if (sub) s.addText(sub, { x: MX, y: 1.44, w: CW, h: 0.35, fontFace: GOTHIC, fontSize: 12.5, color: SOFT, isTextBox: true, margin: 0 });
  s.addText("『THE PRINCIPLE』（仮）方向性ディスカッション — 翔泳社 押久保・大久保 / CONFIDENTIAL", { x: MX, y: 7.08, w: CW, h: 0.3, fontFace: GOTHIC, fontSize: 8.5, color: SOFT, isTextBox: true, margin: 0 });
  return s;
}

// helper: pill label
function pill(s, x, y, w, txt, bg) {
  s.addText(txt, { x, y, w, h: 0.32, fill: { color: bg }, fontFace: "Arial", fontSize: 10, bold: true, color: "FFFFFF", align: "center", valign: "middle", isTextBox: true, margin: 0, charSpacing: 2 });
}

/* ---------- 1. Title ---------- */
{
  const s = base(true);
  s.addText("SHOEISHA  EDITORIAL DISCUSSION DRAFT — CONFIDENTIAL", { x: MX, y: 1.25, w: CW, h: 0.35, fontFace: "Arial", fontSize: 11, bold: true, color: "7AA3E8", charSpacing: 4, isTextBox: true, margin: 0 });
  s.addText("『THE PRINCIPLE』（仮）\n方向性ディスカッション", { x: MX, y: 1.9, w: CW, h: 2.3, fontFace: MINCHO, fontSize: 42, bold: true, color: "FFFFFF", lineSpacing: 58, isTextBox: true, margin: 0 });
  s.addText("骨子ドラフトを受けた「軸・見せ方・伝える順番」のたたき台", { x: MX, y: 4.35, w: CW, h: 0.5, fontFace: GOTHIC, fontSize: 17, color: "C9CDD6", isTextBox: true, margin: 0 });
  s.addShape(pres.ShapeType.line, { x: MX, y: 5.35, w: CW, h: 0, line: { color: "3A3E48", width: 1 } });
  s.addText([
    { text: "2026年8月28日　", options: { color: "FFFFFF" } },
    { text: "翔泳社 押久保剛・大久保　｜　宛先：福田康隆さん MTG（1.5h）　｜　素材：骨子ドラフト（序章・第1〜4章・終章）＋7月メモ", options: { color: "9BA1AE" } },
  ], { x: MX, y: 5.55, w: CW, h: 0.4, fontFace: GOTHIC, fontSize: 12, isTextBox: true, margin: 0 });
}

/* ---------- 2. Goal ---------- */
{
  const s = header(base(), "00 — GOAL", "本日のゴール：90分で3つ決める");
  const rows = [
    ["1", "読者と軸", "誰の・どんな場面の本か。「原理原則」をどの角度から売るか", "本日決めたい"],
    ["2", "構成の背骨", "章立ての基本方針（続編ファースト型か、フェーズ背骨型か）", "方向感まで"],
    ["3", "進め方", "執筆順序・レビューサイクル・タイトル検討の段取り", "本日決めたい"],
  ];
  let y = 2.0;
  rows.forEach(r => {
    s.addShape(pres.ShapeType.rect, { x: MX, y, w: CW, h: 1.06, fill: { color: SURFACE }, line: { color: LINE, width: 0.75 } });
    s.addText(r[0], { x: MX + 0.18, y: y + 0.12, w: 0.8, h: 0.82, fontFace: MINCHO, fontSize: 34, bold: true, color: BLUE, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(r[1], { x: MX + 1.05, y: y + 0.14, w: 2.6, h: 0.78, fontFace: GOTHIC, fontSize: 17, bold: true, color: INK, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(r[2], { x: MX + 3.8, y: y + 0.14, w: 6.4, h: 0.78, fontFace: GOTHIC, fontSize: 12.5, color: INK, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(r[3], { x: MX + 10.35, y: y + 0.3, w: 1.45, h: 0.45, fill: { color: r[3] === "方向感まで" ? BLUESOFT : REDSOFT }, fontFace: GOTHIC, fontSize: 11, bold: true, color: r[3] === "方向感まで" ? BLUE : RED, align: "center", valign: "middle", isTextBox: true, margin: 0 });
    y += 1.26;
  });
  s.addText("タイムボックス案：前提共有 10分 → 読者と軸 30分 → 構成 30分 → 見せ方・タイトル 10分 → 進め方 10分", { x: MX, y: y + 0.1, w: CW, h: 0.4, fontFace: GOTHIC, fontSize: 12, color: SOFT, isTextBox: true, margin: 0 });
}

/* ---------- 3. Recommendation summary ---------- */
{
  const s = header(base(), "SUMMARY", "編集部の推し（先に結論）", "当日はこの4点を叩いてもらう前提のたたき台です");
  const items = [
    ["読者", "THE MODEL読者の「7年後」", "当時の営業・マーケ実務層が、いま経営を任されている。続編の読者は新しい誰かではなく、同じ読者のいまの悩みに定める。"],
    ["軸", "原理原則を売り物に、フェーズを背骨に", "最も新しい発見は「フェーズの誤認が最大の失敗要因」（19社を横から見た帰結）。原理原則はフェーズという地図に載せた瞬間、現在地から引ける実用書になる。"],
    ["順番", "THE MODELアンサーは1章に圧縮", "過去の答え合わせで前半を使い切らず、「横の視点 → フェーズの発見」をできるだけ早く出す。"],
    ["タイトル", "『THE PRINCIPLE』を推す", "序章の結び「自分にとってのPRINCIPLEを作ってほしい」と完全整合。単数形の意味（ダリオ『PRINCIPLES』との差別化）まで含めて当日議論。"],
  ];
  const cw2 = (CW - 0.3) / 2;
  items.forEach((it, i) => {
    const x = MX + (i % 2) * (cw2 + 0.3);
    const y = 2.0 + Math.floor(i / 2) * 2.5;
    s.addShape(pres.ShapeType.rect, { x, y, w: cw2, h: 2.3, fill: { color: SURFACE }, line: { color: LINE, width: 0.75 } });
    pill(s, x + 0.25, y + 0.25, 1.1, it[0], BLUE);
    s.addText(it[1], { x: x + 0.25, y: y + 0.68, w: cw2 - 0.5, h: 0.45, fontFace: MINCHO, fontSize: 16.5, bold: true, color: INK, isTextBox: true, margin: 0 });
    s.addText(it[2], { x: x + 0.25, y: y + 1.18, w: cw2 - 0.5, h: 1.0, fontFace: GOTHIC, fontSize: 11.5, color: INK, lineSpacing: 17, isTextBox: true, margin: 0 });
  });
}

/* ---------- 4. Draft map ---------- */
{
  const s = header(base(), "01 — CURRENT DRAFT", "骨子ドラフトの現状マップ", "共有6ファイルを読み込み整理。「P」印の原理原則の断片は、そのまま商品価値になる粒が揃っている");
  const rows = [
    [{ text: "章", options: { bold: true } }, { text: "内容", options: { bold: true } }],
    ["序章", "なぜもう一度書くのか — 環境の変化（SaaS is Dead／AI）＋立場の変化（縦→横の視点）。原理原則＝判断に根拠を持つための蓄積。マシン／経営視点の定義"],
    ["第1章", "「THE MODEL」とはなんだったのか — 成立秘話（vs シーベル、2004年スライド）／よくある疑問への回答／7年の変化（AIエージェント、支援から完結へ）"],
    ["第2章", "横から見るJapan Cloudと「フェーズ」という発見 — 持続的成長の条件／成長4パターン／時間差の原則　※後半にGTM・報酬設計・マネジメントシステムまで同居＝過積載"],
    ["第3章", "フェーズ別の原理原則 — STARS 5フェーズ×（特徴／重点アクション／原理原則）。「フェーズの誤認が最大の失敗要因」"],
    ["第4章", "採用・リーダーシップ・キャリア — マルチプライヤー／やってはいけない5つ・やるべき4つ（新任リーダーの90日論）"],
    ["終章", "自分のPRINCIPLESを作る — レゴと粘土／各章ワークのとりまとめ／Journey is the reward（退職メール全文）"],
  ];
  const tableRows = rows.map((r, i) => r.map((c, j) => ({
    text: typeof c === "string" ? c : c.text,
    options: {
      bold: i === 0 || j === 0,
      color: i === 0 ? "FFFFFF" : INK,
      fill: { color: i === 0 ? INK : (j === 0 ? SURFACE : PAPER) },
      fontFace: GOTHIC, fontSize: i === 0 ? 11 : 10.5,
      valign: "middle",
    },
  })));
  s.addTable(tableRows, { x: MX, y: 2.05, w: CW, colW: [1.3, CW - 1.3], border: { type: "solid", color: LINE, pt: 0.75 }, margin: 0.07, rowH: 0.62 });
}

/* ---------- 5. Structural signs ---------- */
{
  const s = header(base(), "01 — CURRENT DRAFT", "ドラフトから読み取れる構造上のサイン", "いま構成を決めるのが最も効率的なタイミング");
  const items = [
    ["章構成は未確定", "本文中に第5章（マネジメントシステム）・第6章（立ち上げ）・第7章（新任リーダー）への参照があり、頭の中の構成は7章前後。共有ドラフトの4章立てとズレている。"],
    ["第2章は分割必至", "「フェーズという発見」「GTM原理原則」「マネジメントシステム」が1章に同居。どう割るかの判断が、そのまま「本の軸」の議論になる。"],
    ["体験設計の種がある", "各章末ワーク＋終章での「自分のPRINCIPLE」とりまとめ。読者が書き込む一冊通しの体験は、前作にない差別化資産。"],
  ];
  const cw3 = (CW - 0.6) / 3;
  items.forEach((it, i) => {
    const x = MX + i * (cw3 + 0.3);
    s.addShape(pres.ShapeType.rect, { x, y: 2.15, w: cw3, h: 3.6, fill: { color: SURFACE }, line: { color: LINE, width: 0.75 } });
    s.addText(String(i + 1), { x: x + 0.28, y: 2.4, w: 1, h: 0.6, fontFace: MINCHO, fontSize: 30, bold: true, color: RED, isTextBox: true, margin: 0 });
    s.addText(it[0], { x: x + 0.28, y: 3.05, w: cw3 - 0.56, h: 0.65, fontFace: MINCHO, fontSize: 16, bold: true, color: INK, isTextBox: true, margin: 0 });
    s.addText(it[1], { x: x + 0.28, y: 3.75, w: cw3 - 0.56, h: 1.8, fontFace: GOTHIC, fontSize: 11.5, color: INK, lineSpacing: 17.5, isTextBox: true, margin: 0 });
  });
}

/* ---------- 6. Premise ---------- */
{
  const s = header(base(), "02 — PREMISE", "前提の確認：勝ち筋と、最大の敵");
  const cw2 = (CW - 0.3) / 2;
  s.addShape(pres.ShapeType.rect, { x: MX, y: 2.05, w: cw2, h: 3.4, fill: { color: BLUESOFT }, line: { color: BLUE, width: 1 } });
  s.addText("勝ち筋は「誰が言うか」", { x: MX + 0.3, y: 2.35, w: cw2 - 0.6, h: 0.5, fontFace: MINCHO, fontSize: 18, bold: true, color: BLUE, isTextBox: true, margin: 0 });
  s.addText("原理原則は誰でも語れる。しかし「累計19社の日本法人設立に関わり、12社の取締役として同じ時期に横から見た」人は日本にほぼいない。この観測点の希少性が本書の根拠。序章の「横の視点」がそれ。", { x: MX + 0.3, y: 2.95, w: cw2 - 0.6, h: 2.3, fontFace: GOTHIC, fontSize: 12.5, color: INK, lineSpacing: 20, isTextBox: true, margin: 0 });
  const x2 = MX + cw2 + 0.3;
  s.addShape(pres.ShapeType.rect, { x: x2, y: 2.05, w: cw2, h: 3.4, fill: { color: REDSOFT }, line: { color: RED, width: 1 } });
  s.addText("最大の敵は「原理原則」の抽象度", { x: x2 + 0.3, y: 2.35, w: cw2 - 0.6, h: 0.5, fontFace: MINCHO, fontSize: 18, bold: true, color: RED, isTextBox: true, margin: 0 });
  s.addText("THE MODELが売れたのは、持ち帰れる「型」があったから。本書は「型ではなく原則だ」と言う本であり、型を否定する本は型ほど売れにくい。だから編集の仕事は、型の代わりの「持ち帰れる道具」（フェーズ地図・原則の型化・ワーク）を設計すること。", { x: x2 + 0.3, y: 2.95, w: cw2 - 0.6, h: 2.3, fontFace: GOTHIC, fontSize: 12.5, color: INK, lineSpacing: 20, isTextBox: true, margin: 0 });
  s.addText("あえて指摘：狙いは「フレームワーク紹介で終わらせない」なのに、現骨子はSTARS・Playing to Win・ダリオ等、他者フレームワークの引用が背骨になりつつある。終章の「レゴと粘土」こそ本書の思想 — この思想を序盤に宣言し、主役は福田さん自身の「P」、フレームワークは脇役に。", { x: MX, y: 5.75, w: CW, h: 1.0, fontFace: GOTHIC, fontSize: 12, color: INK, lineSpacing: 18, isTextBox: true, margin: 0, fill: { color: SURFACE } });
}

/* ---------- 7. Issue 1 readers ---------- */
{
  const s = header(base(), "03 — ISSUE 1", "論点1：読者は誰か");
  const rows = [
    ["案", "読者像", "強み", "弱み"],
    ["a", "THE MODEL読者の「7年後」— 当時の実務層がいま部長・役員・社長に", "前作の読者基盤を引き継げる。悩みの変化（実行→設計）が本の主題と一致", "読者の高齢化とともに市場が狭まる"],
    ["b", "これから経営を担う人 — GM候補・次世代リーダー・経営者", "市場が広い。「体系的に経営を学ぶ場が日本にない」への回答になる", "経営書の棚は激戦区。続編の意味が弱まる"],
    ["c", "SaaS/IT業界の当事者", "具体性が最も活きる。講演・SNSの初速", "市場が最も狭い。「業界本」に見えると前作の業界外読者を失う"],
  ];
  const tableRows = rows.map((r, i) => r.map((c, j) => ({
    text: c,
    options: {
      bold: i === 0 || j === 0,
      color: i === 0 ? "FFFFFF" : (j === 0 ? BLUE : INK),
      fill: { color: i === 0 ? INK : PAPER },
      fontFace: GOTHIC, fontSize: i === 0 ? 11.5 : 11,
      align: j === 0 ? "center" : "left",
      valign: "middle",
    },
  })));
  s.addTable(tableRows, { x: MX, y: 2.0, w: CW, colW: [0.7, 4.7, 3.7, 2.83], border: { type: "solid", color: LINE, pt: 0.75 }, margin: 0.08, rowH: 0.75 });
  s.addShape(pres.ShapeType.rect, { x: MX, y: 5.6, w: CW, h: 1.15, fill: { color: BLUESOFT }, line: { color: BLUE, width: 1 } });
  s.addText([
    { text: "推し：a を主読者、b を拡張読者に。", options: { bold: true, color: BLUE } },
    { text: "「THE MODELで実行を学んだあなたが、今度は設計する側に回る番だ」という一本のメッセージで a→b が繋がる。帯・序章の語りかけの主語をここに固定したい。", options: { color: INK } },
  ], { x: MX + 0.3, y: 5.75, w: CW - 0.6, h: 0.85, fontFace: GOTHIC, fontSize: 12.5, lineSpacing: 19, isTextBox: true, margin: 0 });
}

/* ---------- 8. Issue 2 axes ---------- */
{
  const s = header(base(), "04 — ISSUE 2", "論点2：本の軸 — 3つの候補", "福田さんの「どういう軸で書くのがいいか迷っている」への選択肢");
  const items = [
    ["軸A", "続編軸", "「THE MODEL、その後」", "前作の誤解を解き、7年の変化（SaaS is Dead／AI）に答える。", "入口として最強。ただし軸にすると「答え合わせ本」で終わる。→ 1章に圧縮して入口に使う。", BLUE],
    ["軸B", "原理原則軸", "「福田版PRINCIPLES」", "判断に根拠を持つための蓄積を、エピソードとともに編む。終章が着地。", "本書のテーマそのもの。ただし並べるだけでは総花的。売り物ではあるが、背骨は別に必要。", BLUE],
    ["軸C", "フェーズ軸", "「現在地の地図」", "19社を横から見た発見＝フェーズの誤認が最大の失敗要因。フェーズごとに効く原則が変わる。", "最も新しく、最も福田さんにしか書けない主張。読者が現在地から本を引ける実用の背骨。", RED],
  ];
  const cw3 = (CW - 0.6) / 3;
  items.forEach((it, i) => {
    const x = MX + i * (cw3 + 0.3);
    s.addShape(pres.ShapeType.rect, { x, y: 2.15, w: cw3, h: 3.55, fill: { color: SURFACE }, line: { color: LINE, width: 0.75 } });
    pill(s, x + 0.25, y2 = 2.4, 0.95, it[0], it[5]);
    s.addText(it[1] + " — " + it[2], { x: x + 0.25, y: 2.85, w: cw3 - 0.5, h: 0.75, fontFace: MINCHO, fontSize: 15, bold: true, color: INK, lineSpacing: 20, isTextBox: true, margin: 0 });
    s.addText(it[3], { x: x + 0.25, y: 3.65, w: cw3 - 0.5, h: 0.95, fontFace: GOTHIC, fontSize: 10.5, color: SOFT, lineSpacing: 15.5, isTextBox: true, margin: 0 });
    s.addText(it[4], { x: x + 0.25, y: 4.6, w: cw3 - 0.5, h: 1.0, fontFace: GOTHIC, fontSize: 10.5, bold: false, color: INK, lineSpacing: 15.5, isTextBox: true, margin: 0 });
  });
  s.addShape(pres.ShapeType.rect, { x: MX, y: 5.95, w: CW, h: 0.95, fill: { color: BLUESOFT }, line: { color: BLUE, width: 1 } });
  s.addText([
    { text: "推し：Cを背骨に、Bを売り物に、Aは第1章へ圧縮。", options: { bold: true, color: BLUE } },
    { text: "一文で「会社のフェーズを見誤るな。フェーズごとに効く原理原則を、19社の実話で渡す」。前作＝分業という空間の地図、本作＝フェーズという時間の地図。", options: { color: INK } },
  ], { x: MX + 0.3, y: 6.08, w: CW - 0.6, h: 0.7, fontFace: GOTHIC, fontSize: 12, lineSpacing: 18, isTextBox: true, margin: 0 });
}

/* ---------- 9. Issue 3 structure ---------- */
{
  const s = header(base(), "05 — ISSUE 3", "論点3：伝える順番 — 構成2案の比較");
  const cw2 = (CW - 0.3) / 2;
  // 案1
  s.addShape(pres.ShapeType.rect, { x: MX, y: 2.0, w: cw2, h: 3.15, fill: { color: SURFACE }, line: { color: LINE, width: 0.75 } });
  pill(s, MX + 0.25, 2.22, 0.95, "案 1", INK);
  s.addText("続編ファースト型（現骨子の整流）", { x: MX + 0.25, y: 2.62, w: cw2 - 0.5, h: 0.4, fontFace: MINCHO, fontSize: 15.5, bold: true, color: INK, isTextBox: true, margin: 0 });
  s.addText("序章 → THE MODELアンサー → 横の視点と時間差 → GTM戦略の原則 → マネジメントシステム → フェーズ別原則 → 採用・リーダーシップ → 終章", { x: MX + 0.25, y: 3.1, w: cw2 - 0.5, h: 0.95, fontFace: GOTHIC, fontSize: 11, color: SOFT, lineSpacing: 16.5, isTextBox: true, margin: 0 });
  s.addText([
    { text: "○ 現ドラフトから距離が近く執筆負荷が小さい。前作読者の期待に素直\n", options: { color: BLUE } },
    { text: "× テーマ別の並びで「自分はどこを読めばいいか」が見えにくい。前半が過去の話で重い", options: { color: RED } },
  ], { x: MX + 0.25, y: 4.1, w: cw2 - 0.5, h: 0.95, fontFace: GOTHIC, fontSize: 11, lineSpacing: 16.5, isTextBox: true, margin: 0 });
  // 案2
  const x2 = MX + cw2 + 0.3;
  s.addShape(pres.ShapeType.rect, { x: x2, y: 2.0, w: cw2, h: 3.15, fill: { color: PAPER }, line: { color: RED, width: 1.25 } });
  pill(s, x2 + 0.25, 2.22, 0.95, "案 2", RED);
  s.addText("フェーズ背骨型（推し）", { x: x2 + 0.25, y: 2.62, w: cw2 - 0.5, h: 0.4, fontFace: MINCHO, fontSize: 15.5, bold: true, color: INK, isTextBox: true, margin: 0 });
  s.addText("序章 → THE MODELアンサー（圧縮）→ 横の視点と「フェーズ」の発見 → フェーズ別に原則を編む（各フェーズにGTM・システム・人を織り込む）→ 終章 自分のPRINCIPLE", { x: x2 + 0.25, y: 3.1, w: cw2 - 0.5, h: 0.95, fontFace: GOTHIC, fontSize: 11, color: SOFT, lineSpacing: 16.5, isTextBox: true, margin: 0 });
  s.addText([
    { text: "○ 読者が現在地から引ける。「地図→各エリアの原則→自分の原則」と体験が一直線\n", options: { color: BLUE } },
    { text: "× 横断テーマをフェーズに割り付ける再構成コストが大きい", options: { color: RED } },
  ], { x: x2 + 0.25, y: 4.1, w: cw2 - 0.5, h: 0.95, fontFace: GOTHIC, fontSize: 11, lineSpacing: 16.5, isTextBox: true, margin: 0 });
  // 折衷
  s.addShape(pres.ShapeType.rect, { x: MX, y: 5.4, w: CW, h: 1.4, fill: { color: BLUESOFT }, line: { color: BLUE, width: 1 } });
  s.addText([
    { text: "折衷（実務案）：二部構成。", options: { bold: true, color: BLUE } },
    { text: "第1部「地図」＝アンサー＋横の視点＋フェーズの発見。第2部「原則」＝GTM／マネジメントシステム／人・組織のテーマ章に、全原則へ「効くフェーズ」のタグを付ける。テーマ章の書きやすさとフェーズの引きやすさを両立、現ドラフトからの移行も現実的。当日はここを一番議論したい。", options: { color: INK } },
  ], { x: MX + 0.3, y: 5.55, w: CW - 0.6, h: 1.1, fontFace: GOTHIC, fontSize: 12, lineSpacing: 18.5, isTextBox: true, margin: 0 });
}

/* ---------- 10. Issue 4 product design ---------- */
{
  const s = header(base(), "06 — ISSUE 4", "論点4：見せ方 —「原則」をプロダクトとして設計する");
  const items = [
    ["原則の型化", "散在する「P」を〈言い切り1行＋なぜ＋実話1本＋読者への問い〉の定型に統一。全50〜70本を通し番号で管理し、巻末に原則インデックス（フェーズ×テーマ）。→ 持ち帰れる道具 その1"],
    ["ワークの本線化", "仮案の章末ワークを正式採用し、終章「自分のPRINCIPLEを作る」で回収する一冊通しの体験に。書き込んだ瞬間、本が「自分の原理原則ノート」になる。→ 道具 その2"],
    ["図版", "成長4パターン（A〜D）・フェーズ地図（STARS改）・時間差の構造は本書の顔になる図。前作の「あのスライド」級に磨く。2004年スライド等の一次資料は写真的に見せる"],
    ["引用の整理", "ワトキンス・ダリオ・ワイズマン・Playing to Win ほか引用多数。許諾要否の洗い出しを編集側で早期に実施（著者注にも【要確認】複数）。オリジナル原則との比率管理を兼ねる"],
    ["AI章の鮮度", "第1章後半のAI論は出版時点で必ず古びる。校了直前アップデート枠として設計し、構造（変わらない原則）と時事（変わる実行手段）を段落レベルで分離"],
  ];
  let y = 2.0;
  items.forEach(it => {
    s.addText(it[0], { x: MX, y, w: 2.5, h: 0.86, fill: { color: SURFACE }, fontFace: GOTHIC, fontSize: 12.5, bold: true, color: INK, valign: "middle", align: "center", isTextBox: true, margin: 0.05 });
    s.addText(it[1], { x: MX + 2.7, y, w: CW - 2.7, h: 0.86, fontFace: GOTHIC, fontSize: 11, color: INK, valign: "middle", lineSpacing: 15.5, isTextBox: true, margin: 0 });
    y += 0.98;
  });
}

/* ---------- 11. Title ---------- */
{
  const s = header(base(), "07 — TITLE", "タイトルの方向感", "今日決めず、「THEシリーズ英語一語で行くか」の方向感だけ合意できれば十分");
  const rows = [
    ["候補", "根拠・狙い", "論点"],
    ["THE PRINCIPLE", "序章の結び「自分にとってのPRINCIPLEを作ってほしい」と完全整合。THEシリーズの連続性。単数形＝あなた自身の一つの原理原則という渡し方", "ダリオ『PRINCIPLES』との距離感（本文で参照しており確信犯として扱えるか）。カタカナ読みの座り"],
    ["THE PRINCIPLES", "複数の原則集であることに忠実", "ダリオとほぼ同名。検索・書店で埋没"],
    ["THE MODEL 2", "続編認知が最速。現ドラフトの作業名", "「型の続き」を期待させ、本書の主張（型ではなく原則）と自己矛盾"],
    ["THE PHASE", "フェーズ背骨案に忠実。「現在地の地図」が一語で立つ", "原理原則というテーマ性が消える。語の強度が弱い"],
  ];
  const tableRows = rows.map((r, i) => r.map((c, j) => ({
    text: c,
    options: {
      bold: i === 0 || j === 0,
      color: i === 0 ? "FFFFFF" : (i === 1 && j === 0 ? RED : INK),
      fill: { color: i === 0 ? INK : (i === 1 ? REDSOFT : PAPER) },
      fontFace: j === 0 && i > 0 ? "Arial" : GOTHIC, fontSize: i === 0 ? 11.5 : 10.5,
      valign: "middle",
    },
  })));
  s.addTable(tableRows, { x: MX, y: 2.15, w: CW, colW: [2.3, 5.2, 4.43], border: { type: "solid", color: LINE, pt: 0.75 }, margin: 0.08, rowH: 0.7 });
  s.addText("推し：『THE PRINCIPLE』＋日本語サブタイトルで実利を補う（例：「なぜあの会社は、同じ壁にぶつかるのか」「フェーズで読み解く経営の原理原則」）", { x: MX, y: 6.15, w: CW, h: 0.6, fontFace: GOTHIC, fontSize: 12, bold: true, color: BLUE, isTextBox: true, margin: 0 });
}

/* ---------- 12. Risks ---------- */
{
  const s = header(base(), "08 — RISKS", "正直な懸念（先に自分たちで挙げておく）");
  const rows = [
    ["懸念", "中身", "打ち手"],
    ["続編の宿命", "前作比で必ず評価される。「型」ほどのキャッチーさが原理原則にはない", "持ち帰れる道具（原則インデックス・ワーク）を型の代替に。帯は「答え」ではなく「地図」を約束"],
    ["外資IT特化の狭さ", "n=19の具体は強いが読者母数は狭い。「業界回顧録」に見えたら負け", "無理に汎用化せず、結論だけ汎用化（骨子の方針通り）。章末ワークが読み替え装置として機能するか編集で検証"],
    ["引用密度", "他者フレームワーク中心に見えると前作の反省と矛盾。許諾実務も重い", "主役を福田さんの「P」に。引用は出典明記の脇役へ。許諾リストを編集側で即作成"],
    ["AI章の陳腐化", "出版まで1年前後と想定するとAI記述は確実に古びる", "校了直前アップデート枠＋「変わらないもの」中心の記述に寄せる"],
    ["「関心ある人いるのかな」問題", "前作でも途中経過で陥った不安（福田さんメール）", "執筆と並行してAIdiver等で一部を連載・講演化し、読者反応を先に取る。言葉の独り歩き対策も編集が設計"],
  ];
  const tableRows = rows.map((r, i) => r.map((c, j) => ({
    text: c,
    options: {
      bold: i === 0 || j === 0,
      color: i === 0 ? "FFFFFF" : INK,
      fill: { color: i === 0 ? INK : (j === 0 ? SURFACE : PAPER) },
      fontFace: GOTHIC, fontSize: i === 0 ? 11.5 : 10.5,
      valign: "middle",
    },
  })));
  s.addTable(tableRows, { x: MX, y: 2.0, w: CW, colW: [2.6, 4.6, 4.73], border: { type: "solid", color: LINE, pt: 0.75 }, margin: 0.08, rowH: 0.78 });
}

/* ---------- 13. Next ---------- */
{
  const s = header(base(), "09 — NEXT", "進め方（案）");
  const items = [
    ["本日", "軸・読者・構成方針・タイトル方向感の合意。宿題の切り分け"],
    ["〜9月中旬", "編集部：合意した軸で章構成表（原則の割付マトリクス付き）を作成 → 福田さんレビュー"],
    ["9月下旬〜", "福田さん：確定構成で第1稿の執筆開始（完成度の高い終章・フェーズ章から着手する案）。編集部：引用許諾リスト・図版ラフ・ワーク設計"],
    ["執筆中", "章単位のレビューサイクル（章ごとに壁打ち。全部書いてから、にしない）。連載・講演での先行検証を並走"],
    ["校了前", "AI関連記述の最終アップデート。タイトル・帯の最終決定"],
  ];
  let y = 2.05;
  items.forEach((it, i) => {
    s.addText(it[0], { x: MX, y, w: 1.9, h: 0.76, fontFace: "Arial", fontSize: 13, bold: true, color: BLUE, valign: "middle", isTextBox: true, margin: 0 });
    s.addShape(pres.ShapeType.line, { x: MX + 2.0, y: y + 0.05, w: 0, h: 0.66, line: { color: LINE, width: 1 } });
    s.addText(it[1], { x: MX + 2.25, y, w: CW - 2.25, h: 0.76, fontFace: GOTHIC, fontSize: 12.5, color: INK, valign: "middle", lineSpacing: 17, isTextBox: true, margin: 0 });
    y += 0.9;
  });
  s.addText("編集体制：押久保剛（統括）＋大久保（編集担当：丸井さん・川上さん書籍の担当編集）", { x: MX, y: y + 0.15, w: CW, h: 0.4, fontFace: GOTHIC, fontSize: 11.5, color: SOFT, isTextBox: true, margin: 0 });
}

pres.writeFile({ fileName: "C:/Users/020168/Documents/Claude/oshikubo_office/workplace/projects/the-model2-principle/THE_PRINCIPLE_方向性たたき_v1.pptx" }).then(() => console.log("done"));
