# investor エージェント 移設手順書

本オフィス（oshikubo_office）での investor は**仮置き**である。
個人投資の分析はプライベートPCで本格運用する前提のため、移設しやすい形で設計してある。

新PCでは「**A. フォルダをコピー → B. 4項目を再設定 → C. パスを1行修正**」で復旧する。

---

## A. コピーするもの（ファイルコピーで移る）

| # | 対象 | 備考 |
|---|---|---|
| 1 | `.claude/agents/investor.md` | サブエージェント定義（呼び出し口） |
| 2 | `agents/investor/` 一式 | CLAUDE.md・knowledge・**companies**・memory・本ファイル |
| 3 | `workplace/projects/minervini-watch/` | 第2ステージ定点観測リスト |
| 4 | `workplace/projects/kabutan-52w-high-x-watch/` | 52週高値×Xデイリーウォッチ（README・log・snippets） |
| 5 | `workplace/projects/x-serenity-watch/` | X日本株ウォッチ |
| 6 | storage の `08_資/資/新高/` | DUKE。資料本体＋上原素材（`データ・資料集/260711kabuberry_上原_AI分析/`）。**重いので外付け or クラウド経由で** |
| 7 | storage の `08_資/資/ちょうかぶデータ/` | 長期株式投資（ちょうかぶ式）の資料 |
| 8 | storage の `08_資/資/両/` `ダッシュボードサンプル/` `ペライチ_フォーマット.pptx` | 個別銘柄・PF・テンプレート |

> **3〜5を忘れやすい。** 「agents/investor/ だけコピー」では観測リストとログが落ちる。

### 移設先に oshikubo_office を持っていかない場合

`agents/investor/CLAUDE.md` は本オフィスの共通ルール（`workplace/tickets/` のチケット運用、
`agents/<name>/memory/` の3層メモリ）を前提に書かれている。
投資専用の新ワークスペースを作るなら、移設先のルート `CLAUDE.md` に最低限これだけ書いておく。

- チケット置き場: `workplace/tickets/{unstarted,in_progress,completed,pending}/`
- エージェントメモリ: `agents/<name>/memory/{raw,fact,digest}.md`（raw に追記 → fact に昇格 → digest に要約）
- 成果物置き場: `workplace/projects/<案件名>/`、資料の正本は storage をパス参照（コピーしない）

---

## B. 再設定が必要なもの（ファイルコピーでは移らない）

### B-1. 自動メモリ（投資系6本）

現在地: `C:\Users\020168\.claude\projects\C--Users-020168-Documents-Claude-oshikubo-office\memory\`

| ファイル | 内容 |
|---|---|
| `choukabu-method.md` | ちょうかぶ式の運用手法（買値レンジ法、東証PBR0.81が歴史的下限） |
| `personal-investing-domain.md` | 第3ドメインの定義（日経-10%/-20%トリガー、利回り3.75%基準、分散最優先） |
| `kabutan-52w-high-x-daily.md` | 52週高値×X話題デイリーDMの仕様 |
| `x-serenity-japan-watch.md` | X日本株ウォッチの仕様 |
| `x-tweet-fulltext-extraction.md` | Xツイート全文の取得方法 |
| `yahoo-realtime-x-search.md` | Yahoo!リアルタイム検索でX投稿を取得する方法 |

**注意**: このフォルダ名は**ワークスペースのパス由来**（`C--Users-020168-Documents-Claude-oshikubo-office`）。
新PCでユーザー名やフォルダ位置が変わると別フォルダ扱いになり、そのままでは読まれない。

**対策**: 移設時にこの6本の内容を `agents/investor/knowledge/` 側へ正本として移し、
自動メモリはポインタだけにする。そうすればリポジトリのコピーだけで完結する。

### B-2. 定期タスク（4本、全部投資系）

現在地: `C:\Users\020168\.claude\scheduled-tasks\`

| タスク | 内容 |
|---|---|
| `jp-stock-close-report` | 日本株引け後デイリーレポート |
| `jp-stock-pts-morning-report` | PTS夜間ランキングレポート |
| `kabutan-52w-high-x-daily` | 52週高値トップ10×X話題（平日18時） |
| `x-serenity-japan-watch` | X日本株ウォッチ（1日2回） |

各フォルダの `SKILL.md` はコピーできるが、**cron登録そのものは新PCで作り直す**。
`schedule` スキル、または `/loop` から再作成する。

### B-3. MCPコネクタ

| コネクタ | 用途 |
|---|---|
| IRbank（IRコネクト） | 株価・財務・セグメント・開示の**第一データソース**。これが無いと判定ができない |
| Slack | 定期レポートの通知先。DM宛先は `UMNRD48V8` |
| Google Drive | **投資日記の読み取り**。fileId は `knowledge/参照資料マップ.md` §3-2 に記載 |

アカウント側の接続設定のため、新PCで再接続する。

> 投資日記（Googleドキュメント）はクラウド上にあるため**コピー不要**だが、
> Driveコネクタを繋がないと読めない。移設後の疎通確認に含めること。

### B-4. スキル

以下は環境提供（リポジトリ内ファイルではない）。新PCでも同じ Claude Code / Cowork を使うなら追加作業なし。

| スキル | 用途 |
|---|---|
| `stage2-trend-template` | トレンドテンプレート8基準の判定 |
| `stock-purchase-checklist` | 購入前チェック（DUKE式9項目、xlsx出力） |
| `stock-deepdive-report` | 1銘柄の深堀分析レポート（HTML） |
| `stock-perayichi-onepager` | ペライチ1枚（pptx出力） |

ローカルの `.claude/skills/` に投資系スキルは**無い**（入っているのは記事・デザイン系のみ）。

---

## C. パスの修正（1行だけ）

`agents/investor/knowledge/参照資料マップ.md` の冒頭:

```
STORAGE_ROOT = C:\Users\020168\Documents\oshikubo_storage\08_資\資
```

**ここだけ**新PCの資料庫パスに書き換える。他のファイルに絶対パスは書いていないので、
この1行で全参照が復旧する。書き換えた後、他ファイルに絶対パスが混入していないか確認する場合:

```bash
grep -rn "Documents" agents/investor/ .claude/agents/investor.md
```

ヒットしてよいのは `knowledge/参照資料マップ.md` の STORAGE_ROOT 行と、本 README.md の
「現在地」記述だけ。`CLAUDE.md` や `.claude/agents/investor.md` に出てきたら修正する。

---

## 移設チェックリスト

- [ ] A-1〜A-5 をコピーした（projects 3つを忘れていない）
- [ ] A-6〜A-8 の storage 資料をコピーした
- [ ] B-1 自動メモリ6本を knowledge/ 側へ移すか、新しいメモリフォルダに再配置した
- [ ] B-2 定期タスク4本の cron を再作成した
- [ ] B-3 IRbank と Slack を再接続した（Slack DM宛先の確認も）
- [ ] B-4 投資系スキル4つが使える状態か確認した
- [ ] C STORAGE_ROOT を書き換えた
- [ ] 動作確認: 適当な銘柄コードを1つ渡して、ステージ判定＋トレンドテンプレート8条件の
      合格数と不合格条件が返ってくることを確認した

---

## 設計上の約束（移設先でも守る）

- 投資固有のルール・知識は `agents/investor/` の中に閉じる。共通ファイルに散らさない
- 絶対パスは `参照資料マップ.md` の STORAGE_ROOT 1箇所のみ
- 資料の正本は storage に置いたままパス参照する。リポジトリにコピーしない（重い・私的資料）
- DUKE。資料は私的利用のみ。再配布・転載しない
