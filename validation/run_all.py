"""Orchestrator — wiring only. Owns NO concern logic.

Loads the registry data files and the JSON schemas, runs every validation unit,
aggregates results, and FAILS CLOSED (exit code 1) on any violation. This is the
gate the foundation requires: registry and glossary edits do not stand if
validation fails.

Reads from ../registry and ../schemas relative to this file.
"""
import json
import os
import sys

import schema_validator
import integrity_checks
import citation_guard
import glossary_checks
import synthetic_corpus_guard

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def _load(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return json.load(f)


def main():
    rules = _load("registry", "rules.json")
    defer = _load("registry", "defer_register.json")
    glossary = _load("registry", "glossary.json")
    history = _load("registry", "glossary_history.json")
    rule_schema = _load("schemas", "rule.schema.json")
    defer_schema = _load("schemas", "defer.schema.json")
    gloss_schema = _load("schemas", "glossary.schema.json")

    # Stage 2: the Ijara registry (separate files; Murabaha rules stay byte-identical).
    ijara_rules = _load("registry", "rules_ijara.json") if os.path.exists(os.path.join(ROOT, "registry", "rules_ijara.json")) else {"rules": []}
    ijara_defer = _load("registry", "defer_register_ijara.json") if os.path.exists(os.path.join(ROOT, "registry", "defer_register_ijara.json")) else {"entries": []}
    # Merged defer view (so a contested rule's defer_ref to D1/D2 OR D4/D5 resolves).
    merged_defer = {"entries": defer["entries"] + ijara_defer["entries"]}

    results = []  # (check_name, [errors])

    schema_errs = []
    for r in rules["rules"] + ijara_rules["rules"]:
        schema_errs += schema_validator.validate(r, rule_schema, f"rule:{r.get('id')}")
    for e in defer["entries"] + ijara_defer["entries"]:
        schema_errs += schema_validator.validate(e, defer_schema, f"defer:{e.get('id')}")
    for g in glossary["entries"]:
        schema_errs += schema_validator.validate(g, gloss_schema, f"gloss:{g.get('term_id')}")
    results.append(("schema_validator", schema_errs))

    # Integrity: Murabaha rules vs main defer; Ijara rules vs merged defer (D1/D2 reuse + D4/D5).
    integ = integrity_checks.check(rules, defer, glossary) + integrity_checks.check(ijara_rules, merged_defer, glossary)
    results.append(("integrity_checks", integ))
    results.append(("citation_guard", citation_guard.check(rules, merged_defer, glossary) + citation_guard.check(ijara_rules, ijara_defer, {"entries": []})))
    results.append(("glossary_checks", glossary_checks.check(glossary, history)))
    results.append(("synthetic_corpus_guard", synthetic_corpus_guard.check(rules) + synthetic_corpus_guard.check(ijara_rules)))

    total = 0
    print("=" * 64)
    print("Mizan Stage 1a — Registry validation suite")
    print("=" * 64)
    print(f"Loaded: {len(rules['rules'])} Murabaha + {len(ijara_rules['rules'])} Ijara rules · "
          f"{len(defer['entries']) + len(ijara_defer['entries'])} defer entries · "
          f"{len(glossary['entries'])} glossary terms")
    print("-" * 64)
    for name, errs in results:
        status = "PASS" if not errs else f"FAIL ({len(errs)})"
        print(f"  {name:<26} {status}")
        for e in errs:
            print(f"      - {e}")
        total += len(errs)
    print("-" * 64)
    if total == 0:
        print("ALL CHECKS PASS — registry is valid and stands.")
        return 0
    print(f"VALIDATION FAILED — {total} violation(s). Edits fail closed; registry does NOT stand.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
