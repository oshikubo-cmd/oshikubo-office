# チケット: アシックス(7936) CAN-SLIM評価

- ID: 2026-09-23-7936-canslim
- 優先度: 中
- ステータス: **completed**
- 担当者: investor
- 作成日: 2026-09-23
- 完了日: 2026-09-23
- 概要: 押久保からの `/investor-canslim` 依頼。アシックス(7936)をオニールのCAN-SLIM7項目で評価する。既存のステージ2判定・深堀分析（`workplace/projects/7936-asics-box-pullback/`）を土台に、追補レポートとして作成する。

## 実施内容

SKILL.mdのStep1〜4・よくある誤りチェックを全て実施。IRbankコネクタ7種のツールでデータ取得し、C/A/N/S/L/I/Mを判定。日経225連動ETF(1321)の日次終値から200日SMAを自算しMを補完（フォロースルーデー・ディストリビューションデーは取得できずと明記）。ビッグチェンジ判定とPER進捗（実績29.4倍／今期予想21.5倍／来期予想18.3倍、5年平均32.4倍）を算出。

## 結果

3勝（C・A・M）／1敗（I）／3保留（N・S・L）。業績は極めて強いが需給・リーダー性・機関投資家支持に弱さがあり典型的なCAN-SLIM銘柄とは言えない、と結論。ビッグチェンジは①（成長加速）⑤（株主還元強化）に該当するがPERは拡大でなく圧縮中。CAN-SLIMの評価はエントリー判断にすり替えず、既存のステージ2不成立（トレンドテンプレート3/8）によるエントリー対象外の整理を維持した。

## 成果物

- `workplace/projects/7936-asics-box-pullback/2026-09-23_CAN-SLIM評価.md`
- `agents/investor/companies/7936_アシックス/README.md` 更新
- `agents/investor/memory/raw.md` 追記

## 発生した問題と対処

`list_disclosures`の`document_type`はフリーテキストのkeyword検索ではなく前方一致フィルタで、TDnet開示は`document_type`が常にnullのため指定するとTDnet開示（自己株買い等）が漏れる。日付範囲指定に切り替えて目視確認する方式で対処した。

## 再利用可能な学び

- `[INSIGHT]` IRBANKは200日SMAの値そのものを返さないが、ベンチマークETFの1年分日次終値（約252営業日）があれば自算でき、21営業日前との比較で「200日線が上昇中か」も判定できる
- `[INSIGHT]` 信用買残は絶対量だけでなく「価格局面との対応」を見る。アシックスは上昇局面で信用買いが少なく下落局面で急増しており、押し目を個人が信用で拾うパターンと解釈した

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
