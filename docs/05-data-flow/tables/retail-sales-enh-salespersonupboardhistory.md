# 🔍 `Retail_Sales_Enh.SalesPersonUPBoardHistory`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Retail_Sales_Enh.SalesPersonUPBoardHistory"]:::tbl
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"] -- writes --> T
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (1)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_SalespersonUPBoardHistory`

## Readers (6)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_SalesPersonHourlyStats`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_SalespersonUPBoardHistory`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_ScoreboardActivity`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_ScoreboardActivity_20260223`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_ScoreboardManagerNotes`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_ScoreboardManagerNotes_20260223`

---
