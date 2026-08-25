# 新規取引先登録の スプレッドシート→kintone 自動連携

- ID: 2026-08-07_kintone-supplier-auto-registration
- 優先度: 中
- ステータス: unstarted
- 担当者: analyst（自動化・データ連携）
- 作成日: 2026-08-07
- 依頼者: 押久保さん

## 概要

新規取引先登録の運用が「Googleフォーム → スプレッドシート → kintone（アプリ294）へ手動コピペ」となっており、手作業を排除したい。

- 入力元フォーム: https://docs.google.com/forms/d/e/1FAIpQLSdwZ99DuGrF1IGkSDafyI6SJ19JTzAmAc33BehBUfo4Z445AQ/viewform
  - タイトル: 取引先登録フォーム（個人情報同意 / インボイス登録番号 / 取引先区分 ほか複数セクション）
- 連携先: kintone アプリ294（https://shoeisha.cybozu.com/k/294/）

## 推奨方式（案A）

スプレッドシートに紐づけた Google Apps Script（GAS）で、フォーム送信トリガー（onFormSubmit）から kintone REST API（record.json）へレコード自動登録。追加費用ゼロ。

## 必要なもの

1. kintone アプリ294 の APIトークン（レコード追加権限付き）— アプリ設定 > API トークンで発行
2. アプリ294 のフィールドコード一覧（フォーム設問との対応表を作る）
3. shoeisha.cybozu.com のアクセス制限確認（IP制限があるとGASからのAPIが弾かれる）

## タスクリスト

- [ ] kintoneアプリ294のフィールドコードを取得
- [ ] フォーム設問 ↔ kintoneフィールドの対応表を作成
- [ ] GASスクリプト作成（onFormSubmit → kintone record.json POST）
- [ ] APIトークンをスクリプトプロパティに設定（ハードコード禁止）
- [ ] テスト送信で動作確認（テストレコードは確認後削除）
- [ ] 過去分の未転記データがあれば一括投入するか確認

## 代替案

- 案B: ノーコード連携（Yoom / Make / Zapier）— 月額コストあり、保守は楽
- 案C: フォーム自体をトヨクモFormBridgeに置換 — kintone直結でスプシ不要になるが有料＆フォームURL変更が必要
