# 🕸️ Cross-Layer Dependency Graphs

[← Data Flow](README.md) · [← Root](../../README.md)

## A. Proc call graph (`EXEC` → `EXEC`)

Total EXEC edges detected: **234**.

```mermaid
graph TB
    Usp_Refresh_Retail_Wareho["Usp_Refresh_Retail_Warehouse"]
    ETL_Framework_DW_Develope["ETL_Framework.DW_Developer"]
    Usp_Refresh_Retail_Wareho --> ETL_Framework_DW_Develope
    usp_Update_CompanyDetails["usp_Update_CompanyDetails"]
    usp_Update_CompanyDetails --> ETL_Framework_DW_Develope
    usp_Update_EmploymentDeta["usp_Update_EmploymentDetails"]
    usp_Update_EmploymentDeta --> ETL_Framework_DW_Develope
    usp_Update_HREmployeeHist["usp_Update_HREmployeeHistory"]
    usp_Update_HREmployeeHist --> ETL_Framework_DW_Develope
    usp_Update_Jobs["usp_Update_Jobs"]
    usp_Update_Jobs --> ETL_Framework_DW_Develope
    usp_Update_LaborCategory["usp_Update_LaborCategory"]
    usp_Update_LaborCategory --> ETL_Framework_DW_Develope
    usp_Update_OrgLevel["usp_Update_OrgLevel"]
    usp_Update_OrgLevel --> ETL_Framework_DW_Develope
    usp_Update_PayCodes["usp_Update_PayCodes"]
    usp_Update_PayCodes --> ETL_Framework_DW_Develope
    usp_Update_PeopleRecords["usp_Update_PeopleRecords"]
    usp_Update_PeopleRecords --> ETL_Framework_DW_Develope
    usp_Update_PersonDetails["usp_Update_PersonDetails"]
    usp_Update_PersonDetails --> ETL_Framework_DW_Develope
    usp_Update_WorkRules["usp_Update_WorkRules"]
    usp_Update_WorkRules --> ETL_Framework_DW_Develope
    Usp_CreateTableFromParque["Usp_CreateTableFromParquet_Simple_N"]
    in["in"]
    Usp_CreateTableFromParque --> in
    this["this"]
    Usp_CreateTableFromParque --> this
    sys_sp_executesql["sys.sp_executesql"]
    Usp_CreateTableFromParque --> sys_sp_executesql
    Usp_CreateTableFromParque["Usp_CreateTableFromParquet_Straight"]
    Usp_CreateTableFromParque --> sys_sp_executesql
    Usp_CreateTableFromParque["Usp_CreateTableFromParquet_V1"]
    sp_rename["sp_rename"]
    Usp_CreateTableFromParque --> sp_rename
    Usp_CreateTableFromParque["Usp_CreateTableFromParquet_V2"]
    Usp_CreateTableFromParque --> sys_sp_executesql
    usp_GrantSchemaSecurity["usp_GrantSchemaSecurity"]
    them["them"]
    usp_GrantSchemaSecurity --> them
    usp_IncrementalTableLoad["usp_IncrementalTableLoad"]
    the["the"]
    usp_IncrementalTableLoad --> the
    DW_Developer_usp_DropWork["DW_Developer.usp_DropWorkTable"]
    usp_IncrementalTableLoad --> DW_Developer_usp_DropWork
    usp_IncrementalTableLoad_["usp_IncrementalTableLoad_Backup"]
    usp_IncrementalTableLoad_ --> the
    usp_IncrementalTableLoad_ --> DW_Developer_usp_DropWork
    usp_IncrementalTableLoad_["usp_IncrementalTableLoad_CDC"]
    usp_IncrementalTableLoad_ --> the
    usp_IncrementalTableLoad_ --> DW_Developer_usp_DropWork
    usp_RefreshCuratedTableFr["usp_RefreshCuratedTableFromView"]
    usp_RefreshCuratedTableFr --> sp_rename
    DW_Developer_usp_UpdateTa["DW_Developer.usp_UpdateTableDiction"]
    usp_RefreshCuratedTableFr --> DW_Developer_usp_UpdateTa
    usp_RefreshCuratedTableFr --> DW_Developer_usp_DropWork
    usp_RefreshCuratedTableFr["usp_RefreshCuratedTableFromView2"]
    usp_RefreshCuratedTableFr --> sp_rename
    usp_RefreshCuratedTableFr --> DW_Developer_usp_DropWork
    usp_SCD2_TableLoad["usp_SCD2_TableLoad"]
    usp_SCD2_TableLoad --> DW_Developer_usp_DropWork
    Usp_TableFromParquet_Copy["Usp_TableFromParquet_CopyInto_Trunc"]
    Usp_TableFromParquet_Copy --> the
    Usp_TableFromParquet_Open["Usp_TableFromParquet_OpenRowADF"]
    Usp_TableFromParquet_Open --> the
    Usp_TableFromParquet_Open["Usp_TableFromParquet_OpenRowADF_Tru"]
    Usp_TableFromParquet_Open --> the
    Usp_TableFromParquet_Open["Usp_TableFromParquet_OpenRowADF2"]
    Usp_TableFromParquet_Open --> the
    Usp_TableFromParquet_Open["Usp_TableFromParquet_OpenRowADFExte"]
    Usp_TableFromParquet_Open --> the
    usp_Refresh_EnterpriseAPI["usp_Refresh_EnterpriseAPIReprocesse"]
    usp_Refresh_EnterpriseAPI --> ETL_Framework_DW_Develope
    usp_refresh_shopperTrakTa["usp_refresh_shopperTrakTables"]
    usp_refresh_shopperTrakTa --> ETL_Framework_DW_Develope
    usp_Refresh_DataSetKey["usp_Refresh_DataSetKey"]
    MasterData_Retail_Ent_usp["MasterData_Retail_Ent.usp_Refresh_D"]
    usp_Refresh_DataSetKey --> MasterData_Retail_Ent_usp
    Usp_Refresh_EmployeeHisto["Usp_Refresh_EmployeeHistory"]
    MasterData_HR_UKG_Enh_usp["MasterData_HR_UKG_Enh.usp_Update_Pe"]
    Usp_Refresh_EmployeeHisto --> MasterData_HR_UKG_Enh_usp
    MasterData_HR_UKG_Enh_usp["MasterData_HR_UKG_Enh.usp_Update_HR"]
    Usp_Refresh_EmployeeHisto --> MasterData_HR_UKG_Enh_usp
    Usp_Refresh_MasterData_En["Usp_Refresh_MasterData_Ent"]
    Usp_Refresh_MasterData_En --> ETL_Framework_DW_Develope
    Usp_Refresh_MasterData_HR["Usp_Refresh_MasterData_HR_UKG_Enh"]
    MasterData_HR_UKG_Enh_usp["MasterData_HR_UKG_Enh.usp_Update_Or"]
    Usp_Refresh_MasterData_HR --> MasterData_HR_UKG_Enh_usp
    MasterData_HR_UKG_Enh_usp["MasterData_HR_UKG_Enh.usp_Update_Co"]
    Usp_Refresh_MasterData_HR --> MasterData_HR_UKG_Enh_usp
    MasterData_HR_UKG_Enh_usp["MasterData_HR_UKG_Enh.usp_Update_Pa"]
    Usp_Refresh_MasterData_HR --> MasterData_HR_UKG_Enh_usp
    MasterData_HR_UKG_Enh_usp["MasterData_HR_UKG_Enh.usp_Update_Jo"]
    Usp_Refresh_MasterData_HR --> MasterData_HR_UKG_Enh_usp
    MasterData_HR_UKG_Enh_usp["MasterData_HR_UKG_Enh.usp_Update_La"]
    Usp_Refresh_MasterData_HR --> MasterData_HR_UKG_Enh_usp
    MasterData_HR_UKG_Enh_usp["MasterData_HR_UKG_Enh.usp_Update_Pe"]
    Usp_Refresh_MasterData_HR --> MasterData_HR_UKG_Enh_usp
    MasterData_HR_UKG_Enh_usp["MasterData_HR_UKG_Enh.usp_Update_Wo"]
    Usp_Refresh_MasterData_HR --> MasterData_HR_UKG_Enh_usp
    MasterData_HR_UKG_Enh_usp["MasterData_HR_UKG_Enh.usp_Update_Em"]
    Usp_Refresh_MasterData_HR --> MasterData_HR_UKG_Enh_usp
    Usp_Refresh_MasterData_HR --> ETL_Framework_DW_Develope
```

