# `Usp_TableFromParquet_CopyInto_TruncateLoad`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `parquet-loaders`_

_Modified: 2025-09-24 08:20:29.187000 · Code size: 2,094 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Pure compute — no detected reads/writes (may be utility / control flow). Calls 1 other procs. Has error handling (TRY/CATCH).

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
CREATE     PROCEDURE DW_Developer.Usp_TableFromParquet_CopyInto_TruncateLoad
    @DatabaseName NVARCHAR(128),           -- Parameter for database name
    @SchemaName NVARCHAR(128),             -- Parameter for schema name  
    @TableName NVARCHAR(128),              -- Parameter for table name
    @ParquetPath NVARCHAR(500)             -- Parameter for remaining parquet file path
AS
BEGIN
    DECLARE @TruncateSQL NVARCHAR(MAX)
    DECLARE @CopyIntoSQL NVARCHAR(MAX)
    DECLARE @FullTableName NVARCHAR(500)
    
    -- Build full table name
    SET @FullTableName = '[' + @DatabaseName + '].[' + @SchemaName + '].[' + @TableName + ']'
    
    -- Build the TRUNCATE TABLE statement
    SET @TruncateSQL = 'TRUNCATE TABLE ' + @FullTableName
    
    -- Build the COPY INTO statement
    SET @CopyIntoSQL = '
    COPY INTO ' + @FullTableName + '
    FROM ''abfss://5360a935-1984-4775-895f-f4c90bafa19d@onelake.dfs.fabric.microsoft.com/ddadbe2e-c2e2-4949-8e84-81eed6a81c9e/Files/' + @ParquetPath + '''
    WITH (
        FILE_TYPE = ''PARQUET'',
        CREDENTIAL = (IDENTITY = ''Managed Identity'')
    )'
    
    BEGIN TRY
        -- Execute the TRUNCATE statement first
        EXEC sp_executesql @TruncateSQL
        
        -- Execute the COPY INTO statement
        EXEC sp_executesql @CopyIntoSQL
        
        PRINT 'Data successfully loaded into ' + @FullTableName
        
    END TRY
    BEGIN CATCH
        -- Error handling
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE()
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY()
        DECLARE @ErrorState INT = ERROR_STATE()
        
        PRINT 'Error occurred during data load:'
        PRINT 'TRUNCATE SQL: ' + @TruncateSQL
        PRINT 'COPY INTO SQL: ' + @CopyIntoSQL
        
        -- Re-raise the error
        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState)
    END CATCH
    
    -- Optional: Print statements for debugging (uncomment if needed)
    -- PRINT('TRUNCATE: ' + @TruncateSQL)
    -- PRINT('COPY INTO: ' + @CopyIntoSQL)
END

```

---
