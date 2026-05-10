#!/usr/bin/env python3
"""
Build Phase 1-4 detail pages + scan v2 enrichments + dependency graphs.

Phase 1: Per-pipeline detail pages (16 active)        → docs/04-orchestration/pipelines/{name}.md
Phase 2: Per-proc narrative pages (top 60)            → docs/03-logic/procs/{family}/{name}.md
Phase 3: Per-table lineage pages (top 50)             → docs/05-data-flow/tables/{schema}-{table}.md
Phase 4: Cross-layer dependency graphs                → docs/05-data-flow/dependency-graphs.md
Plus: Update some existing pages with v2 scan data.
"""
import json, re
from pathlib import Path
from collections import defaultdict, Counter

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
DOCS = REPO / "docs"

WS = "5360a935-1984-4775-895f-f4c90bafa19d"


def load(name):
    p = DATA / name
    if not p.exists():
        return None
    txt = p.read_text()
    if name == "00-inventory-with-ids.json":
        txt = txt.split("\n", 1)[1]
    return json.loads(txt)


inv = load("00-inventory-with-ids.json") or {}
wh_raw = load("03-warehouses-raw.json") or {}
lh_raw = load("02-lakehouses-raw.json") or {}
nb_raw = load("04-notebooks-raw.json") or {}
pipe_raw = load("05-orchestration-raw.json") or {}
procs = load("06-procs-raw.json") or {}
views = load("07-views-raw.json") or {}
sc_data = load("08-shortcuts-files-raw.json") or {}
runs = load("10-runs-raw.json") or {}
v2 = load("12-scan-v2.json") or {}
wh_samples = load("13-wh-samples.json") or {}

ITEM_BY_NAME = {}
ITEM_BY_ID = {}
for type_name, items in inv.items():
    for it in items:
        ITEM_BY_NAME[it["name"]] = {**it, "type": type_name}
        ITEM_BY_ID[it["id"]] = {**it, "type": type_name}


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(content.rstrip() + "\n")
    print(f"  ✓ {path.relative_to(REPO)}")


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) if c is not None else "" for c in r) + " |")
    return "\n".join(out)


def fmt_int(n):
    if isinstance(n, int):
        return f"{n:,}"
    return str(n) if n is not None else ""


def slugify(name):
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def mermaid(s):
    return "```mermaid\n" + s.strip() + "\n```"


# =============================================================
# SHARED PARSING UTILITIES
# =============================================================

def extract_proc_params(body: str):
    """Extract @param declarations from CREATE PROCEDURE."""
    if not body:
        return []
    m = re.search(r"CREATE\s+(?:OR\s+ALTER\s+)?PROCEDURE\s+\[?[\w\.]+\]?\.?\[?[\w]+\]?\s*\(?(.*?)\)?\s*AS\b",
                  body, re.IGNORECASE | re.DOTALL)
    if not m:
        return []
    params_block = m.group(1)
    params = []
    for pm in re.finditer(r"@(\w+)\s+([\w\(\),]+)", params_block):
        params.append((pm.group(1), pm.group(2)))
    return params


SQL_NOISE = {
    # Top-level keywords / clauses that shouldn't be tables
    "SELECT", "WHERE", "ON", "INNER", "LEFT", "RIGHT", "OUTER", "CROSS", "FULL",
    "WITH", "AS", "AND", "OR", "NOT", "IN", "EXISTS", "UNION", "INTERSECT", "EXCEPT",
    "ORDER", "GROUP", "HAVING", "BY", "TOP", "DISTINCT", "ALL", "BETWEEN", "LIKE",
    "OPENROWSET", "OPENJSON", "STRING_SPLIT", "VALUES", "OPENQUERY",
    # Common variable / placeholder noise
    "LAST", "EXISTING", "THE", "PARQUET", "DST", "OD", "ROW", "ROWS", "TABLE",
    "TARGET", "SRC", "SOURCE", "OUTPUT", "RETURN", "RETURNS",
    # Aliases / misc
    "X", "Y", "Z", "T", "S", "A", "B", "C", "D", "M", "N", "E", "F", "G",
    # @ variables / temp tables filtered separately
}


def is_real_table(name: str):
    """Heuristic: is this a likely real table name."""
    if not name or len(name) < 2:
        return False
    if name.startswith("#") or name.startswith("@"):
        return False
    if name.startswith("'") or name.startswith('"'):
        return False
    if name.isdigit():
        return False
    upper = name.upper()
    if upper in SQL_NOISE:
        return False
    # Common system schemas to filter at table level
    if upper in {"SYS", "INFORMATION_SCHEMA", "TEMPDB", "MASTER", "MSDB"}:
        return False
    # Must have at least one alphabetic char
    if not any(c.isalpha() for c in name):
        return False
    return True


