# tw-stu-skills — Codex & Antigravity 安裝指南

適用平台：**OpenAI Codex CLI** 和 **Google Antigravity IDE**  
版本：V3.1（2026-04-26）

---

## Codex 安裝

### Skills 路徑

```
<your-project>/.agents/skills/<skill-name>/SKILL.md   ← 專案層（推薦）
~/.codex/skills/<skill-name>/SKILL.md                  ← 全域層
```

### 安裝步驟

```bash
git clone https://github.com/FW1201/tw-stu-skills.git

# 安裝到專案目錄
mkdir -p <your-project>/.agents/skills
cp -r tw-stu-skills/tw-stu-*/ <your-project>/.agents/skills/

# 或全域安裝
mkdir -p ~/.codex/skills
cp -r tw-stu-skills/tw-stu-*/ ~/.codex/skills/
```

### 使用方式

```
"我要準備會考國文，幫我出考題"
→ 自動啟用 tw-stu-exam-prep

"幫我寫學習歷程自述"
→ 自動啟用 tw-stu-learning-portfolio

"我看不懂細胞分裂的概念，幫我畫個圖"
→ 自動啟用 tw-stu-concept-viz
```

### MCP Connectors 設定

```toml
# ~/.codex/config.toml

# WebSearch（備考題目、時事素材）
# 已內建，無需設定

# Notion（讀書筆記、學習歷程存檔）
[mcp_servers.notion]
command = "npx"
args = ["-y", "@notionhq/notion-mcp-server"]
env = { NOTION_API_KEY = "${NOTION_API_KEY}" }

# Google Drive（學習歷程文件存檔）
[mcp_servers.google-drive]
command = "npx"
args = ["-y", "@google/mcp-server-googledrive"]
```

### Skills × MCP 需求對照

| Skill | 必要 MCP | 選用 MCP |
|-------|---------|---------|
| tw-stu-exam-prep | WebSearch（內建）| — |
| tw-stu-learning-portfolio | — | Drive, Notion |
| tw-stu-concept-viz | — | — |
| tw-stu-writing-coach | — | — |
| tw-stu-study-planner | — | Notion |
| tw-stu-career-explore | WebSearch | — |

---

## Antigravity 安裝（Google AI IDE）

### Skills 路徑

```
~/.gemini/antigravity/skills/<skill-name>/SKILL.md   ← 全域層
<project>/.agent/skills/<skill-name>/SKILL.md         ← 專案層
```

注意：路徑是 `.agent`（單數），不是 `.agents`。

### 安裝步驟

```bash
mkdir -p ~/.gemini/antigravity/skills
cp -r tw-stu-skills/tw-stu-*/ ~/.gemini/antigravity/skills/
```

### MCP Connectors 設定

**MCP Server Hub（推薦）**：在 Antigravity 介面搜尋 Notion、Google Drive 並啟用。

**JSON 設定**：
```json
// ~/.gemini/antigravity/mcp_config.json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" }
    },
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@google/mcp-server-googledrive"]
    }
  }
}
```

### Antigravity 特有優勢

- **tw-stu-concept-viz**：在 Jupyter Notebook 中即時預覽視覺化圖形
- **tw-stu-study-planner**：可與 Google Calendar MCP 連動建立讀書計畫行事曆

---

## 常見問題

| 問題 | 解決方案 |
|------|---------|
| Codex 找不到 Skill | 確認路徑為 `.agents/skills/`（複數） |
| Antigravity 找不到 Skill | 確認路徑為 `.agent/skills/`（單數） |
| Frontmatter 欄位顯示異常 | `allowed-tools` 是 Claude Code 專屬欄位，Codex/Antigravity 忽略即可，不影響功能 |
