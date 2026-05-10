#!/usr/bin/env python3
"""Extract first Mermaid block from selected docs + render via mmdc to images/."""
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
IMAGES = REPO / "images"
TMP = Path("/tmp")

# (source-md, output-name, fallback-mermaid-if-not-found)
TARGETS = [
    (DOCS / "01-introduction.md", "01-high-level-architecture", None),
    (DOCS / "02-storage" / "README.md", "02-storage-map", None),
    (DOCS / "05-data-flow" / "README.md", "05-data-flow", None),
    (DOCS / "06-cross-workspace" / "README.md", "06-cross-ws", None),
    (DOCS / "07-permissions" / "README.md", "07-permissions", None),
]

# Standalone diagrams (not from a doc)
EXTRA = {
    "05-data-flow": """flowchart LR
    classDef src fill:#e8f4fd,stroke:#3a8;
    classDef ing fill:#fef3c7,stroke:#d97706;
    classDef bronze fill:#dbeafe,stroke:#2563eb;
    classDef silver fill:#e0e7ff,stroke:#4f46e5;
    classDef gold fill:#fce7f3,stroke:#db2777;
    classDef ext fill:#fed,stroke:#c93;

    EDW[ASHLEY_EDW_DEV]:::src
    SYN[Synapse Ashley_Edw]:::src
    DBX[Databricks UC edw_dev]:::src
    SAAS[UKG / AFI / Maximo / SNow / GA]:::src
    ADLS[ADLS Gen2 ashleydevlake]:::ext
    PROD[PROD WS ce4e6503]:::ext

    PIPE[16 ingestion pipelines]:::ing
    ADF[Mounted ADF]:::ing
    NB[Vers5 notebooks]:::ing
    MIRROR[edw_dev Mirror]:::ing

    SD[Source_Data WH<br/>BRONZE 636 tables]:::bronze
    RW[Retail_Warehouse<br/>198 tables 146 procs]:::silver
    WW[Wholesale_Warehouse<br/>209 tables]:::silver
    MD[MasterData_Warehouse]:::silver
    DW[Distribution_Warehouse]:::silver
    CW[Centralized_Warehouse]:::gold
    CL[Centralized_Lakehouse<br/>shortcut to PROD]:::gold

    EDW --> PIPE
    SYN --> PIPE
    SAAS --> ADF
    DBX --> MIRROR
    ADLS --> SD
    PROD --> CL

    PIPE --> SD
    ADF --> SD
    NB --> CL
    MIRROR --> CL

    SD --> RW
    SD --> WW
    SD --> MD
    SD --> DW

    RW --> CW
    WW --> CW
    MD --> CW
    DW --> CW

    CW --> PBI[Power BI]
    CL --> PBI""",
    "08-run-reality": """flowchart LR
    classDef active fill:#86efac,stroke:#15803d,color:#14532d;
    classDef dormant fill:#fed7aa,stroke:#c2410c,color:#7c2d12;
    classDef broken fill:#fecaca,stroke:#dc2626,color:#7f1d1d;

    A1[Source_EDW_Check_Test<br/>64 runs · daily 03:50 UTC]:::active
    A2[Retail_Prod_To_Dev_DataBackFill<br/>58 runs · idle since 2026-04-29]:::active
    A3[Notebook 13<br/>1 run · 2026-04-21]:::active
    D[38 dormant items<br/>15 ETL pipelines · 17 notebooks ·<br/>1 dataflow · 1 reflex]:::dormant
    B[Reflex broken<br/>getDefinition error]:::broken
    F[FabricSLA_Trigger_EnterpriseData<br/>EMPTY wrapper]:::broken""",
    "09-risk-matrix": """quadrantChart
    title Risk severity x category
    x-axis Low impact --> High impact
    y-axis Low effort to fix --> High effort to fix
    quadrant-1 Plan
    quadrant-2 Do now
    quadrant-3 Defer
    quadrant-4 Quick wins
    C1 plaintext SP secret: [0.95, 0.15]
    C2 Prod SPN admin: [0.85, 0.2]
    C3 Quality WH empty: [0.7, 0.6]
    C25 shortcut data: [0.7, 0.7]
    C28 RadarSync ADLS: [0.75, 0.4]
    C5 backfill failures: [0.55, 0.5]
    C6 SLA wrapper empty: [0.5, 0.3]
    C7 hardcoded recipient: [0.35, 0.2]
    C8 Reflex broken: [0.3, 0.15]
    C4 Vers5 dup: [0.45, 0.4]
    C19 13 parquet variants: [0.4, 0.7]"""
}


def extract_first_mermaid(md_path: Path):
    txt = md_path.read_text()
    m = re.search(r"```mermaid\n(.*?)\n```", txt, re.DOTALL)
    if m:
        return m.group(1)
    return None


def render(name, mmd_content):
    mmd_file = TMP / f"_{name}.mmd"
    svg_out = IMAGES / f"{name}.svg"
    mmd_file.write_text(mmd_content)
    print(f"  Rendering {name}.svg ...")
    r = subprocess.run(
        ["mmdc", "-i", str(mmd_file), "-o", str(svg_out), "-b", "white", "--quiet"],
        capture_output=True, text=True, timeout=90,
    )
    if r.returncode == 0:
        print(f"    ✓ {svg_out.relative_to(REPO)}")
    else:
        print(f"    ✗ FAILED: {r.stderr[:200]}")


def main():
    IMAGES.mkdir(exist_ok=True)
    for src, name, fallback in TARGETS:
        mmd = extract_first_mermaid(src) if src.exists() else None
        if mmd is None and fallback:
            mmd = fallback
        if mmd is None:
            print(f"  ⚠️  no Mermaid in {src.name}, skipping")
            continue
        render(name, mmd)
    for name, mmd in EXTRA.items():
        render(name, mmd)


if __name__ == "__main__":
    main()
