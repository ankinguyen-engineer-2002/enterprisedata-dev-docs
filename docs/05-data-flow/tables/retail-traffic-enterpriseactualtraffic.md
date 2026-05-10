# 🔍 `Retail_Traffic.EnterpriseActualTraffic`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Retail_Traffic.EnterpriseActualTraffic"]:::tbl
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Traffic.usp_Load"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Traffic.usp_Refr"] -- writes --> T
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Traffic.Usp_Refr"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Traffic.usp_Load"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_Traffic.usp_Refr"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (2)

- ⚙️ `Retail_Warehouse.Retail_Traffic.usp_Load_EnterpriseActualTraffic_FromHistory`
- ⚙️ `Retail_Warehouse.Retail_Traffic.usp_Refresh_EnterpriseActualTraffic`

## Readers (3)

- ⚙️ `Retail_Warehouse.Retail_Traffic.Usp_Refresh_StoreTraffic`
- ⚙️ `Retail_Warehouse.Retail_Traffic.usp_Load_EnterpriseActualTraffic_FromHistory`
- ⚙️ `Retail_Warehouse.Retail_Traffic.usp_Refresh_EnterpriseActualTraffic`

---
