"""Concern: the scope decision — what Mizan covers, and honest out-of-scope.

Reads the scope registry (the single source of truth) and, given a classifier
result, returns which types Mizan will check (covered + calibrated) and the
explicit OUT-OF-SCOPE findings for everything it recognizes-but-does-not-cover
or does-not-recognize. It NEVER fabricates a rule and NEVER applies one type's
rules to another type.

Out-of-scope findings carry status "out_of_scope" (an allowed non-verdict status)
and the scope registry's bilingual finding text with [X] filled in. For a
recognized-but-not-covered type (tawarruq) the finding surfaces the routed defer
positions (D3). Imports no sibling. Entry points:
  `load_scope(path) -> dict`
  `assess(classification, scope_reg, defer_lookup=None) -> (covered_types, oos_findings)`
"""
import json


def load_scope(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _status_of(scope_reg, ctype):
    for c in scope_reg["coverage"]:
        if c["type"] == ctype:
            return c
    return None


def _oos_finding(scope_reg, component_label, defer_entry=None):
    txt = scope_reg["out_of_scope_finding_text"]
    f = {
        "rule_id": None,
        "status": "out_of_scope",
        "contract_element": f"{component_label} component",
        "component": component_label,
        "quote": "",
        "citations": [],
        "violation_pattern": None,
        "positions": None,
        "routing_ar": "يُحال إلى عالمٍ شرعيٍّ مؤهّل.",
        "routing_en": "Routed to a qualified Sharia scholar.",
        "missing_fact": None,
        "note_ar": txt["ar"].replace("[X]", component_label),
        "note_en": txt["en"].replace("[X]", component_label),
        "note": txt["en"].replace("[X]", component_label),
    }
    if defer_entry:
        f["positions"] = [{"authority": p["authority"], "position_ar": p["position_ar"],
                           "position_en": p["position_en"], "citation": p["citation"]} for p in defer_entry.get("positions", [])]
        f["routing_ar"] = defer_entry.get("routing_ar", f["routing_ar"])
        f["routing_en"] = defer_entry.get("routing_en", f["routing_en"])
    return f


def assess(classification, scope_reg, defer_lookup=None):
    """defer_lookup: dict id->entry (merged defer registers) for routed positions."""
    defer_lookup = defer_lookup or {}
    covered_types, oos = [], []
    for t in classification.get("types", []):
        c = _status_of(scope_reg, t)
        if c and c["status"] == "covered-and-calibrated":
            covered_types.append(t)
        elif c and c["status"] == "recognized-not-covered":
            entry = defer_lookup.get(c.get("defer_ref"))
            oos.append(_oos_finding(scope_reg, t, defer_entry=entry))
        elif t == "unrecognized":
            oos.append(_oos_finding(scope_reg, "unrecognized"))
    for comp in classification.get("unrecognized_components", []):
        oos.append(_oos_finding(scope_reg, comp))
    return covered_types, oos
