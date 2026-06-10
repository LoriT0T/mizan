"""Concern: domain integrity of the registry as a whole.

Asserts the cross-cutting invariants the schema alone cannot:
  I1  every rule has at least one source with a layer + a citation ref;
  I2  every rule entry is bilingual-complete (ar + en on rule text, title,
      and every satisfied_by / violated_by item);
  I3  every contested rule appears in the defer register (via defer_ref, and
      that defer id exists);
  I4  every defer entry carries >= 2 cited positions and a routing;
  I5  provenance discipline preserved: a glossary entry grounded 'provisional'
      must NOT be 'locked' (provisional in -> provisional/locked-pending out,
      never silently promoted).

Stdlib only. No sibling imports. Entry point:
`check(rules_data, defer_data, glossary_data) -> list[str]`.
"""


def check(rules_data, defer_data, glossary_data):
    errors = []
    rules = rules_data.get("rules", [])
    defer_ids = {e["id"] for e in defer_data.get("entries", [])}

    for r in rules:
        rid = r.get("id", "<no-id>")

        # I1 — layer + citation present
        srcs = r.get("sources", [])
        if not srcs:
            errors.append(f"I1 {rid}: no sources (needs a layer + citation)")
        for s in srcs:
            if not s.get("layer"):
                errors.append(f"I1 {rid}: a source is missing its layer")
            if not s.get("ref"):
                errors.append(f"I1 {rid}: a source is missing its citation ref")

        # I2 — bilingual completeness
        for field in ("title_ar", "title_en", "rule_ar", "rule_en"):
            if not r.get(field):
                errors.append(f"I2 {rid}: missing {field}")
        for coll in ("satisfied_by", "violated_by"):
            for i, item in enumerate(r.get(coll, [])):
                if not item.get("ar") or not item.get("en"):
                    errors.append(f"I2 {rid}: {coll}[{i}] not bilingual-complete")

        # I3 — contested rule must route to an existing defer entry
        if r.get("status") == "contested":
            dref = r.get("defer_ref")
            if not dref:
                errors.append(f"I3 {rid}: contested but has no defer_ref")
            elif dref not in defer_ids:
                errors.append(f"I3 {rid}: defer_ref '{dref}' not in defer register")

    # I4 — defer entries well-formed
    for e in defer_data.get("entries", []):
        eid = e.get("id", "<no-id>")
        positions = e.get("positions", [])
        if len(positions) < 2:
            errors.append(f"I4 {eid}: needs >= 2 positions, has {len(positions)}")
        if not e.get("routing_en") or not e.get("routing_ar"):
            errors.append(f"I4 {eid}: missing bilingual routing")
        for i, p in enumerate(positions):
            if not p.get("citation"):
                errors.append(f"I4 {eid}: position[{i}] missing citation")

    # I5 — provenance discipline on glossary
    for g in glossary_data.get("entries", []):
        gid = g.get("term_id", "<no-id>")
        grounded = g.get("grounding", {}).get("established_or_provisional")
        if grounded == "provisional" and g.get("status") == "locked":
            errors.append(f"I5 {gid}: grounded provisional but status 'locked' (silent promotion)")

    return errors
