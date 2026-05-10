# 🔁 Alert_FabricTables_EnterpriseData

_Item ID `6e46ee2f-ec35-4169-87b7-96a64b77e103`_

[← Pipelines](README.md) · [← Orchestration](../README.md) · [← Root](../../../README.md)

## Summary

Alerting via Office365Outlook Logic App (NOT Office365Email activity). Variables: Message, Subject, To, JsonPayload (string). Run usp_DataWarehouseDataFeedAlert_Fabric → Lookup [Performance_Logs].[EmailQueue] WHERE SentStatus='Failed' OR null → ForEach{ Set To/Message/Subject from item, SendEmail (Office365Outlook /v2/Mail), Stored procedure1 usp_EmailQueue_MarkSent(EmailId) }. Logic Apps Office365 connection: /subscriptions/07be1452-124c-4a2c-8d72-751fc8e12b5b/.../Microsoft.Web/connections/1_6e46ee2f-..._cbb2badd-71c2-4ea3-9b50-63cb182016f2 (eastus).

## Status

⚠️ **EMPTY pipeline** — no activities defined.
