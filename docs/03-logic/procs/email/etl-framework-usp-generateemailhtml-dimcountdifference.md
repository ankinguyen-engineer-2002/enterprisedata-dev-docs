# `usp_GenerateEmailHTML_DimCountDifference`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `email`_

_Modified: 2026-04-21 11:36:08.363000 · Code size: 7,760 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 3 sources and writes to 2 sinks.

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `EDWCounts`
- `SourceCounts`
- `Source_Data.Retail_External`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.Performance_Logs`
- `Source_Data.Retail_External`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql
CREATE         PROCEDURE [DW_Developer].[usp_GenerateEmailHTML_DimCountDifference]
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @HTML NVARCHAR(MAX);
    DECLARE @TableRows NVARCHAR(MAX);
    DECLARE @TotalNotMatch INT;
    DECLARE  @Recipients  NVARCHAR(MAX) = N'mohali@ashleyfurniture.com;paswini@ashleyfurniture.com;ibalu@ashleyfurniture.com';

    -------------------------------------------------------------------------
    -- Step 1: Clear old data and insert new comparison results
    -------------------------------------------------------------------------
    TRUNCATE TABLE [Source_Data].[Retail_External].[DimCountDifference];

    -- Insert comparison data
    WITH SourceCounts AS (
        SELECT 
            Tablename,
            YearGroup,
            MonthGroup,
            YearMonth,
            COUNTS AS SourceCount
        FROM [Source_Data].[Retail_External].[DSGDimCount]  
        WHERE Tablename NOT IN ('creditrequeststatuscode','OrderComments','PieceInventory','creditapplication','ProductInventory')
    ),
    EDWCounts AS (
        SELECT 
            Tablename,
            YearGroup,
            MonthGroup,
            YearMonth,
            COUNTS AS EDWCount
        FROM [Source_Data].[Retail_External].[EDWDimCount] 
        WHERE Tablename NOT IN ('creditrequeststatuscode','OrderComments','PieceInventory','creditapplication','ProductInventory')
    )
    INSERT INTO [Source_Data].[Retail_External].[DimCountDifference] (
        Tablename,
        YearGroup,
        MonthGroup,
        YearMonth,
        SourceCount,
        EDWCount,
        Difference,
        Status
    )
    SELECT 
        COALESCE(s.Tablename, e.Tablename) AS Tablename,
        COALESCE(s.YearGroup, e.YearGroup) AS YearGroup,
        COALESCE(s.MonthGroup, e.MonthGroup) AS MonthGroup,
        COALESCE(s.YearMonth, e.YearMonth) AS YearMonth,
        ISNULL(s.SourceCount, 0) AS SourceCount,
        ISNULL(e.EDWCount, 0) AS EDWCount,
        ISNULL(s.SourceCount, 0) - ISNULL(e.EDWCount, 0) AS Difference,
        CASE
            WHEN s.SourceCount = e.EDWCount THEN 'Match'
            WHEN ABS(ISNULL(s.SourceCount, 0) - ISNULL(e.EDWCount, 0)) > 1000 THEN 'Not Match'
            ELSE 'Match'
        END AS Status
    FROM SourceCounts s
    FULL OUTER JOIN EDWCounts e
        ON s.Tablename = e.Tablename 
        AND s.YearMonth = e.YearMonth
    ORDER BY 
        Tablename, 
        YearMonth;

    -------------------------------------------------------------------------
    -- Step 2: Count total "Not Match" records
    -------------------------------------------------------------------------
    SELECT @TotalNotMatch = COUNT(*)
    FROM [Source_Data].[Retail_External].[DimCountDifference]
    WHERE Status = 'Not Match';

    -------------------------------------------------------------------------
    -- Step 3: Generate HTML table rows (Only "Not Match", all months)
    -------------------------------------------------------------------------
    SELECT @TableRows = STRING_AGG(
        CAST(
            '<tr>' +
-- … [134 more lines truncated, full body in data/06-procs-raw.json] --
```

---
