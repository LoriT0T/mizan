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
        "provenance": {"input": "Input #2", "grounding_basis": "grounded"},
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

    def test_axis_vocabularies_are_disjoint(self):
        # The anti-conflation guarantee: 'established' can only be a rule status.
        self.assertTrue(ic.STATUS_VOCAB.isdisjoint(ic.GROUNDING_VOCAB))
        self.assertTrue(ic.STATUS_VOCAB.isdisjoint(ic.GLOSSARY_LIFECYCLE))
        self.assertTrue(ic.GROUNDING_VOCAB.isdisjoint(ic.GLOSSARY_LIFECYCLE))
        self.assertNotIn("established", ic.GROUNDING_VOCAB)

    def test_grounding_basis_off_axis_flagged(self):
        r = _rule()
        r["provenance"]["grounding_basis"] = "established"  # status word on the wrong axis
        errs = ic.check({"rules": [r]}, {"entries": []}, {"entries": []})
        self.assertTrue(any("I5" in e for e in errs))

    def test_glossary_axis_hygiene(self):
        gloss = {"entries": [{"term_id": "G-013", "status": "locked",
                              "provenance": {"sources": ["s"], "grounding_basis": "unverified"}}]}
        self.assertEqual(ic.check({"rules": []}, {"entries": []}, gloss), [])
        bad = {"entries": [{"term_id": "G-013", "status": "locked",
                            "provenance": {"sources": ["s"], "grounding_basis": "established"}}]}
        self.assertTrue(any("I5" in e for e in ic.check({"rules": []}, {"entries": []}, bad)))

    def test_l1_must_be_cbk_or_higher_committee(self):
        r = _rule(sources=[{"layer": "L1", "ref": "Kuwaiti judiciary - Chambers 2025",
                            "principle": "p", "synthetic": False}])
        errs = ic.check({"rules": [r]}, {"entries": []}, {"entries": []})
        self.assertTrue(any("I6" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
