# Claude Codeセッション生ログを oshikubo_storage へ差分アーカイブする
# 元ログ（~/.claude/projects/）はClaude Codeが約30日で自動削除するため、
# 週次でコピーして恒久保存する。アーカイブ側は削除しない（/MIR不使用）。

$src = "C:\Users\020168\.claude\projects"
$dstRoot = "C:\Users\020168\Documents\oshikubo_storage\99_アーカイブ\claude-session-logs"
$dst = Join-Path $dstRoot "projects"
$log = Join-Path $dstRoot "archive_log.txt"

New-Item -ItemType Directory -Force $dst | Out-Null

$stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $log -Value "=== $stamp アーカイブ開始 ===" -Encoding utf8

# /E: サブフォルダ含む全コピー /XO: アーカイブ側が新しければスキップ（差分コピー）
# 削除はしないので、元が消えてもアーカイブは残る
robocopy $src $dst /E /XO /R:2 /W:5 /NP /NDL /NFL | Out-Null
$code = $LASTEXITCODE

# robocopyの終了コード 0-7 は成功（0=差分なし, 1=コピーあり）
if ($code -le 7) {
    $fileCount = (Get-ChildItem $dst -Recurse -File | Measure-Object).Count
    $sizeMB = [math]::Round(((Get-ChildItem $dst -Recurse -File | Measure-Object Length -Sum).Sum / 1MB), 1)
    Add-Content -Path $log -Value "成功 (robocopy code: $code) / アーカイブ計: $fileCount ファイル, ${sizeMB}MB" -Encoding utf8
} else {
    Add-Content -Path $log -Value "エラー (robocopy code: $code)" -Encoding utf8
}
