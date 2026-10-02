---
name: tw-stu-learning-portfolio
description: 組織學生既有作品、經驗與反思，產出內容驅動且可編輯的課程、多元表現或自傳。
metadata:
  version: 3.0.0
  author: 奇老師・數位敘事力社群
---

# 真實學習歷程

適用 Codex 與 Claude Code；可獨立安裝。

## 開始

讀取 [工作方式與資料交換](references/common/workflow.md)，並按需讀取目前工作區的 `student-profile.md` 或 `.json`；不存在仍可工作。

## 任務程序

先區分空白引導框架與已有內容排版；素材是學生原話／作品與日期／位置。每項能力主張連回證據，缺反思用問題引導，不補造家庭、競賽、情緒或成長。
依 course_result／diverse／autobiography 選模式。scripts/generate_portfolio.py --input JSON 消費真實 sections／evidence；--framework 明示空白框架，--content 接收用戶文字並保留，--example 只示例。
保留原話與編輯稿差異，學校年度限制有實際指南才判符合。交付 DOCX、證據 map、編輯／待補項；不代學生上傳備審，不宣稱模型代寫即是自主反思。

## 完成檢查

核對輸入與成品、主張與證據；未執行／未取得／未確認項逐一明示。技能生成成功與真實教學、學術成效分別判斷。

需要本機運算或檔案生成時讀取 [輸入與CLI](references/input-guide.md)。
