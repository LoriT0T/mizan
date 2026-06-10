"""Demonstration: the guards FAIL CLOSED on the two cases the checkpoint names.

  1. The no-reproduced-text citation guard rejects a citation that embeds a
     verbatim standard passage.
  2. The glossary collision gate rejects a candidate whose Arabic form conflicts
     with a locked seed rendering — surfacing it for human resolution.

Run: python3 demo_failclosed.py  (exit 0 means BOTH guards correctly rejected).
"""
import json
import os
import sys

import citation_guard
import glossary_checks

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main():
    ok = True
    print("=" * 64)
    print("FAIL-CLOSED DEMONSTRATION")
    print("=" * 64)

    # --- 1. No-reproduced-text guard ---
    print("\n[1] Citation guard vs. reproduced AAOIFI clause text")
    reproduced = ('AAOIFI SS 8 clause 3/1/1: "' +
                  ("The Institution must purchase the asset and take possession of it "
                   "before selling it to the customer who has issued the purchase order, "
                   "bearing all the risks and rewards incidental to its ownership. ") + '"')
    print(f"    candidate citation (len={len(reproduced)}): {reproduced[:70]}...")
    errs = citation_guard.check_field(reproduced, "principle", "DEMO.principle")
    if errs:
        print("    -> REJECTED (fail closed):")
        for e in errs:
            print(f"         {e}")
    else:
        print("    -> ERROR: guard did NOT reject reproduced text")
        ok = False

    # --- 2. Glossary collision gate ---
    print("\n[2] Glossary collision gate vs. a conflicting rendering of a locked term")
    glossary = json.load(open(os.path.join(ROOT, "registry", "glossary.json"), encoding="utf-8"))
    existing = glossary["entries"]
    candidate = {
        "term_id": "G-900", "canonical_ar": "المرابحة", "canonical_en": "cost-markup contract",
        "status": "provisional", "review_routing": "review list",
    }
    print(f"    candidate: {candidate['canonical_ar']} -> '{candidate['canonical_en']}' "
          f"(locked seed G-001 already renders المرابحة -> 'Murabaha')")
    reasons = glossary_checks.check_candidate(candidate, existing)
    if reasons:
        print("    -> REJECTED (fail closed); surfaced for human resolution:")
        for r in reasons:
            print(f"         {r}")
    else:
        print("    -> ERROR: collision gate did NOT reject the conflicting candidate")
        ok = False

    print("\n" + "-" * 64)
    if ok:
        print("BOTH guards failed closed as required.")
        return 0
    print("A guard did NOT fail closed — investigate.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