def extract_tables_from_body(body: str):
    """Extract source (FROM/JOIN) and sink (INSERT/UPDATE/MERGE) tables."""
    sources = set()
    sinks = set()
    if not body:
        return sources, sinks
    # Sources: FROM/JOIN <schema>.<table>
    src_pat = re.compile(
        r"(?:FROM|JOIN)\s+\[?([^\s\]\.\(\),;]+)\]?\.?\[?([^\s\]\.\(\),;]+)?\]?",
        re.IGNORECASE,
    )
    for m in src_pat.finditer(body):
        a, b = m.group(1), m.group(2)
        if not is_real_table(a):
            continue
        if b and is_real_table(b):
            sources.add(f"{a}.{b}")
        elif b is None or b == "":
            sources.add(a)
    # Sinks
    sink_pat = re.compile(
        r"(?:INSERT\s+INTO|UPDATE|DELETE\s+FROM|MERGE\s+(?:INTO\s+)?|SELECT\s+\*\s+INTO)\s+\[?([^\s\]\.\(\),;]+)\]?\.?\[?([^\s\]\.\(\),;]+)?\]?",
        re.IGNORECASE,
    )
    for m in sink_pat.finditer(body):
        a, b = m.group(1), m.group(2)
        if not is_real_table(a):
            continue
        if b and is_real_table(b):
            sinks.add(f"{a}.{b}")
        elif b is None or b == "":
            sinks.add(a)
    return sources, sinks


def extract_exec_calls(body: str):
    """Find EXEC <proc_name> references."""
    if not body:
        return set()
    out = set()
    pat = re.compile(r"EXEC(?:UTE)?\s+\[?([^\s\]\.\(\),;]+)\]?\.?\[?([^\s\]\.\(\),;]+)?\]?", re.IGNORECASE)
    for m in pat.finditer(body):
        a, b = m.group(1), m.group(2)
        if not a or a.lower() == "sp_executesql":
            continue
        if b:
            out.add(f"{a}.{b}")
        else:
            out.add(a)
    return out


# =============================================================
# PHASE 1 — Per-pipeline detail pages
# =============================================================

def parse_pipeline(name):
    """Read pipeline JSON file and return parsed structure."""
    path = DATA / "pipelines" / f"{name.replace(' ', '_').replace('-', '_').replace('/', '_')}.json"
    if not path.exists():
        # try variants
        for f in (DATA / "pipelines").glob("*.json"):
            try:
                with open(f) as fh:
                    p = json.load(fh)
                if p.get("name") == name:
                    return p
            except Exception:
                pass
        return None
    with open(path) as f:
        return json.load(f)


def walk_activities(activities, depth=0, parent=None):
    """Yield (depth, parent, activity)."""
    for a in activities or []:
        yield depth, parent, a
        # ForEach has 'activities' inside typeProperties
        sub = a.get("typeProperties", {}).get("activities", [])
        if sub:
            yield from walk_activities(sub, depth + 1, a.get("name"))
        # IfCondition has 'ifTrueActivities' and 'ifFalseActivities'
        for branch in ("ifTrueActivities", "ifFalseActivities"):
            sub = a.get("typeProperties", {}).get(branch, [])
            if sub:
                yield from walk_activities(sub, depth + 1, f"{a.get('name')}.{branch}")


def safe_str(obj, max_len=200):
    """Extract a string from various Fabric expression/literal shapes."""
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj[:max_len].replace("|", "\\|").replace("\n", " ")
    if isinstance(obj, dict):
        v = obj.get("value", obj.get("text", ""))
        return safe_str(v, max_len)
    if isinstance(obj, (int, float, bool)):
        return str(obj)
    return str(obj)[:max_len]


def describe_activity(a):
    t = a.get("type", "?")
    tp = a.get("typeProperties", {}) or {}
    desc = []
    try:
        if t == "Lookup":
            src = tp.get("source", {}) or {}
            desc.append(f"Source type: `{src.get('type')}`")
            q = src.get("sqlReaderQuery") or src.get("query")
            if q:
                desc.append(f"Query (truncated): `{safe_str(q, 160)}`")
        elif t == "Filter":
            cond = tp.get("condition")
            desc.append(f"Filter expr: `{safe_str(cond, 200)}`")
        elif t == "ForEach":
            items = tp.get("items")
            desc.append(f"Items: `{safe_str(items, 120)}` · Sequential: {tp.get('isSequential', False)} · BatchCount: {tp.get('batchCount', '—')}")
        elif t == "Copy":
            src = tp.get("source", {}) or {}
            sink = tp.get("sink", {}) or {}
            desc.append(f"Source: `{src.get('type')}`")
            q = src.get("sqlReaderQuery") or src.get("query")
            if q:
                desc.append(f"&nbsp;&nbsp;query: `{safe_str(q, 160)}`")
            desc.append(f"Sink: `{sink.get('type')}`")
            if sink.get("preCopyScript"):
                desc.append(f"&nbsp;&nbsp;preCopy: `{safe_str(sink['preCopyScript'], 120)}`")
            if sink.get("tableOption"):
                desc.append(f"&nbsp;&nbsp;tableOption: `{sink.get('tableOption')}`")
        elif t == "Script":
            scripts = tp.get("scripts", []) or []
            for s in scripts[:3]:
                desc.append(f"Script: `{safe_str(s.get('text'), 200)}`")
        elif t == "ExecutePipeline":
            ref = tp.get("pipeline", {}) or {}
            desc.append(f"Calls pipeline: `{ref.get('referenceName')}` (id `{(ref.get('artifactId','') or '')[:13]}…`)")
        elif t == "IfCondition":
            desc.append(f"Expr: `{safe_str(tp.get('expression'), 200)}`")
        elif t == "SetVariable":
            desc.append(f"Variable `{tp.get('variableName','?')}` = `{safe_str(tp.get('value'), 100)}`")
        elif t in ("WebActivity", "Web", "Office365Outlook"):
            desc.append(f"URL: `{safe_str(tp.get('url'), 120)}`")
        elif t == "AppendVariable":
            desc.append(f"Append `{safe_str(tp.get('value'), 80)}` to `{tp.get('variableName','?')}`")
    except Exception as e:
        desc.append(f"_(parse error: {e})_")
    return desc


