# 🔍 `MasterData_Product_Enh.ProductInfo`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["MasterData_Product_Enh.ProductInfo"]:::tbl
    w_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_Product_Enh."] -- writes --> T
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_Product_Enh."]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_OOM_Wrk.usp_Piec"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Fu"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (1)

- ⚙️ `Retail_Warehouse.MasterData_Product_Enh.usp_Refresh_ProductInfo`

## Readers (4)

- ⚙️ `Retail_Warehouse.MasterData_Product_Enh.usp_Refresh_ProductInfo`
- ⚙️ `Retail_Warehouse.Retail_OOM_Wrk.usp_PieceInventory_InvSubBucketID`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Full_Refresh_SalesOrderHeader`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_SalesOrderHeader`

---
