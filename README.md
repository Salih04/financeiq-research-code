# FinanceIQ research code

Public code repository: [https://github.com/Salih04/financeiq-research-code](https://github.com/Salih04/financeiq-research-code). Research support only; not investment advice.

This repository starts with a fresh Git root. It contains research and backend source,
the approved synthetic-only Kernel snapshot consumer, synthetic fixtures and paper
design documents. It contains no empirical dataset, result artifact or source-data
manifest. No investment edge is established by the software or synthetic tests.

The complete frozen Capstone v1 record, original manuscripts, all data, the app and
machine-of-record verification remain in the restricted private archive. The old
headline interpretation was withdrawn; empirical evidence and limitations remain
in that original record. This export grants no source-data redistribution rights.

The legacy frontend contains embedded empirical evaluation constants and unverified
fallback samples, so it is retained only in the archive. Root/backend test sources
and data-dependent pipelines are also retained there. This is a code reference and
synthetic boundary test package, not a deployable public Capstone demonstration.
No Docker build configuration or image is published.

## Verification

Run `python -B scripts/public_safe_tests.py` after installing
`requirements-public.txt`. It executes exactly 16 PIT consumer and 21 research-core
synthetic tests, fails on missing tests or skips, and checks the explicit file list.
It does not execute legacy pipelines, acquire data, query SQL or touch holdouts.
See [test accounting](docs/TEST_ACCOUNTING.md) for the private suite boundaries.

## Research boundaries and papers

- [Governing Research Charter](docs/process/RESEARCH_CHARTER.md) and its
  [owner addendum](docs/research/OWNER_DECISION_ADDENDUM.md).
- [Paper 1 public methods edition](docs/paper1/draft.md). Empirical sections remain restricted.
- [Paper 2 design](docs/paper2/DESIGN.md) and [unregistered OSF draft](docs/paper2/OSF_PREREGISTRATION_DRAFT.md).
- [Paper 3 candidate design](docs/paper3/DESIGN_CARD.md).

No adoption, registration, holdout access or experiment permission is created by
this export. Historical membership must not be reconstructed from current lists;
the capstone cohort is not the research universe. Missing stored values stay null.
All trials, including failures and abandonment, must be recorded. Outcomes never
flow back into PIT Kernel. Approved synthetic fixtures are unchanged; no new derived
public fixture was created. Future derived fixtures still require FO-4 review.
