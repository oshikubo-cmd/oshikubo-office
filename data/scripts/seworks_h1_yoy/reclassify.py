# Offline re-classification of saved sales/payment raw files (adds ECzine; splits media into event/media-ops/other)
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "h1_raw")
MONTHS = [4, 5, 6, 7, 8]
YEARS = [2025, 2026]

job_sec = {}
for fn in os.listdir(RAW):
    if fn.startswith("jobmap_"):
        for ln in open(os.path.join(RAW, fn), encoding="utf-8"):
            m = re.match(r"^(\S+)\s+\|\s(.+?)\s*\|\s+(\d{4})\s\|", ln)
            if m:
                job_sec[m.group(1)] = m.group(3)

MEDIA_PAT = re.compile(
    r"CodeZine|MarkeZine|EnterpriseZine|Biz/Zine|HRzine|HRZine|AIdiver|AIDiver|ProductZine|CreatorZine|SalesZine|"
    r"CommerceZine|ECzine|Developers Summit|デブサミ|AX Day|Security Online", re.I)
MONTHLY_PAT = re.compile(r"\s20\d{4}$")
EVENT_PAT = re.compile(r"Day 20|Summit|Forum|FORUM|デブサミ|カンファレンス|Conference|（20\d{6}", re.I)

def classify(job, name):
    sec = job_sec.get(job)
    if sec and sec.startswith("06"):
        return "media"
    if sec and sec.startswith("07"):
        return "bp"
    if sec:
        return "other"
    return "media" if MEDIA_PAT.search(name) else "other"

def subtype(name):
    if MONTHLY_PAT.search(name):
        return "媒体月次"
    if EVENT_PAT.search(name):
        return "イベント"
    return "書籍・その他"

sales = {}
sub = {}
rowcounts = {}
for y in YEARS:
    for mth in MONTHS:
        fn = os.path.join(RAW, f"sales_job_{y}_{mth:02d}.txt")
        n = 0
        for ln in open(fn, encoding="utf-8"):
            m = re.match(r"^(\S+)\s+\|\s+(-?[\d,]+)円\s+\|\s+\d+\s+\|\s+\d+\s+\|\s+\d+\s+\|\s?(.*)$", ln)
            if not m:
                continue
            n += 1
            job, amt, name = m.group(1), int(m.group(2).replace(",", "")), m.group(3).strip()
            g = classify(job, name)
            sales[(y, mth, g)] = sales.get((y, mth, g), 0) + amt
            if g == "media":
                st = subtype(name)
                sub[(y, st)] = sub.get((y, st), 0) + amt
        rowcounts[(y, mth)] = n

print("== 売上 月次（再分類後） ==")
print("year\tmonth\tmedia\tother\trows")
for y in YEARS:
    for mth in MONTHS:
        print(f"{y}\t{mth}\t{sales.get((y,mth,'media'),0):,}\t{sales.get((y,mth,'other'),0):,}\t{rowcounts[(y,mth)]}")
print()
print("== 売上 4-8月累計 ==")
for y in YEARS:
    tm = sum(sales.get((y, m, "media"), 0) for m in MONTHS)
    to = sum(sales.get((y, m, "other"), 0) for m in MONTHS)
    tb = sum(sales.get((y, m, "bp"), 0) for m in MONTHS)
    print(f"{y}: media={tm:,}  bp={tb:,}  other={to:,}")
print()
print("== media売上の内訳（4-8月累計） ==")
for (y, st), amt in sorted(sub.items()):
    print(f"{y}\t{st}\t{amt:,}")
