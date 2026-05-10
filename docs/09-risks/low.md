# 🟡 Low Risks (15)

[← Risks](README.md) · [← Root](../../README.md)

| # | Category | Issue | Target | Action |
|---|---|---|---|---|
| C9 | Architecture | Stranded business tables in ETL_Framework (Manufacturing_Maximo.Fedex etc.) | `ETL_Framework` | Move to domain WHs |
| C10 | Maintainability | 4 clones of TableDictionary (`_clone`, `_edw_1`, `_Test`, `_Security`) | `ETL_Framework` | Consolidate; document authoritative copy |
| C11 | Cleanup | Two empty Dataflow staging LH+WH pairs | `DataflowsStaging*` | Delete after confirming Dataflow Test empty |
| C12 | Compatibility | Env runtime drift: Env01 on 1.2, Dev on 1.3 | `environments` | Migrate Env01 to 1.3 |
| C13 | Cleanup | 5 empty test pipelines | `test pipelines` | Delete |
| C14 | Naming | `test` and `pipeline1` are real cross-WS PROD copies | `test+pipeline1` | Rename to descriptive names |
| C15 | Notebooks | `Notebook 13` runs `sc.addPyFile('https://raw.githubusercontent.com/microsoft/fabric-samples/.../util.py')` | `Notebook 13` | Pin to commit SHA or vendor in Environment library |
| C16 | Notebooks | `Vers 5` references stale lakehouse GUID `75f83a27-...` | `Vers 5` | Update or remove |
| C17 | Notebooks | `Sys_Data_pull` cell 1 saveAsTable contract mismatch | `Sys_Data_pull` | Use cell 4's mature impl |
| C18 | Notebooks | `delta_table_path2` undefined in `Rename column names` | `Rename column names` | Fix or remove |
| C19 | Procs | 13 variants of `Usp_CreateTableFromParquet*` | `ETL_Framework` | Consolidate; deprecate dead variants |
| C20 | Centralized_LH | `Retail_Corporate` and `Retail_Corporate_Prod` 1:1 mirror at 5.92B rows | `Centralized_Lakehouse` | Identify canonical; delete duplicate |
| C21 | Permissions | 12 individual user Admins on Dev workspace + 1 broad group | `permissions` | Adopt least-privilege |
| C22 | Descriptions | 70/71 items have empty descriptions | `all items` | Add description for production items |
| C23 | Test sandbox | `Test_Owneraccess` warehouse left over from permissions probe | `Test_Owneraccess` | Delete |

---
