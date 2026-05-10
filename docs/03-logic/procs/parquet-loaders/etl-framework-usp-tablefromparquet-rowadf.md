# `Usp_TableFromParquet_RowADF`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `parquet-loaders`_

_Modified: 2025-08-31 16:04:01.753000 · Code size: 4,612 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 1 sources and writes to 1 sinks. Has error handling (TRY/CATCH). ⚠️ Uses cursor (typically slow). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_FRAMEWORK.DW_Developer`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_FRAMEWORK.DW_Developer`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql
CREATE   PROCEDURE DW_Developer.Usp_TableFromParquet_RowADF
AS
BEGIN
    SET NOCOUNT ON;
 
    DECLARE @all_ok INT = 1;
 
    ------------------------------------------------------------------
    -- 1) Build staging table (no IDENTITY): use ROW_NUMBER() instead
    ------------------------------------------------------------------
    DROP TABLE IF EXISTS ETL_FRAMEWORK.DW_Developer.FabricLoad;
 
    SELECT
        ROW_NUMBER() OVER (ORDER BY (SELECT 1))        AS RowId,               -- surrogate key without IDENTITY
        LTRIM(RTRIM([FabricDatabaseName]))             AS FabricDatabaseName,
        LTRIM(RTRIM([FabricSchemaName]))               AS FabricSchemaName,
        LTRIM(RTRIM([TableName]))                      AS TableName,
        LTRIM(RTRIM([Path]))                           AS [Path],              -- expected suffix after /Files/raw-zone
        [ColumnList]                                   AS ColumnList,
        CAST(0 AS bit)                                 AS Status,              -- 0=pending, 1=loaded
        CAST(NULL AS VARCHAR (2000))                   AS ErrorMessage
    INTO ETL_FRAMEWORK.DW_Developer.FabricLoad
    FROM OPENROWSET(
            BULK 'abfss://5360a935-1984-4775-895f-f4c90bafa19d@onelake.dfs.fabric.microsoft.com/ddadbe2e-c2e2-4949-8e84-81eed6a81c9e/Files/raw-zone/BACKUP/BackupDefinitions/DevTest.csv',
            FORMAT = 'CSV',
            FIELDTERMINATOR = ',',
            FIELDQUOTE = '"',
            PARSER_VERSION = '2.0',
            HEADER_ROW = TRUE
         )
         WITH (
           [FabricDatabaseName] VARCHAR(128),
           [FabricSchemaName]   VARCHAR(128),
           [TableName]          VARCHAR(128),
           [Path]               VARCHAR(1000),
           [ColumnList]         VARCHAR(MAX)
         ) AS defs;
 
    ------------------------------------------------------------------
    -- 2) Process each CSV row (no cursor)
    ------------------------------------------------------------------
    DECLARE
        @RowId        INT,
        @DatabaseName NVARCHAR(128),
        @SchemaName   NVARCHAR(128),
        @TableName    NVARCHAR(128),
        @ParquetPath  NVARCHAR(1000),
        @ColumnList   NVARCHAR(MAX),
        @SQL          NVARCHAR(MAX);
 
    WHILE EXISTS (SELECT 1 FROM ETL_FRAMEWORK.DW_Developer.FabricLoad WHERE ISNULL(Status,0) = 0)
    BEGIN
        SELECT TOP (1)
            @RowId        = RowId,
            @DatabaseName = FabricDatabaseName,
            @SchemaName   = FabricSchemaName,
            @TableName    = TableName,
            @ParquetPath  = [Path],
            @ColumnList   = ColumnList
        FROM ETL_FRAMEWORK.DW_Developer.FabricLoad
        WHERE ISNULL(Status,0) = 0
        ORDER BY RowId;
 
        BEGIN TRY
            -- Keep your original dynamic SQL exactly the same:
            SET @SQL = ' SELECT * INTO [' + @DatabaseName + '].[' + @SchemaName + '].[' + @TableName + '] ' +
                       ' FROM OPENROWSET( ' +
                       '   BULK ''abfss://5360a935-1984-4775-895f-f4c90bafa19d@onelake.dfs.fabric.microsoft.com/ddadbe2e-c2e2-4949-8e84-81eed6a81c9e/Files/raw-zone' + @ParquetPath + ''', ' +
                       '   FORMAT=''PARQUET'' ' +
                       ' ) WITH ( ' + @ColumnList + ' ) AS rows;';
 
            EXEC sp_executesql @SQL;
 
            UPDATE ETL_FRAMEWORK.DW_Developer.FabricLoad
            SET Status = 1, ErrorMessage = NULL
            WHERE RowId = @RowId;
        END TRY
        BEGIN CATCH
            UPDATE ETL_FRAMEWORK.DW_Developer.FabricLoad
            SET Status = 0, ErrorMessage = ERROR_MESSAGE()
-- … [23 more lines truncated, full body in data/06-procs-raw.json] --
```

---
