# `usp_UpdateTableDictionary_ModifiedDate`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `refresh`_

_Modified: 2025-10-19 20:14:18.990000 · Code size: 3,827 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 2 sources and writes to 5 sinks. Has error handling (TRY/CATCH).

## Parameters

| Name | Type |
|---|---|
| `@DestinationDatabase` | VARCHAR(150), |
| `@DestinationSchema` | VARCHAR(150), |
| `@DestinationTable` | VARCHAR(150), |
| `@UpdateQuery` | VARCHAR(5000) |
| `@DateValue` | DATETIME |

## Inputs (FROM/JOIN)

- `DW_Developer.TableDictionary`
- `DW_Developer.fn_GetDate`

## Outputs (INSERT/UPDATE/MERGE)

- `DW_Developer.AuditLog`
- `DW_Developer.TableDictionary`
- `INSERT`
- `into`
- `modified`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql
CREATE PROCEDURE [DW_Developer].[usp_UpdateTableDictionary_ModifiedDate]
    @DestinationDatabase VARCHAR(150),
    @DestinationSchema VARCHAR(150),
    @DestinationTable VARCHAR(150),
    @UpdateQuery VARCHAR(5000) = NULL,
    @DateValue DATETIME = NULL
AS

/* Change Control -----------------------------------------------------------------------------------------------------------
* Sriraghav Venkata, A generic procedure for updating last modified date and log the update into ETL_Framework.[DW_Developer].[TableDictionary_UpdateLog]
---------------------------------------------------------------------------------------------------------------------------*/

BEGIN
    SET NOCOUNT ON;
    
    DECLARE
        @String    VARCHAR(5000),
        @User      VARCHAR(500);
        
    SET @String = 'DW_Developer.usp_UpdateTableDictionary_ModifiedDate: ' + @DestinationDatabase + '.' + @DestinationSchema + '.' + @DestinationTable;
    SET @User = SYSTEM_USER;
    
    BEGIN TRY
        -- Set default date if not provided
        IF @DateValue IS NULL
            SET @DateValue = GETDATE();
            
        SELECT @DateValue = CSTDateValue 
        FROM DW_Developer.fn_GetDate(@DateValue);
        
        -- Set default UpdateQuery if not provided
        IF @UpdateQuery IS NULL
            SET @UpdateQuery = '';

        INSERT INTO DW_Developer.AuditLog
        VALUES (@String, @DateValue, @User, 'Process Start');

        DECLARE @Exists INT;
        
        -- Check if record exists
        SET @Exists = (
            SELECT COUNT(*)
            FROM DW_Developer.TableDictionary
            WHERE DatabaseName = @DestinationDatabase 
            AND SchemaName = @DestinationSchema   
            AND TableName = @DestinationTable
        );

        -- Insert if doesn't exist
        IF @Exists = 0 
        BEGIN
            INSERT INTO DW_Developer.TableDictionary
            ( 
                ServerName, 
                DatabaseName,
                SchemaName,
                TableName,
                ObjectType,
                StorageType,
                UpdateQuery,
                Modified
            )
            VALUES 
            (
                'EDW-Fabric',
                @DestinationDatabase,
                @DestinationSchema, 
                @DestinationTable,
                'Table',
                'Delta',
                @UpdateQuery,
                @DateValue
            );
        END

        -- Update modified date
        -- UPDATE DW_Developer.TableDictionary
        -- SET Modified = @DateValue
        -- WHERE DatabaseName = @DestinationDatabase 
        -- AND SchemaName = @DestinationSchema   
-- … [35 more lines truncated, full body in data/06-procs-raw.json] --
```

---
