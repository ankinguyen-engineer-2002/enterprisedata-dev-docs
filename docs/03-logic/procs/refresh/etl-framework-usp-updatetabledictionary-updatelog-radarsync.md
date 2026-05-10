# `usp_UpdateTableDictionary_UpdateLog_RadarSync`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `refresh`_

_Modified: 2025-12-07 08:52:52.800000 · Code size: 910 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 2 sources and writes to 1 sinks.

## Parameters

| Name | Type |
|---|---|
| `@DestinationDatabase` | NVARCHAR(128), |
| `@SchemaName` | NVARCHAR(128), |
| `@TableName` | NVARCHAR(128 |

## Inputs (FROM/JOIN)

- `DW_Developer.fn_GetDate`
- `dw_developer.tabledictionary`

## Outputs (INSERT/UPDATE/MERGE)

- `DW_Developer.TableDictionary_UpdateLog_RadarSync`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql


CREATE   PROCEDURE [DW_Developer].[usp_UpdateTableDictionary_UpdateLog_RadarSync]
    @DestinationDatabase NVARCHAR(128),
    @SchemaName NVARCHAR(128),
    @TableName NVARCHAR(128)
AS
BEGIN
DECLARE @DateValue DATETIME;
DECLARE @EnhDatabaseName NVARCHAR(128);
DECLARE @EnhSchemaName NVARCHAR(128);
DECLARE @EnhTableName NVARCHAR(128);
SET @DateValue = GETDATE();
        SELECT
            @DateValue = CSTDateValue
        FROM
            DW_Developer.fn_GetDate(@DateValue);

SELECT @EnhDatabaseName=DataBaseName ,@EnhSchemaName = schemaname, 
           @EnhTableName = tablename 
    FROM   dw_developer.tabledictionary  
    WHERE   replicatedsource = ''+@SchemaName+ '.'+@TableName+''

 Insert into [DW_Developer].[TableDictionary_UpdateLog_RadarSync] (DataBaseName,SchemaName,TableName,LastUpdated)
 values (@EnhDatabaseName,@EnhSchemaName,@EnhTableName,@DateValue)
 
END;

```

---
