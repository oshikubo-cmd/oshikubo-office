# ID: 2026-09-06_x-duke-watchlist-daily-setup

- 優先度: 中
- ステータス: completed
- 担当者: investor
- 作成日: 2026-09-06
- 概要: DUKE。が参考にしている投資系Xアカウント25件を対象に、投資関連の投稿を毎日まとめてSlack自分宛DM（channel_id=UMNRD48V8）へ送る定点観測の仕組みを新規構築する。

## 背景

押久保さんより、以下25アカウントの投稿内容のうち投資関連のものを毎日送ってほしいとの依頼。
既存の [workplace/projects/x-serenity-watch/](../../projects/x-serenity-watch/) （1アカウント・日本株言及検知）、
[workplace/projects/kabutan-52w-high-x-watch/](../../projects/kabutan-52w-high-x-watch/) （銘柄別X話題・毎日1本DM）
と同じ技術基盤（プロフィール巡回→syndication APIで全文取得→ID比較で新規判定→Slack DM）を流用する。

## 対象アカウント（25件）

1. ありゃりゃ @aryarya
2. 井村俊哉 @imuvill
3. 上原＠投資家 @uehara_sato4
4. ABCトレーダー @ABC87791035
5. 企業分析ハック @company_hack
6. Ken/1UP投資 @KenichiShimada2
7. kenmo@湘南投資勉強会 @kenmokenmo
8. 五月 @hakureifarm （鍵アカウント）
9. 後藤達也 @goto_finance
10. sak @sak_07_
11. ざら速(ザラ場速報) @ZARASOKU
12. 四季報分析@テンバガー研究所 @shikiho_10
13. 世界四季報 @4ki4
14. たけぞう @noatake1127
15. DAIBOUCHOU @DAIBOUCHO
16. 駄犬 @daken_in_market
17. T.Kamada @Kamada3
18. テスタ @tesuta001
19. hiro_tyun @hiro_tyun
20. ふしちょう @the_phoenix_777
21. 豆山くん @mameyama_kun
22. Made in Japan @InvestInJapan
23. ゆうなぎ(夕凪) @yuunagi_dan
24. Yoyogi Capital @YoyogiCapital
25. Ring @xRINGx
26. DUKE。（本人） @investorduke

## 要件

- 上記25アカウントを毎日1回巡回し、投資・相場関連の投稿を抽出、1本のSlack DM（channel_id=UMNRD48V8）にまとめて送る
- アカウントごとに `last_seen_id` を管理し、新規投稿のみ判定対象にする（x-serenity-watch方式）
- 鍵アカウント（@hakureifarm）は本文取得不可の可能性が高いので、その旨をREADMEに明記し、取得できなければスキップ扱いにする
- 初期セットアップでは各アカウントの最新IDをベースラインとして記録するのみでよい（25件分の遡り全文判定はコスト高のため不要。次回の定時実行から本稼働）
- スケジュールタスクとして `.claude/scheduled-tasks/` に登録し、cronで自動実行する（頻度・時刻は investor エージェントの判断でx-serenity-watch/kabutanの前例に揃える。目安: 毎日20:00 JST）
- 完了後、`agents/investor/README.md` の「担当プロジェクト」表に追加、自動メモリにポインタ登録

## タスクリスト

- [x] `workplace/projects/x-duke-watchlist-daily/` 配下にREADME.md・state.json（26アカウント分）・log.md・browser-snippets.md（x-serenity-watch流用）を作成
- [x] 25アカウント（+作業中に追加されたDUKE。本人 @investorduke を含む計26アカウント）それぞれのプロフィールを巡回し、最新ツイートIDをベースラインとして記録
- [x] `C:\Users\020168\.claude\scheduled-tasks\x-duke-watchlist-daily\SKILL.md` を作成し、`mcp__scheduled-tasks__create_scheduled_task` でスケジュールタスクとして登録（cron `0 7 * * *`）
- [x] `agents/investor/README.md`（移設手順のコピー対象表）・`agents/investor/CLAUDE.md`（担当プロジェクト表）に追記
- [x] 自動メモリへのポインタ登録（MEMORY.md + `x-duke-watchlist-daily.md`）
- [x] `agents/investor/memory/raw.md` に作業ログを追記

