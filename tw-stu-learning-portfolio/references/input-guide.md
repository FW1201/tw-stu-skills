# 本機輸入與執行

mode=content/framework/example、type=course_result/diverse/autobiography、title、sections(heading,text,evidence_ids)、evidence(id,locator,excerpt)。content 文字不可空；所有 evidence_ids 必須存在。CLI --content 是字面原文，--framework 明示空白；新介面不默認生成空白。

[示例結構](../examples/example.json) 僅作格式參考，正式輸入換成使用者實際材料。

```bash
python3 "$SKILL_DIR/scripts/generate_portfolio.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/result.docx"
```
