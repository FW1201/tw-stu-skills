# 本機輸入與執行

title、nodes(id,label,description)、edges(from,to,label)、questions(prompt,answer)。可選 linear(a,b,min,max,step)；只宣稱已實作 y=a*x+b，不把其他模型硬套。節點圖／文字替代／理解題共用同一資料。

[示例結構](../examples/example.json) 僅作格式參考，正式輸入換成使用者實際材料。

```bash
python3 "$SKILL_DIR/scripts/generate_concept.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/result.html"
```
