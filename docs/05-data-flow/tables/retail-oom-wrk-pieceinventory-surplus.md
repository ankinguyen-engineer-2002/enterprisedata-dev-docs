# 🔍 `Retail_OOM_Wrk.PieceInventory_Surplus`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Retail_OOM_Wrk.PieceInventory_Surplus"]:::tbl
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_OOM_Wrk.usp_Piec"] -- writes --> T
    w_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_OOM_Wrk.usp_Piec"] -- writes --> T
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_OOM_Wrk.usp_Inve"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_OOM_Wrk.usp_Inve"]
    T -- read by --> r_retail-warehouse-ret["⚙️ Retail_Warehouse.Retail_OOM_Wrk.usp_Piec"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (2)

- ⚙️ `Retail_Warehouse.Retail_OOM_Wrk.usp_PieceInventory_Surplus`
- ⚙️ `Retail_Warehouse.Retail_OOM_Wrk.usp_PieceInventory_Surplus_ROS`

## Readers (3)

- ⚙️ `Retail_Warehouse.Retail_OOM_Wrk.usp_InventoryDetail`
- ⚙️ `Retail_Warehouse.Retail_OOM_Wrk.usp_InventorySummary_Update`
- ⚙️ `Retail_Warehouse.Retail_OOM_Wrk.usp_PieceInventory_Surplus_ROS`

---
