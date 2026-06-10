"""Isolated test for contract_type_classifier. Imports only the unit + stdlib."""
import unittest
import contract_type_classifier as c


class TestClassifier(unittest.TestCase):
    def test_murabaha(self):
        r = c.classify("Murabaha to the Purchase Orderer; disclosed cost plus a markup.")
        self.assertIn("murabaha", r["types"])
        self.assertNotIn("ijara", r["types"])

    def test_ijara_arabic(self):
        r = c.classify("عقد الإجارة المنتهية بالتمليك؛ الأجرة والمدّة محددتان، والمؤجِّر يملك العين.")
        self.assertIn("ijara", r["types"])

    def test_tawarruq_takes_precedence_over_murabaha_leg(self):
        r = c.classify("Tawarruq monetization: the bank sells a commodity at cost plus markup for cash.")
        self.assertIn("tawarruq", r["types"])
        self.assertNotIn("murabaha", r["types"])  # the cost-plus leg belongs to the tawarruq

    def test_unrecognized_when_no_cue(self):
        r = c.classify("This is a generic agreement about nothing in particular.")
        self.assertEqual(r["types"], ["unrecognized"])

    def test_unrecognized_component_flagged(self):
        r = c.classify("Murabaha to the Purchase Orderer ... plus a Mudaraba investment partnership.")
        self.assertIn("murabaha", r["types"])
        self.assertIn("mudaraba", r["unrecognized_components"])

    def test_fails_to_unrecognized_not_a_guess(self):
        # No cues, no model -> unrecognized (never a guessed type).
        r = c.classify("xyzzy plugh", seam=None)
        self.assertEqual(r["types"], ["unrecognized"])
        self.assertEqual(r["method"], "deterministic")


if __name__ == "__main__":
    unittest.main()
