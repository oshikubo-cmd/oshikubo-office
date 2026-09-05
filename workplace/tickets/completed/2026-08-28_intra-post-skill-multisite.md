# イントラ入稿のスキル化とマルチサイト対応

- ID: 2026-08-28_intra-post-skill-multisite
- 優先度: 高
- ステータス: in_progress
- 担当者: claude（メイン）
- 作成日: 2026-08-28
- 概要: article_poster を EnterpriseZine / CodeZine / MarkeZine / Bizzine の各イントラにも対応させ、入稿手順をスキル化。セミナーレポートスキルと合わせた社内共有手順も整理する。

## タスクリスト

- [x] config.py: 環境変数 MZ_POSTER_BASE_URL によるサイト切替＋Cookieファイルのサイト別分離（cookie_<host>.txt）＋TLS検証の自動既定（stagingのみ非検証）
- [x] 5サイトのログイン・フォーム構造を確認（全サイト同一SSO資格情報で自動ログイン成功）
  - チャンネル欄なし: aidiver / bizzine
  - チャンネル欄あり: markezine（MarkeZine/CommerceZine/SalesZine）、codezine（CodeZine/DeveloperZine/ProductZine）、enterprisezine（DBオンライン/セキュリティオンライン/エンタープライズジン/財務・会計Online）
- [x] .claude/skills/intra-post/SKILL.md を作成
- [x] 社内共有手順の整理（最終報告に記載）

## 発生した問題

- 5サイト連続ログイン＋検証GETの連打後、intra.aidiver.jp が全ページ403（nginx/WAFのレート制限とみられる一時ブロック）。90秒間隔で解除を監視中。スキルにも注意事項として追記済み
- [INSIGHT] イントラへのプログラムアクセスは頻度を抑える。サイト横断の一括検証はやらない方がよい

## 完了記録

- 最終ステータス: completed
- 完了日: 2026-08-28
- 実施内容:
  - マルチサイト対応（MZ_POSTER_BASE_URL環境変数・cookie_<host>.txt分離・TLS検証自動既定）
  - .claude/skills/intra-post/ 作成（入稿手順・5サイト対応表・安全ルール・レート制限注意）
  - .claude/skills/seminar-report-writer/ 作成（claude.aiアカウント側スキルの実体を AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\ 配下から発見しファイル版として複製。共有可能に）
  - 403ブロックは約50分で自然解除を確認。解除後にaidiverでdry-run疎通確認OK
- 成果物: .claude/skills/intra-post/SKILL.md、.claude/skills/seminar-report-writer/SKILL.md、mz_poster改修（config.py）
- [INSIGHT] anthropic-skills系（claude.aiアカウント側）スキルの実体は AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\<uuid>\<uuid>\skills\ にある。Skillツールで起動するとベースディレクトリが表示されるので、それで実パスを特定できる
- [INSIGHT] イントラWAFの403ブロックは今回約50分で解除された（恒久ブロックではない）

## 追記（2026-08-28）

- 共有用zipを作成: `oshikubo_storage\02_社内資料・データ\セミナーレポート＆イントラ入稿スキルセット_2026-08-28.zip`（30ファイル・0.15MB）
- 収録: article_poster改修版（cookie*・実記事フォルダ・__pycache__除外を機械検証済み）＋スキル2種＋受領者向けREADME（セットアップ6手順）

## 追記2（2026-08-28）: CMS変更検知ダイアログの解消

- 事象: 記事668をブラウザの管理画面で登録しようとすると「変更した箇所があります」ダイアログが全行ピンクで表示される
- 原因: スクリプトはLF改行で本文を保存、ブラウザのフォーム送信はCRLF。全行が変更扱いになりCMSの変更検知が発火
- 対処: client.pyに_to_crlf()を追加し、body_formatted/summaryを送信前にCRLF正規化。記事668は同一内容のままCRLFで再保存（CRLF:154/LF:2となり手動保存記事667と同パターンに）
- [INSIGHT] CMSのtextareaはCRLF基準。スクリプト投稿する本文は必ずCRLFに正規化する（共有済みzipにはこの修正が未反映→再作成要）
- 2026-08-28 ユーザー確認: CRLF再保存後、ブラウザ管理画面から通常どおり更新できることを確認（解消済み）
