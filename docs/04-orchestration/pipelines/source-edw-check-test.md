# 🔁 Source_EDW_Check_Test

_Item ID `d2fe32a6-1fc9-44c6-87f4-1ffa6be66344`_

[← Pipelines](README.md) · [← Orchestration](../README.md) · [← Root](../../../README.md)

## Summary

FULL data quality flow comparing EDW vs Source_Data. Lookup metadata from ETL_Framework.DW_Developer.Source_EDW_CountCheck → ForEach{ Truncate Source_Data Retail_External.EDWDimCount + EDWAggregate, IfCondition Flag==true → Copy from on-prem ASHLEY_EDW (SqlServerSource conn 3fff77ab-dcfe-4d37-aedb-c34004a36eed, Retail_Corporate.APBill etc) → Source_Data DW (artifactId f14e2ea6-...) }. Then exec usp_GenerateEmailHTML_DimCountDifference + usp_GenerateEmailHTML_DimAggregateDifference (ETL_Framework). Lookup Performance_Logs.DimEmailQueue → ForEach SendEmail (Office365Email conn f7ca7cad-8f64-4676-a3de-aaac5c547e37, recipients from row, subject 'Count Check Alert - {now}').

## Status

⚠️ **EMPTY pipeline** — no activities defined.
