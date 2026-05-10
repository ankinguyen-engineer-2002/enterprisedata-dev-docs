# 💧 A_Developement
_DEV-SANDBOX tier · ID `1545d3ce-0fae-40b5-b314-ac2fd43e25c5`_

[← Lakehouses](README.md) · [← Storage](../README.md) · [← Root](../../../README.md)

## 🎯 Purpose

**Personal dev sandbox** — 3 local tables (afi_finance, drive4ashley, testing1) + 7 ADLS shortcuts trỏ external storage `ashleydevlake`.

## 📊 Stats

| Metric | Value |
|---|---|
| Tier | DEV-SANDBOX |
| Tables | 3 |
| Rows (live count) | 100,514 |
| Schemas-enabled | No (legacy `dbo` only) |
| Item ID | `1545d3ce-0fae-40b5-b314-ac2fd43e25c5` |

**Highlight:** Schemas-disabled (legacy). Smallest active LH.

## 📋 Tables (3)

**Top 30 tables by row count:**

| Schema | Table | Rows |
|---|---|---|
| `dbo` | `afi_finance_sqlprod_vvssku` | 99,814 |
| `dbo` | `drive4ashleyeventsname` | 695 |
| `dbo` | `testing1` | 5 |

## 🔗 External shortcuts (7)

| Name | Type | Target host/WS | Path |
|---|---|---|---|
| `VVSSku` | ADLS Gen2 | `https://ashleydevlake.dfs.core.windows.net` | `/trusted-zone/MasterData/QTIL/VVSSku` |
| `Testing_shortcut` | ADLS Gen2 | `https://ashleydevlake.dfs.core.windows.net` | `/raw-zone/temp/fabricShortCutTesting/Testing_shortcut` |
| `Joblabor` | ADLS Gen2 | `https://ashleydevlake.dfs.core.windows.net` | `/trusted-zone/Manufacturing/Maximo/Joblabor` |
| `Drive4AshleyEventsname` | ADLS Gen2 | `https://ashleydevlake.dfs.core.windows.net` | `/trusted-zone/MasterData/ADS/GoogleAnalytics_Processed/Drive4AshleyEventsname` |
| `Drive4AshleyDemographicdetails` | ADLS Gen2 | `https://ashleydevlake.dfs.core.windows.net` | `/trusted-zone/MasterData/ADS/GoogleAnalytics_Processed/Drive4AshleyDemographicdetails` |
| `Drive4AshleyConversionsEventname_1` | ADLS Gen2 | `https://ashleydevlake.dfs.core.windows.net` | `/trusted-zone/MasterData/ADS/GoogleAnalytics_Processed/Drive4AshleyConversionsEventname` |
| `Drive4AshleyConversionsEventname` | ADLS Gen2 | `https://ashleydevlake.dfs.core.windows.net` | `/trusted-zone/MasterData/ADS/GoogleAnalytics_Processed/Drive4AshleyConversionsEventname` |

---

**Related:** [06 Cross-Workspace](../../06-cross-workspace/README.md)
