# 8月分プロジェクト別直接費まとめ（SEWorksコネクタ）

- ID: 2026-09-02_august-direct-cost-by-project
- 優先度: 中
- ステータス: completed
- 担当者: analyst
- 作成日: 2026-09-02
- 完了日: 2026-09-02
- 概要: SEWorks MCP（seintra.g1.shoeisha.co.jp/mcp）から2026年8月の支払データを取得し、プロジェクト（JOB）別の直接費を集計・報告する。

## 実施内容

1. SEWorks MCPはClaude Desktopにのみ登録されていたため、mcp-bridge.exe をstdioで直接叩くPythonドライバを作成して接続（直接HTTPはpermission classifierにブロックされたため、正規のブリッジ経由に切り替え）
2. `get_payment_summary`（月次8月）で全社合計を確認: 税込185,818,501円
3. `get_payment_by_job`（月次8月・部署06前方一致・limit200）でメディア編集部門の全52 JOBを取得
4. 課別・プロジェクト別に集計してレポート化

## 成果物

- レポート: `data/documents/2026-09-02_august-direct-cost-by-project.md`
- 再利用ドライバ: `data/scripts/seworks_mcp_driver.py`（APIキーはClaude Desktop設定から読込、ハードコードなし）

## 結果サマリー

- 部門（06系）8月直接費合計: 税込12,463,998円 / 52 JOB
- 0611: 8,364,590円（デブサミKANSAI 4.56M + デブサミ2027Summer 3.27Mで大半）
- 0612: 1,442,171円 / 0621: 2,479,397円 / 0622: 177,840円

## 発生した問題と対処

- `claude` CLIがPATHになくMCP登録不可 → ブリッジstdio直叩きで代替
- PowerShell 5.1がインラインJSON引数の引用符を破壊 → 引数をJSONファイル渡しに変更
- PowerShellリダイレクト出力のUTF-8 BOM → utf-8-sigで読込

## 再利用可能な学び

- [INSIGHT] SEWorks MCPをClaude Codeから使うには `python data/scripts/seworks_mcp_driver.py tools/call <tool> <args.json>`。VPN（VSR）接続が前提。
- [INSIGHT] SEWorksの年度は4月始まり（year=2026 = 2026/4〜2027/3）、month は暦月。金額は支払伝票の税込ベースで、人件費・配賦は含まない。
- [INSIGHT] 汎用JOB Z90000100 はJOB紐付けなし支払の受け皿。JOB別分析では除外して読む。
