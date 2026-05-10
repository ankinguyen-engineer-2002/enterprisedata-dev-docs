# 📚 Glossary

[← Reference](README.md) · [← Root](../../README.md)

## Fabric concepts

| Term | Definition |
|---|---|
| **Workspace** | Logical container in Microsoft Fabric grouping items under one capacity |
| **Capacity** | Compute SKU billed per-hour. East US dedicated 'Large dataset format' for this WS |
| **Warehouse (Fabric)** | T-SQL relational engine on top of OneLake parquet. Supports stored procs, views, MERGE, COPY INTO. Read/write |
| **Lakehouse** | Delta Lake tables + Files folder on OneLake. Has auto-generated SQL Endpoint (read-only T-SQL view) |
| **Schema-enabled Lakehouse** | Newer Fabric feature — supports SQL `[schema].[table]` namespace (legacy LH only `dbo`) |
| **OneLake** | Unified storage (ADLS Gen2 underneath) for all Fabric items. URL pattern `abfss://<wsid>@onelake.dfs.fabric.microsoft.com/<itemid>/Tables/...` |
| **Shortcut** | OneLake symbolic link — point a path in this LH/WH to data in another LH/WH (cross-WS) or external storage. No data copy |
| **SQL Endpoint** | Auto-generated read-only T-SQL surface for a Lakehouse |
| **Data Pipeline** | Visual ETL workflow with activities (Copy, Lookup, ForEach, Script, Notebook, IfCondition, ExecutePipeline). Similar to ADF pipeline |
| **Mounted DataFactory** | Reference link to an existing Azure Data Factory — its pipelines surface inside Fabric without duplication |
| **MirroredAzureDatabricksCatalog** | Live read-only mirror of a Databricks Unity Catalog into Fabric OneLake. Supports Full or Selective mode + autoSync |
| **Dataflow Gen2** | Power Query M-based no-code data prep, with auto-staging Lakehouse + Warehouse |
| **Reflex (Activator)** | Event-driven trigger that watches data and fires actions |
| **Spark Environment** | Reusable compute config (runtime version, pool, libraries) for Spark notebooks/jobs |
| **Semantic Model** | Power BI dataset (renamed). Tabular data model with measures/relationships, queryable via DAX |

## Ashley Furniture domain terms

| Term | Meaning |
|---|---|
| **EDW** | Enterprise Data Warehouse — legacy on-prem SQL Server `ASHLEY_EDW_DEV` / `Ashley_Edw` (Synapse) |
| **AFI** | Ashley Furniture Industries — corp brand. `MasterData_ItemMaster_AFI` = item master domain |
| **UKG** | UKG Pro / Kronos — HR + workforce management SaaS. Schemas `MasterData_HR_UKG_*` |
| **Maximo** | IBM Maximo — manufacturing / asset management. Schema `Manufacturing_Maximo` |
| **AshleyServiceNow** | ServiceNow ITSM. Tables `Retail_DW.AshleyServiceNow*` |
| **ADS** | Ashley Data Source / Ad Services — Google Analytics processed feeds. Subpath `MasterData/ADS/GoogleAnalytics_Processed/Drive4Ashley*` |
| **QTIL** | Quality / supplier-related domain. Subpath `MasterData/QTIL/VVSSku` |
| **Storis_DW** | Storis ERP-related schema in `Commissions_Prototype` |
| **RadarSync** | Internal sync mechanism (`UpdateLog_RadarSync` table) |
| **EDWELoader** | EDW-to-Fabric loader nomenclature (EDW2FabricLoader pipeline) |

## Naming conventions observed

| Pattern | Meaning |
|---|---|
| `_AGR`, `_DSG`, `_Wrk`, `_Enh` suffixes | UKG HR data stages (Agreement/Design/Working/Enhanced) |
| `_Wrk` schema/views | 'Working set' views — feed `usp_RefreshCuratedTableFromView` procs |
| `Retail_Corporate` vs `Retail_Corporate_Prod` | Twin schemas — both shortcuts to PROD `Retail_Corporate` (not duplicated storage) |
| `Vers 5`, `Vers 5 Copy`, `Vers 5new` | Notebook duplicates indicating editing without consolidation |
| `Usp_*` PascalCase | Stored procedure |
| `usp_*` lowercase | Stored procedure (mixed convention) |
| `_clone`, `_Test`, `_Security`, `_edw_1` | TableDictionary clones — sandbox/security/legacy snapshots |
| `Files/<GUID>` | Fabric-internal physical backing for warehouse tables (NOT user shortcuts) |

---
