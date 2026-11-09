# FIQ-07 - outcome-free PIT Kernel consumer requirements (PROPOSED)

**Controlling 2026-11-09 owner authorization:** See the C1–C5 table in
[FIQ07_KERNEL_EVIDENCE_API_REVIEW.md](FIQ07_KERNEL_EVIDENCE_API_REVIEW.md).
Design and invented synthetic implementation of `membership-evidence 1.0.0`
are **AUTHORIZED**; no actual Kernel export or real-input access yet.
KER-10 `BOUND` `LISTING` at effective date is sufficient for U1 membership
validation; security/issuer and cross-period mappings are nullable and only
dependent joins fail. Explicit `as_of`/`system_as_of`, settled authority and
digests are mandatory. Absent evidence is `UNAVAILABLE`, never `NOT_MEMBER`.
FIQ-07 completeness uses 3184 workbook + recorded announcement search with
`SAME_PUBLISHER` **consistency check**, not independent validation; Kernel
G07 independent ancestry is not a FIQ-07 gate (Paper 2 G07 rate priority is
distinct). Public Git/CI contain only code and invented synthetic fixtures;
the only later real recipient is owner-private local vault hash-bundle after
rights and adapter gates. No owner-local rows/counts in Git/CI/chat; publish
aggregates only in papers after study gates. Through 2022-12-31 formations
`ROWS` are permitted only after real gates; 2023–2025 formations are
`COUNTS_ONLY` for four OD-1=B aggregates pending registered opening.
A protected-window pilot is not a row test. Older proposal below remains
dated historical text and **is superseded if inconsistent**.

---

Status: **HISTORICAL 2026-11-07 PROPOSAL / SUPERSEDED WHERE INCONSISTENT**.
Date: 2026-11-07 (Europe/Zurich). Research support, not investment advice.

