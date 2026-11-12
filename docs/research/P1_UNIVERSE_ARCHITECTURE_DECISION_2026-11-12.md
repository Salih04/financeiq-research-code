# OWNER DECISION — P1 per-study universe architecture (2026-11-12)

**Status:** adopted by the owner on 2026-11-12 (Europe/Zurich) through explicit owner answers in chat. The
decision is prospective. It registers no study. It grants no access to real data, holdout or outcomes, and it
makes no new source-rights claim. `NO_NEW_OUTCOME_INSPECTION=true`.
Research support only; not investment advice.

**Question.** Should every study use the same point-in-time universe, or should each study's primary universe
fit its question, with the other universe as a pre-registered secondary? Registration makes the choice a
one-way door for each study.

## 1. Decision: study-specific primaries, staged behind a coverage gate

The terms below follow charter §4. U1 is point-in-time BIST 100 under rule 2.0.0. U2 is the screened,
survivor-inclusive broad universe. The gate is the coverage gate in §3.

| Study (charter §6) | Primary | Secondary | Condition and fallback |
|---|---|---|---|
| Paper 1 — audit | U1 | U2, only if the gate passes | U1 stays primary if at least **75%** of the frozen 40-company cohort's firm-quarters are U1 members. Below that, U2 is primary if the gate passes. If the gate fails, U1 is primary and the claim is limited to index-member firm-quarters. The cohort is the audited object and never a research universe (charter §2). |
| Paper 2 — disclosure event study | U1 | U2 non-members, as a heterogeneity arm | The arm exists only if the gate passes **and** the surprise definition is computable for non-U1 firms. That definition, including the treatment of financials, is fixed across the IAS 29 boundary before any universe work. |
| Study 3 — open modeling | U2 | U1, reported as a stratum and never as a second confirmatory test | Study 3 is registered only if the gate passes. The target is a minimum detectable mean rank IC of **0.03 at 80% power** over the 36 holdout months, which gives an **N floor of 486** (§4). **If the gate fails, Study 3 is not registered and its locked holdout stays unopened.** |
| Paper 3 candidate — fund-flow pressure | Not decided | U1 | Not registered. The rule that maps a holdings profile to a universe is written before a development-window holdings profile runs. Until then, this supersedes the card's provisional "Charter U1" population. |
| Study 4 — LLM agent forward test | U1, forward | None by default | Registered first, because its forward clock runs. Forward membership comes from dated official announcements. The agent's version is pinned and a replacement rule is set before logging starts. |

**Fallback if the gate fails or times out (one outcome per study):**
- Paper 1: U1, with no U2 secondary.
- Paper 2: U1, with no arm.
- Study 3: not registered; its holdout stays unopened.
- Paper 3 candidate: shelved.
- Study 4: unchanged.

A timeout defers Study 3 and the Paper 3 candidate; it never drops them.

## 2. U2 refinement (prospective; no rule version yet)

- U2 is one nested rule: screened non-members plus all U1 members, with the U1 tier kept as a stratum. U1 rule
  2.0.0 is unchanged.
- Screens are cross-sectional ranks or percentiles, computed only from data available before formation. They
  never use nominal TRY thresholds, which drift with inflation. They are fixed on development data and never on
  return results. Index-exit and screen-failure in the same quarter get an explicit rule.
- Each registration fixes an exit-return rule and its sensitivity bounds. Sensitivity values are computed at
  analysis time and never stored. Missing returns stay null.
- A U2 rule version is a later artifact, reviewed separately.

## 3. Coverage gate

