# `usp_InvActivitySummary`

_Schema: `Retail_OOM_Enh` · Warehouse: `Retail_Warehouse` · Family: `other`_

_Modified: 2026-01-21 21:48:07.977000 · Code size: 13,808 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 4 sources and writes to 2 sinks. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `Retail_OOM_Enh.InvActivitySummary`
- `Source_Data.Retail_Corporate`
- `Source_Data.Retail_External`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `Retail_OOM_Enh.InvActivitySummary`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql
CREATE   PROCEDURE [Retail_OOM_Enh].[usp_InvActivitySummary]
AS
BEGIN
    DECLARE @String VARCHAR(5000),
            @DateValue DATETIME,
            @User VARCHAR(500),
            @DestinationDatabase VARCHAR(150),
            @DestinationSchema VARCHAR(150),
            @DestinationTable VARCHAR(150);

    SET @String = 'Retail_OOM_Enh.usp_InvActivitySummary';
    SET @User = SYSTEM_USER;
    SET @DateValue = GETDATE();
    SET @DestinationDatabase = 'Retail_Warehouse';
    SET @DestinationSchema = 'Retail_OOM_Enh';
    SET @DestinationTable = 'usp_InvActivitySummary';

    SELECT @DateValue = CSTDateValue
    FROM [ETL_Framework].[DW_Developer].fn_GetDate(@DateValue);

    INSERT INTO [ETL_Framework].[DW_Developer].[AuditLog]
    VALUES (@String, @DateValue, @User, 'Process Start');

    BEGIN TRY
        DECLARE @TransDate DATE;
        SET @TransDate = CAST(GETDATE() - 1 AS DATE);

        DELETE FROM [Retail_OOM_Enh].[InvActivitySummary] 
        WHERE CAST(TransDate AS DATE) = @TransDate;

        DROP TABLE IF EXISTS #t1, #t2, #RuleMatches;

      
        SELECT  iar.UniqueID,
                iar.StaffID,
                iar.StoreID,
                iar.AdjQty,
                iar.InStorageID,
                iar.OutStorageID,
                iar.ProductID,
                iar.InvTransTypeID,
                iar.TransDate
        INTO #t1
        FROM [Source_Data].[Retail_Corporate].[InvactivityRaw] AS iar
        INNER JOIN [Source_Data].[Retail_External].[LocationGroups] ON LocationID = iar.StoreID
        WHERE LocationGroupID = 'DC'
            AND iar.GroupID NOT IN ('ADVTRK', 'AUCPRM', 'DON', 'DONOWH', 'ISI', 'LABOR', 'MSI', 'PRCARD', 'RESTCK', 'SVC', 'XFI')
            AND  CAST(TransDate AS DATE) >= @TransDate
            AND iar.StaffID IS NOT NULL;

    
        SELECT  i.UniqueID,
                i.StaffID,
                i.StoreID,
                i.AdjQty,
                i.InStorageID,
                i.OutStorageID,
                i.ProductID,
                i.InvTransTypeID,
                i.TransDate,
                tr.RuleID,
                r.FieldName
        INTO #RuleMatches
        FROM #t1 AS i
        CROSS JOIN (
            SELECT DISTINCT RuleID 
            FROM [Source_Data].[Retail_External].[InvActivityRuleDetails]
        ) AS tr
        INNER JOIN [Source_Data].[Retail_External].[InvActivityRuleDetails] AS r
            ON r.RuleID = tr.RuleID
        WHERE 
       
            (r.FieldName = 'StoreID' AND (
                r.Operator IS NULL
                OR (r.Operator = 'EQ' AND r.FieldValue = i.StoreID)
                OR (r.Operator = 'LT' AND i.StoreID < r.FieldValue)
                OR (r.Operator = 'LTE' AND i.StoreID <= r.FieldValue)
                OR (r.Operator = 'GT' AND i.StoreID > r.FieldValue)
                OR (r.Operator = 'GTE' AND i.StoreID >= r.FieldValue)
                OR (r.Operator = 'LIKE' AND i.StoreID LIKE '%' + r.FieldValue + '%')
-- … [231 more lines truncated, full body in data/06-procs-raw.json] --
```

---
