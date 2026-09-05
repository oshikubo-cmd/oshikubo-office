# SFDC（Slack）ウェビナー タイアップ単独メール作成

- ID: 2026-09-02_sfdc-slack-webinar-adr-mail
- 優先度: 高
- ステータス: completed
- 完了日: 2026-09-02
- 担当者: writer
- 作成日: 2026-09-02
- 概要: セールスフォース（Slack）のウェビナー「AI時代の仕事はSlackで動く」への送客を目的とした、AIdiver配信のタイアップ単独メールTEXT原稿を作成する

## 要件

- 配信先: AIdiver
- 飛ばし先URL: https://www.salesforce.com/jp/slack/resources/jp-work-in-the-ai-era-with-slack/?d=701ed00001Y9HDfAAN&nc=701ed00001Y9HaFAAV
- 目的: セミナー申し込みへの誘導
- 素材: oshikubo_storage/03_AIdiver関連/単独メール案件/SFDC/SFDC_20260723 Webinar - AI時代の仕事はSlackで動く 〜 いまSlackとつなぐべきAI・業務アプリ徹底解説 〜.pdf
- フォーマット: writer-adr_mail スキル定型（タイトル35字以内・本文100行以内）

## タスクリスト

- [x] チケット作成
- [x] 素材PDF・LPの情報収集
- [x] タイトル3案作成
- [x] 本文執筆
- [x] 表記チェック
- [x] 保存・報告

## 実施内容・成果物

- 成果物: `oshikubo_storage/03_AIdiver関連/単独メール案件/SFDC/260902_ADR_SFDC単独メール.txt`
- タイトル3案（A:内容フック25.5字 / B:時代変化フック31字 / C:登壇者フック26.5字）、本文78行（規定100行以内）、URL3箇所
- 情報源: イベントLP（Shadow DOM経由で全文取得）＋ウェビナー資料PDF（72p）

## 発生した問題と対処

- LPがWebFetch 403 → ブラウザで開き、Shadow DOMを再帰走査するJSで本文抽出
- PDFはページレンダリング不可 → PyMuPDF fitz.get_text()でテキスト抽出

## 残課題（[要確認]）

- 参加費: LPに明記なし。「無料（フォーム登録制）[要確認]」とした。クライアント（SFDC担当者）に確認要

## 再利用可能な学び

- [INSIGHT] オンデマンド配信案件の開催概要は「形式：オンデマンド配信＋ライブ配信日の注記」形式。CTAは「視聴のお申し込みはこちら」
- [INSIGHT] salesforce.comのLPはShadow DOM構造。writerメモリraw.mdに抽出手順を記録済み

## 確定情報（2026-09-03追記）

- タイトル確定: 「Slack×Google・Claude・Notion連携をデモ解説　鍵はAIコンテキスト」（31.5字）
- 押久保FBを反映: タイトルはクライアント製品（Slack）推し＋AIコンテキスト強調＋デモ明示＋連携ツール名明示
- 最終ファイル: `oshikubo_storage/03_AIdiver関連/単独メール案件/SFDC/260903_ADR_SFDC単独メール.txt`（本文79行・URL3箇所）
- 残課題: 参加費[要確認]（無料想定、クライアント確認待ち）
- 2026-09-03 参加費の[要確認]を解消（押久保確認: 無料でOK）。残課題なし
- 2026-09-03 開催概要のサブタイトル行に破損を発見（末尾「〜」が「空」化・波ダッシュ揺れ）→ LP表記どおりに修正済み
