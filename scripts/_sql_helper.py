#!/usr/bin/env python3
"""
Query Fabric SQL endpoint with AAD access token.
Usage: _sql_helper.py <server_fqdn> <database> <query>
Outputs JSON: {columns: [...], rows: [[...]]}
"""
import sys, json, struct, subprocess
import pyodbc

SQL_COPT_SS_ACCESS_TOKEN = 1256


def get_token():
    out = subprocess.run(
        ["az", "account", "get-access-token", "--resource", "https://database.windows.net"],
        capture_output=True, text=True, check=True,
    )
    return json.loads(out.stdout)["accessToken"]


def make_token_struct(token: str) -> bytes:
    exptoken = b''
    for ch in bytes(token, 'utf-8'):
        exptoken += bytes({ch}) + b'\0'
    return struct.pack('=i', len(exptoken)) + exptoken


def query(server: str, database: str, sql: str):
    token = get_token()
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};DATABASE={database};Encrypt=yes;TrustServerCertificate=no;"
        f"Connection Timeout=30;"
    )
    conn = pyodbc.connect(
        conn_str, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: make_token_struct(token)}
    )
    cur = conn.cursor()
    cur.execute(sql)
    if cur.description is None:
        return {"columns": [], "rows": [], "rowcount": cur.rowcount}
    cols = [c[0] for c in cur.description]
    rows = []
    for r in cur.fetchall():
        rows.append([
            (str(v)[:500] if v is not None and not isinstance(v, (int, float, bool)) else v)
            for v in r
        ])
    return {"columns": cols, "rows": rows, "rowcount": len(rows)}


if __name__ == "__main__":
    server = sys.argv[1]
    database = sys.argv[2]
    sql = sys.argv[3]
    try:
        result = query(server, database, sql)
        print(json.dumps(result, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
