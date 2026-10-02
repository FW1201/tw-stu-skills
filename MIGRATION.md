# 升級與相容性

Codex 與 Claude Code 各自可用；不依賴 Harness 或其他套組。依 skills-manifest.json 選入口與版本。一般內容能力允許自動選用；工作區 profile 是資料且本次要求優先。

研究 PRISMA 改 --input 或 --example；旧數字介面必須五項明確提供，且假定每 report 一 study，正式需轉JSON明示單位。學生portfolio改 --input／--content／--framework／--example，未指定內容模式不再默認空白；--content現在保留文字，diverse已實作。新的本機數值工具參數見各入口 input-guide。

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/release.py
python3 scripts/release.py --package dist
python3 scripts/release.py --install /選定/技能目錄
```

安裝替換 manifest 選定目錄，暫存舊內容只用回滾，成功後清除。既有同名客製內容若需保留請先在工作區另存；使用者作品不應放安裝目錄。安裝hash回讀不等於宿主選用、完整模型對話或教學成效驗收。

Skill 版本與作者移入標準 metadata.version／metadata.author；讀取舊版頂層欄位的自有工具需更新。manifest保留獨立套組版本與Skill版本。
