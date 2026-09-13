# OpenAI 水嶋ディノ氏 動画出演依頼（AIdiver / Inside AIdiver）

- ID: 2026-09-11_openai-mizushima-video-request
- 優先度: 高
- ステータス: in_progress
- 担当者: video-director（押久保レビュー前提）
- 作成日: 2026-09-11
- 概要: OpenAI Japan 水嶋ディノ氏（GTMパートナーシップ責任者）へのAIdiver動画インタビュー出演依頼書を作成する。テーマ案「OpenAIが描く人とAIの協働」。MarkeZine向け講演資料（2026-09-07最終版）をベースに、GPT-6 Astraにフォーカスした内容とする

## インプット

- 講演資料: C:\Users\020168\Downloads\最新版OpenAI_MarkeZine_2026_20260907_最終版_高画質.pptx（21枚・読み上げスクリプト付き）
- 既存対談: workplace/projects/mzday-mizushima-talk-session/質問案_v1.md（MarkeZine Day 2026 Autumn 9/8 実施済み）
- 依頼書の前例: oshikubo_storage/01_進行中/動画_NVIDIA/【取材依頼書_質問あり】NVIDIA井﨑様_AIdiver.docx

## 前提・制約

- 読者層がMZ Day（マーケター）と異なる。AIdiverはCAIO/CDO/CIOクラスの意思決定層 → 経営アジェンダに寄せる
- 9/8対談で消費済みの論点（中の人の使い方／データ→コンテキスト／任せる範囲／世界観）は、そのまま反復しない
- NG: 競合比較（Anthropic・Google等の評価を問う）、炎上系時事ネタ、価格政策への直接の突っ込み、技術詳説
- 水嶋氏は技術者ではなくGTM側。「渦中にいる中の人」としての実感を引き出す
- GPT-6 Astraの事実関係は講演資料が唯一の出典。送付前に一次情報での裏取りが必要

## タスクリスト

- [x] 講演資料の全文抽出（本文＋読み上げスクリプト）
- [x] 既存対談の論点・NG整理
- [x] 依頼書フォーマットの確認（NVIDIA前例）
- [x] 動画企画書の作成
- [x] 出演依頼書（docx）の作成
- [ ] 押久保レビュー

## 成果物

- workplace/projects/openai-mizushima-video/企画書.md
- workplace/projects/openai-mizushima-video/【取材依頼書】OpenAI水嶋様_AIdiver.docx

## 進捗（2026-09-11）

ドラフト完成。押久保レビュー待ち。

### 実施内容

- 講演資料21枚を全文抽出（本文＋読み上げスクリプト）。GPT-6 Astra はSlide 2、AGI使命はSlide 3、対談構成はSlide 21
- 9/8 MZ Day対談の質問案と照合し、反復論点（中の人の使い方／データ→コンテキスト／任せる範囲／世界観）を特定。本動画では「組織の設計・意思決定」レイヤーに高度を上げて回避
- 依頼書は aidiver-interview-request スキルの書式関数・固定法務文言を再利用し、動画版（NVIDIA井﨑様前例）のセクション順で生成

### 未確定・要確認

- 撮影希望時期「2026年10月〜11月中」は仮置き。押久保の稼働で確定が必要
- GPT-6 Astra を含む資料由来の数値・固有名詞は一次情報未裏取り。送付前にファクトチェック必須（企画書に一覧）

## 更新（2026-09-11 その2）

押久保判断により「B案：原文を確認して英語の公式文言に差し替える」を採用。裏取りを実施し依頼書を差し替えた。

### 確定した一次情報

- GPT-6 Astra 発表日: 2026年9月3日（限定提供）／9月4日（一般提供）
- 公式メッセージ: **"Anything you can do on a computer, Astra can do for you. Fast."**
- 出典: OpenAI Developer Community 公式Announcements（タイトル直下の冒頭文）
  https://community.openai.com/t/introducing-gpt-6-astra-the-most-intelligent-and-aligned-model-in-the-world/1394703
- 講演資料スライド2の発表者ノートにあった日本語は、この忠実な訳と確認。水嶋氏の意訳ではないため「御社はこのメッセージを掲げられました」という帰属は正確
- 注: openai.com/index/ の公式ブログは403で直接取得不可。上記公式投稿＋CNBC・Fortune・Al Jazeera で日付・文脈を突き合わせ済み

### 依頼書の変更点

- ●取材趣旨: 「2026年9月3日に発表されたGPT-6 Astraです。「Anything you can do on a computer, Astra can do for you. Fast.」というメッセージのとおり」に差し替え
- ●質問項目 第1問: 英語原文＋日本語訳を併記し、「2026年9月3日のGPT-6 Astraの発表に際して」と日付を明示

### 残りのファクトチェック（未実施）

講演資料由来の以下は未裏取りのまま。送付自体には影響しないが、動画収録前に確認する。

- ChatGPT 週間アクティブユーザー 10億人超（2026年8月）※依頼書の質問2で引用
- OpenAI製品利用企業 200万社超・前年比2倍（2026年8月13日発表）※依頼書の質問2で引用
- ChatGPT広告 年換算売上10億ドル・40カ国・数千社（2026年8月31日発表）
- ChatGPTの音声機能 週間1.5億人超（2026年7月8日公表）
- 企業顧客のマーケティング職におけるCodex週間利用者 26倍（2026年8月12日 Enterprise Signals）

## 更新（2026-09-11 その3）押久保フィードバック反映

1. Astraの引用は日本語に戻す（英語併記はやめる）。※裏取りの結果、講演資料の日本語は公式文言の忠実訳と確認済みのため、日本語のまま引用しても帰属は正確。発表日「2026年9月3日」のみ裏取り成果として本文に残した
2. 取材希望日時: 2026年9月下旬〜11月中旬（仮置きを解消）
3. 取材趣旨を約半分に圧縮（5段落→4段落、冗長な説明を削除）
4. 「本企画で扱いたいのは」→「本企画でフォーカスしたいのは」

### [INSIGHT] 生成スクリプトの日本語編集はBashヒアドキュメント経由で行わない

build_video_req.py の文字列置換をBashヒアドキュメント内のPythonで行ったところ、
波ダッシュ（U+301C）が転送時に化けてマッチに失敗した。日本語を含むスクリプトの編集は
Write/Editツールでファイルごと書き直すこと。
