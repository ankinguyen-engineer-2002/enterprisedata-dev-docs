# 📁 File Index

[← Reference](README.md) · [← Root](../../README.md)

## Repo structure

```
EnterpriseData-Dev-Docs/
├── README.md                            ← landing
├── docs/                                ← this folder
│   ├── 01-introduction.md
│   ├── 02-storage/
│   ├── 03-logic/
│   ├── 04-orchestration/
│   ├── 05-data-flow/
│   ├── 06-cross-workspace/
│   ├── 07-permissions/
│   ├── 08-operations/
│   ├── 09-risks/
│   └── 99-reference/
├── images/                              ← rendered Mermaid SVG
├── data/                                ← raw scan JSONs
│   ├── 00-inventory-with-ids.json
│   ├── 01-permissions-raw.json
│   ├── 02-lakehouses-raw.json (4.6 MB)
│   ├── 03-warehouses-raw.json (2.2 MB)
│   ├── 04-notebooks-raw.json
│   ├── 05-orchestration-raw.json
│   ├── 06-procs-raw.json (1.5 MB)
│   ├── 07-views-raw.json
│   ├── 08-shortcuts-files-raw.json
│   ├── 09-external-guids.json
│   ├── 10-runs-raw.json
│   ├── 11-web-data.json
│   ├── notebooks/   (18 .ipynb + 18 .py)
│   └── pipelines/   (22 .json)
├── scripts/                             ← scan + build
│   ├── _scan_lakehouses.py
│   ├── _scan_procs_views.py
│   ├── _scan_shortcuts_files.py
│   ├── _scan_pipeline_runs.py
│   ├── _sql_helper.py
│   └── _build_docs.py                   ← regen this repo
└── _archive/                            ← old presentation artifacts (preserved)
```

---
