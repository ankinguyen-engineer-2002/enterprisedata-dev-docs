# `usp_Update_DailyPlacements`

_Schema: `Placements` · Warehouse: `Wholesale_Warehouse` · Family: `refresh`_

_Modified: 2025-12-05 17:00:14.673000 · Code size: 14,170 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 9 sources and writes to 5 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `Marketing.PresBillToExceptions`
- `MasterData_Warehouse.MasterData_DW`
- `PDW`
- `Placements.CustItemMonthlyPlacements`
- `Placements.DailyPlacements`
- `Placements_Wrk.tblOrders`
- `Placements_Wrk.tblOrdersDetail`
- `SalesHistory_AFI.OrderHistory`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `Placements.DailyPlacements`
- `Placements_Wrk.tblOrders`
- `Placements_Wrk.tblOrdersDetail`
- `of`

## Calls (EXEC)

- `ETL_Framework.DW_Developer`

## Code (first 80 lines)

```sql
CREATE PROC [Placements].[usp_Update_DailyPlacements]
AS

    /* Change Control -----------------------------------------------------------------------------------------------------------
* Procedure: [Placements].[usp_Update_DailyPlacements]
* Description: 	Procedure created to have a daily update of order placements with the date of actual placement  
* Leandra Edgar (06/05/2009): Created
* Lhulberg (02/20/2017): oving procedure to PDW and changed syntax
* Bob Horton (Jan 2018): Migrated from PDW Cube load view to Azure Data Warehouse
* Gabe De Mayo (3/2/18): Modified to use usp_CreateReplicateWorkTable/updated object existence check/updated error handling
* Amy Morina 04/26/2018 changed all references to GETDATE() to DW_Developer.fn_GetCSTDate(GETDATE())
* Bob Horton 6/18/2018  added Min() function in last insert to associate the placement to the first day the new sale shows up for within the week and not double count throughout the week
* Bob Horton 05/08/2019 swapped out references to MainPiece with dimItemMaster
* 02/26/2020 Changed insert to "Values" syntax to avoid exclusive locks
* Bob Horton 10/24/2023 convert to Fabric
---------------------------------------------------------------------------------------------------------------------------*/

    BEGIN

        DECLARE
            @String    VARCHAR(5000),
            @DateValue DATETIME2(6),
            @User      VARCHAR(500);

        SET @String = 'AFISales_DW.Placements.usp_Update_DailyPlacements';
        SET @User = SYSTEM_USER;
        
        SET @DateValue = Getdate()
         SELECT @DateValue=CSTDateValue from [ETL_Framework].DW_Developer.fn_GetDate(@DateValue)

        INSERT INTO [ETL_Framework].DW_Developer.AuditLog
        VALUES
            (
                @String, @DateValue, @User, 'Process Start'
            );

        BEGIN TRY

            /* declare working variables */
            DECLARE
                @currentYear      SMALLINT,
                @CurrentMonth     SMALLINT,
                @CurrentYearMonth INT,
                @MinDate          DATE;


            SET @currentYear =
                (
                    SELECT
                        [FiscalYear]
                    FROM
                        [MasterData_Warehouse].MasterData_DW.DimDate_NonRetail
                    WHERE
                        [DateID] = CAST(@DateValue AS DATE)
                );
            SET @CurrentMonth =
                (
                    SELECT
                        [FiscalMonth]
                    FROM
                        [MasterData_Warehouse].MasterData_DW.DimDate_NonRetail
                    WHERE
                        [DateID] = CAST(@DateValue AS DATE)
                );
            SET @CurrentYearMonth =
                (
                    SELECT
                        MIN([FiscalWeekYear])
                    FROM
                       [MasterData_Warehouse].MasterData_DW.DimDate_NonRetail
                    WHERE
                        [FiscalYear] = @currentYear
                        AND [FiscalMonth] = @CurrentMonth
                );
            SET @MinDate =
                (
                    SELECT
                        MIN([DateID])
                    FROM
                        [MasterData_Warehouse].MasterData_DW.DimDate_NonRetail
-- … [216 more lines truncated, full body in data/06-procs-raw.json] --
```

---
