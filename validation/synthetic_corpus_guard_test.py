"""Isolated test for synthetic_corpus_guard. Imports only the unit + stdlib."""
import unittest
import synthetic_corpus_guard as scg


class TestSyntheticGuard(unittest.TestCase):
    def test_proper_labels_pass(self):
        rules = {"rules": [{"id": "R1", "sources": [
            {"layer": "L3", "ref": "AAOIFI SS 8", "principle": "p", "synthetic": False},
            {"layer": "L2", "ref": "SYNTHETIC SSB fatwa SSB-SYNTH-MUR-001", "principle": "p", "synthetic": True},
        ]}]}
        self.assertEqual(scg.check(rules), [])

    def test_l2_not_marked_synthetic_flagged(self):
        rules = {"rules": [{"id": "R1", "sources": [
            {"layer": "L2", "ref": "SYNTHETIC fatwa", "principle": "p", "synthetic": False}]}]}
        self.assertTrue(any("S1" in e for e in scg.check(rules)))

    def test_l2_missing_label_flagged(self):
        rules = {"rules": [{"id": "R1", "sources": [
            {"layer": "L2", "ref": "bank fatwa 7", "principle": "p", "synthetic": True}]}]}
        self.assertTrue(any("S2" in e for e in scg.check(rules)))

    def test_real_layer_marked_synthetic_flagged(self):
        rules = {"rules": [{"id": "R1", "sources": [
            {"layer": "L3", "ref": "AAOIFI SS 8", "principle": "p", "synthetic": True}]}]}
        self.assertTrue(any("S3" in e for e in scg.check(rules)))

    def test_judicial_layer_marked_synthetic_flagged(self):
        rules = {"rules": [{"id": "R1", "sources": [
            {"layer": "LJ", "ref": "Kuwaiti judicial practice (Chambers)", "principle": "p", "synthetic": True}]}]}
        self.assertTrue(any("S3" in e for e in scg.check(rules)))

    def test_judicial_layer_real_passes(self):
        rules = {"rules": [{"id": "R1", "sources": [
            {"layer": "LJ", "ref": "Kuwaiti judicial practice (Chambers)", "principle": "p", "synthetic": False}]}]}
        self.assertEqual(scg.check(rules), [])


if __name__ == "__main__":
    unittest.main()
