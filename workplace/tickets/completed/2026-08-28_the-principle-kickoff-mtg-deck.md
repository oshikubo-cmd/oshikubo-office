# THE MODEL続編（仮『THE PRINCIPLE』）方向性すり合わせMTG用たたき資料

- ID: 2026-08-28_the-principle-kickoff-mtg-deck
- 優先度: 高
- ステータス: in_progress
- 担当者: planner（主担当）
- 作成日: 2026-08-28
- 概要: 福田康隆氏（THE MODEL著者）の続編骨子ドラフト（Google Drive共有: 序章・第1〜4章・終章）をベースに、方向性・見せ方・伝える順番をすり合わせる1.5hディスカッションMTG用のたたき資料を作成する。福田氏は「どういう軸で書くのがいいのか迷っている」ため、軸の選択肢を複数提示する。編集担当: 押久保＋大久保。

## 要件

- アウトプット: アーティファクト（HTML）＋ PowerPoint（.pptx）
- 内容: 骨子の現状整理 / 論点 / 軸・見せ方・章順の複数案 / タイトル案（『THE PRINCIPLE』含む）/ 進め方
- 押久保.md 準拠（結論先出し・批判的思考・受益者定義）

## 素材

- Drive: 1wIHYScOvTAxec4VsWFSXHwWkThvqPFrN（序章/第1章/第2章/第3章/第4章/終章、第5〜7章は未共有）
- ローカル: oshikubo_storage/01_進行中/THE MODEL2/260701福田さんメモ.txt（7月相談時のメモ、Shift-JIS）
- 著者メール（2026-08-23）の5ポイント: 原理原則の大事さ / 前半はTHE MODEL続編的位置付け / Japan Cloud複数社観察のストーリー / GTM・採用・リーダーシップ等経営視点厚め / 具体性を高めつつ原理原則へ汎用化

## 完了記録

- 最終ステータス: completed
- 完了日: 2026-08-28
- 実施内容:
  - Drive共有の骨子ドラフト6ファイル（序章・第1〜4章・終章）を全文精読、7月メモ（Shift-JIS）も復元して読解
  - 押久保.md・planner CLAUDE.md 準拠でたたき資料を設計（結論先出し・批判的指摘込み）
  - HTMLアーティファクト公開 + PPTX（13枚、python-pptx製）を生成、PowerPoint COMでビジュアルQA実施
- 成果物:
  - workplace/projects/the-model2-principle/mtg_tataki_v1.html（アーティファクト公開済み）
  - workplace/projects/the-model2-principle/THE_PRINCIPLE_方向性たたき_v1.pptx
  - workplace/projects/the-model2-principle/build_pptx.py（再生成用）
- 発生した問題と対処:
  - ローカルにNode.jsなし → pptxgenjsを断念しpython-pptxへ切替
  - LibreOffice/soffice なし → PowerPoint COM automationでPNG書き出しQA
  - 7月メモがShift-JIS文字化け → PowerShell Get-Content -Encoding Default で復元
- 再利用可能な学び:
  - [INSIGHT] 骨子内の章番号参照の揺れ（未共有の第5〜7章への言及）は「構成未確定」のシグナルとして資料の論点に転用できる
  - [INSIGHT] この端末でのPPTX生成は python-pptx + PowerPoint COM (Export PNG) が確実な組み合わせ
