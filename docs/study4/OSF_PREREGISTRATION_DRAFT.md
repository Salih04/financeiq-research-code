# OSF preregistration draft — Study 4

**v0.1 · 2026-11-10 · DRAFT · NOT REGISTERED**

Research support only; not investment advice. **NOT SUBMITTED.** Registration
identifier, URL, DOI and effective timestamp are **UNSET**. This is the
BEFORE record under [STUDY_RECORD_TEMPLATE.md](../process/STUDY_RECORD_TEMPLATE.md).
Design and owner decisions S4-1 to S4-3 are in [DESIGN_CARD.md](DESIGN_CARD.md).
Nothing here authorizes installation, logging, data access or analysis before
registration. Fields marked **UNSET** are fixed at freeze, before registration.

## BEFORE — proposed registration fields

- **Study ID / version / date:** `study4-llm-agent-forward` / v0.1 draft /
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
  - H6: the IC difference versus each benchmark (B1, B2) is > 0. B0 (zero) is
    H1 itself; B1 and B2 enter as one hypothesis using the smaller of the two
    differences.
  - H7: “buy” recommendations have a higher mean primary outcome than “sell”
    recommendations (two-sided).

### Estimand

- **Population:** U1 2.0.0 members, the charter's quarterly BIST 100 rule.
  FinanceIQ applies it to Kernel membership evidence at the formation in force
  on each trading day t of the logging period.
- **Primary outcome:** for each stock i on day t,
  R(i,t) = TR(i; close t+1 → close t+1+5) − TR(XU100 total-return index;
  same dates).
- **Summary:** the time-series mean of daily cross-sectional rank ICs.

### Universe, data and cutoffs

- **Agent inputs (S4-1):**
  - DSA fetches Yahoo Finance data through its pinned yfinance path;
    paid news search is off.
  - Inputs are hashed per run; they are part of the treatment and never
    reported as data.
- **Logged set:** the BIST 100 list in force at run time, from the latest
  owner-held DataStore 3184 quarter (S4-2). The owner downloads each new
  quarter manually; it is never scripted. Rows outside U1 are dropped at the
  opening.
- **Outcome data:** daily total returns and the XU100 total-return index from
  LSEG (primary). DataStore is the cross-check and fallback. Price source,
  snapshot ID and hash are fixed at opening. Yahoo is never an outcome source.
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
  outcome. A day counts only if it has at least 50 such stocks.
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
  through close t, with the same IC method and a HAC test on the daily IC
  difference.
  - B0: zero.
  - B1: 5-day reversal, −r(t−5, t).
  - B2: MA(5/20) trend sign.
- **Recommendation contrast:** the mean primary outcome of buy minus sell
  stock-days. The standard error is clustered by date.
- **Multiplicity:** H1 is the single primary test. H2–H7 are one Holm family
  at α = 0.05. Every computed configuration enters the experiment ledger, and
  N is reported.
- **Missing data:**
  - Missing runs, scores or outcomes are not imputed or backfilled; they leave
    that stock-day out.
  - Delisting and suspension returns follow the adopted price-source rules; a
    missing return stays null and is reported.
  - Report coverage as valid stock-days divided by planned stock-days.
- **Exclusions:** engineering dry-run outputs from before registration;
  nothing else.

### Stopping rule

- Logging stops after 12 calendar months; then there is one confirmatory
  opening (OD-2 = B). There are no interim looks, and the only monitoring is
  liveness.
- If coverage falls below 80%, the study is still analysed but reported as
  **coverage-compromised**.
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

1. Literature check confirms the contribution.
2. The owner chooses the model, and the system freezes (all UNSET hashes filled).
3. Simulation-based power replaces the approximation, and a sourced cost
   figure replaces the default.
4. The engineering dry run passes on format only; its outputs are discarded.
5. Owner registration on OSF. Logging starts on the next trading day.

## AFTER — deliberately unfilled
