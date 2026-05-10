# 🏬 Retail_Warehouse

_PROD tier · ID `09504907-575d-446a-991a-87fa525166d7`_

[← Warehouses](README.md) · [← Storage](../README.md) · [← Root](../../../README.md)

## 🎯 Purpose

**Silver tier domain warehouse cho retail** — 198 tables, 41 views, 146 stored procs. Largest proc set trong workspace.

## 📊 Stats

| Metric | Value |
|---|---|
| Tier | PROD |
| Schemas | 25 |
| Tables | 198 |
| Views | 41 |
| Stored Procedures | 146 |
| Workspace ID | `5360a935-1984-4775-895f-f4c90bafa19d` |
| Item ID | `09504907-575d-446a-991a-87fa525166d7` |

**Highlight:** Heaviest proc family: 49 Refresh-Load + 38 MERGE + 19 Validate + 13 Audit-DQ. Pattern: usp_RefreshCuratedTableFromView consume _Wrk views.

## 🗂️ Schemas

`INFORMATION_SCHEMA`, `MasterData_Ent`, `MasterData_Ent_Wrk`, `MasterData_HR_UKG_DSG_Enh`, `MasterData_HR_UKG_DSG_Enh_Wrk`, `MasterData_HR_UKG_DSG_Wrk`, `MasterData_HR_UKG_Enh`, `MasterData_HR_UKG_Enh_Wrk`, `MasterData_Product`, `MasterData_Product_Enh`, `MasterData_Product_Wrk`, `MasterData_Retail_Ent`, `MasterData_Retail_Ent_Wrk`, `Retail_OOM_Enh`, `Retail_OOM_Wrk`, `Retail_Sales`, `Retail_Sales_Enh`, `Retail_Sales_Wrk`, `Retail_Traffic`, `Retail_Traffic_Wrk`, `_rsc`, `dbo`, `guest`, `queryinsights`, `sys`

## 📋 Tables (198)

**Top 30 tables (sample):**

| Schema | Table | Rows | Modified |
|---|---|---|---|
| `MasterData_Ent` | `CustomerInfo` | 0 | 2026-02-05 |
| `MasterData_Ent` | `PaymentType` | 0 | 2025-12-09 |
| `MasterData_Ent` | `ReasonCode` | 0 | 2025-10-08 |
| `MasterData_Ent` | `VendorInfo` | 0 | 2025-10-08 |
| `MasterData_HR_UKG_DSG_Enh` | `ChangeLogEmployeesData` | 0 | 2026-01-05 |
| `MasterData_HR_UKG_DSG_Enh` | `CompanyDetails` | 0 | 2026-01-04 |
| `MasterData_HR_UKG_DSG_Enh` | `Employees` | 0 | 2026-01-06 |
| `MasterData_HR_UKG_DSG_Enh` | `EmploymentDetails` | 0 | 2026-01-05 |
| `MasterData_HR_UKG_DSG_Enh` | `HREmployeeHistory` | 0 | 2026-01-06 |
| `MasterData_HR_UKG_DSG_Enh` | `Jobs` | 0 | 2026-01-04 |
| `MasterData_HR_UKG_DSG_Enh` | `LaborCategory` | 0 | 2026-01-04 |
| `MasterData_HR_UKG_DSG_Enh` | `OrgLevel` | 0 | 2026-01-04 |
| `MasterData_HR_UKG_DSG_Enh` | `PayCodes` | 0 | 2026-01-04 |
| `MasterData_HR_UKG_DSG_Enh` | `PeopleRecords` | 0 | 2026-01-06 |
| `MasterData_HR_UKG_DSG_Enh` | `PersonDetails` | 0 | 2026-01-04 |
| `MasterData_HR_UKG_DSG_Enh` | `WorkRules` | 0 | 2026-01-04 |
| `MasterData_HR_UKG_Enh` | `ChangeLogEmployeesData` | 0 | 2026-01-21 |
| `MasterData_HR_UKG_Enh` | `CompanyDetails` | 0 | 2026-01-21 |
| `MasterData_HR_UKG_Enh` | `DTRContractorData` | 0 | 2026-02-05 |
| `MasterData_HR_UKG_Enh` | `Employees` | 0 | 2026-02-05 |
| `MasterData_HR_UKG_Enh` | `EmployeeSupervisor` | 0 | 2026-02-05 |
| `MasterData_HR_UKG_Enh` | `EmploymentDetails` | 0 | 2026-01-21 |
| `MasterData_HR_UKG_Enh` | `HREmployeeHistory` | 0 | 2026-02-05 |
| `MasterData_HR_UKG_Enh` | `Jobs` | 0 | 2026-01-21 |
| `MasterData_HR_UKG_Enh` | `LaborCategory` | 0 | 2026-04-15 |
| `MasterData_HR_UKG_Enh` | `OrgLevel` | 0 | 2026-01-21 |
| `MasterData_HR_UKG_Enh` | `PayCodes` | 0 | 2026-01-21 |
| `MasterData_HR_UKG_Enh` | `PayMatrix` | 0 | 2026-02-05 |
| `MasterData_HR_UKG_Enh` | `PeopleRecords` | 0 | 2026-02-05 |
| `MasterData_HR_UKG_Enh` | `PeopleTimeSheet` | 0 | 2026-02-05 |

_… and 168 more. Full list in [`data/03-warehouses-raw.json`](../../../data/03-warehouses-raw.json)._

## 👁️ User views (29)

| Schema | Views | Names (sample) |
|---|---|---|
| `MasterData_Ent_Wrk` | 4 | `v_CustomerInfo`, `v_PaymentType`, `v_ReasonCode`, `v_VendorInfo` |
| `MasterData_HR_UKG_DSG_Enh_Wrk` | 1 | `v_Employees` |
| `MasterData_HR_UKG_Enh_Wrk` | 3 | `v_EmployeeSupervisor`, `v_Employees`, `v_Timesheet` |
| `MasterData_Product_Wrk` | 3 | `v_ProductGroup`, `v_ProductInfo`, `v_ProductSeries` |
| `MasterData_Retail_Ent_Wrk` | 4 | `v_SalesPerson`, `v_StoreLocation`, `v_StoreLocationCalendar`, `v_StoreLocationGroup` |
| `Retail_Sales_Wrk` | 14 | `v_BucketInventory`, `v_BucketOrderItem`, `v_BucketPOI`, `v_CreditApplication`, `v_CreditReview`, … +9 |

Full view bodies → [`data/07-views-raw.json`](../../../data/07-views-raw.json)

## ⚙️ Stored procedures (146)

| Family | Procs | Examples |
|---|---|---|
| Curated refresh | 100 | `usp_Refresh_DataSetKey`, `Usp_Refresh_EmployeeHistory`, `Usp_Refresh_MasterData_Ent`, …+97 |
| Other | 45 | `usp_DynamicTableCreateAndLoadDirect`, `usp_Buckets_Insert`, `usp_GLHist`, …+42 |
| History/Log | 1 | `usp_Load_EnterpriseActualTraffic_FromHis` |

Full proc bodies → [`data/06-procs-raw.json`](../../../data/06-procs-raw.json)

---

**Related:** [03 Logic — Stored Procedures](../../03-logic/stored-procs.md) · [04 Orchestration — Pipelines](../../04-orchestration/pipelines.md)
