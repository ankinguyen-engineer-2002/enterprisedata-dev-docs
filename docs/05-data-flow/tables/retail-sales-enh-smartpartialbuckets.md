# 🔍 `Retail_Sales_Enh.SmartPartialBuckets`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Retail_Sales_Enh.SmartPartialBuckets"]:::tbl
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"] -- writes --> T
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_GS"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (2)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_BucketInsert`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_BucketInsert_OLD`

## Readers (3)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_GSCLocationProducts_Insert`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_BucketInsert`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_BucketInsert_OLD`

---
