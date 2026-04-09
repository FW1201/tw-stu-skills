# tw-stu-skills — K-12 學習 Claude Skills 套組

> **臺灣中小學生專用 AI 學習工具套組**  
> 基於 108 課綱、12 年國教升學體制設計。核心原則：**引導思考，不替代學習**。

[![Skills](https://img.shields.io/badge/Skills-10-blue)](https://github.com/FW1201/tw-stu-skills)
[![Version](https://img.shields.io/badge/Version-1.0-green)](https://github.com/FW1201/tw-stu-skills)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📦 套組概覽

本套組包含 **10 個 Skills**，面向臺灣國小、國中、高中學生，涵蓋：
- 國中教育會考 / 高中學科能力測驗（學測）/ 分科測驗備考
- 108 課綱學習歷程檔案（MyPortfolio）製作
- AI 工具正確使用觀念與學術誠信
- 蘇格拉底引導問答（不直接給答案）
- 抽象概念互動視覺化

> **相關套組**：[tw-edu-skills（教師）](https://github.com/FW1201/tw-edu-skills) ｜ [tw-research-skills（學術研究）](https://github.com/FW1201/tw-research-skills)

---

## 🛠 Skills 清單

### 升學備考
| Skill | 功能說明 |
|-------|---------|
| `tw-stu-exam-prep` | 會考 / 學測個人化備考助手：目標設定→弱點診斷→練習題引導→進度追蹤→考前心理調適 |
| `tw-stu-study-planner` | 科學化學習計畫：間隔複習排程 × 主動回憶策略 × Google Calendar 自動同步 |

### 學習歷程與生涯
| Skill | 功能說明 |
|-------|---------|
| `tw-stu-learning-portfolio` | 學習歷程檔案製作：活動挖掘→素養連結→MyPortfolio 格式撰寫→備審自述 |
| `tw-stu-career-explore` | 生涯探索與志願選擇：Holland 興趣測評→科系深度探索→多元選修 / 自主學習規劃 |

### 學科能力
| Skill | 功能說明 |
|-------|---------|
| `tw-stu-writing-coach` | 國文素養寫作教練：議論文 / 記敘文 / 說明文架構引導→逐段評析→會考評分標準對應 |
| `tw-stu-vocab-builder` | 詞彙與閱讀素養：古文詞彙→成語語境→素養長文閱讀策略 |
| `tw-stu-socratic` | 蘇格拉底學科問答：各科概念深化理解，**嚴格不直接給答案**，以追問引導學生自行推導 |
| `tw-stu-concept-viz` | 抽象概念互動視覺化：輸入難懂概念→生成 HTML 互動圖形（概念圖/流程圖/時間軸）→5 題理解驗收 |

### AI 素養
| Skill | 功能說明 |
|-------|---------|
| `tw-stu-ai-literacy` | AI 工具正確使用法：三種使用模式辨別→提示詞設計工坊→輸出查核五步驟→學術誠信指引 |

### 套組設定
| Skill | 功能說明 |
|-------|---------|
| `tw-stu-synchronizer` | 個人化套組設定助手，根據年級/弱科/目標學校/升學路徑客製化所有 tw-stu-* Skills 行為 |

---

## 🚀 安裝方式

### Claude Code（推薦）

Claude Code 是本套組設計的**主要平台**，所有功能完整支援。

```bash
# 安裝全套組（10 個 Skills）
npx skills add FW1201/tw-stu-skills --all -a claude-code

# 安裝單一 Skill（例如只安裝升學備考）
npx skills add FW1201/tw-stu-skills tw-stu-exam-prep -a claude-code

# 確認安裝
npx skills list -a claude-code

# 更新套組
npx skills update -a claude-code
```

安裝後，直接以自然語言觸發（例如：「我要準備會考」、「幫我做學習歷程」）。

### Codex CLI

```bash
npx skills add FW1201/tw-stu-skills --all -a codex
```

> ⚠️ **Codex 限制**：
> - `tw-stu-concept-viz` 的 HTML Artifact 互動視覺化**無法預覽**（僅輸出 HTML 程式碼）
> - MCP Connectors（Google Calendar、Notion、Canva）**不可用**，備考排程需手動匯入
> - `tw-stu-study-planner` 的 Google Calendar 自動同步功能不適用

### Antigravity

```bash
npx skills add FW1201/tw-stu-skills --all -a antigravity
```

> ⚠️ **Antigravity 限制**：
> - MCP Connectors 支援程度依個人環境設定而定
> - HTML Artifact 互動預覽需確認瀏覽器整合已啟用
> - `WebSearch`（用於生涯探索、科系資訊查詢）依連線狀態而定

---

## 🔌 MCP Connectors 整合

| Connector | 應用 Skills | 功能 |
|-----------|------------|------|
| Google Calendar | `tw-stu-exam-prep`, `tw-stu-study-planner` | 備考計畫自動建立行程 |
| Notion | `tw-stu-learning-portfolio`, `tw-stu-career-explore` | 學習歷程條目存入知識庫 |
| Canva | `tw-stu-learning-portfolio` | 學習歷程視覺化設計模板 |

---

## ⚠️ 重要設計說明

### 引導而非替代
所有 Skills 嚴格執行「提問引導」機制，**不直接提供完整答案**。  
特別是 `tw-stu-socratic`：
- 使用者給出錯誤答案時 → AI 提供提示，要求再試一次
- 連續 3 次無法回答 → AI 解析思路，但要求學生用自己的話複述

### AI 輸出查核三問
每個 Skill 末段均內建確認機制：
1. 你自己理解了嗎？
2. 有沒有你不同意的部分？
3. 你能用自己的話複述嗎？

---

## 💡 第一次使用建議

**新生入門**（建議順序）：
1. `tw-stu-synchronizer` → 設定個人資料（5 分鐘問卷）
2. `tw-stu-ai-literacy` → 建立正確 AI 使用觀念
3. 依需求選擇其他 Skills

**升學備考**：
1. `tw-stu-exam-prep` → 設定目標與診斷
2. `tw-stu-study-planner` → 整合到每日排程
3. `tw-stu-socratic` → 各科深化理解

---

## 👨‍💻 作者

**奇老師・數位敘事力社群**  
GitHub：[@FW1201](https://github.com/FW1201)

---

*本套組採 MIT 授權。歡迎 Fork 並依台灣課綱更新提交 PR。*
