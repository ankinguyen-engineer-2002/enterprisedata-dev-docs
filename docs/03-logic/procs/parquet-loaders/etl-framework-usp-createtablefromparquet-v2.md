# `Usp_CreateTableFromParquet_V2`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `parquet-loaders`_

_Modified: 2025-10-11 10:11:16.847000 · Code size: 7,915 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Read-only — pulls data from 2 sources. Calls 1 other procs. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

| Name | Type |
|---|---|
| `@DestinationDatabase` | NVARCHAR(128), |
| `@SchemaName` | NVARCHAR(128), |
| `@TableName` | NVARCHAR(128), |
| `@ParquetPath` | NVARCHAR(4000) |

## Inputs (FROM/JOIN)

- `HOLDING`
- `destination`

## Outputs (INSERT/UPDATE/MERGE)

_(none detected)_

## Calls (EXEC)

- `sys.sp_executesql`

## Code (first 80 lines)

```sql
CREATE   PROCEDURE DW_Developer.Usp_CreateTableFromParquet_V2

    @DestinationDatabase NVARCHAR(128),   -- e.g. 'Source_Data'

    @SchemaName          NVARCHAR(128),   -- e.g. 'dbo'

    @TableName           NVARCHAR(128),   -- e.g. 'Fact_Sales'

    @ParquetPath         NVARCHAR(4000)   -- abfss://.../file.parquet (or a folder)

AS

BEGIN

    SET NOCOUNT ON;

    IF ISNULL(@DestinationDatabase,'') = ''  RAISERROR('Destination database cannot be empty',16,1);

    IF ISNULL(@SchemaName,'') = ''           RAISERROR('Schema name cannot be empty',16,1);

    IF ISNULL(@TableName,'') = ''            RAISERROR('Table name cannot be empty',16,1);

    IF ISNULL(@ParquetPath,'') = ''          RAISERROR('Parquet path cannot be empty',16,1);

    DECLARE @db      NVARCHAR(128) = @DestinationDatabase;

    DECLARE @schema  NVARCHAR(128) = @SchemaName;

    DECLARE @table   NVARCHAR(128) = @TableName;

    DECLARE @holding NVARCHAR(128) = @TableName + N'_holding';

    DECLARE @FullFinal   NVARCHAR(776) = QUOTENAME(@db)+N'.'+QUOTENAME(@schema)+N'.'+QUOTENAME(@table);

    DECLARE @FullHolding NVARCHAR(776) = QUOTENAME(@db)+N'.'+QUOTENAME(@schema)+N'.'+QUOTENAME(@holding);

    DECLARE @SQL NVARCHAR(MAX);

    BEGIN TRY

        ----------------------------------------------------------------

        -- (1) Create/refresh HOLDING table from Parquet (destination DB)

        ----------------------------------------------------------------

        SET @SQL = N'

IF OBJECT_ID(''' + @FullHolding + N''',''U'') IS NOT NULL

    DROP TABLE ' + @FullHolding + N';

SELECT *

INTO ' + @FullHolding + N'

FROM OPENROWSET(

    BULK ''' + REPLACE(@ParquetPath,'''','''''') + N''',

    FORMAT = ''PARQUET''

) AS data;';

        EXEC sys.sp_executesql @SQL;

        ----------------------------------------------------------------

        -- (2–4) Build DDL with right-sized string columns, load, drop

        --   Uses destDB INFORMATION_SCHEMA + session #temp tables

        ----------------------------------------------------------------

        DECLARE @schemaLit  NVARCHAR(260) = N'''' + REPLACE(@schema,'''','''''') + N'''';

        DECLARE @holdingLit NVARCHAR(260) = N'''' + REPLACE(@holding,'''','''''') + N'''';

        SET @SQL = N'SET NOCOUNT ON;

-- … [235 more lines truncated, full body in data/06-procs-raw.json] --
```

---
