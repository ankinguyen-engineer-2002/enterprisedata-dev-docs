# `Usp_CreateTableFromParquet_V1`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `parquet-loaders`_

_Modified: 2025-10-16 18:19:05.867000 · Code size: 11,183 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 3 sources and writes to 5 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

| Name | Type |
|---|---|
| `@DestinationDatabase` | NVARCHAR(128), |
| `@SchemaName` | NVARCHAR(128), |
| `@TableName` | NVARCHAR(128), |
| `@ParquetPath` | NVARCHAR(4000), |
| `@UseInferredSchema` | BIT |

## Inputs (FROM/JOIN)

- `DW_Developer.TableDictionary`
- `DW_Developer.fn_GetDate`
- `holding`

## Outputs (INSERT/UPDATE/MERGE)

- `DW_Developer.AuditLog`
- `DW_Developer.TableDictionary`
- `DW_Developer.TableDictionary_UpdateLog`
- `from`
- `metadata`

## Calls (EXEC)

- `sp_rename`

## Code (first 80 lines)

```sql

CREATE   PROCEDURE DW_Developer.Usp_CreateTableFromParquet_v1
    @DestinationDatabase NVARCHAR(128),
    @SchemaName NVARCHAR(128),
    @TableName NVARCHAR(128),
    @ParquetPath NVARCHAR(4000),
    @UseInferredSchema BIT = 1  -- 1 = Use inferred schema (recommended), 0 = Use default VARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @SQL NVARCHAR(MAX);
    DECLARE @FullTableName NVARCHAR(260);
    DECLARE @HoldingTableName NVARCHAR(260);
    DECLARE @DateValue DATETIME;
    DECLARE @String VARCHAR(5000);
    DECLARE @User VARCHAR(500);
    DECLARE @CreateTableSQL NVARCHAR(MAX);
    DECLARE @ColumnDefinitions NVARCHAR(MAX);

    SET @DateValue = GETDATE();
        SELECT
            @DateValue = CSTDateValue
        FROM
            DW_Developer.fn_GetDate(@DateValue);

    SET @String= 'DW_Developer.Usp_CreateTableFromParquet';
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

    -- Build three-part table names
    SET @FullTableName = QUOTENAME(@DestinationDatabase) + '.' + QUOTENAME(@SchemaName) + '.' + QUOTENAME(@TableName);
    SET @HoldingTableName = QUOTENAME(@DestinationDatabase) + '.' + QUOTENAME(@SchemaName) + '.' + QUOTENAME(@TableName + '_holding');

    SET @DateValue = GETDATE();
        SELECT
            @DateValue = CSTDateValue
        FROM
            DW_Developer.fn_GetDate(@DateValue);

    BEGIN TRY
        -- Step 0: Create schema if it doesn't exist
        SET @SQL = '
        USE ' + QUOTENAME(@DestinationDatabase) + ';

        IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = ''' + @SchemaName + ''')
        BEGIN
            EXEC(''CREATE SCHEMA ' + QUOTENAME(@SchemaName) + ''');
            PRINT ''Schema ' + @SchemaName + ' created successfully'';
        END';

        EXEC sp_executesql @SQL;
        PRINT 'Schema ' + @SchemaName + ' verified/created in database ' + @DestinationDatabase;
-- … [201 more lines truncated, full body in data/06-procs-raw.json] --
```

---
