"""Isolated test for citation_guard. Imports only the unit + stdlib."""
import unittest
import citation_guard as cg


class TestCitationGuard(unittest.TestCase):
    def test_short_reference_passes(self):
        self.assertEqual(cg.check_field("AAOIFI Sharia Standard No. 8 (Murabaha)", "ref"), [])

    def test_long_passage_rejected_by_chars(self):
        passage = "x" * 200
        errs = cg.check_field(passage, "ref")
        self.assertTrue(any("C1" in e for e in errs))

    def test_long_passage_rejected_by_words(self):
        passage = " ".join(["word"] * 40)
        errs = cg.check_field(passage, "ref")
        self.assertTrue(any("C1" in e for e in errs))

    def test_reproduced_quote_rejected(self):
        # An embedded verbatim clause over the quote cap must fail closed.
        reproduced = 'SS 8 states: "' + ("the institution shall acquire the asset and " * 5) + '"'
        errs = cg.check_field(reproduced, "principle")
        self.assertTrue(any("C2" in e for e in errs))

    def test_full_registry_shape_passes(self):
        rules = {"rules": [{"id": "R1", "sources": [
            {"ref": "AAOIFI Sharia Standard No. 8 (Murabaha); No. 18 (Possession)",
             "principle": "Acquisition-and-possession requirement before resale.", "synthetic": False}]}]}
        defer = {"entries": [{"id": "D1", "positions": [
            {"citation": "OIC Fiqh Academy Resolution 179 (19/5), Sharjah, 2009"}]}]}
        gloss = {"entries": [{"term_id": "G-001", "provenance": {"sources": ["Input #2, Part 2 (Murabaha)"]}}]}
        self.assertEqual(cg.check(rules, defer, gloss), [])


if __name__ == "__main__":
    unittest.main()
