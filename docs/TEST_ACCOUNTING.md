# Public/private test accounting — 2026-11-07

Code: [https://github.com/Salih04/financeiq-research-code](https://github.com/Salih04/financeiq-research-code). The public and private scopes are different, explicitly listed
below; none of the private tests is claimed as passed by public CI.

| Suite | Public collected/executed requirement | Private archive authority |
| --- | ---: | --- |
| PIT synthetic consumer | 16 / 16, zero skips | Existing approved suite; unchanged source and fixtures |
| Research-core synthetic | 21 / 21, zero skips | Existing approved suite; unchanged source |
| FIQ-07 membership-evidence invented synthetic consumer (authorized 2026-11-09) | 18 / 18, zero skips | New public invented-only suite; does not change prior 16+21 |
| FIQ-07 development-window wire-shape invented tests | 8 / 8, zero skips | No real Kernel round-trip or approved new source-year profile |
| Root `tests/` | 0; entire suite private-only | 1456 collected in the dated approved baseline; 1441 Linux executions + 15 governed deselections |
| Backend `backend/tests/` | 0; entire suite private-only | 916 collected/executed in the dated approved hosted baseline |
| Frontend E2E | NOT RUN | Private local runbook; no authoritative collected count: UNSET |
| Data validation | NOT RUN | Private archive only; no dataset exported |
| Experiments / scientific evaluations | NOT RUN | Require separate scientific execution authority; never public CI |

The root 1456 count is historical native evidence; the hosted backend 916 count
is environment-qualified. Neither is a fresh full-suite execution for this export.
The private archive's `docs/VERIFICATION_BASELINE.md`, `.github/ci-deselect.txt`,
`.github/ci-test-gates.json` and existing CI are unchanged. No baseline is reduced.
Even potentially portable legacy tests are conservatively private-only until their
fixtures and imports receive a separate public-safety review. No derived public
fixture is introduced. FO-4 gates any such future proposal.

## Live pinned-base software evidence

The existing private CI [run 42413434907](https://github.com/Salih04/capstone-financeIQ/actions/runs/42413434907)
succeeded at `c2c328824dc57b6e892205322eeb5a051f50f1ff`. Its software-only ledger/JUnit count artifacts report:
root 1456 collected, 1441 passed, 15 governed deselections, zero skips or failures;
backend 916 collected and passed, zero deselections, skips or failures.
This was an existing run, not a fresh full-suite execution by the export task.
The complete native machine-of-record 1456-test run was not repeated: UNSET.

## Complete private-only test-module list

The second column counts AST test-function declarations, NOT parametrized collected
cases. The suite counts above come from the existing baseline, not AST estimates.
Source OIDs for every excluded module are pinned in the private export manifest.

| Private-only module | Static declarations |
| --- | ---: |
| `tests/test_alternative_targets.py` | 7 |
| `tests/test_artifact_registry.py` | 19 |
| `tests/test_autopsy_claim_safety.py` | 3 |
| `tests/test_benchmark_collector.py` | 6 |
| `tests/test_calibration_bench.py` | 7 |
| `tests/test_cell_provenance.py` | 62 |
| `tests/test_contamination_lab.py` | 36 |
| `tests/test_contract_coverage.py` | 3 |
| `tests/test_contract_evidence_state.py` | 2 |
| `tests/test_corrected_2024_balance.py` | 6 |
| `tests/test_corrected_yearly_ingestion.py` | 9 |
| `tests/test_courtroom_claim_safety.py` | 3 |
| `tests/test_disagreement_atlas.py` | 7 |
| `tests/test_dissent_ledger_claim_safety.py` | 3 |
| `tests/test_excess_basis.py` | 206 |
| `tests/test_feature_dimensionality.py` | 18 |
| `tests/test_feature_passports.py` | 2 |
| `tests/test_free_valuation.py` | 9 |
| `tests/test_friction_claim_safety.py` | 3 |
| `tests/test_friction_sim.py` | 8 |
| `tests/test_influence_map.py` | 10 |
| `tests/test_limitations_register.py` | 29 |
| `tests/test_manual_ingest.py` | 16 |
| `tests/test_missingness_sensitivity.py` | 140 |
| `tests/test_pipeline_guards.py` | 4 |
| `tests/test_pit_guard.py` | 13 |
| `tests/test_pit_prices.py` | 7 |
| `tests/test_placebo_lab.py` | 20 |
| `tests/test_preregistered_2026.py` | 53 |
| `tests/test_rank_stability.py` | 22 |
| `tests/test_regime_lens.py` | 6 |
| `tests/test_research_agent.py` | 16 |
| `tests/test_research_intents.py` | 23 |
| `tests/test_serving_eval.py` | 16 |
| `tests/test_shares_expansion.py` | 9 |
| `tests/test_significance.py` | 14 |
| `tests/test_thesis_positive_control.py` | 50 |
| `tests/test_thesis_stage1b_implementation.py` | 73 |
| `tests/test_thesis_stage1b_registration.py` | 35 |
| `tests/test_thesis_stage2_implementation.py` | 26 |
| `tests/test_thesis_stage2_registration.py` | 25 |
| `tests/test_thesis_stage3_implementation.py` | 25 |
| `tests/test_thesis_stage3_r2_implementation.py` | 19 |
| `tests/test_thesis_stage3_r2_registration.py` | 9 |
| `tests/test_thesis_stage3_registration.py` | 44 |
| `tests/test_valuation_integration.py` | 8 |
| `tests/test_yearly_extraction.py` | 8 |
| `backend/tests/test_analyst_verdicts.py` | 5 |
| `backend/tests/test_auth_hardening.py` | 19 |
| `backend/tests/test_calibration_api.py` | 22 |
| `backend/tests/test_confidence_contract.py` | 1 |
| `backend/tests/test_config.py` | 3 |
| `backend/tests/test_courtroom_service.py` | 7 |
| `backend/tests/test_evidence_status.py` | 5 |
| `backend/tests/test_feature_passports_api.py` | 1 |
| `backend/tests/test_forecasting_api_contract.py` | 4 |
| `backend/tests/test_forecasting_csv_service.py` | 4 |
| `backend/tests/test_forecasting_inference.py` | 5 |
| `backend/tests/test_forecasting_partial_target.py` | 6 |
| `backend/tests/test_friction_autopsy_api.py` | 2 |
| `backend/tests/test_heatmap_missingness.py` | 11 |
| `backend/tests/test_memo_api.py` | 28 |
| `backend/tests/test_missing_value_semantics.py` | 17 |
| `backend/tests/test_postgres_integrity.py` | 7 |
| `backend/tests/test_private_mode.py` | 10 |
| `backend/tests/test_regime_context_api.py` | 2 |
| `backend/tests/test_research_agent_api.py` | 16 |
| `backend/tests/test_research_agent_grounded_artifacts.py` | 12 |
| `backend/tests/test_return_basis_api.py` | 14 |
| `backend/tests/test_security_parallel.py` | 20 |
| `backend/tests/test_security_remediation.py` | 12 |
| `backend/tests/test_shared_record_authz.py` | 11 |
| `backend/tests/test_significance_api.py` | 3 |
| `backend/tests/test_skeptic_service.py` | 10 |
| `backend/tests/test_supabase_jwks.py` | 9 |

Total private-only modules: 75; static declarations: 1405.
