# Kubernetes: the readiness probe that caused an outage

Companion code for **[The Readiness Probe That Turned a Deploy Into an Outage](https://vexpose.blog/)** on vExpose.blog.

Readiness decides **who gets traffic**; liveness decides **who gets killed**. Wire readiness to a deep dependency (or with no startup grace) and a healthy rollout drains the old pods faster than the new ones become Ready — clients get 503s from the exact mechanism meant to prevent them.

| File | What it shows |
|------|---------------|
| [`bad-probes.yaml`](./bad-probes.yaml) | The trap: `/healthz` checks the database, `failureThreshold: 1`, `maxUnavailable: 1`. |
| [`good-probes.yaml`](./good-probes.yaml) | The fix: shallow `/ready`, a `startupProbe` (150s grace), strict liveness, `maxUnavailable: 0`. |

## The rule

Readiness is a promise to your load balancer, not a health dashboard. Make it answer the narrowest question — "send me traffic now?" — and nothing else. Every dependency you fold into it is another way one small failure becomes a total one.

```bash
kubectl apply -f good-probes.yaml
kubectl rollout status deployment/web
```
