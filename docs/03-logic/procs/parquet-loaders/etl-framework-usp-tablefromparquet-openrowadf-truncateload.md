# `Usp_TableFromParquet_OpenRowADF_TruncateLoad`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `parquet-loaders`_

_Modified: 2025-09-04 09:36:19.300000 · Code size: 1,858 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Pure compute — no detected reads/writes (may be utility / control flow). Calls 1 other procs.

## Parameters

| Name | Type |
|---|---|
| `@DatabaseName` | NVARCHAR(128), |
| `@SchemaName` | NVARCHAR(128), |
| `@TableName` | NVARCHAR(128), |
| `@ParquetPath` | NVARCHAR(500) |

## Inputs (FROM/JOIN)

_(none detected)_

## Outputs (INSERT/UPDATE/MERGE)

_(none detected)_

## Calls (EXEC)

- `the`

## Code (first 80 lines)

```sql
CREATE       PROCEDURE DW_Developer.Usp_TableFromParquet_OpenRowADF_TruncateLoad
    @DatabaseName NVARCHAR(128),           -- Parameter for database name
    @SchemaName NVARCHAR(128),             -- Parameter for schema name  
    @TableName NVARCHAR(128),              -- Parameter for table name
    @ParquetPath NVARCHAR(500)             -- Parameter for remaining parquet file path

AS
BEGIN
    DECLARE @SQL NVARCHAR(MAX)
    DECLARE @TruncateSQL NVARCHAR(MAX)
    DECLARE @InsertSQL NVARCHAR(MAX)
    
    -- Build the TRUNCATE TABLE statement
    SET @TruncateSQL = 'TRUNCATE TABLE [' + @DatabaseName + '].[' + @SchemaName + '].[' + @TableName + ']'
    
    -- Build the INSERT statement with OPENROWSET Onelake
    -- SET @InsertSQL = '
    -- INSERT INTO [' + @DatabaseName + '].[' + @SchemaName + '].[' + @TableName + ']
    -- SELECT * 
    -- FROM OPENROWSET(
    --     BULK ''abfss://5360a935-1984-4775-895f-f4c90bafa19d@onelake.dfs.fabric.microsoft.com/ddadbe2e-c2e2-4949-8e84-81eed6a81c9e/Files/raw-zone' + @ParquetPath + ''',
    --     FORMAT=''PARQUET''
    -- ) WITH 
    -- (
    --     ' + @ColumnList + '
    -- ) AS rows;'

    -- Build the INSERT statement with OPENROWSET ADLS
    SET @InsertSQL = '
    INSERT INTO [' + @DatabaseName + '].[' + @SchemaName + '].[' + @TableName + ']
    SELECT * 
    FROM OPENROWSET(
        BULK ''' + @ParquetPath + ''',
        FORMAT=''PARQUET''
    );'
    -- WITH 
    -- (
    --     ' + @ColumnList + '
    -- ) AS rows;'

    -- Execute the TRUNCATE statement first
    EXEC sp_executesql @TruncateSQL
    
    -- Execute the INSERT statement
    EXEC sp_executesql @InsertSQL
    
    -- Optional: Print statements for debugging (uncomment if needed)
    -- PRINT('TRUNCATE: ' + @TruncateSQL)
    -- PRINT('INSERT: ' + @InsertSQL)
END

```

---
