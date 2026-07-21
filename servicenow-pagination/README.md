# ServiceNow REST Pagination Gotcha

Companion code for **The ServiceNow REST pagination gotcha that silently drops records** on [vExpose.blog](https://vexpose.blog).

## The problem

ServiceNow's REST API uses `offset` + `limit` for pagination. When you paginate through a live table—one where records are being created or deleted—the offset becomes stale between calls. Records are silently dropped.

```python
# DON'T: offset drifts as the result set changes
offset = 0
while True:
    records = call_api(offset=offset, limit=100)
    process(records)
    offset += 100  # ← Invalid if records were added/deleted
```

Why? Because `offset` is *positional* within the *current* result set. If a new incident is created and sorts before your current page, all offsets shift down — you skip records.

## The fix

Use `sys_id` as a stable cursor. `sys_id` is immutable; new records don't invalidate your position.

```python
# DO: cursor-based pagination
last_sys_id = ""
while True:
    records = call_api(query=f"sys_id>{last_sys_id}^ORDERBYsys_id", limit=100)
    process(records)
    if records:
        last_sys_id = records[-1]["sys_id"]
```

See [`pagination_gotcha.py`](./pagination_gotcha.py) for the full before-and-after.
