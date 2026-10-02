---
name: tw-stu-study-planner
description: 依可用時段、任務與學習證據安排可重排計畫，輸出本機 Markdown／ICS。
metadata:
  version: 2.0.0
  author: 奇老師・數位敘事力社群
---

# 可重排學習計畫

適用 Codex 與 Claude Code；可獨立安裝。

## 開始

讀取 [工作方式與資料交換](references/common/workflow.md)，並按需讀取目前工作區的 `student-profile.md` 或 `.json`；不存在仍可工作。

## 任務程序

先收真實可用時段、已有義務、截止與任務估計，預留緩衝。間隔複習與主動回憶作爲可調整策略，不宣稱效果3倍；交錯練習是辨別策略，不等於每40分鐘機械換科。
用 scripts/plan.py 分配任務，固定不可用時間先剔除；超出容量的任務列未排，不擠成重疊日程。保存 task_id 與穩定UID，再排時明確取消／替換舊項；ICS爲本機文件，未寫入Calendar不標已同步。
每次覆盤根據實際完成／卡點調整工作量與支援；國小可短任務且保留休息。交付計劃、可用／已排／未排分鐘與調整原因，不強迫連Google Calendar。

## 完成檢查

核對輸入與成品、主張與證據；未執行／未取得／未確認項逐一明示。技能生成成功與真實教學、學術成效分別判斷。

需要本機運算或檔案生成時讀取 [輸入與CLI](references/input-guide.md)。
