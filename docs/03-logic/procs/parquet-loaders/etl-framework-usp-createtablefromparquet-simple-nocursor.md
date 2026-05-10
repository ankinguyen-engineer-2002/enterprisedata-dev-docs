# `Usp_CreateTableFromParquet_Simple_NoCursor`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `parquet-loaders`_

_Modified: 2025-10-11 08:17:29.857000 · Code size: 7,763 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Read-only — pulls data from 4 sources. Calls 3 other procs. Has error handling (TRY/CATCH). ⚠️ Uses cursor (typically slow). ⚠️ Drops tables (destructive).

## Parameters

| Name | Type |
|---|---|
| `@DestinationDatabase` | NVARCHAR(128), |
| `@SchemaName` | NVARCHAR(128), |
| `@TableName` | NVARCHAR(128), |
| `@ParquetPath` | NVARCHAR(4000 |

## Inputs (FROM/JOIN)

- `ColDefs`
- `Cols`
- `Decorated`
- `MaxLens`

## Outputs (INSERT/UPDATE/MERGE)

_(none detected)_

## Calls (EXEC)

- `in`
- `sys.sp_executesql`
- `this`

## Code (first 80 lines)

```sql
CREATE   PROCEDURE DW_Developer.Usp_CreateTableFromParquet_Simple_NoCursor

    @DestinationDatabase NVARCHAR(128),

    @SchemaName          NVARCHAR(128),

    @TableName           NVARCHAR(128),

    @ParquetPath         NVARCHAR(4000)

AS

BEGIN

    SET NOCOUNT ON;

    IF ISNULL(@DestinationDatabase,'') = ''  RAISERROR('Destination database cannot be empty',16,1);

    IF ISNULL(@SchemaName,'') = ''           RAISERROR('Schema name cannot be empty',16,1);

    IF ISNULL(@TableName,'') = ''            RAISERROR('Table name cannot be empty',16,1);

    IF ISNULL(@ParquetPath,'') = ''          RAISERROR('Parquet path cannot be empty',16,1);

    -- Must execute in the destination database (Fabric sys catalogs aren’t cross-db)

    IF DB_NAME() <> @DestinationDatabase

        RAISERROR('Execute this procedure in the destination database: %s',16,1,@DestinationDatabase);

    DECLARE @db      NVARCHAR(128) = @DestinationDatabase;

    DECLARE @schema  NVARCHAR(128) = @SchemaName;

    DECLARE @table   NVARCHAR(128) = @TableName;

    DECLARE @holding NVARCHAR(128) = @TableName + N'_holding';

    DECLARE @FullFinal   NVARCHAR(MAX) = QUOTENAME(@db)+N'.'+QUOTENAME(@schema)+N'.'+QUOTENAME(@table);

    DECLARE @FullHolding NVARCHAR(MAX) = QUOTENAME(@db)+N'.'+QUOTENAME(@schema)+N'.'+QUOTENAME(@holding);

    DECLARE @SQL NVARCHAR(MAX);

    BEGIN TRY

        ----------------------------------------------------------------

        -- 1) Create/refresh holding from Parquet (no USE)

        ----------------------------------------------------------------

        SET @SQL = N'

IF OBJECT_ID(''' + QUOTENAME(@schema)+N'.'+QUOTENAME(@holding) + N''',''U'') IS NOT NULL

    DROP TABLE ' + QUOTENAME(@db)+N'.'+QUOTENAME(@schema)+N'.'+QUOTENAME(@holding) + N';

SELECT *

INTO ' + @FullHolding + N'

FROM OPENROWSET(

    BULK ''' + REPLACE(@ParquetPath,'''','''''') + N''',

    FORMAT = ''PARQUET''

) AS src;';

        EXEC sys.sp_executesql @SQL;

        ----------------------------------------------------------------

        -- 2) Build dynamic batch (no USE; CTE starts with ;WITH)

        ----------------------------------------------------------------

        DECLARE @schemaLit  NVARCHAR(200) = N'''' + REPLACE(@schema,'''','''''') + N'''';

-- … [237 more lines truncated, full body in data/06-procs-raw.json] --
```

---
