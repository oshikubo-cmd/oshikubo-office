# イントラ記事投稿スクリプト（article_poster）試験運用

- ID: 2026-08-27_intra-poster-automation-trial
- 優先度: 中
- ステータス: in_progress
- 担当者: claude（メイン、ドメイン1: 部門経営・AIネイティブ推進）
- 作成日: 2026-08-27
- 概要: 社内エンジニア提供の記事投稿スクリプト（article_poster、旧zip）を使い、イントラ（MarkeZine intra staging）への記事登録を自動化するトライアル。素材はMutureセミナーレポート（axd-s7-muture-seminar-report）を使用。

## 要件

- 投稿先はテストサイト（https://intra.staging.markezine.jp）。本番には投稿しない
- Muture初稿v2（3ページ構成）を article.md 形式に変換し、dry-run で内容確認
- 実投稿（--execute）はユーザーの明示OK後のみ
- 初回ログイン設定（--setup-login）は対話入力のためユーザー自身がPowerShellで実行

## タスクリスト

- [x] プロジェクト構成の把握（README / CLAUDE.md / settings.ini）
- [x] pip install -r requirements.txt（keyring等を追加導入。requests/bs4/lxmlは導入済みだった）
- [x] articles/muture-test/ を作成（article.md + 画像10点。OGPは id669_fb.jpg にリネームしてスロット判定に対応）
- [x] dry-run で変換結果を確認（3ページ・H2×6・本文画像8・arena/external判定OK）
- [ ] ユーザーに --setup-login を依頼（対話入力のため代理実行不可。← いまここ）
- [ ] staging へ --execute（ログイン設定後）

## メモ

- 図版は初稿v2の6枚構成（◎: zu01/03/04/05/07/09）＋人物写真2枚（id669_01_2, id669_02_1）を採用。（○）付き3枚は3P構成のため除外
- メタ: 記事タイプ=テスト投稿 / チャンネル=MarkeZine / 公開ステータス=準備中 / 公開日=2026/09/01（stagingテスト用の仮値）
- 「大企業組織変革支援のレシピ」の[要確認]URLはリンクなしのテキストのまま（テスト投稿のため）

## 対象

- スクリプト: C:\Users\020168\Documents\oshikubo_storage\02_社内資料・データ\article_poster
- 素材: workplace/projects/axd-s7-muture-seminar-report/（初稿v2_3P.md + images/）

## 完了記録

- 最終ステータス: completed
- 完了日: 2026-08-28
- 実施内容:
  - article_poster（社内エンジニア提供）の環境構築（keyring等の追加インストール）
  - Muture初稿v2（3P構成）をmz_poster記法のarticle.mdへ変換、画像10点を配置
  - dry-runで変換確認 → staging（intra.staging.markezine.jp）へ--execute
  - 記事作成・画像10点アップロード・アリーナ/OGPスロット割当・本文再保存まで全ステップ成功
- 成果物: staging記事ID 74008（https://intra.staging.markezine.jp/intra/article/detail/74008）、articles/muture-test/（article.md＋画像）
- 発生した問題と対処:
  - 初回setup-loginでパスワード誤入力→自動ログイン失敗。診断スクリプトでサーバー応答を観測し「Eメールアドレスかパスワードが間違っています」を特定→ユーザーが再登録して解決
  - Git Bash経由の実行はcp932で文字化け→PYTHONIOENCODING=utf-8で解消
- [INSIGHT] OGP画像はツールの命名規則に合わせ `*_fb.jpg` へリネームが必要（例: id669_OGP.jpg → id669_fb.jpg）。アリーナは `*_arena` でそのまま判定される
- [INSIGHT] ログインはshoeisha.jp共通SSO経由。認証失敗時はMZ_POSTER_DEBUG=1で観測し、応答HTML中のエラーメッセージを見ると原因を特定できる
- [INSIGHT] 投稿は毎回「新規記事」を作る。staging記事タイプ=テスト投稿/ステータス=準備中が安全。本番投稿は未検証（settings.iniのbase_url切替が必要）
