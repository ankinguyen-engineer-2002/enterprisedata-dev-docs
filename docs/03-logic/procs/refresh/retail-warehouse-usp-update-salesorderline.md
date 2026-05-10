# `usp_Update_SalesOrderLine`

_Schema: `Retail_Sales_Enh` · Warehouse: `Retail_Warehouse` · Family: `refresh`_

_Modified: 2026-03-29 14:23:58.550000 · Code size: 30,838 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 8 sources and writes to 8 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). Uses explicit transaction. ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `Centralized_Lakehouse.Retail_Corporate`
- `Centralized_Lakehouse.Retail_External`
- `ETL_Framework.DW_Developer`
- `Retail_Sales.SalesAssociateCommission`
- `Retail_Sales.SalesOrderLine`
- `Retail_Sales.SalesOrderLineHistory`
- `Retail_Sales.SalesOrderProductInfo`
- `Retail_Sales_Enh.SalesOrderLine`

## Outputs (INSERT/UPDATE/MERGE)

- `Conflict`
- `Date`
- `Deleted`
- `ETL_Framework.DW_Developer`
- `Line`
- `Retail_Sales_Enh.SalesOrderLine`
- `SFMCLineFulfillmentStatus*/`
- `odi`

## Calls (EXEC)

- `ETL_Framework.DW_Developer`

## Code (first 80 lines)

```sql
CREATE PROCEDURE [Retail_Sales_Enh].[usp_Update_SalesOrderLine]
AS

BEGIN

	DECLARE
			@String VARCHAR(5000),
			@DateValue DATETIME,
			@User VARCHAR(500),
			@DestinationDatabase VARCHAR(150),
			@DestinationSchema VARCHAR(150),
			@DestinationTable VARCHAR(150);
			      
	SET @String = 'Retail_Sales_Enh.usp_Update_SalesOrderLine';
	SET @User = SYSTEM_USER;
	SET @DateValue = GETDATE();
	SET @DestinationDatabase = 'Retail_Warehouse';
	SET @DestinationSchema = 'Retail_Sales_Enh';
	SET @DestinationTable = 'SalesOrderLine';

	SELECT
		@DateValue = CSTDateValue
	FROM [ETL_Framework].[DW_Developer].fn_GetDate(@DateValue);

	INSERT INTO [ETL_Framework].[DW_Developer].[AuditLog]
	VALUES
	(
		@String, @DateValue, @User, 'Process Start'
	);

	--SET TRANSACTION ISOLATION LEVEL SERIALIZABLE; --For Snapshot Isolation and Update Conflict Error

	BEGIN TRY

		DECLARE @MaxID BIGINT = (SELECT ISNULL(MAX(OrderDetailKey),0) FROM [Retail_Sales_Enh].[SalesOrderLine]);

		--TRUNCATE TABLE [Retail_Sales_Enh].[SalesOrderLine];

		IF OBJECT_ID('tempdb..#OrderItemProductInfo') IS NOT NULL 
		DROP TABLE #OrderItemProductInfo;

		SELECT *
		INTO #OrderItemProductInfo
		FROM [Retail_Sales].[SalesOrderProductInfo]
		WHERE InfoStatus = 'Written';

		IF OBJECT_ID('tempdb..#InvoiceItemProductInfo') IS NOT NULL 
		DROP TABLE #InvoiceItemProductInfo;

		SELECT *
		INTO #InvoiceItemProductInfo
		FROM [Retail_Sales].[SalesOrderProductInfo]
		WHERE InfoStatus = 'Invoiced';

		IF OBJECT_ID('tempdb..#OrderItemCommissionInfo') IS NOT NULL 
		DROP TABLE #OrderItemCommissionInfo;

		SELECT *
		INTO #OrderItemCommissionInfo
		FROM [Retail_Sales].[SalesAssociateCommission]
		WHERE CommissionStatus = 'Written';

		IF OBJECT_ID('tempdb..#InvoiceItemCommissionInfo') IS NOT NULL 
		DROP TABLE #InvoiceItemCommissionInfo;

		SELECT *
		INTO #InvoiceItemCommissionInfo
		FROM [Retail_Sales].[SalesAssociateCommission]
		WHERE CommissionStatus = 'Invoiced';

		UPDATE w
		SET w.SerialNumber = CASE WHEN w.TransCodeID = 1 THEN oip.SerialNumber ELSE w.SerialNumber END
			, w.AsIsReasonCodeID = CASE WHEN w.TransCodeID = 1 THEN oip.ReasonCodeID ELSE w.AsIsReasonCodeID END
			, w.DeliveryStatus = ISNULL(w.DeliveryStatus, 'EST')
		FROM 
		(
			SELECT
				SourceOrderID
				, LineNumber
				, SerialNumber
-- … [1074 more lines truncated, full body in data/06-procs-raw.json] --
```

---
