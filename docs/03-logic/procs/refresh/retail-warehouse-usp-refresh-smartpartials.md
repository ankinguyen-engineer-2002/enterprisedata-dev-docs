# `usp_Refresh_SmartPartials`

_Schema: `Retail_Sales_Enh` · Warehouse: `Retail_Warehouse` · Family: `refresh`_

_Modified: 2026-04-27 06:52:01.943000 · Code size: 16,065 chars_

[← Procs](../README.md) · [← Logic](../../README.md) · [← Root](../../../../README.md)

## What it does

Reads from 12 sources and writes to 2 sinks. ⚠️ Drops tables (destructive).

## Parameters

_(none — runs with no parameters)_

## Inputs (FROM/JOIN)

- `AggregatedProducts`
- `Centralized_Lakehouse.Retail_Corporate`
- `Centralized_Lakehouse.Retail_External`
- `Centralized_Lakehouse.Retail_Miniapps`
- `DistinctProducts`
- `Retail_Sales_Enh.GSCDemand`
- `Retail_Sales_Enh.GSCLocationProducts`
- `Retail_Sales_Enh.SmartPartials`
- `Retail_Sales_Enh.SmartPartialsFullyReservedPcs`
- `dbo.wrk_SmartPartials_test`
- `storis.Product`
- `storis.ProductType`

## Outputs (INSERT/UPDATE/MERGE)

- `Retail_Sales_Enh.SmartPartials`
- `Retail_Sales_Enh.SmartPartialsFullyReservedPcs`

## Calls (EXEC)

_(none)_

## Code (first 80 lines)

```sql
CREATE           PROCEDURE [Retail_Sales_Enh].[usp_Refresh_SmartPartials]
AS

BEGIN
	DECLARE @NumWeeksApart INT = 3;

	TRUNCATE TABLE [Retail_Sales_Enh].[SmartPartialsFullyReservedPcs];
	TRUNCATE TABLE [Retail_Sales_Enh].[SmartPartials];

	DROP TABLE IF EXISTS #PossibleOrders, #OrderFlflmntSeries, #BackOrderedOrders;
	DROP TABLE IF EXISTS #SeriesAcrossFflmnt, #FlmntsGreaterThanOne, #FlmntsGreaterThanOneFinal, #OneFlmnt;
	DROP TABLE IF EXISTS #FflmntCnt, #Flmnts, #Flmnts2, #Flmnts3;

	SELECT	gsc.OrderID,
			gsc.OrderFulfillmentID,
			p.VendorModelNbr ProductID,
			gsc.OrderDate,
			gsc.StoreID,
			gsc.ATPDate,
			tc.Description OrderType,
			gsc.TransDate FulfillmentDate,
			gsc.OrigTransDate OrigFulfillmentDate,
			gsc.DeliveryTypeID FulfillmentMethod,
			gsc.DeliveryStatus FulfillmentStatus,
			lp.LocationID FulfillmentStoreID,
			LEFT(p.VendorModelNbr, 4) SeriesID,
			p.ProductTypeID,
			SUM(gsc.Qty * gsc.UnitSellPrice) MerchandiseTotalAudit,
			SUM((gsc.QtyComtd + gsc.QtyFromOH) * gsc.UnitSellPrice) MerchandiseTotalQtyAvailable,
			0 AS IsPossibleSeries,
			SUM(gsc.QtyComtd * gsc.UnitSellPrice) MerchandiseTotalPossible,
			gsc.FilledStatus,
			SUM(gsc.Qty) QtyOrdered,
			SUM(gsc.QtyComtd) QtyComtd,
			SUM(gsc.QtyFromOH) QtyFromOH,
			ROW_NUMBER() OVER (PARTITION BY gsc.OrderID ORDER BY gsc.TransDate) RowASCID,
			ROW_NUMBER() OVER (PARTITION BY gsc.OrderID ORDER BY gsc.TransDate DESC ) RowDESCID,
			gsc.ContactStatusCodeID ContactStatus,
			dcs.DeliveryContactCode DeliveryContactStatus,
			1 AS ind
		--INTO #Flmnts
		FROM [Retail_Sales_Enh].[GSCDemand] gsc
			INNER JOIN [Retail_Sales_Enh].[GSCLocationProducts] lp ON lp.LocProdID = gsc.LocProdID
			INNER JOIN [Centralized_Lakehouse].[Retail_Corporate].[TransCode] tc ON gsc.TransCodeID = tc.TransCodeID
			INNER JOIN [Centralized_Lakehouse].[Retail_Corporate].[Product] p ON lp.ProductID = p.ProductID
			INNER JOIN [Centralized_Lakehouse].[Retail_Miniapps].[WHGRP] grp ON lp.LocationID = grp.WHID
			INNER JOIN [Centralized_Lakehouse].[Retail_Corporate].[OrderFulfillment] flflmnt ON gsc.OrderFulfillmentID = flflmnt.OrderFulfillmentID
			LEFT JOIN  [Centralized_Lakehouse].[Retail_Corporate].[DeliveryContactStatus] dcs ON dcs.DeliveryContactStatusID = flflmnt.DeliveryContactStatusID
		WHERE gsc.TransCodeID IN (0, 1, 7)
			AND WHGP = 'DC'
		GROUP BY gsc.OrderID,
				gsc.OrderFulfillmentID,
				p.VendorModelNbr,
				gsc.OrderDate,
				gsc.StoreID,
				gsc.ATPDate,
				tc.Description,
				gsc.DeliveryTypeID,
				gsc.DeliveryStatus,
				gsc.TransDate,
				gsc.OrigTransDate,
				lp.LocationID,
				p.ProductTypeID,
				gsc.FilledStatus,
				gsc.ContactStatusCodeID,
				dcs.DeliveryContactCode;

	--------------------- ADD BY JANA ---------------------------------------------------------------------------------------
	DROP TABLE IF EXISTS #TRF, #CODE;

	SELECT	oi.OrderID TransferID,
			oi.ItemID AS TransferLineID,
			LEFT(oi.AutoTransOrderItemID, CHARINDEX('*', oi.AutoTransOrderItemID, 1) - 1) AS OrderID,
			RIGHT(oi.AutoTransOrderItemID, LEN(oi.AutoTransOrderItemID) - CHARINDEX('*', oi.AutoTransOrderItemID, 1)) ItemID,
			oi.QtyOrdered,
			oi.DlvyDate
		INTO #TRF
		FROM [Centralized_Lakehouse].[Retail_Corporate].[OrderItem] AS oi 
		WHERE oi.TransCodeID BETWEEN 60 AND 66
			AND oi.AutoTransOrderItemID IS NOT NULL
-- … [369 more lines truncated, full body in data/06-procs-raw.json] --
```

---
