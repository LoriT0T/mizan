"""Isolated test for scope. Imports only the unit + stdlib (+ reads the scope
registry, the read-only source of truth)."""
import os
import unittest
import scope

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCOPE = scope.load_scope(os.path.join(ROOT, "registry", "scope_registry.json"))
DEFER_LOOKUP = {"D3": {"id": "D3", "positions": [{"authority": "OIC", "position_ar": "x", "position_en": "y", "citation": "Res 179"}],
                       "routing_ar": "يُحال", "routing_en": "Refer to SSB"}}


class TestScope(unittest.TestCase):
    def test_covered_type_is_checked(self):
        covered, oos = scope.assess({"types": ["murabaha"], "unrecognized_components": []}, SCOPE)
        self.assertEqual(covered, ["murabaha"])
        self.assertEqual(oos, [])

    def test_ijara_is_covered(self):
        covered, oos = scope.assess({"types": ["ijara"], "unrecognized_components": []}, SCOPE)
        self.assertEqual(covered, ["ijara"])

    def test_tawarruq_recognized_not_covered_routes_to_D3(self):
        covered, oos = scope.assess({"types": ["tawarruq"], "unrecognized_components": []}, SCOPE, DEFER_LOOKUP)
        self.assertEqual(covered, [])
        self.assertEqual(len(oos), 1)
        self.assertEqual(oos[0]["status"], "out_of_scope")
        self.assertTrue(oos[0]["positions"])  # D3 positions surfaced
        self.assertIn("tawarruq", oos[0]["note_en"])

    def test_unrecognized_component_flagged_no_rule(self):
        covered, oos = scope.assess({"types": ["murabaha"], "unrecognized_components": ["mudaraba"]}, SCOPE)
        self.assertEqual(covered, ["murabaha"])          # covered part still checked
        self.assertEqual(len(oos), 1)
        self.assertEqual(oos[0]["status"], "out_of_scope")
        self.assertIn("mudaraba", oos[0]["component"])

    def test_unrecognized_type(self):
        covered, oos = scope.assess({"types": ["unrecognized"], "unrecognized_components": []}, SCOPE)
        self.assertEqual(covered, [])
        self.assertEqual(oos[0]["status"], "out_of_scope")


if __name__ == "__main__":
    unittest.main()
