"""
Coordinated omission: why your p99 latency is lying.

Companion code for:
  https://vexpose.blog/  (Coordinated Omission: Why Your p99 Latency Is Lying)

A closed-loop load test sends the next request only after the previous one returns.
So when the server stalls, the load generator stalls with it — and simply DOESN'T
SEND the requests that should have gone out during the stall. Those missing requests
would have been slow too. By omitting them, the test reports a beautiful p99 for a
system that was, for a moment, serving no one.

The fix (Gil Tene's correction): measure each request's latency from the time it was
SUPPOSED to start (its schedule), not the time it actually started. This demo builds
one stall and shows the gap between the naive and corrected percentiles.
"""

from bisect import bisect_left


def percentile(sorted_vals, p):
    if not sorted_vals:
        return 0.0
    k = (len(sorted_vals) - 1) * (p / 100.0)
    lo = int(k)
    hi = min(lo + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo)


def simulate(target_rps=1000, seconds=10, stall_at=5.0, stall_ms=200.0, base_ms=0.2):
    """One request scheduled every 1/target_rps. Service is `base_ms` except for a
    single `stall_ms` freeze starting at `stall_at`. Returns (naive, corrected) ms."""
    interval = 1000.0 / target_rps          # ms between scheduled requests
    n = int(target_rps * seconds)
    stall_start = stall_at * 1000.0         # ms
    stall_end = stall_start + stall_ms

    naive, corrected = [], []
    clock = 0.0  # when the load generator is free to send the NEXT request (closed loop)

    for i in range(n):
        scheduled = i * interval            # when this request SHOULD have been sent
        actual_start = max(scheduled, clock)  # closed loop: can't send until free

        # Service time: normal, unless we're inside the stall window.
        if actual_start < stall_end and actual_start + base_ms > stall_start:
            # request caught by the freeze: it finishes when the stall ends
            finish = max(actual_start, stall_end)
        else:
            finish = actual_start + base_ms

        naive.append(finish - actual_start)      # what the naive test records
        corrected.append(finish - scheduled)     # honest: measured from the schedule
        clock = finish                           # next request waits for this one

    return sorted(naive), sorted(corrected)


if __name__ == "__main__":
    naive, corrected = simulate()
    print(f"{'percentile':>10} {'naive (ms)':>12} {'corrected (ms)':>16}")
    for p in (50, 90, 99, 99.9):
        print(f"{p:>10} {percentile(naive, p):>12.1f} {percentile(corrected, p):>16.1f}")
    print("\nSame system, same stall. The naive p99 looks healthy; the corrected p99 "
          "shows the freeze every scheduled request actually lived through.")
