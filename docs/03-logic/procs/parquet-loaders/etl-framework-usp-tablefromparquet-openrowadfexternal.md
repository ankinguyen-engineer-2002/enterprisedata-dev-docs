# `Usp_TableFromParquet_OpenRowADFExternal`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `parquet-loaders`_

_Modified: 2025-09-04 09:30:37.253000 · Code size: 1,033 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Pure compute — no detected reads/writes (may be utility / control flow). Calls 1 other procs.

## Parameters

| Name | Type |
|---|---|
| `@DatabaseName` | NVARCHAR(128), |
| `@SchemaName` | NVARCHAR(128), |
| `@TableName` | NVARCHAR(128), |
| `@ParquetPath` | NVARCHAR(500), |
| `@ColumnList` | NVARCHAR(MAX) |

## Inputs (FROM/JOIN)

_(none detected)_

## Outputs (INSERT/UPDATE/MERGE)

_(none detected)_

## Calls (EXEC)

- `the`

## Code (first 80 lines)

```sql
CREATE       PROCEDURE DW_Developer.Usp_TableFromParquet_OpenRowADFExternal
    @DatabaseName NVARCHAR(128),           -- Parameter for database name
    @SchemaName NVARCHAR(128),             -- Parameter for schema name  
    @TableName NVARCHAR(128),              -- Parameter for table name
    @ParquetPath NVARCHAR(500),            -- Parameter for remaining parquet file path
    @ColumnList NVARCHAR(MAX)              -- Parameter for column definitions
AS
BEGIN
    DECLARE @SQL NVARCHAR(MAX)
    
    -- Build the dynamic SQL statement
    SET @SQL = '
    SELECT * INTO [' + @DatabaseName + '].[' + @SchemaName + '].[' + @TableName + ']
    FROM OPENROWSET(
        BULK ''abfss://5360a935-1984-4775-895f-f4c90bafa19d@onelake.dfs.fabric.microsoft.com/ddadbe2e-c2e2-4949-8e84-81eed6a81c9e/Files/raw-zone'+ @ParquetPath + ''',
        FORMAT=''PARQUET''
    ) WITH 
    (
       ' + @ColumnList + '
    ) AS rows;'
    
    -- Execute the dynamic SQL
    --print(@SQL)
    EXEC sp_executesql @SQL
END
```

---