## B. Pipeline → Proc invocations

Total pipeline→proc edges: **0**.

_(no pipeline→proc invocations detected via Script activities)_

## C. Top-30 hottest tables (read+write graph)

```mermaid
graph LR
    ETL_Framework_DW_Develope["ETL_Framework.DW_Developer"]:::tbl
    usp_Refresh_Buckets_([usp_Refresh_Buckets_Updat]) --> ETL_Framework_DW_Develope
    usp_Update_CreditRev([usp_Update_CreditReview]) --> ETL_Framework_DW_Develope
    usp_ProtectionPlanTr([usp_ProtectionPlanTrans_D]) --> ETL_Framework_DW_Develope
    usp_RefreshTimeSheet([usp_RefreshTimeSheetSumma]) --> ETL_Framework_DW_Develope
    Usp_Refresh_StoreTra([Usp_Refresh_StoreTraffic]) --> ETL_Framework_DW_Develope
    ETL_Framework_DW_Develope --> usp_Refresh_Buckets_([usp_Refresh_Buckets_Updat])
    ETL_Framework_DW_Develope --> usp_Update_CreditRev([usp_Update_CreditReview])
    ETL_Framework_DW_Develope --> usp_ProtectionPlanTr([usp_ProtectionPlanTrans_D])
    ETL_Framework_DW_Develope --> usp_RefreshTimeSheet([usp_RefreshTimeSheetSumma])
    ETL_Framework_DW_Develope --> Usp_Refresh_StoreTra([Usp_Refresh_StoreTraffic])
    Source_Data_Retail_Corpor["Source_Data.Retail_Corporate"]:::tbl
    Source_Data_Retail_Corpor --> usp_InventoryDetail([usp_InventoryDetail])
    Source_Data_Retail_Corpor --> usp_ProtectionPlanTr([usp_ProtectionPlanTrans_I])
    Source_Data_Retail_Corpor --> usp_PieceInventory_I([usp_PieceInventory_InvSub])
    Source_Data_Retail_Corpor --> usp_Update_CreditRev([usp_Update_CreditReview])
    Source_Data_Retail_Corpor --> usp_Full_Refresh_Sal([usp_Full_Refresh_SalesOrd])
    Centralized_Lakehouse_Ret["Centralized_Lakehouse.Retail_C"]:::tbl
    Centralized_Lakehouse_Ret --> usp_Refresh_BucketGe([usp_Refresh_BucketGetInve])
    Centralized_Lakehouse_Ret --> usp_Refresh_Buckets_([usp_Refresh_Buckets_Updat])
    Centralized_Lakehouse_Ret --> usp_Refresh_DataSetK([usp_Refresh_DataSetKey])
    Centralized_Lakehouse_Ret --> proc_GSCDemand_Alloc([proc_GSCDemand_Allocate_B])
    Centralized_Lakehouse_Ret --> usp_OrderHist_Paymen([usp_OrderHist_Payments])
    DW_Developer_TableDiction["DW_Developer.TableDictionary"]:::tbl
    usp_UpdateTableDicti([usp_UpdateTableDictionary]) --> DW_Developer_TableDiction
    usp_RefreshCuratedTa([usp_RefreshCuratedTableFr]) --> DW_Developer_TableDiction
    usp_UpdateCuratedTab([usp_UpdateCuratedTableFro]) --> DW_Developer_TableDiction
    Usp_CreateTableFromP([Usp_CreateTableFromParque]) --> DW_Developer_TableDiction
    usp_Audit_Fabric_Tab([usp_Audit_Fabric_Tables]) --> DW_Developer_TableDiction
    DW_Developer_TableDiction --> usp_UpdateTableDicti([usp_UpdateTableDictionary])
    DW_Developer_TableDiction --> usp_RefreshCuratedTa([usp_RefreshCuratedTableFr])
    DW_Developer_TableDiction --> usp_UpdateTableDicti([usp_UpdateTableDictionary])
    DW_Developer_TableDiction --> usp_UpdateCuratedTab([usp_UpdateCuratedTableFro])
    DW_Developer_TableDiction --> usp_DataWarehouseSLA([usp_DataWarehouseSLAAlert])
    Source_Data_Retail_Extern["Source_Data.Retail_External"]:::tbl
    usp_GenerateEmailHTM([usp_GenerateEmailHTML_Dim]) --> Source_Data_Retail_Extern
    usp_GenerateEmailHTM([usp_GenerateEmailHTML_Dim]) --> Source_Data_Retail_Extern
    Source_Data_Retail_Extern --> usp_Update_CreditRev([usp_Update_CreditReview])
    Source_Data_Retail_Extern --> usp_Full_Refresh_Sal([usp_Full_Refresh_SalesOrd])
    Source_Data_Retail_Extern --> usp_GenerateEmailHTM([usp_GenerateEmailHTML_Dim])
    Source_Data_Retail_Extern --> usp_PieceInventory_S([usp_PieceInventory_Surplu])
    Source_Data_Retail_Extern --> usp_Update_StoreTraf([usp_Update_StoreTraffic])
    Retail_OOM_Wrk_PieceInven["Retail_OOM_Wrk.PieceInventory"]:::tbl
    usp_PieceInventory_U([usp_PieceInventory_Update]) --> Retail_OOM_Wrk_PieceInven
    usp_PieceInventory_I([usp_PieceInventory_Intern]) --> Retail_OOM_Wrk_PieceInven
    usp_PieceInventory_U([usp_PieceInventory_Update]) --> Retail_OOM_Wrk_PieceInven
    usp_PieceInventory_I([usp_PieceInventory_Insert]) --> Retail_OOM_Wrk_PieceInven
    usp_PieceInventory_O([usp_PieceInventory_OrderS]) --> Retail_OOM_Wrk_PieceInven
    Retail_OOM_Wrk_PieceInven --> usp_InventoryDetail([usp_InventoryDetail])
    Retail_OOM_Wrk_PieceInven --> usp_InventorySummary([usp_InventorySummary_Inse])
    Retail_OOM_Wrk_PieceInven --> usp_PieceInventory_I([usp_PieceInventory_InvSub])
    Retail_OOM_Wrk_PieceInven --> usp_PieceInventoryTo([usp_PieceInventoryToDART_])
    Retail_OOM_Wrk_PieceInven --> usp_PieceHist_Insert([usp_PieceHist_Insert001])
    DW_Developer_fn_GetDate["DW_Developer.fn_GetDate"]:::tbl
    DW_Developer_fn_GetDate --> usp_UpdateTableDicti([usp_UpdateTableDictionary])
    DW_Developer_fn_GetDate --> usp_RefreshCuratedTa([usp_RefreshCuratedTableFr])
    DW_Developer_fn_GetDate --> usp_RefreshCuratedTa([usp_RefreshCuratedTableFr])
    DW_Developer_fn_GetDate --> usp_DataWarehouseSLA([usp_DataWarehouseSLAAlert])
    DW_Developer_fn_GetDate --> usp_UpdateCuratedTab([usp_UpdateCuratedTableFro])
    Centralized_Lakehouse_Ret["Centralized_Lakehouse.Retail_E"]:::tbl
    Centralized_Lakehouse_Ret --> usp_Refresh_Buckets_([usp_Refresh_Buckets_Updat])
    Centralized_Lakehouse_Ret --> usp_Update_GSCDemand([usp_Update_GSCDemand])
    Centralized_Lakehouse_Ret --> usp_Update_BucketIns([usp_Update_BucketInsert_O])
    Centralized_Lakehouse_Ret --> usp_OrderHist_Paymen([usp_OrderHist_Payments])
    Centralized_Lakehouse_Ret --> usp_GSCLocationProdu([usp_GSCLocationProducts_I])
    Source_Data_Retail_Miniap["Source_Data.Retail_Miniapps"]:::tbl
    Source_Data_Retail_Miniap --> usp_Refresh_DTRContr([usp_Refresh_DTRContractor])
    Source_Data_Retail_Miniap --> usp_InventorySummary([usp_InventorySummary_Upda])
    Source_Data_Retail_Miniap --> Usp_Refresh_Override([Usp_Refresh_OverrideTraff])
    Source_Data_Retail_Miniap --> usp_RefreshTimeSheet([usp_RefreshTimeSheetSumma])
    Source_Data_Retail_Miniap --> Usp_Refresh_RealTime([Usp_Refresh_RealTimeTraff])
    Retail_Sales_Enh_SalesOrd["Retail_Sales_Enh.SalesOrderHea"]:::tbl
    usp_Full_Refresh_Sal([usp_Full_Refresh_SalesOrd]) --> Retail_Sales_Enh_SalesOrd
    usp_Update_SalesOrde([usp_Update_SalesOrderHead]) --> Retail_Sales_Enh_SalesOrd
    Retail_Sales_Enh_SalesOrd --> usp_SalesOrderHist_P([usp_SalesOrderHist_Paymen])
    Retail_Sales_Enh_SalesOrd --> usp_Full_Refresh_Sal([usp_Full_Refresh_SalesOrd])
    Retail_Sales_Enh_SalesOrd --> usp_Update_SalesOrde([usp_Update_SalesOrderHead])
    Retail_Sales_Enh_SalesOrd --> usp_OrderSplit_Proce([usp_OrderSplit_ProcessOrd])
    Retail_Sales_Enh_SalesOrd --> usp_SalesOrderHistPr([usp_SalesOrderHistProcess])
    DW_Developer_AuditLog["DW_Developer.AuditLog"]:::tbl
    usp_UpdateTableDicti([usp_UpdateTableDictionary]) --> DW_Developer_AuditLog
    usp_RefreshCuratedTa([usp_RefreshCuratedTableFr]) --> DW_Developer_AuditLog
    usp_RefreshCuratedTa([usp_RefreshCuratedTableFr]) --> DW_Developer_AuditLog
    usp_UpdateCuratedTab([usp_UpdateCuratedTableFro]) --> DW_Developer_AuditLog
    Usp_CreateTableFromP([Usp_CreateTableFromParque]) --> DW_Developer_AuditLog
    DW_Developer_TableDiction["DW_Developer.TableDictionary_U"]:::tbl
    usp_RefreshCuratedTa([usp_RefreshCuratedTableFr]) --> DW_Developer_TableDiction
    usp_RefreshCuratedTa([usp_RefreshCuratedTableFr]) --> DW_Developer_TableDiction
    usp_UpdateCuratedTab([usp_UpdateCuratedTableFro]) --> DW_Developer_TableDiction
    Usp_CreateTableFromP([Usp_CreateTableFromParque]) --> DW_Developer_TableDiction
    usp_IncrementalTable([usp_IncrementalTableLoad_]) --> DW_Developer_TableDiction
    DW_Developer_TableDiction --> usp_UpdateTableDicti([usp_UpdateTableDictionary])
    Retail_Sales_Enh_GSCDeman["Retail_Sales_Enh.GSCDemand"]:::tbl
    usp_Update_GSCDemand([usp_Update_GSCDemand]) --> Retail_Sales_Enh_GSCDeman
    usp_Insert_GSCDemand([usp_Insert_GSCDemand]) --> Retail_Sales_Enh_GSCDeman
    Retail_Sales_Enh_GSCDeman --> usp_Refresh_SmartPar([usp_Refresh_SmartPartials])
    Retail_Sales_Enh_GSCDeman --> usp_Update_GSCDemand([usp_Update_GSCDemand])
    Retail_Sales_Enh_GSCDeman --> proc_GSCDemand_Alloc([proc_GSCDemand_Allocate_B])
    Retail_Sales_Enh_GSCDeman --> usp_Update_GSCPeriod([usp_Update_GSCPeriodDataS])
    Retail_Sales_Enh_GSCDeman --> usp_Insert_GSCDemand([usp_Insert_GSCDemand])
    MasterData_HR_UKG_Enh_Tim["MasterData_HR_UKG_Enh.TimeShee"]:::tbl
    usp_RefreshTimeSheet([usp_RefreshTimeSheetSumma]) --> MasterData_HR_UKG_Enh_Tim
    usp_RefreshTimeSheet([usp_RefreshTimeSheetSumma]) --> MasterData_HR_UKG_Enh_Tim
    usp_Update_TimeSheet([usp_Update_TimeSheetSumma]) --> MasterData_HR_UKG_Enh_Tim
    usp_RefreshTimeSheet([usp_RefreshTimeSheetSumma]) --> MasterData_HR_UKG_Enh_Tim
    MasterData_HR_UKG_Enh_Tim --> usp_RefreshTimeSheet([usp_RefreshTimeSheetSumma])
    MasterData_HR_UKG_Enh_Tim --> usp_RefreshTimeSheet([usp_RefreshTimeSheetSumma])
    MasterData_HR_UKG_Enh_Tim --> usp_RefreshTimeSheet([usp_RefreshTimeSheetSumma])
    MasterData_HR_UKG_Enh_Tim --> usp_Update_TimeSheet([usp_Update_TimeSheetSumma])
    MasterData_HR_UKG_Enh_Tim --> usp_RefreshTimeSheet([usp_RefreshTimeSheetSumma])
    Retail_Sales_Enh_GSCLocat["Retail_Sales_Enh.GSCLocationPr"]:::tbl
    usp_GSCLocationProdu([usp_GSCLocationProducts_I]) --> Retail_Sales_Enh_GSCLocat
    Retail_Sales_Enh_GSCLocat --> usp_Refresh_SmartPar([usp_Refresh_SmartPartials])
    Retail_Sales_Enh_GSCLocat --> usp_Update_GSCDemand([usp_Update_GSCDemand])
    Retail_Sales_Enh_GSCLocat --> usp_GSCLocationProdu([usp_GSCLocationProducts_I])
    Retail_Sales_Enh_GSCLocat --> usp_Update_GSCPeriod([usp_Update_GSCPeriodDataS])
    Retail_Sales_Enh_GSCLocat --> usp_GSCLocationProdu([usp_GSCLocationProducts_U])
    Source_Data_MasterData_HR["Source_Data.MasterData_HR_UKG_"]:::tbl
    Source_Data_MasterData_HR --> usp_Update_PayCodes([usp_Update_PayCodes])
    Source_Data_MasterData_HR --> usp_Update_Jobs([usp_Update_Jobs])
    Source_Data_MasterData_HR --> usp_Update_PersonDet([usp_Update_PersonDetails])
    Source_Data_MasterData_HR --> usp_Update_OrgLevel([usp_Update_OrgLevel])
    Source_Data_MasterData_HR --> usp_Update_LaborCate([usp_Update_LaborCategory])
    MasterData_Retail_Ent_Sto["MasterData_Retail_Ent.StoreLoc"]:::tbl
    MasterData_Retail_Ent_Sto --> usp_Update_Scoreboar([usp_Update_ScoreboardActi])
    MasterData_Retail_Ent_Sto --> usp_Full_Refresh_Sal([usp_Full_Refresh_SalesOrd])
    MasterData_Retail_Ent_Sto --> usp_Update_Scoreboar([usp_Update_ScoreboardActi])
    MasterData_Retail_Ent_Sto --> usp_Update_SalesOrde([usp_Update_SalesOrderHead])
    MasterData_Retail_Ent_Sto --> Usp_Refresh_RealTime([Usp_Refresh_RealTimeTraff])
    Retail_Sales_Wrk_OrderSpl["Retail_Sales_Wrk.OrderSplit"]:::tbl
    usp_OrderSplit([usp_OrderSplit]) --> Retail_Sales_Wrk_OrderSpl
    usp_SalesOrderHistPr([usp_SalesOrderHistProcess]) --> Retail_Sales_Wrk_OrderSpl
    usp_OrderSplit_OI([usp_OrderSplit_OI]) --> Retail_Sales_Wrk_OrderSpl
    Retail_Sales_Wrk_OrderSpl --> usp_OrderSplit_OI([usp_OrderSplit_OI])
    Retail_Sales_Wrk_OrderSpl --> usp_OrderSplit_Proce([usp_OrderSplit_ProcessOrd])
    Retail_Sales_Wrk_OrderSpl --> usp_OrderSplit_Proce([usp_OrderSplit_ProcessOrd])
    Retail_Sales_Wrk_OrderSpl --> usp_SalesOrderHistPr([usp_SalesOrderHistProcess])
    Retail_Sales_Wrk_OrderSpl --> usp_SalesOrderHist_P([usp_SalesOrderHist_Proces])
    Retail_Sales_Enh_Protecti["Retail_Sales_Enh.ProtectionPla"]:::tbl
    usp_ProtectionPlanTr([usp_ProtectionPlanTrans_D]) --> Retail_Sales_Enh_Protecti
    usp_ProtectionPlanSa([usp_ProtectionPlanSalesTr]) --> Retail_Sales_Enh_Protecti
    usp_ProtectionPlanTr([usp_ProtectionPlanTrans_B]) --> Retail_Sales_Enh_Protecti
    Retail_Sales_Enh_Protecti --> usp_ProtectionPlanTr([usp_ProtectionPlanTrans_I])
    Retail_Sales_Enh_Protecti --> usp_ProtectionPlanTr([usp_ProtectionPlanTrans_D])
    Retail_Sales_Enh_Protecti --> usp_ProtectionPlanSa([usp_ProtectionPlanSalesTr])
    Retail_Sales_Enh_Protecti --> usp_ProtectionPlanTr([usp_ProtectionPlanTrans])
    Retail_Sales_Enh_Protecti --> usp_ProtectionPlanTr([usp_ProtectionPlanTrans_B])
    Retail_Warehouse_Retail_S["Retail_Warehouse.Retail_Sales_"]:::tbl
    usp_Refresh_BucketGe([usp_Refresh_BucketGetInve]) --> Retail_Warehouse_Retail_S
    usp_Refresh_Buckets_([usp_Refresh_Buckets_Updat]) --> Retail_Warehouse_Retail_S
    usp_Refresh_BucketOr([usp_Refresh_BucketOrderIt]) --> Retail_Warehouse_Retail_S
    usp_Refresh_BucketPO([usp_Refresh_BucketPOI]) --> Retail_Warehouse_Retail_S
    usp_Refresh_Buckets_([usp_Refresh_Buckets_Updat]) --> Retail_Warehouse_Retail_S
    Retail_Warehouse_Retail_S --> usp_Refresh_Buckets_([usp_Refresh_Buckets_Updat])
    Retail_Warehouse_Retail_S --> usp_Refresh_Buckets_([usp_Refresh_Buckets_Updat])
    Retail_Sales_Enh_SalesPer["Retail_Sales_Enh.SalesPersonUP"]:::tbl
    usp_Update_Salespers([usp_Update_SalespersonUPB]) --> Retail_Sales_Enh_SalesPer
    Retail_Sales_Enh_SalesPer --> usp_Update_Scoreboar([usp_Update_ScoreboardMana])
    Retail_Sales_Enh_SalesPer --> usp_Update_SalesPers([usp_Update_SalesPersonHou])
    Retail_Sales_Enh_SalesPer --> usp_Update_Scoreboar([usp_Update_ScoreboardActi])
    Retail_Sales_Enh_SalesPer --> usp_Update_Scoreboar([usp_Update_ScoreboardMana])
    Retail_Sales_Enh_SalesPer --> usp_Update_Scoreboar([usp_Update_ScoreboardActi])
    MasterData_HR_UKG_Enh_Pay["MasterData_HR_UKG_Enh.PayMatri"]:::tbl
    usp_Refresh_PayMatri([usp_Refresh_PayMatrix]) --> MasterData_HR_UKG_Enh_Pay
    usp_RefreshTimeSheet([usp_RefreshTimeSheetSumma]) --> MasterData_HR_UKG_Enh_Pay
    usp_RefreshPayMatrix([usp_RefreshPayMatrix]) --> MasterData_HR_UKG_Enh_Pay
    MasterData_HR_UKG_Enh_Pay --> usp_Refresh_PayMatri([usp_Refresh_PayMatrix])
    MasterData_HR_UKG_Enh_Pay --> usp_RefreshTimeSheet([usp_RefreshTimeSheetSumma])
    MasterData_HR_UKG_Enh_Pay --> usp_RefreshPayMatrix([usp_RefreshPayMatrix])
    MasterData_HR_UKG_Enh_Pay --> usp_Update_TimeSheet([usp_Update_TimeSheetSumma])
    Retail_Sales_Wrk_OrderHea["Retail_Sales_Wrk.OrderHeader"]:::tbl
    usp_SalesOrderHistPr([usp_SalesOrderHistProcess]) --> Retail_Sales_Wrk_OrderHea
    Retail_Sales_Wrk_OrderHea --> usp_SalesOrderHist_P([usp_SalesOrderHist_Paymen])
    Retail_Sales_Wrk_OrderHea --> usp_SalesOrderHist_I([usp_SalesOrderHist_Insert])
    Retail_Sales_Wrk_OrderHea --> usp_OrderSplit_Proce([usp_OrderSplit_ProcessOrd])
    Retail_Sales_Wrk_OrderHea --> usp_SalesOrderHistPr([usp_SalesOrderHistProcess])
    Retail_Sales_Wrk_OrderHea --> usp_SalesOrderHist_P([usp_SalesOrderHist_Proces])
    MasterData_Retail_Ent_Dat["MasterData_Retail_Ent.DataSetK"]:::tbl
    usp_Refresh_DataSetK([usp_Refresh_DataSetKey]) --> MasterData_Retail_Ent_Dat
    MasterData_Retail_Ent_Dat --> usp_OrderSplit([usp_OrderSplit])
    MasterData_Retail_Ent_Dat --> usp_OrderSplit_OI([usp_OrderSplit_OI])
    MasterData_Retail_Ent_Dat --> usp_OrderHist_Paymen([usp_OrderHist_Payments])
    MasterData_Retail_Ent_Dat --> usp_Update_SalesOrde([usp_Update_SalesOrderHead])
    MasterData_Retail_Ent_Dat --> usp_SalesOrderHistQu([usp_SalesOrderHistQueue])
    Retail_Sales_Enh_SalesOrd["Retail_Sales_Enh.SalesOrderLin"]:::tbl
    usp_Update_SalesOrde([usp_Update_SalesOrderLine]) --> Retail_Sales_Enh_SalesOrd
    Retail_Sales_Enh_SalesOrd --> usp_Full_Refresh_Sal([usp_Full_Refresh_SalesOrd])
    Retail_Sales_Enh_SalesOrd --> usp_Update_SalesOrde([usp_Update_SalesOrderHead])
    Retail_Sales_Enh_SalesOrd --> usp_Update_SalesOrde([usp_Update_SalesOrderLine])
    Retail_Sales_Enh_SalesOrd --> usp_Update_SalesOrde([usp_Update_SalesOrderLine])
    Retail_Sales_Enh_SalesOrd --> usp_Update_SalesOrde([usp_Update_SalesOrderLine])
    Retail_Sales_Enh_SalesOrd["Retail_Sales_Enh.SalesOrderLin"]:::tbl
    usp_Update_SalesOrde([usp_Update_SalesOrderLine]) --> Retail_Sales_Enh_SalesOrd
    Retail_Sales_Enh_SalesOrd --> usp_SalesOrderCloses([usp_SalesOrderCloses_Proc])
    Retail_Sales_Enh_SalesOrd --> usp_Full_Refresh_Sal([usp_Full_Refresh_SalesOrd])
    Retail_Sales_Enh_SalesOrd --> usp_Update_SalesOrde([usp_Update_SalesOrderLine])
    Retail_Sales_Enh_SalesOrd --> usp_SalesOrderCloses([usp_SalesOrderCloses])
    Retail_Sales_Enh_SalesOrd --> usp_SalesOrderCloses([usp_SalesOrderCloses_Proc])
    Centralized_Lakehouse_Mas["Centralized_Lakehouse.MasterDa"]:::tbl
    Centralized_Lakehouse_Mas --> usp_Update_PayCodes([usp_Update_PayCodes])
    Centralized_Lakehouse_Mas --> usp_Update_Jobs([usp_Update_Jobs])
    Centralized_Lakehouse_Mas --> usp_Update_PersonDet([usp_Update_PersonDetails])
    Centralized_Lakehouse_Mas --> usp_Update_OrgLevel([usp_Update_OrgLevel])
    Centralized_Lakehouse_Mas --> usp_Update_LaborCate([usp_Update_LaborCategory])
    Retail_Sales_Wrk_SOrderHi["Retail_Sales_Wrk.SOrderHist"]:::tbl
    usp_SalesOrderHist_P([usp_SalesOrderHist_Paymen]) --> Retail_Sales_Wrk_SOrderHi
    usp_SalesOrderHistPr([usp_SalesOrderHistProcess]) --> Retail_Sales_Wrk_SOrderHi
    usp_SalesOrderHist_I([usp_SalesOrderHist_Insert]) --> Retail_Sales_Wrk_SOrderHi
    Retail_Sales_Wrk_SOrderHi --> usp_SalesOrderHist_P([usp_SalesOrderHist_Paymen])
    Retail_Sales_Wrk_SOrderHi --> usp_SalesOrderHistPr([usp_SalesOrderHistProcess])
    Retail_Sales_Wrk_SOrderHi --> usp_SalesOrderHist_I([usp_SalesOrderHist_Insert])
    Retail_Sales_Enh_OrderSpl["Retail_Sales_Enh.OrderSplit"]:::tbl
    usp_OrderSplit_Proce([usp_OrderSplit_ProcessOrd]) --> Retail_Sales_Enh_OrderSpl
    usp_OrderSplit_Proce([usp_OrderSplit_ProcessOrd]) --> Retail_Sales_Enh_OrderSpl
    Retail_Sales_Enh_OrderSpl --> usp_OrderSplit_Proce([usp_OrderSplit_ProcessOrd])
    Retail_Sales_Enh_OrderSpl --> usp_SalesOrderHist_P([usp_SalesOrderHist_Proces])
    Retail_Sales_Enh_OrderSpl --> usp_OrderSplit_Proce([usp_OrderSplit_ProcessOrd])
    Retail_Sales_Enh_SmartPar["Retail_Sales_Enh.SmartPartialB"]:::tbl
    usp_Update_BucketIns([usp_Update_BucketInsert_O]) --> Retail_Sales_Enh_SmartPar
    usp_Update_BucketIns([usp_Update_BucketInsert]) --> Retail_Sales_Enh_SmartPar
    Retail_Sales_Enh_SmartPar --> usp_GSCLocationProdu([usp_GSCLocationProducts_I])
    Retail_Sales_Enh_SmartPar --> usp_Update_BucketIns([usp_Update_BucketInsert_O])
    Retail_Sales_Enh_SmartPar --> usp_Update_BucketIns([usp_Update_BucketInsert])
    classDef tbl fill:#cbd5e1,stroke:#475569;
```

---

**Per-table detail:** [Table lineage pages](tables/README.md) — top 50 most-referenced tables.
