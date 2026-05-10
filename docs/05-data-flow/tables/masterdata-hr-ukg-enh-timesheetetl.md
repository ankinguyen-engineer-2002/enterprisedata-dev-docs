# 🔍 `MasterData_HR_UKG_Enh.TimesheetETL`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["MasterData_HR_UKG_Enh.TimesheetETL"]:::tbl
    w_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"] -- writes --> T
    w_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"] -- writes --> T
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"]
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"]
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (2)

- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Refresh_TimesheetETL`
- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Update_TimesheetETL`

## Readers (3)

- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Update_PeopleTimeSheet`
- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Update_TimeSheetHours`
- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Update_TimesheetETL`

---
