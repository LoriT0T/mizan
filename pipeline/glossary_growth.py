"""Concern: turn a detected unknown term-of-art into a PROVISIONAL glossary
candidate, gated fail-closed.

This is the runtime trigger of the Stage-1a growth protocol:
  (a) research the term on demand against public authoritative sources [done by
      the caller; sources passed in — live web research is the on-demand step];
  (b) propose a bilingual entry with its grounding cited;
  (c) append with status: provisional -> routed to the consolidated review list;
  (d) a candidate that conflicts with a locked rendering FAILS CLOSED.

The fail-closed gate is INJECTED (`gate` = Stage-1a glossary_checks.check_candidate)
so this unit imports no sibling. Entry point:
  `propose(term_ar, term_en, def_ar, def_en, sources, existing, gate) -> dict`
returning {candidate, accepted, reasons}. accepted is False (and the candidate
is withheld) whenever the gate returns any reason.
"""


def build_candidate(term_ar, term_en, def_ar, def_en, sources, term_id):
    return {
        "term_id": term_id,
        "canonical_ar": term_ar,
        "canonical_en": term_en,
        "definition_ar": def_ar,
        "definition_en": def_en,
        "status": "provisional",
        "origin": "growth-protocol",
        "review_routing": "Consolidated Arabic review list — provisional; awaiting the principal's calibration to lock.",
        "provenance": {"sources": list(sources), "grounding_basis": "unverified"},
    }


def propose(term_ar, term_en, def_ar, def_en, sources, existing, gate, term_id="G-PROV"):
    candidate = build_candidate(term_ar, term_en, def_ar, def_en, sources, term_id)
    reasons = gate(candidate, existing)  # injected Stage-1a fail-closed collision gate
    return {"candidate": candidate, "accepted": not reasons, "reasons": reasons}
