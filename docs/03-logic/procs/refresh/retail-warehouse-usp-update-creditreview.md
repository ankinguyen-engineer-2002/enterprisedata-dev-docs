# `usp_Update_CreditReview`

_Schema: `Retail_Sales_Enh` · Warehouse: `Retail_Warehouse` · Family: `refresh`_

_Modified: 2026-01-21 21:47:58.633000 · Code size: 10,388 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 6 sources and writes to 3 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `Retail_Sales.CreditReview`
- `Retail_Sales_Enh.CreditApplication`
- `Retail_Sales_Enh.CreditReview`
- `Source_Data.Retail_Corporate`
- `Source_Data.Retail_External`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `Retail_Sales_Enh.CreditReview`
- `cr`

## Calls (EXEC)

- `ETL_Framework.DW_Developer`

## Code (first 80 lines)

```sql
CREATE PROCEDURE [Retail_Sales_Enh].[usp_Update_CreditReview]
AS

BEGIN

	DECLARE
			@String VARCHAR(5000),
			@DateValue DATETIME,
			@User VARCHAR(500),
			@DestinationDatabase VARCHAR(150),
			@DestinationSchema VARCHAR(150),
			@DestinationTable VARCHAR(150);
			      
	SET @String = 'Retail_Sales_Enh.usp_Update_CreditReview';
	SET @User = SYSTEM_USER;
	SET @DateValue = GETDATE()
	SET @DestinationDatabase = 'Retail_Warehouse'
	SET @DestinationSchema = 'Retail_Sales_Enh'
	SET @DestinationTable = 'CreditReview';

	SELECT
		@DateValue = CSTDateValue
	FROM [ETL_Framework].[DW_Developer].fn_GetDate(@DateValue);

	INSERT INTO [ETL_Framework].[DW_Developer].[AuditLog]
	VALUES
	(
		@String, @DateValue, @User, 'Process Start'
	);

	BEGIN TRY

		--TRUNCATE TABLE [Retail_Sales_Enh].[CreditReview];
		
		UPDATE src
		SET OriginalQueuedDateTime = CASE WHEN dst.OriginalQueuedDateTime IS NULL
									 THEN src.RequestDateTime
									 ELSE dst.OriginalQueuedDateTime END
		FROM [Retail_Sales].[CreditReview] src
		LEFT OUTER JOIN [Retail_Sales_Enh].[CreditReview] dst 
		ON src.CreditReviewID = dst.CreditReviewID
		AND	src.CreditSourceTypeID = dst.CreditSourceTypeID
		AND	src.SourceID = dst.SourceID;

		UPDATE	src
		SET CreditAppNumber = crdata.RowNum,
			AppCount = CASE WHEN crdata.RowNum = 1 THEN 1 ELSE 0 END,
			AdjustedStatusCodeID = crdata.AdjustedStatusCodeID
		FROM	
		(
			SELECT 
				ROW_NUMBER() OVER (PARTITION BY cr.StoreID, cr.CustomerID, CAST(cr.RequestDateTime AS DATE) ORDER BY cs.ShortDescription) AS RowNum,
				cr.CreditSourceTypeID,
				cr.CreditReviewID,
				cr.SourceID,
				CASE WHEN tfpm.PaymentTypeVendorID LIKE 'GENESIS%' AND cs.ShortDescription = 'Pending' THEN 7
				ELSE cr.CreditRequestStatusCodeID
				END AS AdjustedStatusCodeID
				FROM [Retail_Sales].[CreditReview] AS cr
				LEFT JOIN [Source_Data].[Retail_Corporate].[CreditRequestStatusCode] AS cs
				ON cs.CreditRequestStatusCodeID = cr.CreditRequestStatusCodeID
				LEFT JOIN [Source_Data].[Retail_External].[FinanceProviderMapping] AS tfpm 
				ON cr.FinanceProviderID = tfpm.FinanceProviderID
				--WHERE cr.CreditRequestStatusCodeID <> 9
		) crdata
		INNER JOIN [Retail_Sales].[CreditReview] src 
		ON src.CreditReviewID = crdata.CreditReviewID
		AND src.CreditSourceTypeID = crdata.CreditSourceTypeID
		AND src.SourceID = crdata.SourceID;

		UPDATE dst
		SET AmountApproved = src.AmountApproved
			, ConditionalLetterRequired = src.ConditionalLetterRequired
			, CosignerCustomerID = src.CosignerCustomerID
			, CreditApplicationID = src.CreditApplicationID
			, CreditBureauID = src.CreditBureauID
			, CreditReportDate = src.CreditReportDate
			, CreditRequestStatusCodeID = src.CreditRequestStatusCodeID
			, CreditReviewStatusCodeID = src.CreditReviewStatusCodeID
			, CreditScore = src.CreditScore
-- … [239 more lines truncated, full body in data/06-procs-raw.json] --
```

---
