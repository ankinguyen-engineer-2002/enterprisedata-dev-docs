# ⚙️ Stored Procedures — Detail Pages

[← Logic](../README.md) · [← Root](../../../README.md)

Per-proc narrative explanation. Top 60 procs (out of 192 total) get detail pages — selected by importance (ETL_Framework first, then by body size).

## By family

### `refresh` (114 procs)

- [`ETL_Framework.DW_Developer.usp_RefreshCuratedTableFromView`](refresh/etl-framework-usp-refreshcuratedtablefromview.md) — 6,316 chars
- [`ETL_Framework.DW_Developer.usp_RefreshCuratedTableFromView2`](refresh/etl-framework-usp-refreshcuratedtablefromview2.md) — 6,072 chars
- [`ETL_Framework.DW_Developer.usp_UpdateCuratedTableFromView_DateRange`](refresh/etl-framework-usp-updatecuratedtablefromview-daterange.md) — 4,954 chars
- [`ETL_Framework.DW_Developer.usp_UpdateTableDictionary_ModifiedDate`](refresh/etl-framework-usp-updatetabledictionary-modifieddate.md) — 3,827 chars
- [`ETL_Framework.DW_Developer.usp_UpdateTableDictionary_UpdateLog_RadarSync`](refresh/etl-framework-usp-updatetabledictionary-updatelog-radarsync.md) — 910 chars
- [`ETL_Framework.DW_Developer.usp_UpdateTableDictionaryModified`](refresh/etl-framework-usp-updatetabledictionarymodified.md) — 1,569 chars
- `Source_Data.Retail_Shoppertrack.usp_Refresh_EnterpriseAPIReprocessedLogs` — 3,474 chars _(no detail page)_
- `Source_Data.Retail_Shoppertrack.usp_refresh_shopperTrakTables` — 5,690 chars _(no detail page)_
- `Retail_Warehouse.dbo.usp_Refresh_DataSetKey` — 128 chars _(no detail page)_
- `Retail_Warehouse.dbo.Usp_Refresh_EmployeeHistory` — 199 chars _(no detail page)_
- `Retail_Warehouse.dbo.Usp_Refresh_MasterData_Ent` — 576 chars _(no detail page)_
- `Retail_Warehouse.dbo.Usp_Refresh_MasterData_HR_UKG_Enh` — 682 chars _(no detail page)_
- `Retail_Warehouse.dbo.Usp_Refresh_MasterData_Product` — 466 chars _(no detail page)_
- `Retail_Warehouse.dbo.Usp_Refresh_MasterData_Product_Enh` — 144 chars _(no detail page)_
- `Retail_Warehouse.dbo.Usp_Refresh_MasterData_Retail_Ent` — 760 chars _(no detail page)_
- `Retail_Warehouse.dbo.Usp_Refresh_Retail_Enh` — 886 chars _(no detail page)_
- `Retail_Warehouse.dbo.Usp_Refresh_Retail_NonCore_Enh` — 533 chars _(no detail page)_
- `Retail_Warehouse.dbo.Usp_Refresh_Retail_Sales` — 1,604 chars _(no detail page)_
- `Retail_Warehouse.dbo.Usp_Refresh_Retail_SalespersonUPBoardHistoryAGR` — 160 chars _(no detail page)_
- `Retail_Warehouse.dbo.Usp_Refresh_Retail_Scoreboard` — 392 chars _(no detail page)_
- `Retail_Warehouse.dbo.Usp_Refresh_Retail_Warehouse` — 2,651 chars _(no detail page)_
- `Retail_Warehouse.dbo.Usp_Refresh_Timesheet` — 501 chars _(no detail page)_
- `Retail_Warehouse.MasterData_HR_UKG_DSG_Enh.usp_Update_CompanyDetails` — 3,012 chars _(no detail page)_
- [`Retail_Warehouse.MasterData_HR_UKG_DSG_Enh.usp_Update_EmploymentDetails`](refresh/retail-warehouse-usp-update-employmentdetails.md) — 26,278 chars
- `Retail_Warehouse.MasterData_HR_UKG_DSG_Enh.usp_Update_HREmployeeHistory` — 3,864 chars _(no detail page)_
- `Retail_Warehouse.MasterData_HR_UKG_DSG_Enh.usp_Update_Jobs` — 3,054 chars _(no detail page)_
- `Retail_Warehouse.MasterData_HR_UKG_DSG_Enh.usp_Update_LaborCategory` — 2,890 chars _(no detail page)_
- `Retail_Warehouse.MasterData_HR_UKG_DSG_Enh.usp_Update_OrgLevel` — 3,302 chars _(no detail page)_
- `Retail_Warehouse.MasterData_HR_UKG_DSG_Enh.usp_Update_PayCodes` — 3,206 chars _(no detail page)_
- `Retail_Warehouse.MasterData_HR_UKG_DSG_Enh.usp_Update_PeopleRecords` — 7,798 chars _(no detail page)_
- _… and 84 more_

