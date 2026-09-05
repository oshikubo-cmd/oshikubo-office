---
name: intra-post
description: 翔泳社イントラ（intra.aidiver.jp / markezine / enterprisezine / codezine / bizzine）への記事入稿スキル。「イントラに入稿して」「イントラに登録して」「id◯◯◯に入れて」「この記事をイントラに投稿」「CMSに登録」など、記事原稿・完成HTMLをイントラ（記事管理システム）へ登録・更新する依頼が来たら必ずこのスキルを使う。新規記事の作成と、既存記事ID への上書き更新（--update）の両方に対応。
---

# イントラ入稿スキル（intra-post）

翔泳社の記事管理イントラへ、記事（メタ情報＋本文＋画像）を半自動入稿する。
実体は社内エンジニア提供の Python ツール `article_poster`（mz_poster）を操作する。

## 設定（環境ごとに1回だけ確認）

- ツールの場所: `C:\Users\020168\Documents\oshikubo_storage\02_社内資料・データ\article_poster`
  （※他の人のPCでは各自の配置場所に読み替える。以下「ツールルート」）
- 前提: Python 3.10+、`pip install -r requirements.txt` 済み、`--setup-login` でログイン登録済み
  （未登録なら本人に PowerShell で `python -m mz_poster.main --setup-login` を実行してもらう。
  パスワード対話入力のため Claude は代理実行できない）

## 対応サイトと切り替え

サイトは環境変数 `MZ_POSTER_BASE_URL` で指定する（settings.ini は書き換えない）。
Cookie はサイトごとに `cookie_<ホスト名>.txt` へ自動分離される。ログイン情報は全サイト共通（shoeisha.jp SSO）。

| 媒体 | MZ_POSTER_BASE_URL | チャンネルタイプ欄 |
|---|---|---|
| AIdiver | https://intra.aidiver.jp | なし |
| MarkeZine | https://intra.markezine.jp | MarkeZine / CommerceZine / SalesZine |
| EnterpriseZine | https://intra.enterprisezine.jp | DBオンライン / セキュリティオンライン / エンタープライズジン / 財務・会計Online |
| CodeZine | https://intra.codezine.jp | CodeZine / DeveloperZine / ProductZine |
| Bizzine | https://intra.bizzine.jp | なし |

チャンネルタイプ欄があるサイトでは、新規作成時に article.md のメタデータ
`- チャンネルタイプ：◯◯` が必須（更新時は省略すれば既存値維持）。

## 手順

### 1. 依頼内容の確認

- 対象サイト（不明なら記事の媒体から判断。迷ったらユーザーに確認）
- **新規作成か、既存記事IDへの上書き更新か**（「id668に入れて」→ 更新。IDの言及がなければ確認する）
- 素材の場所（完成HTML／Markdown原稿／画像フォルダ）

### 2. 入稿フォルダの準備

ツールルートの `articles/<スラッグ>/` を作り、以下を配置する。

**完成HTMLがある場合（推奨・セミナーレポートスキルの出力など）:**
- `article.html` — 本文HTMLのみ。冒頭に `<!-- ■CMS入力欄 … -->` コメントブロックがあれば**除去**する
  （タイトル・サブタイトル・リードはそこから article.md へ転記する）
- `article.md` — **上書きしたいメタだけ**を書く。書式:

```
## メタデータ
- サブタイトル：◯◯（あれば）

## タイトル
記事タイトル

## 概要
　リード文（先頭は全角スペース）
```

新規作成の場合はさらに `- 記事タイプ：記事` `- 公開ステータス：準備中` `- 公開日：YYYY/MM/DD HH:MM～` `- 担当者：◯◯`（＋チャンネルタイプ欄のあるサイトでは `- チャンネルタイプ：◯◯`）と `## 著者`（`- 名前 [著] (著者ID)`）が必要。

**Markdown原稿しかない場合:** `article.md` の `## 内容` に本文を書く（`---` でページ分割、`![alt](file)` ＋次行 `> キャプション` で図版）。

