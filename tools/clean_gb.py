# 公版重建資料清理（Nora 2026-11-21 檢查回報後加）：
# ① 去掉疊影：Canva 的陰影／外框會產生同字重複的文字層，保留最上層
# ② 去掉指定的字：模組二 p.11 標題「This is a real photo, isn't it?」、p.5 講師分組用黑色數字
# ③ 找出與前一頁完全相同的頁（公版本身重複），寫進 skip 清單
import json, hashlib, os, unicodedata
ROOT = os.path.join(os.path.dirname(__file__), "..")
p = os.path.join(ROOT, "src", "gb2_pages.json")
d = json.load(open(p))
norm = lambda s: unicodedata.normalize("NFKC", s).replace(" ", "").replace("‌", "")


def box(t): return (t["x"], t["y"], t["x"] + t["w"], t["y"] + t["h"])


def inter(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0]); h = min(a[3], b[3]) - max(a[1], b[1])
    return max(0, w) * max(0, h)


removed = 0
for k, v in d.items():
    T = v["texts"]; keep = []
    for i, t in enumerate(T):
        a = box(t); area = max(1, (a[2] - a[0]) * (a[3] - a[1])); drop = False
        for L in T[i + 1:]:
            if abs(L["size"] - t["size"]) > 1.5:
                continue
            b = box(L); bl = max(1, (b[2] - b[0]) * (b[3] - b[1])); it = inter(a, b)
            if norm(L["t"]) == norm(t["t"]) and it / area > 0.5:   # 同字疊影
                drop = True; break
            if it / bl > 0.7 and norm(L["t"]) in norm(t["t"]) and len(norm(L["t"])) < len(norm(t["t"])):  # 整行被拆字的上層覆蓋
                drop = True; break
        if not drop:
            keep.append(t)
        else:
            removed += 1
    v["texts"] = keep

if "m2-11" in d:
    d["m2-11"]["texts"] = [t for t in d["m2-11"]["texts"] if "real photo" not in t["t"]]
if "m2-5" in d:
    d["m2-5"]["texts"] = [t for t in d["m2-5"]["texts"] if not (t["t"].strip().isdigit() and t["size"] >= 70 and t["color"] == "#000000")]

skip, prev = [], None
for m, n in (("m1", 26), ("m2", 38), ("m3", 62)):
    prev = None
    for i in range(1, n + 1):
        k = f"{m}-{i}"
        if k not in d: continue
        sig = hashlib.md5(open(os.path.join(ROOT, "docs/assets/gb2", k, "bg.jpg"), "rb").read()).hexdigest() + json.dumps([t["t"] for t in d[k]["texts"] if not t["t"].strip().isdigit()], ensure_ascii=False)
        if sig == prev:
            skip.append(k)
        prev = sig
d["_skip"] = skip
json.dump(d, open(p, "w"), ensure_ascii=False)
print("removed dup texts", removed, "skip pages", skip)
