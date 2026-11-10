# FIQ-07 Fable candidate reproduction - archival DRAFT (2026-11-10)

Public base: `5b1030ad9e6760af22f5f8fc0cf36a355b9f6df8`.

This branch is **intentionally RED / FAIL-FIRST**. The added test file imports
the ORIGINAL public consumer `open_kernel_wire_synthetic` and its existing
invented-only helper, not the earlier reconstructed surrogate. It provides
three existing-behavior controls, two expected-rejection candidate methods with
two subcases each, and a same-listing cross-quarter control. It changes NO
production code, source rights, native synthetic fixture or scientific rule.

After an exact-head hosted GitHub CI run, inspect the two failure methods and
confirm all controls pass. Failure is expected **only in this draft branch**;
it is NOT merge-ready. Before a production patch, owner must fix the versioned
meaning of `archive_search.search_date` (execution vs archive coverage; civil
date same-day ambiguity), and decide if `assertion_ids` have cross-quarter
identity scope. The candidate `FIQ07_FABLE_CANDIDATE_FIX.diff` is stored
for historical review ONLY and has not been applied.

The accepted native invented producer 2022 fixture has archive search dates
after formation but before its 2026 system snapshot. Never enforce
`search_date <= as_of` and do not decide a 1999 lower bound from this audit.

Baseline synthetic suites: 16+21+18+8+4 = 67 PASS. New test module: 6
registered cases; new expected collection count 73. All existing tests must
stay green; only the two Fable candidates are expected fail-first. Any final
fix requires no skips, 73/73 passing exact-head CI, separate review and owner
merge. The public allowlist and test accounting are changed in this DRAFT
only; public main stays unchanged.

No private Kernel files, DataStore source, real ROWS/COUNTS_ONLY, outcome,
holdout, price, DSA, Study 4 logging or OSF. `NO_NEW_OUTCOME_INSPECTION=true`.
