# 🔍 `MasterData_HR_UKG_Enh.PersonDetails`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["MasterData_HR_UKG_Enh.PersonDetails"]:::tbl
    w_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"] -- writes --> T
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"]
    T -- read by --> r_retail-warehouse-mas["⚙️ Retail_Warehouse.MasterData_HR_UKG_Enh.u"]
    T -- read by --> r_retail-warehouse-mas["👁️ Retail_Warehouse.MasterData_HR_UKG_Enh_W"]
    T -- read by --> r_retail-warehouse-mas["👁️ Retail_Warehouse.MasterData_HR_UKG_Enh_W"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (1)

- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Update_PersonDetails`

## Readers (4)

- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Update_EmploymentDetails`
- ⚙️ `Retail_Warehouse.MasterData_HR_UKG_Enh.usp_Update_PersonDetails`
- 👁️ `Retail_Warehouse.MasterData_HR_UKG_Enh_Wrk.v_EmployeeSupervisor`
- 👁️ `Retail_Warehouse.MasterData_HR_UKG_Enh_Wrk.v_Employees`

---
