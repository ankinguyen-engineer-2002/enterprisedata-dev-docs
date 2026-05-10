# 📊 08 — Operations

[← Root](../../README.md)

## Run reality

![Run reality](../../images/08-run-reality.svg)

- **3** items have run history in API window
- **38** items dormant (never ran or older than window)

## ✅ Active items

| Item | Type | # Runs | Last run | Last status |
|---|---|---|---|---|
| `Source_EDW_Check_Test` | DataPipeline | 64 | 2026-05-08T03:50:01 | Completed |
| `Retail_Prod_To_Dev_DataBackFill` | DataPipeline | 58 | 2026-04-29T05:12:23 | Completed |
| `Notebook 13` | Notebook | 1 | 2026-04-21T07:21:29 | Completed |

## 💤 Dormant items

All other 38 orchestration items have no recent run history. See [run-history.md](run-history.md) for full list.

## 🐍 Spark Environments

| Env | Runtime | Pool | Dynamic alloc | Libraries | Last published |
|---|---|---|---|---|---|
| `Env01` | **1.2** ⚠️ | Starter Pool 8c/56g | 1–9 | `pandas==2.2.2` | 2024-04-24 |
| `Dev` | **1.3** | Starter Pool 8c/56g | 1–9 | (none) | 2025-06-10 |

**Risk C12**: Env runtime drift — `Env01` on 1.2 vs `Dev` on 1.3.

## Sub-pages

- [Run history](run-history.md) — full per-item run breakdown
- [Monitoring](monitoring.md) — `Source_EDW_Check_Test` daily + alert pipelines
- [Environments](environments.md) — Spark configs detail

---
