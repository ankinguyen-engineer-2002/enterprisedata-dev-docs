# 🔁 SysTable_Dynamic

_Item ID `cd326847-c25b-408d-8f9e-e086d4cec8e8`_

[← Pipelines](README.md) · [← Orchestration](../README.md) · [← Root](../../../README.md)

## Summary

Variant of SysTable_Snapshot. Same lookup [Centralized_Warehouse].[MetaData].[SysObjectInfo] IsEnabled=1 (artifactId c5a1f95b-...) → ForEach1{ Copy data1: source DataWarehouse @item().SourceWarehouse → sink DataWarehouse @item().TargetWarehouse, schema 'Source_Data_<schema>_adf', precopy drop table IF EXISTS Source_Data_<schema>_adf.<table>, autoCreate }. NO usp_Audit_Fabric_Tables call. Likely targets ADF-mounted source warehouses.

## Status

⚠️ **EMPTY pipeline** — no activities defined.
