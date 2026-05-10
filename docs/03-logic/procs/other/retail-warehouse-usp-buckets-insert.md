# `usp_Buckets_Insert`

_Schema: `Retail_OOM_Enh` · Warehouse: `Retail_Warehouse` · Family: `other`_

_Modified: 2025-10-24 12:08:19.433000 · Code size: 11,303 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 4 sources and writes to 4 sinks. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `Retail_OOM_Enh.Buckets`
- `Source_Data.Retail_Corporate`
- `Source_Data.Retail_External`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `Retail_OOM_Enh.BucketOrders`
- `Retail_OOM_Enh.Buckets`
- `tdg.wrk_BucketInv`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql
CREATE   PROCEDURE [Retail_OOM_Enh].usp_Buckets_Insert
AS
BEGIN

    --// AUDIT LOGGING START //--

    DECLARE @String VARCHAR(5000),
            @DateValue DATETIME,
            @User VARCHAR(500),
            @DestinationDatabase VARCHAR(150),
            @DestinationSchema VARCHAR(150),
            @DestinationTable VARCHAR(150);

    SET @String = 'Retail_OOM_Enh.usp_Buckets_Insert';
    SET @User = SYSTEM_USER;
    SET @DateValue = GETDATE();
    SET @DestinationDatabase = 'Retail_Warehouse';
    SET @DestinationSchema = 'Retail_OOM_Enh';
    SET @DestinationTable = 'Buckets';

    SELECT @DateValue = CSTDateValue
    FROM [ETL_Framework].[DW_Developer].fn_GetDate(@DateValue);

    INSERT INTO [ETL_Framework].[DW_Developer].[AuditLog]
    VALUES
    (
        @String, @DateValue, @User, 'Process Start'
    );

    --// AUDIT LOGGING END //--

    BEGIN TRY

        DECLARE @TransDate DATE = GETDATE();

        DROP TABLE IF EXISTS #BucketInv;
        DROP TABLE IF EXISTS #BucketOrderItem;
        DROP TABLE IF EXISTS #BucketPOI;

        --INSERT INTO tdg.wrk_BucketInv (StoreID, ProductID, QtyOnHand, TotalCost, QtyCommitted, PieceStatusID, ProductTypeID, GroupID, TransDate, DateChanged)
        SELECT  StoreID,
                p.ProductID,
                p.QtyOnHand,
                p.TotalCost,
                COALESCE(p.QtyCommitted, 0) + COALESCE(p.QtySoftCommitted, 0) AS QtyCommitted,
                p.PieceStatusID,
                p.ProductTypeID,
                p.GroupID,
                p.TransDate,
                COALESCE(p.DateChanged, p.DateCreated) AS DateChanged
        INTO #BucketInv
        FROM [Source_Data].[Retail_Corporate].[ProductInventory] p
        WHERE TransDate >= @TransDate;

        INSERT INTO [Retail_OOM_Enh].[Buckets]
        (
            LocationID,
            ProductID,
            QtyOnHand,
            ProcessStatus
        )
        SELECT  StoreID,
                ProductID,
                QOH,
                0 AS ProcessStatus
        FROM
        (
            SELECT  StoreID,
                    ProductID,
                    SUM(QtyOnHand) AS QOH
            FROM #BucketInv ph
            WHERE TransDate = @TransDate
                  AND PieceStatusID < 3
                  AND ProductTypeID = '1'
                  AND GroupID NOT IN ('MST', 'SVT')
                  AND ph.StoreID IS NOT NULL
            GROUP BY StoreID,
                     ProductID
        ) oh
        WHERE ProductID NOT IN
-- … [257 more lines truncated, full body in data/06-procs-raw.json] --
```

---
