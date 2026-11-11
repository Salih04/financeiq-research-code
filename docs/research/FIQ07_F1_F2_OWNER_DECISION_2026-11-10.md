# OWNER CONTRACT DECISIONS — FIQ-07 F1/F2 (2026-11-10)

**Status:** owner-adopted, `membership-evidence` v1.0.0, public invented-only consumer. Canonical dated owner decision is recorded in [issue #10](https://github.com/Salih04/financeiq-research-code/issues/10#issuecomment-6781248365). It is not permission for real data access, scientific execution or automatic merge.

## F1 — Archive-search execution day

`archive_search.search_date` is the archive-search **EXECUTION civil date in Europe/Istanbul**. Consumer condition: `search_date <= system_as_of.astimezone(Europe/Istanbul).date()` with same civil date accepted. No earliest-day lower bound in 1.0.0; source completeness is separately the producer's `source_complete` attestation. No `search_date <= as_of` condition: native invented 2022 fixtures have archive search after formation with later system snapshot.

## F2 — KER-09 immutable assertion statement

`ASSERTION_ID_KIND=STATEMENT`. An ID is one append-only immutable KER-09 assertion version fixing member, status, interval and source document; revisions get new IDs. The native selector emits only covering live heads having the row status; conflicting statuses yield `CONFLICT` and do not enter ROWS.

Consumer invariant **across ALL quarters of one bundle**: `assertion_id -> (member_kind, member_id, status)` constant. Different member or status flip under one ID rejected. Same member + same status across quarters is permitted for multi-quarter intervals. `source_evidence_id`, tier and `tier_cell` are per-quarter locators, **NOT bound** to assertion ID; changed locators must be accepted. The public consumer cannot prove source-document or interval immutability beyond its represented tuple; those remain KER-09 producer duties.

## Exact-head acceptance

Retain 67 baseline invented-only tests, add 10 F1/F2 tests, preserve byte-identical native 2022 fixture, require 77/77 hosted CI PASS and zero skips, then **one independent review on unchanged exact head**, then separate merge decision. All private Kernel operations, real ROWS, protected aggregates, source rights, prices, outcomes, DSA installation, Study 4 logging, model choice and OSF remain closed. `NO_NEW_OUTCOME_INSPECTION=true`.
