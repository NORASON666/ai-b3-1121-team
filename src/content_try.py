# 下午試講合併版（一份）：模組一 → 模組二（不含七大風險）→ 模組三簡報 → 模組三教案說課，各約 4 分鐘
import content_try1 as A, content_try2b as M2, content_try3 as B, content_g3m3 as C
SHOT, ILL = A.SHOT, A.ILL
OUT = "try.html"
CHIP = [("m1", "模組一"), ("m2", "模組二"), ("m3", "模組三"), ("end", "教案")]
TEMPLATE = "template_a.html"
COVER = {"org": "B3 儲備講師試講｜臺北市第三組", "h1": "模組一、二、三＋教案<br><mark>試講</mark>",
         "hand": "每段約 4 分鐘｜按 N 看講稿", "meta": "公版重點頁＋臺北補充＋教案說課",
         "who": "黃馨誼・何敏華・戴貝羽・涂朝淵・周凡淇", "end": "先讓學生想，再讓 AI 問"}


def body(S):
    return [d for d in S if d["t"] not in ("cover", "closing")]


def sec(title, who, k):
    return {"t": "quote", "sec": k, "kicker": who, "title": "", "text": title, "notes": ""}


S = ([{"t": "cover", "sec": "home", "notes": "第三組試講：模組一、模組三簡報、模組三教案，各約 4 分鐘。"}]
     + [sec("① 模組一｜理解指引", "第 1 位｜約 4 分鐘", "m1")] + body(A.S)
     + [sec("② 模組二", "第 2 位｜約 4 分鐘", "m2")] + body(M2.S)
     + [sec("③ 模組三｜AI 賦能教學", "第 3 位｜約 4 分鐘", "m3")] + body(B.S)
     + [sec("④ 模組三教案說課\n郭怡君〈植物如何獲得養分〉", "第 4 位｜約 4 分鐘", "end")] + body(C.S)
     + [{"t": "closing", "notes": "謝謝大家。"}])
