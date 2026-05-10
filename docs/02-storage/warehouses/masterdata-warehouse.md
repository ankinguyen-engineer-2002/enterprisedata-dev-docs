# 🏬 MasterData_Warehouse

_PROD tier · ID `db565620-28ac-4510-a61e-1023743efdc6`_

[← Warehouses](README.md) · [← Storage](../README.md) · [← Root](../../../README.md)

## 🎯 Purpose

**Silver tier master data warehouse** — 46 tables / 0 procs nội bộ. Loaded by ETL_Framework procs (cross-WH).

## 📊 Stats

| Metric | Value |
|---|---|
| Tier | PROD |
| Schemas | 14 |
| Tables | 46 |
| Views | 12 |
| Stored Procedures | 0 |
| Workspace ID | `5360a935-1984-4775-895f-f4c90bafa19d` |
| Item ID | `db565620-28ac-4510-a61e-1023743efdc6` |

**Highlight:** Master data domain — items, customers, vendors, products. Logic centralized in ETL_Framework.

## 🗂️ Schemas

`GeographicData`, `GeographicData_Wrk`, `INFORMATION_SCHEMA`, `MasterData_DW`, `MasterData_DW_Wrk`, `ProductKnowledge`, `ProductKnowledge_Wrk`, `Retail`, `Security`, `_rsc`, `dbo`, `guest`, `queryinsights`, `sys`

## 📋 Tables (46)

**Top 30 tables (sample):**

| Schema | Table | Rows | Modified |
|---|---|---|---|
| `GeographicData` | `CountryMaster` | 0 | 2025-09-26 |
| `GeographicData` | `CountyMaster` | 0 | 2025-09-26 |
| `GeographicData` | `MSAMaster` | 0 | 2025-09-26 |
| `GeographicData` | `StateMaster` | 0 | 2025-09-26 |
| `GeographicData` | `ZipCode` | 0 | 2025-09-26 |
| `MasterData_DW` | `DimDate` | 0 | 2025-09-26 |
| `MasterData_DW` | `DimDate_NonRetail` | 0 | 2025-09-26 |
| `MasterData_DW` | `DimDateTool` | 0 | 2025-09-26 |
| `MasterData_DW` | `DimItemMaster` | 0 | 2025-10-28 |
| `MasterData_DW` | `DimRetailLocations` | 0 | 2025-09-26 |
| `MasterData_DW` | `DimTime` | 0 | 2025-09-26 |
| `ProductKnowledge` | `CatalogImages` | 0 | 2025-09-26 |
| `ProductKnowledge` | `ChildStyleLookup` | 0 | 2025-09-26 |
| `ProductKnowledge` | `Item` | 0 | 2025-09-26 |
| `ProductKnowledge` | `ItemClass` | 0 | 2025-09-26 |
| `ProductKnowledge` | `ItemCodeMaster` | 0 | 2025-09-26 |
| `ProductKnowledge` | `ItemCollectiveClass` | 0 | 2025-09-26 |
| `ProductKnowledge` | `ItemDimensions` | 0 | 2025-09-26 |
| `ProductKnowledge` | `ItemGrouping` | 0 | 2025-09-26 |
| `ProductKnowledge` | `ItemMaster` | 0 | 2025-09-26 |
| `ProductKnowledge` | `ItemMattressTypes` | 0 | 2025-09-26 |
| `ProductKnowledge` | `ItemPublishCodes` | 0 | 2025-09-26 |
| `ProductKnowledge` | `ItemSeries` | 0 | 2025-09-26 |
| `ProductKnowledge` | `ItemStatusCode` | 0 | 2025-09-26 |
| `ProductKnowledge` | `ItemStyle` | 0 | 2025-09-26 |
| `ProductKnowledge` | `LifeStyleArea` | 0 | 2025-09-26 |
| `ProductKnowledge` | `ParentStyleLookup` | 0 | 2025-09-26 |
| `ProductKnowledge` | `RetailSalesCategory` | 0 | 2025-09-26 |
| `ProductKnowledge` | `SeriesGroupingLookup` | 0 | 2025-09-26 |
| `ProductKnowledge` | `SeriesPublishCodes` | 0 | 2025-09-26 |

_… and 16 more. Full list in [`data/03-warehouses-raw.json`](../../../data/03-warehouses-raw.json)._

---

**Related:** [03 Logic — Stored Procedures](../../03-logic/stored-procs.md) · [04 Orchestration — Pipelines](../../04-orchestration/pipelines.md)
