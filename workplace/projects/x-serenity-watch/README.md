# X @aleabitoreddit 日本株ウォッチ

X アカウント **Serenity（@aleabitoreddit）** が日本企業・日本株に言及したときに検知し、
Slack の自分宛DMに通知する監視の仕組み。

## 対象アカウント

- ハンドル: @aleabitoreddit（表示名 Serenity、認証済み）
- 内容: AI / 半導体サプライチェーンのリサーチ
- フォロワー: 102.3万（2026-08-30時点）／投稿 7,452件／2025年7月開設
- プロフィール記載: 「NFA DYOR, no paid promos; may trade/hold names disc, views my own. Not Investment Advice」
- 別アカウント: Serenity Research（@SerenityRSH）を運営

## 運用仕様

| 項目 | 内容 |
|---|---|
| 頻度 | 1日2回（07:53 / 18:53） |
| 通知先 | Slack 自分宛DM（channel_id = `UMNRD48V8`） |
| 検出範囲 | 日本企業への言及すべて（銘柄コード・$ティッカー・社名・Japan文脈） |
| 通知条件 | 日本企業言及を検出したときのみ。ゼロ件なら通知しない |
| 状態管理 | `state.json` の `last_seen_id`。これより大きいIDのみ新規として処理 |
| 履歴 | `log.md` に毎回追記（ヒットなしの回も1行残す） |

ツイートIDは Snowflake 形式で単調増加するため、ID の大小比較がそのまま新旧の判定になる。
ID から投稿時刻も復元できる（`(id >> 22) + 1288834974657` ミリ秒）。

## 処理フロー

1. `state.json` の `last_seen_id` を読む
2. ブラウザで `https://x.com/aleabitoreddit` を開き、`browser-snippets.md` の STEP 1 でID一覧とプレビューを収集
3. `last_seen_id` より大きいIDを新規分として抽出。ゼロ件なら 6 へ
4. `cdn.syndication.twimg.com` に移動し、STEP 2 で新規分の全文を一括取得
5. `keywords.md` を基準に日本企業言及を判定し、ヒットがあれば Slack DM を送信
6. `state.json` を更新し、`log.md` に結果を追記

## 既知の制約

### 1. 未ログインでは直近6件前後しか読めない

X のログイン壁により、プロフィールをスクロールしても表示されるのは直近6件程度で頭打ちになる。
実測では6件で約2日分（本人のタイムライン投稿は1日3件前後）をカバーしており、
12時間間隔のチェックには十分なバッファがある。

ただし連投した日は溢れる可能性があるため、**ギャップ検知**を行う。
取得できた最古ツイートのIDが `last_seen_id` より大きい場合、その間の投稿を見ていないことになるので、
Slack 通知に「取りこぼしの可能性あり」と明記し、`log.md` にも記録する。
ギャップが頻発するようなら頻度を上げる（3〜4回/日）。

### 2. 購読者限定ツイートは本文を取得できない

「Subscribe to unlock」の有料ツイートは、プロフィール上でも syndication API 経由でも本文が読めない
（API は `text` を返さない）。判定不能なので、`log.md` に「本文取得不可」として残す。

実測例: 2093604758485717289 / 2093582328857833883（いずれも 2026-08-29）

### 3. $ASE は日本企業ではない

X の暗号通貨 cashtag 機能により、ツイート中の `$ASE` が syndication API では
`ethereum:0x041ff0e49f6f774e7dc7bd10ee4a14c00b1d80b2`（Asentum というトークン）に置換されて返る。
文脈上は台湾の ASE（日月光）を指しているが、いずれにせよ日本企業ではない。
本文中に `ethereum:0x...` 形式の文字列が出てきたら、元は cashtag だったと解釈する。

### 4. 実行タイミング

スケジュールタスクは Claude Code アプリが起動している間に実行される。
アプリが閉じていた場合は次回起動時にまとめて実行される。

## ファイル

| ファイル | 内容 |
|---|---|
| `README.md` | 本ファイル。仕組みと制約 |
| `keywords.md` | 日本企業の検出キーワードリスト |
| `browser-snippets.md` | ブラウザで実行するJSスニペット2本 |
| `state.json` | 最終処理済みツイートID |
| `log.md` | 実行ログ・検出履歴 |

スケジュールタスク本体: `C:\Users\020168\.claude\scheduled-tasks\x-serenity-japan-watch\SKILL.md`

## 初回実測（2026-08-30）

直近6件（2026-08-27〜08-29）を全文取得して判定した結果、**日本企業への言及はゼロ**。
言及銘柄は $AMKR（米Amkor）、$ASE（台湾）、Powertech（台湾PTI）、$SIVE（スウェーデンSivers）。
後工程・OSAT の話題が中心のため、イビデン・新光電気・TOWA・ディスコ等が今後出てくる可能性はある。
