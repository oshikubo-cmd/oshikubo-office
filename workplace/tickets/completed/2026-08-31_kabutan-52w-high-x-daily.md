# 新高値トップ10 × X話題ポスト デイリー通知の構築

- ID: 2026-08-31_kabutan-52w-high-x-daily
- 優先度: 中
- ステータス: completed
- 担当者: analyst
- 作成日: 2026-08-31
- 完了日: 2026-08-31

## 概要

株探「本日、52週高値を更新した銘柄」（前日比率降順）のトップ10について、
Xで話題になっている投稿をピックアップし、平日18時にSlack自分宛DMで通知する仕組みを構築した。

## 実施内容

- 株探ページ（`col=zenhiritsu`）から前日比率トップ10を抽出するJSスニペットを作成
- X投稿の取得経路を検証・確定（後述）
- 2026-08-31 分でテスト実行し、10銘柄ぶんの話題投稿を収集してDM送信
- プロジェクト文書（README / snippets / log）を作成
- スケジュールタスク `kabutan-52w-high-x-daily`（cron `0 18 * * 1-5`）を登録

## 成果物

- `workplace/projects/kabutan-52w-high-x-watch/README.md` — 仕組み・制約・クエリの作り方
- `workplace/projects/kabutan-52w-high-x-watch/snippets.md` — ブラウザ実行JS 2本
- `workplace/projects/kabutan-52w-high-x-watch/log.md` — 実行ログ
- `C:\Users\020168\.claude\scheduled-tasks\kabutan-52w-high-x-daily\SKILL.md` — タスク本体
- テストDM: https://shoeisha-co.slack.com/archives/DN3ERSWDD/p1788186446810019

## 発生した問題と対処

1. **X本体の検索が使えない** — `x.com/search` は未ログインだとログイン画面にリダイレクトされる。
   Yahoo!リアルタイム検索（`search.yahoo.co.jp/realtime/search?p=...`）に切り替えて解決。
   ログイン不要で、本文・投稿者・RT/いいね数・投稿時刻つきで直近40件が取れる。
2. **一般名詞と同名の銘柄でノイズ大量混入** — 「ヴィッツ」でトヨタ車・ミニカー・アニメキャラの投稿が混入（41件中28件がノイズ）。
   株式文脈キーワードの正規表現フィルタをスニペットに組み込んで13件に絞った。
3. **エンゲージメント上位が煽り・アフィリアカウントに偏る** — 除外はせず、話題度の指標としては採用しつつ
   「どれが事実ベースの材料か」をDM末尾に明示する運用にした。

## 再利用可能な学び

- `[INSIGHT]` **Xの投稿をログインなしで拾うなら Yahoo!リアルタイム検索が唯一の実用解。**
  `search.yahoo.co.jp/realtime/search?p=<query>` を navigate すれば、CSS Modules のクラス
  （`[class*="Tweet_TweetContainer"]` / `Tweet_body__` / `Tweet_action` / `Tweet_time`）から
  本文・RT・いいね・投稿時刻・投稿URLが構造的に取れる。人気順ソートはないので自前で並べる。
  syndication API（cdn.syndication.twimg.com）は個別ツイートID指定の全文取得専用で、検索には使えない。
- `[INSIGHT]` **銘柄名クエリは `<正式名称> OR <コード>` が定石。** 株探の銘柄名は略称なので単体だと取りこぼす。
  コードをORで足しておけば株クラの投稿は確実に拾える。
- `[INSIGHT]` **一般名詞と同名の銘柄には株式文脈フィルタが必須。** フィルタ後の件数がそのまま
  「その銘柄がXでどれだけ話題か」の指標になり、件数が少ないこと自体が有用な情報になる。
