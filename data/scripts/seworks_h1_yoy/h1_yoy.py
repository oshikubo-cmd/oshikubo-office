# H1 (Apr-Aug) YoY: media-editing dept (06xx) vs business-produce dept (07xx)
# Payments by section + sales by JOB (mapped to dept via payment-derived JOB->section map + name patterns).
import json, os, re, subprocess, sys, threading, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BRIDGE = r"C:\Users\020168\seworks-mcp\mcp-bridge.exe"
ARGS = ["--name", "seworks-mcp", "--url", "https://seintra.g1.shoeisha.co.jp/mcp", "--label", "SEWorks"]
CONFIG = os.path.join(os.environ["APPDATA"], "Claude", "claude_desktop_config.json")
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "h1_raw")
os.makedirs(OUTDIR, exist_ok=True)

with open(CONFIG, encoding="utf-8") as f:
    key = json.load(f)["mcpServers"]["seworks-mcp"]["env"]["SEWORKS_MCP_API_KEY"]
env = os.environ.copy()
env["SEWORKS_MCP_API_KEY"] = key

proc = subprocess.Popen([BRIDGE] + ARGS, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL, env=env)
_id = [0]

def rpc(method, params):
    _id[0] += 1
    proc.stdin.write((json.dumps({"jsonrpc": "2.0", "id": _id[0], "method": method, "params": params}) + "\n").encode())
    proc.stdin.flush()
    while True:
        line = proc.stdout.readline()
        if not line:
            raise RuntimeError("bridge closed")
        line = line.strip()
        if not line:
            continue
        msg = json.loads(line)
        if msg.get("id") == _id[0]:
            return msg

rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "claude-code", "version": "1.0"}})
proc.stdin.write((json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n").encode())
proc.stdin.flush()

def call(tool, args, save_as):
    res = rpc("tools/call", {"name": tool, "arguments": args})
    text = res["result"]["content"][0]["text"]
    with open(os.path.join(OUTDIR, save_as), "w", encoding="utf-8") as f:
        f.write(text)
    return text

MONTHS = [4, 5, 6, 7, 8]
YEARS = [2025, 2026]

# ---- 1. payments by section, monthly ----
pay = {}  # (year, month, secgroup) -> amount ; secgroup in {"06","07","other"}
pay_sec_detail = {}  # (year, sec) -> total over months
for y in YEARS:
    for m in MONTHS:
        text = call("get_payment_by_job",
                    {"year": y, "period_type": "monthly", "month": m, "group_by": "section", "limit": 60},
                    f"pay_sec_{y}_{m:02d}.txt")
        header = text.splitlines()[0]
        for ln in text.splitlines():
            mm = re.match(r"^\s*(\d{4})\s*\|\s*(.+?)\s*\|\s*([\d,]+)円", ln)
            if not mm:
                continue
            sec, name, amt = mm.group(1), mm.group(2), int(mm.group(3).replace(",", ""))
            grp = "06" if sec.startswith("06") else ("07" if sec.startswith("07") else "other")
            pay[(y, m, grp)] = pay.get((y, m, grp), 0) + amt
            k = (y, sec + " " + name)
            pay_sec_detail[k] = pay_sec_detail.get(k, 0) + amt
        print(f"pay {y}-{m:02d} ok [{header[:40]}]", file=sys.stderr)

# ---- 2. JOB -> section map from yearly payment job lists ----
job_sec = {}
for y in YEARS:
    for secpfx in ["06", "07"]:
        text = call("get_payment_by_job",
                    {"year": y, "period_type": "yearly", "section_code": secpfx, "limit": 500},
                    f"jobmap_{secpfx}_{y}.txt")
        for ln in text.splitlines():
            mm = re.match(r"^(\S+)\s+\|\s(.+?)\s*\|\s+(\d{4})\s\|", ln)
            if mm:
                job_sec[mm.group(1)] = mm.group(3)
        print(f"jobmap {secpfx} {y}: total {len(job_sec)}", file=sys.stderr)

MEDIA_PAT = re.compile(
    r"CodeZine|MarkeZine|EnterpriseZine|Biz/Zine|HRzine|AIdiver|AIDiver|ProductZine|CreatorZine|SalesZine|CommerceZine|"
    r"Developers Summit|デブサミ|AX Day|Security Online|SalesZine Day|MarkeZine Day|ProductZine Day|EnterpriseZine Day", re.I)

def classify(job, name):
    sec = job_sec.get(job)
    if sec:
        if sec.startswith("06"):
            return "media"
        if sec.startswith("07"):
            return "bp"
        return "other"
    if MEDIA_PAT.search(name):
        return "media?"  # pattern-matched, no payment record
    return "other"

# ---- 3. sales by JOB, monthly ----
sales = {}  # (year, month, grp) -> amount
uncl = {}   # top unclassified rows for audit: (year) -> list
media_rows = {}
for y in YEARS:
    for m in MONTHS:
        text = call("get_sales_summary",
                    {"year": y, "period_type": "monthly", "month": m, "group_by": "job", "limit": 2000},
                    f"sales_job_{y}_{m:02d}.txt")
        n = 0
        for ln in text.splitlines():
            mm = re.match(r"^(\S+)\s+\|\s+(-?[\d,]+)円\s+\|\s+\d+\s+\|\s+\d+\s+\|\s+\d+\s+\|\s?(.*)$", ln)
            if not mm:
                continue
            n += 1
            job, amt, name = mm.group(1), int(mm.group(2).replace(",", "")), mm.group(3).strip()
            grp = classify(job, name)
            g = "media" if grp.startswith("media") else grp
            sales[(y, m, g)] = sales.get((y, m, g), 0) + amt
            if grp in ("media", "media?"):
                media_rows.setdefault(y, []).append((amt, job, name, grp))
            elif abs(amt) >= 1000000:
                uncl.setdefault(y, []).append((amt, job, name))
        print(f"sales {y}-{m:02d}: {n} rows", file=sys.stderr)

# ---- report ----
def fmt(v):
    return f"{v:,}"

print("== 直接費（支払伝票・税込） 月次 ==")
print("year\tmonth\t06media\t07bp\tother")
for y in YEARS:
    for m in MONTHS:
        print(f"{y}\t{m}\t{fmt(pay.get((y,m,'06'),0))}\t{fmt(pay.get((y,m,'07'),0))}\t{fmt(pay.get((y,m,'other'),0))}")
print()
print("== 直接費 4-8月累計 ==")
for y in YEARS:
    t06 = sum(pay.get((y, m, "06"), 0) for m in MONTHS)
    t07 = sum(pay.get((y, m, "07"), 0) for m in MONTHS)
    print(f"{y}: media(06xx)={fmt(t06)}  bp(07xx)={fmt(t07)}")
print()
print("== 部署別 直接費 4-8月累計（06/07のみ） ==")
for (y, secname), amt in sorted(pay_sec_detail.items()):
    if secname[:2] in ("06", "07"):
        print(f"{y}\t{secname}\t{fmt(amt)}")
print()
print("== 売上（JOB別を部門に分類） 月次 ==")
print("year\tmonth\tmedia\tbp\tother")
for y in YEARS:
    for m in MONTHS:
        print(f"{y}\t{m}\t{fmt(sales.get((y,m,'media'),0))}\t{fmt(sales.get((y,m,'bp'),0))}\t{fmt(sales.get((y,m,'other'),0))}")
print()
print("== 売上 4-8月累計 ==")
for y in YEARS:
    tm = sum(sales.get((y, m, "media"), 0) for m in MONTHS)
    tb = sum(sales.get((y, m, "bp"), 0) for m in MONTHS)
    to = sum(sales.get((y, m, "other"), 0) for m in MONTHS)
    print(f"{y}: media={fmt(tm)}  bp={fmt(tb)}  other={fmt(to)}")
print()
print("== media分類の上位JOB（確認用, 各年上位25） ==")
for y in YEARS:
    agg = {}
    for amt, job, name, grp in media_rows.get(y, []):
        k = (job, name, grp)
        agg[k] = agg.get(k, 0) + amt
    for (job, name, grp), amt in sorted(agg.items(), key=lambda x: -x[1])[:25]:
        print(f"{y}\t{job}\t{fmt(amt)}\t{grp}\t{name[:40]}")
print()
print("== 未分類の大口JOB（100万円以上, 確認用, 各年上位15） ==")
for y in YEARS:
    agg = {}
    for amt, job, name in uncl.get(y, []):
        k = (job, name)
        agg[k] = agg.get(k, 0) + amt
    for (job, name), amt in sorted(agg.items(), key=lambda x: -x[1])[:15]:
        print(f"{y}\t{job}\t{fmt(amt)}\t{name[:40]}")

proc.stdin.close()
proc.terminate()
