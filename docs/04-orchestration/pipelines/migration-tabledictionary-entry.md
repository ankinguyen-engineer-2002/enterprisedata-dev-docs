# 🔁 Migration_TableDictionary_entry

_Item ID `78b16747-be29-46db-844e-e9b2e603a9e8`_

[← Pipelines](README.md) · [← Orchestration](../README.md) · [← Root](../../../README.md)

## Summary

Populates ETL_Framework warehouse (artifactId 02c8970b-7af3-4d4e-b011-cc3cdc3825ef) with table dictionary entries. Source: Azure SQL DW Ashley_Edw (Synapse, conn 8df9b408-bd4b-42ca-b8fe-7613a313cd75) running parameterized SELECT from dw_developer.tabledictionary. Sink: ETL_Framework.dw_developer.TableDictionary_Helper (autoCreate). Then SQL Script: MERGE-style upsert from TableDictionary_Helper into TableDictionary, drop helper table.

## Status

⚠️ **EMPTY pipeline** — no activities defined.
