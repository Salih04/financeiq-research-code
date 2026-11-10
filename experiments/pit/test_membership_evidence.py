"""FIQ-07 invented-only membership evidence contract checks: no data or outcomes."""
import copy
import hashlib
import json
from pathlib import Path
import unittest

from experiments.pit.membership_evidence import (
    CONTRACT, VERSION, LABEL, EvidenceRejected, ContractUnverified,
    open_synthetic_bundle, _validate, _canonical,
)


FIXTURE = Path(__file__).parent / "fixtures" / "membership_evidence" / "invented.json"


class MembershipEvidenceSyntheticTest(unittest.TestCase):
    def setUp(self):
        self.raw = FIXTURE.read_bytes()
        self.doc = json.loads(self.raw)
        self.request = copy.deepcopy(self.doc["query"])

    def changed(self, change, *, rehash=True):
        item = copy.deepcopy(self.doc)
        change(item)
        if rehash:
            item["content_hash"] = hashlib.sha256(
                _canonical({k: v for k, v in item.items() if k != "content_hash"})
            ).hexdigest()
        return json.dumps(item, sort_keys=True, separators=(",", ":")).encode()

    def test_approved_invented_bytes_only(self):
        item = open_synthetic_bundle(self.raw, self.request)
        self.assertEqual((CONTRACT, VERSION, item.comparison_label),
                         ("membership-evidence", "1.0.0", LABEL))
        self.assertEqual(item.request, self.request)

    def test_effective_date_bound_listing_and_nullable_issuer(self):
        item = open_synthetic_bundle(self.raw, self.request)
        self.assertEqual(item.status("SYN-LISTING-ALPHA"), "MEMBER")
        self.assertEqual(item.dependent_join("SYN-LISTING-ALPHA", "issuer_id"),
                         "UNAVAILABLE")
        self.assertEqual(item.dependent_join("SYN-LISTING-ALPHA", "security_id"),
                         "UNAVAILABLE")

    def test_explicit_negative_and_absent_not_negative(self):
        item = open_synthetic_bundle(self.raw, self.request)
        self.assertEqual(item.status("SYN-LISTING-BETA"), "NOT_MEMBER")
        self.assertEqual(item.status("SYN-NO-EVIDENCE"), "UNAVAILABLE")
        self.assertEqual(item.status("SYN-LISTING-GAMMA"), "UNAVAILABLE")
        self.assertEqual(item.status("SYN-CODE-ALPHA"), "UNAVAILABLE")

    def test_no_dependent_join_without_positive_member(self):
        item = open_synthetic_bundle(self.raw, self.request)
        self.assertEqual(item.dependent_join("SYN-LISTING-BETA", "issuer_id"),
                         "UNAVAILABLE")
        with self.assertRaises(EvidenceRejected):
            item.dependent_join("SYN-LISTING-ALPHA", "guessed_alias")

    def test_exact_byte_pin_rejects_whitespace_change(self):
        with self.assertRaises(ContractUnverified):
            open_synthetic_bundle(self.raw + b" ", self.request)

    def test_refuse_non_synthetic_and_version_drift(self):
        for field, value in (("synthetic", False), ("contract_version", "1.1.0")):
            with self.subTest(field=field), self.assertRaises(ContractUnverified):
                _validate(self.changed(lambda x: x.__setitem__(field, value)),
                          self.request)

    def test_request_binding_and_missing_explicit_clock(self):
        with self.assertRaises(EvidenceRejected):
            _validate(self.raw, dict(self.request, system_as_of=None))
        with self.assertRaises(EvidenceRejected):
            _validate(self.raw, {k: v for k, v in self.request.items()
                                 if k != "system_as_of"})

    def test_unsettled_or_mixed_system_authority(self):
        for field, value in (("status", "UNSETTLED"),
                             ("cutoff", "2022-10-01T00:00:00Z"),
                             ("lineage", "UNVERIFIED")):
            with self.subTest(field=field), self.assertRaises(EvidenceRejected):
                _validate(self.changed(
                    lambda x: x["settlement"].__setitem__(field, value)),
                    self.request)

    def test_protected_formation_refuses_even_synthetic(self):
        q = dict(self.request, formation_date="2024-01-01",
                 effective_date="2024-01-01",
                 formation_instant="2023-12-31T21:00:00Z")
        with self.assertRaises(ContractUnverified):
            _validate(self.changed(lambda x: x.__setitem__("query", q)), q)

    def test_source_completeness_and_same_publisher_only(self):
        for field, value in (("label", "INDEPENDENT_VALIDATION"),
                             ("label", None)):
            with self.subTest(field=field), self.assertRaises(EvidenceRejected):
                _validate(self.changed(
                    lambda x: x["source_check"].__setitem__(field, value)),
                    self.request)
        with self.assertRaises(EvidenceRejected):
            _validate(self.changed(
                lambda x: x["source_check"]["announcement_search"].__setitem__(
                    "status", "UNAVAILABLE")), self.request)

    def test_publication_after_as_of_refused(self):
        with self.assertRaises(EvidenceRejected):
            _validate(self.changed(
                lambda x: x["memberships"][0].__setitem__(
                    "known_at_upper", "2022-09-30T20:00:00Z")), self.request)

    def test_missing_negative_assertion_not_silently_inferred(self):
        with self.assertRaises(EvidenceRejected):
            _validate(self.changed(
                lambda x: x["memberships"][1].__setitem__("assertion_ids", [])),
                self.request)

    def test_identity_conflict_blocks_affected_member_only(self):
        def contradictory_binding(item):
            item["status"] = "CONFLICT"
            item["known_at_upper"] = None
            item["identity_proof_sha256"] = None
        raw = self.changed(lambda x: contradictory_binding(x["identities"][0]))
        doc = _validate(raw, self.request)
        self.assertEqual(doc["identities"][0]["status"], "CONFLICT")
        other = self.doc["memberships"][1]
        self.assertEqual(other["status"], "NOT_MEMBER")

    def test_tampered_content_hash_and_duplicate_json_keys_refused(self):
        with self.assertRaises(EvidenceRejected):
            _validate(self.changed(
                lambda x: x["settlement"].__setitem__(
                    "proof_sha256", "0" * 64), rehash=False), self.request)
        with self.assertRaises(EvidenceRejected):
            _validate(b'{"contract":"a","contract":"b"}', self.request)

    def test_field_allowlist_and_synthetic_provenance_digest(self):
        with self.assertRaises(EvidenceRejected):
            _validate(self.changed(lambda x: x.__setitem__(
                "undocumented_field", "SYN-FAKE")), self.request)
        with self.assertRaises(EvidenceRejected):
            _validate(self.changed(lambda x: x["memberships"][0].__setitem__(
                "source_doc_digest", None)), self.request)


    def test_unrecorded_announcement_search_refuses(self):
        with self.assertRaises(EvidenceRejected):
            _validate(self.changed(
                lambda x: x["source_check"]["announcement_search"].__setitem__(
                    "recorded", False)), self.request)

    def test_late_ker10_identity_adjudication_refuses(self):
        with self.assertRaises(EvidenceRejected):
            _validate(self.changed(
                lambda x: x["identities"][0].__setitem__(
                    "known_at_upper", "2022-09-30T20:00:00Z")), self.request)

    def test_nonhashable_assertion_ids_refuse_as_contract_error(self):
        with self.assertRaises(EvidenceRejected):
            _validate(self.changed(
                lambda x: x["memberships"][0].__setitem__(
                    "assertion_ids", [{"malformed": "synthetic"}])), self.request)

if __name__ == "__main__":
    unittest.main()
