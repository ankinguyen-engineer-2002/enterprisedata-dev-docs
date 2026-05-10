#!/usr/bin/env python3
"""
Scan OneLake shortcuts on all lakehouses + warehouses, and enumerate Files/ folder
content on prod lakehouses.
"""
import json, subprocess
from pathlib import Path

OUT = Path("/Users/MAC/Documents/Explore_Engineer_Workspace/EnterpriseData-Dev-Scan")
WS_ID = "5360a935-1984-4775-895f-f4c90bafa19d"

LAKEHOUSES = {
    "A_Developement": "1545d3ce-0fae-40b5-b314-ac2fd43e25c5",
    "Centralized_Lakehouse": "50e11300-9fb4-4e82-876c-7183bb2501ba",
    "RadarSync_Test": "ddadbe2e-c2e2-4949-8e84-81eed6a81c9e",
    "DataflowsStagingLakehouse": "68d19239-4abc-456b-9fa4-5dceb4b2d99e",
    "StagingLakehouseForDataflows_20251008191803": "c2583202-eb6f-49bb-9f2f-1bb551b786b0",
}

WAREHOUSES = {
    "ETL_Framework": "02c8970b-7af3-4d4e-b011-cc3cdc3825ef",
    "Source_Data": "f14e2ea6-ae2c-4b90-8e08-522e84f1aefc",
    "Centralized_Warehouse": "c5a1f95b-f9db-4cb7-8ded-396ea70da572",
    "Retail_Warehouse": "09504907-575d-446a-991a-87fa525166d7",
    "Distribution_Warehouse": "7d51a21f-c1fe-4968-930d-1702c0ee39dc",
    "MasterData_Warehouse": "db565620-28ac-4510-a61e-1023743efdc6",
    "Wholesale_Warehouse": "c1ef4a62-f8e2-4d55-96bd-33eb07b81b7c",
    "Quality_Warehouse": "6a6129c1-5342-4ea2-bcb8-9b8a1af8db20",
    "StagingWarehouseForDataflows_20251008191817": "0f273877-0905-4a68-b1c3-814f5c532f43",
    "DataflowsStagingWarehouse": "4cf62bd7-4fe0-4785-bcd4-0f95977725eb",
    "Test_Owneraccess": "2d1d459e-debb-439d-876a-34cd30c44961",
}


def az_get(url, resource="https://api.fabric.microsoft.com"):
    r = subprocess.run(
        ["az", "rest", "--method", "GET", "--url", url, "--resource", resource],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return {"_error": r.stderr.strip()[:300]}
    try:
        return json.loads(r.stdout) if r.stdout.strip() else {}
    except Exception:
        return {"_raw": r.stdout[:500], "_parse_error": True}


def storage_get(url):
    """Use storage token for OneLake DFS."""
    tok = subprocess.run(
        ["az", "account", "get-access-token", "--resource", "https://storage.azure.com",
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    r = subprocess.run(
        ["curl", "-s", "-H", f"Authorization: Bearer {tok}",
         "-H", "x-ms-version: 2020-10-02", url],
        capture_output=True, text=True,
    )
    try:
        return json.loads(r.stdout) if r.stdout.strip() else {}
    except Exception:
        return {"_raw": r.stdout[:500], "_parse_error": True}


def scan_shortcuts(name, item_id):
    print(f"  shortcuts on {name}...", flush=True)
    res = az_get(f"https://api.fabric.microsoft.com/v1/workspaces/{WS_ID}/items/{item_id}/shortcuts")
    if "_error" in res:
        return {"error": res["_error"]}
    return res.get("value", [])


def list_files_recursive(item_id, max_depth=3):
    """Use OneLake DFS to list Files/ folder recursively (limited depth)."""
    base_url = f"https://onelake.dfs.fabric.microsoft.com/{WS_ID}/{item_id}"
    out = []

    def walk(directory, depth=0):
        if depth > max_depth:
            return
        url = f"{base_url}?resource=filesystem&recursive=false&directory={directory}"
        res = storage_get(url)
        if "_error" in res or "_raw" in res:
            return
        for p in res.get("paths", []):
            out.append({
                "name": p.get("name"),
                "isDirectory": p.get("isDirectory") == "true",
                "size": int(p.get("contentLength", 0)),
                "lastModified": p.get("lastModified"),
                "depth": depth,
            })
            if p.get("isDirectory") == "true" and depth < max_depth:
                walk(p["name"], depth + 1)
    walk("Files", depth=0)
    return out


def main():
    out = {"shortcuts": {}, "files": {}}

    print("=== Lakehouse shortcuts ===", flush=True)
    for name, lid in LAKEHOUSES.items():
        out["shortcuts"][name] = scan_shortcuts(name, lid)
        sc = out["shortcuts"][name]
        if isinstance(sc, list):
            print(f"    {len(sc)} shortcuts", flush=True)

    print("\n=== Warehouse shortcuts ===", flush=True)
    for name, wid in WAREHOUSES.items():
        out["shortcuts"][name] = scan_shortcuts(name, wid)
        sc = out["shortcuts"][name]
        if isinstance(sc, list):
            print(f"    {len(sc)} shortcuts", flush=True)

    print("\n=== Files/ folder enum (prod LH only) ===", flush=True)
    for name in ("A_Developement", "Centralized_Lakehouse", "RadarSync_Test"):
        lid = LAKEHOUSES[name]
        print(f"  {name}...", flush=True)
        out["files"][name] = list_files_recursive(lid, max_depth=3)
        print(f"    {len(out['files'][name])} entries", flush=True)

    with open(OUT / "08-shortcuts-files-raw.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nWrote {OUT / '08-shortcuts-files-raw.json'}")


if __name__ == "__main__":
    main()
