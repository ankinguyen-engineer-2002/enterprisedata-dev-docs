# 🏬 Wholesale_Warehouse

_PROD tier · ID `c1ef4a62-f8e2-4d55-96bd-33eb07b81b7c`_

[← Warehouses](README.md) · [← Storage](../README.md) · [← Root](../../../README.md)

## 🎯 Purpose

**Silver tier domain warehouse cho wholesale** — 209 tables, 126 _Wrk views, 8 procs (avg 20K chars/proc, MERGE-heavy).

## 📊 Stats

| Metric | Value |
|---|---|
| Tier | PROD |
| Schemas | 28 |
| Tables | 209 |
| Views | 126 |
| Stored Procedures | 8 |
| Workspace ID | `5360a935-1984-4775-895f-f4c90bafa19d` |
| Item ID | `c1ef4a62-f8e2-4d55-96bd-33eb07b81b7c` |

**Highlight:** Most _Wrk views: Marketing_Wrk (35), CustomerOrders_AFI_Wrk (24), Pricing_AFI_Wrk (20), SalesHistory_AFI_Wrk (12), PartyContacts_Wrk (9).

## 🗂️ Schemas

`AFISales_Wrk`, `CustomerOrders_AFI`, `CustomerOrders_AFI_Wrk`, `Customers`, `Customers_Wrk`, `INFORMATION_SCHEMA`, `Marketing`, `Marketing_Wrk`, `PartyContacts`, `PartyContacts_Wrk`, `Placements`, `Placements_Wrk`, `Pricing_AFI`, `Pricing_AFI_Wrk`, `ProductSourcing_AFI`, `ProductSourcing_AFI_Wrk`, `Purchasing_AFI`, `Purchasing_AFI_Wrk`, `Quality_AFI`, `Quality_AFI_Wrk`, `SalesHistory_AFI`, `SalesHistory_AFI_Archive`, `SalesHistory_AFI_Wrk`, `_rsc`, `dbo`, `guest`, `queryinsights`, `sys`

## 📋 Tables (209)

**Top 30 tables (sample):**

| Schema | Table | Rows | Modified |
|---|---|---|---|
| `AFISales_Wrk` | `ItemStatus_MOP` | 0 | 2025-12-05 |
| `AFISales_Wrk` | `ItemStatus_WOP` | 0 | 2025-12-05 |
| `AFISales_Wrk` | `Weekly_History_tmp` | 0 | 2025-12-05 |
| `CustomerOrders_AFI` | `CreditCodes` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `DashboardValueList` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `DashboardValueList_LOAD` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `ExtendedOrder` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OpenOrderAddress` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OpenOrderComments` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OpenOrderConsumerAddress` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OpenOrderConsumerAddress_LOAD` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OpenOrderDetail` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OpenOrderDiscounts` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OpenOrderDiscounts_LOAD` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OpenOrderExtendedItem` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OpenOrderHeader` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OrderArrivalCode` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OrderArrivalGroup` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OrderAuditDetail` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OrderAuditDetail_LOAD` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OrderAuditHeader` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OrderAuditHeader_LOAD` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OrderCancellationReasonCode` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OrderSchedule` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OrderSchedule_LOAD` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `OrderTypeCode` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `RequestDateChangeAudit` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `RequestDateChangeAudit_LOAD` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `RequestDateChangeCode` | 0 | 2025-09-26 |
| `CustomerOrders_AFI` | `RequestDateChangeCode_LOAD` | 0 | 2025-09-26 |

_… and 179 more. Full list in [`data/03-warehouses-raw.json`](../../../data/03-warehouses-raw.json)._

## 👁️ User views (114)

| Schema | Views | Names (sample) |
|---|---|---|
| `CustomerOrders_AFI_Wrk` | 24 | `v_CreditCodes`, `v_DashboardValueList`, `v_ExtendedOrder`, `v_OpenOrderAddress`, `v_OpenOrderComments`, … +19 |
| `Customers_Wrk` | 7 | `v_AccountMaster`, `v_CustomerCredit`, `v_DeliveryWindow`, `v_ExtendedCustomerProfile`, `v_ServiceRepGroup`, … +2 |
| `Marketing_Wrk` | 35 | `v_AFValueList`, `v_AdFundsRequest`, `v_AdNotice`, `v_AdNoticeDetail`, `v_BusinessType`, … +30 |
| `PartyContacts_Wrk` | 9 | `v_AddressMaster`, `v_CommunicationInfo`, `v_ContactBase`, `v_ContactDefaults`, `v_ContactMaster`, … +4 |
| `Pricing_AFI_Wrk` | 20 | `v_BuyGroupDefault`, `v_BuyGroupMaster`, `v_BuyGroupMember`, `v_BuyGroupPrice`, `v_CommissionClass`, … +15 |
| `ProductSourcing_AFI_Wrk` | 1 | `v_ControlAllocationItems` |
| `Purchasing_AFI_Wrk` | 1 | `v_VendorMaster` |
| `Quality_AFI_Wrk` | 5 | `v_DamageCodes`, `v_ReplacementPartDetail`, `v_ReplacementPartHeader`, `v_ScrapCategoryCodes`, `v_ScrapCodes` |
| `SalesHistory_AFI_Wrk` | 12 | `v_InvoiceConsumerInformation`, `v_InvoiceDetail`, `v_InvoiceDetailProperties`, `v_InvoiceHeader`, `v_InvoiceValueAddedTax`, … +7 |

Full view bodies → [`data/07-views-raw.json`](../../../data/07-views-raw.json)

## ⚙️ Stored procedures (8)

| Family | Procs | Examples |
|---|---|---|
| Curated refresh | 5 | `Usp_Refresh_Wholesale_Warehouse`, `usp_RefreshCustomerOrders_AFI`, `Usp_RefreshCustomers`, …+2 |
| Other | 3 | `usp_Rebuild_CustItemMonthlyPlacements`, `usp_Rebuild_CustItemWeeklyPlacements`, `usp_Rebuild_InvoiceWeeklyPlacements` |

Full proc bodies → [`data/06-procs-raw.json`](../../../data/06-procs-raw.json)

---

**Related:** [03 Logic — Stored Procedures](../../03-logic/stored-procs.md) · [04 Orchestration — Pipelines](../../04-orchestration/pipelines.md)
