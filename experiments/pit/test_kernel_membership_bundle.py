"""Invented wire-shape checks, NOT Kernel producer or real source tests."""
import copy
import hashlib
import json
import unittest

from experiments.pit.kernel_membership_bundle import open_kernel_wire_synthetic
from experiments.pit.membership_evidence import EvidenceRejected


def canonical(obj):
    return json.dumps(obj, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("ascii")


def invented():
    q = "2022Q4"
    request = dict(contract="membership-evidence", version="1.0.0", mode="ROWS",
                   owner_quarters=[q], recipient="SYNTHETIC_TEST_ONLY",
                   profile="SYNTHETIC_DEVELOPMENT_UNPROFILED",
                   coordinates=[dict(quarter=q, effective_date="2022-10-03",
                                     effective_precision="CIVIL_DATE",
                                     as_of="2022-09-30T18:00:00Z",
                                     system_as_of="2022-10-10T00:00:00Z")])
    rows = []
    for i in range(101):
        tier = ("XU030" if i < 30 else "XU050" if i < 50
                else "XU100" if i < 100 else None)
        rows.append(dict(source_code="SYN-CODE-%03d" % i,
            tier_cell=("F%d" % (i + 5)) if tier else None,
            tier=tier, source_evidence_id="SYN-EVIDENCE-%03d" % i,
            member_kind="LISTING", member_id="SYN-LIST-%03d" % i,
            security_id=None, issuer_id=None, identity="BOUND",
            status="MEMBER" if tier else "NOT_MEMBER",
            known_at_upper="2022-09-30T17:00:00Z",
            assertion_ids=["SYN-ASSERT-%03d" % i]))
    part = dict(quarter=q, status="EVIDENCED", rows=rows,
        counts=dict(MEMBER=100, NOT_MEMBER=1, UNKNOWN=0, AMBIGUOUS=0, CONFLICT=0,
                    tier_narrowest=dict(XU030=30, XU050=20, XU100=50)),
        archive_search=dict(search_date="2022-09-29", query="SYN-ARCHIVE",
            result_count=5, intra_period_flag=True, evidence_id="SYN-ARCHIVE-EVIDENCE"),
        settlement=dict(checkpoint_ref="SYN-CHECKPOINT",
            accepted_cutoff="2022-10-10T00:00:00Z",
            proof_kind="SYNTHETIC_NOT_TRUSTED"))
    lineage = {q: ["SYN-ARCHIVE-ROOT", "SYN-WORKBOOK-ROOT"]}
    digest = hashlib.sha256(canonical(request)).hexdigest()
    payload = dict(contract="membership-evidence", version="1.0.0",
        basis="SYNTHETIC_ONLY", independent_source="SAME_PUBLISHER",
        mode="ROWS", owner_quarters=[q], request_sha256=digest,
        source_lineage_sha256=hashlib.sha256(canonical(lineage)).hexdigest(),
        quarters=[part])
    manifest = dict(contract="membership-evidence", version="1.0.0",
        hash_algorithm="sha256", recipient="SYNTHETIC_TEST_ONLY",
        path="membership-evidence.json",
        payload_sha256=hashlib.sha256(canonical(payload)).hexdigest(),
        payload_bytes=len(canonical(payload)), request_sha256=digest,
        source_lineage=lineage)
    return request, manifest, payload


def read(request, manifest, payload):
    m, p = canonical(manifest), canonical(payload)
    return open_kernel_wire_synthetic(
        m, p, request=request, expected_manifest_sha256=hashlib.sha256(m).hexdigest())


class KernelDevelopmentWireTests(unittest.TestCase):
    def test_as_of_must_precede_unverified_formation_day(self):
        for cutoff in ("2022-10-02T21:00:00Z", "2022-10-03T12:00:00Z",
                       "2022-10-09T00:00:00Z"):
            with self.subTest(cutoff=cutoff):
                req, manifest, payload = invented()
                req["coordinates"][0]["as_of"] = cutoff
                digest = hashlib.sha256(canonical(req)).hexdigest()
                payload["request_sha256"] = digest
                manifest["request_sha256"] = digest
                manifest["payload_sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
                manifest["payload_bytes"] = len(canonical(payload))
                with self.assertRaises(EvidenceRejected):
                    read(req, manifest, payload)

    def test_counts_only_member_total_must_match_source_tiers(self):
        req, manifest, payload = invented()
        req["mode"] = "COUNTS_ONLY"
        payload["mode"] = "COUNTS_ONLY"
        for key in ("rows", "archive_search", "settlement"):
            del payload["quarters"][0][key]
        payload["quarters"][0]["counts"]["MEMBER"] = 0
        digest = hashlib.sha256(canonical(req)).hexdigest()
        payload["request_sha256"] = digest
        manifest["request_sha256"] = digest
        manifest["payload_sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
        manifest["payload_bytes"] = len(canonical(payload))
        with self.assertRaises(EvidenceRejected):
            read(req, manifest, payload)

    def test_dev_rows_and_source_tiers(self):
        req, manifest, payload = invented()
        result = read(req, manifest, payload)
        self.assertEqual(result["quarters"][0]["status"], "EVIDENCED")
        self.assertEqual(result["quarters"][0]["counts"]["tier_narrowest"],
                         dict(XU030=30, XU050=20, XU100=50))
        self.assertEqual(result["independent_source"], "SAME_PUBLISHER")

    def test_manifest_payload_request_pins(self):
        req, manifest, payload = invented()
        m, p = canonical(manifest), canonical(payload)
        with self.assertRaises(EvidenceRejected):
            open_kernel_wire_synthetic(m, p, request=req,
                                       expected_manifest_sha256="0"*64)
        with self.assertRaises(EvidenceRejected):
            open_kernel_wire_synthetic(m, p+b" ", request=req,
                                       expected_manifest_sha256=hashlib.sha256(m).hexdigest())
        altered = copy.deepcopy(req)
        altered["coordinates"][0]["system_as_of"] = "2022-10-11T00:00:00Z"
        with self.assertRaises(EvidenceRejected):
            read(altered, manifest, payload)

    def test_no_protected_rows_or_od1_counts(self):
        req, manifest, payload = invented()
        req["owner_quarters"] = ["2025Q1"]
        req["coordinates"][0]["quarter"] = "2025Q1"
        req["coordinates"][0]["effective_date"] = "2025-02-14"
        with self.assertRaises(EvidenceRejected):
            read(req, manifest, payload)
        req, manifest, payload = invented()
        req["mode"] = "COUNTS_ONLY"
        payload["mode"] = "COUNTS_ONLY"
        for key in ("rows", "archive_search", "settlement"):
            del payload["quarters"][0][key]
        digest = hashlib.sha256(canonical(req)).hexdigest()
        payload["request_sha256"] = digest
        manifest["request_sha256"] = digest
        manifest["payload_sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
        manifest["payload_bytes"] = len(canonical(payload))
        self.assertEqual(read(req, manifest, payload)["quarters"][0]["status"], "EVIDENCED")

    def test_lineage_digest_is_bound_to_canonical_manifest_roots(self):
        req, manifest, payload = invented()
        self.assertEqual(payload["source_lineage_sha256"],
                         hashlib.sha256(canonical(manifest["source_lineage"])).hexdigest())
        altered = copy.deepcopy(manifest)
        altered["source_lineage"]["2022Q4"] = ["SYN-OTHER-ROOT", "SYN-WORKBOOK-ROOT"]
        with self.assertRaises(EvidenceRejected):
            read(req, altered, payload)
        req, manifest, payload = invented()
        payload["source_lineage_sha256"] = "0" * 64
        manifest["payload_sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
        manifest["payload_bytes"] = len(canonical(payload))
        with self.assertRaises(EvidenceRejected):
            read(req, manifest, payload)

    def test_unavailable_is_null_not_negative(self):
        req, manifest, payload = invented()
        payload["quarters"] = [dict(quarter="2022Q4", status="UNAVAILABLE",
                                   rows=None, counts=None)]
        manifest["source_lineage"] = {}
        payload["source_lineage_sha256"] = hashlib.sha256(canonical({})).hexdigest()
        manifest["payload_sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
        manifest["payload_bytes"] = len(canonical(payload))
        row = read(req, manifest, payload)["quarters"][0]
        self.assertIsNone(row["counts"])
        self.assertIsNone(row["rows"])

    def test_tier_and_lineage_refusals(self):
        for kind in ("tier", "lineage", "negative"):
            req, manifest, payload = invented()
            if kind == "tier":
                payload["quarters"][0]["rows"][0]["tier_cell"] = "C5"
            elif kind == "lineage":
                manifest["source_lineage"]["2022Q4"] = []
            else:
                payload["quarters"][0]["rows"][-1]["assertion_ids"] = []
            manifest["payload_sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
            manifest["payload_bytes"] = len(canonical(payload))
            with self.subTest(kind=kind), self.assertRaises(EvidenceRejected):
                read(req, manifest, payload)
