# `usp_Full_Refresh_SalesOrderHeader`

_Schema: `Retail_Sales_Enh` · Warehouse: `Retail_Warehouse` · Family: `refresh`_

_Modified: 2026-01-21 21:48:08.697000 · Code size: 29,260 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 13 sources and writes to 6 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). Uses explicit transaction. ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `ETL_Framework.DW_Developer`
- `InvoiceItem`
- `MasterData_Product.ProductGroup`
- `MasterData_Product_Enh.ProductInfo`
- `MasterData_Retail_Ent.StoreLocation`
- `Retail_Sales.SalesOrderHeader`
- `Retail_Sales.SalesOrderLine`
- `Retail_Sales_Enh.SalesAssociateCommission`
- `Retail_Sales_Enh.SalesOrderHeader`
- `Retail_Sales_Enh.SalesOrderLine`
- `Retail_Sales_Enh.SalesOrderLineHistory`
- `Source_Data.Retail_Corporate`
- `Source_Data.Retail_External`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `OH`
- `Retail_Sales.SalesOrderHeader`
- `Retail_Sales_Enh.SalesOrderHeader`
- `SFMC`
- `oh`

## Calls (EXEC)

- `ETL_Framework.DW_Developer`

## Code (first 80 lines)

```sql


CREATE   PROCEDURE [Retail_Sales_Enh].[usp_Full_Refresh_SalesOrderHeader]
AS

BEGIN
	
	DECLARE
            @String VARCHAR(5000),
            @DateValue DATETIME,
            @User VARCHAR(500),
			@DestinationDatabase VARCHAR(150),
			@DestinationSchema VARCHAR(150),
			@DestinationTable VARCHAR(150);
			      
    SET @String = 'Retail_Sales_Enh.usp_Full_Refresh_SalesOrderHeader' ;
    SET @User = SYSTEM_USER;
    SET @DateValue = GETDATE()
	SET @DestinationDatabase = 'Retail_Warehouse'
	SET @DestinationSchema = 'Retail_Sales_Enh'
	SET @DestinationTable = 'SalesOrderHeader';

    SELECT
        @DateValue = CSTDateValue
    FROM [ETL_Framework].[DW_Developer].fn_GetDate(@DateValue);

    INSERT INTO [ETL_Framework].[DW_Developer].[AuditLog]
    VALUES
    (
        @String, @DateValue, @User, 'Process Start'
    );

    BEGIN TRY

		TRUNCATE TABLE [Retail_Sales_Enh].[SalesOrderHeader];

		DECLARE @MaxID BIGINT = (SELECT ISNULL(MAX(OrderKey),0) FROM [Retail_Sales_Enh].[SalesOrderHeader]);

		--DECLARE @StartDate DATE = GETDATE()-3
		--		, @EndDate DATE = GETDATE();

		UPDATE [Retail_Sales].[SalesOrderHeader]
		SET MerchSubTotal = 0
			, InstallationCharge = 0
			, DeliveryCharge = 0
			, TotalAdditionalTaxAmount = 0
			, TotalStateTaxAmount = 0
			, FinanceAmount = 0
			, TotalInvoiceAmount = 0
			, DeliveryChargeCalculated = 0
		WHERE OrderStatus = 'Written' 
		AND RecStatus = 'D';

		SELECT oh.SourceOrderID
			   , SUM(ofmnt.MerchSubTot) ofMerchSubTotal
			   , SUM(ofmnt.DlvyChrg) AS DeliveryCharge
			   , SUM(ofmnt.InstallationChrg) AS InstallationCharge
			   , MAX(COALESCE(ofmnt.DlvyChrgCalculated, 0)) AS DeliveryChargeCalculated
		INTO #Ofment
		FROM [Retail_Sales].[SalesOrderHeader] oh
		INNER JOIN [Source_Data].[Retail_Corporate].[OrderFulfillment] ofmnt
		ON ofmnt.OrderID = oh.SourceOrderID
		WHERE oh.OrderStatus = 'Written' 
		AND ofmnt.RecStatus <> 'D'
		GROUP BY oh.SourceOrderID;

		UPDATE o
		SET o.MerchSubTotal = ofmnt.ofMerchSubTotal
			, o.DeliveryCharge = ofmnt.DeliveryCharge
			, o.InstallationCharge = ofmnt.InstallationCharge
			, o.DeliveryChargeCalculated = ofmnt.DeliveryChargeCalculated
		FROM [Retail_Sales].[SalesOrderHeader] o
		INNER JOIN #Ofment ofmnt
		ON o.SourceOrderID = ofmnt.SourceOrderID
		WHERE o.OrderStatus = 'Written';

		IF OBJECT_ID('tempdb..#OrderData') IS NOT NULL 
		DROP TABLE #OrderData;

		SELECT 
-- … [866 more lines truncated, full body in data/06-procs-raw.json] --
```

---
