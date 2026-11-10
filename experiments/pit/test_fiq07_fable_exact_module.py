"""FIQ-07 synthetic-only fail-first probes for ORIGINAL public consumer module.

Run from a clean checkout of Salih04/financeiq-research-code pinned to
5b1030ad9e6760af22f5f8fc0cf36a355b9f6df8:

    PYTHONPATH=. python -m unittest -v experiments.pit.test_fiq07_fable_exact_module

This suite intentionally FAILS at baseline for the two unpatched candidates.
No real DataStore data, network, holdout, price, returns, or source rights used.
"""
import copy
import hashlib
import json
import unittest

from experiments.pit.kernel_membership_bundle import open_kernel_wire_synthetic
from experiments.pit.membership_evidence import EvidenceRejected
from experiments.pit.test_kernel_membership_bundle import canonical, invented, read


def _rebind(request, manifest, payload):
    """Rebind all canonical invented-only digests after a deliberate mutation."""
    sha = lambda x: hashlib.sha256(canonical(x)).hexdigest()
    payload['request_sha256'] = sha(request)
    payload['source_lineage_sha256'] = sha(manifest['source_lineage'])
    manifest['request_sha256'] = sha(request)
    manifest['payload_sha256'] = sha(payload)
    manifest['payload_bytes'] = len(canonical(payload))


def two_quarters():
    """Invent 2022Q3 and 2022Q4, with independent Q3 assertion IDs."""
    request, manifest, payload = invented()
    q3 = copy.deepcopy(payload['quarters'][0])
    q3['quarter'] = '2022Q3'
    q3['archive_search']['search_date'] = '2022-06-29'
    q3['archive_search']['query'] = 'SYN-ARCHIVE-Q3'
    q3['archive_search']['evidence_id'] = 'SYN-ARCHIVE-EVIDENCE-Q3'
    q3['settlement']['checkpoint_ref'] = 'SYN-CHECKPOINT-Q3'
    for idx, row in enumerate(q3['rows']):
        row['tier_cell'] = f'E{idx + 5}' if row['tier'] is not None else None
        row['source_evidence_id'] = f'SYN-Q3-EVIDENCE-{idx:03d}'
        row['assertion_ids'] = [f'SYN-Q3-ASSERT-{idx:03d}']
        row['known_at_upper'] = '2022-06-30T17:00:00Z'
    request['owner_quarters'] = ['2022Q3', '2022Q4']
    request['coordinates'].insert(0, dict(
        quarter='2022Q3', effective_date='2022-07-01',
        effective_precision='CIVIL_DATE', as_of='2022-06-30T18:00:00Z',
        system_as_of='2022-10-10T00:00:00Z'))
    payload['owner_quarters'] = ['2022Q3', '2022Q4']
    payload['quarters'].insert(0, q3)
    manifest['source_lineage']['2022Q3'] = [
        'SYN-Q3-ARCHIVE-ROOT', 'SYN-Q3-WORKBOOK-ROOT']
    _rebind(request, manifest, payload)
    return request, manifest, payload


class OriginalModuleFableFailFirst(unittest.TestCase):
    def test_control_untouched_q4_is_accepted(self):
        req, man, pay = invented()
        self.assertEqual(read(req, man, pay)['quarters'][0]['status'], 'EVIDENCED')

    def test_control_untouched_two_quarters_are_accepted(self):
        req, man, pay = two_quarters()
        self.assertEqual([q['status'] for q in read(req, man, pay)['quarters']],
                         ['EVIDENCED', 'EVIDENCED'])

    def test_control_same_quarter_assertion_collision_is_rejected(self):
        req, man, pay = invented()
        rows = pay['quarters'][0]['rows']
        rows[0]['assertion_ids'] = list(rows[1]['assertion_ids'])
        _rebind(req, man, pay)
        with self.assertRaises(EvidenceRejected):
            read(req, man, pay)

    def test_F1_search_after_settled_snapshot_rejected(self):
        # Search-after-cutoff is the defensible minimum. Do NOT assert that
        # search_date <= as_of or search_date < formation effective date:
        # a native invented 2022 fixture legitimately searches later.
        for day in ('2022-10-11', '2030-01-01'):
            with self.subTest(archive_search_date=day):
                req, man, pay = invented()
                pay['quarters'][0]['archive_search']['search_date'] = day
                _rebind(req, man, pay)
                with self.assertRaises(EvidenceRejected):
                    read(req, man, pay)

    def test_F2_assertion_reuse_for_another_listing_rejected(self):
        # A reused Q3 assertion is pasted into a distinct Q4 LISTING; both
        # positive and explicit negative variants must fail rather than
        # claiming invented source provenance for two different listings.
        for q4_target in (0, 100):
            with self.subTest(q4_row=q4_target):
                req, man, pay = two_quarters()
                pay['quarters'][1]['rows'][q4_target]['assertion_ids'] = list(
                    pay['quarters'][0]['rows'][1]['assertion_ids'])
                _rebind(req, man, pay)
                with self.assertRaises(EvidenceRejected):
                    read(req, man, pay)

    def test_control_same_listing_cross_quarter_reuse_if_namespace_is_global(self):
        # This control encodes the PROPOSED identity-binding rule, not a
        # blanket prohibition on same-assertion across quarters. Its semantic
        # authority must be approved before merging any fix.
        req, man, pay = two_quarters()
        pay['quarters'][1]['rows'][1]['assertion_ids'] = list(
            pay['quarters'][0]['rows'][1]['assertion_ids'])
        _rebind(req, man, pay)
        self.assertEqual([q['status'] for q in read(req, man, pay)['quarters']],
                         ['EVIDENCED', 'EVIDENCED'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
