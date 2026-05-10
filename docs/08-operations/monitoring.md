# Monitoring System

[← Operations](README.md) · [← Root](../../README.md)

## How monitoring works

```mermaid
sequenceDiagram
    participant SP as ETL Stored Proc
    participant AL as Performance_Logs.EmailQueue
    participant ALERT as Alert_FabricTables
    participant SLA as PL_SLA_Breach
    participant CHECK as Source_EDW_Check_Test (daily 03:50 UTC)
    participant O365 as Office365 Outlook

    Note over SP,AL: Any ETL proc that fails or<br/>misses SLA writes a row.
    SP->>AL: INSERT row (Failed/Pending)
    CHECK->>SP: Truncate Bronze counts
    CHECK->>SP: usp_GenerateEmailHTML_DimCountDifference
    SP-->>AL: INSERT count-diff rows
    CHECK->>O365: Send per-row emails
    ALERT->>SP: usp_DataWarehouseDataFeedAlert_Fabric
    ALERT->>AL: SELECT WHERE status=Failed/NULL
    loop for each unsent
        ALERT->>O365: Send email
        ALERT->>AL: usp_EmailQueue_MarkSent
    end
    SLA->>SP: usp_DataWarehouseSLAAlert_Fabric
    SLA->>O365: Send to hardcoded DL
```

**Key facts:**
- `Source_EDW_Check_Test` is the **only consistently-running** pipeline (daily 03:50 UTC)
- `Alert_FabricTables_EnterpriseData` and `PL_SLA_Breach_EnterpriseData` are **manually triggered** today
- `FabricSLA_Trigger_EnterpriseData` was supposed to wrap them but is empty (risk C6)
- The `f7ca7cad-...` Office365Email connection failed with `DMTS_EntityNotFoundOrUnauthorized` on a manual run — confirm scheduled email actually delivers (C24)

---
