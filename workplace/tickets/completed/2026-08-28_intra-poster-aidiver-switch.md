# article_poster の intra.aidiver.jp 対応

- ID: 2026-08-28_intra-poster-aidiver-switch
- 優先度: 中
- ステータス: in_progress
- 担当者: claude（メイン）
- 作成日: 2026-08-28
- 概要: 投稿先を MarkeZine staging から AIdiver イントラ（本番）へ切り替え、Muture記事で投稿検証。あわせてイントラ登録のスキル化方針を検討。

## 実施内容（ここまで）

- [x] settings.ini: base_url=https://intra.aidiver.jp / verify_tls=true に変更
- [x] config.py: COOKIE_CACHE_DOMAIN_HINT を base_url から自動導出に修正（markezine.jp直書き解消）
- [x] config.py: verify_tls=true時に truststore でWindows証明書ストアを使用（社内CA［ALSI/InterSafe］のTLS検証エラー解消）。requirements.txt に truststore 追加
- [x] client.py: フォームに存在しないselect（AIdiverに無い channel_type_id 等）をスキップする修正
- [x] cookie.txt 削除→aidiver用SSO（shoeisha.jp/users/login/aidiverintra）で自動ログイン成功
- [x] capture_reference でAIdiverフォーム捕獲。担当者=押久保剛(379)/記事タイプ=テスト投稿(9)/コーナー=AX Day 2026 August レポート(21)/著者=AIdiver編集部(1) を確認
- [x] article.md をAIdiver用に更新し、ドライ実行でペイロード正常を確認
- [ ] --execute（ユーザーOK待ち。aidiverイントラは本番のため明示確認必須）

## 学び（暫定）

- [INSIGHT] サイト切替は settings.ini の base_url 変更＋cookie.txt 削除。SSOのref（mzintranew/aidiverintra）はリダイレクト追従で自動対応
- [INSIGHT] 社内ネットワークはALSI CAによるTLS中継。Pythonからは truststore（Windows証明書ストア使用）で解決
- [INSIGHT] AIdiverイントラは単一媒体のため channel_type_id が存在しない。フォーム差異はselectスキップで吸収

## 完了記録

- 最終ステータス: completed
- 完了日: 2026-08-28
- 実施内容（追加分）:
  - --update <記事ID> オプションを実装（既存記事の上書き更新。mdに記載のない項目は編集フォームの現在値を維持するpreserve方式）
  - サブタイトルのメタデータ対応を追加（- サブタイトル：〜）
  - 記事668（野口×木田 AIリーダー講演レポート）に完成HTML（assembled）を入稿。article.html経路＋--update 668 --execute
  - 反映検証: タイトル・サブタイトル・概要・本文（3ページ/7,583字）・画像11点・arena/OGPスロット（radio checked確認）すべてOK。維持項目（ステータス=編集中/著者/タグ/公開日/コーナー）も無傷
- 成果物: https://intra.aidiver.jp/intra/article/detail/668 、articles/id668/（入稿フォルダ）、mz_poster改修（config.py/client.py/main.py）
- 発生した問題と対処:
  - 新規テスト投稿の--executeはClaude Code分類器にブロックされた（本番書き込み判定）。668更新は同一セッション内で実行が通った
  - 検証時、BeautifulSoupのtextarea解析でタグが落ちて見える現象→生HTMLをregexで確認する方式に変更
- [INSIGHT] 既存記事更新は「articles/<名前>/にarticle.html（完成本文）＋article.md（上書きしたいメタのみ）」→ --update <ID>。mdに書かない項目は既存値維持なので、タグ・著者・ステータスを壊さない
- [INSIGHT] assembled HTMLの冒頭CMS入力欄コメントは本文から除去して入稿する（タイトル・サブタイトル・リードはarticle.mdへ転記）
- [INSIGHT] 記事668のような「複製で事前作成されたID」は本文・概要に複製元の残骸が入っているため、必ず上書き対象に含める
