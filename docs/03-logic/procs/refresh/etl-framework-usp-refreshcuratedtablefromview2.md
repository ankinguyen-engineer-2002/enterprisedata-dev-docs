# `usp_RefreshCuratedTableFromView2`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `refresh`_

_Modified: 2025-08-15 21:08:20.520000 · Code size: 6,072 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 1 sources and writes to 2 sinks. Calls 2 other procs. Has error handling (TRY/CATCH).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `DW_Developer.fn_GetDate`

## Outputs (INSERT/UPDATE/MERGE)

- `DW_Developer.AuditLog`
- `DW_Developer.TableDictionary_UpdateLog`

## Calls (EXEC)

- `DW_Developer.usp_DropWorkTable`
- `sp_rename`

## Code (first 80 lines)

```sql

CREATE   PROC [DW_Developer].[usp_RefreshCuratedTableFromView2]
    @DestinationDatabase VARCHAR(150),
    @DestinationSchema   VARCHAR(150),
    @DestinationTable    VARCHAR(150)
AS

/* Change Control -----------------------------------------------------------------------------------------------------------
* Bob Horton,  A generic procedure for curating fact, dim tables using a view for the select logic
* Bob Horton,  11/09/2023  converted to Fabric
---------------------------------------------------------------------------------------------------------------------------*/


  DECLARE
            @String    VARCHAR(5000),
            @DateValue DATETIME,
            @User      VARCHAR(500);

        SET @String
            = 'usp_RefreshCuratedTableFromView: ' + @DestinationDatabase + '.' + @DestinationSchema + '.' + @DestinationTable;
        SET @User = SYSTEM_USER;
        SET @DateValue = GETDATE();
        SELECT
            @DateValue = CSTDateValue
        FROM
            DW_Developer.fn_GetDate(@DateValue);

        INSERT INTO DW_Developer.AuditLog
        VALUES
            (
                @String, @DateValue, @User, 'Process Start'
            );

        BEGIN TRY

            --- Initialize variables

DECLARE @SQLCommand VARCHAR(MAX)
SET @SQLCommand=
'    USE '+@DestinationDatabase+ ' 
      
            DECLARE
                @WorkTable         VARCHAR(500),
                @ViewName          VARCHAR(500),
                @CreateTableString VARCHAR(MAX),
                @CreateStatString  VARCHAR(MAX),
                @RenameString      VARCHAR(750),
                @LiveTable         VARCHAR(500);


            SET @WorkTable = '+@DestinationDatabase + '''.''' + @DestinationSchema + '''.''' + @DestinationTable + '''_LOAD'';
            SET @ViewName = '+ @DestinationDatabase + '''.''' + @DestinationSchema + '''_Wrk.v_''' + @DestinationTable+';
            SET @LiveTable = '+ @DestinationDatabase + '''.''' + @DestinationSchema + '''.''' + @DestinationTable+';


            EXECUTE DW_Developer.usp_DropWorkTable
                @WorkTable;

            --- Create the work table the work veiw

            SET @CreateTableString = ''CREATE TABLE '' + @WorkTable + ''  AS SELECT TOP 0 *  FROM '' + @LiveTable +
                                    '' INSERT INTO '' + @WorkTable + '' SELECT * FROM '' + @ViewName ;
            --SELECT @CreateTableString;
            EXECUTE (@CreateTableString);


            --- Add stats to work table

            SET @CreateStatString =
                (
                    SELECT
                            STRING_AGG(
                                          CONVERT(
                                                     VARCHAR(MAX),
                                                     ''  CREATE STATISTICS '' + t4.name + '' ON '' + @WorkTable + ''([''
                                                     + t2.name + ''])''
                                                 ), ''; ''
                                      )
                    FROM
                            sys.tables        t1
-- … [84 more lines truncated, full body in data/06-procs-raw.json] --
```

---
