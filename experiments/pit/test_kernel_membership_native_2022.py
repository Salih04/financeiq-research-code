"""Pinned invented-only native Kernel 2022Q2/Q3 producer fixture interoperability.

This test does not run the producer, access provider data, create U1 formation,
inspect outcomes, or open any protected period. Fixture source: Kernel PR #31.
"""
import copy
import hashlib
import json
import unittest
from pathlib import Path

from experiments.pit.kernel_membership_bundle import open_kernel_wire_synthetic
from experiments.pit.membership_evidence import EvidenceRejected

FIXTURE = (Path(__file__).resolve().parents[2] / "fixtures" / "synthetic"
           / "membership_evidence_ds3184_2022_v1.json")
EXPECTED_MANIFEST_SHA256 = "99ff0cdb4532d22da4cfb85ca4608496a33905674fadfcb67e2bec81dcf9333b"


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("ascii")


def fixture():
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return doc["request"], doc["manifest"].encode("utf-8"), doc["payload"].encode("utf-8"), doc


def rebound(request, manifest, payload):
    """Rehash a *synthetic mutation* to isolate profile-year rules from pin failures."""
    m, p = json.loads(manifest), json.loads(payload)
    digest = hashlib.sha256(canonical(request)).hexdigest()
    m["request_sha256"] = digest
    p["request_sha256"] = digest
    p_bytes = canonical(p)
    m["payload_sha256"] = hashlib.sha256(p_bytes).hexdigest()
    m["payload_bytes"] = len(p_bytes)
    m_bytes = canonical(m)
    return m_bytes, p_bytes, hashlib.sha256(m_bytes).hexdigest()


class KernelNative2022FixtureTests(unittest.TestCase):
    def test_pinned_native_fixture_accepted(self):
        request, manifest, payload, doc = fixture()
        self.assertEqual(doc["expected_manifest_sha256"], EXPECTED_MANIFEST_SHA256)
        self.assertEqual(hashlib.sha256(manifest).hexdigest(), EXPECTED_MANIFEST_SHA256)
        self.assertEqual(request["profile"], "DATASTORE3184_FINAL_2022")
        self.assertEqual(request["mode"], "ROWS")
        self.assertEqual(request["owner_quarters"], ["2022Q2", "2022Q3"])
        result = open_kernel_wire_synthetic(
            manifest, payload, request=request,
            expected_manifest_sha256=EXPECTED_MANIFEST_SHA256)
        self.assertEqual(result["independent_source"], "SAME_PUBLISHER")
        self.assertEqual(result["mode"], "ROWS")
        self.assertEqual([part["status"] for part in result["quarters"]],
                         ["EVIDENCED", "EVIDENCED"])
        self.assertEqual([len(part["rows"]) for part in result["quarters"]], [100, 101])
        self.assertEqual([part["counts"]["MEMBER"] for part in result["quarters"]], [100, 100])
        self.assertEqual(result["quarters"][1]["counts"]["NOT_MEMBER"], 1)
        for part in result["quarters"]:
            self.assertEqual(part["counts"]["tier_narrowest"],
                             {"XU030": 30, "XU050": 20, "XU100": 50})
            self.assertTrue(all(row["source_code"].startswith("SYN-")
                                and row["member_id"].startswith("SYN-")
                                for row in part["rows"]))

    def test_manifest_pin_tamper_rejected(self):
        request, manifest, payload, _ = fixture()
        with self.assertRaises(EvidenceRejected):
            open_kernel_wire_synthetic(manifest, payload, request=request,
                                       expected_manifest_sha256="0" * 64)
        with self.assertRaises(EvidenceRejected):
            open_kernel_wire_synthetic(manifest + b" ", payload, request=request,
                                       expected_manifest_sha256=EXPECTED_MANIFEST_SHA256)

    def test_payload_tamper_rejected(self):
        request, manifest, payload, _ = fixture()
        with self.assertRaises(EvidenceRejected):
            open_kernel_wire_synthetic(manifest, payload + b" ", request=request,
                                       expected_manifest_sha256=EXPECTED_MANIFEST_SHA256)

    def test_profile_allowlist_and_2022_boundary(self):
        request, manifest, payload, _ = fixture()
        for unsupported in ("DATASTORE3184_FINAL_2025", "DATASTORE3184_FINAL_2021",
                            "SYNTHETIC_OTHER"):
            with self.subTest(profile=unsupported):
                changed = copy.deepcopy(request)
                changed["profile"] = unsupported
                m, p, pin = rebound(changed, manifest, payload)
                with self.assertRaises(EvidenceRejected):
                    open_kernel_wire_synthetic(m, p, request=changed,
                                               expected_manifest_sha256=pin)

        for year in ("2021", "2023"):
            with self.subTest(year=year):
                changed = copy.deepcopy(request)
                changed["owner_quarters"] = [year + "Q2", year + "Q3"]
                changed["coordinates"][0].update(
                    quarter=year + "Q2", effective_date=year + "-05-16")
                changed["coordinates"][1].update(
                    quarter=year + "Q3", effective_date=year + "-08-15")
                m, p, pin = rebound(changed, manifest, payload)
                with self.assertRaises(EvidenceRejected):
                    open_kernel_wire_synthetic(m, p, request=changed,
                                               expected_manifest_sha256=pin)
