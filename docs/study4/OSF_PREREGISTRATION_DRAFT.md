# OSF preregistration draft — Study 4

**v0.2 · 2026-11-10 · DRAFT · NOT REGISTERED** (v0.2 resolves review findings B1–B4 on PR #8)

Research support only; not investment advice. **NOT SUBMITTED.** Registration
identifier, URL, DOI and effective timestamp are **UNSET**. This is the
BEFORE record under [STUDY_RECORD_TEMPLATE.md](../process/STUDY_RECORD_TEMPLATE.md).
Design and owner decisions S4-1 to S4-3 are in [DESIGN_CARD.md](DESIGN_CARD.md).
Nothing here authorizes installation, logging, data access or analysis before
registration. Fields marked **UNSET** are fixed at freeze, before registration.

## BEFORE — proposed registration fields

- **Study ID / version / date:** `study4-llm-agent-forward` / v0.2 draft /
  registration timestamp UNSET.
- **Authors:** UNSET (owner).

### Research question and hypotheses

Does the pinned DSA agent's daily 0–100 score rank BIST U1 stocks by
subsequent excess return, out of sample and forward in time?

- **H1 (primary, one-sided):** the mean daily cross-sectional Spearman rank
  correlation (IC) between the score on day t and the primary outcome is
  greater than zero.
- **H2–H7 (secondary, Holm family of six, one-sided unless stated):**
  - H2: IC > 0 at h = 1.
  - H3: IC > 0 at h = 20.
  - H4: IC > 0 for the information version, close(t)→close(t+5).
  - H5: the top-minus-bottom score-quintile portfolio has positive mean excess
    return net of costs.
  - H6: the agent's IC exceeds **both** B1 and B2. This is an
    intersection-union test: one paired one-sided test per benchmark, each on
    the daily series ΔIC = IC_agent − IC_benchmark, with p_H6 = max(p_B1,
    p_B2). H6 is supported only if both differences are. B0 (zero) is H1
    itself.
  - H7: “buy” stock-days have a different mean primary outcome than “sell”
    stock-days (two-sided).

### Estimand

- **Population:** U1 2.0.0 members, the charter's quarterly BIST 100 rule.
  FinanceIQ applies it to Kernel membership evidence at the formation in force
  on each trading day t of the logging period.
- **Primary outcome:** for each stock i on day t,
  R(i,t) = TR(i; close t+1 → close t+1+5) − TR(XU100 total-return index;
  same dates).
- **Summary:** the time-series mean of daily cross-sectional rank ICs.
  Subtracting one index return per date leaves the ranks unchanged, so the
  primary IC equals the IC on raw total returns. The excess definition
  matters for H5 and H7.

### Universe, data and cutoffs

- **Agent inputs (S4-1):**
  - DSA fetches Yahoo Finance data through its pinned yfinance path;
    paid news search is off.
  - Inputs are hashed per run, and the raw input payloads are archived
    privately so post-close revisions can be audited. They are part of the
    treatment and never reported as data.
- **Logged set (sealed before each run):** `LoggedSet_t` is the union of:
  - (a) the codes in the current quarter of the latest owner-held 3184
    workbook;
  - (b) the codes in Borsa Istanbul's announced next-period composition,
    from the announcement date until the period starts;
  - (c) the codes removed at the last period change, kept for one quarter.

  3184 rights are S4-2 (Kernel PR #36). Downloads and transcription are
  manual, never scripted. The list, its source references and its hash are
  written before the run and never edited.
- **Containment at the opening:** U1 2.0.0 comes from Kernel membership
  evidence. Each U1 member-day is valid, a **list miss** (not in
  `LoggedSet_t`) or a **run miss** (logged, no valid score). Misses stay
  missing. Code renames are resolved through KER-10 `BOUND LISTING`; an
  unresolved code is a list miss. Non-U1 rows are dropped.
- **Outcome data (fixed at registration, outcome-blind):**
  - Primary source: the project's adopted primary daily-price source on the
    registration date. That is LSEG if obtained by 2026-11-30, otherwise
    DataStore, per the daily-price source decision.
  - Exact products: UNSET. For LSEG, a per-stock total-return index and the
    BIST 100 total-return index. For DataStore, a named daily equity price
    product plus corporate actions, with returns built by Kernel KER-13c.
    3184 is membership only and grants no price rights.
  - Before registration the chosen products need a Kernel rights record, a
    PIT snapshot design, a share/listing mapping (KER-10), corporate-action
    and delisting rules, TRY currency and a return formula.
  - There is no switch after registration and no per-day fallback. A missing
    primary return stays missing. The other source, if available at the
    opening, is a pre-registered sensitivity only. Yahoo is never an outcome
    source.
- **Cutoffs:**
  - The score for day t may use only information available by the run time
    (20:00 Europe/Istanbul, day t). The run timestamp and input hash are
    sealed in the log.
  - Benchmarks use prices through the close of t only.
- **Boundaries:** Study 4 uses only the forward holdout. It begins on the first
  logged trading day after OSF registration and ends after 12 calendar months.
  No development-window or 2023–2025 data are used for the agent.
- **Model cutoff (charter §5 rule 8; OD-5 = B):** the pinned model's release
  date and stated training cutoff precede the first logged day, so its
  training cannot contain the outcomes. Model, digest and cutoff: UNSET.

### Frozen system (UNSET until freeze, then hashed)

DSA upstream commit; BIST-path diff hash; Ollama model name and digest;
strategy, prompt and config hashes; decoding settings; run time; pinned output
fields (score and action) and the mapping of action labels to buy/hold/sell.

### Analysis plan

- **Daily IC:** a Spearman correlation across U1 stocks with a valid score and
  outcome, with average ranks for ties. A day counts only if it has at least
  50 such stocks. A day on which either variable has zero cross-sectional
  variance has an undefined IC; it is excluded from that series, and the
  number of such days is reported. This matters mostly for the MA(5/20) sign
  benchmark.
- **Primary test:** mean IC with a Newey–West HAC standard error, lag 5.
  One-sided α = 0.05. Report the estimate and the 90% and 95% confidence
  intervals.
- **Horizon variants:** lag = h for h = 1 and h = 20, with the same entry rule.
- **Quintile portfolio:**
  - Equal-weighted, re-formed daily; holding period 5 days with overlapping
    cohorts (Jegadeesh–Titman averaging).
  - Cost: a fixed round-trip cost (UNSET; default 0.40%, to be replaced by a
    sourced BIST commission-plus-spread estimate before registration).
  - HAC test on the daily series.
- **Benchmarks:** each is computed from the outcome source using prices
  through close t, with the same IC method.
  - B0: zero.
  - B1: 5-day reversal, −r(t−5, t).
  - B2: MA(5/20) trend sign.
- **H6 mechanics:**
  - For each of B1 and B2, take the dates on which both the agent IC and that
    benchmark's IC are defined, and use the daily ΔIC series on that
    intersection.
  - Test each series with a one-sided Newey–West HAC t-test, lag 5.
  - p_H6 = max(p_B1, p_B2), entered once into Holm. This intersection-union
    test is valid at level α without further adjustment.
  - Both component estimates and their date counts are reported.
- **Recommendation contrast (H7):** the mean primary outcome of buy minus
  sell stock-days, pooled over the window. The standard error is clustered by
  date. Dates with only one group contribute only to that group's mean. With
  fewer than 30 buy or 30 sell stock-days in total, H7 is **not estimable**
  and enters Holm with p = 1.
- **Multiplicity:** H1 is the single primary test. H2–H7 are one Holm family
  at α = 0.05. Every computed configuration enters the experiment ledger, and
  N is reported.
- **Missing data:**
  - Missing runs, scores or outcomes are not imputed or backfilled; they leave
    that stock-day out.
  - Delisting and suspension returns follow the adopted price-source rules; a
    missing return stays null and is reported.
  - Coverage denominator: U1 member-days. Report list misses, run misses and
    missing outcomes separately.
  - Sensitivity, pre-registered: H1 restricted to stock-quarters with no list
    or run miss.
- **Exclusions:** engineering dry-run outputs from before registration;
  nothing else.

### Stopping rule

- Logging stops after 12 calendar months; then there is one confirmatory
  opening (OD-2 = B). There are no interim looks, and the only monitoring is
  liveness.
- The study is still analysed but reported as **coverage-compromised** if
  either condition holds:
  - list misses exceed 1% of U1 member-days (this is selection, not noise);
  - valid coverage falls below 80%.
- Before that, the study ends early only if the agent cannot run for 20
  consecutive trading days. It is then reported as abandoned, with its logs
  sealed and unopened, unless a new registration states otherwise.

### Null result

“No practically useful information at h = 5” if the upper bound of the
90% CI for mean IC is below 0.02. An insignificant result whose interval
includes 0.02 is **inconclusive**, not null. Approximate power: 80% for a true
mean IC of about 0.03–0.04 (simulation to replace this before registration).

### Evidence that would change the conclusion

- A positive H1 that disappears under the coverage-complete subsample, or
  under the DataStore fallback prices, is reported as fragile.
- A positive H1 that does not beat B1 and B2 (H6) is reported as no evidence
  of value beyond simple price rules.
- Replication with a second pinned model or a later forward period is required
  before any general claim about LLM agents.

### Claims

Results describe this pinned configuration on BIST over this window only. A
positive confirmatory H1 may support a predictive-ability statement for this
configuration under charter §5 rule 4 (OD-3 = B forward holdout). It never
supports investment advice.

## Required gates before registration

0. Kernel PR #36 (3184 scope) is merged. The outcome source products,
   Kernel rights record and PIT snapshot design exist (see Outcome data).
1. Literature check confirms the contribution.
2. The owner chooses the model, and the system freezes (all UNSET hashes filled).
3. Simulation-based power replaces the approximation, and a sourced cost
   figure replaces the default.
4. The engineering dry run passes on format only; its outputs are discarded.
5. Owner registration on OSF. Logging starts on the next trading day.
6. Before the opening, not before registration: OD-2/OD-3 cross-study
   exposure and clean-forward status checks.

## AFTER — deliberately unfilled
