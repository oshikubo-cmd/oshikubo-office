# 日本企業・日本株 検出キーワード

判定の出発点となるリスト。**このリストは網羅ではない。** リストにない日本企業名・日本の地名文脈でも、
日本企業への言及と読めるものはすべて拾うこと（例: 未上場のRapidus、社名の略称、工場名など）。

## 1. 4桁銘柄コード

`\b(1[0-9]{3}|[2-9][0-9]{3})\b` に加え、以下の主要コードは確実に拾う。
数字単体は誤検出しやすいので、株・銘柄・TSE・Tokyo・Japan などの文脈語とセットのときのみヒット扱いにする。

8035 6857 6146 7735 6920 6525 6728 7729 6315 7751 7731 6925 6951
4063 3436 4185 4186 4004 6988 3402 2802 4901 7741 5201 4021
4062 6967 5334 6971 6981 6762 6976 6963
6723 6758 6526 6503 6501 5803 5801 5802 6954 6861 9984 9432
6701 6702 6752 6594 6506 6324 6481 6480 6965 6856
8031 8058 8001 8053 8002 285A

## 2. 社名（英語表記・略称）

### 半導体製造装置
Tokyo Electron, TEL, Advantest, Disco Corp, DISCO, SCREEN Holdings, Screen Semiconductor,
Lasertec, Kokusai Electric, Ulvac, ULVAC, Tokyo Seimitsu, Accretech, Towa Corp,
Shibaura Mechatronics, Canon Anelva, Canon Tokki, Nikon, Ushio, JEOL, Hitachi High-Tech,
Hitachi Kokusai, Rorze, Daifuku

### 材料・化学
Shin-Etsu, Shin Etsu, SUMCO, JSR Corp, Tokyo Ohka, TOK, Resonac, Showa Denko,
Nitto Denko, Toray, Sumitomo Bakelite, Ajinomoto, ABF (Ajinomoto Build-up Film),
Fujifilm, FUJIFILM, Hoya, HOYA, AGC Inc, Asahi Glass, Nissan Chemical,
Mitsui Chemicals, Sumitomo Chemical, Kaneka, Zeon, Denka

### 基板・実装・電子部品
Ibiden, IBIDEN, Shinko Electric, Nippon Mektron, NGK Insulators, NGK Spark,
Niterra, Kyocera, Murata, Taiyo Yuden, TDK, Rohm, ROHM, Nichicon, Nitto Boseki,
Mitsui Mining and Smelting, Mitsui Kinzoku

### 半導体・デバイス
Renesas, Sony Semiconductor, Sony, Kioxia, Toshiba, Rapidus, Socionext,
Fuji Electric, Mitsubishi Electric, Sanken, Toshiba Electronic Devices

### 電機・機械・その他
Hitachi, Fujikura, Furukawa Electric, Sumitomo Electric, Mitsubishi Heavy,
Fanuc, FANUC, Keyence, SoftBank, NTT, NEC, Fujitsu, Panasonic, Nidec,
Yaskawa, Harmonic Drive, THK, NSK, NTN, Nippon Thompson, IKO,
Hamamatsu Photonics, Anritsu, Yokogawa, Horiba, Nabtesco, Omron, Makita

### 商社・金融
Mitsui, Mitsubishi Corp, Itochu, Sumitomo Corp, Marubeni, Sojitz,
Nomura, Daiwa, SMBC, MUFG, Mizuho

## 3. 市場・国レベルの文脈語

Japan, Japanese, Nippon, Nikkei, TOPIX, TSE, Tokyo Stock Exchange,
JPY, yen, BOJ, Bank of Japan, METI, Kumamoto, Kikuyo, Yokkaichi, Hiroshima fab,
JASM, Japan Advanced Semiconductor Manufacturing

## 4. 除外（誤ヒットしやすい語）

- `$ASE` → 台湾ASE または暗号通貨Asentum。日本企業ではない
- `Powertech` → 台湾PTI
- `Samsung / SK Hynix / TSMC / UMC / Foxconn` → 日本企業ではない
- `Nikon` の写真文脈、`Sony` のゲーム・音楽のみの文脈は、株・サプライチェーンの話でなければ通知不要と判断してよい
  （ただし迷ったら通知する。取りこぼしのほうが損失が大きい）
