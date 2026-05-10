# 🔁 test

_Item ID `9f04dcab-ba84-432b-b9d7-ebc55965b46c`_

[← Pipelines](README.md) · [← Orchestration](../README.md) · [← Root](../../../README.md)

## Summary

Despite name 'test', this is a real cross-workspace cross-warehouse copy. ForEach over array param cw_items_rob (default has 2 entries: Retail_Corporate.TransCode → Storis_DW.TransCode AND Retail_External.TransCodeMap → Rules_Engine.TransCodeMap, both with explicit TabularTranslator mappings). Source: DataWarehouse workspace ce4e6503-b368-496b-95e2-63b43c8b3b0a artifactId d27b3ef9-a331-4489-abca-588f909c4321 (PROD?), conn 73b2ec42-e074-48cf-91f2-c42cc4d1cc81. Sink: FabricSqlDatabase Commissions_Prototype (artifactId 6a9dc9e6-7296-47fb-8faa-ae9340c690f8) workspace 5360a935-..., conn 0a12ed4f-fecf-4cb9-9d0b-29334844bc8c. autoCreate, no staging.

## Status

⚠️ **EMPTY pipeline** — no activities defined.