### `other` (48 procs)

- [`ETL_Framework.DW_Developer.usp_GrantSchemaSecurity`](other/etl-framework-usp-grantschemasecurity.md) — 3,042 chars
- [`ETL_Framework.DW_Developer.Usp_WriteTableToParquet`](other/etl-framework-usp-writetabletoparquet.md) — 4,190 chars
- [`Retail_Warehouse.Retail_OOM_Enh.usp_Buckets_Insert`](other/retail-warehouse-usp-buckets-insert.md) — 11,303 chars
- `Retail_Warehouse.Retail_OOM_Enh.usp_GLHist` — 9,419 chars _(no detail page)_
- [`Retail_Warehouse.Retail_OOM_Enh.usp_InvActivitySummary`](other/retail-warehouse-usp-invactivitysummary.md) — 13,808 chars
- [`Retail_Warehouse.Retail_OOM_Enh.usp_InvActivitySummary_Test`](other/retail-warehouse-usp-invactivitysummary-test.md) — 13,816 chars
- `Retail_Warehouse.Retail_OOM_Enh.usp_InventorySummary_Insert` — 5,432 chars _(no detail page)_
- `Retail_Warehouse.Retail_OOM_Enh.usp_OpenOrderSummary_Insert` — 8,851 chars _(no detail page)_
- [`Retail_Warehouse.Retail_OOM_Enh.usp_OpenOrderSummary_Insert_Detail`](other/retail-warehouse-usp-openordersummary-insert-detail.md) — 10,080 chars
- `Retail_Warehouse.Retail_OOM_Enh.usp_PieceHist_Insert001` — 7,000 chars _(no detail page)_
- `Retail_Warehouse.Retail_OOM_Enh.usp_PieceInventory_Process` — 4,748 chars _(no detail page)_
- `Retail_Warehouse.Retail_OOM_Wrk.usp_InventoryDetail` — 5,674 chars _(no detail page)_
- `Retail_Warehouse.Retail_OOM_Wrk.usp_PieceInventory_Insert001` — 5,548 chars _(no detail page)_
- `Retail_Warehouse.Retail_OOM_Wrk.usp_PieceInventory_InternalTransfers` — 3,005 chars _(no detail page)_
- `Retail_Warehouse.Retail_OOM_Wrk.usp_PieceInventory_InvSubBucketID` — 5,472 chars _(no detail page)_
- `Retail_Warehouse.Retail_OOM_Wrk.usp_PieceInventory_OISoftCommitted` — 6,198 chars _(no detail page)_
- `Retail_Warehouse.Retail_OOM_Wrk.usp_PieceInventory_OrderStoreBrandID` — 3,965 chars _(no detail page)_
- `Retail_Warehouse.Retail_OOM_Wrk.usp_PieceInventory_SoftCommitted` — 5,637 chars _(no detail page)_
- `Retail_Warehouse.Retail_OOM_Wrk.usp_PieceInventory_SoftCommitted_MFR_CWC_ASAP` — 5,565 chars _(no detail page)_
- `Retail_Warehouse.Retail_OOM_Wrk.usp_PieceInventory_Surplus` — 3,976 chars _(no detail page)_
- `Retail_Warehouse.Retail_OOM_Wrk.usp_PieceInventory_Surplus_ROS` — 4,931 chars _(no detail page)_
- `Retail_Warehouse.Retail_Sales_Enh.proc_GSCDemand_Allocate_Batched` — 6,164 chars _(no detail page)_
- `Retail_Warehouse.Retail_Sales_Enh.usp_GSCLocationProducts_Insert` — 5,063 chars _(no detail page)_
- `Retail_Warehouse.Retail_Sales_Enh.usp_GSCSupply_Insert` — 6,375 chars _(no detail page)_
- `Retail_Warehouse.Retail_Sales_Enh.usp_Insert_GSCDemand` — 9,793 chars _(no detail page)_
- `Retail_Warehouse.Retail_Sales_Enh.usp_ProtectionPlanSalesTrans_Insert` — 4,607 chars _(no detail page)_
- [`Retail_Warehouse.Retail_Sales_Enh.usp_ProtectionPlanTrans_Insert`](other/retail-warehouse-usp-protectionplantrans-insert.md) — 10,815 chars
- `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderCloses` — 3,906 chars _(no detail page)_
- `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderCloses_ProcessSUOrder_Bulk` — 6,413 chars _(no detail page)_
- `Retail_Warehouse.Retail_Sales_Enh.usp_SalesOrderCloses_ProcessSUOrders` — 3,931 chars _(no detail page)_
- _… and 18 more_

