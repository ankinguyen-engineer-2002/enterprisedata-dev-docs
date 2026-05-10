# `usp_GenerateEmailHTML_DimAggregateDifference`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `email`_

_Modified: 2026-04-20 09:39:07.803000 · Code size: 8,641 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 3 sources and writes to 2 sinks.

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `EDWAgg`
- `SourceAgg`
- `Source_Data.Retail_External`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.Performance_Logs`
- `Source_Data.Retail_External`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql
CREATE       PROCEDURE [DW_Developer].[usp_GenerateEmailHTML_DimAggregateDifference]
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @HTML NVARCHAR(MAX);
    DECLARE @TableRows NVARCHAR(MAX);
    DECLARE @TotalNotMatch INT;
    DECLARE  @Recipients  NVARCHAR(MAX) = N'mohali@ashleyfurniture.com;paswini@ashleyfurniture.com;ibalu@ashleyfurniture.com';

    -------------------------------------------------------------------------
    -- Step 1: Clear old data and insert new comparison results
    -------------------------------------------------------------------------
    TRUNCATE TABLE [Source_Data].[Retail_External].[DimAggregateDifference];

    -- Insert comparison data
    -- Note: We map the SourceTable and MetricNames to match EDW naming conventions
    WITH SourceAgg AS (
        SELECT 
            REPLACE(SourceTable, '_', '') AS SourceTable,
            YearGroup,
            MonthGroup,
            YearMonth,
            CASE 
                WHEN MetricName = 'DepositPaymentAmt' THEN 'PaymentAmt'
                WHEN MetricName = 'InvoiceTotSaleAmt' THEN 'TotSaleAmt'
                WHEN MetricName = 'InvItemQtyCommitted' THEN 'QtyCommitted'
                WHEN MetricName = 'InvItemQtyOrdered' THEN 'QtyOrdered'
                WHEN MetricName = 'InvItemQtyUndelivered' THEN 'QtyUndelivered'
                WHEN MetricName = 'InvoicePaymentAmt' THEN 'PaymentAmt'
                WHEN MetricName = 'OrderItemQtyCommitted' THEN 'QtyCommitted'
                WHEN MetricName = 'OrderItemQtyOrdered' THEN 'QtyOrdered'
                WHEN MetricName = 'OrderItemQtyUndelivered' THEN 'QtyUndelivered'
                WHEN MetricName = 'OrdersTotSaleAmt' THEN 'TotSaleAmt'
                ELSE MetricName
            END AS MetricName,
            MetricValue AS SourceValue
        FROM [Source_Data].[Retail_External].[DSGAggCount] -- Adjust to your actual Source Aggregate table name
    ),
    EDWAgg AS (
        SELECT 
            SourceTable,
            YearGroup,
            MonthGroup,
            YearMonth,
            MetricName,
            MetricValue AS EDWValue
        FROM [Source_Data].[Retail_External].[EDWAggregate] -- Adjust to your actual EDW Aggregate table name
    )
    INSERT INTO [Source_Data].[Retail_External].[DimAggregateDifference] (
        SourceTable,
        YearGroup,
        MonthGroup,
        YearMonth,
        MetricName,
        SourceValue,
        EDWValue,
        Difference,
        Status
    )
    SELECT 
        COALESCE(s.SourceTable, e.SourceTable) AS SourceTable,
        COALESCE(s.YearGroup, e.YearGroup) AS YearGroup,
        COALESCE(s.MonthGroup, e.MonthGroup) AS MonthGroup,
        COALESCE(s.YearMonth, e.YearMonth) AS YearMonth,
        COALESCE(s.MetricName, e.MetricName) AS MetricName,
        ISNULL(s.SourceValue, 0) AS SourceValue,
        ISNULL(e.EDWValue, 0) AS EDWValue,
        ISNULL(s.SourceValue, 0) - ISNULL(e.EDWValue, 0) AS Difference,
        CASE
            WHEN ISNULL(s.SourceValue, 0) = ISNULL(e.EDWValue, 0) THEN 'Match'
            ELSE 'Not Match'
        END AS Status
    FROM SourceAgg s
    FULL OUTER JOIN EDWAgg e
        ON s.SourceTable = e.SourceTable 
        AND s.YearMonth = e.YearMonth
        AND s.MetricName = e.MetricName
    ORDER BY 
        SourceTable, 
-- … [151 more lines truncated, full body in data/06-procs-raw.json] --
```

---
