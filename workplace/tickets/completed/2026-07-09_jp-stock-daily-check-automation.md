# 日本株 日次株価チェックの自動化

- ID: 2026-07-09_jp-stock-daily-check-automation
- 優先度: 中
- ステータス: completed
- 担当者: analyst
- 作成日: 2026-07-09
- 完了日: 2026-07-09
- 概要: 日本株の日次チェックルーティン（52週高値銘柄、値上がり・値下がりランキング、PTSランキング、各トップ10の理由分析）を自動化し、Slack DMにレポート配信する。

## 実施内容

1. データソースの取得可否をWebFetchで検証
   - ✅ 値上がり/値下がりランキング: Yahoo!ファイナンス（https://finance.yahoo.co.jp/stocks/ranking/up・/down）
   - ✅ 52週高値銘柄: TradingView日本株（https://jp.tradingview.com/markets/stocks-japan/market-movers-52wk-high/）
   - ✅ PTSナイトセッション（値上がり・値下がり両方）: 松井証券（https://www.matsui.co.jp/stock/pts/）
   - ❌ 株探（kabutan.jp）・みんかぶ・バフェットコード: WebFetchが403でブロック
2. スケジュールタスク2本を作成（`C:\Users\020168\.claude\scheduled-tasks\`）
   - `jp-stock-close-report` — 平日16:00過ぎ: 値上がり/値下がりTop10+理由、52週高値更新銘柄
   - `jp-stock-pts-morning-report` — 平日8:00過ぎ: 前夜PTSナイトセッション上昇/下落Top10+理由
3. 出力先はSlack DM（user_id: UMNRD48V8）。個人timesチャンネル等が見つからなかったためDMを既定とした

## 成果物

- スケジュールタスク: `jp-stock-close-report` / `jp-stock-pts-morning-report`
- 各タスクのプロンプトに、休場時の挙動、ソース障害時のフォールバック、理由捏造の禁止を明記

## 発生した問題と対処

- 株探がWebFetchをブロック（403）→ Yahoo!ファイナンス+TradingView+松井証券の組み合わせに変更
- Yahoo!ファイナンスにPTSランキングがない → 松井証券の前営業日夜間ランキング（上昇・下落両掲載）を採用

## 再利用可能な学び

- [INSIGHT] 株探・みんかぶ・バフェットコードはWebFetch不可（403）。日本株ランキング取得はYahoo!ファイナンス（/stocks/ranking/{up|down|yearToDateHigh}）、52週高値はTradingView、PTS夜間は松井証券が安定して取得できる
- [INSIGHT] 松井証券PTSページは「前営業日の夜間取引（17:00〜翌6:00）」なので、朝8時実行で前夜分がちょうど取れる。月曜朝は金曜夜間分になる
- [INSIGHT] scheduled-tasksはアプリ起動中のみ実行される。初回は「Run now」でツール承認を済ませておくと以降の自動実行が止まらない
