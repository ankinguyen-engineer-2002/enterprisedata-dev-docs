# `usp_EmailQueue_MarkSent`

_Schema: `Performance_Logs` · Warehouse: `ETL_Framework` · Family: `email`_

_Modified: 2025-09-12 09:00:18.243000 · Code size: 331 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Write-only — writes to 1 sinks.

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

_(none detected)_

## Outputs (INSERT/UPDATE/MERGE)

- `Performance_Logs.EmailQueue`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql
CREATE   PROC Performance_Logs.usp_EmailQueue_MarkSent
   @EmailId    BIGINT,
   @Status     NVARCHAR(100) = N'Success',
   @ErrorText  NVARCHAR(MAX) = NULL
AS
BEGIN
   UPDATE Performance_Logs.EmailQueue
   SET SentAt = SYSUTCDATETIME(),
       SentStatus = @Status,
       ErrorText = @ErrorText
   WHERE EmailId = @EmailId;
END;

```

---
