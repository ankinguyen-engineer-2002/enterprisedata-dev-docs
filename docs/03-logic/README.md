# 🧠 03 — Logic Layer

[← Root](../../README.md)

## What lives here

Code & transformations that compute over the [Storage Layer](../02-storage/README.md).

| Type | Count | Total size | Detail |
|---|---|---|---|
| ⚙️ **Stored Procedures** | 192 | 1.39 MB code | [See procs →](stored-procs.md) |
| 👁️ **User Views** | 145 | — | [See views →](views.md) |
| 📓 **Notebooks** | 18 | — | [See notebooks →](notebooks.md) |

## 🌳 Logic distribution by warehouse

```mermaid
graph TB
    classDef heavy fill:#fde68a,stroke:#d97706;
    classDef medium fill:#dbeafe,stroke:#2563eb;
    classDef light fill:#e5e7eb,stroke:#6b7280;

    RW[Retail_Warehouse<br/>146 procs · 29 views<br/>957 KB]:::heavy
    ETL[ETL_Framework<br/>35 procs · 2 views<br/>261 KB]:::heavy
    WW[Wholesale_Warehouse<br/>8 procs · 114 views<br/>162 KB]:::medium
    SD[Source_Data<br/>2 procs<br/>9 KB]:::light
    AD[A_Developement LH<br/>1 proc<br/>2 KB]:::light
```

## 📑 Sub-pages

- [⚙️ Stored Procedures](stored-procs.md) — 192 procs grouped by family
- [👁️ Views](views.md) — 145 user views (mostly `_Wrk` working sets)
- [📓 Notebooks](notebooks.md) — 18 notebooks grouped: 6 active prod, 3 Vers5 dup, 6 ad-hoc, 3 empty

---
