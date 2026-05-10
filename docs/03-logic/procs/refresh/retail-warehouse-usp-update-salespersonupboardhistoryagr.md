# `usp_Update_SalespersonUPBoardHistoryAGR`

_Schema: `Retail_Sales` · Warehouse: `Retail_Warehouse` · Family: `refresh`_

_Modified: 2025-10-24 12:08:29.690000 · Code size: 10,806 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 5 sources and writes to 4 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `Retail_Sales.SalesPersonUPBoardHistoryAGR`
- `Retail_Sales.SalesPersonUPBoardHistoryAGRHolding`
- `Source_Data.MasterData_Retail`
- `Source_Data.MasterData_Retail_Wrk`

## Outputs (INSERT/UPDATE/MERGE)

- `DATE`
- `ETL_Framework.DW_Developer`
- `Retail_Sales.SalesPersonUPBoardHistoryAGR`
- `Retail_Sales.SalesPersonUPBoardHistoryAGRHolding`

## Calls (EXEC)

- `ETL_Framework.DW_Developer`

## Code (first 80 lines)

```sql
CREATE PROCEDURE [Retail_Sales].[usp_Update_SalespersonUPBoardHistoryAGR]
AS
BEGIN

	DECLARE
            @String VARCHAR(5000),
            @DateValue DATETIME,
            @User VARCHAR(500),
			@DestinationDatabase VARCHAR(150),
			@DestinationSchema VARCHAR(150),
			@DestinationTable VARCHAR(150);
			      
    SET @String = 'Retail_Sales.usp_Update_SalespersonUPBoardHistoryAGR' ;
    SET @User = SYSTEM_USER;
    SET @DateValue = GETDATE()
	SET @DestinationDatabase = 'Retail_Warehouse'
	SET @DestinationSchema = 'Retail_Sales'
	SET @DestinationTable = 'SalesPersonUPBoardHistoryAGR';

    SELECT
        @DateValue = CSTDateValue
    FROM [ETL_Framework].[DW_Developer].fn_GetDate(@DateValue);

    INSERT INTO [ETL_Framework].[DW_Developer].[AuditLog]
    VALUES
    (
        @String, @DateValue, @User, 'Process Start'
    );

	BEGIN TRY
 
		DECLARE @StartTransDate DATE = GETDATE()-1,
				@EndTransDate DATE = GETDATE();

		DECLARE	@Date3AM DATETIME2(3),
				@NextDate3AM DATETIME2(3);
		SELECT	@Date3AM = CONVERT(DATETIME2(3), FORMAT(DATEADD(hh, 3, DATEADD(dd, DATEDIFF(dd, 0, @StartTransDate), 0)), 'yyyyMMdd H:00:00')),
				@NextDate3AM = CONVERT(DATETIME2(3), FORMAT(DATEADD(hh, 27, DATEADD(dd, DATEDIFF(dd, 0, @EndTransDate), 0)), 'yyyyMMdd H:00:00'));
 
		IF OBJECT_ID('tempdb..#wrk_SalespersonUPBoardHistory') IS NOT NULL
		DROP TABLE #wrk_SalespersonUPBoardHistory;

		SELECT	
			SalespersonUPBoardHistoryID AS HistoryID
			, StoreID
			, SalespersonID
			, SalespersonUPBoardStatusID AS StatusID
			, SalespersonUPBoardHistorySequence AS HistorySequence
			, SalespersonUPBoardHistoryStatusStart AS HistoryStatusStart
			, SalespersonUPBoardHistoryStatusEnd AS HistoryStatusEnd
			, SalespersonRotationTypeID
			, SalespersonUPBoardHistoryGuestName AS HistoryGuestName
			, SalespersonUPBoardHistoryGuestDescription AS HistoryGuestDescription
			, SalespersonUPBoardHistoryGuestCount AS HistoryGuestCount
			, SalespersonUPBoardHistoryIsCloseSale AS HistoryIsCloseSale
			, SalespersonUPBoardHistoryIsProspect AS HistoryIsProspect
			, SalespersonUPBoardHistoryLocalTimeStatusStart AS HistoryLocalTimeStatusStart
			, SalespersonUPBoardHistoryLocalTimeStatusEnd AS HistoryLocalTimeStatusEnd
			, SalespersonUPBoardHistoryGuestPhoneNumber AS HistoryGuestPhoneNumber
			, SalespersonUPBoardHistoryGuestProspecting AS HistoryGuestProspecting
			, SalespersonUPBoardHistoryIsSaleOverThreshold AS HistoryIsSaleOverThreshold
			, SalespersonUPBoardHistoryOverflowCount AS HistoryOverflowCount
			, SalespersonUPBoardHistoryIsSleepAssessment AS HistoryIsSleepAssessment
			, SalespersonUPBoardID AS ID
			, SalespersonUPBoardHistoryStrikeOuts AS HistoryStrikeOuts
			, IsUp AS HistoryCount
			, SalespersonUPBoardHistoryCompleted AS HistoryCompleted
			, IsShot
			, WasFinanceApplicationCreated
			, SalespersonUPBoardReasonManagerAddWith AS ReasonManagerAddWith
			, SalespersonUPBoardReasonManagerAddSP AS ReasonManagerAddSP
			, SalespersonUPBoardReasonManagerAddUps AS ReasonManagerAddUps
			, SalespersonUPBoardReasonManagerRemoveSP AS ReasonManagerRemoveSP
			, SalespersonUPBoardManagerCoachingNotes AS ManagerCoachingNotes
			, CoachingNotesCreationDate AS ManagerCoachingNotesTime
			, IsStrike
			, IsStrikeOut
			, ConsecutiveStrikes
			, ConsecutiveStrikeOuts
		INTO #wrk_SalespersonUPBoardHistory
-- … [244 more lines truncated, full body in data/06-procs-raw.json] --
```

---