def build_phase1_pipelines():
    """Generate per-pipeline detail pages."""
    print("\n=== Phase 1: pipeline detail pages ===")
    out_dir = DOCS / "04-orchestration" / "pipelines"
    out_dir.mkdir(parents=True, exist_ok=True)

    pipe_items = inv.get("DataPipeline", [])
    pipe_summary_md = ["# 🔁 Pipeline Detail Pages",
                       "",
                       "[← Orchestration](../README.md) · [← Root](../../../README.md)",
                       "",
                       "Per-pipeline activity-by-activity walkthroughs.",
                       ""]
    pipe_summary_md.append("## Index")
    pipe_summary_md.append("")

    for it in sorted(pipe_items, key=lambda x: x["name"]):
        name = it["name"]
        pid = it["id"]
        pdef = parse_pipeline(name)
        slug = slugify(name)
        if not pdef:
            print(f"  ⚠️  No definition for {name}, skip")
            continue

        L = []
        L.append(f"# 🔁 {name}")
        L.append("")
        L.append(f"_Item ID `{pid}`_")
        L.append("")
        L.append(f"[← Pipelines](README.md) · [← Orchestration](../README.md) · [← Root](../../../README.md)")
        L.append("")

        summary = pdef.get("summary", "")
        if summary:
            L.append("## Summary")
            L.append("")
            L.append(summary)
            L.append("")

        properties = pdef.get("properties", {})
        activities = properties.get("activities", [])
        variables = properties.get("variables", {})
        params = properties.get("parameters", {})

        if not activities:
            L.append("## Status")
            L.append("")
            L.append("⚠️ **EMPTY pipeline** — no activities defined.")
            L.append("")
            write(out_dir / f"{slug}.md", "\n".join(L))
            pipe_summary_md.append(f"- [`{name}`]({slug}.md) — *empty*")
            continue

        # Activities tree (Mermaid)
        L.append("## Activities tree")
        L.append("")
        merm = ["graph TB"]
        idx = 0
        node_ids = {}
        for d, parent, a in walk_activities(activities):
            idx += 1
            nid = f"a{idx}"
            label = f"{a.get('name','?')}<br/><i>{a.get('type','?')}</i>"
            merm.append(f"    {nid}[{label}]")
            node_ids[a.get("name")] = nid
            if parent and parent in node_ids:
                merm.append(f"    {node_ids[parent]} --> {nid}")
            # Connect by 'dependsOn' if exists (top-level only)
            if d == 0:
                for dep in a.get("dependsOn", []):
                    if isinstance(dep, dict):
                        dnm = dep.get("activity")
                    elif isinstance(dep, str):
                        dnm = dep
                    else:
                        continue
                    if dnm and dnm in node_ids:
                        merm.append(f"    {node_ids[dnm]} --> {nid}")
        L.append(mermaid("\n".join(merm)))
        L.append("")

        # Activity table
        L.append("## Activity-by-activity")
        L.append("")
        rows = []
        for d, parent, a in walk_activities(activities):
            indent = "&nbsp;&nbsp;" * d
            desc_lines = describe_activity(a)
            desc = "<br/>".join(desc_lines) if desc_lines else "—"
            rows.append([
                f"{indent}{a.get('name','?')}",
                a.get('type','?'),
                desc,
            ])
        L.append(md_table(["Activity", "Type", "Detail"], rows))
        L.append("")

        # Parameters / Variables
        if params:
            L.append("## Parameters")
            L.append("")
            L.append(md_table(["Name", "Type", "Default"], [
                [f"`{k}`", v.get("type", "?"), str(v.get("defaultValue", ""))[:80]]
                for k, v in params.items()
            ]))
            L.append("")

        if variables:
            L.append("## Variables")
            L.append("")
            L.append(md_table(["Name", "Type"], [
                [f"`{k}`", v.get("type", "?") if isinstance(v, dict) else str(v)]
                for k, v in variables.items()
            ]))
            L.append("")

        # Run history
        rinfo = runs.get(name, {}).get("runs", [])
        if isinstance(rinfo, list) and rinfo:
            L.append(f"## Run history (last {len(rinfo)} runs)")
            L.append("")
            sorted_r = sorted(rinfo, key=lambda r: r.get("startTimeUtc", ""), reverse=True)
            from collections import Counter
            statuses = Counter(r.get("status", "?") for r in rinfo)
            L.append(f"**Status distribution:** {dict(statuses)}")
            L.append("")
            L.append(md_table(
                ["#", "Start (UTC)", "End", "Status", "Type"],
                [[i+1, (r.get("startTimeUtc") or "?")[:19],
                  (r.get("endTimeUtc") or "?")[:19],
                  r.get("status", "?"),
                  r.get("invokeType", "?")]
                 for i, r in enumerate(sorted_r[:10])],
            ))
            L.append("")

        L.append("## Raw definition")
        L.append("")
        L.append(f"Full JSON: [`data/pipelines/{name.replace(' ', '_').replace('-', '_')}.json`](../../../data/pipelines/{name.replace(' ', '_').replace('-', '_')}.json)")
        L.append("")

        L.append("---")
        write(out_dir / f"{slug}.md", "\n".join(L))
        pipe_summary_md.append(f"- [`{name}`]({slug}.md) — {summary[:100]}{'…' if len(summary) > 100 else ''}")

    pipe_summary_md.append("")
    pipe_summary_md.append("---")
    write(out_dir / "README.md", "\n".join(pipe_summary_md))


