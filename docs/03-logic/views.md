# 👁️ Views (145 user views)

[← Logic](README.md) · [← Root](../../README.md)

## What is a view here?

A T-SQL view that wraps SELECT/JOIN/WHERE business logic. The **`_Wrk` naming convention** = Working set views consumed by `usp_RefreshCuratedTableFromView` family of procs.

Pattern: `INSERT INTO target_curated_table SELECT * FROM domain_Wrk.SomeView`

## Distribution by container

| Container | User views |
|---|---|
| `Wholesale_Warehouse` | 114 |
| `Retail_Warehouse` | 29 |
| `ETL_Framework` | 2 |

## Wholesale_Warehouse `_Wrk` schemas (114 views)

| Schema | Views | Sample names |
|---|---|---|
| `Marketing_Wrk` | 35 | `v_AFValueList`, `v_AdFundsRequest`, `v_AdNotice`, … +32 |
| `CustomerOrders_AFI_Wrk` | 24 | `v_CreditCodes`, `v_DashboardValueList`, `v_ExtendedOrder`, … +21 |
| `Pricing_AFI_Wrk` | 20 | `v_BuyGroupDefault`, `v_BuyGroupMaster`, `v_BuyGroupMember`, … +17 |
| `SalesHistory_AFI_Wrk` | 12 | `v_InvoiceConsumerInformation`, `v_InvoiceDetail`, `v_InvoiceDetailProperties`, … +9 |
| `PartyContacts_Wrk` | 9 | `v_AddressMaster`, `v_CommunicationInfo`, `v_ContactBase`, … +6 |
| `Customers_Wrk` | 7 | `v_AccountMaster`, `v_CustomerCredit`, `v_DeliveryWindow`, … +4 |
| `Quality_AFI_Wrk` | 5 | `v_DamageCodes`, `v_ReplacementPartDetail`, `v_ReplacementPartHeader`, … +2 |
| `ProductSourcing_AFI_Wrk` | 1 | `v_ControlAllocationItems` |
| `Purchasing_AFI_Wrk` | 1 | `v_VendorMaster` |

## Retail_Warehouse `_Wrk` schemas (29 views)

| Schema | Views | Sample names |
|---|---|---|
| `Retail_Sales_Wrk` | 14 | `v_BucketInventory`, `v_BucketOrderItem`, `v_BucketPOI` |
| `MasterData_Ent_Wrk` | 4 | `v_CustomerInfo`, `v_PaymentType`, `v_ReasonCode` |
| `MasterData_Retail_Ent_Wrk` | 4 | `v_SalesPerson`, `v_StoreLocation`, `v_StoreLocationCalendar` |
| `MasterData_HR_UKG_Enh_Wrk` | 3 | `v_EmployeeSupervisor`, `v_Employees`, `v_Timesheet` |
| `MasterData_Product_Wrk` | 3 | `v_ProductGroup`, `v_ProductInfo`, `v_ProductSeries` |
| `MasterData_HR_UKG_DSG_Enh_Wrk` | 1 | `v_Employees` |

## 📂 Drill-down

Full view definitions → [`data/07-views-raw.json`](../../data/07-views-raw.json) (408 KB raw)

---
