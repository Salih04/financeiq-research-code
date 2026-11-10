#!/usr/bin/env python3
"""Run only approved synthetic suites; reject skips, count drift and tree drift."""
import ast
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))


def check_tree():
    m = json.loads((ROOT / 'PUBLIC_TREE.json').read_text())
    expected = {x['path']: x for x in m['files']}
    actual = set()
    for p in ROOT.rglob('*'):
        rel = p.relative_to(ROOT).as_posix()
        if rel == '.git' or rel.startswith('.git/'):
            continue
        if p.is_symlink():
            raise RuntimeError('symlink in public tree')
        if p.is_file():
            actual.add(rel)
            if rel == 'PUBLIC_TREE.json':
                continue
            if rel not in expected or hashlib.sha256(p.read_bytes()).hexdigest() != expected[rel]['sha256']:
                raise RuntimeError('file outside digest allowlist: ' + rel)
            if p.suffix == '.py':
                ast.parse(p.read_bytes(), filename=rel)
    if actual != set(expected) | {'PUBLIC_TREE.json'}:
        raise RuntimeError('public file set drift')


class CountedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passed = 0

    def addSuccess(self, test):
        super().addSuccess(test)
        self.passed += 1


def main():
    check_tree()
    loader = unittest.TestLoader()
    suites = [
        ('pit-synthetic', loader.loadTestsFromName('experiments.pit.test_kernel_snapshot'), 16),
        ('research-core-synthetic', loader.discover(str(ROOT / 'experiments/research_core/tests'), pattern='test_*.py'), 21),
        ('membership-evidence-synthetic', loader.loadTestsFromName('experiments.pit.test_membership_evidence'), 18),
        ('membership-wire-dev-synthetic', loader.loadTestsFromName('experiments.pit.test_kernel_membership_bundle'), 7),
    ]
    rows = []
    ok = True
    for name, suite, expected in suites:
        collected = suite.countTestCases()
        if collected != expected:
            raise RuntimeError('collected count drift: ' + name)
        result = unittest.TextTestRunner(verbosity=1, resultclass=CountedResult).run(suite)
        row = dict(suite=name, collected=collected, executed=result.testsRun, passed=result.passed,
                   skipped=len(result.skipped), failed=len(result.failures), errors=len(result.errors),
                   xfail=len(result.expectedFailures), xpass=len(result.unexpectedSuccesses))
        rows.append(row)
        ok = ok and result.wasSuccessful() and row['passed'] == expected and row['executed'] == expected and not any(row[k] for k in ('skipped', 'xfail', 'xpass'))
    check_tree()
    print(json.dumps({'suites': rows, 'private_root_baseline': 1456, 'private_backend_baseline': 916,
                      'private_suite_execution': 'NOT RUN', 'scientific_validity': 'NOT EVALUATED'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
