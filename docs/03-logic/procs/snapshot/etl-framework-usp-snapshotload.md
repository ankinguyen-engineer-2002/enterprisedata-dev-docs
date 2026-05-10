# `Usp_SnapshotLoad`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `snapshot`_

_Modified: 2025-08-26 09:51:28.350000 · Code size: 3,963 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Read-only — pulls data from 1 sources. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

| Name | Type |
|---|---|
| `@DestinationDatabase` | NVARCHAR(128), |
| `@SchemaName` | NVARCHAR(128), |
| `@TableName` | NVARCHAR(128), |
| `@Columns` | NVARCHAR(MAX), |
| `@RelativePath` | NVARCHAR(2000), |
| `@StageTableName` | NVARCHAR(128) |
| `@FileFormat` | NVARCHAR(20) |

## Inputs (FROM/JOIN)

- `staging`

## Outputs (INSERT/UPDATE/MERGE)

_(none detected)_

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql
CREATE PROCEDURE DW_Developer.Usp_SnapshotLoad
    @DestinationDatabase NVARCHAR(128),
    @SchemaName          NVARCHAR(128),
    @TableName           NVARCHAR(128),
    @Columns             NVARCHAR(MAX),
    @RelativePath        NVARCHAR(2000),
    @StageTableName      NVARCHAR(128) = NULL,
    @FileFormat          NVARCHAR(20) = N'PARQUET'
AS
BEGIN
    SET NOCOUNT ON;

    -- Input validations
    IF @DestinationDatabase IS NULL OR LTRIM(RTRIM(@DestinationDatabase)) = ''
    BEGIN
        RAISERROR('Destination database name cannot be null or empty', 16, 1);
        RETURN;
    END

    IF @SchemaName IS NULL OR LTRIM(RTRIM(@SchemaName)) = ''
    BEGIN
        RAISERROR('Schema name cannot be null or empty', 16, 1);
        RETURN;
    END

    IF @TableName IS NULL OR LTRIM(RTRIM(@TableName)) = ''
    BEGIN
        RAISERROR('Table name cannot be null or empty', 16, 1);
        RETURN;
    END

    IF @Columns IS NULL OR LTRIM(RTRIM(@Columns)) = ''
    BEGIN
        RAISERROR('Columns definition for OPENROWSET cannot be null or empty', 16, 1);
        RETURN;
    END

    IF @RelativePath IS NULL OR LTRIM(RTRIM(@RelativePath)) = ''
    BEGIN
        RAISERROR('Relative Parquet path cannot be null or empty', 16, 1);
        RETURN;
    END

    IF @StageTableName IS NULL OR LTRIM(RTRIM(@StageTableName)) = ''
        SET @StageTableName = @TableName + N'_stage';

    -- Build identifiers and paths
    DECLARE @QDb  NVARCHAR(260) = QUOTENAME(@DestinationDatabase);
    DECLARE @QSch NVARCHAR(260) = QUOTENAME(@SchemaName);
    DECLARE @QTgt NVARCHAR(260) = QUOTENAME(@TableName);
    DECLARE @QStg NVARCHAR(260) = QUOTENAME(@StageTableName);

    DECLARE @FullTarget NVARCHAR(776) = @QDb + N'.' + @QSch + N'.' + @QTgt;
    DECLARE @FullStage  NVARCHAR(776) = @QDb + N'.' + @QSch + N'.' + @QStg;

    -- Constant ABFSS prefix
    DECLARE @AbfssPrefix NVARCHAR(1000) =
        N'abfss://5360a935-1984-4775-895f-f4c90bafa19d@onelake.dfs.fabric.microsoft.com/ddadbe2e-c2e2-4949-8e84-81eed6a81c9e/Files/';

    -- Ensure trailing slash on relative path and build full BULK URL
    DECLARE @BulkFolderUrl NVARCHAR(3000) =
        @AbfssPrefix + CASE WHEN RIGHT(@RelativePath, 1) = '/' THEN @RelativePath ELSE @RelativePath + '/' END;

    DECLARE @SQL NVARCHAR(MAX) = N'
-- 1) Create or refresh staging from Parquet
IF OBJECT_ID(N''' + @FullStage + N''', N''U'') IS NOT NULL
BEGIN
    TRUNCATE TABLE ' + @FullStage + N';
    INSERT INTO ' + @FullStage + N'
    SELECT *
    FROM OPENROWSET(
        BULK N''' + REPLACE(@BulkFolderUrl, '''', '''''') + N''',
        FORMAT = N''' + @FileFormat + N'''
    ) WITH
    (
' + @Columns + N'
    ) AS rows;
END
ELSE
BEGIN
-- … [42 more lines truncated, full body in data/06-procs-raw.json] --
```

---
