# ブラウザ実行スニペット

`mcp__Claude_Browser__javascript_tool` にそのまま貼って実行する。
`x-serenity-watch/browser-snippets.md` の1アカウント版を、25アカウント巡回用に汎用化したもの。
違いは「対象ハンドルをURLから自動判定する」点のみ（毎回ハンドルを書き換えなくてよい）。

navigate と javascript_exec は `browser_batch` で1アカウントぶん3ステップ
（navigate → wait 3秒 → STEP 1）にまとめ、5アカウントずつ程度でバッチすると安定する。

## STEP 1: プロフィールから本人ツイートのIDとプレビュー本文を収集

事前に `https://x.com/<handle>` を navigate し、3秒待つこと。

```js
const EPOCH=1288834974657n;
const HANDLE=location.pathname.split('/')[1].toLowerCase();
const seen=new Map();
const grab=()=>{for(const a of document.querySelectorAll('article')){
  const link=Array.from(a.querySelectorAll('a[href*="/status/"]')).map(x=>x.getAttribute('href')).find(h=>/\/status\/\d+$/.test(h));
  if(!link) continue;
  const m=link.match(/^\/([^\/]+)\/status\/(\d+)/); if(!m) continue;
  if(m[1].toLowerCase()!==HANDLE) continue;   // リポスト・引用元は除外し本人ツイートのみ拾う
  const prev=a.innerText.replace(/\s+/g,' ').trim();
  if(!seen.has(m[2])||prev.length>seen.get(m[2]).length) seen.set(m[2],prev);
}};
grab();
for(let i=0;i<6;i++){ window.scrollBy(0, window.innerHeight*0.9); await new Promise(r=>setTimeout(r,900)); grab(); }
const ids=[...seen.keys()].sort((a,b)=>a<b?1:-1);
({handle:HANDLE, count:ids.length,
  newest:ids[0]||null,
  newest_at: ids.length? new Date(Number((BigInt(ids[0])>>22n)+EPOCH)).toISOString():null,
  oldest:ids[ids.length-1]||null,
  oldest_at: ids.length? new Date(Number((BigInt(ids[ids.length-1])>>22n)+EPOCH)).toISOString():null,
  items: ids.map(id=>({id, at:new Date(Number((BigInt(id)>>22n)+EPOCH)).toISOString(), preview:seen.get(id).slice(0,300)}))})
```

未ログインのため、取得できるのは**直近5〜6件前後**。`HANDLE` は現在のURLパスから自動取得するので、
25アカウント分をコピペで使い回せる（書き換え不要）。

鍵アカウントの場合は `count:0` で返る（記事要素自体が存在しないか、本人ツイートへのリンクが取れない）。
`document.body.innerText` に「ポストは非公開です」「Only approved followers can see」が含まれるかで
鍵アカウント判定ができる（判定不能な場合は以下を追加で実行）。

```js
document.body.innerText.includes('ポストは非公開です') || document.body.innerText.includes('Only approved followers')
```

## STEP 2: 全文の一括取得（複数アカウント混在でよい）

事前に `https://cdn.syndication.twimg.com/tweet-result?id=<任意のID>&token=a&lang=en` を navigate
（同一オリジンにしないと CORS で fetch が失敗する）。`IDS` は**アカウントを問わず新規判定されたID全部**を
1本の配列にまとめてよい（syndication APIはID単位で取得するのでアカウントを気にする必要がない）。

```js
const IDS=["<id1>","<id2>","<id3>"];
const out=[];
for(const id of IDS){
  try{
    const r=await fetch(`https://cdn.syndication.twimg.com/tweet-result?id=${id}&token=a&lang=en`);
    if(!r.ok){ out.push({id, err:`HTTP ${r.status}`}); continue; }
    const j=await r.json();
    out.push({id, user:j.user?.screen_name||null, at:j.created_at,
              sym:(j.entities?.symbols||[]).map(s=>s.text),
              text:j.text||null, quoted:j.quoted_tweet?.text||null});
  }catch(e){ out.push({id, err:String(e)}); }
}
out
```

`text` が null / エラーの場合は購読者限定ツイート（Subscribe to unlock）か取得失敗。
STEP 1 のプレビューで判定できなければ「本文取得不可」としてログに残す。

IDが多いとき（例: 25アカウント×数件で20〜40件）は、一度に大量に fetch すると失敗しやすいので、
10件前後ずつに分けて実行するとよい。