# =============================================================
# PHASE 2 — Per-proc narrative pages
# =============================================================

def proc_family(name):
    n = name.lower()
    if "createtablefromparquet" in n or "tablefromparquet" in n: return "parquet-loaders"
    if "incremental" in n: return "incremental"
    if "scd2" in n: return "scd2"
    if "snapshot" in n: return "snapshot"
    if "audit" in n: return "audit"
    if "alert" in n or "sla" in n: return "alert"
    if "email" in n: return "email"
    if "merge" in n: return "merge"
    if "refresh" in n or "update" in n: return "refresh"
    if "validate" in n or "check" in n: return "validate"
    if "drop" in n or "truncate" in n: return "cleanup"
    if "history" in n or "log" in n: return "history-log"
    if "load" in n or "create" in n or "populate" in n: return "load"
    if "dictionary" in n: return "dictionary"
    return "other"


def build_phase2_procs():
    """Generate per-proc narrative pages for top procs."""
    print("\n=== Phase 2: proc detail pages ===")
    out_dir = DOCS / "03-logic" / "procs"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Collect all procs with body
    all_procs = []
    for wh, plist in procs.items():
        for p in plist:
            if isinstance(p.get("definition"), str):
                all_procs.append({**p, "warehouse": wh, "family": proc_family(p["name"])})
    print(f"  total procs with body: {len(all_procs)}")

    # Index by family
    by_family = defaultdict(list)
    for p in all_procs:
        by_family[p["family"]].append(p)

    # Top 60 by importance: prefer ETL_Framework, then largest bodies
    def score(p):
        s = 0
        if p["warehouse"] == "ETL_Framework":
            s += 1000
        s += min(len(p.get("definition", "")), 50000) // 100
        return s
    all_procs.sort(key=score, reverse=True)
    top_procs = all_procs[:60]

    # Build index
    idx_md = ["# ⚙️ Stored Procedures — Detail Pages",
              "",
              "[← Logic](../README.md) · [← Root](../../../README.md)",
              "",
              f"Per-proc narrative explanation. Top {len(top_procs)} procs (out of {len(all_procs)} total) get detail pages — selected by importance (ETL_Framework first, then by body size).",
              "",
              "## By family",
              ""]

    for fam, plist in sorted(by_family.items(), key=lambda x: -len(x[1])):
        fam_dir = out_dir / fam
        idx_md.append(f"### `{fam}` ({len(plist)} procs)")
        idx_md.append("")
        # Show all in family if small, top 10 if big
        for p in plist[:30]:
            slug = slugify(f"{p['warehouse']}-{p['name']}")
            if p in top_procs:
                idx_md.append(f"- [`{p['warehouse']}.{p['schema']}.{p['name']}`]({fam}/{slug}.md) — {len(p['definition']):,} chars")
            else:
                idx_md.append(f"- `{p['warehouse']}.{p['schema']}.{p['name']}` — {len(p['definition']):,} chars _(no detail page)_")
        if len(plist) > 30:
            idx_md.append(f"- _… and {len(plist)-30} more_")
        idx_md.append("")

    idx_md.append("---")
    write(out_dir / "README.md", "\n".join(idx_md))

    # Build per-proc pages for top 60
    for p in top_procs:
        slug = slugify(f"{p['warehouse']}-{p['name']}")
        fam = p["family"]
        body = p["definition"]
        params = extract_proc_params(body)
        sources, sinks = extract_tables_from_body(body)
        exec_calls = extract_exec_calls(body)

        L = []
        L.append(f"# `{p['name']}`")
        L.append("")
        L.append(f"_Schema: `{p['schema']}` · Warehouse: `{p['warehouse']}` · Family: `{fam}`_")
        L.append("")
        L.append(f"_Modified: {p.get('modify_date', '?')} · Code size: {len(body):,} chars_")
        L.append("")
        L.append(f"[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)")
        L.append("")

        # Inferred narrative
        L.append("## What it does")
        L.append("")
        narrative = []
        if sources and sinks:
            narrative.append(f"Reads from {len(sources)} sources and writes to {len(sinks)} sinks.")
        elif sources:
            narrative.append(f"Read-only — pulls data from {len(sources)} sources.")
        elif sinks:
            narrative.append(f"Write-only — writes to {len(sinks)} sinks.")
        else:
            narrative.append(f"Pure compute — no detected reads/writes (may be utility / control flow).")
        if exec_calls:
            narrative.append(f"Calls {len(exec_calls)} other procs.")
        if "TRY" in body and "CATCH" in body:
            narrative.append("Has error handling (TRY/CATCH).")
        if "TRANSACTION" in body.upper():
            narrative.append("Uses explicit transaction.")
        if "CURSOR" in body.upper():
            narrative.append("⚠️ Uses cursor (typically slow).")
        if "DROP TABLE" in body.upper():
            narrative.append("⚠️ Drops tables (destructive).")
        L.append(" ".join(narrative))
        L.append("")

        # Parameters
        L.append("## Parameters")
        L.append("")
        if params:
            L.append(md_table(["Name", "Type"], [[f"`@{n}`", t] for n, t in params]))
        else:
            L.append("_(none — runs with no parameters)_")
        L.append("")

        # Inputs (sources)
        L.append("## Inputs (FROM/JOIN)")
        L.append("")
        if sources:
            for s in sorted(sources)[:30]:
                L.append(f"- `{s}`")
            if len(sources) > 30:
                L.append(f"- _… +{len(sources)-30} more_")
        else:
            L.append("_(none detected)_")
        L.append("")

        # Outputs (sinks)
        L.append("## Outputs (INSERT/UPDATE/MERGE)")
        L.append("")
        if sinks:
            for s in sorted(sinks)[:30]:
                L.append(f"- `{s}`")
            if len(sinks) > 30:
                L.append(f"- _… +{len(sinks)-30} more_")
        else:
            L.append("_(none detected)_")
        L.append("")

        # Calls
        L.append("## Calls (EXEC)")
        L.append("")
        if exec_calls:
            for c in sorted(exec_calls)[:20]:
                L.append(f"- `{c}`")
        else:
            L.append("_(none)_")
        L.append("")

        # Code excerpt
        L.append("## Code (first 80 lines)")
        L.append("")
        body_lines = body.split("\n")
        excerpt = "\n".join(body_lines[:80])
        if len(body_lines) > 80:
            excerpt += f"\n-- … [{len(body_lines) - 80} more lines truncated, full body in data/06-procs-raw.json] --"
        L.append("```sql")
        L.append(excerpt)
        L.append("```")
        L.append("")

        L.append("---")
        write(out_dir / fam / f"{slug}.md", "\n".join(L))


