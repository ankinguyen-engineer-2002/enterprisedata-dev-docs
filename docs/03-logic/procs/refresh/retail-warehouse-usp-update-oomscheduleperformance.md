# `usp_Update_OOMSchedulePerformance`

_Schema: `Retail_OOM_Enh` · Warehouse: `Retail_Warehouse` · Family: `refresh`_

_Modified: 2026-01-21 21:47:57.040000 · Code size: 12,444 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 5 sources and writes to 2 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `Retail_OOM_Enh.OOMSchedulePerformance`
- `Retail_OOM_Enh.OrderTransDetail`
- `Retail_OOM_Enh.OrderTransDetailDailyStat`
- `Source_Data.Retail_Corporate`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `Retail_OOM_Enh.OOMSchedulePerformance`

## Calls (EXEC)

- `ETL_Framework.DW_Developer`

## Code (first 80 lines)

```sql
CREATE PROCEDURE [Retail_OOM_Enh].[usp_Update_OOMSchedulePerformance]
AS
BEGIN

	DECLARE
			@String VARCHAR(5000),
			@DateValue DATETIME,
			@User VARCHAR(500),
			@DestinationDatabase VARCHAR(150),
			@DestinationSchema VARCHAR(150),
			@DestinationTable VARCHAR(150);
			      
	SET @String = 'Retail_OOM_Enh.usp_Update_OOMSchedulePerformance';
	SET @User = SYSTEM_USER;
	SET @DateValue = GETDATE();
	SET @DestinationDatabase = 'Retail_Warehouse';
	SET @DestinationSchema = 'Retail_OOM_Enh';
	SET @DestinationTable = 'OOMSchedulePerformance';

	SELECT
		@DateValue = CSTDateValue
	FROM [ETL_Framework].[DW_Developer].fn_GetDate(@DateValue);

	INSERT INTO [ETL_Framework].[DW_Developer].[AuditLog]
	VALUES
	(
		@String, @DateValue, @User, 'Process Start'
	);

	BEGIN TRY

		--TRUNCATE TABLE [Retail_OOM_Enh].[OOMSchedulePerformance];

		DECLARE @TransDate DATE = (GETDATE() - 1),
				@WrittenSales DECIMAL(19, 4),
				@TotalScheduleStore DECIMAL(19, 4),
				@TotalScheduleGRT DECIMAL(19, 4),
				@TotalScheduleDTR DECIMAL(19, 4),
				@TotalScheduleAudit DECIMAL(19, 4),
				@TotalScheduleUnassigned DECIMAL(19, 4),
				@TotalScheduleIVR DECIMAL(19, 4),
				@TotalScheduleSMS DECIMAL(19, 4),
				@AttackTarget DECIMAL(19, 4),
				@FilledCleanDelivery DECIMAL(19, 4),
				@ScheduleAtPOS DECIMAL(19, 4),
				@DaysToSchedule DECIMAL(19, 4),
				@AttackTargetNumPreviousDays INT,
				@FilledCleanTarget DECIMAL(19, 4),
				@FilledCleanDeliveryPreviousDay DECIMAL(19, 4),
				@PreviousDaysAverageWrittenSales DECIMAL(19, 4),
				@PreviousDaysAveragePrntSCDPOS DECIMAL(5, 4),
				@SMSMessagesSentCount INT,
				@AutoScheduleOrderCount INT,
				@TotalScheduleStoreOrderCount INT, 
				@TotalScheduleGRTOrderCount INT, 
				@TotalScheduleDTROrderCount INT, 
				@TotalScheduleAuditOrderCount INT, 
				@TotalScheduleUnassignedOrderCount INT, 
				@TotalScheduleIVROrderCount INT, 
				@ScheduleAtPOSOrderCount INT, 
				@TotalScheduleSMSOrderCount INT, 
				@TotalScheduleChatBotOrderCount INT,
				@TotalScheduleChatBot INT;

		SET @AttackTargetNumPreviousDays = 3;
		SET @FilledCleanTarget = 3000000;

		SELECT 
			@WrittenSales = SUM(oi.QtyOrdered * oi.CaseSellingPrice)
		FROM [Source_Data].[Retail_Corporate].[Orders] AS o
		INNER JOIN [Source_Data].[Retail_Corporate].[OrderItem] AS oi 
		ON oi.OrderID = o.OrderID
		WHERE o.RecStatus <> 'D'
		AND oi.RecStatus <> 'D'
		AND o.OrderDate = @TransDate
		AND oi.TransCodeID IN (0, 1, 7);

		-- ScheduleBy StaffTypeID is Store Ops / Sales
		SELECT	
			@TotalScheduleStore = COALESCE(SUM(otdds.OrderAmount), 0)
-- … [276 more lines truncated, full body in data/06-procs-raw.json] --
```

---
