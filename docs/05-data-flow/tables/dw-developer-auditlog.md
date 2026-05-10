# 🔍 `DW_Developer.AuditLog`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["DW_Developer.AuditLog"]:::tbl
    w_etl-framework-dw-dev["⚙️ ETL_Framework.DW_Developer.Usp_CreateTab"] -- writes --> T
    w_etl-framework-dw-dev["⚙️ ETL_Framework.DW_Developer.Usp_CreateTab"] -- writes --> T
    w_etl-framework-dw-dev["⚙️ ETL_Framework.DW_Developer.Usp_WriteTabl"] -- writes --> T
    w_etl-framework-dw-dev["⚙️ ETL_Framework.DW_Developer.usp_Increment"] -- writes --> T
    w_etl-framework-dw-dev["⚙️ ETL_Framework.DW_Developer.usp_Increment"] -- writes --> T
    w_etl-framework-dw-dev["⚙️ ETL_Framework.DW_Developer.usp_Increment"] -- writes --> T
    w_etl-framework-dw-dev["⚙️ ETL_Framework.DW_Developer.usp_RefreshCu"] -- writes --> T
    w_etl-framework-dw-dev["⚙️ ETL_Framework.DW_Developer.usp_RefreshCu"] -- writes --> T
    w_etl-framework-dw-dev["⚙️ ETL_Framework.DW_Developer.usp_SCD2_Tabl"] -- writes --> T
    w_etl-framework-dw-dev["⚙️ ETL_Framework.DW_Developer.usp_UpdateCur"] -- writes --> T
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (11)

- ⚙️ `ETL_Framework.DW_Developer.Usp_CreateTableFromParquet`
- ⚙️ `ETL_Framework.DW_Developer.Usp_CreateTableFromParquet_V1`
- ⚙️ `ETL_Framework.DW_Developer.Usp_WriteTableToParquet`
- ⚙️ `ETL_Framework.DW_Developer.usp_IncrementalTableLoad`
- ⚙️ `ETL_Framework.DW_Developer.usp_IncrementalTableLoad_Backup`
- ⚙️ `ETL_Framework.DW_Developer.usp_IncrementalTableLoad_CDC`
- ⚙️ `ETL_Framework.DW_Developer.usp_RefreshCuratedTableFromView`
- ⚙️ `ETL_Framework.DW_Developer.usp_RefreshCuratedTableFromView2`
- ⚙️ `ETL_Framework.DW_Developer.usp_SCD2_TableLoad`
- ⚙️ `ETL_Framework.DW_Developer.usp_UpdateCuratedTableFromView_DateRange`
- ⚙️ `ETL_Framework.DW_Developer.usp_UpdateTableDictionary_ModifiedDate`

## Readers (0)

_(no readers detected)_

---
