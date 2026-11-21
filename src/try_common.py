# 下午試講 4 分鐘版（講師 2026-11-21 改流程：一組 5 人，每人約 4 分鐘：模組一簡報／模組二七大風險口訣／風險示例／模組三簡報／模組三教案）
# 只挑公版重點頁（公版重建頁，順序不改），加 1～2 頁臺北補充；每頁附講稿，按 N 看
import json, os
from gb_common import EXTRA

_p = os.path.join(os.path.dirname(__file__), "gb2_pages.json")
GB2 = json.load(open(_p))


def gb(key, note):
    m, p = key.split("-")
    return {"t": "gb2", "key": key, "gbno": f"公版 模組{'一二三'[int(m[1]) - 1]} p.{p}", "notes": note}


def pick(src, title):
    x = EXTRA.get(title) or next((d for d in src if d.get("title", "").startswith(title) or title in d.get("title", "")), None)
    if x:
        x = dict(x); x.pop("sec", None); x["badge"] = "臺北補充"
    return x


def deck(cover_h1, cover_hand, items, src):
    S = [{"t": "cover", "sec": "home", "notes": "4 分鐘：只講最有把握、最想分享的重點。"}]
    for it in items:
        if isinstance(it, tuple):
            S.append(gb(*it))
        else:
            x = pick(src, it)
            if x:
                S.append(x)
    S.append({"t": "closing", "notes": "謝謝大家。"})
    return S
