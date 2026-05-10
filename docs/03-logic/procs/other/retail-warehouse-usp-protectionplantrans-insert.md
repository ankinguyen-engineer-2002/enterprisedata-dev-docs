# `usp_ProtectionPlanTrans_Insert`

_Schema: `Retail_Sales_Enh` · Warehouse: `Retail_Warehouse` · Family: `other`_

_Modified: 2026-01-21 21:48:10.600000 · Code size: 10,815 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 6 sources and writes to 5 sinks. Calls 3 other procs. Has error handling (TRY/CATCH). Uses explicit transaction. ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `Retail_Sales_Enh.ProtectionPlanSalesTrans`
- `Retail_Sales_Wrk.ProtectionPlanQueue`
- `Retail_Sales_Wrk.ProtectionPlanTrans`
- `Source_Data.Retail_Corporate`
- `wppq`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `Retail_Sales_Wrk.ProtectionPlanQueue`
- `Retail_Sales_Wrk.ProtectionPlanTrans`
- `wppq`
- `wppt`

## Calls (EXEC)

- `ETL_Framework.DW_Developer`
- `Retail_Sales_Wrk.usp_ProtectionPlanTrans_Bulk`
- `Retail_Sales_Wrk.usp_ProtectionPlanTrans_Delivered_Bulk`

## Code (first 80 lines)

```sql
CREATE PROCEDURE [Retail_Sales_Enh].[usp_ProtectionPlanTrans_Insert]
AS

BEGIN

	SET NOCOUNT ON;

	DECLARE
			@String VARCHAR(5000),
			@DateValue DATETIME,
			@User VARCHAR(500),
			@DestinationDatabase VARCHAR(150),
			@DestinationSchema VARCHAR(150),
			@DestinationTable VARCHAR(150);
			      
	SET @String = 'Retail_Sales_Enh.usp_ProtectionPlanTrans_Insert';
	SET @User = SYSTEM_USER;
	SET @DateValue = GETDATE();
	SET @DestinationDatabase = 'Retail_Warehouse';
	SET @DestinationSchema = 'Retail_Sales_Enh';
	SET @DestinationTable = 'ProtectionPlanSalesTrans';

	SELECT
		@DateValue = CSTDateValue
	FROM [ETL_Framework].[DW_Developer].fn_GetDate(@DateValue);

	INSERT INTO [ETL_Framework].[DW_Developer].[AuditLog]
	VALUES
	(
		@String, @DateValue, @User, 'Process Start'
	);

	BEGIN TRY

		DECLARE @_TransDate DATE = GETDATE()-1

		DECLARE @TransDate DATE;

		SELECT @TransDate  = @_TransDate;

		TRUNCATE TABLE [Retail_Sales_Wrk].[ProtectionPlanTrans];

		TRUNCATE TABLE [Retail_Sales_Wrk].[ProtectionPlanQueue];

		IF OBJECT_ID('tempdb..#TransCode') IS NOT NULL 
		DROP TABLE #TransCode;

		SELECT 
			TransCodeID
			, CASE 
				WHEN TransCodeID BETWEEN 0 AND 9 THEN 1
				WHEN TransCodeID = 20 THEN 1
				WHEN TransCodeID IN (30, 31, 34, 37, 50) THEN -1
				WHEN TransCodeID IN (60, 61, 63, 66) THEN 0
				ELSE NULL
			END AS TransCodeMultiplier
			, Description
		INTO #TransCode
		FROM [Source_Data].[Retail_Corporate].[TransCode]
		WHERE Description <> '<Unknown>';
		
		IF OBJECT_ID('tempdb..#ORD') IS NOT NULL 
		DROP TABLE #ORD;

		SELECT	
			OrderID
			, MAX(TransDate) AS TransDate
		INTO #ORD
		FROM
		(
			SELECT	
				o.OrderID
				, CAST(COALESCE(MAX(o.DateChanged), MAX(o.DateCreated)) AS DATE) AS TransDate
			FROM [Source_Data].[Retail_Corporate].[Orders] AS o
			WHERE CAST(COALESCE(o.DateChanged, o.DateCreated) AS DATE) >= @TransDate
			AND o.TransCodeID NOT IN (3, 6, 63)
			AND o.TransactionSaveTime IS NOT NULL
			GROUP BY o.OrderID
			
			UNION
-- … [328 more lines truncated, full body in data/06-procs-raw.json] --
```

---
