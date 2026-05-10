# 🔍 `MasterData_HR_UKG_Enh.TimeSheetSummary`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["MasterData_HR_UKG_Enh.TimeSheetSummary"]:::tbl
    w_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"] -- writes --> T
    w_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"] -- writes --> T
    w_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"] -- writes --> T
    w_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"] -- writes --> T
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"]
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"]
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"]
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"]
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (4)

- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_RefreshTimeSheetSummaryPayMatrix`
- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_RefreshTimeSheetSummary_ContractorData`
- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_RefreshTimeSheetSummary_TotalDCExpences`
- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Update_TimeSheetSummary`

## Readers (5)

- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_RefreshTimeSheetSummaryPayMatrix`
- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_RefreshTimeSheetSummary_Benefits`
- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_RefreshTimeSheetSummary_ContractorData`
- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_RefreshTimeSheetSummary_TotalDCExpences`
- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Update_TimeSheetSummary`

---
