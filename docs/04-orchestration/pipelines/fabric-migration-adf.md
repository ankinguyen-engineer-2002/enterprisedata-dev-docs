# 🔁 Fabric Migration ADF

_Item ID `3d551bc2-56c1-4425-bc77-01d435e0f1bd`_

[← Pipelines](README.md) · [← Orchestration](../README.md) · [← Root](../../../README.md)

## Summary

Same metadata-driven shape as EDW2FabricLoader BUT source is Azure SQL DW (Synapse) Ashley_Edw via SqlDWSource, conn 8df9b408-bd4b-42ca-b8fe-7613a313cd75. Lookup still reads from ASHLEY_EDW_DEV (Azure SQL DB) FabricMapping (conn 160628f4-...). Sink: Fabric DW Source_Data (artifactId f14e2ea6-ae2c-4b90-8e08-522e84f1aefc). Adds preCopyScript: TRUNCATE TABLE before copy. Variable: Failure (String).

## Status

⚠️ **EMPTY pipeline** — no activities defined.
