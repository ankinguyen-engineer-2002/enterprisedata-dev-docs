# Bronze → Silver (Domain Warehouses)

[← Data Flow](README.md) · [← Root](../../README.md)

## Pattern

```sql
-- Conceptual pattern (per curated table)
EXEC ETL_Framework.DW_Developer.usp_RefreshCuratedTableFromView
    @TargetSchema = 'MasterData_Retail',
    @TargetTable  = 'SalesPerson',
    @SourceView   = 'Source_Data.MasterData_Retail_Wrk.vw_SalesPerson_Working';
```

The proc:
1. Reads from a `_Wrk` Working-set view in `Source_Data` (or a domain warehouse's _Wrk schema)
2. Performs INSERT/UPDATE/MERGE into the target curated table
3. Writes to `ETL_Framework.DW_Developer.AuditLog`

## Domain → procs ratio

| Domain | Tables | Views | Procs internal | Pattern |
|---|---|---|---|---|
| Retail_Warehouse | 198 | 29 (incl. 14 `Retail_Sales_Wrk`) | 146 | Refresh-Load + MERGE + Validate + Audit |
| Wholesale_Warehouse | 209 | 114 `_Wrk` views | 8 (large, ~20K avg) | Multi-table MERGE-heavy |
| MasterData_Warehouse | 46 | — | 0 (driven by ETL_Framework) | External orchestration |
| Distribution_Warehouse | 7 | — | 0 | External orchestration |
| Quality_Warehouse | 0 | — | 0 | 🔴 Empty |

---
