# `usp_OpenOrderSummary_Insert_Detail`

_Schema: `Retail_OOM_Enh` · Warehouse: `Retail_Warehouse` · Family: `other`_

_Modified: 2025-10-24 12:08:20.267000 · Code size: 10,080 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 3 sources and writes to 2 sinks. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `Retail_OOM_Enh.OpenOrderSummaryDetail`
- `Source_Data.Retail_Corporate`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `Retail_OOM_Enh.OpenOrderSummaryDetail`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql
CREATE   PROCEDURE Retail_OOM_Enh.[usp_OpenOrderSummary_Insert_Detail]
AS
BEGIN

    --// AUDIT LOGGING START //--

    DECLARE @String VARCHAR(5000),
            @DateValue DATETIME,
            @User VARCHAR(500),
            @DestinationDatabase VARCHAR(150),
            @DestinationSchema VARCHAR(150),
            @DestinationTable VARCHAR(150);

    SET @String = 'Retail_OOM_Enh.usp_OpenOrderSummary_Insert_Detail';
    SET @User = SYSTEM_USER;
    SET @DateValue = GETDATE();
    SET @DestinationDatabase = 'Retail_Warehouse';
    SET @DestinationSchema = 'Retail_OOM_Enh';
    SET @DestinationTable = 'OpenOrderSummaryDetail';

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

        DELETE FROM Retail_OOM_Enh.[OpenOrderSummaryDetail];

        SELECT  o.OrderID,
                o.OrderDate,
                ofu.OrderFulfillmentID,
                o.OrderBookedStoreID AS StoreID,
                oi.ShipLocnID AS ShipLocationID,
                tc.Description AS OrderType,
                ofu.FulfillmentMethod,
                ofu.FulfillmentStatus,
                ofu.FulfillmentDate,
                NULL AS ContactStatus,
                ofu.DeliveryContactDate AS ContactDate,
                CASE WHEN ofu.FulfillmentDate < CAST(GETDATE() AS DATE) THEN 'Y' ELSE 'N' END AS PastDue,
                o.CustomerID,
                MAX(ofu.MerchSubTot) AS MerchSubTot,
                (
                    SELECT SUM(TaxAmt)
                    FROM [Source_Data].[Retail_Corporate].[OrderFulfillment_TaxDetail] ft
                    WHERE ft.OrderFulfillmentID = ofu.OrderFulfillmentID
                ) fTaxAmt,
                COUNT(DISTINCT ofu.OrderFulfillmentID) AS TotalFulfilment,
                SUM(oi.QtyOrdered) AS QtyOrdered,
                SUM(CASE WHEN o.TransCodeID IN (30, 34, 37) THEN oi.QtyOrdered ELSE oi.QtyCommitted END) AS QtyCommitted,
                MAX(DISTINCT ofu.DlvyChrg) AS DlvyChrg,
                SUM(oi.TotCost * oi.QtyOrdered) AS TotalCost,
                SUM(oi.TotCost * CASE WHEN o.TransCodeID IN (30, 34, 37) THEN oi.QtyOrdered ELSE oi.QtyCommitted END) AS ReservedCost,
                SUM(oi.CaseSellingPrice * oi.QtyOrdered) AS TotalSales,
                SUM(oi.CaseSellingPrice * CASE WHEN o.TransCodeID IN (30, 34, 37) THEN oi.QtyOrdered ELSE oi.QtyCommitted END) AS ReservedSales,
                SUM(p.CubicFeet * oi.QtyOrdered) AS TotalVolume,
                SUM(p.CubicFeet * CASE WHEN o.TransCodeID IN (30, 34, 37) THEN oi.QtyOrdered ELSE oi.QtyCommitted END) AS ReservedVolume,
                SUM(p.CaseWeight * oi.QtyOrdered) AS TotalWeight,
                SUM(p.CaseWeight * CASE WHEN o.TransCodeID IN (30, 31) THEN oi.QtyOrdered ELSE oi.QtyCommitted END) AS ReservedWeight,
                CASE WHEN SUM(oi.QtyOrdered) - SUM(CASE WHEN o.TransCodeID IN (30, 34, 37) THEN oi.QtyOrdered ELSE oi.QtyCommitted END) = 0 THEN 'Y' ELSE 'N' END AS Filled
        INTO #OOM
        FROM [Source_Data].[Retail_Corporate].[Orders] AS o
            INNER JOIN [Source_Data].[Retail_Corporate].[OrderItem] AS oi
                ON oi.OrderID = o.OrderID
            INNER JOIN [Source_Data].[Retail_Corporate].[OrderFulfillment] AS ofu
                ON ofu.OrderFulfillmentID = oi.OrderFulfillmentID
            INNER JOIN [Source_Data].[Retail_Corporate].[TransCode] AS tc
                ON tc.TransCodeID = o.TransCodeID
            INNER JOIN [Source_Data].[Retail_Corporate].[Product] AS p
                ON p.ProductID = oi.ProductID
        WHERE tc.TransCodeID IN (0, 1, 3, 6, 7, 30, 34, 37)
-- … [184 more lines truncated, full body in data/06-procs-raw.json] --
```

---
