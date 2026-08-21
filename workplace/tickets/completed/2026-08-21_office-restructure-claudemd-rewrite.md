# CLAUDE.md・エージェント定義の書き換え案作成

- ID: 2026-08-21-office-restructure
- 優先度: 中
- ステータス: completed
- 完了日: 2026-08-21
- 担当者: main（Claude直轄）
- 作成日: 2026-08-21
- 概要: オフィス名を AIdiver_office → oshikubo_office に変更したことに伴い、CLAUDE.md とエージェント定義の「AIdiver前提」の記述を、執行役員業務メイン＋AIdiver編集長業務の実態に合わせて書き換える案を作成する。

## 要件

- フォルダ構成は変更しない（現構成は役割中立で維持可能と判断済み）
- CLAUDE.md: オフィスの主宰・業務ドメインを最上位に置き、KGI/パーパスをAIdiverドメイン配下に一段下げる
- エージェント定義: analyst / writer / editor / designer の守備範囲を経営業務まで広げる（video-director は現状維持）
- 成果物は「案」として提示し、承認後に適用する

## 対象ファイル

- CLAUDE.md
- agents/analyst/CLAUDE.md
- agents/writer/CLAUDE.md
- agents/editor/CLAUDE.md
- agents/designer/CLAUDE.md
- （掃除候補）agents/agent-name/

## 実施内容

1. 書き換え案を作成（workplace/projects/office-restructure/rewrite-proposal.md）し、ユーザー承認を得た
2. ドメイン1はFY2026メディア編集部門総会資料（2026年4月・押久保発表）に基づき再考。部門数値目標（売上14.7億/粗利7億/営利2.8億）・3視点（収益性・持続性・確実性）・組織体制（第1=IT/第2=ビジネス、33名）・2大テーマ（AIネイティブ/動画ネイティブ）・スローガン「評論家ではなく、実践者であれ」を反映
3. CLAUDE.md: 「組織KGI」「組織パーパス」を廃止し「本オフィスについて」（2ドメイン構造）を新設。KGI/パーパスはドメイン2配下へ移動。サブエージェント構成の守備範囲を拡張
4. analyst / writer / editor / designer のCLAUDE.mdを経営業務込みの定義に更新（video-directorは変更なし）
5. agents/agent-name/（テンプレート残骸）を削除
6. 全5エージェントの memory/raw.md に定義変更を記録

## 成果物

- 更新済み CLAUDE.md、agents/{analyst,writer,editor,designer}/CLAUDE.md
- workplace/projects/office-restructure/rewrite-proposal.md（設計判断の記録）

## 発生した問題と対処

- 総会資料pptxのmarkitdown抽出でシェルリダイレクト経由だと文字化け → Pythonから直接UTF-8でファイル出力して解決

## 再利用可能な学び

- [INSIGHT] 数値目標はCLAUDE.mdに直接記載する運用を採用（ユーザー確認済み）。期が変わったら総会資料をもとにCLAUDE.mdのFY表記・数値を更新すること
- [INSIGHT] Windows環境でmarkitdownの日本語出力をファイル化する際は、シェルの `>` ではなくPython内で encoding='utf-8' 指定で書き出す
