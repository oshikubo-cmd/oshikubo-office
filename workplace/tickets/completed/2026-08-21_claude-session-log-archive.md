# Claude Codeセッションログの恒久アーカイブ設定

- ID: 2026-08-21_claude-session-log-archive
- 優先度: 中
- ステータス: completed
- 担当者: Claude（メイン）
- 作成日: 2026-08-21
- 完了日: 2026-08-21
- 概要: Claude Codeのセッション生ログ（`~/.claude/projects/` 配下のjsonl）は既定で約30日で自動削除されるため、`oshikubo_storage/99_アーカイブ/` へ週次で差分コピーして恒久保存する仕組みを構築する。AXDセミナー（id668）野口氏の「エージェントとのワークをローデータで残す」推奨の実装。

## 実施内容

1. アーカイブスクリプト作成: `data/scripts/archive_claude_session_logs.ps1`
   - `C:\Users\020168\.claude\projects\` 全体を `oshikubo_storage\99_アーカイブ\claude-session-logs\projects\` へ robocopy /E /XO で差分コピー（削除なし＝元が消えてもアーカイブは残る）
   - 実行履歴を `archive_log.txt` に記録
2. 初回アーカイブ実行: 全オフィス分 135ファイル・145.3MB を保存
3. Windowsタスクスケジューラに「Claude Session Log Archive」を登録（毎週月曜 9:30、ユーザーログオン時実行）
4. スケジューラ経由の実行を検証: 終了コード0で成功

## 成果物

- `data/scripts/archive_claude_session_logs.ps1`
- タスクスケジューラ登録「Claude Session Log Archive」
- `oshikubo_storage\99_アーカイブ\claude-session-logs\`（アーカイブ本体＋実行ログ）

## 発生した問題と対処

- BOMなしUTF-8の.ps1をPowerShell 5.1がANSIとして誤読しパースエラー → BOM付きUTF-8に変換して解決
- schtasks /Createは引数内のクォートエスケープで失敗 → Register-ScheduledTaskコマンドレットで登録して解決

## 再利用可能な学び

- [INSIGHT] 日本語コメント入りの.ps1はUTF-8 BOM付きで保存しないとPowerShell 5.1でパースエラーになる
- [INSIGHT] Claude Codeのセッション生ログは既定30日で自動削除（cleanupPeriodDays未設定時）。恒久保存にはstorageへの差分アーカイブが確実
- [INSIGHT] タスクスケジューラ登録はschtasksよりRegister-ScheduledTaskの方がクォート問題を回避できる
