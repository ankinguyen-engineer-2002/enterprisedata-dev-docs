# `usp_SCD2_TableLoad`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `scd2`_

_Modified: 2025-12-24 04:00:58.910000 · Code size: 18,855 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 3 sources and writes to 4 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). Uses explicit transaction. ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `DW_Developer.TableDictionary`
- `DW_Developer.fn_GetDate`
- `condition`

## Outputs (INSERT/UPDATE/MERGE)

- `DW_Developer.AuditLog`
- `DW_Developer.TableDictionary_UpdateLog`
- `T2`
- `current`

## Calls (EXEC)

- `DW_Developer.usp_DropWorkTable`

## Code (first 80 lines)

```sql
CREATE   PROC [DW_Developer].[usp_SCD2_TableLoad]
    @DestinationDatabase VARCHAR(150),
    @DestinationSchema   VARCHAR(150),
    @DestinationTable    VARCHAR(150),
    @OperationName       VARCHAR(100) = NULL
AS

/*----------------   Procedure:  [DW_Developer].[usp_SCD2_TableLoad] ---------------------------------------

 Description: Implements Slowly Changing Dimension Type 2 (SCD2) logic for tracking historical changes
 
 SCD Type 2 maintains historical data by:
 - Creating new rows for changed records
 - Maintaining effective date ranges (EffectiveStartDate, EffectiveEndDate)
 - Using IsCurrent flag to identify active records
 - Closing out old records when changes occur
 
 Requirements:
 - Destination table must have these columns:
   * EffectiveStartDate DATETIME2(6) - When this version became effective
   * EffectiveEndDate DATETIME2(6) - When this version expired (9999-12-31 for current)
   * IsCurrent BIT - 1 for current record, 0 for historical
   * RowVersion INT - Version number for the record (optional but recommended)
 
 - The columns order and types in the Source tables must match the Destination tables
   (excluding the SCD2 tracking columns: EffectiveStartDate, EffectiveEndDate, IsCurrent, RowVersion)
 
 - The primary key (business key) is used to identify the same logical entity across versions
   The PrimaryKey values for both Source and Destination tables must be populated in table dictionary
 
 - UpdateMethod in TableDictionary must be set to 'SCD2'
 
 Process Flow:
 1. Identify changed records by comparing source to current destination records
 2. Close out existing current records (set EffectiveEndDate, IsCurrent = 0)
 3. Insert new versions of changed records
 4. Insert completely new records (not previously in destination)

---------------------------------------------------------------------------------------------------------------------------*/
BEGIN

SET @OperationName = CASE WHEN @OperationName='NULL' THEN NULL ELSE @OperationName END

DECLARE @String VARCHAR(5000), @DateValue DATETIME2(6), @User VARCHAR(500)
SET @String = @DestinationDatabase+'.'+@DestinationSchema+'.'+ @DestinationTable + CASE WHEN @OperationName IS NOT NULL THEN  ' ('+@OperationName+')' ELSE '' END
SET @User = SYSTEM_USER;
SET @DateValue = GETDATE();
SELECT
    @DateValue = CSTDateValue
FROM
    DW_Developer.fn_GetDate(@DateValue);

INSERT INTO DW_Developer.AuditLog
    VALUES
    (
      @String, @DateValue, @User, 'SCD2 Process Start'
    );

  
BEGIN TRY

-- Declare Variables
DECLARE @SqlStr VARCHAR(MAX), 
        @ErrSqlStr VARCHAR(300), 
        @DestinationPrimaryKey VARCHAR(800), 
        @DestinationAlternateKey VARCHAR(800), 
        @SourceSchemaName VARCHAR(200), 
        @SourceTableName VARCHAR(200),
        @SourceSchema VARCHAR(200),
        @SourceTable VARCHAR(200), 
        @SourcePrimaryKey VARCHAR(800),
        @SourceAlternateKey VARCHAR(800),
        @UpdateMethod VARCHAR(20),
        @SourceStartPos INT,
        @SourceStopPos INT,
        @DestinationStartPos INT,
        @DestinationStopPos INT,
        @DestinationFirstColumn VARCHAR(100),
        @SourceFirstColumn VARCHAR(100),
        @SourcePlatform VARCHAR(25),
-- … [372 more lines truncated, full body in data/06-procs-raw.json] --
```

---
