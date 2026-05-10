# 🏬 Centralized_Warehouse

_PROD tier · ID `c5a1f95b-f9db-4cb7-8ded-396ea70da572`_

[← Warehouses](README.md) · [← Storage](../README.md) · [← Root](../../../README.md)

## 🎯 Purpose

**Gold tier warehouse** — 38 tables / **0 procs nội bộ**. Loaded externally bởi `MetaData-Pull` notebook (cross-WH JDBC sync) chứ không có proc bên trong.

## 📊 Stats

| Metric | Value |
|---|---|
| Tier | PROD |
| Schemas | 23 |
| Tables | 38 |
| Views | 12 |
| Stored Procedures | 0 |
| Workspace ID | `5360a935-1984-4775-895f-f4c90bafa19d` |
| Item ID | `c5a1f95b-f9db-4cb7-8ded-396ea70da572` |

**Highlight:** MetaData schema chứa control tables (CopyTables, ShortcutCatalog, SysObjectInfo) drive cho notebooks & system pipelines.

## 🗂️ Schemas

`Distribution_Warehouse_INFORMATION_SCHEMA`, `Distribution_Warehouse_sys`, `ETL_Framework_INFORMATION_SCHEMA`, `ETL_Framework_sys`, `INFORMATION_SCHEMA`, `MasterData_Warehouse_INFORMATION_SCHEMA`, `MasterData_Warehouse_sys`, `MetaData`, `Quality_Warehouse_INFORMATION_SCHEMA`, `Quality_Warehouse_sys`, `Retail_Warehouse_INFORMATION_SCHEMA`, `Retail_Warehouse_sys`, `Source_Data_INFORMATION_SCHEMA`, `Source_Data_INFORMATION_SCHEMA_adf`, `Source_Data_sys`, `Source_Data_sys_adf`, `Wholesale_Warehouse_INFORMATION_SCHEMA`, `Wholesale_Warehouse_sys`, `_rsc`, `dbo`, `guest`, `queryinsights`, `sys`

## 📋 Tables (38)

**Top 30 tables (sample):**

| Schema | Table | Rows | Modified |
|---|---|---|---|
| `dbo` | `ShortcutCatalog` | 0 | 2025-09-07 |
| `MetaData` | `ShortcutCatalog` | 0 | 2025-09-09 |
| `MetaData` | `ShortcutCatalog_bkp` | 0 | 2025-09-09 |
| `MetaData` | `ShortcutCatalog_V1` | 0 | 2025-09-09 |
| `MetaData` | `SysObjectInfo` | 0 | 2025-09-07 |
| `Source_Data_INFORMATION_SCHEMA` | `COLUMNS` | 0 | 2025-11-09 |
| `Source_Data_INFORMATION_SCHEMA` | `TABLES` | 0 | 2025-11-09 |
| `Source_Data_INFORMATION_SCHEMA` | `VIEWS` | 0 | 2025-11-09 |
| `Source_Data_INFORMATION_SCHEMA_adf` | `COLUMNS` | 0 | 2025-09-09 |
| `Source_Data_INFORMATION_SCHEMA_adf` | `TABLES` | 0 | 2025-09-09 |
| `Source_Data_INFORMATION_SCHEMA_adf` | `VIEWS` | 0 | 2025-09-09 |
| `Source_Data_sys` | `all_columns` | 0 | 2025-11-09 |
| `Source_Data_sys` | `columns` | 0 | 2025-11-09 |
| `Source_Data_sys` | `databases` | 0 | 2025-11-09 |
| `Source_Data_sys` | `events` | 0 | 2025-11-09 |
| `Source_Data_sys` | `index_columns` | 0 | 2025-11-09 |
| `Source_Data_sys` | `indexes` | 0 | 2025-11-09 |
| `Source_Data_sys` | `objects` | 0 | 2025-11-09 |
| `Source_Data_sys` | `partition_schemes` | 0 | 2025-11-09 |
| `Source_Data_sys` | `schemas` | 0 | 2025-11-09 |
| `Source_Data_sys` | `stats` | 0 | 2025-11-09 |
| `Source_Data_sys` | `stats_columns` | 0 | 2025-11-09 |
| `Source_Data_sys` | `table_types` | 0 | 2025-11-09 |
| `Source_Data_sys` | `tables` | 0 | 2025-11-09 |
| `Source_Data_sys` | `types` | 0 | 2025-11-09 |
| `Source_Data_sys` | `views` | 0 | 2025-11-09 |
| `Source_Data_sys_adf` | `all_columns` | 0 | 2025-09-09 |
| `Source_Data_sys_adf` | `columns` | 0 | 2025-09-09 |
| `Source_Data_sys_adf` | `databases` | 0 | 2025-09-09 |
| `Source_Data_sys_adf` | `events` | 0 | 2025-09-09 |

_… and 8 more. Full list in [`data/03-warehouses-raw.json`](../../../data/03-warehouses-raw.json)._

---

**Related:** [03 Logic — Stored Procedures](../../03-logic/stored-procs.md) · [04 Orchestration — Pipelines](../../04-orchestration/pipelines.md)
