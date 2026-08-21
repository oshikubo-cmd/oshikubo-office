# 資料庫のリネームとオフィスへの参照統合

- ID: 2026-08-21-storage-integration
- 優先度: 中
- ステータス: completed
- 担当者: main（Claude直轄）
- 作成日: 2026-08-21
- 完了日: 2026-08-21
- 概要: Cowork用に分けていた `cowork_root`（84GB、資料・素材の保管庫）を、今後Claude Codeメインで使う方針に合わせて整理。物理移動はせず「仕事の管理層（oshikubo_office）と保管庫の分離」を維持し、リネーム＋参照統合で対応。

## 実施内容

1. `C:\Users\020168\Documents\cowork_root` → `C:\Users\020168\Documents\oshikubo_storage` にリネーム
2. CLAUDE.md に「外部資料庫（oshikubo_storage）」セクションを新設。ディレクトリ構成と運用ルール（正本参照・案件着手時のみテキスト素材をprojectsへコピー・重いメディアはパス参照）を明記
3. rewrite-proposal.md 内の旧パス参照を更新
4. `押久保.md`（保管庫直下の判断軸定義ファイル）の統合可否を評価 → 統合推奨と判断し、ユーザーに提案（対応は別途）

## 判断の記録

- 84GBの保管庫をgitリポジトリ配下に移すとgit操作が破綻するため、物理統合は不採用
- Claude Codeはパス指定で保管庫を直接読めるため、CLAUDE.mdへの参照記載で実用上は統合される

## 再利用可能な学び

- [INSIGHT] 大容量の資料庫はgit管理下に置かず、CLAUDE.mdからのパス参照で統合する。管理層（チケット・成果物）と保管庫（素材・正本）の分離を維持する
