# 🌊 Dataflow Gen2 `Dataflow Test`

[← Orchestration](README.md) · [← Root](../../README.md)

## Status: 💀 EMPTY

`getDefinition` returns this M code:

```m
[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
```

No queries, no connections.

## Auto-staging companions

Fabric auto-creates these alongside any Dataflow Gen2:
- `DataflowsStagingLakehouse` (LH) — empty
- `StagingLakehouseForDataflows_20251008191803` (LH timestamped) — empty
- `DataflowsStagingWarehouse` (WH) — empty
- `StagingWarehouseForDataflows_20251008191817` (WH timestamped) — empty
- `DataflowsStagingWarehouse` (SemanticModel) — auto-generated

All safe to delete if `Dataflow Test` stays empty (risk **C11**).

---
