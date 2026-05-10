# 🔁 Data Pipelines (22)

[← Orchestration](README.md) · [← Root](../../README.md)

## Run status overview

- **2** pipelines have run history in API window
- **20** dormant (never ran or older than window)

## By group

### ETL/Migration (8)

| Pipeline | Purpose | Status |
|---|---|---|
| `EDW2FabricLoader` | Lookup+Filter+ForEach: Azure SQL DB ASHLEY_EDW_DEV.dw_developer.FabricMapping (Flag=1) → Fabric DW Source_Data; per-row dynamic Query/schema/table | 💤 Dormant |
| `Fabric Migration ADF` | Same shape as EDW2FabricLoader but source = Synapse Ashley_Edw (SqlDWSource), with TRUNCATE precopy | 💤 Dormant |
| `MigrateData` | Single Copy cross-WS: PROD Source_Data Retail_Corporate.BtaData last-90-days → DEV Source_Data | 💤 Dormant |
| `Migration_TableDictionary_entry` | Copy Synapse Ashley_Edw.dw_developer.tabledictionary → ETL_Framework.dw_developer.TableDictionary_Helper, then Script merges into TableDictionary | 💤 Dormant |
| `Load Retail_DW` | Single Copy: Azure SQL Ashley_EDW.Retail_DW.DimItemMaster → Fabric Retail_Warehouse with full ~100-col mapping | 💤 Dormant |
| `Load MasterData_ItemMaster_AFI tables` | 3 parallel Copies: Synapse Ashley_EDW.MasterData_ItemMaster_AFI.{GENDESC, ITEMBL, ITMEXT} → Fabric Source_Data | 💤 Dormant |
| `Retail_Prod_To_Dev_DataBackFill` | On-prem SQL PROD → Fabric Source_Data. Snapshot block (33 tables) Inactive; Incremental Active. ⚠️ Failures since 2026-04-29 | ✅ Active (58 runs) |
| `Adhoc loads` | 💀 EMPTY | 💤 Dormant |

### Quality checks (3)

| Pipeline | Purpose | Status |
|---|---|---|
| `Source_EDW_Check_Test` | ✅ Daily 03:50 UTC. Truncates Bronze counts, copies on-prem ASHLEY_EDW per metadata, runs SPs, sends Office365Email per row. 100% success since 2026-04-21 | ✅ Active (64 runs) |
| `Source_EDW_Aggregate_Check` | Single dangling Lookup — abandoned | 💤 Dormant |
| `Count_Aggreagate_Check_Bronze` | 💀 EMPTY | 💤 Dormant |

### SLA / Alerting (3)

| Pipeline | Purpose | Status |
|---|---|---|
| `Alert_FabricTables_EnterpriseData` | usp_DataWarehouseDataFeedAlert_Fabric → Lookup Performance_Logs.EmailQueue → ForEach send via Office365Outlook + mark sent | 💤 Dormant |
| `PL_SLA_Breach_EnterpriseData` | usp_DataWarehouseSLAAlert_Fabric → ForEach Office365Email1 to ⚠️ HARDCODED DL_AFI_Data_WarehouseGCC@Ashleyfurniture.com | 💤 Dormant |
| `FabricSLA_Trigger_EnterpriseData` | 💀 EMPTY — intended scheduler wrapper | 💤 Dormant |

### System (2)

| Pipeline | Purpose | Status |
|---|---|---|
| `SysTable_Snapshot` | Reads Centralized_Warehouse.MetaData.SysObjectInfo → ForEach dynamic cross-WH Copy into Source_Data_<schema>.<table> + audit SP | 💤 Dormant |
| `SysTable_Dynamic` | Variant with target schema Source_Data_<schema>_adf, no audit SP (asymmetric) | 💤 Dormant |

### Test/junk (6)

| Pipeline | Purpose | Status |
|---|---|---|
| `test` | ⚠️ NOT trivial — ForEach cross-WS Copy from PROD WH → SQLDatabase Commissions_Prototype | 💤 Dormant |
| `pipeline1` | ⚠️ NOT trivial — cross-WS Copy MasterData_Retail.CreditReview → Commissions_Prototype.Storis_DW.CreditReview | 💤 Dormant |
| `pipeline2` | 💀 EMPTY | 💤 Dormant |
| `test1` | 💀 EMPTY | 💤 Dormant |
| `Pipeline_1_test` | 💀 EMPTY | 💤 Dormant |
| `testing_pipeline` | 4-row union → Lakehouse RadarSync_Test.dbo.test_pipeline | 💤 Dormant |

## 📂 Drill-down

- Per-pipeline JSON: [`data/pipelines/`](../../data/pipelines/) (22 .json files)
- Run history detail: [08 Operations / Run history](../08-operations/run-history.md)

---
