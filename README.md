# B3 數位教學指引宣講簡報｜臺北市第三組（公版簡報＋臺北補充，兩套風格）

網址：https://norason666.github.io/ai-b3-1121-team/

- 公版三模組（模組一 26 頁、模組二 38 頁、模組三 62 頁）照原順序、原排版以整頁圖呈現；標「臺北補充」的頁插在相關公版頁之後
- A 套（臺北夜景・霓虹）`docs/a.html`、B 套（普普雜誌・報刊）`docs/b.html`；兩套的臺北補充案例略有不同
- 插頁對照表：`src/gb_common.py` 的 INSERT（公版第 n 頁之後插哪些標題的頁）；插頁內容來自 `src/content_a.py`（A 套案例）、`src/content.py`（B 套案例）與 `gb_common.EXTRA`
- 建置：`DECK=content_gb_a python3.13 src/build.py`、`DECK=content_gb_b python3.13 src/build.py`
- 快捷鍵：H 導覽、1／2／3 模組、←/→ 換頁、S 補充、N 講稿、T 計時、F 全螢幕
