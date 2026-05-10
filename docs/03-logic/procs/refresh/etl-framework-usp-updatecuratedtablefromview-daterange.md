# `usp_UpdateCuratedTableFromView_DateRange`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `refresh`_

_Modified: 2025-08-15 20:54:15.260000 · Code size: 4,954 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 2 sources and writes to 3 sinks. Has error handling (TRY/CATCH).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `DW_Developer.TableDictionary`
- `DW_Developer.fn_GetDate`

## Outputs (INSERT/UPDATE/MERGE)

- `DW_Developer.AuditLog`
- `DW_Developer.TableDictionary`
- `DW_Developer.TableDictionary_UpdateLog`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql
CREATE PROC [DW_Developer].[usp_UpdateCuratedTableFromView_DateRange]
    @DestinationDatabase    VARCHAR(150),
    @DestinationSchema      VARCHAR(150),
    @DestinationTable       VARCHAR(150),
    @SourceDateColumn       VARCHAR(100),
    @DestinationDateColumn  VARCHAR(100),
    @NumberofDays           INT
    
AS

/* Change Control -----------------------------------------------------------------------------------------------------------
* Bob Horton,  A generic procedure for curating fact, dim tables using a view for the select logic 
*              the procedure keys off the date column passed in
* Bob Horton,  11/20/2023  converted to Fabric
---------------------------------------------------------------------------------------------------------------------------*/


  DECLARE
        @String    VARCHAR(5000),
        @DateValue DATETIME,
        @User      VARCHAR(500)
      
        SELECT @String
            = 'usp_UpdateCuratedTableFromView_DateRange: ' + @DestinationDatabase + '.' + @DestinationSchema + '.' + @DestinationTable;
        SELECT @User = SYSTEM_USER;
        SELECT @DateValue = GETDATE();
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

DECLARE 
    @SQLCommand		   VARCHAR(MAX),
	@RenameString      VARCHAR(750),
	@LiveTable         VARCHAR(500),
	@ViewName          VARCHAR(500),
    @MinDate           VARCHAR(20)

SELECT @MinDate = CAST(DATEADD(DAY,@NumberofDays,CAST(GETDATE() AS DATE)) AS VARCHAR(12))
SELECT @ViewName =  @DestinationDatabase + '.' + @DestinationSchema + '_Wrk.v_' + @DestinationTable
SELECT @LiveTable = @DestinationDatabase +'.' + @DestinationSchema + '.' + @DestinationTable



SELECT @SQLCommand=
     
  'DELETE FROM ' + @LiveTable + ' WHERE '+ @DestinationDateColumn + ' >= '''+ @MinDate + ''' 
   INSERT INTO ' + @LiveTable + ' SELECT * FROM ' + @ViewName +' WHERE '+ @SourceDateColumn +' >= '''+ @MinDate +''''


  SELECT @SQLCommand
  EXECUTE (@SQLCommand)

      

      SET @DateValue = GETDATE();
      SELECT
          @DateValue = CSTDateValue
      FROM
            DW_Developer.fn_GetDate(@DateValue);

        INSERT INTO DW_Developer.AuditLog
        VALUES
            (
                @String, @DateValue, @User, 'Process Complete'
            );


        --- Update last modified in Table Dictionary 
        DECLARE @Exists INT
-- … [72 more lines truncated, full body in data/06-procs-raw.json] --
```

---
