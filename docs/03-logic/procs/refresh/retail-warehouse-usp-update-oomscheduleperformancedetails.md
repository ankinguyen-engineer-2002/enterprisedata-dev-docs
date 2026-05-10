# `usp_Update_OOMSchedulePerformanceDetails`

_Schema: `Retail_OOM_Enh` · Warehouse: `Retail_Warehouse` · Family: `refresh`_

_Modified: 2026-01-21 21:47:57.290000 · Code size: 26,728 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 6 sources and writes to 3 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `Retail_OOM_Enh.OOMSchedulePerformanceDetails`
- `Retail_OOM_Enh.OrderTransDetail`
- `Retail_OOM_Enh.OrderTransDetailDailyStat`
- `Retail_OOM_Wrk.OrderTransDetailDailyStat`
- `Source_Data.Retail_Corporate`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `OOMSSPDTL`
- `Retail_OOM_Enh.OOMSchedulePerformanceDetails`

## Calls (EXEC)

- `ETL_Framework.DW_Developer`

## Code (first 80 lines)

```sql
CREATE   PROCEDURE [Retail_OOM_Enh].[usp_Update_OOMSchedulePerformanceDetails]
AS
BEGIN

	DECLARE
			@String VARCHAR(5000),
			@DateValue DATETIME,
			@User VARCHAR(500),
			@DestinationDatabase VARCHAR(150),
			@DestinationSchema VARCHAR(150),
			@DestinationTable VARCHAR(150);
			      
	SET @String = 'Retail_OOM_Enh.usp_Update_OOMSchedulePerformanceDetails';
	SET @User = SYSTEM_USER;
	SET @DateValue = GETDATE();
	SET @DestinationDatabase = 'Retail_Warehouse';
	SET @DestinationSchema = 'Retail_OOM_Enh';
	SET @DestinationTable = 'OOMSchedulePerformanceDetails';

	SELECT
		@DateValue = CSTDateValue
	FROM [ETL_Framework].[DW_Developer].fn_GetDate(@DateValue);

	INSERT INTO [ETL_Framework].[DW_Developer].[AuditLog]
	VALUES
	(
		@String, @DateValue, @User, 'Process Start'
	);

	BEGIN TRY
	
		--Variables
		DECLARE @TransDate DATE = DATEADD(DAY, -1, CAST(GETDATE() AS DATE)),
				@AttackTargetNumPreviousDays SMALLINT = 3,
				@FilledCleanTarget DECIMAL(13, 2) = 3000000;
		
		-----------------------------------------------------------------------------------------------------
		--WrittenSales
		-----------------------------------------------------------------------------------------------------
		IF OBJECT_ID('tempdb..#WrittenSales') IS NOT NULL 
		DROP TABLE #WrittenSales;

		SELECT  
			store_b.STORE_ID AS BookedStoreID
			, store_dc.STORE_ID AS DCStoreID
			, COALESCE(SUM(oi.QtyOrdered * oi.CaseSellingPrice),0) as WrittenSales
			,oi.OrderID
		INTO #WrittenSales
		FROM [Source_Data].[Retail_Corporate].[Orders] AS o
		INNER JOIN [Source_Data].[Retail_Corporate].[OrderItem] AS oi 
		ON oi.OrderID = o.OrderID
		OUTER APPLY 
		(
			SELECT TOP 1 STORE_ID
			FROM 
			(
				SELECT oi2.BookedStoreID AS STORE_ID
				FROM [Source_Data].[Retail_Corporate].[OrderItem] oi2 
				WHERE oi2.OrderID = oi.OrderID
				and oi2.RecStatus <> 'D'
				
				UNION
				
				SELECT ii2.BookedStoreID AS STORE_ID
				FROM [Source_Data].[Retail_Corporate].[InvoiceItem] ii2 
				WHERE ii2.OrderID = oi.OrderID
			) R
		) AS store_b 
		OUTER APPLY 
		(
			SELECT TOP 1 STORE_ID
			FROM 
			(
				SELECT oi3.StoreID AS STORE_ID
				FROM [Source_Data].[Retail_Corporate].[OrderItem] oi3 
				WHERE oi3.OrderID = oi.OrderID
				and oi3.RecStatus <> 'D'
				
				UNION
			
-- … [657 more lines truncated, full body in data/06-procs-raw.json] --
```

---
