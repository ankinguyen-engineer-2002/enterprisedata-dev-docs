#!/usr/bin/env python3
"""Pull last 30 job instances per pipeline + notebook + dataflow.
Save to 10-runs-raw.json, build 10-runs.md."""
import json, subprocess
from datetime import datetime
from pathlib import Path

OUT = Path("/Users/MAC/Documents/Explore_Engineer_Workspace/EnterpriseData-Dev-Scan")
WS = "5360a935-1984-4775-895f-f4c90bafa19d"

# Read inventory for IDs+types
with open(OUT / "00-inventory-with-ids.json") as f:
    txt = f.read()
inv = json.loads(txt.split("\n", 1)[1])

ITEMS = []
for type_name in ("DataPipeline", "Notebook", "Dataflow"):
    for it in inv.get(type_name, []):
        ITEMS.append((type_name, it["name"], it["id"]))


def az_get(url):
    r = subprocess.run(
        ["az", "rest", "--method", "GET", "--url", url, "--resource", "https://api.fabric.microsoft.com"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return {"_err": r.stderr.strip()[:300]}
    try:
        return json.loads(r.stdout) if r.stdout.strip() else {}
    except Exception:
        return {"_raw": r.stdout[:300]}


def fetch_runs(item_id):
    # Common job-instances endpoint
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{WS}/items/{item_id}/jobs/instances?$top=30"
    res = az_get(url)
    if "_err" in res:
        return {"error": res["_err"]}
    return res.get("value", [])


def main():
    out = {}
    for type_name, name, iid in ITEMS:
        print(f"  {type_name} {name}...", flush=True)
        runs = fetch_runs(iid)
        out[name] = {"id": iid, "type": type_name, "runs": runs}
        if isinstance(runs, list):
            print(f"    {len(runs)} runs", flush=True)
    with open(OUT / "10-runs-raw.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nWrote {OUT / '10-runs-raw.json'}")

    # Build markdown
    lines = []
    lines.append("# 10 — Job-instance run history (last ~30 runs each)")
    lines.append("")
    lines.append(f"Captured via `GET /v1/workspaces/{{ws}}/items/{{itemId}}/jobs/instances?$top=30` for {len(ITEMS)} items.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Active items (have run history)")
    lines.append("")
    lines.append("| Item | Type | # runs in window | Last run | Last status |")
    lines.append("|---|---|---:|---|---|")

    active = []
    inactive = []
    for name, d in out.items():
        runs = d.get("runs")
        if isinstance(runs, list) and runs:
            # Sort by start time desc
            sorted_runs = sorted(runs, key=lambda r: r.get("startTimeUtc") or "", reverse=True)
            last = sorted_runs[0]
            active.append((name, d["type"], len(runs), last))
        else:
            inactive.append((name, d["type"]))

    active.sort(key=lambda r: r[3].get("startTimeUtc") or "", reverse=True)
    for name, t, n, last in active:
        st = last.get("startTimeUtc", "?")[:19] if last.get("startTimeUtc") else "?"
        status = last.get("status", "?")
        lines.append(f"| `{name}` | {t} | {n} | {st} | {status} |")

    lines.append("")
    lines.append("## Inactive items (no run history in window)")
    lines.append("")
    lines.append("| Item | Type |")
    lines.append("|---|---|")
    for name, t in sorted(inactive):
        lines.append(f"| `{name}` | {t} |")

    # Per-active-item breakdown
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Per-item run breakdown (active only)")
    lines.append("")
    for name, t, n, last in active:
        runs = sorted(out[name]["runs"], key=lambda r: r.get("startTimeUtc") or "", reverse=True)
        lines.append(f"\n### `{name}` ({t})\n")
        lines.append("| # | Start | End | Status | Type | Run ID |")
        lines.append("|---|---|---|---|---|---|")
        for i, r in enumerate(runs[:15], 1):
            st = (r.get("startTimeUtc") or "?")[:19]
            et = (r.get("endTimeUtc") or "?")[:19]
            rs = r.get("status", "?")
            rt = r.get("jobType") or r.get("invokeType", "?")
            rid = (r.get("id") or "?")[:20]
            lines.append(f"| {i} | {st} | {et} | {rs} | {rt} | `{rid}` |")
        # success rate
        statuses = [r.get("status", "?") for r in runs]
        from collections import Counter
        sc = Counter(statuses)
        lines.append(f"\n**Status distribution:** {dict(sc)}")

    md = "\n".join(lines)
    with open(OUT / "10-runs.md", "w") as f:
        f.write(md)
    print(f"Wrote {OUT / '10-runs.md'} — {len(md):,} chars / {len(md.splitlines()):,} lines")
    print(f"\nSummary: {len(active)} active, {len(inactive)} inactive")


if __name__ == "__main__":
    main()
