# Inaccessible References

[← Cross-Workspace](README.md) · [← Root](../../README.md)

Items referenced from this workspace's notebooks/code that I couldn't read directly.

## Workspaces I got 403 on

- **`13eefa5e-506c-4c07-a500-282bbffddf7d`** — referenced as `WORKSPACE_ID_FILTER` in `ShortCut-pulls_V1.py`. 403 Forbidden when listing items.
- **`sg_DHalama`** (by name only) — target of `nb-sync-uc-fabric-onelake` (writes `Marketing_Lakehouse` there).

## Lakehouses referenced by GUID but not in any workspace I can list

| Inferred name | GUID | Used by |
|---|---|---|
| CostAccounting_Lakehouse | `e4f5f630-4de5-44ba-9213-1dedf08e69e7` | Convert/Copy/Create_External notebooks (3) |
| Wholesale_Lakehouse | `3f8d8040-f40e-49bd-af24-bf81e8b89994` | Vers 5 / Vers 5 Copy default LH |
| Retail_Lakehouse | `cfb3e33f-011e-4766-8722-8913aa655e89` | RunZetaTestQuery default LH |
| Enterprise_Lakehouse | `a41163dc-182c-402a-b97b-08b93351c9b5` | TableDictionary_RJ + Vers5new |
| (stale) | `75f83a27-e35e-42df-8b4b-8ab281ab72c8` | Vers 5 control path — does not resolve anywhere |

These likely live in **personal-developer workspaces** I don't have access to.

---
