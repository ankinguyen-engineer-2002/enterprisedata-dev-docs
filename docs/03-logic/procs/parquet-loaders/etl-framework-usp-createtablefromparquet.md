# `Usp_CreateTableFromParquet`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `parquet-loaders`_

_Modified: 2025-10-20 14:55:33.987000 · Code size: 4,732 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 2 sources and writes to 3 sinks. Has error handling (TRY/CATCH).

## Parameters

| Name | Type |
|---|---|
| `@DestinationDatabase` | NVARCHAR(128), |
| `@SchemaName` | NVARCHAR(128), |
| `@TableName` | NVARCHAR(128), |
| `@ParquetPath` | NVARCHAR(4000 |

## Inputs (FROM/JOIN)

- `DW_Developer.TableDictionary`
- `DW_Developer.fn_GetDate`

## Outputs (INSERT/UPDATE/MERGE)

- `DW_Developer.AuditLog`
- `DW_Developer.TableDictionary`
- `DW_Developer.TableDictionary_UpdateLog`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql
CREATE PROCEDURE DW_Developer.Usp_CreateTableFromParquet
    @DestinationDatabase NVARCHAR(128),
    @SchemaName NVARCHAR(128),
    @TableName NVARCHAR(128),
    @ParquetPath NVARCHAR(4000)
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

    SET @String= 'Usp_CreateTableFromParquet - ' + QUOTENAME(@DestinationDatabase) + '.' + QUOTENAME(@SchemaName) + '.' + QUOTENAME(@TableName);
    SET @User = SYSTEM_USER;

    INSERT INTO [DW_Developer].[AuditLog] (Description, DateTime, [User], Command)
	VALUES (@String,@DateValue,@User,'Process Start');
    
    -- Validate inputs
    IF @DestinationDatabase IS NULL OR @DestinationDatabase = ''
    BEGIN
        RAISERROR('Destination database name cannot be null or empty', 16, 1);
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
    
    -- Build three-part table name
    SET @FullTableName = QUOTENAME(@DestinationDatabase) + '.' + QUOTENAME(@SchemaName) + '.' + QUOTENAME(@TableName);

    SET @DateValue = GETDATE();
        SELECT
            @DateValue = CSTDateValue
        FROM
            DW_Developer.fn_GetDate(@DateValue);
    
    -- Build dynamic SQL
    SET @SQL = '
    USE ' + QUOTENAME(@DestinationDatabase) + ';
    
    -- Create schema if not exists
    --IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = ''' + @SchemaName + ''')
   -- BEGIN
    --    EXEC(''CREATE SCHEMA ' + QUOTENAME(@SchemaName) + ''');
    --END;

    -- truncate table if exists
    IF OBJECT_ID(''' + @FullTableName + ''', ''U'') IS NOT NULL
        TRUNCATE TABLE ' + @FullTableName + ';
    
    -- Create table from Parquet file
    INSERT INTO ' + @FullTableName + '
    SELECT * 
    FROM OPENROWSET(
        BULK ''' + @ParquetPath + ''',
-- … [59 more lines truncated, full body in data/06-procs-raw.json] --
```

---
