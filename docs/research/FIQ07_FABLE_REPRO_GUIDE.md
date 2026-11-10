# FIQ-07 F1/F2 v1.0.0 fix — original-module synthetic verification

Owner-adopted decision: [FIQ-07 issue #10](https://github.com/Salih04/financeiq-research-code/issues/10#issuecomment-6781248365) and `FIQ07_F1_F2_OWNER_DECISION_2026-11-10.md`.

Original fail-first [CI #42907961629](https://github.com/Salih04/financeiq-research-code/actions/runs/42907961629) is historical: 67 baseline test methods passed, four positive controls passed, and two negative-test methods produced four failing subtest reports. The F1/F2 acceptance cases were reproduced in the actual original module, not only a surrogate.

**Applied to this draft PR #15:**
- F1 `archive_search.search_date` = execution civil day in Europe/Istanbul. Compare only with Istanbul civil date of `system_as_of`: same day and earlier allowed, later refused. No lower bound in v1.0.0. Do not compare to `as_of`.
- F2 immutable KER-09 statement version: enforce `assertion_id → (member_kind, member_id, status)` across all quarters. Different member/status under one ID refused; same member/status repeated across quarters permitted. `source_evidence_id`, tier and `tier_cell` are per-quarter row locators and are not bound to an assertion ID. Document identity, revision and interval coverage remain with KER-09 producer.
- Required tests: F1 late dates 2022-10-11 / 2030-01-01 rejected, same Istanbul day (including UTC boundary) and 1999 no-lower-bound accepted; F2 different member and same member status flip rejected, same statement repeated and changed `source_evidence_id`/tier cell accepted.
- Native invented 2022 fixture bytes unchanged. Existing suite counts 16+21+18+8+4=67; new Fable consumer suite = 10, target 77/77 with zero skips. Runner, `docs/TEST_ACCOUNTING.md`, and exact `PUBLIC_TREE.json` hashes must agree.
- **Merge gate:** hosted exact-head PR CI 77/77, zero skips, then one genuine independent reviewer pinned to that unchanged head; no merge solely from this document. Keep PR draft before review.

Scope is **invented-only public consumer**. No private Kernel source, DataStore real ROWS or aggregate contents, provider rights access, market outcomes, DSA installation/logging, model choice, Study 4 execution or OSF. `NO_NEW_OUTCOME_INSPECTION=true`.
