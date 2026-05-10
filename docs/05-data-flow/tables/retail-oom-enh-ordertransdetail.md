# 🔍 `Retail_OOM_Enh.OrderTransDetail`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Retail_OOM_Enh.OrderTransDetail"]:::tbl
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_OOM_Enh.usp_Upda"] -- writes --> T
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_OOM_Enh.usp_Upda"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_OOM_Enh.usp_Upda"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_OOM_Enh.usp_Upda"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_OOM_Enh.usp_Upda"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (1)

- ⚙️ `Retail_Warehouse.Retail_OOM_Enh.usp_Update_OrderTransDetail`

## Readers (4)

- ⚙️ `Retail_Warehouse.Retail_OOM_Enh.usp_Update_OOMSchedulePerformance`
- ⚙️ `Retail_Warehouse.Retail_OOM_Enh.usp_Update_OOMSchedulePerformanceDetails`
- ⚙️ `Retail_Warehouse.Retail_OOM_Enh.usp_Update_OrderTransDetail`
- ⚙️ `Retail_Warehouse.Retail_OOM_Enh.usp_Update_OrderTransDetailDailyStat`

---
