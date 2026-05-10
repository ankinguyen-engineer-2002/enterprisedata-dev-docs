# 🔍 `Retail_Sales_Wrk.SUOrderLoadQueue`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Retail_Sales_Wrk.SUOrderLoadQueue"]:::tbl
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Sa"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Sa"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_SU"] -- writes --> T
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Sa"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_SU"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (3)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderCloses`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderCloses_ProcessSUOrders`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_SUOrder_LoadQueue_GetOrderID`

## Readers (2)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderCloses_ProcessSUOrders`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_SUOrder_LoadQueue_GetOrderID`

---
