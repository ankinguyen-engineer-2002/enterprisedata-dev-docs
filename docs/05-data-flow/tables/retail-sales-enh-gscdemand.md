# 🔍 `Retail_Sales_Enh.GSCDemand`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Retail_Sales_Enh.GSCDemand"]:::tbl
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_In"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"] -- writes --> T
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.proc_G"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_GS"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_GS"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_In"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Re"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Sales_Enh.usp_Up"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (2)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Insert_GSCDemand`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_GSCDemand`

## Readers (7)

- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.proc_GSCDemand_Allocate_Batched`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_GSCLocationProducts_UpdateValues`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_GSCSupply_Insert`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Insert_GSCDemand`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Refresh_SmartPartials`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_GSCDemand`
- ⚙️ `Retail_Warehouse.Retail_Sales_Enh.usp_Update_GSCPeriodDataSet`

---