A **dated, hashed gate memo** fixes the items, exact definitions (denominators, the meaning of "left the
listing", year pooling), thresholds, sources and a backstop date **before any coverage profiling**.

Candidate items:
- Codes that left the listing keep price history up to a last trading day taken from an independent source:
  at least 95%.
- Adjusted returns are computable for at least 95% of stock-quarters in each development year.
- The coverage gap between departed and surviving codes is under 5 percentage points.
- The median post-screen N is at least 486 (Study 3).
- Fundamentals and disclosure timestamps cover at least 90% of firm-quarters, for the studies that use them.
- Point-in-time segment status is available.
- An entity/ticker map handles renames and reused codes.

Rules:
- The gate reads development years only (up to 2022). No 2023–2025 rows, counts or coverage are inspected. That
  includes "structural" holdout coverage, because knowing which codes have holdout rows reveals holdout
  survival.
- The private environment reports PASS or BLOCKED per item. No counts are published.
- The gate clock starts when the legacy 2017–2021 workbook parse passes.

## 4. Power basis (lower bound)

The calculation uses the null variance of a monthly cross-sectional rank IC, about 1.06/(N−3), over 36
independent holdout months. MDE is the minimum detectable mean IC. Real IC variation and dependence enlarge the
required N, so the N floor can only rise once development-window IC volatility is known.

| N | MDE at 50% power (t = 3 expected) | MDE at 80% power | Months needed for IC 0.03 at 80% power |
|---|---|---|---|
| 100 | 0.052 | 0.067 | 179 |
| 200 | 0.037 | 0.047 | 88 |
| 300 | 0.030 | 0.038 | 59 |
| 450 | 0.024 | 0.031 | 39 |

Breadth is decisive only for Study 3. On U1 alone, Study 3 could not confirm a realistic IC within the holdout.
The owner accepted that an N floor of 486 may block Study 3. In that case Study 3 waits for new data rather than
spending its single holdout opening on a test that cannot detect the effect.

## 5. Membership-cell semantics check (all studies, before any registration)

Every universe design assumes that a Product 3184 quarterly cell records the membership in force at the
period-start date. The PIT Kernel checks this outcome-blind and reports only PASS, BLOCKED or INCONCLUSIVE.
- Where intra-period changes are published, the check uses them.
- Charter §4 notes that intra-period changes for the benchmark indices were not published before late 2023. For
  2017–2022, U1's mandatory cross-check against the periodic review announcements, which fails closed, carries
  this assurance.

## 6. Exposure history

The frozen capstone's 2023–2025 results for the 40-company cohort were seen earlier. The holdout is therefore
less clean for those large caps than for non-index firms. Every registration that uses U1 records this.

## 7. Consultation record and G3 governance

**G3 (owner, 2026-11-11).** Claude Fable 5.2 may be used for bounded audits and for design consultation on
consequential decisions, under a protocol:
- The owner logs a prior and criterion weights privately before any run.
- Each run starts in a fresh session; option labels are neutral and their order rotates.
- A red-team run follows, and a cross-family check is mandatory for one-way-door decisions.
- The owner decides.

Limits:
- Models never produce data, outcome-bearing analyses or pre-registration text; the owner writes and the model
  critiques.
- Packets never contain 2023–2025 outcomes, licensed rows, local paths, or counts or hashes of real data, and
  never reveal the owner's preference.
- Transcripts never enter the PIT Kernel.

G3 supersedes the routing statement in the body of open PR #6 that Fable is excluded. The bounded FIQ-07 audit
recorded in issue #10 and fixed in PR #15 is entered retroactively under G3.

**This consultation:** `CONSULT-2026-11-11-01`.
- Three blind Fable 5.2 runs (`claude-fable-5-2`, effort high), with relabelled and rotated options.
- One cross-family run (`gpt-6-astra`, effort medium).
- One Fable 5.2 red-team run against the majority proposal.
- The owner's prior and weights were recorded before run A and are not published.

Frozen packets (SHA-256 of the exact text sent; packets and responses are archived privately):

| Run | SHA-256 |
|---|---|
| A | `f67e1451588461192507e507dd51dedd854b6e21df316b02596a294aabef1c61` |
| B | `7cfd8167f28d7d79c4d4a264092bf92fb49976c87daf1a1364f2a7122af4e28d` |
| C | `c60ea9d850d9db1512302730faa3a8c92ef062f5786173cf9018c7575a5c4749` |
| X (cross-family) | `8bfb956b01b2cc29686251c294337c4c84a60e66df1f2ebdd28b07a9c982a39e` |
| R (red team) | `f52fecfb9d0002e69fd2b155218c24f5b8fb1580c62fc9d5b82a80934ccdf872` |

**Results:**
- All four design runs recommended study-specific primaries with a pre-committed gate.
- The red team found that the proposal holds with changes and listed ten changes. Nine were adopted as stated.
  The tenth, a wider gate, was adopted except for its holdout-coverage item, which was rejected (§3).
- Arguments that relied on remembered post-2022 listed-firm counts were struck.

**Deviations, disclosed:**
- Runs A–C and R ran in fresh agent sessions that loaded project instructions and a memory index, not in clean
  chats. Local transcripts show that no file was read and the owner's prior was not exposed.
- Run X ran in an agent session outside any repository, with a person-level memory, at medium effort.
- The three blind Fable runs all gave P(best) = 0.60, which is uninformative as calibration.
- Agreement within one model family is weak evidence. The cross-family run and the red team agreed on the
  conditions, and the conditions are the substance of this decision.

**Protocol fix:** future runs use a clean chat with no project instructions and no memory.

## 8. Unchanged and still open

**Unchanged:**
- U1 rule 2.0.0.
- The holdout boundaries.
- Charter §5 discipline.
- The capstone record.

**Still open:**
- The gate memo.
- The U2 rule version.
- The membership-cell semantics check.
- The Paper 2 surprise definition.
- The Paper 1 overlap check, which runs privately and reports PASS or BLOCKED only.
- All study registrations, source rights, acquisition and the 2026-11-30 price-source decision.
