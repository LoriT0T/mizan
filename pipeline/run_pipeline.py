"""CLI runner — demonstrates the full pipeline on the synthetic corpus.

Usage:
  python3 run_pipeline.py                 # run every corpus contract, summary view
  python3 run_pipeline.py <file> --full   # one contract, full structured detail

Wiring only (delegates to orchestrator). Honest framing printed up top.
"""
import json
import os
import sys

import orchestrator

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(os.path.dirname(HERE), "corpus")

BANNER = ("Mizan Stage 1b — research aid for a qualified scholar (SSB). "
          "Findings FLAG/IDENTIFY/CITE; the system does NOT determine Sharia compliance. "
          "Synthetic corpus; not validated by any scholar or bank.")


def _print_structure(s):
    print(f"    language: {s['language']} · extraction_complete: {s['extraction_complete']} · method: {s['extraction_method']}")
    if not s["extraction_complete"]:
        print(f"    STATUS: {s.get('status')} · unresolved: {s.get('unresolved')}")
        return
    a = s["asset"]
    print(f"    asset: present={a['present']} permissible={a['permissible']} exists={a['exists']} | {a['quote'][:70]}")
    o, ag = s["ownership"], s["agency"]
    print(f"    R1: acquires_before_sale={o['bank_acquires_before_sale']} bears_risk={o['bank_bears_ownership_risk']} "
          f"buying_agent={ag['customer_is_buying_agent']} sale_before_possession={o['sale_before_possession']}")
    p = s["price_terms"]
    print(f"    R2: cost_disclosed={p['cost_disclosed']} markup_disclosed={p['markup_disclosed']} price_fixed={p['price_fixed_at_contract']}")
    lp = s["late_payment"]
    print(f"    R5: penalty_destination={lp['penalty_destination']} markup_increase_on_late={lp['markup_increase_on_late']}")
    w = s["wad_promise"]
    print(f"    R6: wad_present={w['present']} type={w['type']} binding={w['binding_language']}")
    po = s["prior_ownership"]
    print(f"    R4: already_customers={po['asset_already_customers']} inah_buyback={po['inah_buyback']}")
    if s["unknown_terms"]:
        print(f"    unknown_terms -> growth protocol: {s['unknown_terms']}")
    if s["injection_spans"]:
        print(f"    injection spans recorded (inert): {[h['tag'] for h in s['injection_spans']]}")


def _print_findings(findings):
    for f in findings:
        line = f"      [{f['rule_id']}] {f['status'].upper()}"
        if f.get("contract_element"):
            line += f" · {f['contract_element']}"
        print(line)
        layers = ", ".join(f"{c['layer']}:{c['ref'][:48]}" for c in f["citations"])
        if layers:
            print(f"          cite: {layers}")
        if f.get("quote"):
            print(f"          quote: {f['quote'][:90]}")
        if f.get("violation_pattern"):
            print(f"          matched violation pattern (EN): {f['violation_pattern']['en'][:90]}")
        if f.get("missing_fact"):
            print(f"          missing fact: {f['missing_fact']}")
        if f.get("positions"):
            print(f"          DEFERRAL — positions surfaced:")
            for p in f["positions"]:
                print(f"             · {p['authority']}: {p['position_en'][:80]} [{p['citation'][:48]}]")
            print(f"          routing: {f['routing_en']}")


def _corpus_paths():
    paths = []
    for d in (CORPUS, os.path.join(CORPUS, "stage2")):
        if os.path.isdir(d):
            paths += [os.path.join(d, fn) for fn in os.listdir(d) if fn.endswith(".txt")]
    return sorted(paths, key=os.path.basename)


def run_all():
    print("=" * 78)
    print(BANNER)
    print("=" * 78)
    rules, defer, glossary = orchestrator.load_registry()
    for path in _corpus_paths():
        res = orchestrator.run_contract(path, rules, defer, glossary)
        cls = res.get("classification", {})
        print(f"\n### {os.path.basename(path)}  [{res['seam_mode']}] · classified={cls.get('types')} "
              f"unrecognized={cls.get('unrecognized_components')} · covered(checked)={res.get('covered_types')}")
        _print_structure(res["structure"])
        print(f"    findings (guard {res['guard']}):")
        _print_findings(res["findings"])
    print("\n" + "=" * 78)
    print("END. No verdicts issued. Contested matters deferred to the SSB.")


def run_one(fn):
    path = next((p for d in (CORPUS, os.path.join(CORPUS, "stage2"))
                 for p in [os.path.join(d, fn)] if os.path.exists(p)), os.path.join(CORPUS, fn))
    res = orchestrator.run_contract(path)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] not in ("--full",):
        run_one(sys.argv[1])
    else:
        run_all()
