# 🟠 Medium Risks (8)

[← Risks](README.md) · [← Root](../../README.md)

| # | Category | Issue | Target | Action |
|---|---|---|---|---|
| C26 | Operations | 38/41 orchestration items have no recent run history | `run history` | Audit dormants; remove unused |
| C27 | Lineage | 4 unresolvable lakehouses referenced by notebooks | `notebooks` | Document or remove broken refs |
| C4 | Maintainability | 3 near-duplicate `Vers 5` notebooks with subtle differences and stale lakehouse GUIDs | `Vers5 trio` | Collapse to one parameterized notebook |
| C5 | Reliability | `Retail_Prod_To_Dev_DataBackFill` snapshot Inactive; failures stable since 2026-04-29 | `Retail_Prod_To_Dev_DataBackFill` | Audit; fix and re-enable or delete |
| C6 | Orchestration | `FabricSLA_Trigger_EnterpriseData` empty (intended scheduler wrapper) | `FabricSLA_Trigger_EnterpriseData` | Build or delete |
| C7 | Notification | Hardcoded email recipient in `PL_SLA_Breach` | `PL_SLA_Breach` | Move to EnvironmentControl config table |
| C8 | Orchestration | `Reflex 2024-05-29` cannot export — likely abandoned | `Reflex` | Confirm and delete |
| C24 | DQ | Office365Email connection `f7ca7cad-...` failed `DMTS_EntityNotFoundOrUnauthorized` on manual run | `Source_EDW_Check_Test` | Confirm scheduled branch actually delivers |

---
