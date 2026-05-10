# `usp_Rebuild_CustItemMonthlyPlacements`

_Schema: `Placements` · Warehouse: `Wholesale_Warehouse` · Family: `other`_

_Modified: 2025-12-05 21:57:38.013000 · Code size: 44,316 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 8 sources and writes to 5 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `Marketing.PresBillToExceptions`
- `MasterData_Warehouse.MasterData_DW`
- `Placements_Wrk.ItemStatus_MOP`
- `Placements_Wrk.Monthly_History`
- `Placements_Wrk.PlacementMonthDate`
- `SalesHistory_AFI.OrderHistory`
- `usp_BuildOrderPlacements`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `Placements.CustItemMonthlyPlacements_LOAD`
- `Placements_Wrk.ItemStatus_MOP`
- `Placements_Wrk.Monthly_History`
- `Placements_Wrk.PlacementMonthDate`

## Calls (EXEC)

- `sp_rename`

## Code (first 80 lines)

```sql
CREATE PROC [Placements].[usp_Rebuild_CustItemMonthlyPlacements]
AS

    /* Change Control -----------------------------------------------------------------------------------------------------------
* Procedure: Placements.usp_rebuildOrderPlacements  Called from usp_BuildOrderPlacements
* Business Function : Get order Placement Data - re-engineered logic
* Author: Matt Carter          Date: 01/05/05
* Optimized by Bob Horton, July 2006
* bh added salescategory/region logic 10/2007
* Ed Obaseki remove item with ZZ category
* BH converted to PDW Jan, 2017, converted to ADW JAN 2018
* Gabe De Mayo (2/26/18): Modified to use usp_CreateReplicateWorkTable/updated object existence check/updated error handling
* BH moved start date back to 7 years
* Amy Morina 04/26/2018 changed all references to GETDATE() to DW_Developer.fn_GetCSTDate(GETDATE())
* Bob Horton 05/08/2019 swapped out references to MainPiece with dimItemMaster
* 02/26/2020 Changed insert to "Values" syntax to avoid exclusive locks
* Ragavan V (02/18/2021) -Changed Placements to Wholesale_[$(Wholesale_Warehouse)].SalesHistory_AFI 
* Bob Horton 10/18/2023 converted to Fabric
---------------------------------------------------------------------------------------------------------------------------*/

    BEGIN

        DECLARE
            @String    VARCHAR(5000),
            @DateValue DATETIME2(6),
            @User      VARCHAR(500);

        SET @String = 'AFISales_DW.Placements.usp_Rebuild_CustItemMonthlyPlacements';
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
                @currentYear   SMALLINT,
                @CurrentMonth  SMALLINT,
                @PreviousYear  SMALLINT,
                @PreviousMonth SMALLINT,
                @MidMonthDate  DATE;
            DECLARE
                @StartDate         DATE,
                @StartYear         SMALLINT,
                @StartMonth        SMALLINT
  
            /*** Establish dates ***/

            SET @currentYear =
                (
                    SELECT
                        [FiscalYear]
                    FROM
                        [MasterData_Warehouse].MasterData_DW.DimDate_NonRetail
                    WHERE
                        DateID = CAST(@DateValue AS DATE)
                );
            SET @CurrentMonth =
                (
                    SELECT
                        [FiscalMonth]
                    FROM
                        [MasterData_Warehouse].MasterData_DW.DimDate_NonRetail
                    WHERE
                        DateID =  CAST(@DateValue AS DATE)
                );

            SET @MidMonthDate = CAST(@CurrentMonth AS VARCHAR(2)) + '/15/' + CAST(@currentYear AS CHAR(4));

            SET @PreviousYear =
                (
                    SELECT
                        [FiscalYear]
-- … [839 more lines truncated, full body in data/06-procs-raw.json] --
```

---
