---
name: tw-stu-learning-portfolio
description: >
  引導高中學生自主整理學習歷程檔案（108課綱大學申請入學用），
  包含課程學習成果說明、多元表現敘述、自我評述框架、備審自傳。
  AI 提供架構引導，強調學生自主表達與真實呈現。
  當使用者提及「學習歷程」「備審資料」「課程學習成果」「多元表現」
  「自我評述」「學習歷程檔案」「大學申請」「備審資料製作」「自傳」時觸發。
  分類：K-12 學習（tw-stu-*）
version: 2.0.0
author: 奇老師・數位敘事力社群
allowed-tools: "Bash, Read, Write, Notion, GoogleCalendar, Canva"
disable-model-invocation: true
---

# 學習歷程檔案輔助工具

## Step 0：讀取文件
- `references/portfolio_guide.md`
- `/mnt/skills/public/docx/SKILL.md`


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：資訊收集
1. 學生年級（高一/高二/高三）？
2. 要撰寫哪類文件？
   - 課程學習成果說明（每份800字內）
   - 多元表現綜整心得
   - 自傳/自我陳述
   - 大學科系對應說明
3. 學生提供的關鍵內容（活動、作品、心得）？

## Step 2：生成學習歷程文件

```bash
python scripts/generate_portfolio.py \
  --grade "[高一/高二/高三]" \
  --type "[course_result/diverse/autobiography]" \
  --content "[學生提供的內容摘要]" \
  --target_dept "[目標科系（選填）]" \
  --output "/mnt/user-data/outputs/學習歷程_[類型].docx"
```

## 重要提醒
- 本工具提供框架與引導，最終內容須由學生自己撰寫
- 輸出為草稿，需學生大量修改使其個人化
- 強調真實性：鼓勵學生寫真實的學習歷程

---

## 選件邏輯與反思框架

### 選什麼作品放進去？

最常見的誤解是「放最好的作品」。更有效的邏輯是：
**放能說出「改變」的作品**——這個作品反映了我在哪裡有了什麼改變？

選件時問自己：「我為什麼選這件作品？它反映了我的什麼改變？」
能說出改變在哪裡，才是真正的學習記錄，而不只是「作品集」。

### 反思段落三問框架

每件作品的反思建議用這三個問題展開：
1. 做這件事的時候，我用了什麼方法/策略？
2. 哪個部分有效？哪個部分遇到困難？
3. **下次遇到類似任務，我會先調整什麼？**

> 第三問最重要——連結到行動的反思才不只是「寫感想」。
> 能具體說出「下次我會先___」的學生，學習能力的成長是可觀的。

### 最終頁：讓成長軌跡可見

學習歷程檔案的最後一頁建議加入三欄：
- **我的起點是…**（你一開始在哪裡？）
- **我現在能…**（你到了哪裡？）
- **我接下來想…**（你要去哪裡？）

讓成長軌跡對自己和審查者都清楚可見。

---

## 年級適應 + 引導式收集（v2.0 更新）

### 自動年級偵測
從使用者輸入辨識學習階段（國小/國中/高中），自動調整：
- 教學語言複雜度與詞彙難度
- 布魯姆認知層次分布
- 活動設計的自主程度
- 課綱代碼學段後綴（-E- / -J- / -U-）

詳見：`../../tw_edu_grade_adapter.md`

### 引導式資訊收集
啟動時執行漸進式三輪問答，確保取得充足資訊再開始任務。
詳見：`../../tw_edu_guided_collection.md`

---

## MCP 連接器

### Claude Code ／ Claude.ai（Pro/Team/Enterprise）
```
WebSearch（自動啟用）：
  搜尋最新課綱資料、教材資源、時事素材

Google Drive（若已連接，Settings → Connectors）：
  直接從 Drive 讀取現有教材
  完成後直接儲存輸出文件到 Drive
```

### Codex 平台
MCP Connectors 透過 `~/.codex/config.toml` 設定（`codex mcp add` 指令或手動編輯）。
未設定時自動降級：請參閱上方降級方案。

### Antigravity 平台（Google AI IDE）
MCP 透過 MCP Server Hub（1,500+ servers）或 `~/.gemini/antigravity/mcp_config.json` 設定。
支援 Jupyter Notebook 整合。未設定時自動降級：請參閱上方降級方案。

---

## MCP 整合更新（v3.0）

**讀取全域策略文件：`../../tw_edu_mcp_strategy.md`**

### 本 Skill 適用的 MCP 最佳化

**WebSearch（已啟用）：**
搜尋最新課綱資料、教學素材、時事情境。

**Canva MCP（若已連接）：**
使用者說「幫我做更美觀的版本」或「Canva 設計」時：
→ 呼叫 Canva:generate-design 生成高設計感版本
→ 優先適用：教案封面、簡報、學習單封面

**Google Drive（若已連接）：**
文件生成後詢問：「要上傳到 Google Drive 嗎？」
→ 確認後上傳，返回分享連結
→ 不修改任何現有檔案的分享權限

**安全原則：**
所有 MCP 寫入操作執行前，必須顯示確認摘要並等待使用者確認。
