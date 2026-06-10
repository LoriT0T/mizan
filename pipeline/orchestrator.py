"""Orchestrator — wiring only. Owns NO concern logic.

Loads the locked registry (READ-ONLY), wires the units into the pipeline:
  corpus_loader.load -> input_rail (via extractor) -> model_seam (gated) ->
  extractor -> checker -> never_rules_guard (fail closed).
The registry is never mutated here. The never-rules guard runs on every result;
if it ever trips, the run fails closed (the checker is not allowed to rule).
"""
import json
import os

import input_rail
import model_seam
import extractor
import checker
import never_rules_guard
import corpus_loader
import memo_generator
import matrix_generator
import contract_type_classifier
import scope

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# A small curated watchlist of Islamic-finance terms of art the extractor flags
# when present but absent from the glossary -> routes to the growth protocol.
WATCHLIST = ["مرابحة", "تورق", "التورق", "استصناع", "سلم", "صكوك", "إجارة", "عربون",
             "تولية", "وضيعة", "عينة", "مساومة", "استجرار", "الاستجرار",
             "murabaha", "tawarruq", "istisna", "salam", "sukuk", "ijara",
             "arboun", "tawliyah", "wadiah", "inah", "musawamah", "istijrar"]


def _load(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return json.load(f)


def load_registry():
    return _load("registry", "rules.json"), _load("registry", "defer_register.json"), _load("registry", "glossary.json")


def load_stage2():
    """Ijara registry + scope registry (Stage 2). Murabaha files are untouched."""
    ijara_rules = _load("registry", "rules_ijara.json")
    ijara_defer = _load("registry", "defer_register_ijara.json")
    scope_reg = scope.load_scope(os.path.join(ROOT, "registry", "scope_registry.json"))
    return ijara_rules, ijara_defer, scope_reg


def glossary_terms(glossary):
    terms = set()
    for g in glossary["entries"]:
        terms.add(g["canonical_ar"])
        terms.add(g["canonical_en"])
    return terms


def run_contract(path, rules=None, defer=None, glossary=None, seam=None):
    if rules is None:
        rules, defer, glossary = load_registry()
    ijara_rules, ijara_defer, scope_reg = load_stage2()
    merged_defer = {"entries": defer["entries"] + ijara_defer["entries"]}
    defer_lookup = {e["id"]: e for e in merged_defer["entries"]}
    rules_by_type = {"murabaha": rules, "ijara": ijara_rules}
    if seam is None:
        seam = model_seam.make_seam()

    text = corpus_loader.load(path)
    structure = extractor.extract(text, input_rail, seam, glossary_terms(glossary), WATCHLIST)
    classification = contract_type_classifier.classify(text, seam)
    covered, oos_findings = scope.assess(classification, scope_reg, defer_lookup)

    findings = []
    if covered:
        if not structure["extraction_complete"]:
            findings += checker.check(structure, rules, merged_defer)    # single fail-closed finding
        else:
            for t in covered:                                            # covered parts checked per type
                findings += checker.check(structure, rules_by_type[t], merged_defer)
    # Uncovered/unrecognized parts honestly flagged (no rule fabricated/applied).
    findings += oos_findings

    guard_errors = never_rules_guard.check(findings)
    if guard_errors:
        raise RuntimeError("never-rules guard tripped (fail closed): " + "; ".join(guard_errors))
    return {
        "file": os.path.basename(path),
        "seam_mode": "model-available" if seam.available() else "NO-KEY (deterministic)",
        "structure": structure,
        "classification": classification,
        "covered_types": covered,
        "primary_type": covered[0] if covered else "unrecognized",
        "findings": findings,
        "guard": "passed (no verdict language; statuses non-verdict)",
    }


def generate_for_contract(path, rules=None, defer=None, glossary=None, seam=None, authoritative_lang="ar"):
    """Stage 1c: run the 1b pipeline, then generate the memo + matrix, gated.

    The never-rules guard runs over ALL generated/model-drafted connective prose
    (memo + matrix) as a GENERATION gate; the watermark must be present in the
    rendered memo. Either failing fails the generation closed.
    """
    if rules is None:
        rules, defer, glossary = load_registry()
    if seam is None:
        seam = model_seam.make_seam()
    res = run_contract(path, rules, defer, glossary, seam)
    findings, structure = res["findings"], res["structure"]

    memo = memo_generator.generate(structure, findings, rules, defer, glossary, seam,
                                   authoritative_lang, os.path.basename(path),
                                   contract_type=res["primary_type"])
    matrix = matrix_generator.generate(findings, authoritative_lang)

    gate = never_rules_guard.check_prose(memo["generated_prose"] + matrix["generated_prose"])
    if gate:
        raise RuntimeError("never-rules GENERATION gate tripped (fail closed): " + "; ".join(gate))

    wm = memo["watermark"]
    for doc_name, render_md in (("memo", memo["render_md"]), ("matrix", matrix["render_md"])):
        if wm["ar"] not in render_md or wm["en"] not in render_md:
            raise RuntimeError(f"watermark missing from {doc_name} render — generation fails closed")

    return {"file": os.path.basename(path), "seam_mode": res["seam_mode"],
            "structure": structure, "findings": findings, "memo": memo, "matrix": matrix}
