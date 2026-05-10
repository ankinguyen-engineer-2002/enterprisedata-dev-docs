# `Usp_WriteTableToParquet`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `other`_

_Modified: 2026-03-11 17:20:39.413000 · Code size: 4,190 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 1 sources and writes to 2 sinks. Has error handling (TRY/CATCH).

## Parameters

| Name | Type |
|---|---|
| `@SourceDatabase` | NVARCHAR(128), |
| `@SchemaName` | NVARCHAR(128), |
| `@TableName` | NVARCHAR(128), |
| `@ParquetPath` | NVARCHAR(4000), |
| `@OverwriteExisting` | BIT |

## Inputs (FROM/JOIN)

- `DW_Developer.fn_GetDate`

## Outputs (INSERT/UPDATE/MERGE)

- `DW_Developer.AuditLog`
- `DW_Developer.TableExport_Log`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql
CREATE   PROCEDURE DW_Developer.Usp_WriteTableToParquet
    @SourceDatabase NVARCHAR(128),
    @SchemaName NVARCHAR(128),
    @TableName NVARCHAR(128),
    @ParquetPath NVARCHAR(4000),
    @OverwriteExisting BIT = 1
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @SQL NVARCHAR(MAX);
    DECLARE @FullTableName NVARCHAR(260);
    DECLARE @DateValue DATETIME;
    DECLARE @String VARCHAR(5000);
    DECLARE @User VARCHAR(500);

    SET @DateValue = GETDATE();
    SELECT
        @DateValue = CSTDateValue
    FROM
        DW_Developer.fn_GetDate(@DateValue);

    SET @String = 'Usp_WriteTableToParquet - ' + QUOTENAME(@SourceDatabase) + '.' + QUOTENAME(@SchemaName) + '.' + QUOTENAME(@TableName);
    SET @User = SYSTEM_USER;

    INSERT INTO [DW_Developer].[AuditLog] (Description, DateTime, [User], Command)
    VALUES (@String, @DateValue, @User, 'Process Start');
    
    -- Validate inputs
    IF @SourceDatabase IS NULL OR @SourceDatabase = ''
    BEGIN
        RAISERROR('Source database name cannot be null or empty', 16, 1);
        RETURN;
    END
    
    IF @SchemaName IS NULL OR @SchemaName = ''
    BEGIN
        RAISERROR('Schema name cannot be null or empty', 16, 1);
        RETURN;
    END
    
    IF @TableName IS NULL OR @TableName = ''
    BEGIN
        RAISERROR('Table name cannot be null or empty', 16, 1);
        RETURN;
    END
    
    IF @ParquetPath IS NULL OR @ParquetPath = ''
    BEGIN
        RAISERROR('Parquet path cannot be null or empty', 16, 1);
        RETURN;
    END
    
    -- Ensure path ends with .parquet
    IF RIGHT(@ParquetPath, 8) <> '.parquet'
    BEGIN
        SET @ParquetPath = @ParquetPath + '.parquet';
    END
    
    -- Build three-part table name
    SET @FullTableName = QUOTENAME(@SourceDatabase) + '.' + QUOTENAME(@SchemaName) + '.' + QUOTENAME(@TableName);

    SET @DateValue = GETDATE();
    SELECT
        @DateValue = CSTDateValue
    FROM
        DW_Developer.fn_GetDate(@DateValue);
    
    -- Build dynamic SQL
    SET @SQL = '
    USE ' + QUOTENAME(@SourceDatabase) + ';
    
    -- Verify table exists
    IF OBJECT_ID(''' + @FullTableName + ''', ''U'') IS NULL
    BEGIN
        RAISERROR(''Table does not exist: ' + @FullTableName + ''', 16, 1);
        RETURN;
    END;
    
    -- Write table data to Parquet file in Data Lake
-- … [47 more lines truncated, full body in data/06-procs-raw.json] --
```

---
