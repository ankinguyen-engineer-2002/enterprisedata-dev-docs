# `usp_DataWarehouseSLAAlert_Fabric`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `alert`_

_Modified: 2026-02-27 10:28:40.017000 · Code size: 17,186 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 6 sources and writes to 5 sinks. ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `DW_Developer.TableDictionary`
- `DW_Developer.fn_GetDate`
- `EDW-Fabric.<br/>'`
- `Performance_Logs.EmailQueue`
- `Performance_Logs.tblSLAAlertSuppressionTracker`
- `SLA`

## Outputs (INSERT/UPDATE/MERGE)

- `Alert`
- `Performance_Logs.EmailQueue`
- `Performance_Logs.tblFabricSLAAlertLog`
- `Performance_Logs.tblFabricSLAAlertLogDetail`
- `Performance_Logs.tblSLAAlertSuppressionTracker`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql

CREATE    PROC [DW_Developer].[usp_DataWarehouseSLAAlert_Fabric]
AS
BEGIN
    SET NOCOUNT ON;
    
    -- =============================================
    -- SLA Monitoring for Fabric Warehouse
    -- =============================================
    -- Description: Monitors tables with SLA configurations and sends alerts when deadlines are breached
    -- Author: Data Engineering Team
    -- Date: 2026-02-13
    -- =============================================
    -- IMPORTANT: Fabric Warehouse Compatibility Notes:
    -- - No DATETIME2 + operator (use DATEADD instead)
    -- - No PRIMARY KEY constraints (handle duplicates in logic)
    -- - No CHECK constraints (validate in code)
    -- - Use CAST for datetime conversions
    -- - All SLA times are in CST (Central Standard Time)
    -- =============================================
    
    DECLARE
        @msgTitle           NVARCHAR(400) = N'FABRIC SLA Breach Alert',
        @msgSubject         NVARCHAR(4000),
        @tableHTML          NVARCHAR(MAX),
        @TablesBreaching    INT = 0,
        @TotalTables        INT = 0,
        @PercentBehind      DECIMAL(10,4) = 0,
        @CriticalCount      INT = 0,
        @HighCount          INT = 0,
        @MediumCount        INT = 0,
        @LowCount           INT = 0,
        @CurrentTime_UTC    DATETIME2(3) = SYSUTCDATETIME(),
        @CurrentTime_CST    DATETIME2(3),
        @CurrentDate_CST    DATE,
        @CurrentTimeOnly    TIME,
        @Recipients         NVARCHAR(MAX) = N'RSteinke@Ashleyfurniture.com;DL_AFI_Analytics_AG_DataWarehouse@Ashleyfurniture.com',
        @SuppressionHours   INT = 4;
    
    -- =============================================
    -- STEP 1: Convert Current UTC Time to CST
    -- =============================================
    SELECT @CurrentTime_CST = CSTDateValue 
    FROM DW_Developer.fn_GetDate(@CurrentTime_UTC);
    
    SET @CurrentDate_CST = CAST(@CurrentTime_CST AS DATE);
    SET @CurrentTimeOnly = CAST(@CurrentTime_CST AS TIME);
    
    -- =============================================
    -- STEP 2: Count Total Tables with SLA Configured
    -- =============================================
    SELECT @TotalTables = COUNT(*)
    FROM DW_Developer.TableDictionary
    WHERE SLA_DeadlineTime IS NOT NULL
      AND SLA_DeadlineTime <> '';
    
    -- =============================================
    -- STEP 3: Identify SLA Breaches
    -- =============================================
    -- Create temp table to store potential breaches
    IF OBJECT_ID('tempdb..#sla_breaches') IS NOT NULL DROP TABLE #sla_breaches;

    SELECT
        td.SchemaName,
        td.TableName,
        td.SLA_DeadlineTime,
        td.SLA_Priority,
        td.Modified AS LastUpdated_UTC,
        td.Modified AS LastUpdated_CST,
        -- Calculate the MOST RECENT SLA Deadline that has passed
        -- This is the SLA deadline for today (if current time >= SLA time) or yesterday (if current time < SLA time)
        -- Use DATEADD to add time components (Fabric doesn't support DATETIME2 + operator)
        CASE
            WHEN @CurrentTimeOnly >= CAST(td.SLA_DeadlineTime AS TIME)
            THEN DATEADD(SECOND,
                    DATEPART(HOUR, CAST(td.SLA_DeadlineTime AS TIME)) * 3600 +
                    DATEPART(MINUTE, CAST(td.SLA_DeadlineTime AS TIME)) * 60 +
                    DATEPART(SECOND, CAST(td.SLA_DeadlineTime AS TIME)),
                    CAST(@CurrentDate_CST AS DATETIME2(3)))
            ELSE DATEADD(SECOND,
-- … [327 more lines truncated, full body in data/06-procs-raw.json] --
```

---
