"""Pinned invented-only native Kernel 2022Q2/Q3 producer fixture interoperability.

This test does not run the producer, access provider data, create U1 formation,
inspect outcomes, or open any protected period. Fixture source: Kernel PR #31.
"""
import copy
import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from experiments.pit import kernel_membership_bundle as wire
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


def coherent_reyear(request, manifest, payload, year):
    """Relabel *all* time/quarter/lineage fields in an invented 2022 fixture.

    Other checks remain satisfiable; a negative 2021 result must be caused
    solely by the native 2022 profile-year check, not by an unrelated digest,
    time, row or source-lineage mismatch. The pinned original is never edited.
    """
    changed = copy.deepcopy(request)
    m, p = json.loads(manifest), json.loads(payload)
    original_quarters = changed["owner_quarters"]
    mapped = {q: year + q[4:] for q in original_quarters}
    changed["owner_quarters"] = [mapped[q] for q in original_quarters]
    for coord in changed["coordinates"]:
        coord["quarter"] = mapped[coord["quarter"]]
        coord["effective_date"] = year + coord["effective_date"][4:]
        coord["as_of"] = year + coord["as_of"][4:]
    m["source_lineage"] = {mapped[q]: roots for q, roots in m["source_lineage"].items()}
    p["owner_quarters"] = list(changed["owner_quarters"])
    for part in p["quarters"]:
        part["quarter"] = mapped[part["quarter"]]
        part["archive_search"]["search_date"] = year + part["archive_search"]["search_date"][4:]
        for row in part["rows"]:
            if row["known_at_upper"].startswith("2022-"):
                row["known_at_upper"] = year + row["known_at_upper"][4:]
    p["source_lineage_sha256"] = hashlib.sha256(canonical(m["source_lineage"])).hexdigest()
    return changed, *rebound(changed, canonical(m), canonical(p))


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

        # 2021 lies inside the general <=2022 gate; every digest,
        # effective clock, publication bound, payload and lineage key agrees.
        # The dedicated native profile-year check is the ONLY refusal cause.
        changed, m, p, pin = coherent_reyear(request, manifest, payload, "2021")
        self.assertFalse(wire._native_profile_year_matches(
            changed["profile"], changed["owner_quarters"]))
        with self.assertRaises(EvidenceRejected):
            open_kernel_wire_synthetic(m, p, request=changed,
                                       expected_manifest_sha256=pin)
        # Mutation control: with ONLY that guard bypassed, the very same
        # coherent 2021 synthetic wire is otherwise accepted end-to-end.
        with patch.object(wire, "_native_profile_year_matches", return_value=True):
            result = open_kernel_wire_synthetic(m, p, request=changed,
                                                expected_manifest_sha256=pin)
        self.assertEqual(result["owner_quarters"], ["2021Q2", "2021Q3"])

        # Distinct outer boundary: even with native source-year check bypassed,
        # any 2023 ROWS quarter is refused by the project-wide <=2022 gate.
        changed, m, p, pin = coherent_reyear(request, manifest, payload, "2023")
        with patch.object(wire, "_native_profile_year_matches", return_value=True):
            with self.assertRaises(EvidenceRejected):
                open_kernel_wire_synthetic(m, p, request=changed,
                                           expected_manifest_sha256=pin)
