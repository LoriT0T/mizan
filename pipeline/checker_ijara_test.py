"""Isolated test for the Ijara checker evaluators. Imports only checker + stdlib
(+ reads the read-only Ijara registry + merged defer)."""
import json
import os
import unittest
import checker

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IJARA = json.load(open(os.path.join(ROOT, "registry", "rules_ijara.json"), encoding="utf-8"))
DEFER = json.load(open(os.path.join(ROOT, "registry", "defer_register.json"), encoding="utf-8"))
IDEFER = json.load(open(os.path.join(ROOT, "registry", "defer_register_ijara.json"), encoding="utf-8"))
MERGED = {"entries": DEFER["entries"] + IDEFER["entries"]}


def clean_ijara():
    return {
        "extraction_complete": True,
        "asset": {"present": True, "quote": "العين المؤجرة: عقار"},
        "ijara": {
            "asset_consumable": None, "permissible_use_violation": None, "use_quote": "",
            "rent_defined": True, "rent_quote": "الاجره 500", "term_defined": True, "term_quote": "10 سنوات",
            "unilateral_increase": False, "increase_quote": "",
            "lessor_owns_before_lease": True, "owns_quote": "يملك قبل", "lease_before_acquisition": None, "lba_quote": "",
            "risk_shifted_to_lessee": None, "risk_shift_quote": "", "lessor_bears_ownership_risk": True, "lessor_risk_quote": "المؤجر يتحمل",
            "rent_before_delivery": False, "rent_timing_quote": "بعد التسليم",
            "is_imb": True, "transfer_fused": False, "transfer_quote": "وعد مستقل",
            "sale_leaseback": None, "sale_leaseback_interval": None, "sl_quote": "",
        },
    }


def find(findings, rid):
    return [f for f in findings if f["rule_id"] == rid]


class TestIjaraChecker(unittest.TestCase):
    def _c(self, s):
        return checker.check(s, IJARA, MERGED)

    def test_clean_ijara_satisfies_core_and_defers_imb_wad(self):
        fs = self._c(clean_ijara())
        for rid in ("I1", "I2", "I3", "I4", "I5", "I6"):
            self.assertEqual(find(fs, rid)[0]["status"], "satisfied", rid)
        # IMB -> a D1 wa'd deferral is appended (contested, never adjudicated)
        deferrals = [f for f in fs if f["status"] == "deferral"]
        self.assertTrue(deferrals)
        self.assertTrue(deferrals[0]["positions"])

    def test_I4_riskshift_violation_headline(self):
        s = clean_ijara(); s["ijara"]["risk_shifted_to_lessee"] = True; s["ijara"]["lessor_bears_ownership_risk"] = False
        f = find(self._c(s), "I4")[0]
        self.assertEqual(f["status"], "violated")
        self.assertTrue(f["violation_pattern"])
        layers = {c["layer"] for c in f["citations"]}
        self.assertTrue({"L1", "L3", "L2"}.issubset(layers))

    def test_I6_fusion_violation(self):
        s = clean_ijara(); s["ijara"]["transfer_fused"] = True
        self.assertEqual(find(self._c(s), "I6")[0]["status"], "violated")

    def test_I5_rent_before_delivery_violation(self):
        s = clean_ijara(); s["ijara"]["rent_before_delivery"] = True
        self.assertEqual(find(self._c(s), "I5")[0]["status"], "violated")

    def test_I2_unilateral_increase_violation(self):
        s = clean_ijara(); s["ijara"]["unilateral_increase"] = True
        self.assertEqual(find(self._c(s), "I2")[0]["status"], "violated")

    def test_I7_simultaneous_leaseback_violation(self):
        s = clean_ijara(); s["ijara"]["sale_leaseback"] = True; s["ijara"]["sale_leaseback_interval"] = False
        self.assertEqual(find(self._c(s), "I7")[0]["status"], "violated")

    def test_no_imb_no_wad_deferral(self):
        s = clean_ijara(); s["ijara"]["is_imb"] = False
        self.assertEqual([f for f in self._c(s) if f["status"] == "deferral"], [])

    def test_checker_never_rules_on_ijara(self):
        for f in self._c(clean_ijara()):
            self.assertIn(f["status"], {"satisfied", "violated", "indeterminate", "deferral"})


if __name__ == "__main__":
    unittest.main()
