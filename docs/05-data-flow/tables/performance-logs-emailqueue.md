# 🔍 `Performance_Logs.EmailQueue`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Performance_Logs.EmailQueue"]:::tbl
    w_etl-framework-dw-dev["⚙️ ETL_Framework.DW_Developer.usp_DataWareh"] -- writes --> T
    w_etl-framework-dw-dev["⚙️ ETL_Framework.DW_Developer.usp_DataWareh"] -- writes --> T
    w_etl-framework-perfor["⚙️ ETL_Framework.Performance_Logs.usp_Email"] -- writes --> T
    T -- read by --> r_etl-framework-dw-dev["⚙️ ETL_Framework.DW_Developer.usp_DataWareh"]
    T -- read by --> r_etl-framework-dw-dev["⚙️ ETL_Framework.DW_Developer.usp_DataWareh"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (3)

- ⚙️ `ETL_Framework.DW_Developer.usp_DataWarehouseDataFeedAlert_Fabric`
- ⚙️ `ETL_Framework.DW_Developer.usp_DataWarehouseSLAAlert_Fabric`
- ⚙️ `ETL_Framework.Performance_Logs.usp_EmailQueue_MarkSent`

## Readers (2)

- ⚙️ `ETL_Framework.DW_Developer.usp_DataWarehouseDataFeedAlert_Fabric`
- ⚙️ `ETL_Framework.DW_Developer.usp_DataWarehouseSLAAlert_Fabric`

---
