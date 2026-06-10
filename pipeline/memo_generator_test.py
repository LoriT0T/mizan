"""Isolated test for memo_generator. Imports only the unit + stdlib. FakeSeam — no network."""
import unittest
import memo_generator as mg


class FakeSeam:
    def __init__(self, canned=None, available=True):
        self._canned, self._a = canned, available

    def available(self):
        return self._a

    def interpret(self, prompt, language="en"):
        return self._canned


def structure():
    return {
        "asset": {"present": True, "quote": "Asset: a permissible vehicle", "permissible": True,
                  "permissible_quote": "permissible asset", "exists": True, "exists_quote": ""},
        "ownership": {"bank_acquires_before_sale": True, "acquire_quote": "Bank takes ownership and possession",
                      "bank_bears_ownership_risk": True, "risk_quote": "", "sale_before_possession": None, "sale_before_quote": ""},
        "agency": {"customer_is_buying_agent": None, "quote": ""},
        "price_terms": {"cost_disclosed": True, "cost_quote": "disclosed cost", "markup_disclosed": True,
                        "markup_quote": "", "price_fixed_at_contract": True, "fixed_quote": ""},
        "late_payment": {"penalty_destination": "charity", "charity_quote": "", "penalty_to_income": None,
                         "income_quote": "", "markup_increase_on_late": False, "increase_quote": ""},
        "wad_promise": {"present": True, "type": "unilateral", "binding_language": False, "quote": "unilateral promise"},
        "prior_ownership": {"asset_already_customers": False, "owned_quote": "", "inah_buyback": False, "inah_quote": "", "inah_boundary_ambiguous": False},
    }


def findings_clean():
    sat = lambda rid, ar, en: {"rule_id": rid, "rule_title_ar": ar, "rule_title_en": en, "status": "satisfied",
                               "quote": "clause", "citations": [{"layer": "L3", "ref": "AAOIFI SS 8"}]}
    defer = {"rule_id": "R6", "rule_title_ar": "الوعد", "rule_title_en": "wa'd", "status": "deferral",
             "quote": "promise clause", "citations": [{"layer": "L3", "ref": "AAOIFI SS 8"}],
             "positions": [{"authority": "AAOIFI", "position_ar": "موقف", "position_en": "no bilateral binding", "citation": "SS 8"},
                           {"authority": "OIC", "position_ar": "موقف", "position_en": "morally binding", "citation": "OIC"}],
             "routing_ar": "تُحال إلى الهيئة", "routing_en": "Refer to the SSB"}
    return [sat("R1", "أ", "a"), defer]


class TestMemoGenerator(unittest.TestCase):
    def test_opinion_setter_refuses(self):
        op = mg.OpinionField()
        with self.assertRaises(PermissionError):
            op.set("the contract is fine")
        with self.assertRaises(PermissionError):
            op.fill("anything")

    def test_opinion_section_is_placeholder(self):
        memo = mg.generate(structure(), findings_clean(), {}, {}, {}, seam=None, contract_file="t.txt")
        op = next(s for s in memo["sections"] if s["key"] == "opinion")
        self.assertEqual(op["attributed_ar"], mg.OpinionField.PLACEHOLDER_AR)
        self.assertEqual(op["connective_ar"], "")  # nothing generated into the opinion
        self.assertIn("فارغاً عمداً", memo["render_md"])

    def test_watermark_on_every_section_and_bilingual(self):
        memo = mg.generate(structure(), findings_clean(), {}, {}, {}, seam=None, contract_file="t.txt")
        self.assertIn(mg.WATERMARK_AR, memo["render_md"])
        self.assertIn(mg.WATERMARK_EN, memo["render_md"])
        # watermark appears at least once per section (9) + header + footer
        self.assertGreaterEqual(memo["render_md"].count(mg.WATERMARK_EN), len(memo["sections"]))

    def test_arabic_first_default(self):
        memo = mg.generate(structure(), findings_clean(), {}, {}, {}, seam=None)
        self.assertEqual(memo["authoritative_language"], "ar")

    def test_deferral_section_surfaces_positions_and_routing(self):
        memo = mg.generate(structure(), findings_clean(), {}, {}, {}, seam=None)
        d = next(s for s in memo["sections"] if s["key"] == "deferrals")
        self.assertIn("AAOIFI", d["attributed_en"])
        self.assertIn("Refer to the SSB", d["attributed_en"])

    def test_model_verdict_lands_in_generated_prose(self):
        # A FakeSeam that emits verdict language -> it lands in the gated bucket (caught downstream).
        memo = mg.generate(structure(), findings_clean(), {}, {}, {},
                           seam=FakeSeam(canned={"ar": "هذا العقد حلال", "en": "this contract is permissible"}))
        joined = " ".join(memo["generated_prose"])
        self.assertIn("permissible", joined)   # it is in the GATED bucket, not silently rendered as truth

    def test_verbatim_quote_not_in_generated_prose(self):
        # Attributed verbatim quotes must NOT be in the gated bucket (they are exempt).
        memo = mg.generate(structure(), findings_clean(), {}, {}, {}, seam=None)
        self.assertFalse(any("Asset: a permissible vehicle" in p for p in memo["generated_prose"]))


if __name__ == "__main__":
    unittest.main()
