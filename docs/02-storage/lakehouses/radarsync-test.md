# 💧 RadarSync_Test
_TEST tier · ID `ddadbe2e-c2e2-4949-8e84-81eed6a81c9e`_

[← Lakehouses](README.md) · [← Storage](../README.md) · [← Root](../../../README.md)

## 🎯 Purpose

**Sandbox lakehouse** — 2 local tables (joblabor 4900 rows, test_pipeline 4 rows) + ⚠️ mounts ENTIRE trusted-zone + raw-zone ADLS containers.

## 📊 Stats

| Metric | Value |
|---|---|
| Tier | TEST |
| Tables | 2 |
| Rows (live count) | 4,904 |
| Schemas-enabled | Yes |
| Item ID | `ddadbe2e-c2e2-4949-8e84-81eed6a81c9e` |

**Highlight:** 🔴 Broad ADLS scope — anyone with this LH access reads entire dev data lake.

## 📋 Tables (2)

**Top 30 tables by row count:**

| Schema | Table | Rows |
|---|---|---|
| `dbo` | `joblabor` | 4,900 |
| `dbo` | `test_pipeline` | 4 |

## 🔗 External shortcuts (2)

| Name | Type | Target host/WS | Path |
|---|---|---|---|
| `trusted-zone` | ADLS Gen2 | `https://ashleydevlake.dfs.core.windows.net` | `/trusted-zone` |
| `raw-zone` | ADLS Gen2 | `https://ashleydevlake.dfs.core.windows.net` | `/raw-zone` |

---

**Related:** [06 Cross-Workspace](../../06-cross-workspace/README.md)
