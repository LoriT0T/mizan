"""Isolated test for glossary_growth. Imports only the unit + stdlib.

The fail-closed collision gate is INJECTED (a fake stands in for the Stage-1a
glossary_checks.check_candidate), keeping this test isolated.
"""
import unittest
import glossary_growth as gg


def accept_gate(candidate, existing):
    return []   # no collisions


def reject_gate(candidate, existing):
    return [f"COLLISION {candidate['term_id']}: Arabic conflicts with locked entry"]


class TestGlossaryGrowth(unittest.TestCase):
    def test_candidate_is_provisional_and_unverified(self):
        c = gg.build_candidate("بيع الاستجرار", "istijrar (supply sale)", "تعريف", "definition",
                               ["public source A"], "G-PROV")
        self.assertEqual(c["status"], "provisional")
        self.assertEqual(c["origin"], "growth-protocol")
        self.assertEqual(c["provenance"]["grounding_basis"], "unverified")
        self.assertTrue(c["review_routing"])

    def test_propose_accepts_when_gate_clear(self):
        r = gg.propose("بيع الاستجرار", "istijrar", "تعريف", "def", ["src"], existing=[], gate=accept_gate)
        self.assertTrue(r["accepted"])
        self.assertEqual(r["reasons"], [])

    def test_propose_fails_closed_on_collision(self):
        r = gg.propose("المرابحة", "markup sale", "تعريف", "def", ["src"], existing=[], gate=reject_gate)
        self.assertFalse(r["accepted"])
        self.assertTrue(r["reasons"])


if __name__ == "__main__":
    unittest.main()
