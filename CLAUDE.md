# tw-stu-skills — Claude Code 專案設定
# K-12 學習 Skills Repo
# 最後更新：2026-04-26

---

## Repo 定位

此 repo 包含 **10 個 K-12 學習 Skills**，目標用戶為台灣國小、國中、高中學生。

---

## 工具許可

### 允許（無需確認）
- `WebSearch`：搜尋備考資料、時事素材
- `Read`：讀取 SKILL.md 和 references/ 文件

### 需確認
- `Write`：寫入任何檔案
- `Bash`：執行外部程式

---

## 輸出規範

### 學習素材風格
- 語言：淺白易懂，避免艱深學術語彙
- 視覺化：Neon Circuit 設計系統（互動 HTML Artifact）
- 字型：Noto Sans TC（繁體中文清晰度優先）
- Google Fonts CDN 必須包含在所有 HTML Artifact 的 `<head>` 中

### 設計規範
- 所有 HTML Artifact 使用 `--neon-circuit-*` 命名空間 CSS 變數
- 保留向下相容別名（`--bg`, `--primary` 等）

---

## Skill 開發規範

### Frontmatter 必要欄位
```yaml
name: tw-stu-<name>
description: >
  [功能描述，包含觸發詞]
version: x.x.x
author: 奇老師・數位敘事力社群
allowed-tools: "<最小必要工具清單>"
```

### 禁止
- `disable-model-invocation: true`（學習類 Skill 均需模型生成內容，此欄位不適用）

---

## 測試

```bash
npx skills add . --all -a claude-code
```
