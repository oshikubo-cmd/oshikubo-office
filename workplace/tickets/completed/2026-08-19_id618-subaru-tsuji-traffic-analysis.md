# チケット: id618 スバル辻さん記事の急伸トラフィック分析

- ID: 2026-08-19_id618-subaru-tsuji-traffic-analysis
- 優先度: 高
- ステータス: completed
- 担当者: analyst
- 作成日: 2026-08-19
- 概要: https://aidiver.jp/article/detail/618 （スバル辻氏記事）が公開時は低調だったが、お盆明けから急にPVが伸びている。GA（GA4, property p4255930）で流入元・時系列を分析し、急伸の原因を特定する。

## 要件

- 対象ページ: /article/detail/618
- 期間: 公開日〜2026-08-19（お盆前後の比較を含む）
- 分析観点:
  - 日別PV/ユーザー数の推移（いつから伸びたか）
  - 流入チャネル（Organic Search / Social / Referral / Direct 等）の変化
  - 参照元（referrer）・検索クエリ（可能なら）
  - 新規/リピーター、デバイス等の補助情報

## 成果物

- 分析レポート: data/documents/2026-08-19_id618-traffic-spike-analysis.md
- 共有用アーティファクト: https://claude.ai/code/artifact/d2ae8821-4c42-46ae-b432-a0ab969f1ccc

## 完了記録

- 完了日: 2026-08-19
- 実施内容: GA4（日別推移→参照元/メディア→デバイス→市区町村）、GSC（検索・Discover）、メルマガ配信履歴（Gmail）、はてブAPIで消去法分析
- 結論: 8/18の急伸（約400表示/日）は99%が direct/none、desktop 82%、三鷹市＋太田市（SUBARU東京事業所・群馬製作所の所在地）で64% → **お盆明けのSUBARU社内共有（イントラ/チャット/社内メール）が原因**と判断
- 棄却仮説: Discover（3ヶ月クリック0）、SEO（3ヶ月クリック6）、自社メルマガ（8/17-19号外にリンクなし）、後編波及（8/6公開で時期不一致）、SNSバズ（はてブ0・モバイル17%）
- 発生した問題と対処: GA4のUIがレンダラーフリーズ・タブクラッシュを繰り返した → レポート状態（期間・フィルタ・セカンダリディメンション）をURLパラメータで直接指定し、フレッシュロードさせる方式で回避
- 残課題: 福岡市の43表示（10.9%）は発生源未特定

## [INSIGHT]

- [INSIGHT] direct/none急増 × desktop主体 × 特定都市集中 ＝「取材先企業の社内共有」の典型シグネチャ。都市名と取材先の拠点所在地の照合が決定打になる
- [INSIGHT] GA4が重い環境では `_u.date00/_u.date01`・`_r.explorerCard..filterTerm`・`_r.explorerCard..seldim` をURL直指定して新規ロードすると安定取得できる
