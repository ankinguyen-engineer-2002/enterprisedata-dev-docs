# `usp_Audit_ADW_Tables`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `audit`_

_Modified: 2025-09-09 10:29:56.330000 · Code size: 2,918 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 2 sources and writes to 1 sinks. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `Centralized_Warehouse.Source_Data_sys`
- `ETL_Framework.DW_Developer`

## Outputs (INSERT/UPDATE/MERGE)

- `DW_Developer.TableDictionary`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql


CREATE   PROCEDURE [DW_Developer].[usp_Audit_ADW_Tables]
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
	    IF OBJECT_ID('tempdb..#Temp_t') IS NOT NULL
            DROP TABLE #Temp_t

        
			SELECT DISTINCT 
			'Source_Data' as DatabaseName,
			SCHEMA_NAMEE as SchemaName,
			t.name,
			'HEAP' as StorageType, -- Default to HEAP for Fabric
			t.create_date,
			COUNT(c.column_id) as ColumnCount
			INTO #Temp_t
			FROM 
			(
					SELECT S.Name AS SCHEMA_NAMEE,T.* 
					FROM Centralized_Warehouse.Source_Data_sys.tables  T
					JOIN Centralized_Warehouse.Source_Data_sys.Schemas  S ON  T.schema_id = S.schema_id 
			) t
			JOIN Centralized_Warehouse.Source_Data_sys.columns c ON t.object_id = c.object_id
			WHERE SCHEMA_NAMEE NOT LIKE '%xbk' 
			AND SCHEMA_NAMEE NOT LIKE '%wrk' 
			AND SCHEMA_NAMEE NOT LIKE '%_aggs'
			AND SCHEMA_NAMEE NOT LIKE '%_aggp'
			AND t.name not like '%_Stage' 
			AND t.name not like '%_Landing_%' 
			AND t.name not like '%_Staging' 
			AND t.name not like '%_temp' 
			AND t.name not like '%_Holding'  
			AND t.name not like '%_Wrk'  
			AND t.name not like '%_test'  
			AND t.name not like '%_Backup' 
			AND t.name not like '%_bck' 
			AND t.name not like '%processAdd' 
			AND t.name not like '%_load'
			group by SCHEMA_NAMEE, t.name,t.create_date

	   
        -- Drop temporary table if it exists
        IF OBJECT_ID('tempdb..#NewRecords') IS NOT NULL
            DROP TABLE #NewRecords;

        -- Create temporary table with new records
        SELECT A.*
        INTO #NewRecords
        FROM #Temp_t A
        LEFT JOIN ETL_Framework.[DW_Developer].TableDictionary B 
            ON A.DatabaseName = B.DatabaseName 
            AND A.name = B.tableName 
            AND A.SchemaName = B.SchemaName 
        WHERE B.DatabaseName IS NULL;

        -- Insert new records into TableDictionary
        INSERT INTO DW_Developer.TableDictionary
        (ServerName, DatabaseName, SchemaName, TableName, ObjectType, StorageType, CreateDate, ColumnCount)
        SELECT 
            'EDW-Fabric',
            DatabaseName,
            SchemaName,
            name,
            'Table',
            StorageType,
            create_date,
            ColumnCount 
        FROM #NewRecords;

        -- Clean up temporary table
        DROP TABLE #NewRecords;

    END TRY
    BEGIN CATCH
        -- Error handling
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
-- … [12 more lines truncated, full body in data/06-procs-raw.json] --
```

---
