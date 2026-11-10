# Study 4 candidate — forward evaluation of an LLM stock-research agent on BIST

2026-11-10, Europe/Zurich · **DESIGN · OWNER-APPROVED CANDIDATE · NOT REGISTERED**.
Research support only; not investment advice. This card installs, runs and
acquires nothing and grants no outcome access. Registration fields:
[OSF_PREREGISTRATION_DRAFT.md](OSF_PREREGISTRATION_DRAFT.md).

## Question

Does the daily output of a widely used open-source LLM stock-research agent
carry out-of-sample information about subsequent BIST excess returns? The test
is forward-only, from a configuration frozen before the first logged day.

## Why forward-only

- A language model whose training data covers an evaluation period may already
  know its outcomes (Glasserman & Lin, 2023, look-ahead bias in GPT-based
  return predictions). A historical backtest of the agent on 2017–2025 would
  therefore tend to show a spurious edge. Charter §5 rule 8 and OD-5 = B treat
  such use as exploratory at most. **This study runs no historical backtest of
  the agent.**
- System under test: DSA, `ZhuLinsen/daily_stock_analysis` (MIT licence). Its
  paper (Zhu & Shi, arXiv:2608.26990, 2026) reports software-contract tests. In
  its own words, the evidence does not establish forecasting accuracy or
  investment returns. Stars and forks measure use, not validity.
- Contribution candidate: a pre-registered, point-in-time, forward test in an
  emerging market, with simple benchmarks and a pinned agent. Novelty is
  **unverified**. Before registration, check the literature, starting with
  Lopez-Lira & Tang (2023, “Can ChatGPT forecast stock price movements?”),
  Glasserman & Lin (2023), and recent long-horizon and live evaluations of LLM
  trading strategies.

## Owner decisions (2026-11-10)

Recorded from the owner's explicit chat approval, 2026-11-10.

