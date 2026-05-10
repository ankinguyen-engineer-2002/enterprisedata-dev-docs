# 🏬 Source_Data

_PROD-SRC tier · ID `f14e2ea6-ae2c-4b90-8e08-522e84f1aefc`_

[← Warehouses](README.md) · [← Storage](../README.md) · [← Root](../../../README.md)

## 🎯 Purpose

**Bronze landing layer** — 64 schemas (1 schema per source feed). Loaded by EDW2FabricLoader pipeline + ADF mount + migration pipelines. Largest WH by table count.

## 📊 Stats

| Metric | Value |
|---|---|
| Tier | PROD-SRC |
| Schemas | 64 |
| Tables | 636 |
| Views | 12 |
| Stored Procedures | 2 |
| Workspace ID | `5360a935-1984-4775-895f-f4c90bafa19d` |
| Item ID | `f14e2ea6-ae2c-4b90-8e08-522e84f1aefc` |

**Highlight:** Receives every raw feed. Schemas mirror source-system names: Retail_Corporate, MasterData_HR_UKG_*, Manufacturing_Maximo, etc.

## 🗂️ Schemas

`AFISales`, `AFISales_Wrk`, `INFORMATION_SCHEMA`, `Manufacturing_Inventory`, `Manufacturing_Inventory_AFI`, `Manufacturing_Masterdata`, `Manufacturing_ProductionPlanning_AFI`, `Manufacturing_ProductionPlanning_AFI_Wrk`, `MasterData_GeographicData`, `MasterData_HR_UKG`, `MasterData_HR_UKG_AGR`, `MasterData_HR_UKG_AGR_Wrk`, `MasterData_HR_UKG_DSG`, `MasterData_HR_UKG_DSG_Wrk`, `MasterData_HR_UKG_Wrk`, `MasterData_ItemMaster_AFI`, `MasterData_ItemMaster_AFI_Wrk`, `MasterData_OneSource`, `MasterData_PIM`, `MasterData_ProductKnowledge`, `MasterData_Retail`, `MasterData_Retail_Wrk`, `MasterData_Security`, `Masterdata_Finance`, `Merch_ExternalFiles`, `ResidentHome`, `Retail_ChannelDB`, `Retail_Corporate`, `Retail_Corporate_SCD`, `Retail_Corporate_SCD_Wrk`, `Retail_Corporate_Wrk`, `Retail_Dart`, `Retail_Ecommerce`, `Retail_External`, `Retail_ExternalFiles`, `Retail_Marketing`, `Retail_Miniapps`, `Retail_ProfitSystems`, `Retail_Shoppertrack`, `Retail_Shoppertrack_Wrk`, `SupplyChain_DW`, `SupplyChain_Enh`, `Wholesale_CODIS_AFI`, `Wholesale_Codis_Wrk`, `Wholesale_Customers`, `Wholesale_DemandPlanning_AFI`, `Wholesale_Invoicing_AFI`, `Wholesale_Invoicing_AFI_wrk`, `Wholesale_Marketing`, `Wholesale_PartyContacts`, `Wholesale_ProductSourcing`, `Wholesale_ProductSourcing_AFI`, `Wholesale_ProductSourcing_AFI_Wrk`, `Wholesale_Purchasing_AFI`, `Wholesale_Quality_AFI`, `Wholesale_Quality_AFI_wrk`, `Wholesale_SalesHistory_AFI`, `Wholesale_SalesHistory_AFI_Wrk`, `_rsc`, `dbo`, `guest`, `queryinsights`, `sys`, `wholesale_pricing_afi`

## 📋 Tables (636)

**Top 30 tables (sample):**

| Schema | Table | Rows | Modified |
|---|---|---|---|
| `AFISales` | `ordschd` | 0 | 2025-12-09 |
| `AFISales_Wrk` | `ordschd` | 0 | 2025-12-09 |
| `Manufacturing_Inventory` | `TFRPRTY` | 0 | 2025-12-16 |
| `Manufacturing_Inventory_AFI` | `TFRDTL` | 0 | 2025-12-16 |
| `Manufacturing_Inventory_AFI` | `TFRHDR` | 0 | 2025-12-16 |
| `Manufacturing_Inventory_AFI` | `TODETL` | 0 | 2025-12-16 |
| `Manufacturing_Masterdata` | `WMSOLSTS` | 0 | 2025-10-21 |
| `Manufacturing_ProductionPlanning_AFI` | `MOHMST` | 0 | 2025-12-16 |
| `Manufacturing_ProductionPlanning_AFI` | `MOMAST` | 0 | 2025-12-09 |
| `Manufacturing_ProductionPlanning_AFI` | `MSIORD` | 0 | 2025-12-09 |
| `Manufacturing_ProductionPlanning_AFI_Wrk` | `MOHMST` | 0 | 2025-12-16 |
| `Masterdata_Finance` | `ResidentHomeWeeklyWrittenSales` | 0 | 2026-01-24 |
| `Masterdata_Finance` | `ResidentHomeWeeklyWrittenSalesSKU` | 0 | 2026-01-24 |
| `Masterdata_Finance` | `RHPIMmapping` | 0 | 2026-01-24 |
| `MasterData_GeographicData` | `CountryMaster` | 0 | 2025-12-09 |
| `MasterData_GeographicData` | `CountyMaster` | 0 | 2025-12-09 |
| `MasterData_GeographicData` | `MSAMaster` | 0 | 2025-12-09 |
| `MasterData_GeographicData` | `StateMaster` | 0 | 2025-12-09 |
| `MasterData_GeographicData` | `ZipCode` | 0 | 2025-12-09 |
| `MasterData_HR_UKG` | `CommonDataApprovals` | 0 | 2026-03-17 |
| `MasterData_HR_UKG` | `CompanyDetails` | 0 | 2026-02-11 |
| `MasterData_HR_UKG` | `EmploymentDetails` | 0 | 2026-02-11 |
| `MasterData_HR_UKG` | `HyperFind` | 0 | 2026-02-11 |
| `MasterData_HR_UKG` | `Jobs` | 0 | 2026-02-11 |
| `MasterData_HR_UKG` | `Locations` | 0 | 2026-02-11 |
| `MasterData_HR_UKG` | `OrgLevel` | 0 | 2026-02-11 |
| `MasterData_HR_UKG` | `PayCodes` | 0 | 2026-02-11 |
| `MasterData_HR_UKG` | `PersonDetails` | 0 | 2026-02-11 |
| `MasterData_HR_UKG` | `ProcessedSegmentLaborCategories` | 0 | 2026-02-11 |
| `MasterData_HR_UKG` | `TimecardProcessedSegment` | 0 | 2026-02-11 |

_… and 606 more. Full list in [`data/03-warehouses-raw.json`](../../../data/03-warehouses-raw.json)._

## ⚙️ Stored procedures (2)

| Family | Procs | Examples |
|---|---|---|
| Curated refresh | 2 | `usp_Refresh_EnterpriseAPIReprocessedLogs`, `usp_refresh_shopperTrakTables` |

Full proc bodies → [`data/06-procs-raw.json`](../../../data/06-procs-raw.json)

---

**Related:** [03 Logic — Stored Procedures](../../03-logic/stored-procs.md) · [04 Orchestration — Pipelines](../../04-orchestration/pipelines.md)
