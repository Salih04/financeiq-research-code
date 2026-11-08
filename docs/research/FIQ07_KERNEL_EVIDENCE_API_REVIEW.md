# FIQ-07 — source-evidence API fit and contract-review gates

**Status: PROPOSED TECHNICAL REVIEW ONLY — NOT AN ADOPTED EXCHANGE SCHEMA,
SOURCE-RIGHTS DECISION, UNIVERSE BUILD OR EXECUTION AUTHORIZATION.**

Review date: 2026-11-08 (Europe/Zurich). FinanceIQ's governing
[Research Charter](../process/RESEARCH_CHARTER.md),
[owner addendum](OWNER_DECISION_ADDENDUM.md),
[adopted U1-only rule v2.0.0](UNIVERSE_RULE.md) and the
[FIQ-07 consumer requirements](FIQ07_KERNEL_CONSUMER_REQUIREMENTS.md) take
precedence. See [FIQ-07 tracking issue](https://github.com/Salih04/financeiq-research-code/issues/2).

This is an **outcome-free consumer-side mapping of currently implemented
*internal* PIT Kernel selectors**. It neither reproduces private Kernel
implementation nor requests a new membership engine. Function names identify
existing capabilities for an access-controlled contract review; they are not
public APIs, approved export formats or promises of deployability.

## 1. Existing capability versus missing contract

| Existing internal selector or report | Verified software semantics | Missing before FinanceIQ can consume it |
| --- | --- | --- |
| KER-09 `persisted_membership_as_of` | As-of evidence for one explicitly typed member in a collection. Responses distinguish `MEMBER`, evidenced `NOT_MEMBER`, `UNKNOWN`, `AMBIGUOUS` and `CONFLICT`, and retain source assertion lineage and later-effective pending claims. | Approved exchange row type, legal per-operation export, exact query and response schema, collection-definition rights and source completeness |
| KER-09 `persisted_memberships_as_of` | Returns source-evidenced member results at the requested cutoff; **not a full official roster** or proof that omitted members are nonmembers. | Publisher channel inventory, negative-search and copy-set completeness evidence; no inferred absent rows |
| KER-10 `persisted_identity_record_as_of` | Source-evidenced, typed historical binding; returns `BOUND`, `UNKNOWN` or `CONFLICT` with version IDs. Requires a settled system cutoff. | Separately evidenced durable **listing → security → issuer** mapping. A BIST listing/code binding is not itself issuer/security equivalence |
| KER-13e `persisted_quarterly_membership_counts` / local report | Compares explicitly presented membership evidence and identity at aligned cutoffs; the owner-local report describes **same-publisher channel consistency**. | Independent-source corroboration, G03 filing metadata, comprehensive research formation coverage; any proposed publication of counts needs separate clearance |
| Existing `4.0.0` snapshot | Published filing-fact envelope with pinned schema and hash semantics. | Membership, identity, event and completeness rows are **not included**. Do not reinterpret filing facts, change historical hashes or relax E-1 six-envelope acceptance pins |

Internal APIs require **no FinanceIQ write-back**. No source bytes, local
paths, company codes, observed pilot counts, returns, securities or empirical
performance belong in this public code-only review. A rights-safe internal
reference implementation is not proof of permission to transfer actual rows.

## 2. Three clocks and precision are mandatory

A future request must explicitly identify the relevant **official formation
period and effective instant** separately from Kernel source-evidence
`effective_date` (a collection-local civil date), public-availability
`as_of` (bounded by reviewed `known_at_upper`) and settled recording
`system_as_of` (anchored commit authority, not `recorded_at` or retrieval).

The reviewed contract must pin both cutoffs, the exact source vintage and
immutable query/response digest. Refuse an unavailable, unreviewed, uncommitted
or unsettled record rather than substituting an available date. Unknown
publication time stays unknown. A civil effective date without evidenced
intraday precision cannot establish same-day event order or the U1 formation
instant. Source evidence publicly available only *at* F is not silently
treated as admissible if the adopted U1 rule requires it to precede F.

## 3. Proposed failure and release boundaries

These are **review requirements, not implemented response enums**:

- Preserve each actual Kernel status without collapsing `UNKNOWN`,
  `AMBIGUOUS` or `CONFLICT` to `NOT_MEMBER`. Only explicit reviewed
  negative evidence can produce an actual nonmember assertion. A
  `WITHDRAWN` supersession never revives an expired version.
- Distinguish **no evidence**, **incomplete channel/search**, **unsettled
  system authority**, **unverified source rights**, **identity mismatch**,
  **chronology ambiguity** and **unsupported contract**. Missing fields
  or unknown publication bounds block the affected formation, not a
  favorable result.
- If approved in the future, the receiver must independently check the
  contract version, immutable digest, source lineage, exact field allowlist,
  cutoffs, identity type and operation-scoped rights record. Any mismatch
  refuses before using rows in FinanceIQ research.
- An internally admissible rights decision for parsing/retention is **not**
  permission for downstream private sharing, public redistribution,
  public aggregates, machine-learning use or future retention. A current
  chain-head/expiry/conditions check and explicit destination/operation
  clearance remain required at the time of every proposed export.
- Kernel supplies source claims, timestamp authority and immutable lineage.
  FinanceIQ alone applies adopted U1 v2.0.0 formation, exclusions and
  strata. Neither Kernel nor a successful consistency check chooses a
  research universe, target, threshold, result or trial.

## 4. Minimum owner / Kernel decisions before implementing an adapter

| Gate | Present disposition | Required decision or evidence |
| --- | --- | --- |
| **C1. Projection** | **NOT APPROVED** | Review whether an additional, independently versioned **read-only source-evidence envelope** may be designed over existing KER-09/10 selectors, without amending `4.0.0` or exposing raw internal records |
| **C2. Identities/time** | **UNSET** | Approve type system, source lineage and official-period precision, binding of publication and settled commit authority, and which error distinctions survive the projection |
| **C3. Completeness** | **UNVERIFIED** | Demonstrate authorized source-channel coverage and revision/search provenance, plus distinct independent corroboration if required; same-publisher agreement is insufficient |
| **C4. Rights/transport** | **CLOSED** | Confirm exact source/product/recipient, permitted operations, field allowlist, retention, authentication, destination and publishability of any aggregate; enforce latest applicable rights decision |
| **C5. Science** | **BLOCKED** | Separate owner decisions for U2, G03/KAP evidence and feasibility; per-study registration, exposure ledger and protected-period access remain closed |

**Suggested authorization sequence:** First approve **contract design and
independent review only**; then review a separate synthetic-only public
consumer proposal *if* exact projection and allowable test fixtures are
approved. No new public fixtures or CI tests are authorized by this note;
the existing **16 PIT + 21 research-core** suite remains unchanged. Any
derived public fixture requires FO-4 review. Only separately authorized,
rights-cleared private data work could later test a consumer against real
sources, and that still would not create scientific or holdout authority.

Do not infer adoption of unresolved internal Kernel governance from a merged
software implementation. No historic decision or trial record is overwritten.
