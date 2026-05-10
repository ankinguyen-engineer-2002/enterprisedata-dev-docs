# 🔴 Critical & High Risks (5)

[← Risks](README.md) · [← Root](../../README.md)

These need immediate attention.

## C1: 🔴 Critical

**Category:** Security
**Target:** `MetaData-Pull notebook`

**Issue:** Plaintext SP secret `<REDACTED-rotate-pending>` in `MetaData-Pull` cell 1 (AshleyBI app, tenant `5a9d9cfd-...`)

**Action:** Rotate immediately. Cells 2/3 use Key Vault correctly; delete cell 1

---

## C2: 🔴 High

**Category:** Security
**Target:** `permissions`

**Issue:** `AshleyBIApplicationProd` SPN holds Admin on Dev workspace

**Action:** Remove or downgrade to Contributor

---

## C3: 🔴 High

**Category:** Architecture
**Target:** `Quality_Warehouse`

**Issue:** `Quality_Warehouse` (PROD tier) is empty (0 tables/procs)

**Action:** Either build or remove

---

## C25: 🔴 High

**Category:** Architecture
**Target:** `Centralized_Lakehouse`

**Issue:** 5.92B rows in Centralized_Lakehouse are shortcut-backed (not real DEV data)

**Action:** Document, ensure team doesn't write back

---

## C28: 🔴 High

**Category:** Security
**Target:** `RadarSync_Test`

**Issue:** `RadarSync_Test` mounts entire trusted+raw ADLS zones — broad scope

**Action:** Restrict scope or audit access

---
