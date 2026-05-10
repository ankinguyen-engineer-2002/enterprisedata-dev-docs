# Source → Bronze (`Source_Data`)

[← Data Flow](README.md) · [← Root](../../README.md)

## Sources

| Source system | Type | Connection / location | Loader |
|---|---|---|---|
| ASHLEY_EDW_DEV | On-prem SQL Server | `3fff77ab-...` SqlServer connection | EDW2FabricLoader · Source_EDW_Check_Test · Retail_Prod_To_Dev_DataBackFill |
| Ashley_Edw | Synapse SQLDW | Synapse linked service | Fabric Migration ADF · Load MasterData_ItemMaster_AFI · Migration_TableDictionary_entry |
| Ashley_EDW | Azure SQL DB | ASHLEY_EDW_DEV.dw_developer.FabricMapping | Load Retail_DW · EDW2FabricLoader (metadata) |
| UKG / AFI / Maximo / SNow / GA | SaaS | Various | Mounted ADF `ashleyv2datafactory` |
| edw_dev | Databricks UC | Connection `1d4b92c8-...` | Mirror (no pipeline) |
| ashleydevlake | ADLS Gen2 | Connection `65655456-...` | Notebooks via shortcuts in A_Developement / RadarSync_Test |

## Active loaders

Of 8 ETL pipelines, only **`Source_EDW_Check_Test`** runs daily (03:50 UTC). All others are dormant or recently-active (`Retail_Prod_To_Dev_DataBackFill` last ran 2026-04-29).

---
