# `usp_Update_SalesOrderHeader`

_Schema: `Retail_Sales_Enh` · Warehouse: `Retail_Warehouse` · Family: `refresh`_

_Modified: 2026-03-29 16:12:55.483000 · Code size: 37,869 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 18 sources and writes to 7 sinks. Calls 1 other procs. Has error handling (TRY/CATCH). Uses explicit transaction. ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `Centralized_Lakehouse.Retail_Corporate`
- `Centralized_Lakehouse.Retail_External`
- `ETL_Framework.DW_Developer`
- `InvoiceItem`
- `MasterData_Product.ProductGroup`
- `MasterData_Product_Enh.ProductInfo`
- `MasterData_Retail_Ent.DataSetKey`
- `MasterData_Retail_Ent.StoreLocation`
- `Pradeep`
- `Retail_Sales.SalesAssociateCommission`
- `Retail_Sales.SalesOrderFulfillment`
- `Retail_Sales.SalesOrderHeader`
- `Retail_Sales.SalesOrderLine`
- `Retail_Sales.SalesOrderLineHistory`
- `Retail_Sales_Enh.SalesOrderHeader`
- `Retail_Sales_Enh.SalesOrderLine`
- `SalesOrderLine*/`
- `Source_Data.Retail_Corporate_SCD`

## Outputs (INSERT/UPDATE/MERGE)

- `ETL_Framework.DW_Developer`
- `OH`
- `Retail_Sales.SalesOrderHeader`
- `Retail_Sales_Enh.SalesOrderHeader`
- `SFMC`
- `oh`
- `stmt`

## Calls (EXEC)

- `ETL_Framework.DW_Developer`

## Code (first 80 lines)

```sql
CREATE PROCEDURE [Retail_Sales_Enh].[usp_Update_SalesOrderHeader]
AS

BEGIN
	
	DECLARE
            @String VARCHAR(5000),
            @DateValue DATETIME,
            @User VARCHAR(500),
			@DestinationDatabase VARCHAR(150),
			@DestinationSchema VARCHAR(150),
			@DestinationTable VARCHAR(150);
			      
    SET @String = 'Retail_Sales_Enh.usp_Update_SalesOrderHeader' ;
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

		--TRUNCATE TABLE [Retail_Sales_Enh].[SalesOrderHeader];

		DECLARE @MaxID BIGINT = (SELECT ISNULL(MAX(OrderKey),0) FROM [Retail_Sales_Enh].[SalesOrderHeader]);

		IF OBJECT_ID('tempdb..#OrderFulfillment') IS NOT NULL 
		DROP TABLE #OrderFulfillment;

		SELECT
			SourceOrderID
			, MerchSubTotal
			, DeliveryCharge
			, InstallationCharge
			, DeliveryChargeCalculated
			, RecStatus
			, DateChanged
			, DateCreated
		INTO #OrderFulfillment
		FROM [Retail_Sales].[SalesOrderFulfillment];

		IF OBJECT_ID('tempdb..#OrderItemCommissionInfo') IS NOT NULL 
		DROP TABLE #OrderItemCommissionInfo;

		SELECT *
		INTO #OrderItemCommissionInfo
		FROM [Retail_Sales].[SalesAssociateCommission]
		WHERE CommissionStatus = 'Written';

		IF OBJECT_ID('tempdb..#OrderComments') IS NOT NULL 
		DROP TABLE #OrderComments;

		SELECT 
			oc.RecordID AS SourceOrderID
			, oc.StaffID
		INTO #OrderComments
		FROM [Centralized_Lakehouse].[Retail_Corporate].[OrderComments] oc
		WHERE oc.RecordID IN
		(
			SELECT DataSetKeyValue
			FROM [MasterData_Retail_Ent].[DataSetKey]
		)		
		AND oc.Comment LIKE 'Delivery charge override%';

		UPDATE [Retail_Sales].[SalesOrderHeader]
		SET MerchSubTotal = 0
			, InstallationCharge = 0
			, DeliveryCharge = 0
			, TotalAdditionalTaxAmount = 0
			, TotalStateTaxAmount = 0
-- … [1143 more lines truncated, full body in data/06-procs-raw.json] --
```

---
