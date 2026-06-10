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


def scope_info():
    """The scope registry dict (engine-provided so the web layer reads no registry files)."""
    return _load("registry", "scope_registry.json")


def calibration_status():
    """Summarize Arabic calibration state from the registries (engine-provided).
    The web reads this — never the registry files — to show an honest badge."""
    mur = _load("registry", "rules.json")["rules"]
    ija = _load("registry", "rules_ijara.json")["rules"]
    gloss = _load("registry", "glossary.json")["entries"]
    mur_locked = all(r.get("arabic_review_status") == "locked" for r in mur)
    ija_pending = [r["id"] for r in ija if r.get("arabic_review_status") != "locked"]
    gloss_prov = [g["term_id"] for g in gloss if g.get("status") == "provisional"]
    return {
        "murabaha_locked": mur_locked,
        "ijara_pending": ija_pending,
        "glossary_provisional": gloss_prov,
        "summary_en": ("Murabaha Arabic: calibrated (locked). "
                       + (f"Ijara Arabic ({', '.join(ija_pending)}) + glossary "
                          f"({len(gloss_prov)} provisional terms): Arabic pending expert calibration."
                          if ija_pending or gloss_prov else "All Arabic calibrated.")),
        "summary_ar": ("عربية المرابحة: مُعايَرة (مُثبَّتة). "
                       + ("عربية الإجارة والمصطلحات المضافة: بانتظار معايرة الخبير."
                          if ija_pending or gloss_prov else "كل العربية مُعايَرة.")),
    }


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
    text = corpus_loader.load(path)   # corpus files must carry the SYNTHETIC label (fail closed)
    return run_text(text, os.path.basename(path), rules, defer, glossary, seam)


def run_text(text, source_label="(input)", rules=None, defer=None, glossary=None, seam=None):
    """Run the pipeline on raw contract TEXT (e.g. a web upload/paste). Same engine
    as run_contract, minus the corpus SYNTHETIC-label requirement. Content still
    passes the input rail (injection-inert). Public, additive interface."""
    if rules is None:
        rules, defer, glossary = load_registry()
    ijara_rules, ijara_defer, scope_reg = load_stage2()
    merged_defer = {"entries": defer["entries"] + ijara_defer["entries"]}
    defer_lookup = {e["id"]: e for e in merged_defer["entries"]}
    rules_by_type = {"murabaha": rules, "ijara": ijara_rules}
    if seam is None:
        seam = model_seam.make_seam()

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
        "file": source_label,
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
    text = corpus_loader.load(path)
    return generate_for_text(text, os.path.basename(path), rules, defer, glossary, seam, authoritative_lang)


def generate_for_text(text, source_label="(input)", rules=None, defer=None, glossary=None, seam=None, authoritative_lang="ar"):
    """Stage 3: run + generate memo/matrix from raw TEXT (web). Additive interface."""
    if rules is None:
        rules, defer, glossary = load_registry()
    if seam is None:
        seam = model_seam.make_seam()
    res = run_text(text, source_label, rules, defer, glossary, seam)
    findings, structure = res["findings"], res["structure"]

    memo = memo_generator.generate(structure, findings, rules, defer, glossary, seam,
                                   authoritative_lang, source_label,
                                   contract_type=res["primary_type"])
    matrix = matrix_generator.generate(findings, authoritative_lang)

    gate = never_rules_guard.check_prose(memo["generated_prose"] + matrix["generated_prose"])
    if gate:
        raise RuntimeError("never-rules GENERATION gate tripped (fail closed): " + "; ".join(gate))

    wm = memo["watermark"]
    for doc_name, render_md in (("memo", memo["render_md"]), ("matrix", matrix["render_md"])):
        if wm["ar"] not in render_md or wm["en"] not in render_md:
            raise RuntimeError(f"watermark missing from {doc_name} render — generation fails closed")

    return {"file": source_label, "seam_mode": res["seam_mode"],
            "classification": res["classification"], "covered_types": res["covered_types"],
            "primary_type": res["primary_type"],
            "structure": structure, "findings": findings, "memo": memo, "matrix": matrix}
