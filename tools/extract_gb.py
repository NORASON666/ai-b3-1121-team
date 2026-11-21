# 公版 PDF → 可動畫的元素：每頁拆成「背景圖形層（去掉文字與點陣圖）」＋「點陣圖元素」＋「真的文字」
# 輸出 docs/assets/gb2/<m>-<p>/bg.png、i<k>.png，以及 src/gb2_pages.json（位置以 1920×1080 為準）
# 用法：python3.13 tools/extract_gb.py <公版 PDF 目錄> [只做某頁，例如 m2-7]
import fitz, json, os, sys, re

SRC = sys.argv[1]
ONLY = sys.argv[2] if len(sys.argv) > 2 else None
ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "docs", "assets", "gb2")
FILES = {"m1": "模組一", "m2": "模組二", "m3": "模組三"}
W = 1920


def hexcolor(c):
    return "#%06x" % c


def page_parts(doc, pno, key):
    page = doc[pno]
    pw, ph = page.rect.width, page.rect.height
    s = W / pw
    d = os.path.join(OUT, key)
    os.makedirs(d, exist_ok=True)
    out = {"w": W, "h": round(ph * s), "imgs": [], "texts": []}

    # 1) 文字：以 line 為單位，取第一個 span 的字型樣式
    td = page.get_text("dict")
    rects = []
    for b in td["blocks"]:
        if b.get("type") != 0:
            continue
        for ln in b["lines"]:
            spans = [sp for sp in ln["spans"] if sp["text"].strip()]
            if not spans:
                continue
            if abs(ln["dir"][1]) > 0.5:  # 直排或旋轉的字留在背景
                continue
            # 同一行裡字級或顏色不同的字分組輸出（例：「…歷程」後面接的大字「HUMAN」）
            groups = []
            for sp in ln["spans"]:
                key2 = (round(sp["size"]), sp["color"])
                if groups and groups[-1][0] == key2:
                    groups[-1][1].append(sp)
                else:
                    groups.append((key2, [sp]))
            for _, sps in groups:
                txt = "".join(z["text"] for z in sps)
                if not txt.strip():
                    continue
                gx0 = min(z["bbox"][0] for z in sps); gy0 = min(z["bbox"][1] for z in sps)
                gx1 = max(z["bbox"][2] for z in sps); gy1 = max(z["bbox"][3] for z in sps)
                sp = max(sps, key=lambda z: len(z["text"]))
                bold = bool(sp["flags"] & 16) or "Bold" in sp["font"] or "Black" in sp["font"] or "Heavy" in sp["font"]
                out["texts"].append({"x": round(gx0 * s), "y": round(gy0 * s), "w": round((gx1 - gx0) * s), "h": round((gy1 - gy0) * s),
                                     "size": round(sp["size"] * s, 1), "color": hexcolor(sp["color"]), "bold": bold, "t": txt})
            rects.append(fitz.Rect(ln["bbox"]))

    # 2) 點陣圖保留在背景層（Canva 圖片有裁切遮罩，單獨拆出會跑位）

    # 3) 背景圖形層：刪掉文字（redaction 只動文字）與點陣圖後輸出
    for r in rects:
        page.add_redact_annot(r)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE, text=fitz.PDF_REDACT_TEXT_REMOVE)
    pm = page.get_pixmap(matrix=fitz.Matrix(s, s), alpha=False)
    pm.save(os.path.join(d, "bg.jpg"), jpg_quality=84)
    return out


def main():
    data = {}
    jp = os.path.join(ROOT, "src", "gb2_pages.json")
    if ONLY and os.path.exists(jp):
        data = json.load(open(jp))
    for m, pre in FILES.items():
        f = [x for x in os.listdir(SRC) if x.startswith(pre) and x.endswith(".pdf")][0]
        doc = fitz.open(os.path.join(SRC, f))
        for p in range(len(doc)):
            key = f"{m}-{p + 1}"
            if ONLY and key != ONLY:
                continue
            data[key] = page_parts(doc, p, key)
        doc.close()
    # 模組二 p.5 七大風險總覽上的黑色大數字 1～6 是講師分組用的 Padlet 連結（Nora 2026-11-21：去掉）
    if "m2-5" in data:
        data["m2-5"]["texts"] = [x for x in data["m2-5"]["texts"] if not (x["t"].strip().isdigit() and x["size"] >= 70 and x["color"] == "#000000")]
    json.dump(data, open(jp, "w"), ensure_ascii=False)
    print("pages", len(data))


main()