# =============================================================
# PHASE 3 — Per-table lineage pages
# =============================================================

def build_phase3_table_lineage():
    """Cross-reference all procs/views/notebooks/pipelines → tables, then per-table lineage page."""
    print("\n=== Phase 3: table lineage pages ===")

    # Build (table → readers, table → writers) maps
    table_readers = defaultdict(set)  # full_name → set of (kind, name)
    table_writers = defaultdict(set)

    # Iterate procs
    for wh, plist in procs.items():
        for p in plist:
            body = p.get("definition")
            if not isinstance(body, str):
                continue
            sources, sinks = extract_tables_from_body(body)
            label = f"proc:{wh}.{p['schema']}.{p['name']}"
            for s in sources:
                table_readers[s].add(label)
            for s in sinks:
                table_writers[s].add(label)

    # Iterate views
    for db, vlist in views.items():
        for v in vlist:
            body = v.get("definition")
            if not isinstance(body, str) or v.get("schema") in ("sys", "queryinsights"):
                continue
            sources, _ = extract_tables_from_body(body)
            label = f"view:{db}.{v['schema']}.{v['name']}"
            for s in sources:
                table_readers[s].add(label)

    # Iterate notebooks (parse code)
    for nb_name, info in nb_raw.items():
        if not isinstance(info, dict):
            continue
        for inp in info.get("inputs", []) or []:
            table_readers[inp].add(f"nb:{nb_name}")
        for out in info.get("outputs", []) or []:
            table_writers[out].add(f"nb:{nb_name}")

    # Top 50 most-referenced tables (combined readers + writers)
    all_tables = set(table_readers.keys()) | set(table_writers.keys())
    table_score = {t: len(table_readers.get(t, set())) + len(table_writers.get(t, set())) for t in all_tables}
    top_tables = sorted(table_score.items(), key=lambda x: -x[1])[:50]

    out_dir = DOCS / "05-data-flow" / "tables"
    out_dir.mkdir(parents=True, exist_ok=True)

    idx_md = ["# 🔍 Table Lineage — Top 50 most-referenced tables",
              "",
              "[← Data Flow](../README.md) · [← Root](../../../README.md)",
              "",
              f"Cross-referenced from all 192 procs + 145 views + 18 notebooks.",
              ""]
    idx_md.append(md_table(
        ["Table", "Readers", "Writers", "Total refs"],
        [[f"[`{t}`]({slugify(t)}.md)", len(table_readers.get(t, set())), len(table_writers.get(t, set())), s]
         for t, s in top_tables],
    ))
    idx_md.append("")
    idx_md.append("---")
    write(out_dir / "README.md", "\n".join(idx_md))

    # Per-table page
    for t, _score in top_tables:
        readers = sorted(table_readers.get(t, set()))
        writers = sorted(table_writers.get(t, set()))

        L = []
        L.append(f"# 🔍 `{t}`")
        L.append("")
        L.append(f"[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)")
        L.append("")

        # Mini lineage Mermaid
        L.append("## Lineage")
        L.append("")
        merm = ["graph LR"]
        merm.append(f"    T[\"{t}\"]:::tbl")
        for w in writers[:10]:
            kind, nm = w.split(":", 1)
            wid = f"w_{slugify(nm)[:20]}"
            ic = "📓" if kind == "nb" else "⚙️" if kind == "proc" else "👁️"
            merm.append(f"    {wid}[\"{ic} {nm[:40]}\"] -- writes --> T")
        for r in readers[:10]:
            kind, nm = r.split(":", 1)
            rid = f"r_{slugify(nm)[:20]}"
            ic = "📓" if kind == "nb" else "⚙️" if kind == "proc" else "👁️"
            merm.append(f"    T -- read by --> {rid}[\"{ic} {nm[:40]}\"]")
        merm.append("    classDef tbl fill:#cbd5e1,stroke:#475569;")
        L.append(mermaid("\n".join(merm)))
        L.append("")

        # Writers
        L.append(f"## Writers ({len(writers)})")
        L.append("")
        if writers:
            for w in writers[:30]:
                kind, nm = w.split(":", 1)
                ic = "📓" if kind == "nb" else "⚙️" if kind == "proc" else "👁️"
                L.append(f"- {ic} `{nm}`")
            if len(writers) > 30:
                L.append(f"- _… +{len(writers)-30} more_")
        else:
            L.append("_(no writers detected — possibly read-only or written by external process)_")
        L.append("")

        # Readers
        L.append(f"## Readers ({len(readers)})")
        L.append("")
        if readers:
            for r in readers[:30]:
                kind, nm = r.split(":", 1)
                ic = "📓" if kind == "nb" else "⚙️" if kind == "proc" else "👁️"
                L.append(f"- {ic} `{nm}`")
            if len(readers) > 30:
                L.append(f"- _… +{len(readers)-30} more_")
        else:
            L.append("_(no readers detected)_")
        L.append("")

        L.append("---")
        write(out_dir / f"{slugify(t)}.md", "\n".join(L))


