#!/usr/bin/env python3
"""
Build EnterpriseData-Dev-Docs/ — a GitHub-style documentation repo.

Generates ~40 markdown files from raw scan JSONs in data/.
Heavy use of Mermaid diagrams. Cross-linked via relative paths.

Run from repo root:
    python3 scripts/_build_docs.py
"""
import json
from pathlib import Path
from collections import defaultdict, Counter

# Resolve repo root regardless of where the script is invoked
SCRIPT = Path(__file__).resolve()
REPO = SCRIPT.parent.parent  # …/EnterpriseData-Dev-Docs/
DATA = REPO / "data"
DOCS = REPO / "docs"
IMAGES = REPO / "images"

WS_ID = "5360a935-1984-4775-895f-f4c90bafa19d"
PROD_WS = "ce4e6503-b368-496b-95e2-63b43c8b3b0a"


def load(name):
    p = DATA / name
    if not p.exists():
        return None
    txt = p.read_text()
    if name == "00-inventory-with-ids.json":
        txt = txt.split("\n", 1)[1]
    return json.loads(txt)


inv = load("00-inventory-with-ids.json") or {}
perms = load("01-permissions-raw.json") or {}
lh = load("02-lakehouses-raw.json") or {}
wh = load("03-warehouses-raw.json") or {}
nb_meta = load("04-notebooks-raw.json") or {}
pipe_meta = load("05-orchestration-raw.json") or {}
procs = load("06-procs-raw.json") or {}
views = load("07-views-raw.json") or {}
sc_data = load("08-shortcuts-files-raw.json") or {}
runs = load("10-runs-raw.json") or {}

ITEM_BY_NAME = {}
for type_name, items in inv.items():
    for it in items:
        ITEM_BY_NAME[it["name"]] = {**it, "type": type_name}


# =============================================================
# Helpers
# =============================================================

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
    return str(n)


def short_id(s):
    return s[:13] + "…" if len(s) > 13 else s


def mermaid(s):
    return "```mermaid\n" + s.strip() + "\n```"


def get_run_status(name, type_name="DataPipeline"):
    info = runs.get(name, {})
    if isinstance(info, dict):
        rlist = info.get("runs", [])
        if isinstance(rlist, list) and rlist:
            return f"✅ Active ({len(rlist)} runs)"
    if type_name in ("DataPipeline", "Notebook", "Dataflow"):
        return "💤 Dormant"
    return "—"


# =============================================================
# Root README
# =============================================================

def build_root_readme():
    L = []
    L.append("# 🧠 EnterpriseData-Dev — Documentation Repository")
    L.append("")
    L.append("> **Living documentation** for Microsoft Fabric workspace `EnterpriseData-Dev` (Ashley Furniture). Generated from a comprehensive scan capturing all 71 items, 192 stored procedures, 145 views, 412 shortcuts, 412 GUIDs cross-referenced, and full code bodies.")
    L.append("")
    L.append("## 📌 Workspace identity")
    L.append("")
    L.append(md_table(
        ["Field", "Value"],
        [
            ["Workspace name", "`EnterpriseData-Dev`"],
            ["Workspace ID", f"`{WS_ID}`"],
            ["Tenant", "Ashley Furniture (`@Ashleyfurniture.com`)"],
            ["Capacity", "`30d06c17-...` East US, Dedicated, Large dataset"],
            ["Workspace SPN", "`14bfa211-3cab-...`"],
            ["Total items scanned", "**71**"],
            ["Scan date", "2026-05-08"],
            ["Doc generated", "2026-05-10"],
        ],
    ))
    L.append("")
    L.append("## 📊 At a glance")
    L.append("")
    L.append("![Stats](https://img.shields.io/badge/items-71-blue) ![Stats](https://img.shields.io/badge/warehouses-11-blue) ![Stats](https://img.shields.io/badge/lakehouses-5-cyan) ![Stats](https://img.shields.io/badge/pipelines-22-green) ![Stats](https://img.shields.io/badge/notebooks-18-orange) ![Stats](https://img.shields.io/badge/stored_procs-192-purple) ![Stats](https://img.shields.io/badge/views-145-pink) ![Stats](https://img.shields.io/badge/risks-28-red)")
    L.append("")
    L.append("## 🗺️ Repository map")
    L.append("")
    L.append(mermaid("""mindmap
  root((🧠 EnterpriseData<br/>Dev))
    📘 01 Introduction
      Architecture overview
      Business context
    📦 02 Storage
      11 Warehouses
      5 Lakehouses
      1 SQLDatabase
    🧠 03 Logic
      192 Procedures
      145 Views
      18 Notebooks
    🔁 04 Orchestration
      22 Pipelines
      Mirror Databricks
      Mounted ADF
      Dataflow Reflex
    🔀 05 Data Flow
      Source to Bronze
      Bronze to Silver
      Silver to Gold
    🔗 06 Cross-Workspace
      PROD dependencies
      ADLS storage
      Inaccessible refs
    🔐 07 Permissions
      34 principals
      Service Principals
    📊 08 Operations
      Run history
      Monitoring
      Environments
    ⚠️ 09 Risks
      28 issues
      Critical: 1
      High: 4
    📚 99 Reference
      Glossary
      ID reference
      File index"""))
    L.append("")
    L.append("## 📚 Documentation index")
    L.append("")
    L.append("| § | Topic | Description |")
    L.append("|---|---|---|")
    L.append("| 01 | [📘 Introduction](docs/01-introduction.md) | What is this workspace, business context, key concepts |")
    L.append("| 02 | [📦 Storage Layer](docs/02-storage/README.md) | 11 WH + 5 LH + 1 SQLDB — where data lives |")
    L.append("| 03 | [🧠 Logic Layer](docs/03-logic/README.md) | 192 procs + 145 views + 18 notebooks — what computes |")
    L.append("| 04 | [🔁 Orchestration](docs/04-orchestration/README.md) | 22 pipelines + mirror + ADF — what schedules |")
    L.append("| 05 | [🔀 Data Flow](docs/05-data-flow/README.md) | End-to-end lineage source → sink |")
    L.append("| 06 | [🔗 Cross-Workspace](docs/06-cross-workspace/README.md) | External dependencies |")
    L.append("| 07 | [🔐 Permissions](docs/07-permissions/README.md) | 34 principals, role matrix, SPN risks |")
    L.append("| 08 | [📊 Operations](docs/08-operations/README.md) | Run history + monitoring + envs |")
    L.append("| 09 | [⚠️ Risks](docs/09-risks/README.md) | 28-risk register |")
    L.append("| 99 | [📚 Reference](docs/99-reference/README.md) | Glossary, IDs, methodology |")
    L.append("")
    L.append("## 🚦 Reading recipes")
    L.append("")
    L.append("### Recipe 1 — New contributor onboarding (30 min)")
    L.append("1. [📘 Introduction](docs/01-introduction.md) — 5 min")
    L.append("2. [📦 Storage overview](docs/02-storage/README.md) — 5 min")
    L.append("3. [🔀 Data Flow](docs/05-data-flow/README.md) — 10 min")
    L.append("4. [⚠️ Top 5 risks](docs/09-risks/README.md) — 10 min")
    L.append("")
    L.append("### Recipe 2 — Debug a specific table/proc/pipeline")
    L.append("1. [99 ID Reference](docs/99-reference/id-reference.md) — find the item")
    L.append("2. Click drill-down link → its dedicated page")
    L.append("3. Raw JSON or code in [`data/`](data/) folder if needed")
    L.append("")
    L.append("### Recipe 3 — Audit security & risks")
    L.append("1. [🔐 Permissions](docs/07-permissions/README.md)")
    L.append("2. [⚠️ Risks — Critical & High](docs/09-risks/critical-and-high.md)")
    L.append("3. [🔗 Cross-WS deps](docs/06-cross-workspace/README.md)")
    L.append("")
    L.append("## 🏗️ Repo structure")
    L.append("")
    L.append("```")
    L.append("EnterpriseData-Dev-Docs/")
    L.append("├── README.md                           ← you are here")
    L.append("├── docs/")
    L.append("│   ├── 01-introduction.md")
    L.append("│   ├── 02-storage/")
    L.append("│   │   ├── README.md                  ← storage overview")
    L.append("│   │   ├── warehouses/")
    L.append("│   │   │   ├── README.md             ← 11 WH compared")
    L.append("│   │   │   ├── etl-framework.md      ← control plane deep dive")
    L.append("│   │   │   ├── source-data.md")
    L.append("│   │   │   ├── retail-warehouse.md")
    L.append("│   │   │   ├── wholesale-warehouse.md")
    L.append("│   │   │   ├── centralized-warehouse.md")
    L.append("│   │   │   ├── masterdata-warehouse.md")
    L.append("│   │   │   ├── distribution-warehouse.md")
    L.append("│   │   │   └── quality-warehouse.md")
    L.append("│   │   └── lakehouses/")
    L.append("│   │       ├── README.md")
    L.append("│   │       ├── centralized-lakehouse.md")
    L.append("│   │       ├── a-developement.md")
    L.append("│   │       └── radarsync-test.md")
    L.append("│   ├── 03-logic/")
    L.append("│   ├── 04-orchestration/")
    L.append("│   ├── 05-data-flow/")
    L.append("│   ├── 06-cross-workspace/")
    L.append("│   ├── 07-permissions/")
    L.append("│   ├── 08-operations/")
    L.append("│   ├── 09-risks/")
    L.append("│   └── 99-reference/")
    L.append("├── images/                             ← rendered Mermaid SVG/PNG")
    L.append("├── data/                               ← raw scan JSON (preserved)")
    L.append("├── scripts/                            ← scan + build scripts")
    L.append("└── _archive/                           ← old artifacts (preserved)")
    L.append("```")
    L.append("")
    L.append("## 🔧 Regenerate")
    L.append("")
    L.append("```bash")
    L.append("# Re-scan the workspace (~30 minutes)")
    L.append("python3 scripts/_scan_lakehouses.py")
    L.append("python3 scripts/_scan_procs_views.py")
    L.append("python3 scripts/_scan_shortcuts_files.py")
    L.append("python3 scripts/_scan_pipeline_runs.py")
    L.append("")
    L.append("# Re-build all docs")
    L.append("python3 scripts/_build_docs.py")
    L.append("```")
    L.append("")
    L.append("---")
    L.append("")
    L.append("_Scan date: 2026-05-08 · Doc generated: 2026-05-10_")
    write(REPO / "README.md", "\n".join(L))


# =============================================================
# 01 Introduction
# =============================================================

