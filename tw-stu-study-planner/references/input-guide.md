# 本機輸入與執行

plan_id、timezone、generated_at(含UTC offset)、slots(start,end)、blocked(start,end)、tasks(id,title,minutes,可選deadline)、buffer_fraction、chunk_minutes。所有時間明示 offset，重疊可用時段拒絕。輸出 JSON 内 markdown 與 ics 可另存 .md/.ics；不能標已同步。

[示例結構](../examples/example.json) 僅作格式參考，正式輸入換成使用者實際材料。

```bash
python3 "$SKILL_DIR/scripts/plan.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/result.json"
```
