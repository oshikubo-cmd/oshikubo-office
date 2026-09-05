# X @aleabitoreddit 日本株言及の監視体制構築

- ID: 2026-08-30_x-serenity-japan-watch
- 優先度: 中
- ステータス: completed
- 完了日: 2026-08-30
- 担当者: analyst
- 作成日: 2026-08-30
- ドメイン: 個人投資（第3ドメイン）

## 概要

X アカウント Serenity（@aleabitoreddit / AI・半導体サプライチェーン調査、フォロワー102.3万）が
日本企業・日本株に言及したときに検知し、Slack DM で通知する監視の仕組みを構築する。

## 要件

- 頻度: 1日2回（朝・夕）
- 通知先: Slack 自分宛DM（UMNRD48V8）
- 検出範囲: 日本企業への言及すべて（銘柄コード・$ティッカー・社名・Japan文脈）
- 取りこぼし防止のため本文は全文取得する（「さらに表示」で切れた状態で判定しない）

## タスクリスト

- [x] アカウントの実在・取得可否の確認（未ログインでタイムライン本文が取得可能）
- [x] ツイートID・正確な投稿時刻の抽出方法の確立
- [x] 全文取得手段の確立（cdn.syndication.twimg.com の一括fetch）
- [x] 日本企業キーワードリストの作成
- [x] 収集スクリプト・状態ファイルの作成
- [x] 初回の遡り検証（実際の日本株言及頻度の把握）
- [x] スケジュールタスクの登録

## 対象ファイル

- workplace/projects/x-serenity-watch/

## 成果物

- workplace/projects/x-serenity-watch/（README・keywords・browser-snippets・state・log）
- スケジュールタスク x-serenity-japan-watch（C:/Users/020168/.claude/scheduled-tasks/x-serenity-japan-watch/SKILL.md）
- Slack DM 通知先: DN3ERSWDD（自分宛DM）

## 実施内容（2026-08-30）

- @aleabitoreddit の実在とプロフィールを確認（Serenity / AI・半導体サプライチェーン調査 / フォロワー102.3万 / 投稿7,452件）
- 未ログインでもタイムライン本文が取得可能なことを確認
- ツイートID・投稿時刻の抽出方法を確立（Snowflake ID から時刻を復元）
- 全文取得手段を確立（cdn.syndication.twimg.com への同一オリジン一括fetch）
- 直近6件（8/27〜8/29）を全文判定 → 日本企業言及は0件
- workplace/projects/x-serenity-watch/ に README・keywords・snippets・state・log を作成
- スケジュールタスク x-serenity-japan-watch を登録（cron: 53 7,18 * * *）

## 発生した問題と対処

1. curl による外部アクセスがサンドボックスで不可 → ブラウザ経由に切り替え
2. ページ内fetchが cdn.syndication.twimg.com へCORSでブロック → 同オリジンに navigate してから fetch する方式に変更
3. 未ログインだと直近6件前後しか読めない → ギャップ検知（最古IDが last_seen_id より新しければ警告）を仕様に組み込み
4. 購読者限定ツイートは本文取得不可 → 判定不能として log.md に記録する運用に

## 再利用可能な学び

- [INSIGHT] X のツイート全文は `https://cdn.syndication.twimg.com/tweet-result?id=<id>&token=a&lang=en` で未ログイン取得できる。ただしCORSがあるため、ブラウザで同オリジンに navigate してから fetch する必要がある
- [INSIGHT] ツイートIDは Snowflake 形式。`(id >> 22) + 1288834974657` ミリ秒で投稿時刻が復元でき、ID の大小比較がそのまま新旧判定になるので、監視の状態管理は last_seen_id 1つで足りる
- [INSIGHT] X の未ログイン閲覧はプロフィールで直近6件前後が上限。スクロールしても増えないため、監視間隔は投稿ペースとこのバッファから逆算する必要がある
- [INSIGHT] X の暗号通貨cashtag機能により、$ASE のような株式ティッカーが syndication API では `ethereum:0x...` に置換されて返ることがある
- [INSIGHT] scheduled-tasks の schedule 表示は次回1回分のみの人間可読表現。複数時刻cron（"53 7,18 * * *"）でも1つしか表示されないので、cronExpression フィールドで検証する
