"""Concern: the checker FLAGS, IDENTIFIES, CITES — it never RULES.

No checker-authored output may assert a permissibility verdict. Enforced two
ways, fail-closed:
  N1  status is one of {satisfied, violated, indeterminate, deferral} — never a
      permissibility word;
  N2  checker-AUTHORED prose fields (status, note, summary) contain no verdict
      token (حلال / حرام / permissible / impermissible / halal / haram /
      compliant / non-compliant).

Scope: only the checker's own fields are scanned. Attributed/quoted registry
text (the `quote`, `citations`, `positions` fields) is EXEMPT — it legitimately
contains words like "impermissible" inside a cited scholarly position, which the
checker reports without adopting. Quoting a position is not ruling.

Stdlib only. No sibling imports. Entry point: `check(findings) -> list[str]`.
"""
import re

ALLOWED_STATUS = {"satisfied", "violated", "indeterminate", "deferral"}
_VERDICT = re.compile(r"\b(permissible|impermissible|halal|haram|sharia[- ]?compliant|non[- ]?compliant|compliant)\b"
                      r"|حلال|حرام", re.IGNORECASE)
_AUTHORED_FIELDS = ("status", "note", "summary")


def check_prose(segments):
    """Generation gate (Stage 1c): scan GENERATED connective prose for verdict
    language. `segments` is the list of strings the generator authored or the
    model drafted — NOT the verbatim contract quotes and NOT the registry
    citations/positions (those are assembled deterministically and are exempt by
    construction, never placed in this list). Returns reasons (empty == clean).
    A non-empty return means: fail the generation closed."""
    errors = []
    for i, seg in enumerate(segments):
        if isinstance(seg, str) and _VERDICT.search(seg):
            errors.append(f"N3 generated-prose[{i}]: verdict language in generated/model-drafted prose: {seg[:80]!r}")
    return errors


def check(findings):
    errors = []
    for i, f in enumerate(findings):
        status = f.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"N1 finding[{i}] ({f.get('rule_id')}): status '{status}' is not an allowed non-verdict status {sorted(ALLOWED_STATUS)}")
        for field in _AUTHORED_FIELDS:
            val = f.get(field, "")
            if isinstance(val, str) and _VERDICT.search(val):
                errors.append(f"N2 finding[{i}] ({f.get('rule_id')}): checker-authored field '{field}' contains verdict language: {val!r}")
    return errors
