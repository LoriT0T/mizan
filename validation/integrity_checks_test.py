"""Isolated test for integrity_checks. Imports only the unit + stdlib."""
import unittest
import integrity_checks as ic


def _rule(**over):
    base = {
        "id": "R1", "status": "established",
        "title_ar": "ع", "title_en": "t", "rule_ar": "ع", "rule_en": "t",
        "satisfied_by": [{"ar": "ع", "en": "e"}],
        "violated_by": [{"ar": "ع", "en": "e"}],
        "sources": [{"layer": "L3", "ref": "AAOIFI SS 8", "principle": "p", "synthetic": False}],
    }
    base.update(over)
    return base


class TestIntegrity(unittest.TestCase):
    def test_clean_registry_passes(self):
        rules = {"rules": [_rule()]}
        defer = {"entries": []}
        gloss = {"entries": []}
        self.assertEqual(ic.check(rules, defer, gloss), [])

    def test_missing_layer_flagged(self):
        r = _rule(sources=[{"ref": "x", "principle": "p", "synthetic": False}])
        errs = ic.check({"rules": [r]}, {"entries": []}, {"entries": []})
        self.assertTrue(any("I1" in e for e in errs))

    def test_not_bilingual_flagged(self):
        r = _rule(satisfied_by=[{"ar": "ع", "en": ""}])
        errs = ic.check({"rules": [r]}, {"entries": []}, {"entries": []})
        self.assertTrue(any("I2" in e and "satisfied_by" in e for e in errs))

    def test_contested_without_defer_flagged(self):
        r = _rule(status="contested")  # no defer_ref
        errs = ic.check({"rules": [r]}, {"entries": []}, {"entries": []})
        self.assertTrue(any("I3" in e for e in errs))

    def test_contested_with_dangling_defer_ref(self):
        r = _rule(status="contested", defer_ref="D9")
        errs = ic.check({"rules": [r]}, {"entries": [{"id": "D1", "positions": [], "routing_ar": "", "routing_en": ""}]}, {"entries": []})
        self.assertTrue(any("I3" in e and "D9" in e for e in errs))

    def test_defer_needs_two_positions(self):
        defer = {"entries": [{"id": "D1", "positions": [{"citation": "c"}], "routing_ar": "x", "routing_en": "y"}]}
        errs = ic.check({"rules": []}, defer, {"entries": []})
        self.assertTrue(any("I4" in e and "D1" in e for e in errs))

    def test_provisional_not_promoted(self):
        gloss = {"entries": [{"term_id": "G-013", "status": "locked",
                              "grounding": {"established_or_provisional": "provisional"}}]}
        errs = ic.check({"rules": []}, {"entries": []}, gloss)
        self.assertTrue(any("I5" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
