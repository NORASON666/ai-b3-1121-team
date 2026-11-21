# B 套（普普雜誌・報刊）：公版骨架＋臺北補充（案例用 content 的那一批）
from content import S as _SRC, SHOT, ILL
from gb_common import build
OUT = "b.html"
TEMPLATE = "template_b.html"
COVER = {"org": "B3 數位教學指引工作坊｜公版簡報＋臺北補充", "h1": "115 年中小學教師<br><mark>數位與 AI 教學指引</mark>",
         "hand": "公版三模組・臺北案例", "meta": "臺北市第三組", "who": "黃馨誼・何敏華・戴貝羽・涂朝淵・周凡淇", "end": "講指引，就用老師看得到的例子"}
S = build(_SRC, COVER["who"])
