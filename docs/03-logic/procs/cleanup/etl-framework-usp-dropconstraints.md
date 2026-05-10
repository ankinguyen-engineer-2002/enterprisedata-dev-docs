# `usp_DropConstraints`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `cleanup`_

_Modified: 2025-08-15 20:54:14.927000 · Code size: 10,624 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Pure compute — no detected reads/writes (may be utility / control flow). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

_(none detected)_

## Outputs (INSERT/UPDATE/MERGE)

_(none detected)_

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql

CREATE PROC [DW_Developer].[usp_DropConstraints]
    (@DatabaseName VARCHAR(200))
AS

   --ETL_Framework.[DW_Developer].[usp_DropConstraints] 'Finance_Warehouse'
   -- Drops all unque key and primary key constraints blocking drop/rename refresh logic... constraints likely created by data modeling (PowerBI retains the relationsihps in the model without the constraints existing)

    DECLARE @SQLCommand VARCHAR(MAX);
    SET @SQLCommand
        = 'USE ' + @DatabaseName
          + ' 
    DECLARE
	
        @TableName      VARCHAR(200),
		@SchemaName     VARCHAR(200),
        @ConstraintName VARCHAR(200),
        @ConstraintType VARCHAR(10),
        @ColumnName     VARCHAR(100),
        @ObjectType     CHAR(1),
        @Counter        INT,
        @CounterMax     INT,
        @DropSQL        VARCHAR(6000),
		@SQLInsert      VARCHAR(8000)
			   
    CREATE TABLE #Constraints
        (
            rowID          INT,
            TableName      VARCHAR(200),
			SchemaName     VARCHAR(200),
            ConstraintName VARCHAR(200),
            ConstraintType VARCHAR(20),
            ColumnName     VARCHAR(200),
            ObjectType     CHAR(1)
        )


     INSERT INTO #Constraints
  
        (
            rowID,
            TableName,
			SchemaName,
            ConstraintName,
            ConstraintType,
            ColumnName,
            ObjectType
        )
                SELECT DISTINCT
                       ROW_NUMBER() OVER (ORDER BY
                                           ConstraintName
                                         ),
                       TableName,
					   SchemaName,
                       ConstraintName,
                       ConstraintType,
                       ColumnName,
                       ObjectType
                FROM
                       (
                           SELECT
                                   tables.name               AS TableName,
                                   schemas.name              AS SchemaName,
                                   key_constraints.name      AS ConstraintName,
                                   key_constraints.type_desc AS ConstraintType,
                                   columns.name              AS ColumnName,
                                   ''T''                       AS ObjectType
                           FROM
                                   sys.tables
                               INNER JOIN
                                   sys.schemas
                                       ON tables.schema_id = schemas.schema_id
                               INNER JOIN
                                   sys.indexes
                                       ON tables.object_id = indexes.object_id
                               INNER JOIN
                                   sys.index_columns
                                       ON indexes.object_id = index_columns.object_id
                                          AND indexes.index_id = index_columns.index_id
                               INNER JOIN
-- … [164 more lines truncated, full body in data/06-procs-raw.json] --
```

---
