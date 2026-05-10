# `usp_GrantSchemaSecurity`

_Schema: `DW_Developer` · Warehouse: `ETL_Framework` · Family: `other`_

_Modified: 2025-08-22 15:01:35.580000 · Code size: 3,042 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Read-only — pulls data from 2 sources. Calls 1 other procs.

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `DW_Developer.TableDictionary_Security`
- `metadata`

## Outputs (INSERT/UPDATE/MERGE)

_(none detected)_

## Calls (EXEC)

- `them`

## Code (first 80 lines)

```sql

create PROC [DW_Developer].[usp_GrantSchemaSecurity] AS

--- Generate Grants from metadata table.... the process will generate grants and execute them regardless if they exist or not.   
--- Regranting doesn't throw an error and with coalation differences on Master data sys objects it's difficult to caputure what 
--- doesn't exist yet... that can be a future enhancement
---  SQL_Latin1_General_CP1_CI_AS  vs Latin1_General_100_CI_AS_KS_WS_SC_UTF8


SELECT distinct PermissionType+ ' ON SCHEMA :: ' + schemas.name +' TO ['+ Username+'] ' from 
(SELECT 'GRANT SELECT' PermissionType, UserName, SchemaMapping,Include_WRK_Schemas,Include_XBK_Schemas
FROM DW_Developer.TableDictionary_Security WHERE [Select] = 1
UNION ALL 
SELECT 'GRANT ALTER' PermissionType, UserName, SchemaMapping,Include_WRK_Schemas,Include_XBK_Schemas
FROM DW_Developer.TableDictionary_Security WHERE [Alter] = 1
UNION ALL 
SELECT 'GRANT INSERT' PermissionType, UserName, SchemaMapping,Include_WRK_Schemas,Include_XBK_Schemas
FROM DW_Developer.TableDictionary_Security WHERE [Insert] = 1
UNION ALL 
SELECT 'GRANT UPDATE' PermissionType, UserName, SchemaMapping,Include_WRK_Schemas,Include_XBK_Schemas
FROM DW_Developer.TableDictionary_Security WHERE [Update] = 1
UNION ALL 
SELECT 'GRANT DELETE' PermissionType,UserName, SchemaMapping,Include_WRK_Schemas,Include_XBK_Schemas
FROM DW_Developer.TableDictionary_Security WHERE [Delete] = 1
UNION ALL 
SELECT 'GRANT VIEW DEFINITION' PermissionType,  UserName, SchemaMapping,Include_WRK_Schemas,Include_XBK_Schemas
FROM DW_Developer.TableDictionary_Security WHERE [ViewDefinition] = 1
UNION ALL 
SELECT 'GRANT CONTROL' PermissionType, UserName, SchemaMapping,Include_WRK_Schemas,Include_XBK_Schemas
FROM DW_Developer.TableDictionary_Security WHERE [Control] = 1
UNION ALL 
SELECT 'GRANT REFERENCES' PermissionType, UserName, SchemaMapping,Include_WRK_Schemas,Include_XBK_Schemas
FROM DW_Developer.TableDictionary_Security WHERE [References] = 1
UNION ALL 
SELECT 'GRANT EXECUTE' PermissionType, UserName, SchemaMapping,Include_WRK_Schemas,Include_XBK_Schemas
FROM DW_Developer.TableDictionary_Security WHERE [Execute] = 1
UNION ALL
SELECT 'GRANT UNMASK' PermissionType, UserName, SchemaMapping,Include_WRK_Schemas,Include_XBK_Schemas
FROM DW_Developer.TableDictionary_Security WHERE [Unmask] = 1

) T1 
JOIN sys.schemas on name like SchemaMapping
 and schemas.name not like CASE WHEN [Include_WRK_Schemas] = 1 THEN 'Z$Z@Z' ELSE '%WRK' END 
 and schemas.name not like CASE WHEN [Include_XBK_Schemas] = 1 THEN 'Z$Z@Z' ELSE '%XBK' END 
LEFT JOIN 
(
SELECT  USER_NAME(grantee_principal_id) as username2,SCHEMA_NAME(major_id) as schemaname2, [Permission_name]
FROM sys.database_permissions AS Perm
left JOIN sys.database_principals AS Prin
ON Perm.major_ID = Prin.principal_id AND class_desc = 'SCHEMA'
where SCHEMA_NAME(major_id) is not null 
) t2 on schemas.name = schemaname2 and userName = username2 and PermissionType= 'GRANT '+[Permission_name]
 where schemaname2 is null
```

---