This is FinanceIQ's minimum *consumer-side* request for a separately reviewed,
one-way PIT Kernel interface. It is not a Kernel implementation plan, an adopted
exchange schema, a source-rights decision, a research registration, or permission
to read real membership, historical observations, outcomes or holdouts. It changes
no existing source, model, experiment or evaluation. See [FIQ-07 issue #2](https://github.com/Salih04/financeiq-research-code/issues/2).

## Authority and current capability

- The [Research Charter](../process/RESEARCH_CHARTER.md) governs U1 and holdout
  boundaries. The [owner addendum](OWNER_DECISION_ADDENDUM.md) preserves scoped
  approvals and unresolved evidence gates.
- The owner adopted [U1-only v2.0.0](UNIVERSE_RULE.md) on 2026-11-03. It defines
  FinanceIQ's formation/admission semantics, including 3184 narrowest-tier
  interpretation, per-quarter 30/20/50 validation, source chronology, identity,
  events, survivor inclusion and nullable G03 strata. The numbers are *rules*,
  not empirical membership measurements.
- The current [Kernel snapshot consumer](../../experiments/pit/kernel_snapshot.py)
  pins contract `4.0.0` and six approved E-1 invented filing-fact envelopes.
  It explicitly rejects other bytes with `ContractUnverified`. It does **not**
  provide an approved membership, identity, event, source-channel completeness,
  or template-stratum interface. Do not expand E-1 acceptance by removing hash
  pins or repurposing filing-fact keys.
- The older private FIQ-07 task card refers to v1.0.0 and broader data it did
  not prove available. That dated task is not current authorization.

## Consumer input needs - proposed field concepts, NOT an existing schema

All facts below require immutable content identifiers, exact source identity,
version, acquisition timestamp and evidenced public-availability bounds. Types,
names, cardinality, serialization, allowed source channels, rights and transport
version are **UNSET** pending separate Kernel/owner review. A timestamp's upper
bound must be used conservatively when checking availability.

The proposed interface must also keep **independent as-of and system-time
cutoffs**. Source-publication availability is not the system's recording or
settlement time: a later imported/replayed assertion must not become visible in
an earlier system snapshot. An independently verified commit authority (or a
separately reviewed equivalent) must bind the stored version to its system-time
cutoff. Acquisition, insertion and source effective dates must never silently
substitute for either public knowledge time or settled system time. These are
contract requirements, **not** evidence that an exporter already provides them.

| Outcome-free concept | Minimum required evidence | FinanceIQ-side rule it enables |
| --- | --- | --- |
| Official index period | Year/quarter label, official effective date/instant (historical Europe/Istanbul), provenance and precision | Bind formation F to the true period, not download or first-trade date |
| 3184 workbook block | In-document year/quarter label, source copy ID/content hash, original narrowest-tier code and source share/security code, parsing quality | Quarter binding and the approved XU030/XU050/XU100 tier interpretation |
| First-party public copy | Source kind, document ID, content hash, publication lower/upper bounds, retrieval time and ordered-copy lineage | Enforce strictly pre-F availability and B2/22-B compatible copy chronology |
| Channel completeness | Scope, retention limits, workbook coverage, documented BIST archive query/date/result count/pagination/caps and found-copy reconciliation | Fail closed when required source-channel completeness or negative search is unproved |
| Identity mapping | KER-10 BOUND LISTING at effective date; nullable security/issuer and cross-period mapping with evidence and collision flags | U1 formation validation requires BOUND LISTING, and only dependent security/issuer joins fail when unavailable; no literal-code inference |
| Membership collection and assertion | Collection definition, member kind (listing/security/entity or reviewed equivalent), effective local civil interval and zone, typed member identity, source version/chain, public-knowledge bound, settled system-time authority, and explicit positive/negative/withdrawn evidence | Preserve source assertions and uncertainty without deriving a research universe or inferring a missing roster row as negative evidence |
| BIST review or change event | Official ADD/REMOVE/other applicable action, public bounds, effective time, member/reserve role, ordering and evidence of integration in the periodic table | Apply M5/M6, same-day IN0/OUT0 and conditional predecessor M7 |
| KAP statement template | Versioned first-party template category/effective interval, documented identity binding and holdings-class evidence or null | Classify G03 bank/insurance/standard TFRS; preserve unknown holdings/null |
| Evidence envelope | Snapshot/request binding, content and algorithm digests, contract version, allowed field set, immutable source references | Pin a reviewed read-only consumer; reject incompatible or altered inputs |

This table **does not request** prices, returns, scores, rankings, forecasts,
outcome availability, empirical coverage counts, individual protected-period rows,
or any private corpus for the public repository. Research selection/inference
belongs to FinanceIQ; source acquisition, proof and lineage belong to Kernel.
No FinanceIQ result or performance feedback is sent to Kernel.

## Membership and timing interpretation (proposed, not implemented)

An internal source-membership answer must preserve the distinction between
**explicitly evidenced nonmembership** and **absence of evidence**. Unknown,
ambiguous and conflicting claims remain separate refusal states (or separately
reviewed equivalents), never `false`, zero, or an inferred negative row.
A future-effective assertion known before its effective interval begins must
not be applied early. A superseded or withdrawn assertion must not be silently
revived from an older chain version. Member-kind mismatches, multiple identity
candidates and conflicting admissible chains block the affected operation.

Collection-local civil dates and evidence of an official effective *instant*
are different precision classes. A civil interval alone does not establish
intraday event ordering or a formation instant. Where FinanceIQ's U1 rule needs
that ordering, require separately evidenced precision; otherwise refuse that
formation rather than inventing an exchange opening/closing clock.

FinanceIQ must keep public-knowledge `as_of`, recorded `system_as_of` and
formation/economic valid time distinct, and bind them to the exact requested
snapshot, digest, rights assessment and source version. Any proposed transfer
of row-level material into a private research runtime needs its own lawful
operation-specific rights and scope decision; **a public code-only document is
not a data-sharing authorization**. Protected-period individual rows are not
unlocked by this interface design or by the owner-approved aggregate-only OD-1
metadata allowance.

## Fail-closed consumer requirements (not yet implemented)

1. Reject an unreviewed contract major/minor/schema or hash algorithm and any
   missing, duplicated, inconsistent or unbound source/identity/effective-time
   claim. Pin the exact reviewed contract and digest set first.
2. For F, require first-party period timing plus source copy *public-availability
   upper bound* strictly before F, and compatible workbook/announcement period
   labels. A later retrieval cannot make a historical formation eligible.
3. Treat missing source retention, channel search, pagination/caps, ambiguous
   revisions or unexplained differences as **unavailable**, not an empty source.
   Evaluate all period labels before global deficiency propagation (23-B).
4. Retain literal tier evidence; unknown cells yield null/unavailable, not
   nonmembership. Validate independent 30/20/50 narrowest counts, nested
   30/50/100 and identities before accepting any formation.
5. Reject missing/conflicting security-issuer identity, source-tier collisions,
   unknown event integration or unresolved simultaneous event ordering. Preserve
   all causes, including NOT EVALUATED versus NOT EVALUABLE; do not make M7 a
   favorable fallback when it can be evaluated and mismatches.
6. Keep exiting/delisted constituents in the accepted formation cohort. Defer
   entrants between reviews until the next official formation. Nullable G03
   strata and holdings never become guessed classifications.
7. Never use current constituents, the frozen Capstone v1 list, today's sector
   label, implicit interpolation, favorable-source choice or a return-driven
   formation/window cutoff.
8. The public consumer must remain inert without an authorized binding. No
   network/source acquisition, DB query, hidden source-data read, protected
   aggregate, real-data construction, experiment or Kernel write is permitted by
   this document. Protected access and study-specific registration remain
   separate gates.

## Proposed *future* synthetic acceptance cases - NOT EXECUTED HERE

These are test descriptions, not created fixtures or new CI tests:

- A valid-looking tier count with an unknown quarter/publication bound **fails**;
  a count alone cannot establish provenance or point-in-time admission.
- XU030/XU050/XU100 narrowest tiers imply nested membership only when
  the cell and identity are evidenced; missing/unknown tier remains null.
- Intra-quarter exit/delisting retains the original formation member; late
  entrant is absent until the next formation. This is a rule, not an observed case.
- Workbook/announcement identity disagreement, duplicate row, contradictory
  tier or out-of-order event **fails** without silent deduplication.
- An unavailable template evidence class leaves the G03 value null and the
  affected operation blocked; no sector-name inference.
- A forged hash, wrong contract, altered read-only snapshot or a value with
  unknown/late `known_at_upper` is rejected. The existing six E-1 synthetic
  envelopes remain accepted only for their current purpose.

The **historical proposal** added no synthetic test. The owner on 2026-11-09
authorized **invented synthetic-only** consumer tests for the new contract.
Report new suite counts transparently without reducing baseline PIT 16 and
research-core 21. Any *derived from private source* public fixture still
requires FO-4 and publication clearance; none is approved here.

## Decisions and evidence still required

- **Interface status: UNSET.** Kernel owner must review whether a compatible
  outcome-free membership/evidence contract exists. Exact field vocabulary,
  snapshot version, maximum payload, transport rights and validation rules are
  not assumed from today's E-1 consumer.
- **Source evidence: UNVERIFIED.** Completeness, historical vintage/publication,
  effective-dated identities, justified B2 revisions and KER-13b templates
  require independent source proof. This request does not claim that any source
  was accessed, purchased, searched or complete.
- **Science gates: UNSET/BLOCKED as applicable.** U2, G03 source adequacy,
  joint KAP/price feasibility, OD-4/14/15 window choices, protected metadata
  OD-1 eligibility, exposure ledger, study registration and holdout openings are
  unchanged. No real U1 formation or protected aggregate is authorized.
- **Owner sequence:** review this request as *requirements only*; obtain an
  approved Kernel contract independently; then review a fail-closed FinanceIQ
  consumer and synthetic tests under the public test-count policy. Only
  separately authorized data-bound work may run against real sources.

This proposal is intentionally free of source observations, actual identity
tables, vendor paths, empirical results, quantitative coverage and credentials.
Publication in a code-only repository is not evidence of licence or validity.
