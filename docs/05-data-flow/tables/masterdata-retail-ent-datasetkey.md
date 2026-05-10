# 🔍 `MasterData_Retail_Ent.DataSetKey`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["MasterData_Retail_Ent.DataSetKey"]:::tbl
    w_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_Retail_Ent.u"] -- writes --> T
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Sa"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Or"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Or"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Or"]
    T -- read by --> r_retail-warehouse-ret["👁️ Retail_Warehouse.Retail_Sales_Wrk.v_Sale"]
    T -- read by --> r_retail-warehouse-ret["👁️ Retail_Warehouse.Retail_Sales_Wrk.v_Sale"]
    T -- read by --> r_retail-warehouse-ret["👁️ Retail_Warehouse.Retail_Sales_Wrk.v_Sale"]
    T -- read by --> r_retail-warehouse-ret["👁️ Retail_Warehouse.Retail_Sales_Wrk.v_Sale"]
    T -- read by --> r_retail-warehouse-ret["👁️ Retail_Warehouse.Retail_Sales_Wrk.v_Sale"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (1)

- ⚙️ `Retail_Warehouse.MasterData_Retail_Ent.usp_Refresh_DataSetKey`

## Readers (10)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderHistQueue`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_SalesOrderHeader`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_OrderHist_Payments`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_OrderSplit`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_OrderSplit_OI`
- 👁️ `Retail_Warehouse.Retail_Sales_Wrk.v_SalesAssociateCommission`
- 👁️ `Retail_Warehouse.Retail_Sales_Wrk.v_SalesOrderFulfillment`
- 👁️ `Retail_Warehouse.Retail_Sales_Wrk.v_SalesOrderHeader`
- 👁️ `Retail_Warehouse.Retail_Sales_Wrk.v_SalesOrderLine`
- 👁️ `Retail_Warehouse.Retail_Sales_Wrk.v_SalesOrderProductInfo`

---
