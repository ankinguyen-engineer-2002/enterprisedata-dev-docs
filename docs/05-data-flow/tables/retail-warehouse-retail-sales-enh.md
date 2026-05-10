# 🔍 `Retail_Warehouse.Retail_Sales_Enh`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Retail_Warehouse.Retail_Sales_Enh"]:::tbl
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Re"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Re"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Re"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Re"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Re"] -- writes --> T
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Re"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Re"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (5)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Refresh_BucketGetInventory`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Refresh_BucketOrderItem`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Refresh_BucketPOI`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Refresh_Buckets_Update`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Refresh_Buckets_Update_Test`

## Readers (2)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Refresh_Buckets_Update`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Refresh_Buckets_Update_Test`

---
