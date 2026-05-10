# 🔬 Methodology

[← Reference](README.md) · [← Root](../../README.md)

## How data was collected

| Phase | Approach |
|---|---|
| Inventory + IDs | `GET https://api.fabric.microsoft.com/v1/workspaces/{ws}/items` → `00-inventory-with-ids.json` |
| Permissions | Power BI `/myorg/groups/{id}/users` (Fabric `/v1/workspaces/{id}/roleAssignments` returned 403 in this scope) |
| Per-item metadata | `GET /v1/workspaces/{ws}/items/{itemId}` (no createdDate/modifiedDate exposed) |
| Warehouse + Lakehouse SQL | `pyodbc` over ODBC Driver 18 for SQL Server with AAD access token. All queries READ-ONLY (`SELECT`, `INFORMATION_SCHEMA`, `COUNT_BIG`) |
| Pipeline definitions | `POST /v1/workspaces/{ws}/dataPipelines/{id}/getDefinition` then base64-decode `definition.parts[].payload` |
| Notebook definitions | `POST /v1/workspaces/{ws}/notebooks/{id}/getDefinition?format=ipynb` then base64-decode parts |
| Mirror config | `GET /v1/workspaces/{ws}/mirroredAzureDatabricksCatalogs/{id}` plus status endpoint |
| Mounted ADF | `GET /v1/workspaces/{ws}/mountedDataFactories/{id}` |
| Reflex | `getDefinition` failed with `Activator_Export_FailedToExportActivator_ReflexBackendError` |
| Stored procs + views | `SELECT m.definition FROM sys.sql_modules m JOIN sys.procedures/views` |
| Shortcuts | `GET /v1/workspaces/{ws}/items/{itemId}/shortcuts` per item |
| Files/ folder enum | OneLake DFS `?resource=filesystem&recursive=false&directory=Files` recursively |
| Run history | `GET /v1/workspaces/{ws}/items/{itemId}/jobs/instances?$top=30` per item |

## Constraints encountered

- Item-level `createdDate` / `modifiedDate` / `lastModifiedBy` are **not exposed** by the Fabric `/v1/items/{id}` endpoint
- Fabric Lakehouse SQL endpoints return **0** from `sys.partitions.rows` (used `COUNT_BIG(*)` instead)
- Workspace `13eefa5e-...` returned 403 Forbidden when listing items
- 4 lakehouse GUIDs referenced by notebooks but not in any accessible workspace

## Confidence tagging

Per the SUPER RULE §0 zero-hallucination guideline:
- **[Verified]** — observed directly in data/code
- **[Likely]** — strong inference from context
- **[Speculation]** — guess, needs owner confirmation

---
