"""Isolated test for never_rules_guard. Imports only the unit + stdlib.

Includes the demonstration that the guard REJECTS verdict language.
"""
import unittest
import never_rules_guard as g


class TestNeverRulesGuard(unittest.TestCase):
    def test_allowed_statuses_pass(self):
        findings = [{"rule_id": "R1", "status": "satisfied", "note": "Bank takes possession before resale."},
                    {"rule_id": "R6", "status": "deferral", "note": "Routed to the SSB."}]
        self.assertEqual(g.check(findings), [])

    def test_verdict_status_rejected(self):
        errs = g.check([{"rule_id": "R3", "status": "permissible", "note": ""}])
        self.assertTrue(any("N1" in e for e in errs))

    def test_verdict_word_in_note_rejected_english(self):
        errs = g.check([{"rule_id": "R3", "status": "violated", "note": "This contract is impermissible."}])
        self.assertTrue(any("N2" in e for e in errs))

    def test_verdict_word_in_note_rejected_arabic(self):
        errs = g.check([{"rule_id": "R3", "status": "violated", "note": "هذا العقد حرام."}])
        self.assertTrue(any("N2" in e for e in errs))

    def test_check_prose_clean_passes(self):
        self.assertEqual(g.check_prose(["The aqd is a Murabaha to the Purchase Orderer.",
                                        "العقدُ مرابحةٌ للآمر بالشراء."]), [])

    def test_check_prose_catches_english_verdict(self):
        errs = g.check_prose(["This contract is impermissible and must be rejected."])
        self.assertTrue(any("N3" in e for e in errs))

    def test_check_prose_catches_arabic_verdict(self):
        errs = g.check_prose(["هذا العقد حلال."])
        self.assertTrue(any("N3" in e for e in errs))

    def test_quoted_position_is_exempt(self):
        # 'impermissible' inside an attributed quote/position is reported, not ruled.
        finding = {"rule_id": "R6", "status": "deferral", "note": "Routed to the SSB.",
                   "quote": "both parties are bound",
                   "positions": [{"authority": "OIC", "position_en": "a bilateral binding promise is impermissible",
                                  "position_ar": "ملزم ممنوع", "citation": "OIC res."}]}
        self.assertEqual(g.check([finding]), [])


if __name__ == "__main__":
    unittest.main()
