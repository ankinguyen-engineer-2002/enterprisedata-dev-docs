# `usp_Update_WFMTimesheet`

_Schema: `MasterData_HR_UKG_Enh` · Warehouse: `Retail_Warehouse` · Family: `refresh`_

_Modified: 2026-02-05 22:10:10.203000 · Code size: 16,823 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 10 sources and writes to 6 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `MasterData_HR_UKG_Enh.Employees`
- `MasterData_HR_UKG_Enh.PayCodes`
- `MasterData_HR_UKG_Enh.ProcessedPaycodesErrors`
- `MasterData_HR_UKG_Enh.ProcessedSegmentErrors`
- `MasterData_HR_UKG_Enh.WFMTimesheet`
- `Source_Data.MasterData_HR_UKG_DSG`
- `Source_Data.Retail_Miniapps`
- `apps`
- `pcr`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `MasterData_HR_UKG_Enh.ProcessedPaycodesErrors`
- `MasterData_HR_UKG_Enh.ProcessedSegmentErrors`
- `MasterData_HR_UKG_Enh.WFMTimesheet`
- `pc`
- `pcr`

## Calls (EXEC)

- `ETL_Framework.DW_Developer`

## Code (first 80 lines)

```sql
-- no changes needed

CREATE   PROCEDURE [MasterData_HR_UKG_Enh].[usp_Update_WFMTimesheet] 
AS
BEGIN

	DECLARE
            @String VARCHAR(5000),
            @DateValue DATETIME,
            @User VARCHAR(500),
			@DestinationDatabase VARCHAR(150),
			@DestinationSchema VARCHAR(150),
			@DestinationTable VARCHAR(150);
			      
    SET @String = 'MasterData_HR_UKG_Enh.usp_Update_WFMTimesheet';
    SET @User = SYSTEM_USER;
    SET @DateValue = GETDATE()
	SET @DestinationDatabase = 'Retail_Warehouse'
	SET @DestinationSchema = 'MasterData_HR_UKG_Enh'
	SET @DestinationTable = 'WFMTimesheet';

    SELECT
        @DateValue = CSTDateValue
    FROM [ETL_Framework].[DW_Developer].fn_GetDate(@DateValue);

    INSERT INTO [ETL_Framework].[DW_Developer].[AuditLog]
    VALUES
    (
        @String, @DateValue, @User, 'Process Start'
    );

	BEGIN TRY

		DECLARE @MinDate DATE = CAST(DATEADD(DAY, -30, GETDATE()) AS DATE)
				, @MaxDate DATE = CAST(GETDATE() AS DATE)
				, @Today DATE = GETDATE();

		IF OBJECT_ID('tempdb..#Paycodes_PTOs') IS NOT NULL
		DROP TABLE #Paycodes_PTOs;

		SELECT *
        INTO #Paycodes_PTOs
        FROM 
		(
			SELECT 401 PayCodeID
			UNION
			SELECT 301 PayCodeID
			UNION
			SELECT 362 PayCodeID
			UNION
			SELECT 354 PayCodeID
			UNION
			SELECT 251 PayCodeID
			UNION
			SELECT 357 PayCodeID
			UNION
			SELECT 360 PayCodeID
			UNION
			SELECT 253 PayCodeID
			UNION
			SELECT 352 PayCodeID
			UNION
			SELECT 701 PayCodeID
		) AS Paycodes_PTOs;

		--SEGMENTS

		IF OBJECT_ID('tempdb..#segments') IS NOT NULL
		DROP TABLE #segments;

		SELECT	
			segmentId AS SegmentID
			, itemId AS WorkShiftID
			, employeeQualifier AS EmployeeNumber
			, CAST(roundedStartDateTime AS DATETIME2(3)) AS StartDateTime
			, CAST(roundedEndDateTime AS DATETIME2(3)) AS EndDateTime
			, CAST(applyDate AS DATE) ApplyDate
			, durationInSeconds AS DurationInSeconds
			, segmentTypeId AS SegmentTypeID
			, inProgress AS InProgress
-- … [538 more lines truncated, full body in data/06-procs-raw.json] --
```

---
