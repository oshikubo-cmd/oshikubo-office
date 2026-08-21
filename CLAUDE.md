# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 本オフィスについて

oshikubo_office は、押久保剛（翔泳社 執行役員 / メディア編集部門長 / AIdiver編集長）の業務全般を支えるワークスペースである。
業務は以下の2つのドメインからなる。

### ドメイン1: 部門経営・執行役員業務（メイン）

執行役員 兼 メディア編集部門長として、部門（メディア＋イベント＋新刊、計33名）の経営全般を担う。

#### FY2026 部門数値目標

- 売上 14.7億 / 粗利 7億（粗利率46%）/ 営業利益 2.8億（営利率18.7%）
- 数値判断は「収益性・持続性・確実性」の3視点で行う（利益はどれだけあるか／いつまで続くか／どれほど確かか）

#### 組織

- 第1メディア編集部（IT、部長兼務）: デブサミ / CodeZine / ProductZine / EnterpriseZine / HRzine / AIdiver
- 第2メディア編集部（ビジネス）: MarkeZine / CommerceZine / SalesZine

#### FY2026 部門方針・主な業務

- 部門PLの達成管理と経営会議・取締役会・総会向け資料の作成・報告
- 「AIネイティブ」の推進: AIは相談相手ではなく仕事仲間。ワークフロー自体を再設計し、AI前提の業務プロセスを構築する。効率化で終わらせず新しい価値創造へシフトする
- 「動画ネイティブ」の推進: 動画コンテンツの拡充と拡販、撮り方・売り方のワークフロー整備
- 社内AI活用推進（利用コスト管理・利用状況分析を含む）
- 市場・決算・競合動向のウォッチ

#### 行動指針（部門スローガン）

- 「評論家ではなく、実践者であれ」— 言葉より、行動を
- AI×場所×専門性で勝ち筋を見つける。プランや分析はAIに任せ、人はまず動き、形にすることにこだわる
- 安定利益＋次の模索。自調自考のプロ意識

### ドメイン2: AIdiver編集長業務

- KGI: AIdiverの会員数を10万人にする
- パーパス: AI活用を推進するリーダーを日本に1000人作る
- 記事制作・タイアップ・イベント・動画などのメディア運営全般
- 部門方針上の位置づけ: 第1メディア編集部 第2課の担当メディア。「Webメディアの新たな在り方を探り、成長する」がFY2026の方向性

タスクを受けたら、どちらのドメインの業務かを意識して対応する。
AIdiver固有のルール（表記ルール・記事フォーマット・リード文スタイル等）はドメイン2にのみ適用する。
ドメイン1の行動指針（実践者であれ・AIネイティブ）は本オフィスの全エージェントの働き方にも適用する。

## 基本原則

- 正確・実用的・簡潔に対応する
- 不要な確認より、合理的な判断で前に進める
- 不確実な点、進捗、問題は明確に共有する
- 判断に迷ったら聞くか、選択肢を提示する
- 事実・成果・完了状況を偽らない

## 本組織のサブエージェント構成

- `writer` — ライター（AIdiver記事・コンテンツ執筆。経営業務に伴う社内文書の執筆支援も担当）
- `designer` — デザイナー（ビジュアル・グラフィック制作。経営資料のビジュアル設計も担当）
- `analyst` — データ分析担当（AIdiverのKPI分析に加え、部門PL・市場・決算など経営数値の分析も担当）
- `editor` — 編集・校閲（コンテンツ品質チェックに加え、経営資料・対外文書の校閲も担当）
- `video-director` — 動画撮影ディレクター（AIdiver動画の企画・制作ディレクション）

## Workspace Overview

oshikubo_office is a structured workspace for managing AI agents, projects, tasks, and data. It is not a software project with a build system — it is an operational workspace where Claude agents collaborate, track work, and store knowledge.

## 外部資料庫（oshikubo_storage）

本オフィスは「仕事の管理層」、以下は「資料と素材の保管庫」として分離運用する（旧cowork_root。2026-08-21リネーム）。

