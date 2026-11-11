"""Pure, invented-only reference oracle for the Study 4 P0 policy."""

import hashlib
import json


POLICY_SHA256 = "92dec31d8a14e6ed883cd6bec48b3f345965d8a2008cb6f168354fd5796cb9f6"


class Denied(RuntimeError):
    """A fixed, payload-free denial."""


def canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("ascii")


def fixture_for(slot):
    return canonical({"fixture": "S4-INVENTED-ONLY", "slot": slot})


def seal_intent_for(slot):
    return canonical({
        "score": 17,
        "action": "INVENTED_ACTION",
        "provenance": {
            "slot": slot,
            "fixture_sha256": hashlib.sha256(fixture_for(slot)).hexdigest(),
            "policy_sha256": POLICY_SHA256,
        },
    })


class Oracle:
    """One synthetic occurrence. It owns no I/O handles or DSA imports."""

    def __init__(self, policy, profile, observed_launch, slot):
        if type(policy) is not bytes or hashlib.sha256(policy).hexdigest() != POLICY_SHA256:
            raise Denied("policy denied")
        if type(profile) is not str or profile != "invented_oracle":
            raise Denied("profile denied")
        rules = json.loads(policy)["profiles"][profile]
        if (
            type(observed_launch) is not bytes
            or observed_launch != canonical(rules["observed_launch"])
            or type(slot) is not int
            or not 1 <= slot <= 999
        ):
            raise Denied("preflight denied")

        self._allowed = frozenset(rules["allow"])
        self._slot = slot
        self._read = False
        self._staged = None
        self._closed = False
        self._denials = 0
        self._effects = []

    @property
    def denials(self):
        return self._denials

    @property
    def effects(self):
        return tuple(self._effects)

    def _deny(self):
        self._denials += 1
        self.abort()
        raise Denied("capability denied")

    def request(self, capability, payload):
        """Check the operation before any modeled effect, including reads."""
        if (
            self._closed
            or type(capability) is not str
            or capability not in self._allowed
            or type(payload) is not bytes
        ):
            self._deny()

        if capability == "fixture.read":
            if self._read or payload != fixture_for(self._slot):
                self._deny()
            self._read = True
            self._effects.append("fixture.read")
            return fixture_for(self._slot)

        if capability == "seal.stage":
            if not self._read or self._staged is not None or payload != seal_intent_for(self._slot):
                self._deny()
            self._staged = payload
            self._effects.append("seal.stage")
            return None

        self._deny()

    def abort(self):
        """Drop pending output on a miss, exception, or policy violation."""
        self._closed = True
        self._staged = None

    def finish(self):
        """Supervisor-only: obtain a one-shot in-memory seal intent."""
        pending = self._staged
        self.abort()
        if pending is not None:
            self._effects.append("seal.release")
        return pending
