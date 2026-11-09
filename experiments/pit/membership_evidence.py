"""FIQ-07 membership-evidence 1.0.0: *invented synthetic bytes only*.

This is FinanceIQ's read-only proof-of-contract consumer, not a Kernel adapter.
No IO/network/database, implicit latest watermark, real-source rights or U1
formation is authorized. The six E-1 filing-fact pins stay untouched.
"""
from __future__ import annotations

from datetime import date, datetime
import hashlib
import hmac
import json
import re
from zoneinfo import ZoneInfo


class EvidenceRejected(ValueError):
    """Malformed, ambiguous, or inadmissible synthetic evidence."""


class ContractUnverified(EvidenceRejected):
    """Not one of the exact owner-authorized invented fixture bytes."""


CONTRACT = "membership-evidence"
VERSION = "1.0.0"
LABEL = "SAME_PUBLISHER"
MAX_BYTES = 262144
# Pinned exact invented fixture bytes; intentionally *no* real source adapter.
APPROVED_SYNTHETIC_BYTES = frozenset({"f66949afb64944f4b2b31a2adb334c337535bd1939ba0ffce4a338c5dad4d7dc"})
_QUERY = frozenset({"formation_date", "formation_instant", "effective_date",
                    "as_of", "system_as_of"})
_ROW = frozenset({"member_kind", "member_id", "status", "assertion_ids",
                  "known_at_upper", "source_doc_digest", "chain_digest"})
_ID = frozenset({"member_kind", "member_id", "status", "effective_date",
                 "known_at_upper", "identity_proof_sha256", "mapping_proof_sha256",
                 "security_id", "issuer_id", "cross_period_equivalence"})
_STAMP = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](?:\.[0-9]{1,6})?Z\Z")
_DAY = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\Z")
_DIGEST = re.compile(r"[a-f0-9]{64}\Z")
_STATUSES = frozenset({"MEMBER", "NOT_MEMBER", "UNKNOWN", "AMBIGUOUS", "CONFLICT"})


def _fields(value, names, label):
    if type(value) is not dict or set(value) != set(names):
        raise EvidenceRejected("invalid " + label + " fields")


def _json(raw):
    if type(raw) is not bytes or not raw or len(raw) > MAX_BYTES:
        raise EvidenceRejected("invalid synthetic bytes")

    def pairs(items):
        obj = {}
        for key, val in items:
            if key in obj:
                raise EvidenceRejected("duplicate key")
            obj[key] = val
        return obj

    def nonfinite(_):
        raise EvidenceRejected("nonfinite JSON")

    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                          parse_constant=nonfinite)
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise EvidenceRejected("invalid JSON") from exc


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def _time(value):
    if type(value) is not str or _STAMP.fullmatch(value) is None:
        raise EvidenceRejected("explicit UTC instant required")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EvidenceRejected("invalid instant") from exc


def _date(value):
    if type(value) is not str or _DAY.fullmatch(value) is None:
        raise EvidenceRejected("civil date required")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise EvidenceRejected("invalid civil date") from exc


def _hash(value):
    if type(value) is not str or _DIGEST.fullmatch(value) is None:
        raise EvidenceRejected("sha256 required")


def _synthetic_id(value):
    if type(value) is not str or not value.startswith("SYN-") or len(value) > 90:
        raise EvidenceRejected("invented synthetic ID required")


