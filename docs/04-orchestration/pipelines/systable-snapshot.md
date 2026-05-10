# 🔁 SysTable_Snapshot

_Item ID `893e6a5e-c5af-4682-9fc6-2918f9d0d6c0`_

[← Pipelines](README.md) · [← Orchestration](../README.md) · [← Root](../../../README.md)

## Summary

DYNAMIC cross-warehouse snapshot copy. Lookup [Centralized_Warehouse].[MetaData].[SysObjectInfo] WHERE IsEnabled=1 (artifactId c5a1f95b-f9db-4cb7-8ded-396ea70da572) → ForEach1{ Copy data1: source DataWarehouse @item().SourceWarehouse → sink DataWarehouse @item().TargetWarehouse, target schema 'Source_Data_'+@item().schemaName, table @item().tableName, preCopyScript drop table IF EXISTS Source_Data_<schema>.<table>, autoCreate, retry 3 } → Stored procedure1 usp_Audit_Fabric_Tables (ETL_Framework). Parameters: WorkspaceId default=5360a935-..., ConnectionString default endpoint of fabric DW.

## Status

⚠️ **EMPTY pipeline** — no activities defined.
