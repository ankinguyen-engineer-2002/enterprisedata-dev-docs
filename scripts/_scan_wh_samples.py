#!/usr/bin/env python3
"""Scan top-50 tables per warehouse: COUNT(*) + SELECT TOP 5 *.
Save to data/13-wh-samples.json.
"""
import json, struct, subprocess
from pathlib import Path
import pyodbc

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"

SQL_COPT_SS_ACCESS_TOKEN = 1256
WH_HOST = "7woj2wroypauvkpn72b56t46ju-gwuwau4edf2upck76teqxl5btu.datawarehouse.fabric.microsoft.com"

WHS = [
    "ETL_Framework",
    "Source_Data",
    "Centralized_Warehouse",
    "Retail_Warehouse",
    "Wholesale_Warehouse",
    "MasterData_Warehouse",
    "Distribution_Warehouse",
]


def get_token():
    o = subprocess.run(
        ["az", "account", "get-access-token", "--resource", "https://database.windows.net"],
        capture_output=True, text=True, check=True,
    )
    return json.loads(o.stdout)["accessToken"]


def make_token_struct(token):
    e = b""
    for ch in bytes(token, "utf-8"):
        e += bytes({ch}) + b"\0"
    return struct.pack("=i", len(e)) + e


def connect(server, db):
    tok = get_token()
    cs = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={db};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;"
    return pyodbc.connect(cs, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: make_token_struct(tok)})


def query(conn, sql):
    cur = conn.cursor()
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


def main():
    out = {}
    for wh in WHS:
        print(f"\n=== {wh} ===")
        try:
            conn = connect(WH_HOST, wh)
        except Exception as e:
            print(f"  Connect ERR: {e}")
            out[wh] = {"error": str(e)[:200]}
            continue

        # Get table list with COUNT_BIG (use system view if Fabric has it)
        try:
            _, rows = query(conn, """
                SELECT s.name AS schema_name, t.name AS table_name
                FROM sys.tables t
                JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE s.name NOT IN ('sys','queryinsights','INFORMATION_SCHEMA')
                ORDER BY s.name, t.name
            """)
            tables = [(r[0], r[1]) for r in rows]
        except Exception as e:
            print(f"  list tables ERR: {e}")
            out[wh] = {"error_list": str(e)[:200]}
            continue

        print(f"  {len(tables)} user tables. Counting + sampling top 50...")
        counts = {}
        for sch, t in tables:
            full = f"[{sch}].[{t}]"
            try:
                _, rcs = query(conn, f"SELECT COUNT_BIG(*) FROM {full}")
                counts[f"{sch}.{t}"] = int(rcs[0][0]) if rcs else 0
            except Exception as e:
                counts[f"{sch}.{t}"] = None

        # Top 50 by count
        valid = [(k, v) for k, v in counts.items() if isinstance(v, int)]
        valid.sort(key=lambda x: -x[1])
        top = valid[:50]
        print(f"  top 50 candidates")

        samples = {}
        for k, _v in top:
            sch, t = k.split(".", 1)
            full = f"[{sch}].[{t}]"
            try:
                cols, rows = query(conn, f"SELECT TOP 5 * FROM {full}")
                samples[k] = {"columns": cols, "rows": rows}
            except Exception as e:
                samples[k] = {"error": str(e)[:200]}
        print(f"  sampled {len(samples)} tables")
        out[wh] = {
            "table_count": len(tables),
            "counts": counts,
            "top_50_samples": samples,
        }
        conn.close()

    target = DATA / "13-wh-samples.json"
    with open(target, "w") as f:
        json.dump(out, f, indent=2, default=str)
    sz = target.stat().st_size
    print(f"\nWrote {target} — {sz:,} bytes")


if __name__ == "__main__":
    main()
