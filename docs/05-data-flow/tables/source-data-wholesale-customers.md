# 🔍 `Source_Data.Wholesale_Customers`

[← Tables](README.md) · [← Data Flow](../README.md) · [← Root](../../../README.md)

## Lineage

```mermaid
graph LR
    T["Source_Data.Wholesale_Customers"]:::tbl
    T -- read by --> r_wholesale-warehouse-["👁️ Wholesale_Warehouse.Customers_Wrk.v_Acco"]
    T -- read by --> r_wholesale-warehouse-["👁️ Wholesale_Warehouse.Customers_Wrk.v_Deli"]
    T -- read by --> r_wholesale-warehouse-["👁️ Wholesale_Warehouse.Customers_Wrk.v_Exte"]
    T -- read by --> r_wholesale-warehouse-["👁️ Wholesale_Warehouse.Customers_Wrk.v_Serv"]
    T -- read by --> r_wholesale-warehouse-["👁️ Wholesale_Warehouse.Customers_Wrk.v_Serv"]
    T -- read by --> r_wholesale-warehouse-["👁️ Wholesale_Warehouse.Customers_Wrk.v_Ship"]
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

## Writers (0)

_(no writers detected — possibly read-only or written by external process)_

## Readers (6)

- 👁️ `Wholesale_Warehouse.Customers_Wrk.v_AccountMaster`
- 👁️ `Wholesale_Warehouse.Customers_Wrk.v_DeliveryWindow`
- 👁️ `Wholesale_Warehouse.Customers_Wrk.v_ExtendedCustomerProfile`
- 👁️ `Wholesale_Warehouse.Customers_Wrk.v_ServiceRepGroup`
- 👁️ `Wholesale_Warehouse.Customers_Wrk.v_ServiceRepID`
- 👁️ `Wholesale_Warehouse.Customers_Wrk.v_ShippingLocations`

---
