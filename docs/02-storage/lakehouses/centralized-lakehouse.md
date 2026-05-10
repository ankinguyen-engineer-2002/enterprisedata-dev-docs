# 💧 Centralized_Lakehouse
_PROD tier · ID `50e11300-9fb4-4e82-876c-7183bb2501ba`_

[← Lakehouses](README.md) · [← Storage](../README.md) · [← Root](../../../README.md)

## 🎯 Purpose

**Shortcut-aggregation layer** — 501 tables / 5.92 B rows nhưng 18 shortcuts trỏ thẳng vào PROD WS Source_Data + Retail_Warehouse. Data thật KHÔNG ở DEV.

## 📊 Stats

| Metric | Value |
|---|---|
| Tier | PROD |
| Tables | 501 |
| Rows (live count) | 5,923,323,398 |
| Schemas-enabled | Yes |
| Item ID | `50e11300-9fb4-4e82-876c-7183bb2501ba` |

**Highlight:** 21 schemas. Twin schemas Retail_Corporate ↔ Retail_Corporate_Prod = 2 shortcuts cùng PROD path.

## 📋 Tables (501)

**Top 30 tables by row count:**

| Schema | Table | Rows |
|---|---|---|
| `Retail_Corporate` | `PieceInventory` | 664,813,365 |
| `Retail_Corporate_Prod` | `PieceInventory` | 664,813,365 |
| `Retail_Corporate` | `ProductInventory` | 288,889,999 |
| `Retail_Corporate_Prod` | `ProductInventory` | 288,889,999 |
| `Retail_Corporate` | `OrderComments` | 152,155,426 |
| `Retail_Corporate_Prod` | `OrderComments` | 152,155,426 |
| `MasterData_Retail` | `GLPostDetail` | 151,780,680 |
| `Retail_Corporate` | `InvactivityRaw` | 137,156,646 |
| `Retail_Corporate_Prod` | `InvactivityRaw` | 137,156,646 |
| `MasterData_HR_UKG_DSG` | `CommonDataApprovals` | 67,287,065 |
| `Retail_Sales_Enh` | `SalesOrderProductInfo` | 63,366,448 |
| `Retail_Sales_Enh` | `SalesAssociateCommission` | 58,344,646 |
| `Retail_Corporate` | `InvoiceItem_ProductInfo` | 57,693,737 |
| `Retail_Corporate_Prod` | `InvoiceItem_ProductInfo` | 57,693,737 |
| `MasterData_Retail` | `GLPost_References` | 57,322,834 |
| `Retail_Dart` | `OrdTransDetailDailyStat` | 57,076,068 |
| `Retail_Corporate` | `BtaData` | 56,322,667 |
| `Retail_Corporate_Prod` | `BtaData` | 56,322,667 |
| `Retail_Sales_Enh` | `SalesOrderLine` | 55,802,189 |
| `Retail_Sales_Enh` | `SalesOrderLine_bkp_PALM` | 55,153,848 |
| `Retail_Corporate` | `InvoiceItem_ProductInfo_HISTORY` | 54,901,205 |
| `Retail_Corporate_Prod` | `InvoiceItem_ProductInfo_HISTORY` | 54,901,205 |
| `Retail_Corporate` | `InvoiceItem_CommissionInfo` | 53,144,684 |
| `Retail_Corporate_Prod` | `InvoiceItem_CommissionInfo` | 53,144,684 |
| `Retail_Corporate` | `InvoiceItem` | 52,064,512 |
| `Retail_Corporate_Prod` | `InvoiceItem` | 52,064,512 |
| `Retail_Corporate` | `InvoiceItem_CommissionInfo_HISTORY` | 50,493,684 |
| `Retail_Corporate_Prod` | `InvoiceItem_CommissionInfo_HISTORY` | 50,493,684 |
| `Retail_Corporate` | `BtaData_Clone` | 50,126,244 |
| `Retail_Corporate_Prod` | `BtaData_Clone` | 50,126,244 |

_… and 471 more._

## 🔗 External shortcuts (18)

| Name | Type | Target host/WS | Path |
|---|---|---|---|
| `Retail_Sales_Enh` | OneLake | WS `ce4e6503…` | `Tables/Retail_Sales_Enh` |
| `Retail_Sales` | OneLake | WS `ce4e6503…` | `Tables/Retail_Sales` |
| `Retail_Miniapps` | OneLake | WS `ce4e6503…` | `Tables/Retail_Miniapps` |
| `Retail_External` | OneLake | WS `ce4e6503…` | `Tables/Retail_External` |
| `Retail_Dart` | OneLake | WS `ce4e6503…` | `Tables/Retail_Dart` |
| `Retail_Corporate_Prod` | OneLake | WS `ce4e6503…` | `Tables/Retail_Corporate` |
| `Retail_Corporate` | OneLake | WS `ce4e6503…` | `Tables/Retail_Corporate` |
| `MasterData_Retail_Ent` | OneLake | WS `ce4e6503…` | `Tables/MasterData_Retail_Ent` |
| `MasterData_Retail` | OneLake | WS `ce4e6503…` | `Tables/MasterData_Retail` |
| `MasterData_Product_Enh` | OneLake | WS `ce4e6503…` | `Tables/MasterData_Product_Enh` |
| `MasterData_Product` | OneLake | WS `ce4e6503…` | `Tables/MasterData_Product` |
| `MasterData_HR_UKG_Wrk` | OneLake | WS `ce4e6503…` | `Tables/MasterData_HR_UKG_Wrk` |
| `MasterData_HR_UKG_Enh` | OneLake | WS `ce4e6503…` | `Tables/MasterData_HR_UKG_Enh` |
| `MasterData_HR_UKG_DSG_Wrk` | OneLake | WS `ce4e6503…` | `Tables/MasterData_HR_UKG_DSG_Wrk` |
| `MasterData_HR_UKG_DSG` | OneLake | WS `ce4e6503…` | `Tables/MasterData_HR_UKG_DSG` |
| `MasterData_HR_UKG_AGR_Wrk` | OneLake | WS `ce4e6503…` | `Tables/MasterData_HR_UKG_AGR_Wrk` |
| `MasterData_HR_UKG_AGR` | OneLake | WS `ce4e6503…` | `Tables/MasterData_HR_UKG_AGR` |
| `masterdata_hr_ukg` | OneLake | WS `ce4e6503…` | `Tables/masterdata_hr_ukg` |

---

**Related:** [06 Cross-Workspace](../../06-cross-workspace/README.md)
