"""Isolated test for glossary_checks. Imports only the unit + stdlib.

Includes the FAIL-CLOSED collision demonstration (negative path) the checkpoint
requires.
"""
import unittest
import glossary_checks as gc


def _entry(tid, ar, en, status="locked-pending-calibration", routing=None):
    e = {"term_id": tid, "canonical_ar": ar, "canonical_en": en, "status": status}
    if routing:
        e["review_routing"] = routing
    return e


class TestGlossaryChecks(unittest.TestCase):
    def test_clean_glossary_passes(self):
        gloss = {"entries": [_entry("G-001", "المرابحة", "Murabaha")]}
        hist = {"versions": [{"added": ["G-001"]}]}
        self.assertEqual(gc.check(gloss, hist), [])

    def test_two_english_renderings_for_one_arabic(self):
        gloss = {"entries": [_entry("G-001", "المرابحة", "Murabaha"),
                             _entry("G-002", "المرابحة", "Cost-plus sale")]}
        hist = {"versions": [{"added": ["G-001", "G-002"]}]}
        errs = gc.check(gloss, hist)
        self.assertTrue(any("G1" in e for e in errs))

    def test_provisional_requires_routing(self):
        gloss = {"entries": [_entry("G-013", "بيع التولية", "tawliyah", status="provisional")]}
        hist = {"versions": [{"added": ["G-013"]}]}
        errs = gc.check(gloss, hist)
        self.assertTrue(any("G2" in e for e in errs))

    def test_history_coverage(self):
        gloss = {"entries": [_entry("G-099", "x", "y")]}
        hist = {"versions": [{"added": []}]}
        errs = gc.check(gloss, hist)
        self.assertTrue(any("G4" in e for e in errs))

    # ---- FAIL-CLOSED collision gate (the demonstration) ----
    def test_candidate_safe_when_no_conflict(self):
        existing = [_entry("G-001", "المرابحة", "Murabaha")]
        candidate = _entry("G-013", "بيع التولية", "tawliyah (sale at cost)",
                           status="provisional", routing="review list")
        self.assertEqual(gc.check_candidate(candidate, existing), [])

    def test_candidate_colliding_arabic_fails_closed(self):
        existing = [_entry("G-001", "المرابحة", "Murabaha")]  # locked-pending
        candidate = _entry("G-050", "المرابحة", "markup sale",
                           status="provisional", routing="review list")
        reasons = gc.check_candidate(candidate, existing)
        self.assertTrue(reasons, "collision must fail closed")
        self.assertTrue(any("locked" in r and "المرابحة" in r for r in reasons))

    def test_candidate_duplicate_id_fails_closed(self):
        existing = [_entry("G-001", "المرابحة", "Murabaha")]
        candidate = _entry("G-001", "بيع جديد", "new sale",
                           status="provisional", routing="review list")
        self.assertTrue(any("term_id already exists" in r for r in gc.check_candidate(candidate, existing)))


if __name__ == "__main__":
    unittest.main()
