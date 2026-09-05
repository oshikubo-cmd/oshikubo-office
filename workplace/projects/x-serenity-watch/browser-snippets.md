# ブラウザ実行スニペット

`mcp__Claude_Browser__javascript_tool` にそのまま貼って実行する。

## STEP 1: プロフィールから本人ツイートのIDとプレビュー本文を収集

事前に `https://x.com/aleabitoreddit` を navigate し、3秒待つこと。

```js
const EPOCH=1288834974657n;
const seen=new Map();
const grab=()=>{for(const a of document.querySelectorAll('article')){
  const link=Array.from(a.querySelectorAll('a[href*="/status/"]')).map(x=>x.getAttribute('href')).find(h=>/\/status\/\d+$/.test(h));
  if(!link) continue;
  const m=link.match(/^\/([^\/]+)\/status\/(\d+)/); if(!m) continue;
  if(m[1].toLowerCase()!=='aleabitoreddit') continue;
  const prev=a.innerText.replace(/\s+/g,' ').trim();
  if(!seen.has(m[2])||prev.length>seen.get(m[2]).length) seen.set(m[2],prev);
}};
grab();
for(let i=0;i<8;i++){ window.scrollBy(0, window.innerHeight*0.9); await new Promise(r=>setTimeout(r,900)); grab(); }
const ids=[...seen.keys()].sort((a,b)=>a<b?1:-1);
({count:ids.length,
  newest:ids[0], oldest:ids[ids.length-1],
  oldest_at: ids.length? new Date(Number((BigInt(ids[ids.length-1])>>22n)+EPOCH)).toISOString():null,
  items: ids.map(id=>({id, at:new Date(Number((BigInt(id)>>22n)+EPOCH)).toISOString(), preview:seen.get(id).slice(0,400)}))})
```

未ログインのため、取得できるのは**直近6件前後**。`oldest_at` が前回実行時刻より新しい場合は
取りこぼしが発生している（ギャップ）ので、通知にその旨を添える。

## STEP 2: 全文の一括取得

事前に `https://cdn.syndication.twimg.com/tweet-result?id=<任意のID>&token=a&lang=en` を navigate
（同一オリジンにしないと CORS で fetch が失敗する）。`IDS` を STEP 1 の新規ID配列に差し替えて実行。

```js
const IDS=["<id1>","<id2>"];
const out=[];
for(const id of IDS){
  try{
    const r=await fetch(`https://cdn.syndication.twimg.com/tweet-result?id=${id}&token=a&lang=en`);
    if(!r.ok){ out.push({id, err:`HTTP ${r.status}`}); continue; }
    const j=await r.json();
    out.push({id, at:j.created_at, sym:(j.entities?.symbols||[]).map(s=>s.text),
              text:j.text||null, quoted:j.quoted_tweet?.text||null});
  }catch(e){ out.push({id, err:String(e)}); }
}
out
```

`text` が null / エラーの場合は購読者限定ツイート（Subscribe to unlock）。本文は取得できないので
STEP 1 のプレビューで判定し、判定不能なら「本文取得不可」としてログに残す。
