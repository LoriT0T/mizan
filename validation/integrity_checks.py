"""Concern: domain integrity of the registry as a whole.

Asserts the cross-cutting invariants the schema alone cannot:
  I1  every rule has at least one source with a layer + a citation ref;
  I2  every rule entry is bilingual-complete (ar + en on rule text, title,
      and every satisfied_by / violated_by item);
  I3  every contested rule appears in the defer register (via defer_ref, and
      that defer id exists);
  I4  every defer entry carries >= 2 cited positions and a routing;
  I5  axis hygiene (the anti-conflation guarantee): the rule-status axis
      (established|contested), the provenance grounding-basis axis
      (grounded|unverified), and the glossary lifecycle axis
      (locked-pending-calibration|provisional|locked) use PAIRWISE-DISJOINT
      vocabularies, and every value sits in its own axis. So 'established'
      can only ever mean rule status, never a sourcing label;
  I6  L1 hygiene: every source on layer L1 references CBK or the Higher
      Committee ONLY (judicial practice belongs on layer LJ, AAOIFI on L3).

Stdlib only. No sibling imports. Entry point:
`check(rules_data, defer_data, glossary_data) -> list[str]`.
"""

# Three independent axes — their vocabularies must never overlap (this is what
# makes them impossible to confuse at a glance).
STATUS_VOCAB = {"established", "contested"}                                   # rule Sharia-clarity
GROUNDING_VOCAB = {"grounded", "unverified"}                                  # provenance sourcing strength
GLOSSARY_LIFECYCLE = {"locked-pending-calibration", "provisional", "locked"}  # human-calibration lifecycle
# Enforced as a load-time invariant so a future edit cannot reintroduce overlap:
assert STATUS_VOCAB.isdisjoint(GROUNDING_VOCAB)
assert STATUS_VOCAB.isdisjoint(GLOSSARY_LIFECYCLE)
assert GROUNDING_VOCAB.isdisjoint(GLOSSARY_LIFECYCLE)


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

        # I5 — axis hygiene (rule status + provenance grounding_basis)
        if r.get("status") not in STATUS_VOCAB:
            errors.append(f"I5 {rid}: status '{r.get('status')}' not in the rule-status axis {sorted(STATUS_VOCAB)}")
        gb = r.get("provenance", {}).get("grounding_basis")
        if gb not in GROUNDING_VOCAB:
            errors.append(f"I5 {rid}: provenance.grounding_basis '{gb}' not in the grounding axis {sorted(GROUNDING_VOCAB)}")

        # I6 — L1 contains only CBK / Higher Committee
        for s in srcs:
            if s.get("layer") == "L1" and not ("CBK" in s.get("ref", "") or "Higher Committee" in s.get("ref", "")):
                errors.append(f"I6 {rid}: L1 source ref '{s.get('ref')}' is not CBK/Higher Committee (judicial practice -> LJ, AAOIFI -> L3)")

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
        # I5 — defer provenance grounding_basis on its own axis
        gb = e.get("provenance", {}).get("grounding_basis")
        if gb not in GROUNDING_VOCAB:
            errors.append(f"I5 {eid}: provenance.grounding_basis '{gb}' not in the grounding axis {sorted(GROUNDING_VOCAB)}")

    # I5 — glossary axis hygiene (lifecycle status + provenance grounding_basis)
    for g in glossary_data.get("entries", []):
        gid = g.get("term_id", "<no-id>")
        if g.get("status") not in GLOSSARY_LIFECYCLE:
            errors.append(f"I5 {gid}: status '{g.get('status')}' not in the glossary lifecycle axis {sorted(GLOSSARY_LIFECYCLE)}")
        gb = g.get("provenance", {}).get("grounding_basis")
        if gb not in GROUNDING_VOCAB:
            errors.append(f"I5 {gid}: provenance.grounding_basis '{gb}' not in the grounding axis {sorted(GROUNDING_VOCAB)}")

    return errors
