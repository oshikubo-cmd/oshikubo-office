# -*- coding: utf-8 -*-
"""Anthropic spend report CSV を集計する。

入力: 管理コンソールの spend report CSV
出力: 標準出力に JSON（集計結果）

集計条件:
- net/gross spend は全件 0（シート課金契約のため）なので、
  トークン量から公開API従量課金レートで「推定従量換算額」を算出する。
- 単価は Anthropic 公開API価格（2026-08時点、USD / 1M tokens）。
  cache read = input x 0.1、cache write 5m = input x 1.25、cache write 1h = input x 2.0
"""
import csv
import json
import sys
from collections import defaultdict

PRICE = {
    "claude-fable-5": (10.0, 50.0),
    "claude-opus-5": (5.0, 25.0),
    "claude-opus-4-8": (5.0, 25.0),
    "claude-opus-4-7": (5.0, 25.0),
    "claude-opus-4-6": (5.0, 25.0),
    "claude-sonnet-5": (3.0, 15.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5-20251001": (1.0, 5.0),
}
TIER = {
    "claude-fable-5": "Fable 5",
    "claude-opus-5": "Opus 5",
    "claude-opus-4-8": "Opus 4.8",
    "claude-opus-4-7": "Opus 4.7",
    "claude-opus-4-6": "Opus 4.6",
    "claude-sonnet-5": "Sonnet 5",
    "claude-sonnet-4-6": "Sonnet 4.6",
    "claude-haiku-4-5-20251001": "Haiku 4.5",
}
FAMILY = {
    "claude-fable-5": "Fable",
    "claude-opus-5": "Opus",
    "claude-opus-4-8": "Opus",
    "claude-opus-4-7": "Opus",
    "claude-opus-4-6": "Opus",
    "claude-sonnet-5": "Sonnet",
    "claude-sonnet-4-6": "Sonnet",
    "claude-haiku-4-5-20251001": "Haiku",
}

INT_COLS = [
    "total_requests", "total_prompt_tokens", "total_completion_tokens",
    "total_uncached_input_tokens", "total_cache_read_tokens",
    "total_cache_write_5m_tokens", "total_cache_write_1h_tokens",
    "total_web_search_count",
]


def blank():
    d = {c: 0 for c in INT_COLS}
    d["est_usd"] = 0.0
    d["rows"] = 0
    return d


def add(dst, row, est):
    for c in INT_COLS:
        dst[c] += row[c]
    dst["est_usd"] += est
    dst["rows"] += 1


def main(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            for c in INT_COLS:
                r[c] = int(r[c] or 0)
            r["net"] = float(r["total_net_spend_usd"] or 0)
            r["gross"] = float(r["total_gross_spend_usd"] or 0)
            rows.append(r)

    total = blank()
    by_user = defaultdict(blank)
    by_product = defaultdict(blank)
    by_model = defaultdict(blank)
    by_family = defaultdict(blank)
    by_user_product = defaultdict(blank)
    user_models = defaultdict(set)
    user_products = defaultdict(set)
    net_sum = gross_sum = 0.0
    unknown_models = set()

    for r in rows:
        m = r["model"]
        if m not in PRICE:
            unknown_models.add(m)
            est = 0.0
        else:
            pin, pout = PRICE[m]
            est = (
                r["total_uncached_input_tokens"] * pin
                + r["total_cache_read_tokens"] * pin * 0.1
                + r["total_cache_write_5m_tokens"] * pin * 1.25
                + r["total_cache_write_1h_tokens"] * pin * 2.0
                + r["total_completion_tokens"] * pout
            ) / 1000000
        r["est_usd"] = est
        net_sum += r["net"]
        gross_sum += r["gross"]
        u = r["user_email"]
        add(total, r, est)
        add(by_user[u], r, est)
        add(by_product[r["product"]], r, est)
        add(by_model[TIER.get(m, m)], r, est)
        add(by_family[FAMILY.get(m, "unknown")], r, est)
        add(by_user_product[(u, r["product"])], r, est)
        user_models[u].add(TIER.get(m, m))
        user_products[u].add(r["product"])

    def srt(d):
        return sorted(d.items(), key=lambda kv: -kv[1]["total_requests"])

    def pack(d, count_users=False):
        out = []
        for k, v in srt(d):
            pt = v["total_prompt_tokens"]
            item = {
                "key": k,
                "requests": v["total_requests"],
                "prompt_tokens": pt,
                "completion_tokens": v["total_completion_tokens"],
                "uncached_input": v["total_uncached_input_tokens"],
                "cache_read": v["total_cache_read_tokens"],
                "cache_write": v["total_cache_write_5m_tokens"] + v["total_cache_write_1h_tokens"],
                "web_search": v["total_web_search_count"],
                "est_usd": round(v["est_usd"], 2),
                "tokens_per_req": round(pt / v["total_requests"]) if v["total_requests"] else 0,
            }
            if count_users:
                item["users"] = len({u for (u, p) in by_user_product if p == k})
            out.append(item)
        return out

    users = []
    for u, v in srt(by_user):
        pt = v["total_prompt_tokens"]
        users.append({
            "user": u,
            "requests": v["total_requests"],
            "prompt_tokens": pt,
            "completion_tokens": v["total_completion_tokens"],
            "uncached_input": v["total_uncached_input_tokens"],
            "cache_read": v["total_cache_read_tokens"],
            "cache_write": v["total_cache_write_5m_tokens"] + v["total_cache_write_1h_tokens"],
            "web_search": v["total_web_search_count"],
            "est_usd": round(v["est_usd"], 2),
            "tokens_per_req": round(pt / v["total_requests"]) if v["total_requests"] else 0,
            "products": sorted(user_products[u]),
            "models": sorted(user_models[u]),
            "by_product": {p: by_user_product[(uu, p)]["total_requests"]
                           for (uu, p) in by_user_product if uu == u},
        })

    tp = total["total_prompt_tokens"]
    result = {
        "source": path,
        "period": "2026-05-21 - 2026-08-19",
        "row_count": len(rows),
        "totals": {
            "users": len(by_user),
            "requests": total["total_requests"],
            "prompt_tokens": tp,
            "completion_tokens": total["total_completion_tokens"],
            "uncached_input": total["total_uncached_input_tokens"],
            "cache_read": total["total_cache_read_tokens"],
            "cache_write_5m": total["total_cache_write_5m_tokens"],
            "cache_write_1h": total["total_cache_write_1h_tokens"],
            "web_search": total["total_web_search_count"],
            "net_spend_usd": net_sum,
            "gross_spend_usd": gross_sum,
            "est_usd": round(total["est_usd"], 2),
            "cache_read_ratio": round(total["total_cache_read_tokens"] / tp * 100, 1),
            "tokens_per_req": round(tp / total["total_requests"]),
            "output_per_req": round(total["total_completion_tokens"] / total["total_requests"]),
        },
        "by_product": pack(by_product, count_users=True),
        "by_model": pack(by_model),
        "by_family": pack(by_family),
        "by_user": users,
        "unknown_models": sorted(unknown_models),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
