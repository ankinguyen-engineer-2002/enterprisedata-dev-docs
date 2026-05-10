# 🔍 `Retail_Sales_Wrk.SOrderHist`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Retail_Sales_Wrk.SOrderHist"]:::tbl
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Sa"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Sa"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Sa"] -- writes --> T
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Sa"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Sa"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Sa"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (3)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderHistProcessOrders_Bulk`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_SalesOrderHist_Insert_Bulk`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_SalesOrderHist_Payments_Bulk`

## Readers (3)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderHistProcessOrders_Bulk`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_SalesOrderHist_Insert_Bulk`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_SalesOrderHist_Payments_Bulk`

---
