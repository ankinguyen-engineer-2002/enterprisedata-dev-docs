# 🏭 Mounted Data Factory `ashleyv2datafactory`

[← Orchestration](README.md) · [← Root](../../README.md)

## Configuration

| Field | Value |
|---|---|
| Item ID | `ab9391a5-3161-4a74-9cfc-c5bdc28f902f` |
| Type | MountedDataFactory |
| Resource path | `/subscriptions/68cde257-828b-4f5e-a7f1-4eb9683c89d6/resourceGroups/IoT_Hub/providers/Microsoft.DataFactory/factories/ashleyv2datafactory` |
| Subscription | `68cde257-...` |
| Resource group | `IoT_Hub` |
| ADF name | `ashleyv2datafactory` |
| Mode | Mount-only (legacy ADF surfaced inside Fabric) |

## 🔗 What it surfaces

This isn't a Fabric pipeline — it's a **link** to an external Azure Data Factory whose pipelines are visible inside this Fabric workspace. The legacy ADF predates the BI/data platform consolidation (RG name `IoT_Hub` is a hint).

## 🔍 Indirect references

- `SysTable_Dynamic` pipeline targets `Source_Data_<schema>_adf` schemas — the `_adf` suffix indicates ADF-driven loads.
- ADF pipelines visible from here populate `Source_Data` warehouse via the same flows.

---
