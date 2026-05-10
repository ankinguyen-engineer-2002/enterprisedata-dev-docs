# 🔍 `Retail_Sales_Wrk.SUOrderDateQueue`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Retail_Sales_Wrk.SUOrderDateQueue"]:::tbl
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Sa"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Sa"] -- writes --> T
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Sa"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Sa"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Sa"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Sa"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (2)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderCloses`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderCloses_ProcessSUOrders`

## Readers (4)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderCloses`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderCloses_ProcessSUOrder_Bulk`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderCloses_ProcessSUOrders`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_SalesOrderCloses_ProcessSUOrder_Bulk`

---
