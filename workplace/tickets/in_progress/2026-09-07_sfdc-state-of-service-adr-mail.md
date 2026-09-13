# SFDC「State of Service」AIエージェント関連 タイアップ単独メール作成

- ID: 2026-09-07_sfdc-state-of-service-adr-mail
- 優先度: 高
- ステータス: in_progress
- 担当者: writer
- 作成日: 2026-09-07
- 概要: セールスフォース・ジャパンのコンテンツ（State of Service / AIエージェント）への送客を目的とした、AIdiver配信のタイアップ単独メールTEXT原稿を作成する

## 要件

- 配信先: AIdiver
- 飛ばし先URL: https://www.salesforce.com/jp/service/resources/state-of-service-ai-agents/?d=701ed00001Yo61JAAR&nc=701ed00001YnszHAAR&utm_source=shoeisha&utm_medium=tp_email&utm_campaign=jp-svclobaw&utm_content=all-ebook-701ed00001Yo61JAAR
- 目的: セミナー申し込みへの誘導
- 参考資料URL: https://www.salesforce.com/jp/service/resources/state-of-service-ai-agents-edition/
- フォーマット: writer-adr_mail スキル定型（タイトル35字以内・本文100行以内）
- ファイル名規定: YYMMDD_ADR_<クライアント名>単独メール.txt → 260907_ADR_SFDC単独メール.txt

## 前提メモ（前回案件からの引き継ぎ）

- タイトルはクライアント製品推し（SFDC案件の製品名を主役に）
- 所属・肩書きは半角スペース区切り、35字以内なら1行化
- salesforce.com のLPはWebFetch 403 / Shadow DOM構造 → ブラウザ＋再帰JSで抽出

## タスクリスト

- [x] チケット作成
- [ ] LP・資料ページの情報収集
- [ ] 送客先の性質確認（セミナー/ウェビナー/eBook）
- [ ] タイトル3案作成
- [ ] 本文執筆
- [ ] 表記チェック
- [ ] 保存・報告

## 進捗（2026-09-07）

- [x] LP・資料ページの情報収集（Shadow DOM再帰JSで抽出。WebFetchは403）
- [x] 送客先の性質確認 → **セミナーではなく調査レポート（eBook）のフォーム登録ダウンロード**。LPのCTAは「調査レポートを読む」
- [x] タイトル3案作成（27.0 / 28.0 / 28.5字）
- [x] 本文執筆（81行・URL3箇所）
- [x] 表記チェック（35字超なし、「——」なし、「」。なし、[要確認]なし）
- [x] 保存

## 成果物

- `oshikubo_storage/03_AIdiver関連/単独メール案件/260907_ADR_SFDC単独メール.txt`

## 依頼内容との相違（要判断）

- 依頼の目的は「セミナー申し込みへの誘導」だったが、指定LPは調査レポートのダウンロード（ゲート付きeBook）。
  セミナー要素はLP・資料ページのいずれにも存在しないため、**レポートDL誘導**として執筆した。
  セミナー送客が必要な場合は別途セミナーLPの支給が必要。

## 使用した一次情報（LP／資料ページ）

- レポート名: 『カスタマーサービス最新事情』特別版　AIエージェントエディション（全4章）
- 調査: 2026年3月9日～4月4日、5地域13か国、サービス担当者3,075人、ダブルブラインド方式。日本はN=300
- 主要データ: エージェント型AI導入率39％→66％（1年）／導入組織の70％が60日以内に価値実感／
  AI関与のケース解決40％が自律完結／83％が5チャネル以上に展開／最も向上したKPIは顧客満足度／
  AI利用担当者の88％がツール切替時間短縮／オペレーション担当72％がデータ準備を課題／
  担当者70％がデータプライバシー懸念でAI導入が遅延・制限／顧客対応AI導入企業の77％が人間へ切替可能
