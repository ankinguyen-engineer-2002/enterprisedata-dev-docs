#!/usr/bin/env python3
"""
Scan all 5 Lakehouses in EnterpriseData-Dev workspace.
- Connect via Fabric SQL Endpoint with AAD token (pyodbc).
- For schema-enabled LH: query INFORMATION_SCHEMA.
- For legacy LH: same INFORMATION_SCHEMA works (no schemas).
- Output: 02-lakehouses-raw.json
"""
import json, struct, subprocess, sys, time
from pathlib import Path

import pyodbc

SQL_COPT_SS_ACCESS_TOKEN = 1256
OUT_DIR = Path("/Users/MAC/Documents/Explore_Engineer_Workspace/EnterpriseData-Dev-Scan")

LAKEHOUSES = [
    {
        "name": "A_Developement",
        "id": "1545d3ce-0fae-40b5-b314-ac2fd43e25c5",
        "tier": "PROD-ish",
        "server": "7woj2wroypauvkpn72b56t46ju-gwuwau4edf2upck76teqxl5btu.datawarehouse.pbidedicated.windows.net",
        "database": "A_Developement",
        "schemas_enabled": False,
        "sample_top_n": 3,
    },
    {
        "name": "Centralized_Lakehouse",
        "id": "50e11300-9fb4-4e82-876c-7183bb2501ba",
        "tier": "PROD",
        "server": "7woj2wroypauvkpn72b56t46ju-gwuwau4edf2upck76teqxl5btu.datawarehouse.fabric.microsoft.com",
        "database": "Centralized_Lakehouse",
        "schemas_enabled": True,
        "sample_top_n": 25,
    },
    {
        "name": "RadarSync_Test",
        "id": "ddadbe2e-c2e2-4949-8e84-81eed6a81c9e",
        "tier": "TEST/SANDBOX",
        "server": "7woj2wroypauvkpn72b56t46ju-gwuwau4edf2upck76teqxl5btu.datawarehouse.fabric.microsoft.com",
        "database": "RadarSync_Test",
        "schemas_enabled": True,
        "sample_top_n": 2,
    },
    {
        "name": "DataflowsStagingLakehouse",
        "id": "68d19239-4abc-456b-9fa4-5dceb4b2d99e",
        "tier": "STAGING-AUTO",
        "skip_deep": True,
    },
    {
        "name": "StagingLakehouseForDataflows_20251008191803",
        "id": "c2583202-eb6f-49bb-9f2f-1bb551b786b0",
        "tier": "STAGING-AUTO",
        "skip_deep": True,
    },
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
        f"Connection Timeout=30;"
    )
    return pyodbc.connect(
        conn_str, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: make_token_struct(token)}
    )


def query(conn, sql: str, params=None):
    cur = conn.cursor()
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    if cur.description is None:
        return [], []
    cols = [c[0] for c in cur.description]
    rows = []
    for r in cur.fetchall():
        rows.append([
            (str(v)[:300] if v is not None and not isinstance(v, (int, float, bool)) else v)
            for v in r
        ])
    return cols, rows


def scan_one(lh):
    if lh.get("skip_deep"):
        return {"tables": [], "columns": [], "row_counts": {}, "samples": {}, "note": "STAGING-AUTO — listing skipped (auto-created by Dataflow Gen2, confirmed empty earlier via lakehouses/{id}/tables endpoint)"}
    print(f"\n=== {lh['name']} ===", flush=True)
    conn = connect(lh["server"], lh["database"])

    # Tables
    cols, rows = query(
        conn,
        "SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE FROM INFORMATION_SCHEMA.TABLES "
        "WHERE TABLE_SCHEMA NOT IN ('sys','queryinsights','INFORMATION_SCHEMA') "
        "ORDER BY TABLE_SCHEMA, TABLE_NAME",
    )
    tables = [{"schema": r[0], "name": r[1], "type": r[2]} for r in rows]
    print(f"  tables: {len(tables)}", flush=True)

    # Columns (whole DB at once)
    cols, rows = query(
        conn,
        "SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION, DATA_TYPE, "
        "CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, NUMERIC_SCALE, IS_NULLABLE "
        "FROM INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_SCHEMA NOT IN ('sys','queryinsights','INFORMATION_SCHEMA') "
        "ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION",
    )
    columns = [
        {"schema": r[0], "table": r[1], "name": r[2], "ordinal": r[3], "type": r[4],
         "char_max_len": r[5], "num_prec": r[6], "num_scale": r[7], "nullable": r[8]}
        for r in rows
    ]
    print(f"  columns: {len(columns)}", flush=True)

    # Row counts — per table COUNT(*); cap to all tables but with timeout protection
    row_counts = {}
    for i, t in enumerate(tables):
        full = f"[{t['schema']}].[{t['name']}]" if t["schema"] else f"[{t['name']}]"
        try:
            _, r = query(conn, f"SELECT COUNT_BIG(*) FROM {full}")
            row_counts[f"{t['schema']}.{t['name']}"] = int(r[0][0]) if r else None
        except Exception as e:
            row_counts[f"{t['schema']}.{t['name']}"] = f"ERR: {str(e)[:120]}"
        if (i + 1) % 50 == 0:
            print(f"    counted {i+1}/{len(tables)}", flush=True)

    # Samples — top N tables by row count
    valid_counts = [(k, v) for k, v in row_counts.items() if isinstance(v, int) and v > 0]
    valid_counts.sort(key=lambda x: -x[1])
    top_tables = valid_counts[: lh.get("sample_top_n", 10)]
    samples = {}
    for k, _cnt in top_tables:
        s, n = k.split(".", 1)
        full = f"[{s}].[{n}]" if s else f"[{n}]"
        try:
            cols2, rows2 = query(conn, f"SELECT TOP 5 * FROM {full}")
            samples[k] = {"columns": cols2, "rows": rows2}
        except Exception as e:
            samples[k] = {"error": str(e)[:200]}

    return {"tables": tables, "columns": columns, "row_counts": row_counts, "samples": samples}


def main():
    out = {}
    for lh in LAKEHOUSES:
        try:
            scan = scan_one(lh)
            out[lh["name"]] = {**lh, **scan}
        except Exception as e:
            out[lh["name"]] = {**lh, "error": str(e)[:300]}
            print(f"  ERROR: {e}", flush=True)
    with open(OUT_DIR / "02-lakehouses-raw.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nWrote {OUT_DIR / '02-lakehouses-raw.json'}")
    return out


if __name__ == "__main__":
    main()
