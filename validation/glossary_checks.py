"""Concern: the glossary never silently holds two renderings of one term.

Invariants:
  G1  one rendering per term — canonical_ar unique, canonical_en unique, and no
      Arabic form mapping to two English renderings (or vice versa);
  G2  provisional routing — every status:'provisional' entry carries a
      review_routing (it must be routed to the consolidated review list);
  G3  unique term ids;
  G4  append-only history — every glossary term_id is recorded in the history
      'added' lists (the glossary is versioned; nothing appears unrecorded).

Plus the FAIL-CLOSED collision gate a future appender must call BEFORE adding:
  `check_candidate(candidate, existing_entries) -> list[str]`
A non-empty return means: do NOT append; surface for human resolution.

'Locked rendering' = any entry whose status is 'locked' or
'locked-pending-calibration' (seed). Stdlib only. No sibling imports.
"""

_LOCKED = {"locked", "locked-pending-calibration"}


def check(glossary_data, history_data):
    errors = []
    entries = glossary_data.get("entries", [])

    ar_to_en, en_to_ar, ids = {}, {}, set()
    for g in entries:
        gid = g.get("term_id", "<no-id>")
        ar, en = g.get("canonical_ar"), g.get("canonical_en")

        if gid in ids:
            errors.append(f"G3 {gid}: duplicate term_id")
        ids.add(gid)

        if ar in ar_to_en and ar_to_en[ar] != en:
            errors.append(f"G1 {gid}: Arabic '{ar}' already renders as '{ar_to_en[ar]}', not '{en}'")
        ar_to_en.setdefault(ar, en)

        if en in en_to_ar and en_to_ar[en] != ar:
            errors.append(f"G1 {gid}: English '{en}' already maps to '{en_to_ar[en]}', not '{ar}'")
        en_to_ar.setdefault(en, ar)

        if g.get("status") == "provisional" and not g.get("review_routing"):
            errors.append(f"G2 {gid}: provisional entry without review_routing")

    # G4 — append-only history coverage
    recorded = set()
    for v in history_data.get("versions", []):
        recorded.update(v.get("added", []))
    for g in entries:
        gid = g.get("term_id", "<no-id>")
        if gid not in recorded:
            errors.append(f"G4 {gid}: not recorded in glossary history (append-only violation)")

    return errors


def check_candidate(candidate, existing_entries):
    """Fail-closed gate: returns reasons the candidate may NOT be appended.
    Empty list == safe to append."""
    reasons = []
    cid = candidate.get("term_id", "<no-id>")
    car, cen = candidate.get("canonical_ar"), candidate.get("canonical_en")

    for g in existing_entries:
        if g.get("term_id") == cid:
            reasons.append(f"COLLISION {cid}: term_id already exists")
        locked = g.get("status") in _LOCKED
        if g.get("canonical_ar") == car and g.get("canonical_en") != cen:
            tag = "locked " if locked else ""
            reasons.append(f"COLLISION {cid}: Arabic '{car}' conflicts with {tag}entry {g.get('term_id')} "
                           f"rendered '{g.get('canonical_en')}' (candidate says '{cen}')")
        if g.get("canonical_en") == cen and g.get("canonical_ar") != car:
            tag = "locked " if locked else ""
            reasons.append(f"COLLISION {cid}: English '{cen}' conflicts with {tag}entry {g.get('term_id')} "
                           f"Arabic '{g.get('canonical_ar')}' (candidate says '{car}')")

    if candidate.get("status") == "provisional" and not candidate.get("review_routing"):
        reasons.append(f"COLLISION {cid}: provisional candidate must declare review_routing before append")

    return reasons
