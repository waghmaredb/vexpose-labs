"""
The ServiceNow REST pagination gotcha that silently drops records.

Companion code for: https://vexpose.blog/

The problem: using offset-based pagination in ServiceNow REST API while
the result set is changing (records added/deleted between page fetches)
silently skips or duplicates records.

Example: processing all incidents in a table, updating each one as you go.
If new incidents arrive between pagination calls, your offset becomes stale
and you skip records — or fetch the same ones twice.

The fix: use sys_id as a stable cursor instead of offset.
"""

import requests
from typing import Generator


# DON'T DO THIS: offset-based pagination with a changing result set
def fetch_incidents_unsafe(instance_url: str, username: str, password: str) -> Generator[dict, None, None]:
    """
    Using offset + limit on a live table. If records are added/deleted during
    iteration, offsets drift and records are silently dropped.
    """
    limit = 100
    offset = 0

    while True:
        # This offset is only valid for the *exact* result set at this moment.
        # If a new incident is created, all offsets after it shift.
        response = requests.get(
            f"{instance_url}/api/now/table/incident",
            params={
                "sysparm_limit": limit,
                "sysparm_offset": offset,
                "sysparm_query": "ORDERBYnumber",  # Missing secondary sort — unstable
            },
            auth=(username, password),
        )
        response.raise_for_status()

        incidents = response.json()["result"]
        if not incidents:
            break

        for incident in incidents:
            yield incident

        offset += limit  # ← This offset may now be invalid


# DO THIS: sys_id-based cursor for stable pagination
def fetch_incidents_safe(instance_url: str, username: str, password: str) -> Generator[dict, None, None]:
    """
    Use sys_id as a stable cursor. sys_id never changes; new records don't
    invalidate our position in the result set.
    """
    limit = 100
    last_sys_id = ""  # Empty string = start from beginning

    while True:
        # Query: fetch records with sys_id > last_sys_id, ordered by sys_id.
        # New records don't affect pagination — they sort after our cursor.
        query = "sys_idSTARTSWITH" if last_sys_id else "sys_idISNOTEMPTY"
        if last_sys_id:
            query = f"sys_id>{last_sys_id}^ORDERBYsys_id"
        else:
            query = "ORDERBYsys_id"

        response = requests.get(
            f"{instance_url}/api/now/table/incident",
            params={
                "sysparm_limit": limit,
                "sysparm_query": query,
                "sysparm_exclude_reference_link": "true",  # Minimize payload
            },
            auth=(username, password),
        )
        response.raise_for_status()

        incidents = response.json()["result"]
        if not incidents:
            break

        for incident in incidents:
            yield incident
            last_sys_id = incident["sys_id"]  # Advance cursor


if __name__ == "__main__":
    # Usage example:
    # for incident in fetch_incidents_safe(
    #     instance_url="https://dev12345.service-now.com",
    #     username="api_user",
    #     password="api_password",
    # ):
    #     print(f"Processing {incident['number']}")
    #     # Update incident, create related records, etc.
    #     # New incidents added during this loop won't be skipped.

    print("See the blog post for the full explanation.")
