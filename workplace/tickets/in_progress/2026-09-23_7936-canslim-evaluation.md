# チケット: アシックス(7936) CAN-SLIM評価

- ID: 2026-09-23-7936-canslim
- 優先度: 中
- ステータス: in_progress
- 担当者: investor
- 作成日: 2026-09-23
- 概要: 押久保からの `/investor-canslim` 依頼。アシックス(7936)をオニールのCAN-SLIM7項目で評価する。既存のステージ2判定・深堀分析（`workplace/projects/7936-asics-box-pullback/`）を土台に、追補レポートとして作成する。

## 要件

- `.claude/skills/investor-canslim/SKILL.md` のStep1〜4、よくある誤りチェックを厳密に実施
- IRbankコネクタでデータ取得（get_valuation_metrics_history, get_weekly_margin_balance, get_financials, list_shareholders, list_disclosures, list_segments）
- C/A/N/S/L/I/Mを○/△/✗/取得できずで判定。Mは別途確認または「取得できず」明記
- ビッグチェンジ判定（サブ教材§1-9の5パターン）とPER拡大進捗を数字で
- 役割分担の混同禁止: CAN-SLIM高評価でもステージ2不成立ならエントリー対象外の整理を維持

## 変更予定のファイル

- 新規: `workplace/projects/7936-asics-box-pullback/2026-09-23_CAN-SLIM評価.md`
- 更新: `agents/investor/companies/7936_アシックス/README.md`
- 更新: `agents/investor/memory/raw.md`