# =============================================================
# PHASE 4 — Cross-layer dependency graphs
# =============================================================

def build_phase4_graphs():
    """Build proc call graph + pipeline→proc map + table read/write graph."""
    print("\n=== Phase 4: dependency graphs ===")

    # 1. Proc call graph (EXEC → EXEC)
    call_edges = []  # (from_proc, to_proc)
    proc_index = {}  # name → (warehouse, schema, name)
    for wh, plist in procs.items():
        for p in plist:
            if isinstance(p.get("definition"), str):
                proc_index[p["name"]] = (wh, p["schema"], p["name"])
                proc_index[f"{p['schema']}.{p['name']}"] = (wh, p["schema"], p["name"])
                proc_index[f"[{p['schema']}].[{p['name']}]"] = (wh, p["schema"], p["name"])
                exec_calls = extract_exec_calls(p["definition"])
                for c in exec_calls:
                    call_edges.append((p["name"], c))

    # 2. Pipeline → proc map (Script activities running EXEC ...)
    pipe_proc_edges = []
    for pf in (DATA / "pipelines").glob("*.json"):
        try:
            pdef = json.load(open(pf))
        except Exception:
            continue
        pipe_name = pdef.get("name", pf.stem)
        for d, parent, a in walk_activities(pdef.get("properties", {}).get("activities", [])):
            if a.get("type") == "Script":
                scripts = a.get("typeProperties", {}).get("scripts", [])
                for s in scripts:
                    txt = s.get("text", "")
                    if isinstance(txt, dict):
                        txt = txt.get("value", "")
                    if isinstance(txt, str):
                        for ec in extract_exec_calls(txt):
                            pipe_proc_edges.append((pipe_name, ec))
            if a.get("type") == "Copy":
                # preCopyScript may have proc calls
                ps = a.get("typeProperties", {}).get("sink", {}).get("preCopyScript")
                if isinstance(ps, dict):
                    ps = ps.get("value", "")
                if isinstance(ps, str):
                    for ec in extract_exec_calls(ps):
                        pipe_proc_edges.append((pipe_name, ec))

    # 3. Top tables read/write graph (top 30 tables only for readability)
    L = []
    L.append("# 🕸️ Cross-Layer Dependency Graphs")
    L.append("")
    L.append("[← Data Flow](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## A. Proc call graph (`EXEC` → `EXEC`)")
    L.append("")
    L.append(f"Total EXEC edges detected: **{len(call_edges)}**.")
    L.append("")
    if call_edges:
        # Aggregate
        edge_count = Counter(call_edges)
        # Top 50 edges by frequency
        top_edges = edge_count.most_common(50)
        merm = ["graph TB"]
        seen_nodes = set()
        for (a, b), cnt in top_edges:
            for n in (a, b):
                if n not in seen_nodes:
                    seen_nodes.add(n)
                    safe_n = re.sub(r"[^\w]", "_", n)[:25]
                    merm.append(f"    {safe_n}[\"{n[:35]}\"]")
            sa = re.sub(r"[^\w]", "_", a)[:25]
            sb = re.sub(r"[^\w]", "_", b)[:25]
            merm.append(f"    {sa} --> {sb}")
        L.append(mermaid("\n".join(merm)))
        L.append("")
    else:
        L.append("_(no EXEC calls detected)_")
        L.append("")

    L.append("## B. Pipeline → Proc invocations")
    L.append("")
    L.append(f"Total pipeline→proc edges: **{len(pipe_proc_edges)}**.")
    L.append("")
    if pipe_proc_edges:
        edge_count = Counter(pipe_proc_edges)
        top_edges = edge_count.most_common(40)
        merm = ["graph LR"]
        seen = set()
        for (a, b), cnt in top_edges:
            for n in (a, b):
                if n not in seen:
                    seen.add(n)
                    safe_n = re.sub(r"[^\w]", "_", n)[:25]
                    if a == n:
                        merm.append(f"    {safe_n}([{n[:35]}]):::pipe")
                    else:
                        merm.append(f"    {safe_n}[{n[:35]}]:::proc")
            sa = re.sub(r"[^\w]", "_", a)[:25]
            sb = re.sub(r"[^\w]", "_", b)[:25]
            merm.append(f"    {sa} --> {sb}")
        merm.append("    classDef pipe fill:#dbeafe,stroke:#2563eb;")
        merm.append("    classDef proc fill:#f0e8fd,stroke:#94f;")
        L.append(mermaid("\n".join(merm)))
        L.append("")
    else:
        L.append("_(no pipeline→proc invocations detected via Script activities)_")
        L.append("")

    L.append("## C. Top-30 hottest tables (read+write graph)")
    L.append("")
    # Reuse data from phase 3
    table_readers = defaultdict(set)
    table_writers = defaultdict(set)
    for wh, plist in procs.items():
        for p in plist:
            body = p.get("definition")
            if not isinstance(body, str): continue
            sources, sinks = extract_tables_from_body(body)
            label = p["name"]
            for s in sources:
                table_readers[s].add(label)
            for s in sinks:
                table_writers[s].add(label)
    all_tbls = set(table_readers.keys()) | set(table_writers.keys())
    score = {t: len(table_readers.get(t, set())) + len(table_writers.get(t, set())) for t in all_tbls}
    top30 = sorted(score.items(), key=lambda x: -x[1])[:30]
    merm = ["graph LR"]
    for t, _ in top30:
        st = re.sub(r"[^\w]", "_", t)[:25]
        merm.append(f"    {st}[\"{t[:30]}\"]:::tbl")
        for w in list(table_writers.get(t, set()))[:5]:
            sw = re.sub(r"[^\w]", "_", w)[:20]
            merm.append(f"    {sw}([{w[:25]}]) --> {st}")
        for r in list(table_readers.get(t, set()))[:5]:
            sr = re.sub(r"[^\w]", "_", r)[:20]
            merm.append(f"    {st} --> {sr}([{r[:25]}])")
    merm.append("    classDef tbl fill:#cbd5e1,stroke:#475569;")
    L.append(mermaid("\n".join(merm)))
    L.append("")

    L.append("---")
    L.append("")
    L.append("**Per-table detail:** [Table lineage pages](tables/README.md) — top 50 most-referenced tables.")
    write(DOCS / "05-data-flow" / "dependency-graphs.md", "\n".join(L))


