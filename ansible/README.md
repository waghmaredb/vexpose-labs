# Ansible: a `changed` you can't trust is worse than no signal

Companion code for **[Your Ansible Playbook Says 'changed' Every Run. It's Lying.](https://vexpose.blog/)** on vExpose.blog.

`command` and `shell` report `changed` every run by definition — so a real change hides in the wall of false ones, and a handler can fire a needless production restart because a task cried wolf. Idempotency is the whole promise of a config tool.

| File | What it shows |
|------|---------------|
| [`site.yml`](./site.yml) | Three fixes: the stateful `user` module; `creates:` to guard a shelled-out command; `changed_when` / `failed_when` to define "changed" from output. |
| [`ci-idempotence.sh`](./ci-idempotence.sh) | The regression gate — run twice; fail the build if the second pass reports any `changed`. |

## The rule

Make every task earn its status: reach for the stateful module first, guard commands with `creates`/`removes`, and set `changed_when` whenever you shell out. The goal isn't a quiet run — it's a run where yellow always **means** something.

```bash
./ci-idempotence.sh site.yml   # second run must be all ok
```