### `parquet-loaders` (12 procs)

- [`ETL_Framework.DW_Developer.Usp_CreateTableFromParquet`](parquet-loaders/etl-framework-usp-createtablefromparquet.md) — 4,732 chars
- [`ETL_Framework.DW_Developer.Usp_CreateTableFromParquet_1`](parquet-loaders/etl-framework-usp-createtablefromparquet-1.md) — 4,485 chars
- [`ETL_Framework.DW_Developer.Usp_CreateTableFromParquet_Simple_NoCursor`](parquet-loaders/etl-framework-usp-createtablefromparquet-simple-nocursor.md) — 7,763 chars
- [`ETL_Framework.DW_Developer.Usp_CreateTableFromParquet_Straight`](parquet-loaders/etl-framework-usp-createtablefromparquet-straight.md) — 6,260 chars
- [`ETL_Framework.DW_Developer.Usp_CreateTableFromParquet_V1`](parquet-loaders/etl-framework-usp-createtablefromparquet-v1.md) — 11,183 chars
- [`ETL_Framework.DW_Developer.Usp_CreateTableFromParquet_V2`](parquet-loaders/etl-framework-usp-createtablefromparquet-v2.md) — 7,915 chars
- [`ETL_Framework.DW_Developer.Usp_TableFromParquet_CopyInto_TruncateLoad`](parquet-loaders/etl-framework-usp-tablefromparquet-copyinto-truncateload.md) — 2,094 chars
- [`ETL_Framework.DW_Developer.Usp_TableFromParquet_OpenRowADF`](parquet-loaders/etl-framework-usp-tablefromparquet-openrowadf.md) — 951 chars
- [`ETL_Framework.DW_Developer.Usp_TableFromParquet_OpenRowADF_TruncateLoad`](parquet-loaders/etl-framework-usp-tablefromparquet-openrowadf-truncateload.md) — 1,858 chars
- [`ETL_Framework.DW_Developer.Usp_TableFromParquet_OpenRowADF2`](parquet-loaders/etl-framework-usp-tablefromparquet-openrowadf2.md) — 1,203 chars
- [`ETL_Framework.DW_Developer.Usp_TableFromParquet_OpenRowADFExternal`](parquet-loaders/etl-framework-usp-tablefromparquet-openrowadfexternal.md) — 1,033 chars
- [`ETL_Framework.DW_Developer.Usp_TableFromParquet_RowADF`](parquet-loaders/etl-framework-usp-tablefromparquet-rowadf.md) — 4,612 chars

