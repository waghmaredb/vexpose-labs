"""
Scoped ServiceNow adapter for an agentic ITSM system.

Companion code for:
  https://vexpose.blog/2026/07/16/agentic-itsm-reference-architecture/

The agent's power is defined by the surface area of this class — and that
surface area is a design decision you make on purpose. Note what is NOT here:
there is no generic run_query() or execute(). The agent never gets your admin
token; it gets exactly these operations, backed by a least-privilege account.
"""

import os
import requests


class ServiceNowAdapter:
    """Exposes ONLY whitelisted operations, backed by a least-privilege account."""

    def __init__(self):
        self.base = os.environ["SN_INSTANCE_URL"]
        self.auth = (os.environ["SN_AGENT_USER"], os.environ["SN_AGENT_TOKEN"])

    def add_work_note(self, sys_id: str, note: str):
        return self._patch(sys_id, {"work_notes": note})

    def reassign(self, sys_id: str, group: str):
        return self._patch(sys_id, {"assignment_group": group})

    def _patch(self, sys_id: str, body: dict):
        r = requests.patch(
            f"{self.base}/api/now/table/incident/{sys_id}",
            json=body,
            auth=self.auth,
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