def _validate(raw, request):
    """Pure validator, also used for negative invented synthetic tests.

    This is not a production entrypoint. open_synthetic_bundle first enforces
    an exact approved byte digest.
    """
    envelope = _json(raw)
    _fields(envelope, {"contract", "contract_version", "synthetic",
                       "query", "settlement", "source_check",
                       "identities", "memberships", "content_hash"}, "envelope")
    if (envelope["contract"] != CONTRACT or envelope["contract_version"] != VERSION
            or envelope["synthetic"] is not True):
        raise ContractUnverified("unsupported or non-synthetic contract")
    _fields(request, _QUERY, "external request")
    _fields(envelope["query"], _QUERY, "bundle request")
    if _canonical(request) != _canonical(envelope["query"]):
        raise EvidenceRejected("external request mismatch")
    q = envelope["query"]
    formation = _date(q["formation_date"])
    if formation > date(2022, 12, 31):
        # Protected 2023–2025 counts are governed by a separate OD-1=B path;
        # no protected individual rows (nor protected aggregate payloads) here.
        raise ContractUnverified("protected or forward formation rows closed")
    effective = _date(q["effective_date"])
    if effective != formation:
        raise EvidenceRejected("effective date and formation date mismatch")
    ftime, asof, system = (_time(q[k]) for k in
                           ("formation_instant", "as_of", "system_as_of"))
    if ftime.astimezone(ZoneInfo("Europe/Istanbul")).date() != formation:
        raise EvidenceRejected("formation instant/civil date mismatch")
    if asof >= ftime:
        raise EvidenceRejected("public knowledge cutoff must precede formation")

    settled = envelope["settlement"]
    _fields(settled, {"status", "lineage", "cutoff", "proof_sha256"}, "settlement")
    if settled["status"] != "SETTLED":
        raise EvidenceRejected("unsettled authority")
    _synthetic_id(settled["lineage"])
    _hash(settled["proof_sha256"])
    if _time(settled["cutoff"]) != system:
        raise EvidenceRejected("mixed or implicit settlement cutoff")

    source = envelope["source_check"]
    _fields(source, {"label", "workbook", "announcement_search"}, "source check")
    if source["label"] != LABEL:
        raise EvidenceRejected("same-publisher consistency label required")
    quarter = str(formation.year) + "Q" + str((formation.month - 1) // 3 + 1)
    for name in ("workbook", "announcement_search"):
        proof = source[name]
        _fields(proof, {"status", "period", "known_at_upper", "proof_sha256"} |
                ({"recorded"} if name == "announcement_search" else set()), name)
        if name == "announcement_search" and proof["recorded"] is not True:
            raise EvidenceRejected("documented announcement search required")
        if proof["status"] != "EVIDENCED" or proof["period"] != quarter:
            raise EvidenceRejected("incomplete U1 channel/period evidence")
        _hash(proof["proof_sha256"])
        upper = _time(proof["known_at_upper"])
        if upper > asof or upper >= ftime:
            raise EvidenceRejected("channel not public before formation")

    identities = envelope["identities"]
    memberships = envelope["memberships"]
    if type(identities) is not list or type(memberships) is not list or not memberships:
        raise EvidenceRejected("invented evidence arrays required")
    by_identity = {}
    for identity in identities:
        _fields(identity, _ID, "identity")
        _synthetic_id(identity["member_id"])
        if identity["member_id"] in by_identity:
            raise EvidenceRejected("duplicate identity")
        if (identity["member_kind"] != "LISTING"
                or identity["status"] not in ("BOUND", "UNKNOWN", "CONFLICT")
                or _date(identity["effective_date"]) != effective):
            raise EvidenceRejected("invalid effective-date listing identity")
        if identity["status"] == "BOUND":
            _hash(identity["identity_proof_sha256"])
            if (_time(identity["known_at_upper"]) > asof or
                    _time(identity["known_at_upper"]) >= ftime):
                raise EvidenceRejected("identity not public before formation")
        elif (identity["known_at_upper"] is not None or
              identity["identity_proof_sha256"] is not None):
            raise EvidenceRejected("unresolved identity cannot claim binding")
        for field in ("security_id", "issuer_id", "cross_period_equivalence"):
            if identity[field] is not None:
                _synthetic_id(identity[field])
        if identity["mapping_proof_sha256"] is not None:
            _hash(identity["mapping_proof_sha256"])
        by_identity[identity["member_id"]] = identity
    by_member, assertions = {}, set()
    for row in memberships:
        _fields(row, _ROW, "membership")
        _synthetic_id(row["member_id"])
        if row["member_kind"] != "LISTING" or row["status"] not in _STATUSES:
            raise EvidenceRejected("invalid typed membership")
        if row["member_id"] in by_member:
            raise EvidenceRejected("duplicate membership")
        ids = row["assertion_ids"]
        if type(ids) is not list:
            raise EvidenceRejected("malformed assertions")
        for aid in ids:
            _synthetic_id(aid)
        if len(ids) != len(set(ids)):
            raise EvidenceRejected("duplicate assertions")
        for aid in ids:
            if aid in assertions:
                raise EvidenceRejected("assertion reused by different members")
            assertions.add(aid)
        if row["status"] in ("MEMBER", "NOT_MEMBER"):
            if not ids:
                raise EvidenceRejected("explicit positive/negative evidence required")
            _hash(row["source_doc_digest"])
            _hash(row["chain_digest"])
            if _time(row["known_at_upper"]) > asof or _time(row["known_at_upper"]) >= ftime:
                raise EvidenceRejected("late membership evidence")
        elif ids or any(row[k] is not None for k in
                        ("known_at_upper", "source_doc_digest", "chain_digest")):
            raise EvidenceRejected("uncertain state cannot pretend source assertion")
        by_member[row["member_id"]] = row
    _hash(envelope["content_hash"])
    content = {k: v for k, v in envelope.items() if k != "content_hash"}
    if not hmac.compare_digest(
            hashlib.sha256(_canonical(content)).hexdigest(), envelope["content_hash"]):
        raise EvidenceRejected("canonical content digest mismatch")
    return envelope


class SyntheticMembershipEvidence:
    """Immutable, invented-only inspection surface. No actual U1 formation."""

    def __init__(self, raw, request):
        if (type(raw) is not bytes or
                hashlib.sha256(raw).hexdigest() not in APPROVED_SYNTHETIC_BYTES):
            raise ContractUnverified("only pinned invented fixture bytes supported")
        env = _validate(raw, request)
        self._raw = raw
        self._query = _canonical(env["query"])
        self._rows = {x["member_id"]: x for x in env["memberships"]}
        self._identities = {x["member_id"]: x for x in env["identities"]}

    @property
    def request(self):
        return _json(self._query)

    @property
    def comparison_label(self):
        return LABEL

    def status(self, member_id):
        """Unknown/ambiguous/missing identity is UNAVAILABLE, never NOT_MEMBER."""
        if type(member_id) is not str:
            raise EvidenceRejected("typed member id required")
        item = self._rows.get(member_id)
        ident = self._identities.get(member_id)
        if (item is None or ident is None or
                ident["status"] != "BOUND" or ident["member_kind"] != "LISTING"):
            return "UNAVAILABLE"
        return item["status"] if item["status"] in ("MEMBER", "NOT_MEMBER") else "UNAVAILABLE"

    def dependent_join(self, member_id, field):
        """Only missing dependent issuer/security/equivalence join fails."""
        if field not in ("security_id", "issuer_id", "cross_period_equivalence"):
            raise EvidenceRejected("unsupported dependent join")
        if self.status(member_id) != "MEMBER":
            return "UNAVAILABLE"
        identity = self._identities[member_id]
        if identity["mapping_proof_sha256"] is None:
            return "UNAVAILABLE"
        return identity[field] or "UNAVAILABLE"


def open_synthetic_bundle(raw: bytes, request: dict) -> SyntheticMembershipEvidence:
    """Only preapproved invented fixture bytes; no path/network/vault adapter."""
    return SyntheticMembershipEvidence(raw, request)