**画像:**
- 本文で参照する画像のみコピー（コメントアウト中の予備図版はコピーしない）
- 一覧サムネは `*_arena.jpg`（400×300）
- OGP画像は **`*_fb.jpg` にリネーム必須**（例: `id668_OGP.jpg` → `id668_fb.jpg`、1200×630）

### 3. ドライ実行（必須）

```
cd <ツールルート>
MZ_POSTER_BASE_URL=<対象サイトURL> PYTHONIOENCODING=utf-8 python -m mz_poster.main articles/<スラッグ>            # 新規
MZ_POSTER_BASE_URL=<対象サイトURL> PYTHONIOENCODING=utf-8 python -m mz_poster.main articles/<スラッグ> --update <記事ID>  # 更新
```

- ペイロード（タイトル・メタ・本文文字数・画像スロット）をユーザーに提示する
- **更新時の重要仕様**: article.md に書いていない項目（公開ステータス・著者・タグ・公開日・コーナー等）は
  イントラ上の現在値がそのまま維持される。更新前に現在値を取得し「差し替える項目／維持される項目」を分けて見せること
- select値の不一致エラーが出たら `python -m mz_poster.capture_reference` でそのサイトの実選択肢を取得して合わせる

### 4. 実行（ユーザーの明示OKが必須）

**イントラは本番システム。ユーザーの明示的なOKなしに `--execute` してはならない。**

```
MZ_POSTER_BASE_URL=<対象サイトURL> PYTHONIOENCODING=utf-8 python -m mz_poster.main articles/<スラッグ> [--update <記事ID>] --execute
```

処理順: 記事作成（新規のみ）→ 画像アップロード → arena/OGPスロット割当 → 本文保存（最後）。

### 5. 反映検証

実行後、記事編集ページを取得して確認する（BeautifulSoupのtextarea解析はタグが落ちるため、**生HTMLをregexで**確認する）:
- タイトル・サブタイトル・概要が想定どおりか
- 本文の文字数と `<div id="p1">`〜ページ数、画像パス（`/static/images/article/<ID>/…`）
- スロット: `name="summary_thumbnail_200"` / `name="portal_image"` の radio が対象ファイル名で checked か
- 更新時: 維持すべき項目（ステータス・著者・タグ）が無傷か

### 6. 報告

記事URL（`https://<ホスト>/intra/article/detail/<ID>`）と反映内容・維持項目を報告し、
オフィスのルールに従いチケットを完了させる。

## 注意・既知の落とし穴

- **更新（--update）はメタのみの変更でも本文を毎回再保存する**。イントラ上で直接編集された本文を上書きする事故が起きた（2026-09-01、id667）。更新実行前に必ず現行本文をGET（/intra/article/detail/{id} の body_formatted）してローカルにバックアップし、手元版との差分を確認。差分があれば取り込むかユーザーに確認してからpushする

- ログイン失敗時は `MZ_POSTER_DEBUG=1` を付けて観測し、応答HTML内のエラーメッセージ（「Eメールアドレスかパスワードが間違っています」等）を確認する
- 資格情報が誤っている場合は本人に `--setup-login` の再実行を依頼（上書き登録される）
- 社内ネットワークはALSI社のCAでTLS中継されるが、truststore組み込み済みのため対応不要（エラーが出たら `pip install truststore`）
- 複製で事前作成された記事IDは本文・概要に複製元の残骸が入っていることがある。更新時は必ず上書き対象に含める
- 新規投稿は実行のたびに新しい記事を作る。誤って重複作成した場合は削除できないため、公開ステータスを「ボツ」に変更する運用
- **短時間の連続アクセスに注意**: イントラのnginx/WAFはレート制限があり、複数サイトへの連続ログインや検証GETの連打で一時的に403ブロックされることがある（2026-08-28に発生）。検証は必要最小限にし、403が全ページで返り始めたら数分〜数十分待って再試行する。ブロック中に再ログインを繰り返さない
