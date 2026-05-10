#!/usr/bin/env python3
"""Scan v2 — gap closing.
Captures: git integration, connections, workspace spark settings, capacity,
mirror tables list, sample per-item permissions.
"""
import json, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
WS = "5360a935-1984-4775-895f-f4c90bafa19d"


def az(method, url, resource="https://api.fabric.microsoft.com"):
    r = subprocess.run(
        ["az", "rest", "--method", method, "--url", url, "--resource", resource],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return {"_error": r.stderr.strip()[:300], "_status": r.returncode}
    try:
        return json.loads(r.stdout) if r.stdout.strip() else {}
    except Exception as e:
        return {"_raw": r.stdout[:600], "_parse_error": str(e)}


def main():
    out = {}

    print("[1] Git integration (Azure DevOps) ...")
    out["git_connection"] = az("GET", f"https://api.fabric.microsoft.com/v1/workspaces/{WS}/git/connection")
    out["git_status"] = az("GET", f"https://api.fabric.microsoft.com/v1/workspaces/{WS}/git/status")
    print(f"  state={out['git_connection'].get('gitConnectionState')}")

    print("[2] Connections (data sources) ...")
    out["connections"] = az("GET", "https://api.fabric.microsoft.com/v1/connections")
    if "value" in out["connections"]:
        print(f"  {len(out['connections']['value'])} connections")
    # Get gateways too
    out["gateways"] = az("GET", "https://api.fabric.microsoft.com/v1/gateways")

    print("[3] Workspace Spark settings ...")
    out["spark_settings"] = az("GET", f"https://api.fabric.microsoft.com/v1/workspaces/{WS}/spark/settings")
    out["spark_pools"] = az("GET", f"https://api.fabric.microsoft.com/v1/workspaces/{WS}/spark/pools")
    out["spark_libraries"] = az("GET", f"https://api.fabric.microsoft.com/v1/workspaces/{WS}/spark/libraries")
    print(f"  runtime={out['spark_settings'].get('environment', {}).get('runtimeVersion')}")

    print("[4] Capacity details ...")
    cap_id = "30d06c17-b0f4-4709-9a20-e29c96e8863e"
    out["capacities"] = az("GET", "https://api.fabric.microsoft.com/v1/capacities")
    found = None
    if "value" in out["capacities"]:
        for c in out["capacities"]["value"]:
            if c.get("id") == cap_id:
                found = c
                break
    out["our_capacity"] = found
    if found:
        print(f"  capacity SKU={found.get('sku')} state={found.get('state')}")
    else:
        print(f"  capacity {cap_id} not in our scope (cross-subscription)")

    print("[5] Mirror tables list ...")
    mirror_id = "1e284ab4-dc84-4421-a96d-fe4f942cec97"
    out["mirror_tables"] = az(
        "POST",
        f"https://api.fabric.microsoft.com/v1/workspaces/{WS}/mirroredAzureDatabricksCatalogs/{mirror_id}/getDefinition",
    )
    # Try alternative endpoints
    out["mirror_status"] = az(
        "GET",
        f"https://api.fabric.microsoft.com/v1/workspaces/{WS}/mirroredAzureDatabricksCatalogs/{mirror_id}/getStatus",
    )

    print("[6] Per-item permissions (sample 4 items) ...")
    perms = {}
    for nm, iid in [
        ("ETL_Framework", "02c8970b-7af3-4d4e-b011-cc3cdc3825ef"),
        ("Source_Data", "f14e2ea6-ae2c-4b90-8e08-522e84f1aefc"),
        ("Centralized_Lakehouse", "50e11300-9fb4-4e82-876c-7183bb2501ba"),
        ("MetaData-Pull", "e289e3ad-2245-4211-9522-0edb56f94726"),
    ]:
        # Try Power BI admin API for per-item permissions
        perms[nm] = az(
            "GET",
            f"https://api.powerbi.com/v1.0/myorg/admin/groups/{WS}/datasets",
            resource="https://analysis.windows.net/powerbi/api",
        )

    out["per_item_permissions"] = perms

    print("[7] Folders ...")
    out["folders"] = az("GET", f"https://api.fabric.microsoft.com/v1/workspaces/{WS}/folders")

    print("[8] Domain workspace details (Power BI admin) ...")
    out["pbi_workspace"] = az(
        "GET",
        f"https://api.powerbi.com/v1.0/myorg/groups/{WS}",
        resource="https://analysis.windows.net/powerbi/api",
    )

    print("[9] Lakehouse Files/ deeper enum (Centralized_Lakehouse depth=5) ...")
    # OneLake DFS
    cl_id = "50e11300-9fb4-4e82-876c-7183bb2501ba"
    files_deep = []

    def storage_token():
        r = subprocess.run(
            ["az", "account", "get-access-token", "--resource", "https://storage.azure.com",
             "--query", "accessToken", "-o", "tsv"],
            capture_output=True, text=True, check=True,
        )
        return r.stdout.strip()

    tok = storage_token()
    base = f"https://onelake.dfs.fabric.microsoft.com/{WS}/{cl_id}"

    def list_dir(directory, depth):
        if depth > 5:
            return
        url = f"{base}?resource=filesystem&recursive=false&directory={directory}"
        r = subprocess.run(
            ["curl", "-s", "-H", f"Authorization: Bearer {tok}",
             "-H", "x-ms-version: 2020-10-02", url],
            capture_output=True, text=True,
        )
        try:
            data = json.loads(r.stdout)
        except Exception:
            return
        for p in data.get("paths", [])[:200]:
            files_deep.append({
                "name": p.get("name"),
                "isDirectory": p.get("isDirectory") == "true",
                "size": int(p.get("contentLength", 0)),
                "depth": depth,
            })
            if p.get("isDirectory") == "true" and depth < 5 and len(files_deep) < 1500:
                list_dir(p["name"], depth + 1)

    list_dir("Files", 0)
    out["files_deep_centralized_lh"] = files_deep
    print(f"  {len(files_deep)} entries in Centralized_Lakehouse Files/")

    # Save
    DATA.mkdir(exist_ok=True)
    target = DATA / "12-scan-v2.json"
    with open(target, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nWrote {target} — {target.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