# =============================================================
# Update existing pages with v2 scan info
# =============================================================

def update_introduction_with_git():
    """Add Git integration block to 01-introduction.md."""
    git_info = v2.get("git_connection", {})
    if not git_info or "_error" in git_info:
        return
    p = git_info.get("gitProviderDetails", {})
    snippet = f"""

## 🔄 Git integration (Azure DevOps)

The workspace is **`{git_info.get('gitConnectionState','?')}`** to Azure DevOps:

| Field | Value |
|---|---|
| Provider | `{p.get('gitProviderType','?')}` |
| Organization | `{p.get('organizationName','?')}` |
| Project | `{p.get('projectName','?')}` |
| Repository | `{p.get('repositoryName','?')}` |
| Branch | `{p.get('branchName','?')}` |
| Directory | `{p.get('directoryName','?')}` |
| Sync state | `{git_info.get('gitConnectionState','?')}` |

→ **The Azure DevOps repo is the source of truth.** Changes to items in this workspace should flow through Git PRs in `{p.get('organizationName','?')}/{p.get('projectName','?')}/{p.get('repositoryName','?')}`. Direct UI edits without git commit will desync.
"""
    p_md = DOCS / "01-introduction.md"
    if p_md.exists():
        existing = p_md.read_text()
        if "Git integration" not in existing:
            with open(p_md, "a") as f:
                f.write(snippet)
            print(f"  ✓ Updated 01-introduction.md (added Git integration)")


