#!/usr/bin/env python3
"""Patch root README.md + sub-section READMEs to link to new detail pages."""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"


def patch(path: Path, marker: str, insertion: str):
    if not path.exists():
        return
    txt = path.read_text()
    if insertion.strip() in txt:
        return  # already patched
    if marker in txt:
        new = txt.replace(marker, marker + insertion)
        path.write_text(new)
        print(f"  ✓ patched {path.relative_to(REPO)}")
    else:
        # Append at end
        with open(path, "a") as f:
            f.write(insertion)
        print(f"  ✓ appended to {path.relative_to(REPO)}")


# 1. Root README — add new sub-pages section
root = REPO / "README.md"
addition = """

## 🔬 NEW: Detail layer (v2 — added 2026-05-10)

The repo now ships **per-item deep-dive pages** beyond the high-level overview:

| Detail layer | Pages | Description |
|---|---:|---|
| [📜 Per-pipeline walkthroughs](docs/04-orchestration/pipelines/README.md) | 22 | Activity tree + source/sink mapping + parameters + run history per pipeline |
| [⚙️ Per-proc narrative](docs/03-logic/procs/README.md) | 60 | Inputs/outputs detected, narrative explanation, code excerpt for top procs |
| [🔍 Per-table lineage](docs/05-data-flow/tables/README.md) | 50 | Top tables with writers/readers + Mermaid lineage subgraph |
| [🕸️ Dependency graphs](docs/05-data-flow/dependency-graphs.md) | 1 | Proc call graph + pipeline→proc edges |
| [🔌 Connections](docs/06-cross-workspace/connections.md) | 1 | 12 data sources (SharePoint, SQL, Lakehouse) |
| [⚙️ Workspace settings](docs/08-operations/workspace-settings.md) | 1 | Spark settings + capacity + folders |

> **Navigate top-down:** start with [01-introduction.md](docs/01-introduction.md), drill via category READMEs, end at detail pages above.
"""
patch(root, "## 🔧 Regenerate", addition + "\n")

# 2. docs/03-logic/README.md — add link to procs/ folder
addition = """
## 🔬 Detail pages
- [⚙️ Per-proc narrative pages (60)](procs/README.md) — top stored procedures with inputs/outputs/code
"""
patch(DOCS / "03-logic" / "README.md", "## 📑 Sub-pages", addition + "\n")

# 3. docs/04-orchestration/README.md — add link to pipelines/ folder
addition = """
## 🔬 Detail pages
- [📜 Per-pipeline walkthroughs (22)](pipelines/README.md) — activity-by-activity per pipeline
"""
patch(DOCS / "04-orchestration" / "README.md", "## 📑 Sub-pages", addition + "\n")

# 4. docs/05-data-flow/README.md — add link to tables/ + dependency-graphs
addition = """
## 🔬 Detail pages
- [🔍 Per-table lineage (50)](tables/README.md) — top tables with writers/readers/Mermaid
- [🕸️ Dependency graphs](dependency-graphs.md) — proc call graph + pipeline→proc edges
"""
patch(DOCS / "05-data-flow" / "README.md", "## Per-leg pages", addition + "\n")

# 5. docs/06-cross-workspace/README.md — add link to connections
addition = """
- [🔌 Connections (12)](connections.md) — data sources (SharePoint, SQL, Lakehouse)
"""
patch(DOCS / "06-cross-workspace" / "README.md", "- [Inaccessible references]", addition)

# 6. docs/08-operations/README.md — add link to workspace-settings
addition = """
- [⚙️ Workspace settings](workspace-settings.md) — Spark + capacity + folders
"""
patch(DOCS / "08-operations" / "README.md", "- [Environments](environments.md)", addition)

print("\nDone patching navigation.")
