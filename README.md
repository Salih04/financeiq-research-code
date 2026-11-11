# Study 4 S4-OPS-P0 · Lane C

**Source review and invented-only engineering preparation. P0 runtime gate remains open.**
`NO_NEW_OUTCOME_INSPECTION=true`

This packet addresses [FinanceIQ issue #14](https://github.com/Salih04/financeiq-research-code/issues/14).
The public DSA source pin is `ZhuLinsen/daily_stock_analysis@ef44660f00e08ce66dcd4dc4d2e700836c45e833`.
The versioned policy has an empty unapproved-runtime allowlist and two in-memory
capabilities for a standalone Python oracle. No DSA code was installed,
imported or run. Review used Git source blobs and static parsing. The oracle
uses no provider, database, model, real input, study output or durable sink.

## Findings at the upstream pin

| Surface | Verified behavior and consequence |
| --- | --- |
| Automatic default | The dataclass, environment parser and example all enable backtesting by default. The auto hook checks that flag, calls the service when enabled and catches exceptions. A successful process exit cannot establish that the hook was never entered. [Dataclass](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/config.py#L1293-L1302) · [Parser](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/config.py#L2285-L2291) · [Example](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/.env.example#L842-L850) · [Hook](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/main.py#L862-L885) |
| Normal, empty and error exits | The hook runs after ordinary completion, empty broker portfolio with market review off, empty configured watchlist, missing expected report, and deferred report-save failure when control reaches the final return. The all-markets-closed branch returns directly. The outer analysis exception handler returns false or re-raises without calling the hook. Portfolio resolution and initial pipeline imports sit outside that handler. Both direct returns and exceptions still require external enforcement before and during startup. [Early branches](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/main.py#L938-L1009) · [Second watchlist guard](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/main.py#L1057-L1067) · [Report failures](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/main.py#L1248-L1273) · [Final return and exception](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/main.py#L1348-L1386) |
| Manual backtest | `--backtest` dispatches directly. The four `/api/v1/backtest` endpoints are `POST /run` and `GET /results`, `/performance` and `/performance/{code}`. The handlers call the service independently of the auto hook, including reads of existing results. The service can read local forward windows, call a provider to refill gaps, persist evaluation rows and recompute summaries. Empty candidate selection can avoid those effects while leaving the entry point reachable. [CLI](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/main.py#L1891-L1907) · [Router](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/api/v1/router.py#L66-L70) · [Handlers](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/api/v1/endpoints/backtest.py#L45-L237) · [Local window](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/services/backtest_service.py#L91-L168) · [Refill](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/services/backtest_service.py#L891-L912) · [Persistence](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/services/backtest_service.py#L254-L263) |
| Decision signals | Under `/api/v1/decision-signals`, `POST /outcomes/run` independently evaluates and upserts outcomes using local anchor and forward bars. `GET /outcomes`, `/outcomes/stats`, `/{signal_id}/outcomes` and `/stocks/{stock_code}/review` disclose evaluation data or review summaries. `GET/PUT /{signal_id}/feedback` read or write feedback. `POST /reassess` is a separate persisted-history replay path. Deny the entire router, including ancillary signal endpoints, in the sealed worker. [Run, reads and reassess](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/api/v1/endpoints/decision_signals.py#L211-L394) · [Per-signal outcomes and feedback](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/api/v1/endpoints/decision_signals.py#L456-L533) · [Writes](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/services/decision_signal_outcome_service.py#L148-L185) · [Local forward read](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/services/decision_signal_outcome_service.py#L551-L595) |
| Skill-opinion evaluator and samples | `SkillOpinionOutcomeService.run_outcomes` enumerates missing or pending sample/horizon keys, reads local forward windows, persists outcomes and can advance retry markers on errors. The analysis pipeline has a separate post-history-save hook that persists **samples**. The production-source reference scan found no direct caller of the skill outcome writer and no explicit registration of it in the inspected CLI/API schedulers. The two service modules importing from the evaluator service import constants. This finding is scoped to the pinned source search and its reviewed entry points. [Evaluation and retry](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/services/skill_opinion_outcome_service.py#L39-L191) · [Pipeline trigger](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/core/pipeline.py#L1886-L1913) · [Sample persistence](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/core/pipeline.py#L2850-L2888) |
| Skill weights, memory and tools | Skill aggregation reads stored performance through the weight and performance services. `AGENT_SKILL_AUTOWEIGHT` falls back to `AGENT_STRATEGY_AUTOWEIGHT` with default true. The aggregator also returns true when config lookup raises. Agent memory can read decision-signal review and backtest summaries when enabled. The default registry separately registers backtest summary tools. Removing a write path leaves these reads and feedback into scores reachable unless independently removed or denied. [Config aliases](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/config.py#L2131-L2135) · [Aggregation](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/agent/skills/aggregator.py#L206-L266) · [Weight read](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/services/skill_opinion_weight_service.py#L48-L69) · [Repository read](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/services/skill_opinion_performance_service.py#L35-L70) · [Memory](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/agent/memory.py#L182-L209) · [Calibration](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/agent/memory.py#L273-L329) · [Tool registry](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/agent/factory.py#L350-L376) |
| Startup and mutable settings | `--serve` can fall through to startup analysis. `--serve-only` disables the scheduler's immediate analysis on this launch path and can restore persisted schedules. `--webui(-only)` aliases and `WEBUI_ENABLED` can activate Web mode. A serve startup failure can fall through with `--serve`, while `--serve-only` returns an error. API lifespan can reconcile scheduling and starts stock-index refresh and AkShare cache warmup. `PUT /api/v1/system/config` can persist and reload settings. The manual scheduler run-now route calls the watchdog without checking schedule-enabled in `run_now`. [Web startup and fallthrough](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/main.py#L1801-L1889) · [One-shot](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/main.py#L2098-L2127) · [Lifespan](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/api/app.py#L239-L297) · [Warmup thread](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/services/name_to_code_resolver.py#L360-L374) · [Config update](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/api/v1/endpoints/system_config.py#L364-L388) · [Run now](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/services/runtime_scheduler.py#L766-L790) |
| Background work and alternate launchers | The CLI scheduler reaches full analysis and can register an immediate alert worker. The Web runtime can start a scheduler thread and a watchdog child process, and can also register event-monitor callbacks. The API analysis queue can dispatch its own analysis or generic background work. Stock-index refresh can occur on CLI analysis independently of Web startup. Direct `server.py`, container entrypoint and upstream scheduled or manual workflows are additional execution surfaces to exclude. [CLI scheduler](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/main.py#L2045-L2096) · [Scheduled analysis wrapper](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/main.py#L1389-L1406) · [Worker process](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/services/runtime_scheduler.py#L62-L87) · [Background registration](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/services/runtime_scheduler.py#L642-L750) · [Queue](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/src/services/task_queue.py#L510-L598) · [CLI refresh](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/main.py#L625-L640) · [Server](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/server.py#L29-L58) · [Entrypoint](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/docker/entrypoint.sh#L85-L92) · [Workflow](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ef44660f00e08ce66dcd4dc4d2e700836c45e833/.github/workflows/00-daily-analysis.yml#L1-L13) |

Twenty-one targeted assertions on the pinned source passed using Python AST or
literal checks on Git blobs. The search for the skill-opinion writer included
`main.py`, `server.py`, `webui.py`, Python source under `src`, `api`, `bot`
and `scripts`, desktop launcher sources, container files and workflows.
Literal reference search cannot establish absence of dynamic imports, indirect
aliases, packaged plugins or deployment-specific jobs. Source data assets,
database files, evaluation fixtures and executable upstream entry points were
outside the inspection.

## Proposed external enforcement

The Study 4 draft specifies a pinned DSA input path, an input availability
cutoff and sealed output custody. The following is a candidate engineering
boundary. The exact licensed operations, approved fork and production grants
remain unset. [Study 4 draft](https://github.com/Salih04/financeiq-research-code/blob/5b1030ad9e6760af22f5f8fc0cf36a355b9f6df8/docs/study4/OSF_PREREGISTRATION_DRAFT.md#L53-L107)

1. **Preflight before loading any DSA code.** An external supervisor verifies
   a signed manifest binding upstream and fork commits, build/runtime and
   dependency digests, executable and exact argument vector, normalized
   effective config, broker schema, output schema, isolation rules and
   clock/cutoff policy. Build a minimal sealed worker with one audited
   one-shot adapter. Start from an empty environment, explicit read-only
   config, clean working directory and exact file-descriptor set. Reject
   duplicate or unknown config, aliases that disagree, unexpected mounts,
   open descriptors, unapproved identities, startup schedule, network or
   process capabilities, hash drift and invalid clock. Disable dynamic
   config reload and fallback. A missing, unverifiable or stale preflight
   aborts before import. The current manifest grants no real entry point.
2. **Remove alternate execution and feedback paths.** At the eventual fork,
   exclude stock Web/API/UI, bot/desktop/hosted launchers, scheduler and
   worker registration, history replay, backtest/evaluator registration
   and automatic tuning. Use an explicit tool registry and validate its
   dispatch targets, including hidden/aliased tools. Freeze and verify
   effective `BACKTEST_ENABLED=false`, `AGENT_MEMORY_ENABLED=false`,
   `AGENT_SKILL_AUTOWEIGHT=false` and the legacy autoweight alias false.
   Freeze `WEBUI_ENABLED`, `SCHEDULE_ENABLED`, `RUN_IMMEDIATELY`,
   `SCHEDULE_RUN_IMMEDIATELY`, `AGENT_EVENT_MONITOR_ENABLED` and
   `STOCK_INDEX_REMOTE_UPDATE_ENABLED` false. Exclude all scheduler override
   variables, paid search and unattended cache refresh. These are
   defense-in-depth settings. The audited adapter must explicitly invoke
   the intended computation and fail when config, tool setup or dependency
   initialization fails. Stock CLI, even with `--dry-run`, is outside the
   allowlist.
3. **Enforce capability separation outside the worker.** Use a disposable
   isolated execution environment with a read-only minimal image, bounded
   private scratch, no network interface or sockets (including loopback,
   Unix sockets and inherited descriptors), no subprocess or external
   scheduler access and no provider credentials. Strip host mounts, home,
   shared caches, DBs and SQLite sidecars, browser and container sockets,
   secrets, archive paths and outcome/benchmark stores. Deny all
   unlisted opens, launches and dispatches. Start every occurrence fresh,
   with no persistent DSA analysis history, evaluator tables, feedback,
   performance, prior score store or repo credentials. Give each trusted
   supervisor, input custodian and output custodian a separate identity.
   The investigator and scoring worker get no read authority on the
   output or outcome stores. The custodian must be unable to return data
   or previous outcomes to the worker.
4. **Bind inputs to one occurrence.** For any future separately authorized
   profile, use a single immutable per-occurrence input snapshot supplied
   over a dedicated read-only channel. A separate trusted collector, if
   needed, is limited to exact provider operation, verified origin,
   symbol set, request window, field list, source-time and availability
   rules. It receives no predictions, study history or outcome-store
   access. Reject redirects, proxy overrides, user URLs, fallback to
   other providers or paid news, malformed/missing timestamps, later
   revisions that cannot be attested at the cutoff, unknown response
   fields and mixed or future timestamps. Check the request before any
   access and the response before making it visible. Pin the snapshot,
   subject set and cutoff together, with no arbitrary date queries or
   second fetch after worker start. Current-day cutoff alone allows an
   evaluator to compare older predictions with later bars inside that
   cutoff. Eliminate the evaluator and prior predictions and expose
   only the current occurrence snapshot. Show that a future collector
   or adapter preserves the frozen treatment before enabling any real
   grant. The Yahoo access path and compatibility remain unproven.
5. **Seal once after verification.** A dedicated output channel accepts
   one bounded, typed score/action candidate per approved subject, with
   supervisor-derived provenance. It carries no free text, rankings,
   outcomes, diagnostic payloads or historical state. Raw approved inputs
   and required metadata go directly to separate private custody.
   Suppress payloads from stdout/stderr, traces, prompts in diagnostics,
   UI, reports, caches, crash dumps and telemetry. The custodian stages
   output without readback, checks expected occurrence, identity,
   counts, schema, final process status and trusted guard verdict, then
   atomically commits at most once per occurrence. Keep output invisible
   until the registered opening. A retry cannot publish twice or rerun
   an elapsed occurrence. Ordinary empty, missing-input, no-report or
   crash paths drop the candidate. Future permitted miss accounting
   would use only the registered sealed mechanism. No study logging is
   implemented here.
6. **Latch a violation at the trusted boundary.** A forbidden attempt,
   unavailable or untrustworthy enforcement signal, unexpected process or
   inconsistent verdict invalidates the occurrence even if application
   code catches an exception and exits successfully. Kill the worker and
   descendants, discard staged outputs, revoke occurrence capabilities
   and hold subsequent execution pending owner review. A later clean run
   cannot erase that latch. Carry the latch across restarts and handle
   timeout, cancellation, duplicate dispatch and failures between stage
   and commit. The preparation oracle models an in-memory per-occurrence
   latch. Durable, campaign-wide enforcement needs a separate implementation.

## Versioned allowlist and invented oracle

[`allowlist.v1.json`](allowlist.v1.json) binds the source-review pin and
declares deny-and-latch for unknown operations. The oracle pins its byte digest.
`unapproved_runtime` has no grants and refuses startup. `invented_oracle`
allows one exact `fixture.read` and one `seal.stage` in that order for the
same synthetic slot. Preflight requires an exact invented launch observation.
An independent supervisor would have to obtain launch observations from the
execution boundary in a real implementation. The harness supplies invented
bytes for these observations. No DSA interface or OS capability is granted by
this policy.

Run from this directory with the Python standard library.

```sh
python3 -I -B -c 'import runpy, sys; sys.path.insert(0, "."); runpy.run_path("test_p0_oracle.py", run_name="__main__")' -v
```

Ten test groups passed with zero skips. The 24-slot liveness control produced
21 in-memory seal intents and three misses (empty queue, no report, and crash
after staging). The tests check manifest and launch drift, startup inactivity,
modeled hook injection across analysis exits, CLI/API/worker/service attempts,
local and remote reads, writes, feedback paths, malformed inputs, duplicate
operations and caught denials after staging. The oracle checks zero modeled
forbidden effects and drops any staged intent on a violation. These probes
send invented capability labels through one reference gate. They do not invoke
or monkeypatch upstream functions, dispatch HTTP requests, test a real
scheduler, observe actual sockets or exercise a durable store.

## Gaps that keep P0 open

- **Fork, entry point and dependencies.** The public upstream SHA is evidence
  for this source review. Freeze the eventual fork, complete its import-time
  and transitive dependency review, enumerate its jobs and loaded tools and
  verify build/runtime identity. Check effective config before import and after
  initialization, including dotenv and mutable settings paths. Dynamic
  dispatch, installed plugins, packaged launchers and native libraries remain
  unproven. Re-review and re-run synthetic negatives on any drift.
- **Isolation and data semantics.** Even a correctly limited network does not
  stop reads of cached local forward windows. A valid timestamp and approved
  host cannot establish when a field became knowable or whether it was
  restated. Side channels through a host, provider or model adapter, local
  state and covert payloads in an otherwise valid score/action remain
  residual risks. Custodian separation, denial of all investigator reads
  and no feedback channel need independent verification. Provider rights,
  exact operation and field semantics, payload availability proof and
  treatment equivalence are unresolved.
- **Runtime acceptance, after separate authorization.** Use an isolated
  invented-only environment with fake providers, stores and outputs.
  Instrument both forbidden attempts and durable side effects independently
  of DSA. Exercise cold and warm start, cache warmup, every CLI/API/worker
  path, empty and populated invented histories, every normal/miss/error
  branch, retry markers, timeout and process-tree cleanup, commit races and
  restart behavior. Use canaries for local forward reads, refill, attempted
  egress, historic caches, summary writes/reads, tuning and dashboard access.
  Require zero forbidden attempts during clean positive cases, zero
  forbidden effects in all cases, invalidation even on swallowed denials,
  and a 20+ invented-slot liveness run. Check that an injected monitor
  failure and deliberate forbidden dispatch are both detected. Obtain
  independent review of exact artifact hashes and controls before treating
  P0 as implemented. Study 4's existing authorization, rights and
  registration gates continue to govern real work.
