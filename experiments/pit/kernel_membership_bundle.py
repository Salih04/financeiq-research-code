"""FIQ-07 invented-only Kernel wire-format validation.

No I/O or production adapter. Besides in-memory synthetic development shapes,
this consumer accepts the pinned native-producer 2022 invented fixture profile.
Neither demonstrates real source access, authorized ROWS, OD-1 aggregates or U1.
"""
import hashlib
import hmac
import json
import re
from datetime import date, datetime, time, timezone
from zoneinfo import ZoneInfo

from .membership_evidence import EvidenceRejected, _json, _hash, _time, _date, _synthetic_id

_STATUSES = ("MEMBER", "NOT_MEMBER", "UNKNOWN", "AMBIGUOUS", "CONFLICT")
_TIERS = {"XU030": 30, "XU050": 20, "XU100": 50}
_REQUEST = {"contract", "version", "mode", "owner_quarters", "coordinates", "recipient", "profile"}
_COORD = {"quarter", "effective_date", "effective_precision", "as_of", "system_as_of"}
_MANIFEST = {"contract", "version", "hash_algorithm", "recipient", "path", "payload_sha256",
             "payload_bytes", "request_sha256", "source_lineage"}
_PAYLOAD = {"contract", "version", "basis", "independent_source", "mode",
            "owner_quarters", "request_sha256", "source_lineage_sha256", "quarters"}
_ROW = {"source_code", "tier_cell", "tier", "source_evidence_id", "member_kind",
        "member_id", "security_id", "issuer_id", "identity", "status",
        "known_at_upper", "assertion_ids"}
_SEARCH = {"search_date", "query", "result_count", "intra_period_flag", "evidence_id"}
_SETTLE = {"checkpoint_ref", "accepted_cutoff", "proof_kind"}
# Additional reviewed source-year profile: only invented 2022 fixture bytes.
_NATIVE_DEVELOPMENT_PROFILES = frozenset({"DATASTORE3184_FINAL_2022"})


def _deny():
    raise EvidenceRejected("synthetic Kernel wire shape refused")


def _exact(obj, fields):
    if type(obj) is not dict or set(obj) != fields:
        _deny()


def _canonical(obj):
    try:
        return json.dumps(obj, sort_keys=True, ensure_ascii=True,
                          separators=(",", ":"), allow_nan=False).encode("ascii")
    except (TypeError, ValueError, UnicodeError, OverflowError):
        _deny()


def _digest(obj):
    return hashlib.sha256(_canonical(obj)).hexdigest()


def _syn(s):
    try:
        _synthetic_id(s)
    except EvidenceRejected:
        _deny()


def _native_profile_year_matches(profile, quarters):
    """Pure source-year constraint; independently mutation-tested with coherent wire."""
    return (profile not in _NATIVE_DEVELOPMENT_PROFILES
            or all(q.startswith("2022Q") for q in quarters))


