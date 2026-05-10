# 📦 02 — Storage Layer

[← Back to root](../../README.md)

## What lives here

Storage = where data physically resides (or *appears* to reside via shortcuts). Three storage primitives in this workspace:

| Type | Count | Total tables | Total rows | Detail |
|---|---|---|---|---|
| 🏬 **Warehouse** | 11 | 1,165 | — | [See Warehouses →](warehouses/README.md) |
| 💧 **Lakehouse** | 5 | 506 | 5,923,323,398 | [See Lakehouses →](lakehouses/README.md) |
| 🗄️ **SQLDatabase** | 1 | — | — | Commissions_Prototype (sink) |

> Most of those 5.92 B rows are **OneLake shortcuts to the PROD workspace**, not stored locally. See [05 Data Flow](../05-data-flow/README.md) and [06 Cross-Workspace](../06-cross-workspace/README.md).

## 🗺️ Storage map

![Storage map](../../images/02-storage-map.svg)

```mermaid
graph TB
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
    ETL -. drives .-> MD
```

## 📑 Sub-pages

- [🏬 **Warehouses (11)** ](warehouses/README.md) — relational T-SQL containers
- [💧 **Lakehouses (5)**](lakehouses/README.md) — Delta Lake on OneLake

## ⚠️ Storage-related risks

- **C3 (High)**: `Quality_Warehouse` (PROD tier) is empty — needs build or remove decision
- **C25 (High)**: 5.92 B rows in `Centralized_Lakehouse` are shortcut-backed, not real DEV data
- **C28 (High)**: `RadarSync_Test` mounts entire trusted+raw ADLS zones — broad scope
- **C20 (Low)**: Twin schemas `Retail_Corporate` ↔ `Retail_Corporate_Prod` confusion

Full risk list → [09 Risks](../09-risks/README.md)

---

**Next:** [🏬 Warehouses →](warehouses/README.md) or [💧 Lakehouses →](lakehouses/README.md)
