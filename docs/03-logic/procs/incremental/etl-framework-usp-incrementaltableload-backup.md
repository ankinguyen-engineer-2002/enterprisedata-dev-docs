# `usp_IncrementalTableLoad_Backup`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `incremental`_

_Modified: 2025-09-03 10:11:25.413000 · Code size: 23,617 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 5 sources and writes to 5 sinks. Calls 2 other procs. Has error handling (TRY/CATCH). Uses explicit transaction.

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `DW_Developer.TableDictionary`
- `DW_Developer.fn_GetDate`
- `ReplicatedSource`
- `an`
- `current`

## Outputs (INSERT/UPDATE/MERGE)

- `DW_Developer.AuditLog`
- `DW_Developer.TableDictionary_UpdateLog`
- `T2`
- `matching`
- `to`

## Calls (EXEC)

- `DW_Developer.usp_DropWorkTable`
- `the`

## Code (first 80 lines)

```sql
CREATE PROC [DW_Developer].[usp_IncrementalTableLoad_Backup]

    @DestinationDatabase VARCHAR(150),
    @DestinationSchema   VARCHAR(150),
    @DestinationTable    VARCHAR(150),
	@OperationName    VARCHAR(100)
    AS

/*----------------   Procedure:  [DW_Developer].[usp_IncrementalTableLoadTable] ---------------------------------------

 Description: To upsert the recent data to Gold Layer tables from an Source tables using primary key values and such
 

 
 - The columns order and types in the Source tables must match the Destination tables... with no additional or missing columns
   but the column names can be different
 
 - The primary key is used to test if the Source table row exists in the Destination table
   The tbkPrimaryKey values for both the Source and Destination tables must be populated in table dictionary
   Both tables need the same PK combinations in the same order (names can be different)
 
 
   If Alternate key is used to override the primary key, then it needs to have a common column with it instead
   This will avoid data shuffles on the source and destination tables.


 - The Source Source table reference is pulled from ReplicatedSource in table Dictionary
 
 - DateKey values must be populated in the dictionary for both the Source and Destination tables for the date based ETL methods.
   This can be left blank for all other methods 
 
 - One of the following ETL Methods must be populated in the Destination table's dictionary row for UpdateMethod

      'Upsert' - Using the Primary Key values, Update matching, then insert missing rows into the Enhanced table
	  
	  'Insert' - using the primary Key values, insert what's missing

	  'Append' - Just append the data from the Source table  (Probably shouldn't be used for Gold Layer feeds)

	  'DateKey' - Needs the primary key and an inline date column which is used to compare the Destination table to the 
	             extended table to delete any rows that changed, then append any that are missing

				 This method assumes rows can not be deleted and all updates trigger an update to a datekey value in 
				 an in-line audit field

	 'DateRange' - Only needs date columns to identify rows that fall within the range to delete then insert 
	        
			    This is the only type that uses the DateRangeDays value basing the date range on the number of days from 
				current date... or if a 0 is passed, the min-max dates from the Source table will determine the date range 
				
				This method assumes rows can be updatd or deleted within a recent time frame and the range covers any changes
				that could occur.... this also is a method to use when there is no primary key to do insert or upsert logic

     'Identity' - Using an auto-incrimenting identity key from the source, this method will only append rows with a 
	             key value greater than the current max value that already exists in the Destination table.  This method assumes
				 rows can not be updated or deleted at the source
				 Identity will pass back to the calling program the new Max(Identity) value

     
     
	 'DELINSERT' - Using the Primary Key values, Delete matching, then append the data from the Source table into Enhanced table.


---------------------------------------------------------------------------------------------------------------------------*/


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
-- … [470 more lines truncated, full body in data/06-procs-raw.json] --
```

---
