# `usp_Update_OrderTransDetail`

_Schema: `Retail_OOM_Enh` · Warehouse: `Retail_Warehouse` · Family: `refresh`_

_Modified: 2026-02-05 22:10:10.680000 · Code size: 10,997 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 5 sources and writes to 3 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `Retail_OOM_Enh.OrderChangeRegistry`
- `Retail_OOM_Enh.OrderTransDetail`
- `Retail_OOM_Wrk.OrderComments`
- `Source_Data.Retail_Corporate`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `Retail_OOM_Enh.OrderTransDetail`
- `otd`

## Calls (EXEC)

- `ETL_Framework.DW_Developer`

## Code (first 80 lines)

```sql
CREATE PROCEDURE [Retail_OOM_Enh].[usp_Update_OrderTransDetail]
AS
BEGIN

	DECLARE
			@String VARCHAR(5000),
			@DateValue DATETIME,
			@User VARCHAR(500),
			@DestinationDatabase VARCHAR(150),
			@DestinationSchema VARCHAR(150),
			@DestinationTable VARCHAR(150);
			      
	SET @String = 'Retail_OOM_Enh.usp_Update_OrderTransDetail';
	SET @User = SYSTEM_USER;
	SET @DateValue = GETDATE();
	SET @DestinationDatabase = 'Retail_Warehouse';
	SET @DestinationSchema = 'Retail_OOM_Enh';
	SET @DestinationTable = 'OrderTransDetail';

	SELECT
		@DateValue = CSTDateValue
	FROM [ETL_Framework].[DW_Developer].fn_GetDate(@DateValue);

	INSERT INTO [ETL_Framework].[DW_Developer].[AuditLog]
	VALUES
	(
		@String, @DateValue, @User, 'Process Start'
	);

	BEGIN TRY

		--TRUNCATE TABLE [Retail_OOM_Enh].[OrderTransDetail];

		DECLARE @MaxID BIGINT = (SELECT ISNULL(MAX(OrderTransDetailID), 0) FROM [Retail_OOM_Enh].[OrderTransDetail]);
		
		IF OBJECT_ID('tempdb..#OrderTrans') IS NOT NULL 
		DROP TABLE #OrderTrans;

		SELECT
			 OrderID
			, ItemID
			, ProductID
			, WrittenDate
			, VendorModelNumber
			, KitGroupNumber
			, TransCodeID
			, Quantity
			, UnitListPrice
			, UnitSellPrice
			, UnitCost
			, OtherDiscount
			, ProductDiscountCode
			, SpecialOrderFlag
			, AsIsReasonCodeID
			, DateCreated
			, DateChanged
			, DeliveryDate
			, DeliveryStatus
			, DeliveryStatusAtPOS
			, DeliveryType
			, DeliveryStoreID
			, StockLocationID
			, ReasonCodeID
			, PriceOverrideStaffID
		INTO #OrderTrans
		FROM
		(
			/* Open or Voided OrderItem Lines */
			SELECT
				oi.OrderID
				, oi.ItemID
				, oi.ProductID
				, oi.WrittenDate
				, CASE WHEN oi.SpecOrderFlg = 1 THEN oi.SpecialOrder_Frame ELSE p.VendorModelNbr END AS VendorModelNumber
				, oi.KitGroupNumber
				, oi.TransCodeID
				, oi.QtyOrdered AS Quantity
				, oi.CasePriceDefault AS UnitListPrice
				, oi.CaseSellingPrice AS UnitSellPrice
				, oi.LineCost / NULLIF(oi.QtyOrdered, 0) AS UnitCost
-- … [336 more lines truncated, full body in data/06-procs-raw.json] --
```

---