### `audit` (3 procs)

- [`ETL_Framework.DW_Developer.usp_Audit_ADW_Tables`](audit/etl-framework-usp-audit-adw-tables.md) — 2,918 chars
- [`ETL_Framework.DW_Developer.usp_Audit_ADW_Tables_V1`](audit/etl-framework-usp-audit-adw-tables-v1.md) — 2,921 chars
- [`ETL_Framework.DW_Developer.usp_Audit_Fabric_Tables`](audit/etl-framework-usp-audit-fabric-tables.md) — 2,925 chars

### `email` (3 procs)

- [`ETL_Framework.DW_Developer.usp_GenerateEmailHTML_DimAggregateDifference`](email/etl-framework-usp-generateemailhtml-dimaggregatedifference.md) — 8,641 chars
- [`ETL_Framework.DW_Developer.usp_GenerateEmailHTML_DimCountDifference`](email/etl-framework-usp-generateemailhtml-dimcountdifference.md) — 7,760 chars
- [`ETL_Framework.Performance_Logs.usp_EmailQueue_MarkSent`](email/etl-framework-usp-emailqueue-marksent.md) — 331 chars

### `incremental` (3 procs)

- [`ETL_Framework.DW_Developer.usp_IncrementalTableLoad`](incremental/etl-framework-usp-incrementaltableload.md) — 34,475 chars
- [`ETL_Framework.DW_Developer.usp_IncrementalTableLoad_Backup`](incremental/etl-framework-usp-incrementaltableload-backup.md) — 23,617 chars
- [`ETL_Framework.DW_Developer.usp_IncrementalTableLoad_CDC`](incremental/etl-framework-usp-incrementaltableload-cdc.md) — 34,481 chars

### `alert` (2 procs)

- [`ETL_Framework.DW_Developer.usp_DataWarehouseDataFeedAlert_Fabric`](alert/etl-framework-usp-datawarehousedatafeedalert-fabric.md) — 7,229 chars
- [`ETL_Framework.DW_Developer.usp_DataWarehouseSLAAlert_Fabric`](alert/etl-framework-usp-datawarehouseslaalert-fabric.md) — 17,186 chars

### `cleanup` (2 procs)

- [`ETL_Framework.DW_Developer.usp_DropConstraints`](cleanup/etl-framework-usp-dropconstraints.md) — 10,624 chars
- [`ETL_Framework.DW_Developer.usp_DropWorkTable`](cleanup/etl-framework-usp-dropworktable.md) — 572 chars

### `load` (2 procs)

- `Retail_Warehouse.MasterData_Retail_Ent.usp_DynamicTableCreateAndLoadDirect` — 5,202 chars _(no detail page)_
- `Retail_Warehouse.Retail_Sales_Wrk.usp_SUOrder_LoadQueue_GetOrderID` — 2,071 chars _(no detail page)_

### `scd2` (1 procs)

- [`ETL_Framework.DW_Developer.usp_SCD2_TableLoad`](scd2/etl-framework-usp-scd2-tableload.md) — 18,855 chars

### `snapshot` (1 procs)

- [`ETL_Framework.DW_Developer.Usp_SnapshotLoad`](snapshot/etl-framework-usp-snapshotload.md) — 3,963 chars

### `history-log` (1 procs)

- `Retail_Warehouse.Retail_Traffic.usp_Load_EnterpriseActualTraffic_FromHistory` — 2,195 chars _(no detail page)_

---
