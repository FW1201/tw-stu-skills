---
name: tw-stu-concept-viz
description: 用可離線 HTML 圖解學科概念，提供鍵盤操作、文字替代與理解／遷移問題。
metadata:
  version: 2.0.0
  author: 奇老師・數位敘事力社群
---

# 互動概念圖解

適用 Codex 與 Claude Code；可獨立安裝。

## 開始

讀取 [工作方式與資料交換](references/common/workflow.md)，並按需讀取目前工作區的 `student-profile.md` 或 `.json`；不存在仍可工作。

## 任務程序

先確認概念、已有理解與年段，選擇概念圖、時間線、比較、流程或有計算關係的互動圖。節點／關係來自已知教材；循環因果不稱無環圖。
用 scripts/generate_concept.py --input JSON 產離線 HTML：節點可點選、鍵盤操作、顯示關係與說明，文字列表等價表達；可選 linear 模型讓滑桿改變已給定 a*x+b 的結果，不硬編碼漂亮卻無意義動畫。
輸出與圖共同依據的問題與新情境，檢查學生解釋而非點擊次數。圖的顏色不是唯一線索；手機與鍵盤可用，不能聯網纔開得動的庫不作必要依賴。

## 完成檢查

核對輸入與成品、主張與證據；未執行／未取得／未確認項逐一明示。技能生成成功與真實教學、學術成效分別判斷。

需要本機運算或檔案生成時讀取 [輸入與CLI](references/input-guide.md)。
