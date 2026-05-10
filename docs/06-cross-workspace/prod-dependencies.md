# PROD Workspace Dependencies

[← Cross-Workspace](README.md) · [← Root](../../README.md)

## PROD `EnterpriseData` (`ce4e6503-...`) inventory (discovered)

| Type | Name | ID | Notes |
|---|---|---|---|
| Lakehouse | Centralized_Lakehouse | `08de1cf3-d529-4a71-8f6f-4c8d6f3b2018` |  |
| Warehouse | Source_Data | `d27b3ef9-a331-4489-abca-588f909c4321` | ← target of 12 DEV shortcuts |
| Warehouse | Retail_Warehouse | `d8bec39c-5973-47e9-aa68-67c0f0c4a771` | ← target of 6 DEV shortcuts |
| Warehouse | Centralized_Warehouse | `513a8f2c-...` |  |
| Warehouse | AI_Warehouse | `d47c0980-...` | 🆕 PROD-only (not in DEV) |
| Warehouse | A_Production2 | `67ea8404-...` | 🆕 PROD-only |
| Warehouse | Distribution_Warehouse | `c4099421-...` |  |
| Warehouse | ETL_Framework | `0d84211d-...` |  |
| Warehouse | EnterpriseData | `83183106-...` | 🆕 PROD-only |
| Warehouse | Enterprise_Warehouse | `3468b240-...` | 🆕 PROD-only |
| Warehouse | MasterData_Warehouse | `d8e6439b-...` |  |
| Warehouse | Quality_Warehouse | `063c11ae-...` | (empty in DEV too) |
| Warehouse | SupplyChain_Warehouse | `d926e44c-...` | 🆕 PROD-only |
| Warehouse | Wholesale_Warehouse | `9293af4e-...` |  |

**5 warehouses exist in PROD but not DEV**: `AI_Warehouse`, `A_Production2`, `EnterpriseData`, `Enterprise_Warehouse`, `SupplyChain_Warehouse`. These domains aren't mirrored to DEV.

## Shortcut detail

All 18 cross-WS shortcuts originate from `Centralized_Lakehouse` in DEV:

| DEV path | → Target WS | → Target item | → Target path |
|---|---|---|---|
| Tables/Retail_Sales_Enh | PROD ce4e6503 | d8bec39c (Retail_Warehouse) | Tables/Retail_Sales_Enh |
| Tables/Retail_Sales | PROD ce4e6503 | d8bec39c | Tables/Retail_Sales |
| Tables/Retail_Miniapps | PROD ce4e6503 | d27b3ef9 (Source_Data) | Tables/Retail_Miniapps |
| Tables/Retail_External | PROD ce4e6503 | d27b3ef9 | Tables/Retail_External |
| Tables/Retail_Dart | PROD ce4e6503 | d27b3ef9 | Tables/Retail_Dart |
| Tables/Retail_Corporate_Prod | PROD ce4e6503 | d27b3ef9 | Tables/Retail_Corporate |
| Tables/Retail_Corporate | PROD ce4e6503 | d27b3ef9 | Tables/Retail_Corporate |
| Tables/MasterData_Retail* | PROD ce4e6503 | d27b3ef9 | Tables/MasterData_Retail* |
| Tables/MasterData_Product* | PROD ce4e6503 | d27b3ef9 | Tables/MasterData_Product* |
| Tables/MasterData_HR_UKG_* | PROD ce4e6503 | d27b3ef9 | Tables/MasterData_HR_UKG_* |

---
