# 🔍 `Source_Data.MasterData_Retail`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Source_Data.MasterData_Retail"]:::tbl
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_OOM_Enh.usp_GLHi"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales.usp_Update"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    T -- read by --> r_retail-warehouse-mas["👁️ Retail_Warehouse.MasterData_Retail_Ent_W"]
    T -- read by --> r_retail-warehouse-ret["👁️ Retail_Warehouse.Retail_Sales_Wrk.v_Cred"]
    T -- read by --> r_retail-warehouse-ret["👁️ Retail_Warehouse.Retail_Sales_Wrk.v_Regi"]
    T -- read by --> r_retail-warehouse-ret["👁️ Retail_Warehouse.Retail_Sales_Wrk.v_Sale"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (0)

_(no writers detected — possibly read-only or written by external process)_

## Readers (8)

- ⚙️ `Retail_Warehouse.Retail_OOM_Enh.usp_GLHist`
- ⚙️ `Retail_Warehouse.Retail_Sales.usp_Update_SalespersonUPBoardHistoryAGR`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_SalesPersonHourlyStats`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_SalespersonUPBoardHistory`
- 👁️ `Retail_Warehouse.MasterData_Retail_Ent_Wrk.v_StoreLocation`
- 👁️ `Retail_Warehouse.Retail_Sales_Wrk.v_CreditReview`
- 👁️ `Retail_Warehouse.Retail_Sales_Wrk.v_RegisteredGuest`
- 👁️ `Retail_Warehouse.Retail_Sales_Wrk.v_SalesOrderHeader`

---
