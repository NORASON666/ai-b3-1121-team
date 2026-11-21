# 在「AI Agent 可以幫老師做什麼」之後加 Replit 刪庫案例（模組二講師口述的那件事）
# 用法：python3.13 tools/add_replit.py <content.py 路徑>
import sys
p = sys.argv[1]
c = open(p).read()
if "Replit" in c:
    print("already"); sys.exit()
new = '''
    {"t": "shotText", "kicker": "模組二｜Agent 的風險", "title": "AI Agent 刪掉公司整個資料庫",
     "img": "news_replit.png",
     "text": ["2025-07：一家公司試用 Replit 的 AI 寫程式代理人 12 天",
              "程式凍結期間，AI 沒經同意就**刪除了正式資料庫**，還一度隱瞞",
              "沒有可用的自動備份；AI 自己說「我犯了災難性的錯誤」",
              "Replit 執行長道歉，之後把正式資料庫和測試環境分開"],
     "foot": "給 AI 權限前先問：它能刪什麼？有沒有備份？誰來把關？",
     "src": "Fortune 2025-07-23（截圖）",
     "notes": "上午講師講的那個例子，就是這件事：公司太信任 AI 代理人，結果正式資料庫被刪掉，備份也救不回來。對老師的提醒：讓 AI 動手前，先想它能碰到什麼資料，學生資料一律不要交給它。",
     "sup": [{"kind": "新聞", "evidence": "媒體報導", "title": "Replit AI 代理人刪庫事件（2025-07）",
              "points": ["SaaStr 創辦人 Jason Lemkin 試用 12 天，AI 在程式凍結期間刪除正式資料庫", "當時正式與測試共用同一個資料庫，沒有可用的自動備份", "Replit 改為正式資料庫與開發資料庫分離，AI 不能修改正式資料"],
              "limits": ["資料庫筆數各報導不同（1,200 多位主管／2,400 多筆紀錄），不要引用數字"],
              "url": "https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/"}]},
'''
k = c.find('"kicker": "模組二｜應用情境"')
s = c.rfind("    {", 0, k)
depth, i = 0, s
while True:
    ch = c[i]
    if ch == "{": depth += 1
    elif ch == "}":
        depth -= 1
        if depth == 0: break
    i += 1
e = i + 2
c = c[:e] + new + c[e:]
open(p, "w").write(c)
print("added")