def build_introduction():
    L = []
    L.append("# 📘 01 — Introduction")
    L.append("")
    L.append("[← Back to root](../README.md)")
    L.append("")
    L.append("## What is `EnterpriseData-Dev`?")
    L.append("")
    L.append("A **Microsoft Fabric workspace** in Ashley Furniture's tenant that serves as the **DEV environment** of the company's enterprise data platform. It mirrors the structure of the legacy SQL Server EDW (`ASHLEY_EDW_DEV` + Synapse `Ashley_Edw`) onto Fabric Warehouses + Lakehouses, while keeping a parallel Databricks Unity Catalog (`edw_dev`) live-mirrored.")
    L.append("")
    L.append("## 🏢 Business context")
    L.append("")
    L.append("Ashley Furniture is in the **middle of a multi-year EDW → Fabric migration**. Evidence visible in this workspace:")
    L.append("")
    L.append("- **Mounted Azure Data Factory** `ashleyv2datafactory` (RG `IoT_Hub`) — the legacy ADF still alive and referenced.")
    L.append("- Pipeline `Fabric Migration ADF` ports table definitions from Synapse `Ashley_Edw.dw_developer.tabledictionary` into Fabric.")
    L.append("- Pipeline `EDW2FabricLoader` reads metadata config `ASHLEY_EDW_DEV.dw_developer.FabricMapping` (Flag=1) → row-by-row Copy into Fabric `Source_Data`.")
    L.append("- **Mirrored Databricks Catalog** `edw_dev` syncing in Full / autoSync mode (last sync 2026-05-08 05:57 Success).")
    L.append("- **`ETL_Framework` warehouse** with 35 stored procedures + 65-column `TableDictionary` = the workspace's metadata-driven orchestration brain.")
    L.append("")
    L.append("## 🏗️ High-level architecture")
    L.append("")
    L.append("![High-level architecture](../images/01-high-level-architecture.svg)")
    L.append("")
    L.append("> Open the SVG in a browser for full zoom. Source Mermaid below.")
    L.append("")
    L.append(mermaid("""flowchart LR
    classDef src fill:#e8f4fd,stroke:#3a8;
    classDef store fill:#fef9e7,stroke:#cb3;
    classDef logic fill:#f0e8fd,stroke:#94f;
    classDef orch fill:#e7fae8,stroke:#3a3;
    classDef ext fill:#fed,stroke:#c93;
    classDef prod fill:#fdd,stroke:#c33;

    EDW[(ASHLEY_EDW_DEV<br/>SQL Server)]:::src
    SYN[(Synapse Ashley_Edw)]:::src
    DBX[(Databricks UC<br/>edw_dev catalog)]:::src
    ADLS[ADLS Gen2<br/>ashleydevlake]:::ext
    SAAS[UKG / AFI / Maximo / SNow / GA]:::src
    PROD[(PROD WS ce4e6503<br/>14 WH + 1 LH)]:::prod

    ADF[Mounted ADF<br/>ashleyv2datafactory]:::orch
    PIPE[16 pipelines]:::orch
    MIRROR[edw_dev Mirror]:::orch

    SD[Source_Data WH<br/>64 schemas / 636 tables]:::store
    ETL[ETL_Framework<br/>35 procs + TableDictionary]:::store
    DOMAIN[Retail / Wholesale / MasterData /<br/>Distribution / Quality WHs]:::store
    CW[Centralized_Warehouse<br/>+ Centralized_Lakehouse]:::store

    EDW --> PIPE
    SYN --> PIPE
    SAAS --> ADF
    DBX --> MIRROR
    ADLS -.shortcuts.-> SD
    PROD -.18 OneLake shortcuts.-> CW

    ADF --> SD
    PIPE --> SD
    MIRROR -.OneLake surface.-> CW

    SD --> ETL
    ETL -- usp_RefreshCuratedTableFromView --> DOMAIN
    DOMAIN --> CW
    CW --> PBI[Power BI / Reporting]"""))
    L.append("")
    L.append("## 🧩 Key concepts")
    L.append("")
    L.append("Fabric introduces several object types you'll encounter throughout this doc:")
    L.append("")
    L.append(md_table(
        ["Object", "What it is"],
        [
            ["**Workspace**", "Logical container grouping items under one capacity"],
            ["**Warehouse**", "T-SQL relational engine on top of OneLake parquet (read/write)"],
            ["**Lakehouse**", "Delta Lake tables + Files folder on OneLake (with auto SQL endpoint)"],
            ["**Schema-enabled Lakehouse**", "Newer LH variant supporting `[schema].[table]` namespace (vs legacy `dbo` only)"],
            ["**OneLake**", "Unified ADLS Gen2 storage backing all Fabric items"],
            ["**Shortcut**", "Symbolic link — point a path in this LH/WH to data elsewhere (cross-WS or external)"],
            ["**Mirror (Databricks)**", "Live read-only mirror of a Databricks UC into Fabric OneLake"],
            ["**Mounted ADF**", "Reference link to existing Azure Data Factory — surfaces inside Fabric"],
            ["**Dataflow Gen2**", "Power Query M-based no-code data prep with auto-staging"],
            ["**Reflex (Activator)**", "Event-driven trigger watching data and firing actions"],
            ["**Spark Environment**", "Reusable compute config (runtime, pool, libraries) for notebooks"],
        ],
    ))
    L.append("")
    L.append("Full glossary including **Ashley Furniture domain terms** (UKG, AFI, Maximo, ADS, etc.) → [99 Reference / Glossary](99-reference/glossary.md)")
    L.append("")
    L.append("## 🔥 5 things you must know before contributing")
    L.append("")
    L.append("1. **🚨 The data isn't really here.** Centralized_Lakehouse 5.92 B rows are 18 OneLake shortcuts to PROD workspace `EnterpriseData` (`ce4e6503-...`). Don't write back unless you mean to affect PROD-shaped paths.")
    L.append("2. **🛌 Most things are dormant.** Only **3 of 41** orchestration items have any recent run history. The workspace is mostly a **definition store**.")
    L.append("3. **⚠️ ETL_Framework is the brain.** Any change to `TableDictionary` or its 35 procs ripples through all domain warehouses.")
    L.append("4. **🔴 Critical security risk:** `MetaData-Pull` notebook cell 1 has a plaintext SP secret. Rotate immediately.")
    L.append("5. **🔁 Naming is treacherous.** Pipelines named `test`, `pipeline1` are real cross-WS PROD copies into `Commissions_Prototype`. Rename before touching.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("**Next:** [📦 02 — Storage Layer](02-storage/README.md)")
    write(DOCS / "01-introduction.md", "\n".join(L))


# =============================================================
# 02 Storage Layer
# =============================================================

WH_DEFS = {
    "ETL_Framework": {
        "tier": "PROD-CTRL", "id": "02c8970b-7af3-4d4e-b011-cc3cdc3825ef",
        "purpose": "**Control plane warehouse** — chứa `TableDictionary` (65-cột master catalog) + 35 stored procs điều phối parquet→Delta loading + audit + SLA logging cho toàn bộ workspace.",
        "schemas_count": 13, "tables_count": 31, "views_count": 14, "procs_count": 35,
        "highlight": "Hub of the whole workspace. Every loader proc lives here. AuditLog + EmailQueue tables are here.",
    },
    "Source_Data": {
        "tier": "PROD-SRC", "id": "f14e2ea6-ae2c-4b90-8e08-522e84f1aefc",
        "purpose": "**Bronze landing layer** — 64 schemas (1 schema per source feed). Loaded by EDW2FabricLoader pipeline + ADF mount + migration pipelines. Largest WH by table count.",
        "schemas_count": 64, "tables_count": 636, "views_count": 12, "procs_count": 2,
        "highlight": "Receives every raw feed. Schemas mirror source-system names: Retail_Corporate, MasterData_HR_UKG_*, Manufacturing_Maximo, etc.",
    },
    "Centralized_Warehouse": {
        "tier": "PROD", "id": "c5a1f95b-f9db-4cb7-8ded-396ea70da572",
        "purpose": "**Gold tier warehouse** — 38 tables / **0 procs nội bộ**. Loaded externally bởi `MetaData-Pull` notebook (cross-WH JDBC sync) chứ không có proc bên trong.",
        "schemas_count": 23, "tables_count": 38, "views_count": 12, "procs_count": 0,
        "highlight": "MetaData schema chứa control tables (CopyTables, ShortcutCatalog, SysObjectInfo) drive cho notebooks & system pipelines.",
    },
    "Retail_Warehouse": {
        "tier": "PROD", "id": "09504907-575d-446a-991a-87fa525166d7",
        "purpose": "**Silver tier domain warehouse cho retail** — 198 tables, 41 views, 146 stored procs. Largest proc set trong workspace.",
        "schemas_count": 25, "tables_count": 198, "views_count": 41, "procs_count": 146,
        "highlight": "Heaviest proc family: 49 Refresh-Load + 38 MERGE + 19 Validate + 13 Audit-DQ. Pattern: usp_RefreshCuratedTableFromView consume _Wrk views.",
    },
    "Wholesale_Warehouse": {
        "tier": "PROD", "id": "c1ef4a62-f8e2-4d55-96bd-33eb07b81b7c",
        "purpose": "**Silver tier domain warehouse cho wholesale** — 209 tables, 126 _Wrk views, 8 procs (avg 20K chars/proc, MERGE-heavy).",
        "schemas_count": 28, "tables_count": 209, "views_count": 126, "procs_count": 8,
        "highlight": "Most _Wrk views: Marketing_Wrk (35), CustomerOrders_AFI_Wrk (24), Pricing_AFI_Wrk (20), SalesHistory_AFI_Wrk (12), PartyContacts_Wrk (9).",
    },
    "MasterData_Warehouse": {
        "tier": "PROD", "id": "db565620-28ac-4510-a61e-1023743efdc6",
        "purpose": "**Silver tier master data warehouse** — 46 tables / 0 procs nội bộ. Loaded by ETL_Framework procs (cross-WH).",
        "schemas_count": 14, "tables_count": 46, "views_count": 12, "procs_count": 0,
        "highlight": "Master data domain — items, customers, vendors, products. Logic centralized in ETL_Framework.",
    },
    "Distribution_Warehouse": {
        "tier": "PROD", "id": "7d51a21f-c1fe-4968-930d-1702c0ee39dc",
        "purpose": "**Silver tier distribution domain — chỉ 7 tables**, có thể là shadow domain chưa build đầy đủ. [Likely].",
        "schemas_count": 8, "tables_count": 7, "views_count": 12, "procs_count": 0,
        "highlight": "Only 7 tables — incomplete or future domain.",
    },
    "Quality_Warehouse": {
        "tier": "PROD-EMPTY", "id": "6a6129c1-5342-4ea2-bcb8-9b8a1af8db20",
        "purpose": "**EMPTY** — Tier=PROD nhưng 0 tables / 0 procs. Có thể là DQ domain chưa build hoặc đã bị bỏ. [Speculation on intent]",
        "schemas_count": 6, "tables_count": 0, "views_count": 12, "procs_count": 0,
        "highlight": "🔴 PROD tier empty shell — needs decision: build or remove.",
    },
    "StagingWarehouseForDataflows_20251008191817": {
        "tier": "AUTO", "id": "0f273877-...",
        "purpose": "Auto-provisioned Dataflow Gen2 staging WH. Empty.",
        "schemas_count": 6, "tables_count": 0, "views_count": 12, "procs_count": 0,
        "highlight": "Companion auto-staging cho Dataflow Test. Safe to delete if Dataflow Test stays empty.",
    },
    "DataflowsStagingWarehouse": {
        "tier": "AUTO", "id": "4cf62bd7-...",
        "purpose": "Auto-provisioned Dataflow Gen2 staging WH. Empty.",
        "schemas_count": 6, "tables_count": 0, "views_count": 12, "procs_count": 0,
        "highlight": "Same as the timestamped twin.",
    },
    "Test_Owneraccess": {
        "tier": "TEST", "id": "2d1d459e-...",
        "purpose": "Leftover từ permissions-testing exercise — empty TEST WH.",
        "schemas_count": 6, "tables_count": 0, "views_count": 12, "procs_count": 0,
        "highlight": "Safe to delete.",
    },
}

LH_DEFS = {
    "Centralized_Lakehouse": {
        "tier": "PROD", "id": "50e11300-9fb4-4e82-876c-7183bb2501ba",
        "purpose": "**Shortcut-aggregation layer** — 501 tables / 5.92 B rows nhưng 18 shortcuts trỏ thẳng vào PROD WS Source_Data + Retail_Warehouse. Data thật KHÔNG ở DEV.",
        "tables_count": 501, "rows": 5923323398, "schemas_enabled": True,
        "highlight": "21 schemas. Twin schemas Retail_Corporate ↔ Retail_Corporate_Prod = 2 shortcuts cùng PROD path.",
    },
    "A_Developement": {
        "tier": "DEV-SANDBOX", "id": "1545d3ce-0fae-40b5-b314-ac2fd43e25c5",
        "purpose": "**Personal dev sandbox** — 3 local tables (afi_finance, drive4ashley, testing1) + 7 ADLS shortcuts trỏ external storage `ashleydevlake`.",
        "tables_count": 3, "rows": 100514, "schemas_enabled": False,
        "highlight": "Schemas-disabled (legacy). Smallest active LH.",
    },
    "RadarSync_Test": {
        "tier": "TEST", "id": "ddadbe2e-c2e2-4949-8e84-81eed6a81c9e",
        "purpose": "**Sandbox lakehouse** — 2 local tables (joblabor 4900 rows, test_pipeline 4 rows) + ⚠️ mounts ENTIRE trusted-zone + raw-zone ADLS containers.",
        "tables_count": 2, "rows": 4904, "schemas_enabled": True,
        "highlight": "🔴 Broad ADLS scope — anyone with this LH access reads entire dev data lake.",
    },
    "DataflowsStagingLakehouse": {
        "tier": "AUTO", "id": "68d19239-...",
        "purpose": "Auto-staging companion cho Dataflow Test. Empty.",
        "tables_count": 0, "rows": 0, "schemas_enabled": False,
        "highlight": "Safe to delete.",
    },
    "StagingLakehouseForDataflows_20251008191803": {
        "tier": "AUTO", "id": "c2583202-...",
        "purpose": "Auto-staging companion cho Dataflow Test (timestamped twin). Empty.",
        "tables_count": 0, "rows": 0, "schemas_enabled": False,
        "highlight": "Safe to delete.",
    },
}


def build_storage_readme():
    L = []
    L.append("# 📦 02 — Storage Layer")
    L.append("")
    L.append("[← Back to root](../../README.md)")
    L.append("")
    L.append("## What lives here")
    L.append("")
    L.append("Storage = where data physically resides (or *appears* to reside via shortcuts). Three storage primitives in this workspace:")
    L.append("")
    L.append(md_table(
        ["Type", "Count", "Total tables", "Total rows", "Detail"],
        [
            ["🏬 **Warehouse**", "11", "1,165", "—", "[See Warehouses →](warehouses/README.md)"],
            ["💧 **Lakehouse**", "5", "506", "5,923,323,398", "[See Lakehouses →](lakehouses/README.md)"],
            ["🗄️ **SQLDatabase**", "1", "—", "—", "Commissions_Prototype (sink)"],
        ],
    ))
    L.append("")
    L.append("> Most of those 5.92 B rows are **OneLake shortcuts to the PROD workspace**, not stored locally. See [05 Data Flow](../05-data-flow/README.md) and [06 Cross-Workspace](../06-cross-workspace/README.md).")
    L.append("")
    L.append("## 🗺️ Storage map")
    L.append("")
    L.append("![Storage map](../../images/02-storage-map.svg)")
    L.append("")
    L.append(mermaid("""graph TB
    classDef ctrl fill:#fef3c7,stroke:#d97706,color:#92400e;
    classDef src fill:#dbeafe,stroke:#2563eb,color:#1e3a8a;
    classDef silver fill:#e0e7ff,stroke:#4f46e5,color:#312e81;
    classDef gold fill:#fce7f3,stroke:#db2777,color:#831843;
    classDef empty fill:#fee2e2,stroke:#dc2626,color:#7f1d1d;
    classDef auto fill:#f3f4f6,stroke:#6b7280,color:#374151;
    classDef lh fill:#cffafe,stroke:#0891b2,color:#164e63;

    subgraph CTRL[Control Plane]
        ETL[ETL_Framework<br/>35 procs · 14 views<br/>TableDictionary]:::ctrl
    end

    subgraph BRONZE[Bronze - Source landing]
        SD[Source_Data<br/>64 schemas / 636 tables]:::src
    end

    subgraph SILVER[Silver - Domain warehouses]
        RW[Retail_Warehouse<br/>198 tables · 146 procs]:::silver
        WW[Wholesale_Warehouse<br/>209 tables · 114 _Wrk views]:::silver
        MD[MasterData_Warehouse<br/>46 tables]:::silver
        DW[Distribution_Warehouse<br/>7 tables]:::silver
        QW[🔴 Quality_Warehouse<br/>EMPTY]:::empty
    end

    subgraph GOLD[Gold - Aggregation]
        CW[Centralized_Warehouse<br/>38 tables · 0 procs]:::gold
        CL[(Centralized_Lakehouse<br/>501 tables · 5.92B rows<br/>shortcut-backed)]:::lh
    end

    subgraph LHS[Other Lakehouses]
        AD[A_Developement<br/>3 tables sandbox]:::lh
        RST[RadarSync_Test<br/>2 tables · ADLS mounts]:::lh
    end

    subgraph AUTO_STG[Auto-staging - Dataflow Gen2]
        AUTO1[2 staging WH + 2 staging LH<br/>EMPTY]:::auto
    end

    SD --> RW
    SD --> WW
    SD --> MD
    SD --> DW
    RW --> CW
    WW --> CW
    MD --> CW
    DW --> CW
    ETL -. drives .-> SD
    ETL -. drives .-> RW
    ETL -. drives .-> WW
    ETL -. drives .-> MD"""))
    L.append("")
    L.append("## 📑 Sub-pages")
    L.append("")
    L.append("- [🏬 **Warehouses (11)** ](warehouses/README.md) — relational T-SQL containers")
    L.append("- [💧 **Lakehouses (5)**](lakehouses/README.md) — Delta Lake on OneLake")
    L.append("")
    L.append("## ⚠️ Storage-related risks")
    L.append("")
    L.append("- **C3 (High)**: `Quality_Warehouse` (PROD tier) is empty — needs build or remove decision")
    L.append("- **C25 (High)**: 5.92 B rows in `Centralized_Lakehouse` are shortcut-backed, not real DEV data")
    L.append("- **C28 (High)**: `RadarSync_Test` mounts entire trusted+raw ADLS zones — broad scope")
    L.append("- **C20 (Low)**: Twin schemas `Retail_Corporate` ↔ `Retail_Corporate_Prod` confusion")
    L.append("")
    L.append("Full risk list → [09 Risks](../09-risks/README.md)")
    L.append("")
    L.append("---")
    L.append("")
    L.append("**Next:** [🏬 Warehouses →](warehouses/README.md) or [💧 Lakehouses →](lakehouses/README.md)")
    write(DOCS / "02-storage" / "README.md", "\n".join(L))


def build_warehouses_readme():
    L = []
    L.append("# 🏬 Warehouses (11)")
    L.append("")
    L.append("[← Storage](../README.md) · [← Root](../../../README.md)")
    L.append("")
    L.append("## Comparison table")
    L.append("")
    L.append(md_table(
        ["Warehouse", "Tier", "Schemas", "Tables", "Views", "Procs", "Detail"],
        [[
            f"[`{name}`]({name.lower().replace('_','-')}.md)" if name in ("ETL_Framework","Source_Data","Centralized_Warehouse","Retail_Warehouse","Wholesale_Warehouse","MasterData_Warehouse","Distribution_Warehouse","Quality_Warehouse") else f"`{name}`",
            d["tier"],
            d["schemas_count"], d["tables_count"], d["views_count"], d["procs_count"],
            f"[→]({name.lower().replace('_','-')}.md)" if name in ("ETL_Framework","Source_Data","Centralized_Warehouse","Retail_Warehouse","Wholesale_Warehouse","MasterData_Warehouse","Distribution_Warehouse","Quality_Warehouse") else "(auto/test)",
        ] for name, d in WH_DEFS.items()],
    ))
    L.append("")
    L.append("**Total:** 199 schemas · 1,165 tables · 277 views · 191 procedures")
    L.append("")
    L.append("## 🎯 Warehouse roles in the architecture")
    L.append("")
    L.append(mermaid("""flowchart LR
    classDef ctrl fill:#fef3c7,stroke:#d97706,color:#92400e;
    classDef src fill:#dbeafe,stroke:#2563eb,color:#1e3a8a;
    classDef silver fill:#e0e7ff,stroke:#4f46e5,color:#312e81;
    classDef gold fill:#fce7f3,stroke:#db2777,color:#831843;
    classDef empty fill:#fee2e2,stroke:#dc2626,color:#7f1d1d;

    ETL[ETL_Framework<br/>CONTROL PLANE<br/>35 procs · TableDictionary]:::ctrl
    SD[Source_Data<br/>BRONZE<br/>636 tables / 64 schemas]:::src
    RW[Retail_Warehouse<br/>SILVER · 198 tables<br/>146 procs]:::silver
    WW[Wholesale_Warehouse<br/>SILVER · 209 tables<br/>114 _Wrk views]:::silver
    MD[MasterData_Warehouse<br/>SILVER · 46 tables]:::silver
    DW[Distribution_Warehouse<br/>SILVER · 7 tables]:::silver
    QW[Quality_Warehouse<br/>EMPTY 🔴]:::empty
    CW[Centralized_Warehouse<br/>GOLD · 38 tables · 0 procs]:::gold

    SD --> RW
    SD --> WW
    SD --> MD
    SD --> DW
    RW --> CW
    WW --> CW
    MD --> CW
    DW --> CW
    ETL -. drives .-> SD
    ETL -. drives .-> RW
    ETL -. drives .-> WW
    ETL -. drives .-> MD
    ETL -. drives .-> DW"""))
    L.append("")
    L.append("## 📚 Per-warehouse detail")
    L.append("")
    for name in ("ETL_Framework","Source_Data","Centralized_Warehouse","Retail_Warehouse","Wholesale_Warehouse","MasterData_Warehouse","Distribution_Warehouse","Quality_Warehouse"):
        d = WH_DEFS[name]
        slug = name.lower().replace("_", "-")
        L.append(f"### [{name}]({slug}.md) · _{d['tier']}_")
        L.append("")
        L.append(d["purpose"])
        L.append("")
        L.append(f"_{d['highlight']}_")
        L.append("")
    L.append("")
    L.append("**Test/staging WHs (no detail page):**")
    for name in ("StagingWarehouseForDataflows_20251008191817","DataflowsStagingWarehouse","Test_Owneraccess"):
        d = WH_DEFS[name]
        L.append(f"- `{name}` — _{d['tier']}_. {d['purpose']}")
    L.append("")
    L.append("---")
    L.append("")
    L.append("**Next:** any warehouse above, or [💧 Lakehouses →](../lakehouses/README.md)")
    write(DOCS / "02-storage" / "warehouses" / "README.md", "\n".join(L))


def build_warehouse_page(name, slug, extra_sections=None):
    """Generate a per-warehouse detailed page."""
    d = WH_DEFS[name]
    L = []
    L.append(f"# 🏬 {name}")
    L.append("")
    L.append(f"_{d['tier']} tier · ID `{d['id']}`_")
    L.append("")
    L.append("[← Warehouses](README.md) · [← Storage](../README.md) · [← Root](../../../README.md)")
    L.append("")
    L.append("## 🎯 Purpose")
    L.append("")
    L.append(d["purpose"])
    L.append("")
    L.append("## 📊 Stats")
    L.append("")
    L.append(md_table(
        ["Metric", "Value"],
        [
            ["Tier", d["tier"]],
            ["Schemas", d["schemas_count"]],
            ["Tables", d["tables_count"]],
            ["Views", d["views_count"]],
            ["Stored Procedures", d["procs_count"]],
            ["Workspace ID", f"`{WS_ID}`"],
            ["Item ID", f"`{d['id']}`"],
        ],
    ))
    L.append("")
    L.append(f"**Highlight:** {d['highlight']}")
    L.append("")
    # Schemas list
    wh_data = wh.get(name, {})
    schemas = wh_data.get("schemas", [])
    if schemas:
        L.append("## 🗂️ Schemas")
        L.append("")
        L.append(", ".join(f"`{s}`" for s in sorted(schemas)))
        L.append("")
    # Top tables
    tables = wh_data.get("tables", [])
    if tables:
        L.append(f"## 📋 Tables ({len(tables)})")
        L.append("")
        # Top 30 by row count
        sorted_tbl = sorted(tables, key=lambda t: -(t.get("row_count") or 0))
        top = sorted_tbl[:30]
        rows = []
        for t in top:
            rows.append([
                f"`{t.get('schema_name')}`",
                f"`{t.get('table_name')}`",
                fmt_int(t.get("row_count", 0) or 0),
                t.get("modify_date", "")[:10] if t.get("modify_date") else "",
            ])
        L.append("**Top 30 tables (sample):**")
        L.append("")
        L.append(md_table(["Schema", "Table", "Rows", "Modified"], rows))
        if len(tables) > 30:
            L.append(f"\n_… and {len(tables) - 30} more. Full list in [`data/03-warehouses-raw.json`](../../../data/03-warehouses-raw.json)._")
        L.append("")
    # Views user only
    user_views = [v for v in views.get(name, [])
                  if isinstance(v.get("definition"), str)
                  and v.get("schema") not in {"sys", "queryinsights", "INFORMATION_SCHEMA"}]
    if user_views:
        L.append(f"## 👁️ User views ({len(user_views)})")
        L.append("")
        by_sch = defaultdict(list)
        for v in user_views:
            by_sch[v["schema"]].append(v["name"])
        L.append(md_table(["Schema", "Views", "Names (sample)"], [
            [f"`{s}`", len(vs), ", ".join(f"`{n}`" for n in sorted(vs)[:5]) + (f", … +{len(vs)-5}" if len(vs) > 5 else "")]
            for s, vs in sorted(by_sch.items())
        ]))
        L.append("")
        L.append("Full view bodies → [`data/07-views-raw.json`](../../../data/07-views-raw.json)")
        L.append("")
    # Procs by family
    real_procs = [p for p in procs.get(name, []) if isinstance(p.get("definition"), str)]
    if real_procs:
        L.append(f"## ⚙️ Stored procedures ({len(real_procs)})")
        L.append("")

        def fam(name):
            n = name.lower()
            if "createtablefromparquet" in n or "tablefromparquet" in n: return "Parquet loaders"
            if "incremental" in n: return "Incremental"
            if "scd2" in n or "snapshot" in n: return "SCD2/Snapshot"
            if "refresh" in n or "update" in n: return "Curated refresh"
            if "audit" in n: return "Audit/DQ"
            if "alert" in n or "sla" in n or "email" in n: return "Alert/SLA"
            if "dictionary" in n: return "Dictionary upkeep"
            if "merge" in n: return "MERGE"
            if "validate" in n or "check" in n: return "Validate"
            if "history" in n or "log" in n: return "History/Log"
            if "drop" in n or "truncate" in n: return "Drop/Cleanup"
            return "Other"
        by_fam = defaultdict(list)
        for p in real_procs:
            by_fam[fam(p["name"])].append(p)
        L.append(md_table(["Family", "Procs", "Examples"], [
            [f, len(plist), ", ".join(f"`{p['name'][:40]}`" for p in plist[:3]) + (f", …+{len(plist)-3}" if len(plist) > 3 else "")]
            for f, plist in sorted(by_fam.items(), key=lambda x: -len(x[1]))
        ]))
        L.append("")
        L.append("Full proc bodies → [`data/06-procs-raw.json`](../../../data/06-procs-raw.json)")
        L.append("")
    # Extra sections
    if extra_sections:
        L.append(extra_sections)
    L.append("---")
    L.append("")
    L.append(f"**Related:** [03 Logic — Stored Procedures](../../03-logic/stored-procs.md) · [04 Orchestration — Pipelines](../../04-orchestration/pipelines.md)")
    write(DOCS / "02-storage" / "warehouses" / f"{slug}.md", "\n".join(L))


# ETL_Framework gets richer detail
def etl_framework_extra():
    L = []
    L.append("## 🧠 The brain — `TableDictionary` (65 columns)")
    L.append("")
    L.append("This single table is the **metadata-driven orchestration heart** of the workspace. One row per managed object.")
    L.append("")
    L.append("**Key columns observed in sample data:**")
    L.append("")
    L.append("- `ServerName` / `DatabaseName` / `SchemaName` / `TableName` — the target (Fabric or EDW)")
    L.append("- `ObjectType` — TABLE / VIEW / etc.")
    L.append("- `PrimaryKey` / `AlternateKey`")
    L.append("- `StorageType` — `Delta` / `HEAP` / etc.")
    L.append("- `DistributionKey` / `IndexType` — `CLUSTERED` etc.")
    L.append("- `SourceSystem` / `SourceServer` / `SourceDatabase` / `SourceObject` — where the data comes from")
    L.append("- `ETLTool` — `Databricks` / `ADF` / etc.")
    L.append("- `PackageName` / `RefreshRate` / `UpdateMethod`")
    L.append("- `ExtractQuery` / `UpdateQuery` — the actual SQL/proc invocation")
    L.append("")
    L.append("**Example sample row:**")
    L.append("```")
    L.append("EDW-Fabric / Source_Data / MasterData_HR_UKG_DSG_Wrk / TAPayCodeMap")
    L.append("StorageType=Delta, IndexType=CLUSTERED, ETLTool=Databricks,")
    L.append("UpdateQuery=[DW_Developer].[Usp_CreateTableFromParquet]")
    L.append("```")
    L.append("")
    L.append("→ confirms the metadata-driven, parquet-based ingestion via Databricks → Fabric Delta tables.")
    L.append("")
    L.append("## 🔄 Procedure family tree")
    L.append("")
    L.append(mermaid("""graph TB
    TD[TableDictionary] --> P_LOAD[📥 Parquet Loaders<br/>13 variants]
    TD --> P_INC[♻️ Incremental + CDC<br/>3 procs]
    TD --> P_SCD[🕰️ SCD2 + Snapshot<br/>3 procs]
    TD --> P_REF[🔄 Curated Refresh<br/>3 procs]
    TD --> P_AUD[🔍 Audit + DQ<br/>5 procs]
    TD --> P_DICT[📚 Dictionary upkeep<br/>3 procs]
    TD --> P_UTL[🔧 Utilities<br/>5 procs]

    P_LOAD --> SOURCE[Source_Data<br/>Bronze]
    P_INC --> SOURCE
    P_SCD --> SOURCE
    SOURCE --> P_REF
    P_REF --> DOMAIN[Retail / Wholesale /<br/>MasterData / Distribution]
    P_AUD --> EQ[EmailQueue]
    P_DICT --> TD"""))
    L.append("")
    L.append("## 📋 Other key tables")
    L.append("")
    L.append(md_table(
        ["Table", "Purpose"],
        [
            ["`DW_Developer.AuditLog`", "Runtime audit log (Description, DateTime, User, Command). Real errors visible: `usp_RefreshCuratedTableFromView: Retail_Warehouse.MasterData_Retail.SalesPerson` with `String or binary data would be truncated.`"],
            ["`DW_Developer.EnvironmentControl`", "Env routing — sample: `GBL / AzureDataFabric / DEV / Source_Data` confirms this is the DEV env"],
            ["`DW_Developer.FabricLoad`", "Fabric-specific load metadata"],
            ["`DW_Developer.Source_EDW_AggCheck`", "Aggregate reconciliation EDW vs Fabric"],
            ["`DW_Developer.Source_EDW_CountCheck`", "Row-count reconciliation"],
            ["`Performance_Logs.tblFabricDataFeedAlertLog`", "Data-feed alert log (+ _Detail sibling)"],
            ["`Performance_Logs.tblFabricSLAAlertLog`", "SLA alert log (+ _Detail sibling)"],
            ["`Performance_Logs.EmailQueue`", "Outbound email queue"],
            ["`Performance_Logs.DimEmailQueue`", "Dimension table for email queue"],
        ],
    ))
    L.append("")
    L.append("## ⚠️ Risks specific to ETL_Framework")
    L.append("")
    L.append("- **C9 (Low)**: Stranded business tables in ETL_Framework (`Manufacturing_Maximo.Fedex`, `MasterData_ItemMaster_AFI.ITEMASA`, `Retail_DW.AshleyServiceNow*`, `BtaData`, `FlatBOM`, `kit`, `StoreMasterCustom`) — should live in domain WHs")
    L.append("- **C10 (Low)**: 4 clones of `TableDictionary` (`_clone`, `_edw_1`, `_Test`, `_Security`) + 2 `_UpdateLog*` siblings → drift / authority ambiguity")
    L.append("- **C19 (Low)**: 13 parquet-loader proc variants — needs consolidation")
    L.append("")
    return "\n".join(L)


# =============================================================
# 02 Storage — Lakehouses
# =============================================================

def build_lakehouses_readme():
    L = []
    L.append("# 💧 Lakehouses (5)")
    L.append("")
    L.append("[← Storage](../README.md) · [← Root](../../../README.md)")
    L.append("")
    L.append("## Comparison table")
    L.append("")
    L.append(md_table(
        ["Lakehouse", "Tier", "Tables", "Rows", "Schemas-enabled?", "Detail"],
        [[
            f"[`{name}`]({name.lower().replace('_','-').replace(' ','-')}.md)" if name in ("Centralized_Lakehouse","A_Developement","RadarSync_Test") else f"`{name}`",
            d["tier"],
            d["tables_count"],
            fmt_int(d["rows"]),
            "✅" if d["schemas_enabled"] else "—",
            f"[→]({name.lower().replace('_','-').replace(' ','-')}.md)" if name in ("Centralized_Lakehouse","A_Developement","RadarSync_Test") else "(empty staging)",
        ] for name, d in LH_DEFS.items()],
    ))
    L.append("")
    L.append("**Total:** 506 tables · 5,923,323,398 rows")
    L.append("")
    L.append("## 🌐 Lakehouse purposes at a glance")
    L.append("")
    L.append(mermaid("""flowchart LR
    classDef shortcut fill:#fef3c7,stroke:#d97706,color:#92400e;
    classDef sandbox fill:#cffafe,stroke:#0891b2,color:#164e63;
    classDef test fill:#fee2e2,stroke:#dc2626,color:#7f1d1d;
    classDef empty fill:#f3f4f6,stroke:#6b7280,color:#374151;

    CL[Centralized_Lakehouse<br/>501 tables · 5.92B rows<br/>SHORTCUT-BACKED]:::shortcut
    AD[A_Developement<br/>3 tables · 100K rows<br/>+ 7 ADLS shortcuts]:::sandbox
    RST[RadarSync_Test<br/>2 tables · 4.9K rows<br/>+ entire ADLS zones]:::test
    DSL[DataflowsStagingLakehouse<br/>EMPTY]:::empty
    SLF[StagingLakehouseForDataflows_20251008<br/>EMPTY]:::empty"""))
    L.append("")
    for name in ("Centralized_Lakehouse", "A_Developement", "RadarSync_Test"):
        d = LH_DEFS[name]
        slug = name.lower().replace("_", "-").replace(" ", "-")
        L.append(f"### [{name}]({slug}.md) · _{d['tier']}_")
        L.append("")
        L.append(d["purpose"])
        L.append("")
        L.append(f"_{d['highlight']}_")
        L.append("")
    L.append("---")
    L.append("")
    L.append("**Next:** any lakehouse above")
    write(DOCS / "02-storage" / "lakehouses" / "README.md", "\n".join(L))


def build_lakehouse_page(name, slug, extra_sections=None):
    d = LH_DEFS[name]
    L = []
    L.append(f"# 💧 {name}")
    L.append(f"_{d['tier']} tier · ID `{d['id']}`_")
    L.append("")
    L.append("[← Lakehouses](README.md) · [← Storage](../README.md) · [← Root](../../../README.md)")
    L.append("")
    L.append("## 🎯 Purpose")
    L.append("")
    L.append(d["purpose"])
    L.append("")
    L.append("## 📊 Stats")
    L.append("")
    L.append(md_table(
        ["Metric", "Value"],
        [
            ["Tier", d["tier"]],
            ["Tables", d["tables_count"]],
            ["Rows (live count)", fmt_int(d["rows"])],
            ["Schemas-enabled", "Yes" if d["schemas_enabled"] else "No (legacy `dbo` only)"],
            ["Item ID", f"`{d['id']}`"],
        ],
    ))
    L.append("")
    L.append(f"**Highlight:** {d['highlight']}")
    L.append("")
    # Tables
    lh_data = lh.get(name, {})
    tables = lh_data.get("tables", [])
    if tables:
        L.append(f"## 📋 Tables ({len(tables)})")
        L.append("")
        rc_map = lh_data.get("row_counts", {})

        def rc(t):
            v = rc_map.get(f"{t['schema']}.{t['name']}", 0)
            return v if isinstance(v, int) else 0

        sorted_tbl = sorted(tables, key=lambda t: -rc(t))
        rows = []
        for t in sorted_tbl[:30]:
            rows.append([
                f"`{t.get('schema')}`",
                f"`{t.get('name')}`",
                fmt_int(rc(t)),
            ])
        L.append("**Top 30 tables by row count:**")
        L.append("")
        L.append(md_table(["Schema", "Table", "Rows"], rows))
        if len(tables) > 30:
            L.append(f"\n_… and {len(tables) - 30} more._")
        L.append("")
    # Shortcuts
    shortcuts = sc_data.get("shortcuts", {}).get(name, [])
    if isinstance(shortcuts, list) and shortcuts:
        # filter to non-internal shortcuts (cross-WS or external)
        ext = [s for s in shortcuts if isinstance(s.get("target"), dict) and (
            (s["target"].get("type") == "OneLake" and s["target"].get("oneLake", {}).get("workspaceId") != WS_ID)
            or s["target"].get("type") != "OneLake"
        )]
        if ext:
            L.append(f"## 🔗 External shortcuts ({len(ext)})")
            L.append("")
            rows = []
            for s in ext:
                t = s.get("target", {})
                if t.get("type") == "OneLake":
                    ol = t.get("oneLake", {})
                    rows.append([
                        f"`{s.get('name','')}`",
                        "OneLake",
                        f"WS `{ol.get('workspaceId','')[:8]}…`",
                        f"`{ol.get('path','')}`",
                    ])
                elif t.get("type") == "AdlsGen2":
                    a = t.get("adlsGen2", {})
                    rows.append([
                        f"`{s.get('name','')}`",
                        "ADLS Gen2",
                        f"`{a.get('location','')}`",
                        f"`{a.get('subpath','')}`",
                    ])
            L.append(md_table(["Name", "Type", "Target host/WS", "Path"], rows))
            L.append("")
    if extra_sections:
        L.append(extra_sections)
    L.append("---")
    L.append("")
    L.append("**Related:** [06 Cross-Workspace](../../06-cross-workspace/README.md)")
    write(DOCS / "02-storage" / "lakehouses" / f"{slug}.md", "\n".join(L))


# =============================================================
# 03 Logic Layer
# =============================================================

def build_logic_readme():
    L = []
    L.append("# 🧠 03 — Logic Layer")
    L.append("")
    L.append("[← Root](../../README.md)")
    L.append("")
    L.append("## What lives here")
    L.append("")
    L.append("Code & transformations that compute over the [Storage Layer](../02-storage/README.md).")
    L.append("")
    L.append(md_table(
        ["Type", "Count", "Total size", "Detail"],
        [
            ["⚙️ **Stored Procedures**", "192", "1.39 MB code", "[See procs →](stored-procs.md)"],
            ["👁️ **User Views**", "145", "—", "[See views →](views.md)"],
            ["📓 **Notebooks**", "18", "—", "[See notebooks →](notebooks.md)"],
        ],
    ))
    L.append("")
    L.append("## 🌳 Logic distribution by warehouse")
    L.append("")
    L.append(mermaid("""graph TB
    classDef heavy fill:#fde68a,stroke:#d97706;
    classDef medium fill:#dbeafe,stroke:#2563eb;
    classDef light fill:#e5e7eb,stroke:#6b7280;

    RW[Retail_Warehouse<br/>146 procs · 29 views<br/>957 KB]:::heavy
    ETL[ETL_Framework<br/>35 procs · 2 views<br/>261 KB]:::heavy
    WW[Wholesale_Warehouse<br/>8 procs · 114 views<br/>162 KB]:::medium
    SD[Source_Data<br/>2 procs<br/>9 KB]:::light
    AD[A_Developement LH<br/>1 proc<br/>2 KB]:::light"""))
    L.append("")
    L.append("## 📑 Sub-pages")
    L.append("")
    L.append("- [⚙️ Stored Procedures](stored-procs.md) — 192 procs grouped by family")
    L.append("- [👁️ Views](views.md) — 145 user views (mostly `_Wrk` working sets)")
    L.append("- [📓 Notebooks](notebooks.md) — 18 notebooks grouped: 6 active prod, 3 Vers5 dup, 6 ad-hoc, 3 empty")
    L.append("")
    L.append("---")
    write(DOCS / "03-logic" / "README.md", "\n".join(L))


def build_logic_procs():
    L = []
    L.append("# ⚙️ Stored Procedures (192)")
    L.append("")
    L.append("[← Logic](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## Distribution")
    L.append("")
    rows = []
    for c, lst in procs.items():
        valid = [p for p in lst if isinstance(p.get("definition"), str)]
        if valid:
            total = sum(len(p["definition"]) for p in valid)
            rows.append([f"`{c}`", len(valid), f"{total:,}", f"{int(total/len(valid)):,}"])
    rows.sort(key=lambda r: -r[1])
    L.append(md_table(["Container", "Procs", "Total chars", "Avg/proc"], rows))
    L.append("")
    L.append("## ETL_Framework families (35 procs)")
    L.append("")
    L.append(mermaid("""graph LR
    classDef family fill:#dfe;stroke:#393;

    P_LOAD[📥 Parquet loaders<br/>13 variants<br/>Usp_CreateTableFromParquet*<br/>Usp_TableFromParquet_*]:::family
    P_INC[♻️ Incremental + CDC<br/>3 procs<br/>usp_IncrementalTableLoad*]:::family
    P_SCD[🕰️ SCD2 + Snapshot<br/>3 procs<br/>usp_SCD2_TableLoad<br/>Usp_SnapshotLoad<br/>Usp_WriteTableToParquet]:::family
    P_REF[🔄 Curated refresh<br/>3 procs<br/>usp_RefreshCuratedTableFromView<br/>+ _2 + _DateRange]:::family
    P_AUD[🔍 Audit + DQ + Alert<br/>5 procs<br/>usp_Audit_*<br/>usp_DataWarehouseAlert_*]:::family
    P_DICT[📚 Dictionary upkeep<br/>3 procs]:::family
    P_UTL[🔧 Utilities<br/>5 procs<br/>usp_DropConstraints<br/>usp_GenerateEmailHTML_*<br/>EmailQueue_MarkSent]:::family"""))
    L.append("")
    L.append("## Retail_Warehouse families (146 procs)")
    L.append("")
    rlist = [p for p in procs.get("Retail_Warehouse", []) if isinstance(p.get("definition"), str)]

    def fam(name):
        n = name.lower()
        if "merge" in n: return "MERGE"
        if "incremental" in n: return "Incremental"
        if "scd2" in n: return "SCD2"
        if "snapshot" in n: return "Snapshot"
        if "audit" in n: return "Audit/DQ"
        if "alert" in n or "sla" in n: return "Alert/SLA"
        if "refresh" in n or "update" in n or "load" in n or "populate" in n or "create" in n: return "Refresh/Load"
        if "drop" in n or "truncate" in n: return "Drop/Cleanup"
        if "validate" in n or "check" in n: return "Validate"
        if "history" in n or "log" in n: return "History/Log"
        return "Other"

    by_fam = defaultdict(list)
    for p in rlist:
        by_fam[fam(p["name"])].append(p)
    L.append(md_table(["Family", "Count", "Sample procs"], [
        [f, len(plist), ", ".join(f"`{p['name'][:35]}`" for p in plist[:3])]
        for f, plist in sorted(by_fam.items(), key=lambda x: -len(x[1]))
    ]))
    L.append("")
    L.append("## Wholesale_Warehouse procs (8)")
    L.append("")
    wholesale = [p for p in procs.get("Wholesale_Warehouse", []) if isinstance(p.get("definition"), str)]
    L.append(md_table(["Schema", "Proc name", "Size (chars)"], [
        [f"`{p['schema']}`", f"`{p['name']}`", fmt_int(len(p["definition"]))]
        for p in wholesale
    ]))
    L.append("")
    L.append("## 📂 Drill-down")
    L.append("")
    L.append("Full proc bodies → [`data/06-procs-raw.json`](../../data/06-procs-raw.json) (1.5 MB raw)")
    L.append("")
    L.append("Or per-warehouse details:")
    L.append("- [ETL_Framework](../02-storage/warehouses/etl-framework.md)")
    L.append("- [Retail_Warehouse](../02-storage/warehouses/retail-warehouse.md)")
    L.append("- [Wholesale_Warehouse](../02-storage/warehouses/wholesale-warehouse.md)")
    L.append("")
    L.append("---")
    write(DOCS / "03-logic" / "stored-procs.md", "\n".join(L))


def build_logic_views():
    L = []
    L.append("# 👁️ Views (145 user views)")
    L.append("")
    L.append("[← Logic](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## What is a view here?")
    L.append("")
    L.append("A T-SQL view that wraps SELECT/JOIN/WHERE business logic. The **`_Wrk` naming convention** = Working set views consumed by `usp_RefreshCuratedTableFromView` family of procs.")
    L.append("")
    L.append("Pattern: `INSERT INTO target_curated_table SELECT * FROM domain_Wrk.SomeView`")
    L.append("")
    L.append("## Distribution by container")
    L.append("")
    rows = []
    for c, lst in views.items():
        user_v = [v for v in lst if isinstance(v.get("definition"), str) and v.get("schema") not in {"sys", "queryinsights", "INFORMATION_SCHEMA"}]
        if user_v:
            rows.append([f"`{c}`", len(user_v)])
    rows.sort(key=lambda r: -r[1])
    L.append(md_table(["Container", "User views"], rows))
    L.append("")
    L.append("## Wholesale_Warehouse `_Wrk` schemas (114 views)")
    L.append("")
    wholesale_views = [v for v in views.get("Wholesale_Warehouse", []) if isinstance(v.get("definition"), str) and v.get("schema") not in {"sys", "queryinsights"}]
    by_sch = defaultdict(list)
    for v in wholesale_views:
        by_sch[v["schema"]].append(v["name"])
    L.append(md_table(["Schema", "Views", "Sample names"], [
        [f"`{s}`", len(vs), ", ".join(f"`{n}`" for n in sorted(vs)[:3]) + (f", … +{len(vs)-3}" if len(vs) > 3 else "")]
        for s, vs in sorted(by_sch.items(), key=lambda x: -len(x[1]))
    ]))
    L.append("")
    L.append("## Retail_Warehouse `_Wrk` schemas (29 views)")
    L.append("")
    retail_views = [v for v in views.get("Retail_Warehouse", []) if isinstance(v.get("definition"), str) and v.get("schema") not in {"sys", "queryinsights"}]
    by_sch = defaultdict(list)
    for v in retail_views:
        by_sch[v["schema"]].append(v["name"])
    L.append(md_table(["Schema", "Views", "Sample names"], [
        [f"`{s}`", len(vs), ", ".join(f"`{n}`" for n in sorted(vs)[:3])]
        for s, vs in sorted(by_sch.items(), key=lambda x: -len(x[1]))
    ]))
    L.append("")
    L.append("## 📂 Drill-down")
    L.append("")
    L.append("Full view definitions → [`data/07-views-raw.json`](../../data/07-views-raw.json) (408 KB raw)")
    L.append("")
    L.append("---")
    write(DOCS / "03-logic" / "views.md", "\n".join(L))


def build_logic_notebooks():
    L = []
    L.append("# 📓 Notebooks (18)")
    L.append("")
    L.append("[← Logic](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## Groups")
    L.append("")
    L.append(mermaid("""mindmap
  root((18 Notebooks))
    Active production
      MetaData-Pull 🔴 secret
      ShortCut-pulls_V1
      Sys_Data_pull
      TableDictionary_RJ
      Utilities (library)
      nb-sync-uc-fabric-onelake
    Vers5 trio dup
      Vers 5 (orig + date-std)
      Vers 5 Copy
      Vers 5new
    Ad-hoc utilities
      Convert decimal to Int
      Copy uppercase columns
      Create External Table
      Create Lakehouse view
      Rename column names 🐞
      RunZetaTestQuery
    Empty / test
      Test Notebook
      Notebook 12
      Notebook 13"""))
    L.append("")
    L.append("## 🔥 Active production (6)")
    L.append("")
    NB_DETAILS = [
        ("MetaData-Pull", "🔴 Plaintext SP secret cell 1", "Cross-WH JDBC sync — đọc Centralized_Warehouse.MetaData.CopyTables rồi copy mọi WH → Centralized_Warehouse.{src}_{schema}.{table}"),
        ("ShortCut-pulls_V1", "Cross-WS scan", "Inventories all shortcuts on Lakehouses+Warehouses via Fabric REST → writes Centralized_Warehouse.MetaData.ShortcutCatalog. WS filter trỏ 13eefa5e (ngoài DEV)"),
        ("Sys_Data_pull", "—", "Variant của MetaData-Pull, restricted to Source_Data WH. Cell 4 mature impl với TokenManager + retry/backoff"),
        ("TableDictionary_RJ", "—", "Reads Enterprise_Lakehouse.dw_developer.tabledictionary → parquet → Enterprise_Lakehouse.{schema}.{table}"),
        ("Utilities", "Library", "Library notebook — Databricks-UC ↔ Fabric-shortcut helpers. Called via `%run`"),
        ("nb-sync-uc-fabric-onelake", "Cross-WS target", "%run Utilities → sync edw_dev.retail_marketing UC → Marketing_Lakehouse trong workspace sg_DHalama"),
    ]
    L.append(md_table(
        ["Notebook", "Tag", "Purpose"],
        [[f"`{n}`", t, p] for n, t, p in NB_DETAILS],
    ))
    L.append("")
    L.append("## 🟠 Vers 5 trio (3 near-duplicates)")
    L.append("")
    L.append(md_table(
        ["Variant", "Cells", "Default LH", "Distinguishing"],
        [
            ["Vers 5 (orig)", "1", "Wholesale_Lakehouse", "Filter `%HGD%`. **Has date-standardize step**. Stale lakehouse GUID `75f83a27-...`"],
            ["Vers 5 Copy", "2", "Wholesale_Lakehouse", "Filter `OneSource%` + `PartyContacts%`. **No date-standardize**. Workspace-name path"],
            ["Vers 5new", "2", "Enterprise_Lakehouse", "Cell 1 same as Copy cell 2 minus `NOT LIKE %Msa%`. Cell 2 byte-identical to Copy cell 2"],
        ],
    ))
    L.append("")
    L.append("**Recommendation:** collapse into 1 parameterized notebook. Parameters: `filter_clause`, `target_lakehouse`, `enable_date_standardize`. Merge in Vers 5's date-standardize step.")
    L.append("")
    L.append("## 🟡 Ad-hoc utilities (6)")
    L.append("")
    AD_HOC = [
        ("Convert a column in a delta from decimal to Int", "Cast `GMCFISCALMONTH` decimal→int trên `CostAccounting_Lakehouse/Tables/FIF115`"),
        ("Copy Data from source to target (deltas) convert column names to upper case", "Copies `GrossMarginCubeData` → `FIF115` uppercasing column names"),
        ("Create External Table from parquet in Lakehouse", "Reads `FIF115.snappy.parquet` → external Delta `CostAccounting_Lakehouse.FIF115_Load`"),
        ("Create a Lakehouse view", "Demo SQL — creates view `caassd` rồi DROP"),
        ("Rename column names in a delta table", "Renames ~60 columns trên `Finance_Lakehouse.Wholesale_Invoicing_AFI/TSITXN`. 🐞 `delta_table_path2` undefined → NameError"),
        ("RunZetaTestQuery", "3 exploration queries trên `DHalama_Lakehouse` + `Retail_Lakehouse`. No writes"),
    ]
    L.append(md_table(["Notebook", "Purpose"], [[f"`{n}`", p] for n, p in AD_HOC]))
    L.append("")
    L.append("## 💀 Empty / test (3)")
    L.append("")
    L.append("- `Test Notebook` — ADF pipeline-run scratchpad (29 LOC)")
    L.append("- `Notebook 12` — Empty SQL stub (2 lines comment)")
    L.append("- `Notebook 13` — Placeholder của MS Fabric UC↔OneLake sample. ⚠️ Loads `util.py` từ public GitHub raw URL (supply-chain risk)")
    L.append("")
    L.append("## 🔗 Notebook dependency graph")
    L.append("")
    L.append("Only **one** internal edge in the entire workspace:")
    L.append("")
    L.append(mermaid("""flowchart LR
    NSU[nb-sync-uc-fabric-onelake]
    UTL[Utilities]
    NSU --%run--> UTL"""))
    L.append("")
    L.append("No `mssparkutils.notebook.run` calls anywhere.")
    L.append("")
    L.append("## 📂 Drill-down")
    L.append("")
    L.append("- Per-notebook source code: [`data/notebooks/`](../../data/notebooks/) (18 .ipynb + 18 .py)")
    L.append("- Structured analysis: [`data/04-notebooks-raw.json`](../../data/04-notebooks-raw.json)")
    L.append("")
    L.append("---")
    write(DOCS / "03-logic" / "notebooks.md", "\n".join(L))


# =============================================================
# 04 Orchestration
# =============================================================

PIPE_GROUPS = {
    "ETL/Migration": [
        ("EDW2FabricLoader", "Lookup+Filter+ForEach: Azure SQL DB ASHLEY_EDW_DEV.dw_developer.FabricMapping (Flag=1) → Fabric DW Source_Data; per-row dynamic Query/schema/table"),
        ("Fabric Migration ADF", "Same shape as EDW2FabricLoader but source = Synapse Ashley_Edw (SqlDWSource), with TRUNCATE precopy"),
        ("MigrateData", "Single Copy cross-WS: PROD Source_Data Retail_Corporate.BtaData last-90-days → DEV Source_Data"),
        ("Migration_TableDictionary_entry", "Copy Synapse Ashley_Edw.dw_developer.tabledictionary → ETL_Framework.dw_developer.TableDictionary_Helper, then Script merges into TableDictionary"),
        ("Load Retail_DW", "Single Copy: Azure SQL Ashley_EDW.Retail_DW.DimItemMaster → Fabric Retail_Warehouse with full ~100-col mapping"),
        ("Load MasterData_ItemMaster_AFI tables", "3 parallel Copies: Synapse Ashley_EDW.MasterData_ItemMaster_AFI.{GENDESC, ITEMBL, ITMEXT} → Fabric Source_Data"),
        ("Retail_Prod_To_Dev_DataBackFill", "On-prem SQL PROD → Fabric Source_Data. Snapshot block (33 tables) Inactive; Incremental Active. ⚠️ Failures since 2026-04-29"),
        ("Adhoc loads", "💀 EMPTY"),
    ],
    "Quality checks": [
        ("Source_EDW_Check_Test", "✅ Daily 03:50 UTC. Truncates Bronze counts, copies on-prem ASHLEY_EDW per metadata, runs SPs, sends Office365Email per row. 100% success since 2026-04-21"),
        ("Source_EDW_Aggregate_Check", "Single dangling Lookup — abandoned"),
        ("Count_Aggreagate_Check_Bronze", "💀 EMPTY"),
    ],
    "SLA / Alerting": [
        ("Alert_FabricTables_EnterpriseData", "usp_DataWarehouseDataFeedAlert_Fabric → Lookup Performance_Logs.EmailQueue → ForEach send via Office365Outlook + mark sent"),
        ("PL_SLA_Breach_EnterpriseData", "usp_DataWarehouseSLAAlert_Fabric → ForEach Office365Email1 to ⚠️ HARDCODED DL_AFI_Data_WarehouseGCC@Ashleyfurniture.com"),
        ("FabricSLA_Trigger_EnterpriseData", "💀 EMPTY — intended scheduler wrapper"),
    ],
    "System": [
        ("SysTable_Snapshot", "Reads Centralized_Warehouse.MetaData.SysObjectInfo → ForEach dynamic cross-WH Copy into Source_Data_<schema>.<table> + audit SP"),
        ("SysTable_Dynamic", "Variant with target schema Source_Data_<schema>_adf, no audit SP (asymmetric)"),
    ],
    "Test/junk": [
        ("test", "⚠️ NOT trivial — ForEach cross-WS Copy from PROD WH → SQLDatabase Commissions_Prototype"),
        ("pipeline1", "⚠️ NOT trivial — cross-WS Copy MasterData_Retail.CreditReview → Commissions_Prototype.Storis_DW.CreditReview"),
        ("pipeline2", "💀 EMPTY"),
        ("test1", "💀 EMPTY"),
        ("Pipeline_1_test", "💀 EMPTY"),
        ("testing_pipeline", "4-row union → Lakehouse RadarSync_Test.dbo.test_pipeline"),
    ],
}


def build_orch_readme():
    L = []
    L.append("# 🔁 04 — Orchestration")
    L.append("")
    L.append("[← Root](../../README.md)")
    L.append("")
    L.append("## What lives here")
    L.append("")
    L.append("Triggers, schedulers, and integrations — what schedules **when** logic runs.")
    L.append("")
    L.append(md_table(
        ["Type", "Count", "Detail"],
        [
            ["🔁 **Data Pipelines**", "22", "[See pipelines →](pipelines.md)"],
            ["🪞 **Mirror (Databricks)**", "1", "[See mirror →](mirror.md)"],
            ["🏭 **Mounted ADF**", "1", "[See ADF →](adf.md)"],
            ["🌊 **Dataflow Gen2**", "1", "[See dataflow →](dataflow.md)"],
            ["⚡ **Reflex (Activator)**", "1", "[See reflex →](reflex.md)"],
            ["🐍 **Spark Environments**", "2", "[See operations →](../08-operations/environments.md)"],
            ["📈 **Semantic Model**", "1", "Auto-generated for Dataflow staging"],
        ],
    ))
    L.append("")
    L.append("## 🚦 Pipeline call graph")
    L.append("")
    L.append("> **No `ExecutePipeline` activities exist anywhere.** All pipelines run independently. Coupling is via shared metadata tables.")
    L.append("")
    L.append(mermaid("""flowchart TB
    subgraph META[Shared metadata]
        FM[FabricMapping]
        TD[TableDictionary]
        SOI[SysObjectInfo]
        EQ[EmailQueue]
    end

    EDW2[EDW2FabricLoader] -.reads.-> FM
    FMA[Fabric Migration ADF] -.reads.-> FM
    SECT[Source_EDW_Check_Test<br/>daily 03:50 UTC ✅] -.reads.-> SECC[Source_EDW_CountCheck]
    SS[SysTable_Snapshot] -.reads.-> SOI
    SD[SysTable_Dynamic] -.reads.-> SOI
    ALERT[Alert_FabricTables] -.reads.-> EQ
    SLA[PL_SLA_Breach] -.reads.-> EQ"""))
    L.append("")
    L.append("## 📑 Sub-pages")
    L.append("")
    L.append("- [🔁 Pipelines (22)](pipelines.md) — categorized + run status")
    L.append("- [🪞 Mirror (Databricks UC `edw_dev`)](mirror.md)")
    L.append("- [🏭 Mounted ADF (`ashleyv2datafactory`)](adf.md)")
    L.append("- [🌊 Dataflow Gen2 (`Dataflow Test`)](dataflow.md)")
    L.append("- [⚡ Reflex (broken)](reflex.md)")
    L.append("")
    L.append("## ⚠️ Orchestration risks")
    L.append("")
    L.append("- **C5**: `Retail_Prod_To_Dev_DataBackFill` failures since 2026-04-29")
    L.append("- **C6**: `FabricSLA_Trigger_EnterpriseData` empty wrapper")
    L.append("- **C7**: Hardcoded recipient in `PL_SLA_Breach`")
    L.append("- **C8**: Reflex broken `getDefinition`")
    L.append("- **C13/C14**: Empty test pipelines + misnamed `test`/`pipeline1` cross-WS PROD copies")
    L.append("")
    L.append("Full risk list → [09 Risks](../09-risks/README.md)")
    L.append("")
    L.append("---")
    write(DOCS / "04-orchestration" / "README.md", "\n".join(L))


def build_orch_pipelines():
    L = []
    L.append("# 🔁 Data Pipelines (22)")
    L.append("")
    L.append("[← Orchestration](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## Run status overview")
    L.append("")
    active = sum(1 for n in [it["name"] for it in inv.get("DataPipeline", [])]
                 if isinstance(runs.get(n, {}).get("runs"), list) and runs[n]["runs"])
    L.append(f"- **{active}** pipelines have run history in API window")
    L.append(f"- **{22 - active}** dormant (never ran or older than window)")
    L.append("")
    L.append("## By group")
    L.append("")
    for grp, items in PIPE_GROUPS.items():
        L.append(f"### {grp} ({len(items)})")
        L.append("")
        rows = []
        for nm, desc in items:
            st = get_run_status(nm, "DataPipeline")
            rows.append([f"`{nm}`", desc, st])
        L.append(md_table(["Pipeline", "Purpose", "Status"], rows))
        L.append("")
    L.append("## 📂 Drill-down")
    L.append("")
    L.append("- Per-pipeline JSON: [`data/pipelines/`](../../data/pipelines/) (22 .json files)")
    L.append("- Run history detail: [08 Operations / Run history](../08-operations/run-history.md)")
    L.append("")
    L.append("---")
    write(DOCS / "04-orchestration" / "pipelines.md", "\n".join(L))


def build_orch_mirror():
    L = []
    L.append("# 🪞 Mirrored Azure Databricks Catalog `edw_dev`")
    L.append("")
    L.append("[← Orchestration](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## Configuration")
    L.append("")
    L.append(md_table(
        ["Field", "Value"],
        [
            ["Item ID", "`1e284ab4-dc84-4421-a96d-fe4f942cec97`"],
            ["Type", "MirroredAzureDatabricksCatalog"],
            ["Source connection", "`1d4b92c8-...` (Databricks workspace)"],
            ["Source catalog", "`edw_dev`"],
            ["Mode", "**Full** (all schemas mirrored)"],
            ["autoSync", "**Enabled**"],
            ["Last sync", "2026-05-08 05:57:00Z **Success**"],
        ],
    ))
    L.append("")
    L.append("## 🌐 What it does")
    L.append("")
    L.append("Live read-only mirror of an Azure Databricks Unity Catalog catalog into Fabric OneLake. Tables in `edw_dev` UC become queryable from Fabric with **zero data movement** — they're surfaced via OneLake.")
    L.append("")
    L.append(mermaid("""flowchart LR
    DBX[(Databricks UC<br/>edw_dev catalog<br/>retail_marketing schema +<br/>others)]
    MIRROR[edw_dev<br/>MirroredAzureDatabricksCatalog<br/>Full + autoSync]
    OL[Fabric OneLake<br/>+ SQL endpoint]

    DBX -.live mirror.-> MIRROR
    MIRROR -.OneLake surface.-> OL"""))
    L.append("")
    L.append("## 🔍 Consumers")
    L.append("")
    L.append("**No pipeline references this mirror as source/sink** — pipelines don't need to. Consumers access mirrored data via:")
    L.append("- OneLake path (`abfss://...edw_dev/...`) from Spark/notebooks")
    L.append("- SQL endpoint (same host as Fabric DWs)")
    L.append("")
    L.append("Notebook `nb-sync-uc-fabric-onelake` syncs `edw_dev.retail_marketing` UC → `Marketing_Lakehouse` in workspace `sg_DHalama`.")
    L.append("")
    L.append("---")
    write(DOCS / "04-orchestration" / "mirror.md", "\n".join(L))


def build_orch_adf():
    L = []
    L.append("# 🏭 Mounted Data Factory `ashleyv2datafactory`")
    L.append("")
    L.append("[← Orchestration](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## Configuration")
    L.append("")
    L.append(md_table(
        ["Field", "Value"],
        [
            ["Item ID", "`ab9391a5-3161-4a74-9cfc-c5bdc28f902f`"],
            ["Type", "MountedDataFactory"],
            ["Resource path", "`/subscriptions/68cde257-828b-4f5e-a7f1-4eb9683c89d6/resourceGroups/IoT_Hub/providers/Microsoft.DataFactory/factories/ashleyv2datafactory`"],
            ["Subscription", "`68cde257-...`"],
            ["Resource group", "`IoT_Hub`"],
            ["ADF name", "`ashleyv2datafactory`"],
            ["Mode", "Mount-only (legacy ADF surfaced inside Fabric)"],
        ],
    ))
    L.append("")
    L.append("## 🔗 What it surfaces")
    L.append("")
    L.append("This isn't a Fabric pipeline — it's a **link** to an external Azure Data Factory whose pipelines are visible inside this Fabric workspace. The legacy ADF predates the BI/data platform consolidation (RG name `IoT_Hub` is a hint).")
    L.append("")
    L.append("## 🔍 Indirect references")
    L.append("")
    L.append("- `SysTable_Dynamic` pipeline targets `Source_Data_<schema>_adf` schemas — the `_adf` suffix indicates ADF-driven loads.")
    L.append("- ADF pipelines visible from here populate `Source_Data` warehouse via the same flows.")
    L.append("")
    L.append("---")
    write(DOCS / "04-orchestration" / "adf.md", "\n".join(L))


def build_orch_dataflow():
    L = []
    L.append("# 🌊 Dataflow Gen2 `Dataflow Test`")
    L.append("")
    L.append("[← Orchestration](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## Status: 💀 EMPTY")
    L.append("")
    L.append("`getDefinition` returns this M code:")
    L.append("")
    L.append("```m")
    L.append('[StagingDefinition = [Kind = "FastCopy"]]')
    L.append("section Section1;")
    L.append("```")
    L.append("")
    L.append("No queries, no connections.")
    L.append("")
    L.append("## Auto-staging companions")
    L.append("")
    L.append("Fabric auto-creates these alongside any Dataflow Gen2:")
    L.append("- `DataflowsStagingLakehouse` (LH) — empty")
    L.append("- `StagingLakehouseForDataflows_20251008191803` (LH timestamped) — empty")
    L.append("- `DataflowsStagingWarehouse` (WH) — empty")
    L.append("- `StagingWarehouseForDataflows_20251008191817` (WH timestamped) — empty")
    L.append("- `DataflowsStagingWarehouse` (SemanticModel) — auto-generated")
    L.append("")
    L.append("All safe to delete if `Dataflow Test` stays empty (risk **C11**).")
    L.append("")
    L.append("---")
    write(DOCS / "04-orchestration" / "dataflow.md", "\n".join(L))


def build_orch_reflex():
    L = []
    L.append("# ⚡ Reflex `Reflex 2024-05-29 14:19:44`")
    L.append("")
    L.append("[← Orchestration](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## Status: 💀 BROKEN")
    L.append("")
    L.append("Item ID: `c9a38887-75ce-49e2-82ea-c0d9df39e154`")
    L.append("")
    L.append("`getDefinition` returns:")
    L.append("```")
    L.append("Activator_Export_FailedToExportActivator_ReflexBackendError")
    L.append('"Invalid artifact id" / data sources not GIT/CICD-supported')
    L.append("```")
    L.append("")
    L.append("Triggers and targets are **unrecoverable via API**. The default datestamp name (`2024-05-29`) and ~1-year staleness suggest abandonment (risk **C8**).")
    L.append("")
    L.append("**Recommendation:** confirm with workspace owner, then delete.")
    L.append("")
    L.append("---")
    write(DOCS / "04-orchestration" / "reflex.md", "\n".join(L))


# =============================================================
# 05 Data Flow
# =============================================================

def build_data_flow():
    L = []
    L.append("# 🔀 05 — Data Flow (End-to-End Lineage)")
    L.append("")
    L.append("[← Root](../../README.md)")
    L.append("")
    L.append("## The big picture")
    L.append("")
    L.append("![Data flow](../../images/05-data-flow.svg)")
    L.append("")
    L.append(mermaid("""flowchart LR
    classDef src fill:#e8f4fd,stroke:#3a8;
    classDef ing fill:#fef3c7,stroke:#d97706;
    classDef bronze fill:#dbeafe,stroke:#2563eb;
    classDef silver fill:#e0e7ff,stroke:#4f46e5;
    classDef gold fill:#fce7f3,stroke:#db2777;
    classDef ext fill:#fed,stroke:#c93;

    %% External sources
    EDW[(ASHLEY_EDW_DEV)]:::src
    SYN[(Synapse Ashley_Edw)]:::src
    DBX[(Databricks UC<br/>edw_dev)]:::src
    SAAS[UKG / AFI / Maximo /<br/>AshleyServiceNow / GA]:::src
    ADLS[ADLS Gen2<br/>ashleydevlake]:::ext
    PROD[(PROD WS<br/>ce4e6503)]:::ext

    %% Ingestion
    PIPE_EDW[EDW2FabricLoader]:::ing
    PIPE_MIG[Fabric Migration ADF]:::ing
    PIPE_RET[Load Retail_DW]:::ing
    PIPE_MD[Load MasterData_AFI]:::ing
    PIPE_BACK[Retail_Prod_To_Dev_DataBackFill]:::ing
    ADF[Mounted ADF<br/>ashleyv2datafactory]:::ing
    NB_VERS5[Vers5 notebooks]:::ing
    MIRROR[edw_dev Mirror]:::ing

    %% Bronze
    SD[Source_Data WH<br/>BRONZE<br/>64 schemas / 636 tables]:::bronze

    %% Silver
    RW[Retail_Warehouse<br/>198 tables · 146 procs]:::silver
    WW[Wholesale_Warehouse<br/>209 tables · 114 _Wrk views]:::silver
    MD[MasterData_Warehouse<br/>46 tables]:::silver
    DW[Distribution_Warehouse<br/>7 tables]:::silver

    %% Gold
    CW[Centralized_Warehouse<br/>38 tables · 0 procs]:::gold
    CL[(Centralized_Lakehouse<br/>501 tables · 5.92B rows<br/>shortcut to PROD)]:::gold

    %% Wiring
    EDW --> PIPE_EDW
    EDW --> PIPE_RET
    EDW -.> PIPE_BACK
    SYN --> PIPE_MIG
    SYN --> PIPE_MD
    SAAS --> ADF
    DBX --> MIRROR
    ADLS -.shortcuts.-> SD

    PIPE_EDW --> SD
    PIPE_MIG --> SD
    PIPE_MD --> SD
    PIPE_BACK --> SD
    ADF --> SD
    PIPE_RET --> RW
    NB_VERS5 --> CL
    MIRROR -.OneLake.-> CL
    PROD -.18 OneLake shortcuts.-> CL

    SD -- usp_RefreshCuratedTableFromView --> RW
    SD -- usp_RefreshCuratedTableFromView --> WW
    SD -- usp_RefreshCuratedTableFromView --> MD
    SD -- usp_RefreshCuratedTableFromView --> DW

    RW --> CW
    WW --> CW
    MD --> CW
    DW --> CW

    CW --> PBI[Power BI / Reporting]
    CL --> PBI"""))
    L.append("")
    L.append("## Following one row from upstream to consumption")
    L.append("")
    L.append("1. **Source** — row originates in:")
    L.append("   - On-prem SQL Server `ASHLEY_EDW_DEV` (e.g. `Retail_DW.DimItemMaster`)")
    L.append("   - Synapse SQLDW `Ashley_Edw`")
    L.append("   - SaaS feed via UKG / AFI / Maximo / AshleyServiceNow → Mounted ADF")
    L.append("   - Databricks Unity Catalog `edw_dev` → Mirror (Full + autoSync)")
    L.append("")
    L.append("2. **Ingestion** — by one of:")
    L.append("   - Fabric Pipeline (driven by `ETL_Framework.TableDictionary` or `…FabricMapping`)")
    L.append("   - Mounted ADF (legacy ingestion path)")
    L.append("   - Notebook calling `Usp_CreateTableFromParquet*` (parquet on ADLS → Delta)")
    L.append("   - Mirror (no pipeline; data lives in OneLake automatically)")
    L.append("")
    L.append("3. **Lands in `Source_Data`** — Bronze tier WH (64 schemas / 636 tables). Some tables also written to `Centralized_Lakehouse` via Vers5 notebook family.")
    L.append("")
    L.append("4. **Promoted to domain warehouse** — via `usp_RefreshCuratedTableFromView` → `Retail_Warehouse`, `Wholesale_Warehouse`, `MasterData_Warehouse`, `Distribution_Warehouse`.")
    L.append("")
    L.append("5. **Aggregated into `Centralized_Warehouse`** — 38 tables / 0 procs — loaded by external orchestrators / notebooks (e.g. `MetaData-Pull`).")
    L.append("")
    L.append("6. **Consumed** — by Power BI semantic models (1 in this WS, others elsewhere) and SQLDatabase `Commissions_Prototype` (via misnamed `test` and `pipeline1` pipelines).")
    L.append("")
    L.append("7. **Audit trail** — in `ETL_Framework.DW_Developer.AuditLog`. SLA breaches & data-feed failures land in `Performance_Logs.EmailQueue` and emailed via Office365 Logic App.")
    L.append("")
    L.append("## Per-leg pages")
    L.append("")
    L.append("- [Source → Bronze](source-to-bronze.md) — how raw data lands in `Source_Data`")
    L.append("- [Bronze → Silver](bronze-to-silver.md) — how `usp_RefreshCuratedTableFromView` populates domain WHs")
    L.append("- [Silver → Gold](silver-to-gold.md) — how `Centralized_Warehouse` and `Centralized_Lakehouse` are populated")
    L.append("")
    L.append("---")
    write(DOCS / "05-data-flow" / "README.md", "\n".join(L))


def build_data_flow_legs():
    # Source → Bronze
    L = []
    L.append("# Source → Bronze (`Source_Data`)")
    L.append("")
    L.append("[← Data Flow](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## Sources")
    L.append("")
    L.append(md_table(
        ["Source system", "Type", "Connection / location", "Loader"],
        [
            ["ASHLEY_EDW_DEV", "On-prem SQL Server", "`3fff77ab-...` SqlServer connection", "EDW2FabricLoader · Source_EDW_Check_Test · Retail_Prod_To_Dev_DataBackFill"],
            ["Ashley_Edw", "Synapse SQLDW", "Synapse linked service", "Fabric Migration ADF · Load MasterData_ItemMaster_AFI · Migration_TableDictionary_entry"],
            ["Ashley_EDW", "Azure SQL DB", "ASHLEY_EDW_DEV.dw_developer.FabricMapping", "Load Retail_DW · EDW2FabricLoader (metadata)"],
            ["UKG / AFI / Maximo / SNow / GA", "SaaS", "Various", "Mounted ADF `ashleyv2datafactory`"],
            ["edw_dev", "Databricks UC", "Connection `1d4b92c8-...`", "Mirror (no pipeline)"],
            ["ashleydevlake", "ADLS Gen2", "Connection `65655456-...`", "Notebooks via shortcuts in A_Developement / RadarSync_Test"],
        ],
    ))
    L.append("")
    L.append("## Active loaders")
    L.append("")
    L.append("Of 8 ETL pipelines, only **`Source_EDW_Check_Test`** runs daily (03:50 UTC). All others are dormant or recently-active (`Retail_Prod_To_Dev_DataBackFill` last ran 2026-04-29).")
    L.append("")
    L.append("---")
    write(DOCS / "05-data-flow" / "source-to-bronze.md", "\n".join(L))

    # Bronze → Silver
    L = []
    L.append("# Bronze → Silver (Domain Warehouses)")
    L.append("")
    L.append("[← Data Flow](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## Pattern")
    L.append("")
    L.append("```sql")
    L.append("-- Conceptual pattern (per curated table)")
    L.append("EXEC ETL_Framework.DW_Developer.usp_RefreshCuratedTableFromView")
    L.append("    @TargetSchema = 'MasterData_Retail',")
    L.append("    @TargetTable  = 'SalesPerson',")
    L.append("    @SourceView   = 'Source_Data.MasterData_Retail_Wrk.vw_SalesPerson_Working';")
    L.append("```")
    L.append("")
    L.append("The proc:")
    L.append("1. Reads from a `_Wrk` Working-set view in `Source_Data` (or a domain warehouse's _Wrk schema)")
    L.append("2. Performs INSERT/UPDATE/MERGE into the target curated table")
    L.append("3. Writes to `ETL_Framework.DW_Developer.AuditLog`")
    L.append("")
    L.append("## Domain → procs ratio")
    L.append("")
    L.append(md_table(
        ["Domain", "Tables", "Views", "Procs internal", "Pattern"],
        [
            ["Retail_Warehouse", "198", "29 (incl. 14 `Retail_Sales_Wrk`)", "146", "Refresh-Load + MERGE + Validate + Audit"],
            ["Wholesale_Warehouse", "209", "114 `_Wrk` views", "8 (large, ~20K avg)", "Multi-table MERGE-heavy"],
            ["MasterData_Warehouse", "46", "—", "0 (driven by ETL_Framework)", "External orchestration"],
            ["Distribution_Warehouse", "7", "—", "0", "External orchestration"],
            ["Quality_Warehouse", "0", "—", "0", "🔴 Empty"],
        ],
    ))
    L.append("")
    L.append("---")
    write(DOCS / "05-data-flow" / "bronze-to-silver.md", "\n".join(L))

    # Silver → Gold
    L = []
    L.append("# Silver → Gold (Centralized)")
    L.append("")
    L.append("[← Data Flow](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## Two parallel gold layers")
    L.append("")
    L.append("### Centralized_Warehouse — 38 tables, 0 procs")
    L.append("")
    L.append("Has no internal stored procs. Loaded externally by `MetaData-Pull` notebook which:")
    L.append("- Reads `Centralized_Warehouse.MetaData.CopyTables` config")
    L.append("- JDBC-copies all warehouses into `Centralized_Warehouse.{src_wh}_{schema}.{table}`")
    L.append("")
    L.append("### Centralized_Lakehouse — 501 tables, 5.92 B rows")
    L.append("")
    L.append("**SHORTCUT-BACKED.** 18 OneLake shortcuts:")
    L.append("- 12 → PROD `Source_Data` WH (`d27b3ef9-...`)")
    L.append("- 6 → PROD `Retail_Warehouse` WH (`d8bec39c-...`)")
    L.append("")
    L.append("Twin schemas `Retail_Corporate` ↔ `Retail_Corporate_Prod` = 2 shortcuts to the same PROD path.")
    L.append("")
    L.append(mermaid("""flowchart LR
    PROD_SD[(PROD Source_Data)]
    PROD_RW[(PROD Retail_Warehouse)]
    DEV_CL[(DEV Centralized_Lakehouse<br/>501 tables · 5.92B rows)]

    PROD_SD -- 12 OneLake shortcuts --> DEV_CL
    PROD_RW -- 6 OneLake shortcuts --> DEV_CL"""))
    L.append("")
    L.append("**Implication:** writes to DEV `Centralized_Lakehouse` schemas backed by shortcuts will **affect PROD-shaped paths**. Read-only consumption is safe; transformations should target a separate output table.")
    L.append("")
    L.append("---")
    write(DOCS / "05-data-flow" / "silver-to-gold.md", "\n".join(L))


# =============================================================
# 06 Cross-Workspace
# =============================================================

def build_cross_ws():
    L = []
    L.append("# 🔗 06 — Cross-Workspace Dependencies")
    L.append("")
    L.append("[← Root](../../README.md)")
    L.append("")
    L.append("## Map")
    L.append("")
    L.append("![Cross-WS](../../images/06-cross-ws.svg)")
    L.append("")
    L.append(mermaid("""flowchart LR
    classDef ext fill:#fed,stroke:#c93;
    classDef prod fill:#fdd,stroke:#c33;
    classDef unknown fill:#fcf,stroke:#93c;

    subgraph DEV[EnterpriseData-Dev<br/>5360a935]
        DEV_CL[Centralized_Lakehouse]
        DEV_AD[A_Developement LH]
        DEV_RST[RadarSync_Test LH]
        DEV_NB[Notebooks]
    end
    subgraph PROD[PROD WS EnterpriseData<br/>ce4e6503<br/>14 WH + 1 LH]
        P_SD[(Source_Data WH<br/>d27b3ef9)]
        P_RW[(Retail_Warehouse WH<br/>d8bec39c)]
        P_OTH[+12 other items]
    end
    subgraph UNK[Unknown / inaccessible]
        U_LHS[CostAccounting_LH<br/>Wholesale_LH<br/>Retail_LH<br/>Enterprise_LH]
        U_WS1[WS 13eefa5e 403]
        U_WS2[sg_DHalama]
    end
    subgraph EXT[External Azure]
        ADLS[ashleydevlake.dfs.core.windows.net<br/>ADLS Gen2]
        ADF[ashleyv2datafactory<br/>RG IoT_Hub]
        EDW[(ASHLEY_EDW_DEV)]
        SYN[(Synapse Ashley_Edw)]
    end

    P_SD -- 12 shortcuts --> DEV_CL
    P_RW -- 6 shortcuts --> DEV_CL
    ADLS -- 7 shortcuts --> DEV_AD
    ADLS -- 2 broad mounts --> DEV_RST
    EDW --> DEV_NB
    SYN --> DEV_NB
    ADF -- mounted --> DEV_NB
    DEV_NB -.references.-> U_LHS
    DEV_NB -.target/source.-> U_WS1
    DEV_NB -.target.-> U_WS2

    class ADLS,ADF,EDW,SYN ext;
    class P_SD,P_RW,P_OTH prod;
    class U_LHS,U_WS1,U_WS2 unknown;"""))
    L.append("")
    L.append("## Sub-pages")
    L.append("")
    L.append("- [PROD dependencies](prod-dependencies.md) — 18 OneLake shortcuts + PROD inventory")
    L.append("- [ADLS storage](adls-storage.md) — 9 ADLS Gen2 shortcuts to `ashleydevlake`")
    L.append("- [Inaccessible references](inaccessible-refs.md) — workspaces and items I couldn't read")
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append(md_table(
        ["Category", "Count", "Detail"],
        [
            ["OneLake shortcuts within DEV (Fabric-internal)", "385", "Internal table-to-files mapping"],
            ["OneLake shortcuts to PROD WS", "**18**", "All to `ce4e6503-...` Source_Data + Retail_Warehouse"],
            ["ADLS Gen2 shortcuts", "**9**", "All to `ashleydevlake.dfs.core.windows.net`"],
            ["Inaccessible workspaces", "2", "WS `13eefa5e-...` (403), WS `sg_DHalama` (by name)"],
            ["Unresolvable lakehouses", "4 + 1 stale", "CostAccounting_LH, Wholesale_LH, Retail_LH, Enterprise_LH, stale 75f83a27"],
        ],
    ))
    L.append("")
    L.append("---")
    write(DOCS / "06-cross-workspace" / "README.md", "\n".join(L))

    # PROD deps detail
    L = []
    L.append("# PROD Workspace Dependencies")
    L.append("")
    L.append("[← Cross-Workspace](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## PROD `EnterpriseData` (`ce4e6503-...`) inventory (discovered)")
    L.append("")
    L.append(md_table(
        ["Type", "Name", "ID", "Notes"],
        [
            ["Lakehouse", "Centralized_Lakehouse", "`08de1cf3-d529-4a71-8f6f-4c8d6f3b2018`", ""],
            ["Warehouse", "Source_Data", "`d27b3ef9-a331-4489-abca-588f909c4321`", "← target of 12 DEV shortcuts"],
            ["Warehouse", "Retail_Warehouse", "`d8bec39c-5973-47e9-aa68-67c0f0c4a771`", "← target of 6 DEV shortcuts"],
            ["Warehouse", "Centralized_Warehouse", "`513a8f2c-...`", ""],
            ["Warehouse", "AI_Warehouse", "`d47c0980-...`", "🆕 PROD-only (not in DEV)"],
            ["Warehouse", "A_Production2", "`67ea8404-...`", "🆕 PROD-only"],
            ["Warehouse", "Distribution_Warehouse", "`c4099421-...`", ""],
            ["Warehouse", "ETL_Framework", "`0d84211d-...`", ""],
            ["Warehouse", "EnterpriseData", "`83183106-...`", "🆕 PROD-only"],
            ["Warehouse", "Enterprise_Warehouse", "`3468b240-...`", "🆕 PROD-only"],
            ["Warehouse", "MasterData_Warehouse", "`d8e6439b-...`", ""],
            ["Warehouse", "Quality_Warehouse", "`063c11ae-...`", "(empty in DEV too)"],
            ["Warehouse", "SupplyChain_Warehouse", "`d926e44c-...`", "🆕 PROD-only"],
            ["Warehouse", "Wholesale_Warehouse", "`9293af4e-...`", ""],
        ],
    ))
    L.append("")
    L.append("**5 warehouses exist in PROD but not DEV**: `AI_Warehouse`, `A_Production2`, `EnterpriseData`, `Enterprise_Warehouse`, `SupplyChain_Warehouse`. These domains aren't mirrored to DEV.")
    L.append("")
    L.append("## Shortcut detail")
    L.append("")
    L.append("All 18 cross-WS shortcuts originate from `Centralized_Lakehouse` in DEV:")
    L.append("")
    L.append(md_table(
        ["DEV path", "→ Target WS", "→ Target item", "→ Target path"],
        [
            ["Tables/Retail_Sales_Enh", "PROD ce4e6503", "d8bec39c (Retail_Warehouse)", "Tables/Retail_Sales_Enh"],
            ["Tables/Retail_Sales", "PROD ce4e6503", "d8bec39c", "Tables/Retail_Sales"],
            ["Tables/Retail_Miniapps", "PROD ce4e6503", "d27b3ef9 (Source_Data)", "Tables/Retail_Miniapps"],
            ["Tables/Retail_External", "PROD ce4e6503", "d27b3ef9", "Tables/Retail_External"],
            ["Tables/Retail_Dart", "PROD ce4e6503", "d27b3ef9", "Tables/Retail_Dart"],
            ["Tables/Retail_Corporate_Prod", "PROD ce4e6503", "d27b3ef9", "Tables/Retail_Corporate"],
            ["Tables/Retail_Corporate", "PROD ce4e6503", "d27b3ef9", "Tables/Retail_Corporate"],
            ["Tables/MasterData_Retail*", "PROD ce4e6503", "d27b3ef9", "Tables/MasterData_Retail*"],
            ["Tables/MasterData_Product*", "PROD ce4e6503", "d27b3ef9", "Tables/MasterData_Product*"],
            ["Tables/MasterData_HR_UKG_*", "PROD ce4e6503", "d27b3ef9", "Tables/MasterData_HR_UKG_*"],
        ],
    ))
    L.append("")
    L.append("---")
    write(DOCS / "06-cross-workspace" / "prod-dependencies.md", "\n".join(L))

    # ADLS storage
    L = []
    L.append("# External ADLS Gen2 Storage")
    L.append("")
    L.append("[← Cross-Workspace](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## Storage account")
    L.append("")
    L.append(md_table(
        ["Field", "Value"],
        [
            ["Account", "`ashleydevlake.dfs.core.windows.net`"],
            ["Connection ID", "`65655456-2ff7-4981-8911-2320b6738f35`"],
            ["Containers", "`trusted-zone`, `raw-zone`"],
        ],
    ))
    L.append("")
    L.append("## Mounted shortcuts")
    L.append("")
    L.append(md_table(
        ["Lakehouse", "Mounted as", "Subpath"],
        [
            ["A_Developement", "`VVSSku`", "`/trusted-zone/MasterData/QTIL/VVSSku`"],
            ["A_Developement", "`Joblabor`", "`/trusted-zone/Manufacturing/Maximo/Joblabor`"],
            ["A_Developement", "`Drive4AshleyEventsname`", "`/trusted-zone/MasterData/ADS/GoogleAnalytics_Processed/Drive4AshleyEventsname`"],
            ["A_Developement", "`Drive4AshleyDemographicdetails`", "`/trusted-zone/.../Drive4AshleyDemographicdetails`"],
            ["A_Developement", "`Drive4AshleyConversionsEventname` (×2)", "`/trusted-zone/.../Drive4AshleyConversionsEventname` (duplicate)"],
            ["A_Developement", "`Testing_shortcut`", "`/raw-zone/temp/fabricShortCutTesting/Testing_shortcut`"],
            ["RadarSync_Test", "`trusted-zone`", "`/trusted-zone` (**entire container** ⚠️)"],
            ["RadarSync_Test", "`raw-zone`", "`/raw-zone` (**entire container** ⚠️)"],
        ],
    ))
    L.append("")
    L.append("## ⚠️ Risk C28")
    L.append("")
    L.append("`RadarSync_Test` mounts the **entire** `trusted-zone` and `raw-zone` containers. Anyone with access to that lakehouse can read all of Maximo, MasterData, Retail raw/trusted-zone data. Restrict scope or audit access list.")
    L.append("")
    L.append("---")
    write(DOCS / "06-cross-workspace" / "adls-storage.md", "\n".join(L))

    # Inaccessible refs
    L = []
    L.append("# Inaccessible References")
    L.append("")
    L.append("[← Cross-Workspace](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("Items referenced from this workspace's notebooks/code that I couldn't read directly.")
    L.append("")
    L.append("## Workspaces I got 403 on")
    L.append("")
    L.append("- **`13eefa5e-506c-4c07-a500-282bbffddf7d`** — referenced as `WORKSPACE_ID_FILTER` in `ShortCut-pulls_V1.py`. 403 Forbidden when listing items.")
    L.append("- **`sg_DHalama`** (by name only) — target of `nb-sync-uc-fabric-onelake` (writes `Marketing_Lakehouse` there).")
    L.append("")
    L.append("## Lakehouses referenced by GUID but not in any workspace I can list")
    L.append("")
    L.append(md_table(
        ["Inferred name", "GUID", "Used by"],
        [
            ["CostAccounting_Lakehouse", "`e4f5f630-4de5-44ba-9213-1dedf08e69e7`", "Convert/Copy/Create_External notebooks (3)"],
            ["Wholesale_Lakehouse", "`3f8d8040-f40e-49bd-af24-bf81e8b89994`", "Vers 5 / Vers 5 Copy default LH"],
            ["Retail_Lakehouse", "`cfb3e33f-011e-4766-8722-8913aa655e89`", "RunZetaTestQuery default LH"],
            ["Enterprise_Lakehouse", "`a41163dc-182c-402a-b97b-08b93351c9b5`", "TableDictionary_RJ + Vers5new"],
            ["(stale)", "`75f83a27-e35e-42df-8b4b-8ab281ab72c8`", "Vers 5 control path — does not resolve anywhere"],
        ],
    ))
    L.append("")
    L.append("These likely live in **personal-developer workspaces** I don't have access to.")
    L.append("")
    L.append("---")
    write(DOCS / "06-cross-workspace" / "inaccessible-refs.md", "\n".join(L))


# =============================================================
# 07 Permissions
# =============================================================

def build_permissions():
    L = []
    L.append("# 🔐 07 — Permissions")
    L.append("")
    L.append("[← Root](../../README.md)")
    L.append("")
    L.append("## Role distribution (34 principals)")
    L.append("")
    L.append("![Permissions tree](../../images/07-permissions.svg)")
    L.append("")
    L.append(mermaid("""graph TB
    classDef admin fill:#fee2e2,stroke:#dc2626;
    classDef member fill:#fef3c7,stroke:#d97706;
    classDef contrib fill:#dbeafe,stroke:#2563eb;
    classDef viewer fill:#e5e7eb,stroke:#6b7280;
    classDef spn fill:#fecaca,stroke:#991b1b;
    classDef group fill:#fde68a,stroke:#ca8a04;

    WS[Workspace<br/>EnterpriseData-Dev<br/>34 principals]

    WS --> A[👑 Admins · 12]:::admin
    WS --> M[Members · 6]:::member
    WS --> C[Contributors · 14]:::contrib
    WS --> V[Viewers · 2]:::viewer

    A --> AG[Group · Sg_AFI_Role_BIDataWarehouse_All_Unv]:::group
    A --> A1[👤 8 individual users]
    A --> AS1[🤖 onelakedev-connector]:::spn
    A --> AS2[🤖 AshleyBIApplicationDev]:::spn
    A --> AS3[🤖 AshleyBIApplicationProd ⚠️]:::spn"""))
    L.append("")
    L.append("## Composition")
    L.append("")
    L.append(md_table(
        ["Type", "Count"],
        [
            ["Users", "22"],
            ["Apps (SPN)", "8"],
            ["Groups", "4"],
        ],
    ))
    L.append("")
    L.append("**No external (non-`@Ashleyfurniture.com`) users.**")
    L.append("")
    L.append("## Admin principals (12)")
    L.append("")
    ra = perms.get("roleAssignments", [])
    admin_rows = []
    for r in ra:
        if r.get("groupUserAccessRight") == "Admin":
            pt = r.get("principalType", "?")
            name = r.get("displayName") or r.get("emailAddress") or "?"
            risky = "⚠️ " if "AshleyBIApplicationProd" in name else ""
            admin_rows.append([
                f"{risky}`{name}`",
                pt,
                f"`{(r.get('identifier') or '?')[:36]}`",
            ])
    L.append(md_table(["Principal", "Type", "Identifier"], admin_rows))
    L.append("")
    L.append("## ⚠️ Service Principals — concentrated power")
    L.append("")
    L.append(md_table(
        ["SPN", "Object ID", "Inferred purpose", "Risk"],
        [
            ["`onelakedev-connector`", "`558ce77f-...`", "OneLake access bridge for connectors", "🟠 Wide blast radius"],
            ["`AshleyBIApplicationDev`", "`dcf4eadd-...`", "Dev-tier app (used by dev jobs)", "✅ Acceptable for Dev"],
            ["`AshleyBIApplicationProd`", "`2b8e5809-...`", "Prod app (used by prod jobs) — **Admin on Dev WS**", "🔴 Cross-env contamination (C2)"],
        ],
    ))
    L.append("")
    L.append("**Action item:** treat `AshleyBIApplicationProd` as security-critical. Rotate, scope-down, or remove.")
    L.append("")
    L.append("## Capacity & identity")
    L.append("")
    L.append(md_table(
        ["Field", "Value"],
        [
            ["Capacity ID", "`30d06c17-b0f4-4709-9a20-e29c96e8863e`"],
            ["Region", "East US"],
            ["Tier", "Dedicated, Large dataset format"],
            ["SKU", "Not visible from current scope (capacity owned by another subscription)"],
            ["Workspace identity (SPN)", "`14bfa211-3cab-40ae-bfd3-23c853ef619f`"],
        ],
    ))
    L.append("")
    L.append("---")
    write(DOCS / "07-permissions" / "README.md", "\n".join(L))


# =============================================================
# 08 Operations
# =============================================================

def build_operations():
    L = []
    L.append("# 📊 08 — Operations")
    L.append("")
    L.append("[← Root](../../README.md)")
    L.append("")
    L.append("## Run reality")
    L.append("")
    L.append("![Run reality](../../images/08-run-reality.svg)")
    L.append("")
    active_items = []
    dormant_items = []
    for name, info in runs.items():
        rlist = info.get("runs") if isinstance(info, dict) else None
        if isinstance(rlist, list) and rlist:
            sorted_r = sorted(rlist, key=lambda r: r.get("startTimeUtc") or "", reverse=True)
            last = sorted_r[0]
            active_items.append({
                "name": name,
                "type": info.get("type", "?"),
                "runs": len(rlist),
                "last": last.get("startTimeUtc", "")[:19],
                "status": last.get("status", "?"),
            })
        else:
            dormant_items.append({"name": name, "type": info.get("type", "?")})

    L.append(f"- **{len(active_items)}** items have run history in API window")
    L.append(f"- **{len(dormant_items)}** items dormant (never ran or older than window)")
    L.append("")
    L.append("## ✅ Active items")
    L.append("")
    if active_items:
        active_items.sort(key=lambda x: -x["runs"])
        L.append(md_table(
            ["Item", "Type", "# Runs", "Last run", "Last status"],
            [[f"`{a['name']}`", a["type"], a["runs"], a["last"], a["status"]] for a in active_items],
        ))
    L.append("")
    L.append("## 💤 Dormant items")
    L.append("")
    L.append(f"All other {len(dormant_items)} orchestration items have no recent run history. See [run-history.md](run-history.md) for full list.")
    L.append("")
    L.append("## 🐍 Spark Environments")
    L.append("")
    L.append(md_table(
        ["Env", "Runtime", "Pool", "Dynamic alloc", "Libraries", "Last published"],
        [
            ["`Env01`", "**1.2** ⚠️", "Starter Pool 8c/56g", "1–9", "`pandas==2.2.2`", "2024-04-24"],
            ["`Dev`", "**1.3**", "Starter Pool 8c/56g", "1–9", "(none)", "2025-06-10"],
        ],
    ))
    L.append("")
    L.append("**Risk C12**: Env runtime drift — `Env01` on 1.2 vs `Dev` on 1.3.")
    L.append("")
    L.append("## Sub-pages")
    L.append("")
    L.append("- [Run history](run-history.md) — full per-item run breakdown")
    L.append("- [Monitoring](monitoring.md) — `Source_EDW_Check_Test` daily + alert pipelines")
    L.append("- [Environments](environments.md) — Spark configs detail")
    L.append("")
    L.append("---")
    write(DOCS / "08-operations" / "README.md", "\n".join(L))

    # Run history
    L = []
    L.append("# Run History (full)")
    L.append("")
    L.append("[← Operations](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## Active (3)")
    L.append("")
    if active_items:
        active_items.sort(key=lambda x: -x["runs"])
        L.append(md_table(
            ["Item", "Type", "# Runs", "Last run", "Last status"],
            [[f"`{a['name']}`", a["type"], a["runs"], a["last"], a["status"]] for a in active_items],
        ))
    L.append("")
    L.append(f"## Dormant ({len(dormant_items)})")
    L.append("")
    by_type = defaultdict(list)
    for d in dormant_items:
        by_type[d["type"]].append(d["name"])
    for t, names in sorted(by_type.items()):
        L.append(f"### {t} ({len(names)})")
        L.append("")
        for n in sorted(names):
            L.append(f"- `{n}`")
        L.append("")
    L.append("---")
    write(DOCS / "08-operations" / "run-history.md", "\n".join(L))

    # Monitoring
    L = []
    L.append("# Monitoring System")
    L.append("")
    L.append("[← Operations](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## How monitoring works")
    L.append("")
    L.append(mermaid("""sequenceDiagram
    participant SP as ETL Stored Proc
    participant AL as Performance_Logs.EmailQueue
    participant ALERT as Alert_FabricTables
    participant SLA as PL_SLA_Breach
    participant CHECK as Source_EDW_Check_Test (daily 03:50 UTC)
    participant O365 as Office365 Outlook

    Note over SP,AL: Any ETL proc that fails or<br/>misses SLA writes a row.
    SP->>AL: INSERT row (Failed/Pending)
    CHECK->>SP: Truncate Bronze counts
    CHECK->>SP: usp_GenerateEmailHTML_DimCountDifference
    SP-->>AL: INSERT count-diff rows
    CHECK->>O365: Send per-row emails
    ALERT->>SP: usp_DataWarehouseDataFeedAlert_Fabric
    ALERT->>AL: SELECT WHERE status=Failed/NULL
    loop for each unsent
        ALERT->>O365: Send email
        ALERT->>AL: usp_EmailQueue_MarkSent
    end
    SLA->>SP: usp_DataWarehouseSLAAlert_Fabric
    SLA->>O365: Send to hardcoded DL"""))
    L.append("")
    L.append("**Key facts:**")
    L.append("- `Source_EDW_Check_Test` is the **only consistently-running** pipeline (daily 03:50 UTC)")
    L.append("- `Alert_FabricTables_EnterpriseData` and `PL_SLA_Breach_EnterpriseData` are **manually triggered** today")
    L.append("- `FabricSLA_Trigger_EnterpriseData` was supposed to wrap them but is empty (risk C6)")
    L.append("- The `f7ca7cad-...` Office365Email connection failed with `DMTS_EntityNotFoundOrUnauthorized` on a manual run — confirm scheduled email actually delivers (C24)")
    L.append("")
    L.append("---")
    write(DOCS / "08-operations" / "monitoring.md", "\n".join(L))

    # Environments
    L = []
    L.append("# Spark Environments")
    L.append("")
    L.append("[← Operations](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## `Env01` (`9d2b5e1b-...`)")
    L.append("")
    L.append(md_table(
        ["Field", "Value"],
        [
            ["Runtime", "**1.2** ⚠️ outdated"],
            ["Pool", "Starter Pool 8c/56g"],
            ["Dynamic alloc", "1-9 executors"],
            ["Libraries", "`pandas==2.2.2`"],
            ["Last published", "2024-04-24"],
        ],
    ))
    L.append("")
    L.append("## `Dev` (`79333c60-...`)")
    L.append("")
    L.append(md_table(
        ["Field", "Value"],
        [
            ["Runtime", "**1.3** current"],
            ["Pool", "Starter Pool 8c/56g"],
            ["Dynamic alloc", "1-9 executors"],
            ["Libraries", "(none published)"],
            ["Last published", "2025-06-10"],
        ],
    ))
    L.append("")
    L.append("**Risk C12:** Notebooks may inadvertently target the older `Env01`. Migrate `Env01` to runtime 1.3 or document why the freeze.")
    L.append("")
    L.append("---")
    write(DOCS / "08-operations" / "environments.md", "\n".join(L))


# =============================================================
# 09 Risks
# =============================================================

RISKS = [
    ("C1", "🔴 Critical", "Security", "Plaintext SP secret `<REDACTED-rotate-pending>` in `MetaData-Pull` cell 1 (AshleyBI app, tenant `5a9d9cfd-...`)", "MetaData-Pull notebook", "Rotate immediately. Cells 2/3 use Key Vault correctly; delete cell 1"),
    ("C2", "🔴 High", "Security", "`AshleyBIApplicationProd` SPN holds Admin on Dev workspace", "permissions", "Remove or downgrade to Contributor"),
    ("C3", "🔴 High", "Architecture", "`Quality_Warehouse` (PROD tier) is empty (0 tables/procs)", "Quality_Warehouse", "Either build or remove"),
    ("C25", "🔴 High", "Architecture", "5.92B rows in Centralized_Lakehouse are shortcut-backed (not real DEV data)", "Centralized_Lakehouse", "Document, ensure team doesn't write back"),
    ("C28", "🔴 High", "Security", "`RadarSync_Test` mounts entire trusted+raw ADLS zones — broad scope", "RadarSync_Test", "Restrict scope or audit access"),
    ("C26", "🟠 Medium", "Operations", "38/41 orchestration items have no recent run history", "run history", "Audit dormants; remove unused"),
    ("C27", "🟠 Medium", "Lineage", "4 unresolvable lakehouses referenced by notebooks", "notebooks", "Document or remove broken refs"),
    ("C4", "🟠 Medium", "Maintainability", "3 near-duplicate `Vers 5` notebooks with subtle differences and stale lakehouse GUIDs", "Vers5 trio", "Collapse to one parameterized notebook"),
    ("C5", "🟠 Medium", "Reliability", "`Retail_Prod_To_Dev_DataBackFill` snapshot Inactive; failures stable since 2026-04-29", "Retail_Prod_To_Dev_DataBackFill", "Audit; fix and re-enable or delete"),
    ("C6", "🟠 Medium", "Orchestration", "`FabricSLA_Trigger_EnterpriseData` empty (intended scheduler wrapper)", "FabricSLA_Trigger_EnterpriseData", "Build or delete"),
    ("C7", "🟠 Medium", "Notification", "Hardcoded email recipient in `PL_SLA_Breach`", "PL_SLA_Breach", "Move to EnvironmentControl config table"),
    ("C8", "🟠 Medium", "Orchestration", "`Reflex 2024-05-29` cannot export — likely abandoned", "Reflex", "Confirm and delete"),
    ("C24", "🟠 Medium", "DQ", "Office365Email connection `f7ca7cad-...` failed `DMTS_EntityNotFoundOrUnauthorized` on manual run", "Source_EDW_Check_Test", "Confirm scheduled branch actually delivers"),
    ("C9", "🟡 Low", "Architecture", "Stranded business tables in ETL_Framework (Manufacturing_Maximo.Fedex etc.)", "ETL_Framework", "Move to domain WHs"),
    ("C10", "🟡 Low", "Maintainability", "4 clones of TableDictionary (`_clone`, `_edw_1`, `_Test`, `_Security`)", "ETL_Framework", "Consolidate; document authoritative copy"),
    ("C11", "🟡 Low", "Cleanup", "Two empty Dataflow staging LH+WH pairs", "DataflowsStaging*", "Delete after confirming Dataflow Test empty"),
    ("C12", "🟡 Low", "Compatibility", "Env runtime drift: Env01 on 1.2, Dev on 1.3", "environments", "Migrate Env01 to 1.3"),
    ("C13", "🟡 Low", "Cleanup", "5 empty test pipelines", "test pipelines", "Delete"),
    ("C14", "🟡 Low", "Naming", "`test` and `pipeline1` are real cross-WS PROD copies", "test+pipeline1", "Rename to descriptive names"),
    ("C15", "🟡 Low", "Notebooks", "`Notebook 13` runs `sc.addPyFile('https://raw.githubusercontent.com/microsoft/fabric-samples/.../util.py')`", "Notebook 13", "Pin to commit SHA or vendor in Environment library"),
    ("C16", "🟡 Low", "Notebooks", "`Vers 5` references stale lakehouse GUID `75f83a27-...`", "Vers 5", "Update or remove"),
    ("C17", "🟡 Low", "Notebooks", "`Sys_Data_pull` cell 1 saveAsTable contract mismatch", "Sys_Data_pull", "Use cell 4's mature impl"),
    ("C18", "🟡 Low", "Notebooks", "`delta_table_path2` undefined in `Rename column names`", "Rename column names", "Fix or remove"),
    ("C19", "🟡 Low", "Procs", "13 variants of `Usp_CreateTableFromParquet*`", "ETL_Framework", "Consolidate; deprecate dead variants"),
    ("C20", "🟡 Low", "Centralized_LH", "`Retail_Corporate` and `Retail_Corporate_Prod` 1:1 mirror at 5.92B rows", "Centralized_Lakehouse", "Identify canonical; delete duplicate"),
    ("C21", "🟡 Low", "Permissions", "12 individual user Admins on Dev workspace + 1 broad group", "permissions", "Adopt least-privilege"),
    ("C22", "🟡 Low", "Descriptions", "70/71 items have empty descriptions", "all items", "Add description for production items"),
    ("C23", "🟡 Low", "Test sandbox", "`Test_Owneraccess` warehouse left over from permissions probe", "Test_Owneraccess", "Delete"),
]


def build_risks():
    L = []
    L.append("# ⚠️ 09 — Risks (28 total)")
    L.append("")
    L.append("[← Root](../../README.md)")
    L.append("")
    L.append("## Distribution")
    L.append("")
    L.append("![Risk matrix](../../images/09-risk-matrix.svg)")
    L.append("")
    L.append("```")
    L.append("🔴 Critical:  █ 1     (security)")
    L.append("🔴 High:      ████ 4  (security/architecture)")
    L.append("🟠 Medium:    ████████ 8 (orchestration/maintainability)")
    L.append("🟡 Low:       ███████████████ 15 (cleanup/naming)")
    L.append("```")
    L.append("")
    L.append("## Sub-pages")
    L.append("")
    L.append("- [Critical & High (5)](critical-and-high.md) — must address")
    L.append("- [Medium (8)](medium.md)")
    L.append("- [Low (15)](low.md)")
    L.append("")
    L.append("## Full register")
    L.append("")
    rows = []
    for code, sev, cat, issue, target, action in RISKS:
        rows.append([code, sev, cat, issue, f"`{target}`", action])
    L.append(md_table(["#", "Severity", "Category", "Issue", "Target", "Action"], rows))
    L.append("")
    L.append("---")
    write(DOCS / "09-risks" / "README.md", "\n".join(L))

    # Critical & High
    L = []
    L.append("# 🔴 Critical & High Risks (5)")
    L.append("")
    L.append("[← Risks](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("These need immediate attention.")
    L.append("")
    for code, sev, cat, issue, target, action in RISKS:
        if "🔴" in sev:
            L.append(f"## {code}: {sev}")
            L.append("")
            L.append(f"**Category:** {cat}")
            L.append(f"**Target:** `{target}`")
            L.append("")
            L.append(f"**Issue:** {issue}")
            L.append("")
            L.append(f"**Action:** {action}")
            L.append("")
            L.append("---")
            L.append("")
    write(DOCS / "09-risks" / "critical-and-high.md", "\n".join(L))

    # Medium
    L = []
    L.append("# 🟠 Medium Risks (8)")
    L.append("")
    L.append("[← Risks](README.md) · [← Root](../../README.md)")
    L.append("")
    rows = []
    for code, sev, cat, issue, target, action in RISKS:
        if "Medium" in sev:
            rows.append([code, cat, issue, f"`{target}`", action])
    L.append(md_table(["#", "Category", "Issue", "Target", "Action"], rows))
    L.append("")
    L.append("---")
    write(DOCS / "09-risks" / "medium.md", "\n".join(L))

    # Low
    L = []
    L.append("# 🟡 Low Risks (15)")
    L.append("")
    L.append("[← Risks](README.md) · [← Root](../../README.md)")
    L.append("")
    rows = []
    for code, sev, cat, issue, target, action in RISKS:
        if "Low" in sev:
            rows.append([code, cat, issue, f"`{target}`", action])
    L.append(md_table(["#", "Category", "Issue", "Target", "Action"], rows))
    L.append("")
    L.append("---")
    write(DOCS / "09-risks" / "low.md", "\n".join(L))


# =============================================================
# 99 Reference
# =============================================================

def build_reference():
    # README
    L = []
    L.append("# 📚 99 — Reference")
    L.append("")
    L.append("[← Root](../../README.md)")
    L.append("")
    L.append("## Sub-pages")
    L.append("")
    L.append("- [Glossary](glossary.md) — Fabric concepts + Ashley domain terms")
    L.append("- [ID Reference](id-reference.md) — every item GUID with name")
    L.append("- [File Index](file-index.md) — what's in this repo")
    L.append("- [Methodology](methodology.md) — how data was scanned")
    L.append("")
    L.append("---")
    write(DOCS / "99-reference" / "README.md", "\n".join(L))

    # Glossary
    L = []
    L.append("# 📚 Glossary")
    L.append("")
    L.append("[← Reference](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## Fabric concepts")
    L.append("")
    L.append(md_table(["Term", "Definition"], [
        ["**Workspace**", "Logical container in Microsoft Fabric grouping items under one capacity"],
        ["**Capacity**", "Compute SKU billed per-hour. East US dedicated 'Large dataset format' for this WS"],
        ["**Warehouse (Fabric)**", "T-SQL relational engine on top of OneLake parquet. Supports stored procs, views, MERGE, COPY INTO. Read/write"],
        ["**Lakehouse**", "Delta Lake tables + Files folder on OneLake. Has auto-generated SQL Endpoint (read-only T-SQL view)"],
        ["**Schema-enabled Lakehouse**", "Newer Fabric feature — supports SQL `[schema].[table]` namespace (legacy LH only `dbo`)"],
        ["**OneLake**", "Unified storage (ADLS Gen2 underneath) for all Fabric items. URL pattern `abfss://<wsid>@onelake.dfs.fabric.microsoft.com/<itemid>/Tables/...`"],
        ["**Shortcut**", "OneLake symbolic link — point a path in this LH/WH to data in another LH/WH (cross-WS) or external storage. No data copy"],
        ["**SQL Endpoint**", "Auto-generated read-only T-SQL surface for a Lakehouse"],
        ["**Data Pipeline**", "Visual ETL workflow with activities (Copy, Lookup, ForEach, Script, Notebook, IfCondition, ExecutePipeline). Similar to ADF pipeline"],
        ["**Mounted DataFactory**", "Reference link to an existing Azure Data Factory — its pipelines surface inside Fabric without duplication"],
        ["**MirroredAzureDatabricksCatalog**", "Live read-only mirror of a Databricks Unity Catalog into Fabric OneLake. Supports Full or Selective mode + autoSync"],
        ["**Dataflow Gen2**", "Power Query M-based no-code data prep, with auto-staging Lakehouse + Warehouse"],
        ["**Reflex (Activator)**", "Event-driven trigger that watches data and fires actions"],
        ["**Spark Environment**", "Reusable compute config (runtime version, pool, libraries) for Spark notebooks/jobs"],
        ["**Semantic Model**", "Power BI dataset (renamed). Tabular data model with measures/relationships, queryable via DAX"],
    ]))
    L.append("")
    L.append("## Ashley Furniture domain terms")
    L.append("")
    L.append(md_table(["Term", "Meaning"], [
        ["**EDW**", "Enterprise Data Warehouse — legacy on-prem SQL Server `ASHLEY_EDW_DEV` / `Ashley_Edw` (Synapse)"],
        ["**AFI**", "Ashley Furniture Industries — corp brand. `MasterData_ItemMaster_AFI` = item master domain"],
        ["**UKG**", "UKG Pro / Kronos — HR + workforce management SaaS. Schemas `MasterData_HR_UKG_*`"],
        ["**Maximo**", "IBM Maximo — manufacturing / asset management. Schema `Manufacturing_Maximo`"],
        ["**AshleyServiceNow**", "ServiceNow ITSM. Tables `Retail_DW.AshleyServiceNow*`"],
        ["**ADS**", "Ashley Data Source / Ad Services — Google Analytics processed feeds. Subpath `MasterData/ADS/GoogleAnalytics_Processed/Drive4Ashley*`"],
        ["**QTIL**", "Quality / supplier-related domain. Subpath `MasterData/QTIL/VVSSku`"],
        ["**Storis_DW**", "Storis ERP-related schema in `Commissions_Prototype`"],
        ["**RadarSync**", "Internal sync mechanism (`UpdateLog_RadarSync` table)"],
        ["**EDWELoader**", "EDW-to-Fabric loader nomenclature (EDW2FabricLoader pipeline)"],
    ]))
    L.append("")
    L.append("## Naming conventions observed")
    L.append("")
    L.append(md_table(["Pattern", "Meaning"], [
        ["`_AGR`, `_DSG`, `_Wrk`, `_Enh` suffixes", "UKG HR data stages (Agreement/Design/Working/Enhanced)"],
        ["`_Wrk` schema/views", "'Working set' views — feed `usp_RefreshCuratedTableFromView` procs"],
        ["`Retail_Corporate` vs `Retail_Corporate_Prod`", "Twin schemas — both shortcuts to PROD `Retail_Corporate` (not duplicated storage)"],
        ["`Vers 5`, `Vers 5 Copy`, `Vers 5new`", "Notebook duplicates indicating editing without consolidation"],
        ["`Usp_*` PascalCase", "Stored procedure"],
        ["`usp_*` lowercase", "Stored procedure (mixed convention)"],
        ["`_clone`, `_Test`, `_Security`, `_edw_1`", "TableDictionary clones — sandbox/security/legacy snapshots"],
        ["`Files/<GUID>`", "Fabric-internal physical backing for warehouse tables (NOT user shortcuts)"],
    ]))
    L.append("")
    L.append("---")
    write(DOCS / "99-reference" / "glossary.md", "\n".join(L))

    # ID reference
    L = []
    L.append("# 🆔 ID Reference")
    L.append("")
    L.append("[← Reference](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("Every item in workspace `EnterpriseData-Dev` with its GUID.")
    L.append("")
    for type_name, items in inv.items():
        if not items:
            continue
        L.append(f"## {type_name} ({len(items)})")
        L.append("")
        L.append(md_table(
            ["Name", "ID"],
            [[f"`{it['name']}`", f"`{it['id']}`"] for it in sorted(items, key=lambda x: x["name"])],
        ))
        L.append("")
    L.append("---")
    write(DOCS / "99-reference" / "id-reference.md", "\n".join(L))

    # File index
    L = []
    L.append("# 📁 File Index")
    L.append("")
    L.append("[← Reference](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## Repo structure")
    L.append("")
    L.append("```")
    L.append("EnterpriseData-Dev-Docs/")
    L.append("├── README.md                            ← landing")
    L.append("├── docs/                                ← this folder")
    L.append("│   ├── 01-introduction.md")
    L.append("│   ├── 02-storage/")
    L.append("│   ├── 03-logic/")
    L.append("│   ├── 04-orchestration/")
    L.append("│   ├── 05-data-flow/")
    L.append("│   ├── 06-cross-workspace/")
    L.append("│   ├── 07-permissions/")
    L.append("│   ├── 08-operations/")
    L.append("│   ├── 09-risks/")
    L.append("│   └── 99-reference/")
    L.append("├── images/                              ← rendered Mermaid SVG")
    L.append("├── data/                                ← raw scan JSONs")
    L.append("│   ├── 00-inventory-with-ids.json")
    L.append("│   ├── 01-permissions-raw.json")
    L.append("│   ├── 02-lakehouses-raw.json (4.6 MB)")
    L.append("│   ├── 03-warehouses-raw.json (2.2 MB)")
    L.append("│   ├── 04-notebooks-raw.json")
    L.append("│   ├── 05-orchestration-raw.json")
    L.append("│   ├── 06-procs-raw.json (1.5 MB)")
    L.append("│   ├── 07-views-raw.json")
    L.append("│   ├── 08-shortcuts-files-raw.json")
    L.append("│   ├── 09-external-guids.json")
    L.append("│   ├── 10-runs-raw.json")
    L.append("│   ├── 11-web-data.json")
    L.append("│   ├── notebooks/   (18 .ipynb + 18 .py)")
    L.append("│   └── pipelines/   (22 .json)")
    L.append("├── scripts/                             ← scan + build")
    L.append("│   ├── _scan_lakehouses.py")
    L.append("│   ├── _scan_procs_views.py")
    L.append("│   ├── _scan_shortcuts_files.py")
    L.append("│   ├── _scan_pipeline_runs.py")
    L.append("│   ├── _sql_helper.py")
    L.append("│   └── _build_docs.py                   ← regen this repo")
    L.append("└── _archive/                            ← old presentation artifacts (preserved)")
    L.append("```")
    L.append("")
    L.append("---")
    write(DOCS / "99-reference" / "file-index.md", "\n".join(L))

    # Methodology
    L = []
    L.append("# 🔬 Methodology")
    L.append("")
    L.append("[← Reference](README.md) · [← Root](../../README.md)")
    L.append("")
    L.append("## How data was collected")
    L.append("")
    L.append(md_table(["Phase", "Approach"], [
        ["Inventory + IDs", "`GET https://api.fabric.microsoft.com/v1/workspaces/{ws}/items` → `00-inventory-with-ids.json`"],
        ["Permissions", "Power BI `/myorg/groups/{id}/users` (Fabric `/v1/workspaces/{id}/roleAssignments` returned 403 in this scope)"],
        ["Per-item metadata", "`GET /v1/workspaces/{ws}/items/{itemId}` (no createdDate/modifiedDate exposed)"],
        ["Warehouse + Lakehouse SQL", "`pyodbc` over ODBC Driver 18 for SQL Server with AAD access token. All queries READ-ONLY (`SELECT`, `INFORMATION_SCHEMA`, `COUNT_BIG`)"],
        ["Pipeline definitions", "`POST /v1/workspaces/{ws}/dataPipelines/{id}/getDefinition` then base64-decode `definition.parts[].payload`"],
        ["Notebook definitions", "`POST /v1/workspaces/{ws}/notebooks/{id}/getDefinition?format=ipynb` then base64-decode parts"],
        ["Mirror config", "`GET /v1/workspaces/{ws}/mirroredAzureDatabricksCatalogs/{id}` plus status endpoint"],
        ["Mounted ADF", "`GET /v1/workspaces/{ws}/mountedDataFactories/{id}`"],
        ["Reflex", "`getDefinition` failed with `Activator_Export_FailedToExportActivator_ReflexBackendError`"],
        ["Stored procs + views", "`SELECT m.definition FROM sys.sql_modules m JOIN sys.procedures/views`"],
        ["Shortcuts", "`GET /v1/workspaces/{ws}/items/{itemId}/shortcuts` per item"],
        ["Files/ folder enum", "OneLake DFS `?resource=filesystem&recursive=false&directory=Files` recursively"],
        ["Run history", "`GET /v1/workspaces/{ws}/items/{itemId}/jobs/instances?$top=30` per item"],
    ]))
    L.append("")
    L.append("## Constraints encountered")
    L.append("")
    L.append("- Item-level `createdDate` / `modifiedDate` / `lastModifiedBy` are **not exposed** by the Fabric `/v1/items/{id}` endpoint")
    L.append("- Fabric Lakehouse SQL endpoints return **0** from `sys.partitions.rows` (used `COUNT_BIG(*)` instead)")
    L.append("- Workspace `13eefa5e-...` returned 403 Forbidden when listing items")
    L.append("- 4 lakehouse GUIDs referenced by notebooks but not in any accessible workspace")
    L.append("")
    L.append("## Confidence tagging")
    L.append("")
    L.append("Per the SUPER RULE §0 zero-hallucination guideline:")
    L.append("- **[Verified]** — observed directly in data/code")
    L.append("- **[Likely]** — strong inference from context")
    L.append("- **[Speculation]** — guess, needs owner confirmation")
    L.append("")
    L.append("---")
    write(DOCS / "99-reference" / "methodology.md", "\n".join(L))


# =============================================================
# Main
# =============================================================

def main():
    print("Building EnterpriseData-Dev-Docs/...")
    build_root_readme()
    build_introduction()

    build_storage_readme()
    build_warehouses_readme()
    build_warehouse_page("ETL_Framework", "etl-framework", etl_framework_extra())
    for nm in ("Source_Data", "Centralized_Warehouse", "Retail_Warehouse",
               "Wholesale_Warehouse", "MasterData_Warehouse", "Distribution_Warehouse",
               "Quality_Warehouse"):
        build_warehouse_page(nm, nm.lower().replace("_", "-"))

    build_lakehouses_readme()
    build_lakehouse_page("Centralized_Lakehouse", "centralized-lakehouse")
    build_lakehouse_page("A_Developement", "a-developement")
    build_lakehouse_page("RadarSync_Test", "radarsync-test")

    build_logic_readme()
    build_logic_procs()
    build_logic_views()
    build_logic_notebooks()

    build_orch_readme()
    build_orch_pipelines()
    build_orch_mirror()
    build_orch_adf()
    build_orch_dataflow()
    build_orch_reflex()

    build_data_flow()
    build_data_flow_legs()

    build_cross_ws()

    build_permissions()

    build_operations()

    build_risks()

    build_reference()

    print("\nDone! Now render Mermaid diagrams to images/ via _render_images.py.")


if __name__ == "__main__":
    main()
