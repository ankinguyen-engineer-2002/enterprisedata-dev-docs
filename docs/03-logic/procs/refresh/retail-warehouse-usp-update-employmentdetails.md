# `usp_Update_EmploymentDetails`

_Schema: `MasterData_HR_UKG_DSG_Enh` · Warehouse: `Retail_Warehouse` · Family: `refresh`_

_Modified: 2026-01-06 17:55:58.013000 · Code size: 26,278 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 8 sources and writes to 5 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `MasterData_HR_UKG_DSG_Enh.ChangeLogEmployeesData`
- `MasterData_HR_UKG_DSG_Enh.CompanyDetails`
- `MasterData_HR_UKG_DSG_Enh.EmploymentDetails`
- `MasterData_HR_UKG_DSG_Enh.Jobs`
- `MasterData_HR_UKG_DSG_Enh.OrgLevel`
- `MasterData_HR_UKG_DSG_Enh.PersonDetails`
- `Source_Data.MasterData_HR_UKG_DSG`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `MasterData_HR_UKG_DSG_Enh.ChangeLogEmployeesData`
- `MasterData_HR_UKG_DSG_Enh.EmploymentDetails`
- `ed`
- `wed`

## Calls (EXEC)

- `ETL_Framework.DW_Developer`

## Code (first 80 lines)

```sql
CREATE PROCEDURE [MasterData_HR_UKG_DSG_Enh].[usp_Update_EmploymentDetails]
AS

BEGIN

	DECLARE
            @String VARCHAR(5000),
            @DateValue DATETIME,
            @User VARCHAR(500),
			@DestinationDatabase VARCHAR(150),
			@DestinationSchema VARCHAR(150),
			@DestinationTable VARCHAR(150);
			      
    SET @String = 'MasterData_HR_UKG_DSG_Enh.usp_Update_EmploymentDetails' ;
    SET @User = SYSTEM_USER;
    SET @DateValue = GETDATE()
	SET @DestinationDatabase = 'Retail_Warehouse'
	SET @DestinationSchema = 'MasterData_HR_UKG_DSG_Enh'
	SET @DestinationTable = 'EmploymentDetails';

    SELECT
        @DateValue = CSTDateValue
    FROM [ETL_Framework].[DW_Developer].fn_GetDate(@DateValue);

    INSERT INTO [ETL_Framework].[DW_Developer].[AuditLog]
    VALUES
    (
        @String, @DateValue, @User, 'Process Start'
    );

    BEGIN TRY

		IF OBJECT_ID('tempdb..#wrk_EmploymentDetails') IS NOT NULL 
		DROP TABLE #wrk_EmploymentDetails;

		SELECT	
			wed.*
			, ROW_NUMBER() OVER (PARTITION BY wed.employeeNumber ORDER BY wed.employeeStatusCode, wed.dateTimeCreated DESC) AS indexx
			, ROW_NUMBER() OVER (PARTITION BY wed.employeeID ORDER BY wed.employeeStatusCode, wed.dateTimeCreated DESC) AS indexx2
		INTO #wrk_EmploymentDetails
		FROM [Source_Data].[MasterData_HR_UKG_DSG].[EmploymentDetails] wed;


		DELETE FROM #wrk_EmploymentDetails 
		WHERE indexx>1;

		DELETE FROM #wrk_EmploymentDetails 
		WHERE indexx2>1;

		IF OBJECT_ID('tempdb..#EmploymentDetailsRaw') IS NOT NULL 
		DROP TABLE #EmploymentDetailsRaw;

		SELECT	
			wed.*
			, pd.PersonDetailKey
			, cd.CompanyDetailKey AS CompanyKey
			, j.JobKey AS PrimaryJobKey
			, ol1.OrgLevelKey AS OrgLevel1Key
			, ol2.OrgLevelKey AS OrgLevel2Key
			, ol3.OrgLevelKey AS OrgLevel3Key
			, ol4.OrgLevelKey AS OrgLevel4Key
			, 0 AS IsModified
 		INTO #EmploymentDetailsRaw
		FROM #wrk_EmploymentDetails wed
		LEFT JOIN [MasterData_HR_UKG_DSG_Enh].[PersonDetails] pd 
		ON pd.EmployeeID = wed.employeeID
		LEFT JOIN [MasterData_HR_UKG_DSG_Enh].[CompanyDetails] cd 
		ON cd.CompanyID = wed.companyID
		LEFT JOIN [MasterData_HR_UKG_DSG_Enh].[Jobs] j 
		ON j.JobCode = wed.primaryJobCode
		LEFT JOIN [MasterData_HR_UKG_DSG_Enh].[OrgLevel] ol1 
		ON ol1.OrgCode = wed.orgLevel1Code 
		AND ol1.OrgLevel = 1 
		LEFT JOIN [MasterData_HR_UKG_DSG_Enh].[OrgLevel] ol2 
		ON ol2.OrgCode = wed.orgLevel2Code 
		AND ol2.OrgLevel = 2 
		LEFT JOIN [MasterData_HR_UKG_DSG_Enh].[OrgLevel] ol3 
		ON ol3.OrgCode = wed.orgLevel3Code 
		AND ol3.OrgLevel = 3 
		LEFT JOIN [MasterData_HR_UKG_DSG_Enh].[OrgLevel] ol4 
-- … [837 more lines truncated, full body in data/06-procs-raw.json] --
```

---
