# `usp_Update_SalespersonUPBoardHistory`

_Schema: `Retail_Sales_Enh` · Warehouse: `Retail_Warehouse` · Family: `refresh`_

_Modified: 2026-03-24 09:01:31.630000 · Code size: 20,637 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 12 sources and writes to 3 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `FilteredSalesPerson`
- `Holding`
- `RankedMasterData`
- `RankedSalesPerson`
- `Retail_Sales_Enh.SalesPersonUPBoardHistory`
- `Retail_Sales_Enh.SalesPersonUPBoardHistoryAGRHolding`
- `SalesPersonUPBoardHistory_test_20260312`
- `Source_Data.MasterData_Retail`
- `Source_Data.Retail_Corporate`
- `Source_Data.Retail_External`
- `Source_Data.Retail_Miniapps`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `Retail_Sales_Enh.SalesPersonUPBoardHistory`
- `Retail_Sales_Enh.SalesPersonUPBoardHistoryAGRHolding`

## Calls (EXEC)

- `ETL_Framework.DW_Developer`

## Code (first 80 lines)

```sql
CREATE       PROCEDURE [Retail_Sales_Enh].[usp_Update_SalespersonUPBoardHistory]
AS
BEGIN

	DECLARE
            @String VARCHAR(5000),
            @DateValue DATETIME,
            @User VARCHAR(500),
			@DestinationDatabase VARCHAR(150),
			@DestinationSchema VARCHAR(150),
			@DestinationTable VARCHAR(150);

    SET @String = 'Retail_Sales_Enh.usp_Update_SalespersonUPBoardHistory';
    SET @User = SYSTEM_USER;
    SET @DateValue = GETDATE()
	SET @DestinationDatabase = 'Retail_Warehouse'
	SET @DestinationSchema = 'Retail_Sales_Enh'
	SET @DestinationTable = 'SalesPersonUPBoardHistory';

    SELECT
        @DateValue = CSTDateValue
    FROM [ETL_Framework].[DW_Developer].fn_GetDate(@DateValue);

    INSERT INTO [ETL_Framework].[DW_Developer].[AuditLog]
    VALUES
    (
        @String, @DateValue, @User, 'Process Start'
    );

	BEGIN TRY

		--TRUNCATE TABLE [Retail_Sales_Enh].[SalesPersonUPBoardHistory];
		
/*		DECLARE @StartTransDate DATE
				, @EndTransDate DATE;

		SELECT @EndTransDate = MAX(SalespersonUPBoardHistoryStatusStart)
		FROM [Source_Data].[MasterData_Retail].[SalespersonUPBoardHistoryAGR];

		SET @StartTransDate = DATEADD(DAY, -1, @EndTransDate);
*/		
		DECLARE @StartTransDate DATE = GETDATE()-31
				, @EndTransDate DATE = GETDATE();

		DECLARE	@Date3AM DATETIME2(3)
				, @NextDate3AM DATETIME2(3);
		SELECT	@Date3AM = CONVERT(DATETIME2(3), FORMAT(DATEADD(hh, 3, DATEADD(dd, DATEDIFF(dd, 0, @StartTransDate), 0)), 'yyyyMMdd H:00:00'))
				, @NextDate3AM = CONVERT(DATETIME2(3), FORMAT(DATEADD(hh, 27, DATEADD(dd, DATEDIFF(dd, 0, @EndTransDate), 0)), 'yyyyMMdd H:00:00'));
		
		IF OBJECT_ID('tempdb..#Store') IS NOT NULL
		DROP TABLE #Store;

		SELECT 
			ss.StoreID AS ScoreboardStoreID
			, CASE WHEN ss.StoreNumber = 16090 THEN 421
				WHEN ss.StoreNumber = 16198 THEN 622
				WHEN ss.StoreNumber = 16736 THEN 720
				WHEN ss.StoreNumber = 16680 THEN 719
				WHEN ss.StoreNumber = 7521 THEN 342
				WHEN ss.StoreNumber = 7551 THEN 332
				WHEN ss.StoreNumber = 99999 THEN 999
				ELSE st.RetailSystemNumber END AS StoreID
			, ss.StoreName
		INTO #Store
		FROM [Source_Data].[MasterData_Retail].[ScoreboardStore] ss
		LEFT JOIN [Source_Data].[MasterData_Retail].[SiteMasterLocations] st
		ON (LEN(ss.StoreNumber) = 3 AND LTRIM(ss.StoreNumber, '0') = st.RetailSystemNumber)
		OR (LEN(ss.StoreNumber) <> 3 AND ss.StoreNumber = st.financialUnitNumber);

		IF OBJECT_ID('tempdb..#SalesPerson') IS NOT NULL
		DROP TABLE #SalesPerson;

		;WITH RankedSalesPerson AS 
		(
			SELECT	
				-- s.EmployeeNbr AS EmployeeNumber
				COALESCE(s.EmployeeNbr, ei.EmployeeNumber, s1.EmployeeNbr) AS EmployeeNumber
				, IIF(ISNULL(sm.people_id, 0) > 0, sm.people_id, NULL) AS PeopleID
				, sm.active_status AS ActiveStatus
				, COALESCE(s.SalespersonID, spx.SalespersonID) AS SalesPersonID
-- … [517 more lines truncated, full body in data/06-procs-raw.json] --
```

---