def open_kernel_wire_synthetic(manifest, payload, *, request, expected_manifest_sha256):
    """Validate invented development-window manifest/payload structure and hashes.

    The manifest pin must be independently obtained, never copied from an
    untrusted input. This is a shape test, not a native producer round-trip.
    """
    if (type(manifest) is not bytes or type(payload) is not bytes
            or not manifest or not payload or
            len(manifest) > 262144 or len(payload) > 262144):
        _deny()
    _hash(expected_manifest_sha256)
    if not hmac.compare_digest(hashlib.sha256(manifest).hexdigest(),
                               expected_manifest_sha256):
        _deny()
    m, e = _json(manifest), _json(payload)
    _exact(request, _REQUEST)
    _exact(m, _MANIFEST)
    _exact(e, _PAYLOAD)
    quarters = request["owner_quarters"]
    if (request["contract"] != "membership-evidence"
            or request["version"] != "1.0.0"
            or request["recipient"] != "SYNTHETIC_TEST_ONLY"
            or request["mode"] not in ("ROWS", "COUNTS_ONLY")
            or type(request["profile"]) is not str
            or not (request["profile"].startswith("SYNTHETIC_DEVELOPMENT_")
                    or request["profile"] in _NATIVE_DEVELOPMENT_PROFILES)
            or type(quarters) is not list or not quarters
            or any(type(q) is not str
                   or re.fullmatch(r"20[0-2][0-9]Q[1-4]", q) is None
                   or int(q[:4]) > 2022 for q in quarters)
            or quarters != sorted(set(quarters))
            or type(request["coordinates"]) is not list
            or len(request["coordinates"]) != len(quarters)):
        _deny()
    # Native source-year profiles may not be relabelled as another year.
    if not _native_profile_year_matches(request["profile"], quarters):
        _deny()
    coords, cutoffs = {}, set()
    for q, coord in zip(quarters, request["coordinates"]):
        _exact(coord, _COORD)
        day = _date(coord["effective_date"])
        # CIVIL_DATE has no independently proven intraday formation instant.
        # Reject knowledge at/after the earliest Istanbul-day boundary;
        # admitting same-day information requires a separate evidenced F.
        day_start = datetime.combine(
            day, time.min, tzinfo=ZoneInfo("Europe/Istanbul")).astimezone(timezone.utc)
        if _time(coord["as_of"]) >= day_start:
            _deny()
        if (coord["quarter"] != q or coord["effective_precision"] != "CIVIL_DATE"
                or day.year != int(q[:4]) or (day.month - 1) // 3 + 1 != int(q[-1])
                or _time(coord["as_of"]) >= _time(coord["system_as_of"])):
            _deny()
        coords[q] = coord
        cutoffs.add(coord["system_as_of"])
    if len(cutoffs) != 1:
        _deny()
    for key in ("payload_sha256", "request_sha256"):
        _hash(m[key])
    _hash(e["request_sha256"])
    _hash(e["source_lineage_sha256"])
    if (m["contract"] != "membership-evidence" or m["version"] != "1.0.0"
            or m["hash_algorithm"] != "sha256"
            or m["recipient"] != "SYNTHETIC_TEST_ONLY"
            or m["path"] != "membership-evidence.json"
            or type(m["payload_bytes"]) is not int
            or m["payload_bytes"] != len(payload)
            or m["payload_sha256"] != hashlib.sha256(payload).hexdigest()
            or m["request_sha256"] != _digest(request)
            or e["contract"] != "membership-evidence" or e["version"] != "1.0.0"
            or e["basis"] != "SYNTHETIC_ONLY"
            or e["independent_source"] != "SAME_PUBLISHER"
            or e["mode"] != request["mode"]
            or e["owner_quarters"] != quarters
            or e["request_sha256"] != _digest(request)
            or e["source_lineage_sha256"] != _digest(m["source_lineage"])
            or manifest != _canonical(m) or payload != _canonical(e)
            or type(e["quarters"]) is not list or len(e["quarters"]) != len(quarters)
            or type(m["source_lineage"]) is not dict):
        _deny()
    available = set()
    # KER-09 immutable assertion versions retain their member and status.
    assertion_statements = {}
    for q, part in zip(quarters, e["quarters"]):
        if type(part) is not dict or part.get("quarter") != q:
            _deny()
        if part.get("status") == "UNAVAILABLE":
            expected = {"quarter": q, "status": "UNAVAILABLE", "counts": None}
            if request["mode"] == "ROWS":
                expected["rows"] = None
            if part != expected or q in m["source_lineage"]:
                _deny()
            continue
        if part.get("status") != "EVIDENCED":
            _deny()
        if request["mode"] == "ROWS":
            _exact(part, {"quarter", "status", "rows", "counts",
                          "archive_search", "settlement"})
            _exact(part["archive_search"], _SEARCH)
            _exact(part["settlement"], _SETTLE)
            settled = part["settlement"]
            if (settled["accepted_cutoff"] != coords[q]["system_as_of"]
                    or settled["proof_kind"] != "SYNTHETIC_NOT_TRUSTED"):
                _deny()
            _syn(settled["checkpoint_ref"])
            archive = part["archive_search"]
            # Search execution civil day is Europe/Istanbul, not formation as_of.
            search_day = _date(archive["search_date"])
            cutoff = _time(coords[q]["system_as_of"])
            istanbul = ZoneInfo("Europe/Istanbul")
            try:
                settled_day = cutoff.astimezone(istanbul).date()
            except OverflowError:
                # An offset under 24 hours can only overflow upward on the
                # final UTC day. Every representable search day is then earlier.
                if cutoff.date() != date.max:
                    _deny()
                settled_day = date.max
            if search_day > settled_day:
                _deny()
            _syn(archive["query"])
            _syn(archive["evidence_id"])
            if (type(archive["result_count"]) is not int or archive["result_count"] < 0
                    or type(archive["intra_period_flag"]) is not bool):
                _deny()
        else:
            _exact(part, {"quarter", "status", "counts"})
        counts = part["counts"]
        _exact(counts, set(_STATUSES) | {"tier_narrowest"})
        for status in _STATUSES:
            if type(counts[status]) is not int or counts[status] < 0:
                _deny()
        _exact(counts["tier_narrowest"], set(_TIERS))
        if any(type(counts["tier_narrowest"][tier]) is not int
               or counts["tier_narrowest"][tier] != count
               for tier, count in _TIERS.items()):
            _deny()
        # Source-tier membership arithmetic is a cross-mode invariant.
        # An externally pinned digest does not establish logical consistency.
        if counts["MEMBER"] != sum(counts["tier_narrowest"].values()):
            _deny()
        if request["mode"] == "ROWS":
            rows = part["rows"]
            if type(rows) is not list or not rows:
                _deny()
            codes, members, cells, assertion_ids = set(), set(), set(), set()
            statuses = dict.fromkeys(_STATUSES, 0)
            tiers = dict.fromkeys(_TIERS, 0)
            for row in rows:
                _exact(row, _ROW)
                for key in ("source_code", "source_evidence_id", "member_id"):
                    _syn(row[key])
                if (row["member_kind"] != "LISTING" or row["identity"] != "BOUND"
                        or row["status"] not in ("MEMBER", "NOT_MEMBER")
                        or row["source_code"] in codes or row["member_id"] in members
                        or type(row["assertion_ids"]) is not list
                        or not row["assertion_ids"]
                        or row["security_id"] is not None or row["issuer_id"] is not None):
                    _deny()
                codes.add(row["source_code"])
                members.add(row["member_id"])
                for aid in row["assertion_ids"]:
                    _syn(aid)
                    if aid in assertion_ids:
                        _deny()
                    assertion_ids.add(aid)
                    statement = (row["member_kind"], row["member_id"], row["status"])
                    if (aid in assertion_statements
                            and assertion_statements[aid] != statement):
                        _deny()
                    assertion_statements[aid] = statement
                if _time(row["known_at_upper"]) > _time(coords[q]["as_of"]):
                    _deny()
                if row["status"] == "MEMBER":
                    if row["tier"] not in _TIERS:
                        _deny()
                    column = "CDEF"[int(q[-1]) - 1]
                    if (type(row["tier_cell"]) is not str
                            or re.fullmatch(column + r"(?:[5-9]|[1-9][0-9]+)",
                                            row["tier_cell"]) is None
                            or row["tier_cell"] in cells):
                        _deny()
                    cells.add(row["tier_cell"])
                    tiers[row["tier"]] += 1
                elif row["tier"] is not None or row["tier_cell"] is not None:
                    _deny()
                statuses[row["status"]] += 1
            if statuses != {k: counts[k] for k in _STATUSES} or tiers != counts["tier_narrowest"]:
                _deny()
        roots = m["source_lineage"].get(q)
        if type(roots) is not list or len(roots) < 2 or roots != sorted(set(roots)):
            _deny()
        for root in roots:
            _syn(root)
        available.add(q)
    if set(m["source_lineage"]) != available:
        _deny()
    return e
