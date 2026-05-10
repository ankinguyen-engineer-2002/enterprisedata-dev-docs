# External ADLS Gen2 Storage

[← Cross-Workspace](README.md) · [← Root](../../README.md)

## Storage account

| Field | Value |
|---|---|
| Account | `ashleydevlake.dfs.core.windows.net` |
| Connection ID | `65655456-2ff7-4981-8911-2320b6738f35` |
| Containers | `trusted-zone`, `raw-zone` |

## Mounted shortcuts

| Lakehouse | Mounted as | Subpath |
|---|---|---|
| A_Developement | `VVSSku` | `/trusted-zone/MasterData/QTIL/VVSSku` |
| A_Developement | `Joblabor` | `/trusted-zone/Manufacturing/Maximo/Joblabor` |
| A_Developement | `Drive4AshleyEventsname` | `/trusted-zone/MasterData/ADS/GoogleAnalytics_Processed/Drive4AshleyEventsname` |
| A_Developement | `Drive4AshleyDemographicdetails` | `/trusted-zone/.../Drive4AshleyDemographicdetails` |
| A_Developement | `Drive4AshleyConversionsEventname` (×2) | `/trusted-zone/.../Drive4AshleyConversionsEventname` (duplicate) |
| A_Developement | `Testing_shortcut` | `/raw-zone/temp/fabricShortCutTesting/Testing_shortcut` |
| RadarSync_Test | `trusted-zone` | `/trusted-zone` (**entire container** ⚠️) |
| RadarSync_Test | `raw-zone` | `/raw-zone` (**entire container** ⚠️) |

## ⚠️ Risk C28

`RadarSync_Test` mounts the **entire** `trusted-zone` and `raw-zone` containers. Anyone with access to that lakehouse can read all of Maximo, MasterData, Retail raw/trusted-zone data. Restrict scope or audit access list.

---