def build_connections_page():
    """Generate connections page from v2 scan."""
    conns = v2.get("connections", {}).get("value", [])
    if not conns:
        return
    out_dir = DOCS / "06-cross-workspace"
    L = []
    L.append("# 🔌 Connections (Data Sources)")
    L.append("")
    L.append("[← Cross-Workspace](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append(f"**{len(conns)} connections** visible to current user, used by pipelines + dataflows.")
    L.append("")
    rows = []
    for c in conns:
        cd = c.get("connectionDetails", {}) if isinstance(c.get("connectionDetails"), dict) else {}
        ct = c.get("connectivityType", "?")
        cred = c.get("credentialDetails", {}) if isinstance(c.get("credentialDetails"), dict) else {}
        rows.append([
            f"`{c.get('displayName','?')[:60]}`",
            f"`{c.get('id','')[:13]}…`",
            cd.get("type", "?"),
            ct,
            cred.get("credentialType", "?"),
            f"`{(cd.get('path') or '?')[:80]}`",
        ])
    L.append(md_table(
        ["Display name", "ID", "Type", "Connectivity", "Credential", "Path"],
        rows,
    ))
    L.append("")
    L.append("## Distribution by type")
    L.append("")
    type_count = Counter(c.get("connectionDetails", {}).get("type", "?") for c in conns)
    L.append(md_table(["Type", "Count"], [[f"`{k}`", v] for k, v in type_count.most_common()]))
    L.append("")
    L.append("---")
    write(out_dir / "connections.md", "\n".join(L))


def build_workspace_settings_page():
    """Generate workspace Spark settings + capacity page."""
    spark = v2.get("spark_settings", {})
    pools = v2.get("spark_pools", {})
    libs = v2.get("spark_libraries", {})
    capacity = v2.get("our_capacity")
    folders = v2.get("folders", {})

    L = []
    L.append("# ⚙️ Workspace Settings")
    L.append("")
    L.append("[← Operations](README.md) · [← Root](../../README.md)")
    L.append("")

    L.append("## Spark Settings (workspace-level)")
    L.append("")
    if spark and "_error" not in spark:
        L.append(md_table(
            ["Setting", "Value"],
            [
                ["Default runtime", f"`{spark.get('environment',{}).get('runtimeVersion','?')}`"],
                ["Automatic logging", str(spark.get("automaticLog", {}).get("enabled"))],
                ["High-concurrency interactive", str(spark.get("highConcurrency",{}).get("notebookInteractiveRunEnabled"))],
                ["High-concurrency pipeline", str(spark.get("highConcurrency",{}).get("notebookPipelineRunEnabled"))],
                ["Conservative job admission", str(spark.get("job",{}).get("conservativeJobAdmissionEnabled"))],
                ["Session timeout (min)", spark.get("job",{}).get("sessionTimeoutInMinutes")],
                ["Customize compute", str(spark.get("pool",{}).get("customizeComputeEnabled"))],
                ["Default pool ID", f"`{spark.get('pool',{}).get('defaultPool',{}).get('id','?')}`"],
            ],
        ))
    else:
        L.append("_(unable to fetch Spark settings)_")
    L.append("")

    L.append("## Spark Pools")
    L.append("")
    pool_list = pools.get("value", []) if isinstance(pools, dict) else []
    if pool_list:
        L.append(md_table(
            ["Name", "Type", "Node", "Auto-scale"],
            [[p.get("name","?"), p.get("type","?"),
              p.get("nodeSize","?"),
              f"{p.get('autoScale',{}).get('minNodeCount','?')}-{p.get('autoScale',{}).get('maxNodeCount','?')}"]
             for p in pool_list],
        ))
    else:
        L.append("_(no custom pools — using starter pools)_")
    L.append("")

    L.append("## Capacity")
    L.append("")
    if capacity:
        L.append(md_table(["Field", "Value"], [
            ["ID", f"`{capacity.get('id')}`"],
            ["SKU", f"`{capacity.get('sku')}`"],
            ["State", f"`{capacity.get('state')}`"],
            ["Region", f"`{capacity.get('region')}`"],
            ["Display name", f"`{capacity.get('displayName')}`"],
        ]))
    else:
        L.append("_Capacity `30d06c17-b0f4-4709-9a20-e29c96e8863e` not in current scope (cross-subscription). Region East US per workspace settings._")
    L.append("")

    L.append("## Workspace Folders")
    L.append("")
    folder_list = folders.get("value", []) if isinstance(folders, dict) else []
    if folder_list:
        L.append(md_table(["Name", "ID"], [[f"`{f.get('displayName')}`", f"`{f.get('id','')[:13]}…`"] for f in folder_list]))
    else:
        L.append("_(no folders)_")
    L.append("")

    L.append("---")
    write(DOCS / "08-operations" / "workspace-settings.md", "\n".join(L))


# =============================================================
# Main
# =============================================================

def main():
    update_introduction_with_git()
    build_connections_page()
    build_workspace_settings_page()
    build_phase1_pipelines()
    build_phase2_procs()
    build_phase3_table_lineage()
    build_phase4_graphs()
    print("\nDone! Update root README + render new SVGs next.")


if __name__ == "__main__":
    main()
