# 🔁 MigrateData

_Item ID `370e30d6-10ad-4b3d-b220-927c299dea03`_

[← Pipelines](README.md) · [← Orchestration](../README.md) · [← Root](../../../README.md)

## Summary

Single Copy activity. CROSS-WORKSPACE COPY. Source: DataWarehouse in workspace ce4e6503-b368-496b-95e2-63b43c8b3b0a (PROD?), artifactId d27b3ef9-a331-4489-abca-588f909c4321, schema Retail_Corporate.BtaData, query selects ~90 columns where COALESCE(DateCreated,DateChanged) >= 90 days ago. Sink: Fabric DW Source_Data (artifactId f14e2ea6-ae2c-4b90-8e08-522e84f1aefc), schema Retail_Corporate.BtaData. enableStaging=true. Connection fb0943d0-5c4f-4cd4-beb1-01f032b765cd.

## Status

⚠️ **EMPTY pipeline** — no activities defined.
