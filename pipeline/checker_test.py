"""Isolated test for checker. Imports only the unit + stdlib (+ reads the locked
registry JSON, which is the read-only source of truth).

Proves each seeded defect is caught by its rule, the clean contract passes,
R6 always defers, R4 boundary defers, and indeterminate/fail-closed paths hold.
"""
import copy
import json
import os
import unittest
import checker

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES = json.load(open(os.path.join(ROOT, "registry", "rules.json"), encoding="utf-8"))
DEFER = json.load(open(os.path.join(ROOT, "registry", "defer_register.json"), encoding="utf-8"))


def clean_structure():
    return {
        "extraction_complete": True,
        "asset": {"present": True, "quote": "Asset: a vehicle", "permissible": True, "permissible_quote": "permissible asset",
                  "exists": True, "exists_quote": "Asset: a vehicle"},
        "ownership": {"bank_acquires_before_sale": True, "acquire_quote": "Bank takes ownership and possession",
                      "bank_bears_ownership_risk": True, "risk_quote": "bearing all risks",
                      "sale_before_possession": None, "sale_before_quote": ""},
        "agency": {"customer_is_buying_agent": None, "quote": ""},
        "price_terms": {"cost_disclosed": True, "cost_quote": "disclosed cost", "markup_disclosed": True,
                        "markup_quote": "disclosed markup", "price_fixed_at_contract": True, "fixed_quote": "fixed at contract"},
        "late_payment": {"penalty_to_charity": True, "charity_quote": "to charity", "penalty_to_income": None,
                         "income_quote": "", "markup_increase_on_late": False, "increase_quote": "shall not increase",
                         "penalty_destination": "charity"},
        "wad_promise": {"present": True, "type": "unilateral", "binding_language": False, "quote": "unilateral promise"},
        "prior_ownership": {"asset_already_customers": False, "owned_quote": "not owned by the customer",
                            "inah_buyback": False, "inah_quote": "", "inah_boundary_ambiguous": False},
    }


def find(findings, rid):
    return next(f for f in findings if f["rule_id"] == rid)


class TestChecker(unittest.TestCase):
    def _check(self, s):
        return checker.check(s, RULES, DEFER)

    def test_clean_satisfies_R1_R5_and_defers_R6(self):
        fs = self._check(clean_structure())
        for rid in ("R1", "R2", "R3", "R4", "R5"):
            self.assertEqual(find(fs, rid)["status"], "satisfied", rid)
        r6 = find(fs, "R6")
        self.assertEqual(r6["status"], "deferral")
        self.assertTrue(r6["positions"])
        self.assertIn("SSB", r6["routing_en"])

    def test_R1_agency_violation_with_citation_layers(self):
        s = clean_structure(); s["agency"]["customer_is_buying_agent"] = True
        f = find(self._check(s), "R1")
        self.assertEqual(f["status"], "violated")
        self.assertTrue(f["violation_pattern"])
        layers = {c["layer"] for c in f["citations"]}
        self.assertTrue({"LJ", "L1", "L3", "L2"}.issubset(layers))

    def test_R2_undisclosed_violation(self):
        s = clean_structure(); s["price_terms"]["cost_disclosed"] = False; s["price_terms"]["markup_disclosed"] = False
        self.assertEqual(find(self._check(s), "R2")["status"], "violated")

    def test_R3_impermissible_violation(self):
        s = clean_structure(); s["asset"]["permissible"] = False
        self.assertEqual(find(self._check(s), "R3")["status"], "violated")

    def test_R4_inah_violation(self):
        s = clean_structure(); s["prior_ownership"]["inah_buyback"] = True; s["prior_ownership"]["asset_already_customers"] = True
        self.assertEqual(find(self._check(s), "R4")["status"], "violated")

    def test_R5_penalty_income_violation(self):
        s = clean_structure(); s["late_payment"]["penalty_to_income"] = True; s["late_payment"]["penalty_destination"] = "bank_income"
        self.assertEqual(find(self._check(s), "R5")["status"], "violated")

    def test_R6_bilateral_is_deferral_not_violation(self):
        s = clean_structure(); s["wad_promise"]["type"] = "bilateral"; s["wad_promise"]["binding_language"] = True
        f = find(self._check(s), "R6")
        self.assertEqual(f["status"], "deferral")
        self.assertNotEqual(f["status"], "violated")
        self.assertTrue(f["positions"])

    def test_R4_boundary_ambiguity_defers_to_D2(self):
        s = clean_structure(); s["prior_ownership"]["inah_boundary_ambiguous"] = True
        f = find(self._check(s), "R4")
        self.assertEqual(f["status"], "deferral")
        self.assertTrue(f["positions"])

    def test_indeterminate_names_missing_fact(self):
        s = clean_structure()
        s["ownership"] = {"bank_acquires_before_sale": None, "acquire_quote": "", "bank_bears_ownership_risk": None,
                          "risk_quote": "", "sale_before_possession": None, "sale_before_quote": ""}
        s["agency"]["customer_is_buying_agent"] = None
        f = find(self._check(s), "R1")
        self.assertEqual(f["status"], "indeterminate")
        self.assertTrue(f["missing_fact"])

    def test_incomplete_extraction_fails_closed(self):
        s = {"extraction_complete": False, "status": "extraction incomplete — requires human review", "unresolved": ["R2"]}
        fs = checker.check(s, RULES, DEFER)
        self.assertEqual(len(fs), 1)
        self.assertEqual(fs[0]["status"], "indeterminate")
        self.assertIsNone(fs[0]["rule_id"])

    def test_checker_never_mutates_registry(self):
        before = copy.deepcopy(RULES)
        self._check(clean_structure())
        self.assertEqual(RULES, before)


if __name__ == "__main__":
    unittest.main()
