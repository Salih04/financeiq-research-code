"""Standalone negative probes. All inputs are invented capability labels or bytes."""

from pathlib import Path
import json
import unittest

from p0_oracle import Denied, Oracle, canonical, fixture_for, seal_intent_for


POLICY = Path(__file__).with_name("allowlist.v1.json").read_bytes()
LAUNCH = {
    "entrypoint": "pure-oracle/1",
    "source_imports": False,
    "socket_access": False,
    "ambient_storage": False,
    "background_jobs": False,
    "history_feedback": False,
    "runtime_override": False,
}


def start(slot=1, *, policy=POLICY, profile="invented_oracle", launch=None):
    return Oracle(policy, profile, canonical(LAUNCH) if launch is None else launch, slot)


class OracleTests(unittest.TestCase):
    def assert_latched(self, oracle, effects=()):
        self.assertEqual(oracle.denials, 1)
        self.assertEqual(oracle.effects, effects)
        self.assertIsNone(oracle.finish())
        with self.assertRaisesRegex(Denied, "^capability denied$"):
            oracle.request("fixture.read", fixture_for(1))
        self.assertEqual(oracle.effects, effects)
        self.assertEqual(oracle.denials, 2)

    def test_profiles_and_manifest_changes_fail_closed(self):
        for profile in ("unapproved_runtime", "invented_oracle/2", "", None):
            with self.subTest(profile=profile), self.assertRaises(Denied):
                start(profile=profile)
        for policy in (b"", POLICY + b"\n", POLICY.replace(b'"fixture.read"', b'"network.open"')):
            with self.subTest(policy_length=len(policy)), self.assertRaises(Denied):
                start(policy=policy)
        manifest = json.loads(POLICY)
        self.assertEqual(manifest["profiles"]["unapproved_runtime"]["allow"], [])
        self.assertEqual(manifest["unknown"], "deny_and_latch")

    def test_launch_drift_and_noncanonical_preflight_fail_closed(self):
        for field in LAUNCH:
            for replacement in (None, True, 0, "false"):
                with self.subTest(field=field, replacement=replacement), self.assertRaises(Denied):
                    start(launch=canonical({**LAUNCH, field: replacement}))
            missing = {key: value for key, value in LAUNCH.items() if key != field}
            with self.subTest(missing=field), self.assertRaises(Denied):
                start(launch=canonical(missing))
        for launch in (
            canonical({**LAUNCH, "extra": False}),
            canonical(LAUNCH).replace(b'"socket_access":false', b'"socket_access":true,"socket_access":false'),
            b"",
        ):
            with self.subTest(length=len(launch)), self.assertRaises(Denied):
                start(launch=launch)
        for slot in (True, 0, 1000, "1"):
            with self.subTest(slot=slot), self.assertRaises(Denied):
                start(slot=slot)

    def test_startup_has_no_effects_and_no_output(self):
        oracle = start()
        self.assertIsNone(oracle.finish())
        self.assertEqual(oracle.effects, ())
        self.assertEqual(oracle.denials, 0)

    def test_twenty_four_invented_slots_stay_live_across_ordinary_misses(self):
        releases = 0
        for slot in range(1, 25):
            with self.subTest(slot=slot):
                oracle = start(slot)
                self.assertEqual(oracle.effects, ())
                if slot == 4:  # Empty input queue.
                    oracle.abort()
                    expected_effects = ()
                else:
                    self.assertEqual(oracle.request("fixture.read", fixture_for(slot)), fixture_for(slot))
                    expected_effects = ("fixture.read",)
                    if slot == 11:  # No report.
                        oracle.abort()
                    elif slot == 17:  # Crash after staging.
                        oracle.request("seal.stage", seal_intent_for(slot))
                        oracle.abort()
                        expected_effects += ("seal.stage",)
                    else:
                        oracle.request("seal.stage", seal_intent_for(slot))
                        expected_effects += ("seal.stage", "seal.release")
                release = oracle.finish()
                if slot in {4, 11, 17}:
                    self.assertIsNone(release)
                else:
                    releases += 1
                    self.assertEqual(release, seal_intent_for(slot))
                    self.assertEqual(set(json.loads(release)), {"score", "action", "provenance"})
                self.assertIsNone(oracle.finish())
                self.assertEqual(oracle.effects, expected_effects)
                self.assertEqual(oracle.denials, 0)
        self.assertEqual(releases, 21)

    def test_cli_startup_scheduler_queue_and_agent_tools_denied(self):
        for capability in (
            "exec:python main.py",
            "exec:python main.py --backtest",
            "exec:python main.py --serve",
            "exec:python main.py --serve-only",
            "exec:python main.py --webui-only",
            "exec:python main.py --schedule",
            "exec:python main.py --dry-run",
            "exec:server:app",
            "exec:docker-entrypoint",
            "exec:workflow-dispatch",
            "job:auto-backtest",
            "job:runtime-scheduler",
            "job:alert-worker",
            "job:stock-index-refresh",
            "job:akshare-warmup",
            "job:analysis-queue",
            "job:decision-signal-outcomes",
            "job:skill-opinion-outcomes",
            "service:BacktestService.run_backtest",
            "service:DecisionSignalOutcomeService.run_outcomes",
            "service:SkillOpinionOutcomeService.run_outcomes",
            "tool:get_skill_backtest_summary",
            "tool:get_strategy_backtest_summary",
            "tool:get_stock_backtest_summary",
            "feedback:memory",
            "feedback:skill-autoweight",
            "feedback:promote-strategy",
        ):
            with self.subTest(capability=capability):
                oracle = start()
                with self.assertRaises(Denied):
                    oracle.request(capability, b"")
                self.assert_latched(oracle)

    def test_injected_backtest_hook_aborts_each_analysis_exit(self):
        for exit_path, started in (
            ("empty-broker-portfolio", False),
            ("empty-configured-watchlist", False),
            ("no-report", True),
            ("report-save-failure", True),
            ("successful-analysis", True),
            ("closed-market", False),
            ("unexpected-error", True),
        ):
            with self.subTest(exit_path=exit_path):
                oracle = start()
                effects = ()
                if started:
                    oracle.request("fixture.read", fixture_for(1))
                    effects = ("fixture.read",)
                with self.assertRaises(Denied):
                    oracle.request("job:auto-backtest", b"")
                self.assert_latched(oracle, effects)

    def test_http_routes_and_path_variants_denied(self):
        for route in (
            "POST /api/v1/backtest/run",
            "GET /api/v1/backtest/results",
            "GET /api/v1/backtest/performance",
            "GET /api/v1/backtest/performance/INVENTED",
            "POST /api/v1/decision-signals/outcomes/run",
            "GET /api/v1/decision-signals/outcomes",
            "GET /api/v1/decision-signals/outcomes/stats",
            "GET /api/v1/decision-signals/1/outcomes",
            "GET /api/v1/decision-signals/1/feedback",
            "PUT /api/v1/decision-signals/1/feedback",
            "GET /api/v1/decision-signals/stocks/INVENTED/review",
            "POST /api/v1/decision-signals/reassess",
            "GET /api/v1/history",
            "POST /api/v1/analysis/analyze",
            "GET /backtest",
            "GET /openapi.json",
            "POST /api/v1/system/scheduler/run-now",
            "PUT /api/v1/system/config",
            "POST /api/v1/%62acktest/run",
            "POST //api/v1/backtest/run",
            "POST /api/v1/backtest/./run?force=1",
        ):
            with self.subTest(route=route):
                oracle = start()
                with self.assertRaises(Denied):
                    oracle.request("http:" + route, b"")
                self.assert_latched(oracle)

    def test_network_storage_and_output_denied_even_if_caught_after_staging(self):
        for capability in (
            "network:provider",
            "network:post-cutoff",
            "network:older-anchor-forward-window",
            "network:benchmark",
            "network:redirect",
            "network:paid-news-fallback",
            "network:loopback",
            "network:dns",
            "db:read:stock_daily",
            "db:read:analysis_history",
            "db:read:backtest_summaries",
            "db:write:backtest_results",
            "db:write:backtest_summaries",
            "db:write:decision_signal_outcomes",
            "db:write:decision_signal_feedback",
            "db:write:skill_opinion_outcomes",
            "db:write:skill_opinion_samples",
            "db:write:retry_marker",
            "fs:read:prior-cache",
            "fs:write:report",
            "fs:write:log",
            "output:rankings",
            "output:raw-payload",
            "output:diagnostics",
            "future-capability",
            None,
        ):
            with self.subTest(capability=capability):
                oracle = start()
                oracle.request("fixture.read", fixture_for(1))
                oracle.request("seal.stage", seal_intent_for(1))
                try:
                    oracle.request(capability, b"INVENTED_DO_NOT_ECHO")
                except Denied as error:
                    self.assertEqual(str(error), "capability denied")
                else:
                    self.fail("forbidden capability reached the boundary without a denial")
                self.assert_latched(oracle, ("fixture.read", "seal.stage"))

    def test_allowed_capability_rejects_bad_payloads_and_wrong_order(self):
        output = json.loads(seal_intent_for(1))
        for capability, payload in (
            ("fixture.read", fixture_for(2)),
            ("fixture.read", fixture_for(1).replace(b'"slot":1', b'"slot":2,"slot":1')),
            ("fixture.read", bytearray(fixture_for(1))),
            ("seal.stage", canonical({**output, "ranking": "INVENTED"})),
            ("seal.stage", canonical({**output, "score": True})),
            ("seal.stage", canonical({**output, "action": "INVENTED_FREE_TEXT"})),
            ("seal.stage", seal_intent_for(2)),
            ("seal.stage", b""),
        ):
            with self.subTest(capability=capability, length=len(payload)):
                oracle = start()
                effects = ()
                if capability == "seal.stage":
                    oracle.request("fixture.read", fixture_for(1))
                    effects = ("fixture.read",)
                with self.assertRaises(Denied):
                    oracle.request(capability, payload)
                self.assert_latched(oracle, effects)
        oracle = start()
        with self.assertRaises(Denied):
            oracle.request("seal.stage", seal_intent_for(1))
        self.assert_latched(oracle)

    def test_duplicate_operations_cannot_publish(self):
        for capability, payload in (
            ("fixture.read", fixture_for(1)),
            ("seal.stage", seal_intent_for(1)),
        ):
            with self.subTest(capability=capability):
                oracle = start()
                oracle.request("fixture.read", fixture_for(1))
                effects = ("fixture.read",)
                if capability == "seal.stage":
                    oracle.request(capability, payload)
                    effects += ("seal.stage",)
                with self.assertRaises(Denied):
                    oracle.request(capability, payload)
                self.assert_latched(oracle, effects)


if __name__ == "__main__":
    unittest.main()
