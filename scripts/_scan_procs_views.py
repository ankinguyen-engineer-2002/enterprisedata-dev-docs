#!/usr/bin/env python3
"""
Scan all stored procedure bodies + view definitions across 11 warehouses
and lakehouses. Save to 06-procs-raw.json and 07-views-raw.json.
"""
import json, struct, subprocess, sys
from pathlib import Path
import pyodbc

SQL_COPT_SS_ACCESS_TOKEN = 1256
OUT = Path("/Users/MAC/Documents/Explore_Engineer_Workspace/EnterpriseData-Dev-Scan")

# Same SQLEP cluster fronts both warehouses and lakehouses (except A_Developement which is on pbidedicated)
WH_HOST = "7woj2wroypauvkpn72b56t46ju-gwuwau4edf2upck76teqxl5btu.datawarehouse.fabric.microsoft.com"
LH_HOST_PBI = "7woj2wroypauvkpn72b56t46ju-gwuwau4edf2upck76teqxl5btu.datawarehouse.pbidedicated.windows.net"

WAREHOUSES = [
    ("ETL_Framework", WH_HOST),
    ("Source_Data", WH_HOST),
    ("Centralized_Warehouse", WH_HOST),
    ("Retail_Warehouse", WH_HOST),
    ("Distribution_Warehouse", WH_HOST),
    ("MasterData_Warehouse", WH_HOST),
    ("Wholesale_Warehouse", WH_HOST),
    ("Quality_Warehouse", WH_HOST),
    ("StagingWarehouseForDataflows_20251008191817", WH_HOST),
    ("DataflowsStagingWarehouse", WH_HOST),
    ("Test_Owneraccess", WH_HOST),
]

LAKEHOUSES = [
    ("A_Developement", LH_HOST_PBI),
    ("Centralized_Lakehouse", WH_HOST),
    ("RadarSync_Test", WH_HOST),
]


def get_token():
    out = subprocess.run(
        ["az", "account", "get-access-token", "--resource", "https://database.windows.net"],
        capture_output=True, text=True, check=True,
    )
    return json.loads(out.stdout)["accessToken"]


def make_token_struct(token: str) -> bytes:
    exptoken = b""
    for ch in bytes(token, "utf-8"):
        exptoken += bytes({ch}) + b"\0"
    return struct.pack("=i", len(exptoken)) + exptoken


def connect(server: str, database: str):
    token = get_token()
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};DATABASE={database};Encrypt=yes;TrustServerCertificate=no;"
        f"Connection Timeout=60;"
    )
    return pyodbc.connect(
        conn_str, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: make_token_struct(token)}
    )


def query(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    if cur.description is None:
        return [], []
    cols = [c[0] for c in cur.description]
    rows = cur.fetchall()
    return cols, rows


def scan_procs(database: str, server: str):
    print(f"  procs in {database}...", flush=True)
    conn = connect(server, database)
    sql = """
        SELECT s.name AS schema_name, p.name AS proc_name,
               p.modify_date, p.create_date,
               m.definition
        FROM sys.procedures p
        JOIN sys.schemas s ON p.schema_id = s.schema_id
        LEFT JOIN sys.sql_modules m ON p.object_id = m.object_id
        ORDER BY s.name, p.name
    """
    try:
        cols, rows = query(conn, sql)
        out = []
        for r in rows:
            out.append({
                "schema": r[0],
                "name": r[1],
                "modify_date": str(r[2]) if r[2] else None,
                "create_date": str(r[3]) if r[3] else None,
                "definition": r[4],
            })
        print(f"    captured {len(out)} procs", flush=True)
        return out
    except Exception as e:
        print(f"    ERROR: {e}", flush=True)
        return [{"error": str(e)[:200]}]


def scan_views(database: str, server: str):
    print(f"  views in {database}...", flush=True)
    conn = connect(server, database)
    sql = """
        SELECT s.name AS schema_name, v.name AS view_name,
               v.modify_date, v.create_date,
               m.definition
        FROM sys.views v
        JOIN sys.schemas s ON v.schema_id = s.schema_id
        LEFT JOIN sys.sql_modules m ON v.object_id = m.object_id
        ORDER BY s.name, v.name
    """
    try:
        cols, rows = query(conn, sql)
        out = []
        for r in rows:
            out.append({
                "schema": r[0],
                "name": r[1],
                "modify_date": str(r[2]) if r[2] else None,
                "create_date": str(r[3]) if r[3] else None,
                "definition": r[4],
            })
        print(f"    captured {len(out)} views", flush=True)
        return out
    except Exception as e:
        print(f"    ERROR: {e}", flush=True)
        return [{"error": str(e)[:200]}]


def main():
    procs = {}
    views = {}
    print("=== Warehouses ===", flush=True)
    for name, host in WAREHOUSES:
        print(f"\n[{name}]", flush=True)
        try:
            procs[name] = scan_procs(name, host)
            views[name] = scan_views(name, host)
        except Exception as e:
            print(f"  WAREHOUSE ERROR: {e}", flush=True)
            procs[name] = [{"error": str(e)[:200]}]
            views[name] = [{"error": str(e)[:200]}]

    print("\n=== Lakehouses ===", flush=True)
    for name, host in LAKEHOUSES:
        print(f"\n[{name}]", flush=True)
        try:
            procs[name] = scan_procs(name, host)  # lakehouses can have procs (rare)
            views[name] = scan_views(name, host)
        except Exception as e:
            print(f"  LAKEHOUSE ERROR: {e}", flush=True)
            procs[name] = [{"error": str(e)[:200]}]
            views[name] = [{"error": str(e)[:200]}]

    with open(OUT / "06-procs-raw.json", "w") as f:
        json.dump(procs, f, indent=2, default=str)
    with open(OUT / "07-views-raw.json", "w") as f:
        json.dump(views, f, indent=2, default=str)

    # Stats
    print("\n=== Summary ===", flush=True)
    total_procs = sum(len([x for x in v if "definition" in x]) for v in procs.values())
    total_views = sum(len([x for x in v if "definition" in x]) for v in views.values())
    procs_with_body = sum(
        sum(1 for x in v if isinstance(x.get("definition"), str) and len(x["definition"]) > 10)
        for v in procs.values()
    )
    views_with_body = sum(
        sum(1 for x in v if isinstance(x.get("definition"), str) and len(x["definition"]) > 10)
        for v in views.values()
    )
    print(f"  Total proc records: {total_procs}, with body: {procs_with_body}")
    print(f"  Total view records: {total_views}, with body: {views_with_body}")


if __name__ == "__main__":
    main()
