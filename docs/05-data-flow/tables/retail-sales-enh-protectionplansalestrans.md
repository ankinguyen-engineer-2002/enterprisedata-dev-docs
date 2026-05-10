# 🔍 `Retail_Sales_Enh.ProtectionPlanSalesTrans`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Retail_Sales_Enh.ProtectionPlanSalesTrans"]:::tbl
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Pr"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Pr"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Pr"] -- writes --> T
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Pr"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Pr"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Pr"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Pr"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Wrk.usp_Pr"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (3)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_ProtectionPlanSalesTrans_Insert`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_ProtectionPlanTrans_Bulk`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_ProtectionPlanTrans_Delivered_Bulk`

## Readers (5)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_ProtectionPlanSalesTrans_Insert`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_ProtectionPlanTrans_Insert`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_ProtectionPlanTrans`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_ProtectionPlanTrans_Bulk`
- ⚙️ `Retail_Warehouse.Retail_Sales_Wrk.usp_ProtectionPlanTrans_Delivered_Bulk`

---
