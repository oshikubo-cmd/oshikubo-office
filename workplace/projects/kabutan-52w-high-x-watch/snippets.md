# ブラウザ実行スニペット

`mcp__Claude_Browser__javascript_tool` にそのまま貼って実行する。
navigate と javascript_exec は `browser_batch` でまとめて流すと速い。

## STEP 1: 株探から前日比率トップ10を取得

事前に以下へ navigate すること。

```
https://kabutan.jp/warning/record_w52_high_price?&market=0&capitalization=-1&stc=code&stm=1&col=zenhiritsu
```

```js
const tb=document.querySelector('table.stock_table');
const rows=[...tb.rows].slice(1).map(r=>{
  const c=[...r.cells].map(x=>x.innerText.replace(/\s+/g,' ').trim()).filter(x=>x!=='');
  return {code:c[0], name:c[1], market:c[2], price:c[3], chg:c[4], pct:c[5]};
});
({date:document.body.innerText.match(/\d{4}年\d{1,2}月\d{1,2}日/)?.[0]||null, top10:rows.slice(0,10)})
```

セル構造は「S」（ストップ高フラグ）などの有無で列がずれるため、
空セルを落としてから前から詰める形にしてある。`S` が入った行は `chg` が `S` になるので、
`chg`/`pct` が `+123` / `+12.34%` の形になっているかを目視で確認し、ずれていたら
`c` 配列をそのまま見て取り直すこと。

## STEP 2: Yahoo!リアルタイム検索からX投稿を抽出

銘柄ごとに以下へ navigate（`<名称> OR <コード>`。README「クエリの作り方」参照）。

```
https://search.yahoo.co.jp/realtime/search?p=ティアフォー OR 593A
```

```js
await new Promise(r=>setTimeout(r,1500));
const STK=/(株|銘柄|S高|ストップ高|急騰|決算|PTS|出来高|上場|投資|チャート|寄り|終値|材料|東証|円台|[0-9]{3}[0-9A][)）])/;
const out=[];
for(const c of document.querySelectorAll('[class*="Tweet_TweetContainer"]')){
  const a=c.querySelector('a[href*="/status/"]');
  const m=a&&a.href.match(/(?:x|twitter)\.com\/([^\/?]+)\/status\/(\d+)/); if(!m) continue;
  const body=(c.querySelector('[class*="Tweet_body__"]')?.innerText||'').replace(/\s+/g,' ').trim();
  if(!STK.test(body)) continue;   // 株式文脈のない投稿を除外
  const act=((c.querySelector('[class*="Tweet_action"]')?.innerText)||'').trim()
              .split(/\s+/).map(x=>parseInt(x.replace(/[^\d]/g,''),10)||0); // [返信, RT, いいね]
  out.push({id:m[2], user:m[1], url:`https://x.com/${m[1]}/status/${m[2]}`,
            rt:act[1]||0, lk:act[2]||0,
            time:(c.querySelector('[class*="Tweet_time"]')?.innerText||'').trim(),
            text:body.slice(0,220)});
}
const u=[...new Map(out.map(o=>[o.id,o])).values()];
({q:document.title.slice(0,24), n:u.length,
  top:u.sort((a,b)=>(b.lk+b.rt*3)-(a.lk+a.rt*3)).slice(0,4)})
```

- `n` がフィルタ後の件数＝**その銘柄の話題度の目安**。0〜2件なら「Xでは話題になっていない」と報告する
- 並べ替えは `いいね + RT×3`。Yahoo!リアルタイム検索自体に人気順ソートはないので自前で並べる
- 取得できるのは新着順の直近40件程度。18時実行なら当日ザラ場〜引け後がカバーされる

## セレクタが壊れたときの調べ方

Yahoo!リアルタイム検索は CSS Modules のハッシュ付きクラス名（`Tweet_body__3tH8T` 等）を使う。
ハッシュ部分は変わりうるので、いずれも `[class*="Tweet_xxx"]` の前方一致で書いてある。
構造ごと変わった場合は以下で当たりを付ける。

```js
const c=[...document.querySelectorAll('[class*="Tweet_"]')][0]?.closest('[class*="Container"]');
[...c.querySelectorAll('*')].filter(e=>/Tweet_/.test((e.className||'').toString()))
  .map(e=>({cls:e.className.toString(), txt:e.innerText.replace(/\s+/g,' ').slice(0,60)}))
```
