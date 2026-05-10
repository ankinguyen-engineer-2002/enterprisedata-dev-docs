# `Usp_Refresh_Wholesale_Warehouse`

_Schema: `dbo` · Warehouse: `Wholesale_Warehouse` · Family: `refresh`_

_Modified: 2025-09-26 15:06:46.347000 · Code size: 15,631 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Pure compute — no detected reads/writes (may be utility / control flow). Calls 1 other procs.

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

_(none detected)_

## Outputs (INSERT/UPDATE/MERGE)

_(none detected)_

## Calls (EXEC)

- `ETL_Framework.DW_Developer`

## Code (first 80 lines)

```sql
CREATE Procedure dbo.Usp_Refresh_Wholesale_Warehouse as

---- Customers  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Customers','AccountMaster'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Customers','CustomerCredit' 
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Customers','DeliveryWindow'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Customers','ExtendedCustomerProfile' 
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Customers','ServiceRepGroup' 
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Customers','ServiceRepID' 
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Customers','ShippingLocations' 

---- CustomerOrders_AFI
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','CreditCodes'  --- no view
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','DashboardValueList'
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','ExtendedOrder'  --- date 
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','OpenOrderAddress' 
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','OpenOrderComments' 
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','OpenOrderConsumerAddress' 
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','OpenOrderDetail'
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','OpenOrderDiscounts'  -- no view
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','OpenOrderExtendedItem'  --no view
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','OpenOrderHeader'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','OrderArrivalCode'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','OrderArrivalGroup'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','OrderAuditDetail'  --no view
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','OrderAuditHeader'  --no view
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','OrderCancellationReasonCode'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','OrderSchedule'  --date
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','OrderTypeCode'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','RequestDateChangeAudit'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','RequestDateChangeCode'
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','RouteTimeFenceControl'    
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','RouteZoneControl'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','SchedulerControl'  --dates
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','TermsCode'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','WarehouseFillRequest'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','CustomerOrders_AFI','WarehouseMaster'  

--- Marketing
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','AdFundsRequest'  --data issue
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','AdNotice'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','AdNoticeDetail'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','AFValueList'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','BusinessType'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','BusinessTypeLifeStyleArea'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','CRMAdvertisingFunds'   -- no view
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','CRMVelocityDriver'   -- no view
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','CustomerOwnershipExceptions'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','Divisions'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','FinancialDivision'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','ItemMaster'  --- data conversion varchar to numeric
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','LocationDeliveryMode'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','MarketCommitments'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','MarketCommitmentsSum'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','MarketLookup'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','MarketPotential'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','MarketPotential2' -- no view
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','MoSeriesMargins'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','MrktSpclstMaster'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','MrktSpclstInfo'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','MrktSpclstMaster'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','MrktSpclstRegion'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','PresBillToExceptions'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','ProductLineMaster'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','Regions'  -- date issue
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','RepCustomerFilter'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','SalesCategory'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','SalesTeamMaster'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','SalesTeamMembers'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','SetDetailCustom'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','TerritoryAssignment'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','TravelBooks'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','Marketing','WarRoomCountryCodes'  

--- PartyContacts  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','PartyContacts','AddressMaster'  --issue
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','PartyContacts','CommunicationInfo'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','PartyContacts','ContactBase'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','PartyContacts','ContactDefaults'  
EXEC [ETL_Framework].[DW_Developer].[usp_RefreshCuratedTableFromView] 'Wholesale_Warehouse','PartyContacts','ContactMaster'  --issue
-- … [57 more lines truncated, full body in data/06-procs-raw.json] --
```

---
