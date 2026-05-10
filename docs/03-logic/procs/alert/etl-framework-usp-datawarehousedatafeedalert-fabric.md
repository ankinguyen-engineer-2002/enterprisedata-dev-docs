# `usp_DataWarehouseDataFeedAlert_Fabric`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `alert`_

_Modified: 2025-10-29 06:53:45.343000 · Code size: 7,229 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 3 sources and writes to 3 sinks. ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `DW_Developer.TableDictionary`
- `Performance_Logs.EmailQueue`
- `Performance_Logs.tblFabricDataFeedAlertLogDetail`

## Outputs (INSERT/UPDATE/MERGE)

- `Performance_Logs.EmailQueue`
- `Performance_Logs.tblFabricDataFeedAlertLog`
- `Performance_Logs.tblFabricDataFeedAlertLogDetail`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql
CREATE   PROC [DW_Developer].[usp_DataWarehouseDataFeedAlert_Fabric]
AS
BEGIN
   SET NOCOUNT ON;
   DECLARE
       @msgTitle       NVARCHAR(400) = N'FABRIC Table Dictionary Objects that are behind schedule',
       @msgSubject     NVARCHAR(4000),
       @tableHTML      NVARCHAR(MAX),
       @TablesBehind   INT,
       @TotalTables    INT,
       @PercentBehind  DECIMAL(10,4),
       @CurrentTime    DATETIME2(3) = SYSUTCDATETIME(),
       @Recipients     NVARCHAR(MAX) = N'RSteinke@Ashleyfurniture.com;DL_AFI_Analytics_AG_DataWarehouse@Ashleyfurniture.com';
   -------------------------------------------------------------------------
   -- Identify all monitored tables and the ones that are behind
   -------------------------------------------------------------------------
   -- Total monitored tables
   SELECT @TotalTables = COUNT(*)
   FROM DW_Developer.TableDictionary
   WHERE SchemaName NOT LIKE '%Wrk'
     AND ISNULL(RefreshRate,0) > 0;
	 --select @TotalTables
   -- Put "behind" tables into a temp table
   IF OBJECT_ID('tempdb..#behind') IS NOT NULL DROP TABLE #behind;
   SELECT
       HoursLate   = DATEDIFF(HOUR, Modified, SYSUTCDATETIME()) - ISNULL(RefreshRate,0),
       LastUpdated = Modified,
       RefreshRate = ISNULL(RefreshRate,0),
       SchemaName  = SchemaName,
       TableName   = TableName,
       JobServer   = JobServer,
       JobName     = JobName
   INTO #behind
   FROM DW_Developer.TableDictionary
   WHERE SchemaName NOT LIKE '%Wrk'
     AND ISNULL(RefreshRate,0) > 0
     AND DATEDIFF(HOUR, Modified, SYSUTCDATETIME()) > ISNULL(RefreshRate,0);
	-- select * from #behind
   SELECT @TablesBehind = COUNT(*) FROM #behind;
   SET @PercentBehind = CASE WHEN @TotalTables > 0
                             THEN CAST(@TablesBehind AS DECIMAL(10,4)) / @TotalTables * 100
                             ELSE 0 END;
   -- Subject line (Fabric Warehouse doesn't have @@SERVERNAME; include DB name instead)
   DECLARE @DbName SYSNAME = DB_NAME();
   SET @msgSubject = CONCAT(@DbName, N' DataWarehouse Data Feed Alert: ',
                            @PercentBehind, N'% behind (',
                            @TablesBehind, N' of ', @TotalTables, N')');
   -------------------------------------------------------------------------
   -- Logging: summary + detail
   -------------------------------------------------------------------------
   INSERT INTO Performance_Logs.tblFabricDataFeedAlertLog (AuditTime, TablesBehind, TotalTables, PercentBehind)
   VALUES (@CurrentTime, @TablesBehind, @TotalTables, @PercentBehind);
   IF @TablesBehind > 0
   BEGIN
       INSERT INTO Performance_Logs.tblFabricDataFeedAlertLogDetail
           (AuditTime, SchemaName, TableName, HoursLate, RefreshRate, LastUpdated, JobServer, JobName)
       SELECT @CurrentTime, SchemaName, TableName, HoursLate, RefreshRate, LastUpdated, JobServer, JobName
       FROM #behind;
   END;

   --select * from Performance_Logs.tblFabricDataFeedAlertLogDetail
   -------------------------------------------------------------------------
   -- Build the HTML for email
   -------------------------------------------------------------------------
   IF @TablesBehind > 0
   BEGIN
       DECLARE @Rows NVARCHAR(MAX) = N'';
       DECLARE @i INT = 1;
       DECLARE @MaxRows INT;
       DECLARE @HoursLate INT, @LastUpdated DATETIME2, @RefreshRate INT,
               @SchemaName NVARCHAR(128), @TableName NVARCHAR(128),
               @JobServer NVARCHAR(128), @JobName NVARCHAR(128);

       -- Create temp table with row numbers (Fabric SQL Warehouse compatible)
       IF OBJECT_ID('tempdb..#behind_ordered') IS NOT NULL DROP TABLE #behind_ordered;
       SELECT
           ROW_NUMBER() OVER (ORDER BY HoursLate DESC) AS RowNum,
           HoursLate, LastUpdated, RefreshRate, SchemaName, TableName, JobServer, JobName
       INTO #behind_ordered
       FROM #behind
-- … [82 more lines truncated, full body in data/06-procs-raw.json] --
```

---
