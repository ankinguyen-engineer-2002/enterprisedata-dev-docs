# ⚙️ Stored Procedures (192)

[← Logic](README.md) · [← Root](../../README.md)

## Distribution

| Container | Procs | Total chars | Avg/proc |
|---|---|---|---|
| `Retail_Warehouse` | 146 | 957,087 | 6,555 |
| `ETL_Framework` | 35 | 261,467 | 7,470 |
| `Wholesale_Warehouse` | 8 | 162,408 | 20,301 |
| `Source_Data` | 2 | 9,164 | 4,582 |
| `A_Developement` | 1 | 2,393 | 2,393 |

## ETL_Framework families (35 procs)

```mermaid
graph LR
    classDef family fill:#dfe;stroke:#393;

    P_LOAD[📥 Parquet loaders<br/>13 variants<br/>Usp_CreateTableFromParquet*<br/>Usp_TableFromParquet_*]:::family
    P_INC[♻️ Incremental + CDC<br/>3 procs<br/>usp_IncrementalTableLoad*]:::family
    P_SCD[🕰️ SCD2 + Snapshot<br/>3 procs<br/>usp_SCD2_TableLoad<br/>Usp_SnapshotLoad<br/>Usp_WriteTableToParquet]:::family
    P_REF[🔄 Curated refresh<br/>3 procs<br/>usp_RefreshCuratedTableFromView<br/>+ _2 + _DateRange]:::family
    P_AUD[🔍 Audit + DQ + Alert<br/>5 procs<br/>usp_Audit_*<br/>usp_DataWarehouseAlert_*]:::family
    P_DICT[📚 Dictionary upkeep<br/>3 procs]:::family
    P_UTL[🔧 Utilities<br/>5 procs<br/>usp_DropConstraints<br/>usp_GenerateEmailHTML_*<br/>EmailQueue_MarkSent]:::family
```

## Retail_Warehouse families (146 procs)

| Family | Count | Sample procs |
|---|---|---|
| Refresh/Load | 103 | `usp_Refresh_DataSetKey`, `Usp_Refresh_EmployeeHistory`, `Usp_Refresh_MasterData_Ent` |
| Other | 43 | `usp_Buckets_Insert`, `usp_GLHist`, `usp_InvActivitySummary` |

## Wholesale_Warehouse procs (8)

| Schema | Proc name | Size (chars) |
|---|---|---|
| `dbo` | `Usp_Refresh_Wholesale_Warehouse` | 15,631 |
| `dbo` | `usp_RefreshCustomerOrders_AFI` | 3,635 |
| `dbo` | `Usp_RefreshCustomers` | 1,036 |
| `dbo` | `usp_RefreshSalesHistory_AFI` | 1,883 |
| `Placements` | `usp_Rebuild_CustItemMonthlyPlacements` | 44,316 |
| `Placements` | `usp_Rebuild_CustItemWeeklyPlacements` | 39,246 |
| `Placements` | `usp_Rebuild_InvoiceWeeklyPlacements` | 42,491 |
| `Placements` | `usp_Update_DailyPlacements` | 14,170 |

## 📂 Drill-down

Full proc bodies → [`data/06-procs-raw.json`](../../data/06-procs-raw.json) (1.5 MB raw)

Or per-warehouse details:
- [ETL_Framework](../02-storage/warehouses/etl-framework.md)
- [Retail_Warehouse](../02-storage/warehouses/retail-warehouse.md)
- [Wholesale_Warehouse](../02-storage/warehouses/wholesale-warehouse.md)

---
