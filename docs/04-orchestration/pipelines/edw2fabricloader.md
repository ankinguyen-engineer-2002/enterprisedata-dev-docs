# 🔁 EDW2FabricLoader

_Item ID `28d162b6-5baa-4d35-9a7c-6c605bb6a826`_

[← Pipelines](README.md) · [← Orchestration](../README.md) · [← Root](../../../README.md)

## Summary

Metadata-driven copy from Azure SQL DB ASHLEY_EDW_DEV.dw_developer.FabricMapping → Fabric DW (artifactId f14e2ea6-ae2c-4b90-8e08-522e84f1aefc = Source_Data warehouse). Filters by Flag=1, executes per-row Query, updates status back.

## Activities tree

```mermaid
graph TB
    a1[MetadataTableLookup<br/><i>Lookup</i>]
    a2[FilterEnabled<br/><i>Filter</i>]
    a1 --> a2
    a3[ForEach<br/><i>ForEach</i>]
    a2 --> a3
    a4[LoadFabricTable<br/><i>Copy</i>]
    a3 --> a4
    a5[SucessLoad<br/><i>Script</i>]
    a3 --> a5
    a6[ErrorMessage<br/><i>SetVariable</i>]
    a3 --> a6
    a7[FailureLoad<br/><i>Script</i>]
    a3 --> a7
```

## Activity-by-activity

| Activity | Type | Detail |
|---|---|---|
| MetadataTableLookup | Lookup | Source type: `AzureSqlSource`<br/>Query (truncated): `SELECT EDWTableName, EDWSchemaName, FabricSchemaName, FabricDataBaseName, Query, Flag, LastloadStatus, LastLaodDate FROM [dw_developer].[FabricMapping]` |
| FilterEnabled | Filter | Filter expr: `@equals(item().Flag,1)` |
| ForEach | ForEach | Items: `@activity('FilterEnabled').output.value` · Sequential: False · BatchCount: — |
| &nbsp;&nbsp;LoadFabricTable | Copy | Source: `None`<br/>Sink: `None` |
| &nbsp;&nbsp;SucessLoad | Script | — |
| &nbsp;&nbsp;ErrorMessage | SetVariable | Variable `?` = `` |
| &nbsp;&nbsp;FailureLoad | Script | — |

## Variables

| Name | Type |
|---|---|
| `ErrorMessage` | String |

## Raw definition

Full JSON: [`data/pipelines/EDW2FabricLoader.json`](../../../data/pipelines/EDW2FabricLoader.json)

---
