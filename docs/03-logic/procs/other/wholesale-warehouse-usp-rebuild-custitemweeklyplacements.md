# `usp_Rebuild_CustItemWeeklyPlacements`

_Schema: `Placements` · Warehouse: `Wholesale_Warehouse` · Family: `other`_

_Modified: 2025-12-05 22:42:59.287000 · Code size: 39,246 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 7 sources and writes to 4 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `Marketing.PresBillToExceptions`
- `MasterData_Warehouse.MasterData_DW`
- `Placements_Wrk.ItemStatus_WOP`
- `Placements_Wrk.Weekly_History`
- `SalesHistory_AFI.OrderHistory`
- `usp_BuildOrderPlacements`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `Placements.CustItemWeeklyPlacements_LOAD`
- `Placements_Wrk.ItemStatus_WOP`
- `Placements_Wrk.Weekly_History`

## Calls (EXEC)

- `sp_rename`

## Code (first 80 lines)

```sql
CREATE PROC [Placements].[usp_Rebuild_CustItemWeeklyPlacements]
AS

    /* Change Control -----------------------------------------------------------------------------------------------------------
* Procedure: Placements.usp_Rebuild_WeeklyOrderPlacements  Called from usp_BuildOrderPlacements
* Description: Get order Placement Data - re-engineered logic
* Author: Matt Carter          Date: 01/05/05
* Optimized by Bob Horton, July 2006
* bh added salescategory/region logic 10/2007
* Ed Obaseki remove item with ZZ category
* BH converted to PDW Jan, 2017
* BH converted to Weekly Buckets, 4/20/2017
* Gabe De Mayo (2/26/18): Modified to use usp_CreateReplicateWorkTable/updated object existence check/updated error handling
* Amy Morina 04/26/2018 changed all references to GETDATE() to DW_Developer.fn_GetCSTDate(GETDATE())
* Bob Horton 05/08/2019 swapped out references to MainPiece with dimItemMaster
* 02/26/2020 Changed insert to "Values" syntax to avoid exclusive locks
* Bob Horton 10/18/2023 converted to Fabric
---------------------------------------------------------------------------------------------------------------------------*/

    BEGIN

        DECLARE
            @String    VARCHAR(5000),
            @DateValue DATETIME2(6),
            @User      VARCHAR(500);
        SET @String = 'AFISales_DW.Placements.usp_Rebuild_CustItemWeeklyPlacements';
        SET @User = SYSTEM_USER;
        SET @DateValue = GETDATE();
        SELECT @DateValue=CSTDateValue from [ETL_Framework].DW_Developer.fn_GetDate(@DateValue)

        INSERT INTO [ETL_Framework].DW_Developer.AuditLog
        VALUES
            (
                @String, @DateValue, @User, 'Process Start'
            );

        BEGIN TRY

            /* declare working variables */
            DECLARE
                @currentYear  SMALLINT,
                @CurrentWeek  SMALLINT,
                @PreviousYear SMALLINT,
                @PreviousWeek SMALLINT,
                @StartDate    DATE


            /*** Establish dates ***/

            SET @currentYear =
                (
                    SELECT
                        [FiscalYear]
                    FROM
                        [MasterData_Warehouse].MasterData_DW.DimDate_NonRetail
                    WHERE
                        DateID = CAST(@DateValue as DATE)
                );

            SET @CurrentWeek =
                (
                    SELECT
                        [FiscalWeek]
                    FROM
                        [MasterData_Warehouse].MasterData_DW.DimDate_NonRetail
                    WHERE
                        DateID = CAST(@DateValue as DATE)
                );
 

            SET @PreviousYear =
                (
                    SELECT
                        [FiscalYear]
                    FROM
                        [MasterData_Warehouse].MasterData_DW.DimDate_NonRetail
                    WHERE
                        DateID = DATEADD(DAY, -7, CAST(@DateValue AS DATE))
                );
            SET @PreviousWeek =
-- … [735 more lines truncated, full body in data/06-procs-raw.json] --
```

---
