# `usp_Update_SalesOrderLineHistory`

_Schema: `Retail_Sales_Enh` · Warehouse: `Retail_Warehouse` · Family: `refresh`_

_Modified: 2026-01-21 21:47:59.697000 · Code size: 19,003 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 10 sources and writes to 7 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). Uses explicit transaction. ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `Enterprise_Lakehouse.Retail_Corporate`
- `ProtectionPlanSalesTrans`
- `Retail_Sales.SalesOrderLineHistory`
- `Retail_Sales_Enh.SalesOrderHeader`
- `Retail_Sales_Enh.SalesOrderLine`
- `Retail_Sales_Enh.SalesOrderLineHistory`
- `Source_Data.Retail_Corporate`
- `Source_Data.Retail_External`
- `tot`

## Outputs (INSERT/UPDATE/MERGE)

- `BTA`
- `ETL_Framework.DW_Developer`
- `Retail_Sales_Enh.SalesOrderLineHistory`
- `bd`
- `bta`
- `sales`
- `sdt`

## Calls (EXEC)

- `ETL_Framework.DW_Developer`

## Code (first 80 lines)

```sql
CREATE PROCEDURE [Retail_Sales_Enh].[usp_Update_SalesOrderLineHistory]
AS

BEGIN

	DECLARE
			@String VARCHAR(5000),
			@DateValue DATETIME,
			@User VARCHAR(500),
			@DestinationDatabase VARCHAR(150),
			@DestinationSchema VARCHAR(150),
			@DestinationTable VARCHAR(150);
			      
	SET @String = 'Retail_Sales_Enh.usp_Update_SalesOrderLineHistory';
	SET @User = SYSTEM_USER;
	SET @DateValue = GETDATE();
	SET @DestinationDatabase = 'Retail_Warehouse';
	SET @DestinationSchema = 'Retail_Sales_Enh';
	SET @DestinationTable = 'SalesOrderLineHistory';

	SELECT
		@DateValue = CSTDateValue
	FROM [ETL_Framework].[DW_Developer].fn_GetDate(@DateValue);

	INSERT INTO [ETL_Framework].[DW_Developer].[AuditLog]
	VALUES
	(
		@String, @DateValue, @User, 'Process Start'
	);

	--SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

	BEGIN TRY

		--TRUNCATE TABLE [Retail_Sales_Enh].[SalesOrderLineHistory];

		DECLARE @StartDate DATE = GETDATE()-3
				, @EndDate DATE = GETDATE();
				
		DELETE FROM [Retail_Sales_Enh].[SalesOrderLineHistory]
		WHERE COALESCE(CAST(DateChanged AS DATE), CAST(DateCreated AS DATE)) BETWEEN @StartDate AND @EndDate;

		IF OBJECT_ID('tempdb..#SalesOrderLineHistoryHolding') IS NOT NULL 
		DROP TABLE #SalesOrderLineHistoryHolding;

		SELECT  
			Source
			, SourceSystem
			, BtaID
			, CASE WHEN Source = 'W' THEN 1 ELSE 6 END AS SalesDataTypeKey
			, AsIsSaleReasonCodeID
			, BaseOrderID
			, SourceOrderID
			, TransDate
			, CONVERT(VARCHAR(8), TransDate, 112) AS TransDateKey
			, LineNumber
			, LineStatus
			, ItemDescription
			, SKU
			, QuantityOrdered
			, NetPrice
			, ProtectionPlanSKU
			, ProtectionPlanID
			, ProtectionPlanPrice
			, ProtectionPlanCost
			, IsServiceItem
			, HasProtectionPlan
			, WarrantyEndDate
			, StoreID
			, KitOrPackageQuantity
			, KitOrPackageSKU
			, NetCost
			, CategoryID
			, GroupID
			, CustomerID
			, DiscountCode
			, DeliveryStoreID
			, DeliveryTypeCodeID
			, SalesPersonID
			, ServiceTypeID
-- … [629 more lines truncated, full body in data/06-procs-raw.json] --
```

---
