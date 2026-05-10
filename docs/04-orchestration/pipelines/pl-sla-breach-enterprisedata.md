# 🔁 PL_SLA_Breach_EnterpriseData

_Item ID `3d156c8a-49e3-4d86-abee-bce9a815e1e4`_

[← Pipelines](README.md) · [← Orchestration](../README.md) · [← Root](../../../README.md)

## Summary

SLA breach alerting. Run usp_DataWarehouseSLAAlert_Fabric → Lookup Performance_Logs.EmailQueue (Failed/null) → ForEach{ Office365Email1 send to DL_AFI_Data_WarehouseGCC@Ashleyfurniture.com (HARDCODED recipient), Stored procedure1 usp_EmailQueue_MarkSent(EmailId, retry 3) }. Office365Email connection af7880ae-4d79-4e37-b7a7-c4a8e18bd5ae.

## Status

⚠️ **EMPTY pipeline** — no activities defined.
