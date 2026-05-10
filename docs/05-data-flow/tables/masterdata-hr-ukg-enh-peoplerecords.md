# 🔍 `MasterData_HR_UKG_Enh.PeopleRecords`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["MasterData_HR_UKG_Enh.PeopleRecords"]:::tbl
    w_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"] -- writes --> T
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"]
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"]
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"]
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (1)

- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Update_PeopleRecords`

## Readers (4)

- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Update_HREmployeeHistory`
- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Update_PeopleRecords`
- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Update_PeopleTimeSheet`
- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Update_TimeSheetHours`

---
