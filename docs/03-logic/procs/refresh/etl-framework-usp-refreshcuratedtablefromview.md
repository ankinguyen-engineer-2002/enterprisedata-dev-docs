# `usp_RefreshCuratedTableFromView`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `refresh`_

_Modified: 2026-02-05 06:31:48.943000 · Code size: 6,316 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 2 sources and writes to 3 sinks. Calls 3 other procs. Has error handling (TRY/CATCH).

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

- `DW_Developer.usp_DropWorkTable`
- `DW_Developer.usp_UpdateTableDictionary_ModifiedDate`
- `sp_rename`

## Code (first 80 lines)

```sql
CREATE PROC [DW_Developer].[usp_RefreshCuratedTableFromView]
    @DestinationDatabase VARCHAR(150),
    @DestinationSchema   VARCHAR(150),
    @DestinationTable    VARCHAR(150),
    @CheckforEmpty       INT = 0
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

DECLARE @SQLCommand		   VARCHAR(MAX),
		@RenameString      VARCHAR(750),
		@LiveTable         VARCHAR(500),
		@WorkTable         VARCHAR(500),
		@ViewName          VARCHAR(500)

SET @WorkTable = @DestinationDatabase +'.' + @DestinationSchema + '.' + @DestinationTable + '_LOAD'
SET @ViewName =  @DestinationDatabase + '.' + @DestinationSchema + '_Wrk.v_' + @DestinationTable
SET @LiveTable = @DestinationDatabase +'.' + @DestinationSchema + '.' + @DestinationTable

EXECUTE DW_Developer.usp_DropWorkTable  @WorkTable;

--- Create the work table from the work veiw,  if zero rows in view, skip the insert command to avoid truncate errors

SELECT @SQLCommand=
'    USE '+@DestinationDatabase+ ' 
      
            DECLARE
                @CreateTableString VARCHAR(MAX)
            SET @CreateTableString=''DECLARE  @RowCount BIGINT '


            IF @CheckforEmpty = 1 
              BEGIN
                SELECT @SQLCommand=@SQLCommand+' SET @RowCount = (SELECT COUNT(*) FROM '+@ViewName+ ') '
              END
            ELSE
               BEGIN
                 SELECT @SQLCommand=@SQLCommand+' SET @RowCount = 1 '
               END

           SELECT @SQLCommand=@SQLCommand+'
   
            CREATE TABLE ' + @WorkTable + '  AS SELECT TOP 0 *  FROM ' + @LiveTable + ' 
                          
            IF @RowCount > 0 
             BEGIN    
                                      INSERT INTO ' + @WorkTable + ' SELECT * FROM ' + @ViewName +' 
             END ''                       

            SELECT @CreateTableString;
            EXECUTE (@CreateTableString);
-- … [106 more lines truncated, full body in data/06-procs-raw.json] --
```

---
