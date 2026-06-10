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


def glossary_terms(glossary):
    terms = set()
    for g in glossary["entries"]:
        terms.add(g["canonical_ar"])
        terms.add(g["canonical_en"])
    return terms


def run_contract(path, rules=None, defer=None, glossary=None, seam=None):
    if rules is None:
        rules, defer, glossary = load_registry()
    if seam is None:
        seam = model_seam.make_seam()
    text = corpus_loader.load(path)
    structure = extractor.extract(text, input_rail, seam, glossary_terms(glossary), WATCHLIST)
    findings = checker.check(structure, rules, defer)
    guard_errors = never_rules_guard.check(findings)
    if guard_errors:
        # The checker is structurally forbidden from ruling. If it ever does, stop.
        raise RuntimeError("never-rules guard tripped (fail closed): " + "; ".join(guard_errors))
    return {
        "file": os.path.basename(path),
        "seam_mode": "model-available" if seam.available() else "NO-KEY (deterministic)",
        "structure": structure,
        "findings": findings,
        "guard": "passed (no verdict language; statuses non-verdict)",
    }
