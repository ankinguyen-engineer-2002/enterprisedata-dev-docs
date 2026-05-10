# 🔗 06 — Cross-Workspace Dependencies

[← Root](../../README.md)

## Map

![Cross-WS](../../images/06-cross-ws.svg)

```mermaid
flowchart LR
    classDef ext fill:#fed,stroke:#c93;
    classDef prod fill:#fdd,stroke:#c33;
    classDef unknown fill:#fcf,stroke:#93c;

    subgraph DEV[EnterpriseData-Dev<br/>5360a935]
        DEV_CL[Centralized_Lakehouse]
        DEV_AD[A_Developement LH]
        DEV_RST[RadarSync_Test LH]
        DEV_NB[Notebooks]
    end
    subgraph PROD[PROD WS EnterpriseData<br/>ce4e6503<br/>14 WH + 1 LH]
        P_SD[(Source_Data WH<br/>d27b3ef9)]
        P_RW[(Retail_Warehouse WH<br/>d8bec39c)]
        P_OTH[+12 other items]
    end
    subgraph UNK[Unknown / inaccessible]
        U_LHS[CostAccounting_LH<br/>Wholesale_LH<br/>Retail_LH<br/>Enterprise_LH]
        U_WS1[WS 13eefa5e 403]
        U_WS2[sg_DHalama]
    end
    subgraph EXT[External Azure]
        ADLS[ashleydevlake.dfs.core.windows.net<br/>ADLS Gen2]
        ADF[ashleyv2datafactory<br/>RG IoT_Hub]
        EDW[(ASHLEY_EDW_DEV)]
        SYN[(Synapse Ashley_Edw)]
    end

    P_SD -- 12 shortcuts --> DEV_CL
    P_RW -- 6 shortcuts --> DEV_CL
    ADLS -- 7 shortcuts --> DEV_AD
    ADLS -- 2 broad mounts --> DEV_RST
    EDW --> DEV_NB
    SYN --> DEV_NB
    ADF -- mounted --> DEV_NB
    DEV_NB -.references.-> U_LHS
    DEV_NB -.target/source.-> U_WS1
    DEV_NB -.target.-> U_WS2

    class ADLS,ADF,EDW,SYN ext;
    class P_SD,P_RW,P_OTH prod;
    class U_LHS,U_WS1,U_WS2 unknown;
```

## Sub-pages

- [PROD dependencies](prod-dependencies.md) — 18 OneLake shortcuts + PROD inventory
- [ADLS storage](adls-storage.md) — 9 ADLS Gen2 shortcuts to `ashleydevlake`
- [Inaccessible references]
- [🔌 Connections (12)](connections.md) — data sources (SharePoint, SQL, Lakehouse)
(inaccessible-refs.md) — workspaces and items I couldn't read

## Summary

| Category | Count | Detail |
|---|---|---|
| OneLake shortcuts within DEV (Fabric-internal) | 385 | Internal table-to-files mapping |
| OneLake shortcuts to PROD WS | **18** | All to `ce4e6503-...` Source_Data + Retail_Warehouse |
| ADLS Gen2 shortcuts | **9** | All to `ashleydevlake.dfs.core.windows.net` |
| Inaccessible workspaces | 2 | WS `13eefa5e-...` (403), WS `sg_DHalama` (by name) |
| Unresolvable lakehouses | 4 + 1 stale | CostAccounting_LH, Wholesale_LH, Retail_LH, Enterprise_LH, stale 75f83a27 |

---