## 完了報告

- 最終ステータス: completed
- 完了日: 2026-09-06
- 実施内容:
  1. `workplace/projects/x-duke-watchlist-daily/`（README.md・browser-snippets.md・state.json・log.md）を新規作成。技術方式は `x-serenity-watch`（ID比較→syndication API全文取得）、ダイジェスト形式は `kabutan-52w-high-x-watch`（毎日1本、ヒットゼロでも送信）を踏襲
  2. 26アカウント（当初25件＋作業中にチケットへ追加された DUKE。本人 @investorduke）のプロフィールを `browser_batch` で5件ずつ巡回し、最新投稿IDをベースラインとして `state.json` に記録（初期セットアップにつき全文判定・DM送信は未実施）
  3. `.claude/scheduled-tasks/x-duke-watchlist-daily/SKILL.md` を `mcp__scheduled-tasks__create_scheduled_task` / `update_scheduled_task` で作成・更新。cron `0 7 * * *`（毎日朝7時台JST）。初回自動実行は2026-09-07予定
  4. `agents/investor/CLAUDE.md`（担当プロジェクト表）・`agents/investor/README.md`（移設手順のコピー対象表）に追記
  5. 自動メモリに `x-duke-watchlist-daily.md` を新規作成し、`MEMORY.md` に1行追加
  6. `agents/investor/memory/raw.md` に作業ログ（データソース・取得日・判明事実・INSIGHT）を追記
- 成果物:
  - `workplace/projects/x-duke-watchlist-daily/README.md` / `browser-snippets.md` / `state.json` / `log.md`
  - `C:\Users\020168\.claude\scheduled-tasks\x-duke-watchlist-daily\SKILL.md`（スケジュールタスク）
  - `agents/investor/CLAUDE.md`、`agents/investor/README.md`
  - `C:\Users\020168\.claude\projects\C--Users-020168-Documents-Claude-oshikubo-office\memory\x-duke-watchlist-daily.md`、`MEMORY.md`
  - `agents/investor/memory/raw.md`
- 発生した問題と対処:
  1. 鍵アカウントが2件判明。チケット記載の `@hakureifarm` に加え、`@YoyogiCapital` も初期セットアップ時に「ポストは非公開です」表示を確認。README・state.jsonの両方に明記し、スキップ扱いとした
  2. 作業途中でチケットファイル自体が更新され、26件目のアカウント（DUKE。本人 @investorduke）が対象リストに追加されているのを検知。公開アカウントであることを確認したうえで全成果物（README・state.json・log.md・スケジュールタスクのプロンプト・自動メモリ）を26アカウント版に更新した
  3. `agents/investor/README.md` に担当プロジェクト表を追記しようとした際、実際にはREADME.mdではなくCLAUDE.mdに当該表があることに気づき（README.mdは移設手順書）、誤ってREADME.mdの別表（移設コピー対象表）に不正な行を挿入してしまった。すぐに気づき修正（CLAUDE.mdの担当プロジェクト表に正しく追記、README.mdの移設対象表にも正規の行番号で追記）
- 再利用可能な学び:
  - `[INSIGHT]` 複数アカウント監視を1件ずつ`navigate`→`javascript_tool`で処理すると往復コストが大きいが、`browser_batch`に「navigate→wait 3秒→javascript_tool」を1セットとして5アカウント分（15アクション）ずつ積むと安定して流せた
  - `[INSIGHT]` 鍵アカウント判定はJS側で`document.body.innerText`に「ポストは非公開です」「Only approved followers」が含まれるかで機械的に判定できる
  - `[INSIGHT]` syndication API全文取得はアカウントをまたいでID配列を1本にまとめて一括fetchできる（IDだけで引けるためアカウント単位に分ける必要がない）
  - `[INSIGHT]` `agents/investor/README.md` と `CLAUDE.md` はどちらも投資家エージェントの説明ファイルだが役割が異なる（README.md=新PC移設手順書、CLAUDE.md=エージェント本体の運用定義・担当プロジェクト表）。今後 investor 関連でファイルを編集する際は、編集前に対象ファイルの実際の見出し・表を確認してから書き込むこと