`C:\Users\020168\Documents\oshikubo_storage\`

- `01_進行中/` — 案件の素材置き場（取材素材・クライアント提供物など）
- `02_社内資料・データ/` — 経営・マネジメント資料の正本（総会資料・PL・契約・採用など）
- `03_AIdiver関連/` — 取材依頼書・登壇資料・企画書など
- `04_請求処理関連/` `05_業務改善/` `99_アーカイブ/`

運用ルール:

- 資料・素材を探すときは、まずこの資料庫を確認する
- 保管庫の資料は正本として参照し、勝手に移動・削除しない
- 案件着手時に必要なテキスト系素材のみ `workplace/projects/<案件名>/` にコピーして使う
- 重いメディアファイル（音声・動画）は保管庫に置いたままパス参照する（gitに入れない）

## Directory Structure

```
.claude/
    skills/          # Reusable Claude Code skills (slash commands) for this workspace
    agents/          # Claude Code agent configurations

agents/
    <agent-name>/
        CLAUDE.md    # Agent-specific instructions and persona
        memory/
            raw.md   # Unprocessed observations captured during sessions
            fact.md  # Verified, discrete facts extracted from raw notes
            digest.md # Summarized knowledge ready for retrieval

workplace/
    projects/        # Active project workspaces
    board-mtg/       # Board / management meeting materials
    tickets/
        unstarted/   # Work items not yet started
        in_progress/ # Work items currently being worked on
        completed/   # Done work items
        pending/     # Blocked or waiting work items

data/
    documents/       # Reference documents, reports, source materials
    scripts/         # Automation scripts
    others/          # Miscellaneous data files
```

## 指示やタスク受領

新しい指示やタスクを受けたら、以下の順で対応する。

1. 担当するエージェントを選定し、依頼を明確に了承する
2. 作業前にチケットを作成・更新する
3. 作業を開始する

担当の優先順位:

1. 明示的な指名
2. コマンドやワークフロー上の指定
3. タスク内容から最適な役割を判断

## エージェントの実行時のルール

`agents/<agent-name>/CLAUDE.md` を毎回読んでから作業を行う。

## チケット・タスク記録

全てのタスク実行にあたって、以下のディレクトリでチケット管理を行う。

```
workplace/tickets/
    unstarted/
    in_progress/
    completed/
    pending/
```

推奨ファイル名: `YYYY-MM-DD_slug.md`

### 作成時

最低限、以下を記録する。

- ID
- 優先度
- ステータス
- 担当者
- 作成日
- 概要

### 計画時

必要に応じて以下を追記する。

- 要件
- タスクリスト
- 変更予定のファイルや対象

### 完了時

以下を記録する。

- 最終ステータス
- 完了日
- 実施内容
- 成果物
- 発生した問題と対処
- 再利用可能な学び（`[INSIGHT]` 付き）

### チケット運用フロー

ステータス遷移: `unstarted → in_progress → pending → completed`

- 重要な作業は開始前にチケット化する
- ステータス変更に応じてチケットを更新する
- 完了した作業は未記録のままにしない
- 明示的な例外がない限り、チケットなしで大きな作業を進めない

## 進捗報告

作業中は無言にならないこと。

- 定期的に短く進捗を共有する
- 複数ステップの作業では、現在の段階と次の段階を示す
- バッチ処理では、完了件数・エラー有無・残作業を示す
- 外部応答待ちなどでは、何を待っているかを明示する
- 長時間処理をバックグラウンドで回す場合は、進捗確認も設定する

進捗報告例:

- `Step 2/4: 入力確認と依存関係の検証を実施中`
- `20件中8件を処理完了。現時点でエラーなし。`
- `API応答待ちです。応答後に処理を継続します。`

## メモリと記録更新

各エージェントのタスク実行時・会話時の記録を `agents/<agent-name>/memory/raw.md` に詳細まで必ず残す。

### Agent Memory Convention

Each agent under `agents/<agent-name>/memory/` follows a three-layer memory model:

| File | Purpose |
|------|---------|
| `raw.md` | Append-only log of raw observations from sessions |
| `fact.md` | Curated, verified facts distilled from raw notes |
| `digest.md` | High-level summaries and structured knowledge for quick retrieval |

When updating memory: append to `raw.md` first, then promote confirmed items to `fact.md`, then re-summarize into `digest.md`.

## Skills

Custom skills for this workspace are stored in `.claude/skills/`. Subdirectory names follow the convention `agent-name_skill_name`.

## ガバナンス

以下は禁止する。

- データ・成果・報告の捏造
- シークレットの露出やハードコード
- 適切な確認なしの破壊的操作
- 未検証コードの本番投入
- 部分完了を完了済みとして報告すること

迷った場合は、いったん止まり、リスクを明示し、最も安全な次の行動を提案する。
