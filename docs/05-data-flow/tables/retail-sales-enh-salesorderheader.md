# 🔍 `Retail_Sales_Enh.SalesOrderHeader`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Retail_Sales_Enh.SalesOrderHeader"]:::tbl
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Fu"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"] -- writes --> T
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Fu"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Sa"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Sa"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Sa"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Or"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Sa"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (2)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Full_Refresh_SalesOrderHeader`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_SalesOrderHeader`

## Readers (9)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Full_Refresh_SalesOrderHeader`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderCloses`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderHistProcessOrders_Bulk`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderHistQueue`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_SalesOrderHeader`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_SalesOrderLineHistory`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_SalesOrderLineHistoryTest`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_OrderSplit_ProcessOrder_Bulk`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_SalesOrderHist_Payments_Bulk`

---