| ID | Decision |
| --- | --- |
| S4-1 | **Yahoo Finance is allowed only as the agent's input.** Access is through DSA's yfinance path with `.IS` symbols. It is part of the system under test, and results describe the agent as configured, including those inputs. No Yahoo value is used as an outcome, benchmark input, price, return or reported number. Outcomes use the adopted price source: LSEG primary, DataStore cross-check and fallback. Yahoo stays development-only everywhere else. |
| S4-2 | **DataStore 3184 rights cover 2017 onward, including annual archives published later, until research end**, on the 2026-10-29 FINAL terms. The authority is the Kernel governance record: [financeiq-pit-kernel PR #36](https://github.com/Salih04/financeiq-pit-kernel/pull/36). **Study 4 cannot register before PR #36 merges.** Logging builds its daily list from the owner's manually downloaded 3184 files. At the opening, U1 needs Kernel custody of the 2026–2027 files, which is gated by the separate Kernel policy succession. Recorded rights are not an executable custody grant. |
| S4-3 | **DSA lives outside FinanceIQ and the PIT Kernel.** Its code, dependencies and run environment sit in a separate private environment. FinanceIQ receives only the sealed log. Charter §7 and the repository rules (no acquisition code, no quarantined news API) are unchanged. |

Constraints that follow from existing rules, not new decisions: no paid API,
so the model runs locally through Ollama and DSA's paid news search stays
disabled. Exploratory peeking at logged output is forbidden (charter §5
rule 7; OD-2 = B: one confirmatory opening).

## System under test (frozen before the first logged day)

- A DSA fork pinned to one commit, plus a BIST market path (yfinance `.IS`
  symbols). The diff is recorded and hashed.
- A local open-weights model served by Ollama, pinned by model digest. Its
  release date and stated training cutoff are recorded, and both must precede
  the first logged day. The model is chosen before registration: it must fit
  the owner's machine and handle Turkish and English.
- Fixed strategy set, prompts and configuration (hashed); deterministic
  decoding (temperature 0 or a fixed seed); a fixed daily run time. News
  search is off.
- Any later change starts a **new arm** with its own registration and clock.
  The original arm keeps running unchanged.

## Sealed logging protocol

- One run each BIST trading day at 20:00 Europe/Istanbul, after the close and
  before the next open.
- **Logged set, sealed before each run.** `LoggedSet_t` is a deliberate
  superset of the expected U1 for day t. It is the union of:
  - (a) every code with a tier cell in the current quarter of the latest
    owner-held 3184 workbook;
  - (b) every code in Borsa Istanbul's announced composition for the next
    index period, from the announcement date until that period starts. The
    owner transcribes it manually from the public announcement and records
    the announcement reference and date;
  - (c) every code removed at the last period change, kept for one quarter.

  The list, its source references and its hash are written before the run
  and never edited. Codes are logged as published; renames are resolved at
  the opening through KER-10 `BOUND LISTING`.
- **Containment is checked, not assumed.** At the opening, U1 2.0.0 comes from
  Kernel membership evidence. Every U1 member-day falls into one of three
  groups:
  - logged with a valid score;
  - a **list miss**: absent from `LoggedSet_t`;
  - a **run miss**: logged but without a valid score (no `.IS` symbol, input
    failure or agent failure).

  Both kinds of miss stay **missing** and are never backfilled. They are
  reported separately, and the draft's coverage and sensitivity rules apply.
  Non-U1 rows are dropped.
- Each stock-day record holds:
  - trading date and code;
  - the agent's action and 0–100 score, with the exact output fields pinned at freeze;
  - any price levels and the raw output text;
  - the input-data hash, config hash and model digest;
  - run start and end times in UTC.

  The raw input payloads of each run are archived privately, so post-close
  data revisions can be audited. A hash alone cannot show what the agent saw.
- Storage is append-only JSONL in owner-private storage, never Git. Each day
  gets a hash-chained root, and only that root is sent to a free external
  timestamp service (for example OpenTimestamps). The root reveals nothing.
- **Blinding.** No one reads logged outputs or computes performance before the
  single confirmatory opening. A monitor checks liveness only: the run
  finished, and the row count equals the logged-set size. Failed or missing
  runs are recorded as missing and **never backfilled**.

## Evaluation outline

Full plan: [OSF_PREREGISTRATION_DRAFT.md](OSF_PREREGISTRATION_DRAFT.md).

| Item | Choice |
| --- | --- |
| Primary outcome | Total return from the close of t+1 to the close of t+1+h, with h = 5 trading days, in excess of the XU100 total-return index over the same dates. Entry is conservative because the signal arrives after the close of t. One index return is subtracted from every stock on a date, so the rank IC equals the IC on raw total returns; the excess definition matters for H5 and H7. |
| Outcome source | Fixed at registration by rule: the project's adopted primary daily-price source on that date. That is LSEG if obtained by 2026-11-30, otherwise DataStore (daily-price source decision). Exact products, rights record and PIT snapshot design must exist before registration. There is no switch afterwards; the other source is a pre-registered sensitivity only. 3184 is a membership product and gives no price rights. |
| Primary metric | Mean daily cross-sectional Spearman rank IC between the score and the primary outcome. One-sided test of mean IC > 0 at α = 0.05 with Newey–West standard errors (lag 5). |
| Secondary (Holm) | IC at h = 1 and h = 20; close(t)→close(t+5) information version; top-minus-bottom quintile excess return net of a fixed cost; H6 against B1 and B2 by intersection-union, p = max of the two paired p-values; buy-minus-sell mean outcome. |
| Benchmarks | Zero (market); 5-day reversal (−r[t−5, t]); MA(5/20) trend sign. All are computed from the adopted price source using prices through the close of t. |
| Duration | 12 months of logging, about 250 trading days, then one opening. |

**Power (approximate; to be replaced by simulation before registration).**
With about 100 names, the daily IC standard error is about 0.10. With 5-day
overlap and cross-sectional dependence, the standard error of the mean IC over
250 days is about 0.012–0.016. That gives 80% one-sided power only for a true
mean IC of about 0.03–0.04 or more, so a smaller real effect will likely be
missed. The registration states this.

## Order of work and prerequisites

0. Kernel PR #36 (3184 scope) merges. The outcome source has its exact
   products, a Kernel rights record and a PIT snapshot design (see outcome
   source above).
1. Literature check for novelty, then the owner chooses the model.
2. Freeze the DSA commit, the BIST path diff, the model digest and the
   prompt/config hashes. Run an engineering dry run on a few days; its outputs
   are checked for format only, discarded and excluded.
3. The owner registers the pre-registration on OSF.
4. Logging starts on the next trading day after registration. That day opens
   Study 4's forward holdout.
5. Before the opening: OD-2/OD-3 cross-study exposure and clean-forward
   status checks. At the opening: outcome data from the registered source,
   and U1 membership from the Kernel (2026–2027 custody needs the Kernel
   policy succession). Neither is needed to start logging.

## Risks and limits

- Yahoo outages or symbol errors cause missing days. They are logged and never
  backfilled, and Yahoo's data quality is part of the treatment.
- The owner's machine must be awake at run time. Missing days count against
  the coverage threshold in the draft.
- A local model may be weaker than a commercial API. Claims cover this pinned
  configuration only.
- Prompt-injection exposure is reduced (news off, strategy files pinned), not
  eliminated.
- Not on the critical path: Kernel PR #31 → real 2022 data → U1 → Papers 1–2
  keep priority. Owner setup takes about one day; after that the run is
  automatic.
