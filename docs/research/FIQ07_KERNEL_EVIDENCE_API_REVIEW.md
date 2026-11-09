# FIQ-07 — source-evidence API fit and contract-review gates

**Status: OWNER-AUTHORIZED DESIGN AND SYNTHETIC IMPLEMENTATION — REAL-DATA AND HOLDOUT GATED.**

## Controlling owner decisions — 2026-11-09 (C1–C5)

**AUTHORIZED:** design and synthetic-only public consumer implementation of
`membership-evidence 1.0.0`, **read-only and one-way Kernel→FinanceIQ**.
The filing-fact `4.0.0` contract and its six pinned E-1 synthetic envelopes
are unchanged. The earlier Kernel [Issue #28 feasibility answer](https://github.com/Salih04/financeiq-pit-kernel/issues/28)
was nonbinding and predates this owner authorization. The older 2026-11-08
proposal below is preserved as dated evidence; where its `UNSET`, no-synthetic
authorization or independent-source requirements conflict, **this decision
controls prospectively**.

| Gate | Owner disposition |
| --- | --- |
| **C1 — canonical U1 identity** | KER-10 **`BOUND` `LISTING` at effective date**. Issuer/security and cross-period equivalence are nullable; only a join needing an unresolved mapping fails. No literal-code matching outside KER-10 mappings. Absent evidence = `UNAVAILABLE`, never `NOT_MEMBER`. No new source membership engine. |
| **C2 — time and integrity** | Explicit `as_of`, `system_as_of`, effective-time coordinate, pinned request/content digests and verified settled authority are mandatory; reject implicit/latest, missing, ambiguous, unsettled or incomparable recording authority. |
| **C3 — completeness and comparison** | Adopt U1 v2.0.0's first-party **3184 workbook + recorded announcement search** completeness rule. Independent-source validation is **NOT required for FIQ-07**. Label any comparison `SAME_PUBLISHER` and call it a **consistency check**, never independent validation. Kernel **G07 independent-ancestry** comparison is not passed and is not a FIQ-07 gate. Paper 2 **G07 rate-priority** is a different gate, unchanged. Missing in-scope evidence stays `UNAVAILABLE`. |
| **C4 — private recipient** | Any *later authorized* real delivery is only to the **owner's private local environment** as a vault file bundle with verified hashes. Public Git and CI hold **consumer code and invented synthetic fixtures only**. No owner-local rows or counts in Git, CI or chat. Aggregates may appear **only in a paper** after its study-specific gates. Exact current source/operation/recipient rights and retention are still separately required; no real export now. |
| **C5 — research boundary** | FinanceIQ alone applies U1 2.0.0. Formation dates **through 2022-12-31:** `ROWS` access class, subject to rights, a merged Kernel adapter and loaded private development files. **2023-01-01 through 2025-12-31:** `COUNTS_ONLY`, restricted to the four OD-1=B aggregates until registered opening. The protected-window pilot is **not** the FIQ-07 row test; use a development-window quarter. No holdout opening or real experiment permission. |

**Execution sequence:** this PR is **docs-only**, owner directs ready + merge
without an additional review round. Then create a separate public,
synthetic-only consumer implementation and independently check the expanded
synthetic suite. Actual source transfer stays closed until the Kernel adapter
is merged, the rights-cleared vault bundle is loaded locally, and applicable
science/research gates are satisfied. Do not backdate adoption.

---

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
| KER-09 `persisted_membership_as_of` | As-of evidence for one explicitly typed member in a collection. Responses distinguish `MEMBER`, evidenced `NOT_MEMBER`, `UNKNOWN`, `AMBIGUOUS` and `CONFLICT`, and return covering assertion IDs, a known-at upper bound and pending-claim IDs; the response does **not** include complete source-document or version-chain lineage. | Approved exchange row type, legal per-operation export, exact query and response schema, collection-definition rights and source completeness |
| KER-09 `persisted_memberships_as_of` | Returns source-evidenced member results at the requested cutoff; **not a full official roster** or proof that omitted members are nonmembers. | Publisher channel inventory, negative-search and copy-set completeness evidence; no inferred absent rows |
| KER-10 `persisted_identity_record_as_of` | Source-evidenced, typed historical binding; returns `BOUND`, `UNKNOWN` or `CONFLICT` with version IDs. Requires a settled system cutoff. | Separately evidenced durable **listing → security → issuer** mapping. A BIST listing/code binding is not itself issuer/security equivalence |
| KER-13e `persisted_quarterly_membership_counts` / local report | Compares explicitly presented membership evidence and identity at aligned cutoffs; the owner-local report describes **same-publisher channel consistency**. | Independent-source corroboration, G03 filing metadata, comprehensive research formation coverage; any proposed publication of counts needs separate clearance |
| Existing `4.0.0` snapshot | Published filing-fact envelope with pinned schema and hash semantics. | Membership, identity, event and completeness rows are **not included**. Do not reinterpret filing facts, change historical hashes or relax E-1 six-envelope acceptance pins |

Internal APIs require **no FinanceIQ write-back**. No source bytes, local
paths, company codes, observed pilot counts, returns, securities or empirical
performance belong in this public code-only review. A rights-safe internal
reference implementation is not proof of permission to transfer actual rows.

**Current response is not provenance-complete.** KER-09's source-evidence
selector returns `assertion_ids`, `known_at_upper` and a limited `pending`
summary, but not `source_doc_id`, `source_hash`, full supersession-chain
records, or the settled commit-authority proof as exchange fields. These are
used or validated internally, not exposed as a self-contained transferable
attestation. An independently reviewed rights-scoped projection would need
to define how the minimum required lineage/authority is authenticated without
exposing prohibited source material. The consumer must reject missing
lineage rather than infer it from an assertion identifier.

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

### No implicit latest watermark or mixed settlement lineage

KER-09's *internal* persisted membership functions currently accept an omitted
`system_as_of` and then use an accepted latest settlement watermark. That is a
convenience for an internal query, **not a deterministic FinanceIQ exchange
contract**. A future consumer must supply a nonempty, explicit, version-pinned
`system_as_of` on every request, record the returned accepted cutoff, and
verify its relation to the requested cutoff before any result can be used.
Do not construct a research cohort by combining individually valid answers
queried at different implicit/latest watermarks.

If an approved projection ever combines KER-09 membership, KER-10 identity
and another source-channel comparison, it must bind them to a **verified
consistent settled state**. Merely choosing the numerically earliest of
multiple system timestamps is not proof that independent recording histories
share a comparable commit authority. Where shared lineage, durability or
cross-schema settlement comparability is unproved, return an explicit
unavailable/refusal outcome rather than merging the apparent answers.
The exact alignment and proof mechanism is **UNSET** for owner/Kernel review.

A future synthetic acceptance criterion (NOT a fixture or test introduced
here) is that a request with missing implicit system cutoff, mixed cutoffs,
unsettled authority or unverifiable cross-history comparability is rejected,
even when the source membership responses otherwise appear consistent.

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

## 4. Current status

The controlling 2026-11-09 owner decisions above authorize the new synthetic
consumer; their implementation does not require independent-source G07 for
FIQ-07, inferred issuer IDs, access to protected rows, or a new membership
engine. The older review table and unapproved design suggestions were
superseded; unresolved **real-data rights, Kernel adapter and private bundle**
gates remain. Neither a successful consistency check nor this documentation
constitutes scientific validity.
