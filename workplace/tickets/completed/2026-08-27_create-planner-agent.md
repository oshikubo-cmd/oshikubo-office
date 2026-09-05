# plannerエージェント新設 + analystの定性リサーチ拡張

- ID: 2026-08-27_create-planner-agent
- 優先度: 中
- ステータス: completed
- 担当者: メイン（オフィス整備タスクのため直接実施）
- 作成日: 2026-08-27
- 完了日: 2026-08-27
- 概要: 企画の上流工程を担う planner エージェントを新設。researcher は新設せず、analyst の責務に定性リサーチを明文化して拡張（案1採用）。

## 実施内容

- [x] agents/planner/CLAUDE.md 作成（役割・行動ルール・企画書フォーマット）
- [x] agents/planner/memory/{raw,fact,digest}.md 作成
- [x] .claude/agents/planner.md 登録
- [x] agents/analyst/CLAUDE.md に「定性リサーチ（researcher兼務）」セクション追加＋責務1行追加
- [x] .claude/agents/analyst.md の description・責務を同期
- [x] オフィス CLAUDE.md のサブエージェント一覧に planner 追加・analyst 説明更新
- [x] agents/analyst/memory/raw.md に役割拡張を記録

## 成果物

- `agents/planner/CLAUDE.md` / `agents/planner/memory/`（3層）
- `.claude/agents/planner.md`
- `agents/analyst/CLAUDE.md`（定性リサーチセクション）
- `.claude/agents/analyst.md` / オフィス `CLAUDE.md` 更新

## 設計上の決定事項

- planner の守備範囲は「何をやるか」まで。動画台本・記事構成案など領域内の実施設計は各実行エージェント持ち（video-director との棲み分け）
- 経営系企画は `押久保.md` 必読＋3視点（収益性・持続性・確実性）評価を企画書に明記。AIdiver企画は KGI（会員10万人）貢献経路を明記
- 企画書には「リスク・弱点」を自分で書く欄を必須化（批判的思考の先回り）

## 再利用可能な学び

- [INSIGHT] 新エージェント追加時の必要ファイルは4点セット: `agents/<name>/CLAUDE.md`、`memory/{raw,fact,digest}.md`、`.claude/agents/<name>.md`、オフィス CLAUDE.md の一覧追記。既存エージェントの `.claude/agents/*.md` はfrontmatter（name/description）＋「セッション開始時/終了時に必ず行うこと」の型で統一されている
- [INSIGHT] 役割が既存エージェントと重なる新設案は、まず既存エージェントの責務拡張で吸収し、業務量で分離を判断する（researcher→analyst兼務の判断パターン）
