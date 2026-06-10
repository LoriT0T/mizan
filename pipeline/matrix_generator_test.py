"""Isolated test for matrix_generator. Imports only the unit + stdlib."""
import unittest
import matrix_generator as mx


def violated(rid):
    return {"rule_id": rid, "rule_title_ar": "ع", "rule_title_en": "t", "status": "violated",
            "quote": "البند ...", "citations": [{"layer": "L3", "ref": "AAOIFI SS 8"}]}


def deferral():
    return {"rule_id": "R6", "rule_title_ar": "الوعد", "rule_title_en": "wa'd", "status": "deferral",
            "quote": "promise", "citations": [{"layer": "L3", "ref": "AAOIFI SS 8"}]}


def satisfied(rid):
    return {"rule_id": rid, "rule_title_ar": "ع", "rule_title_en": "t", "status": "satisfied",
            "quote": "ok", "citations": []}


class TestMatrixGenerator(unittest.TestCase):
    def test_satisfied_excluded(self):
        m = mx.generate([satisfied("R1"), satisfied("R2")])
        self.assertEqual(m["rows"], [])

    def test_violation_row_has_severity_remediation_and_layers(self):
        m = mx.generate([violated("R1")])
        row = m["rows"][0]
        self.assertEqual(row["severity"], "major")
        self.assertTrue(row["remediation_ar"] and row["remediation_en"])
        self.assertIn("[L3] AAOIFI SS 8", row["citations"])
        self.assertEqual(row["status_field"], "open")
        self.assertEqual(row["owner"], "")

    def test_deferral_row_not_graded(self):
        m = mx.generate([deferral()])
        row = m["rows"][0]
        self.assertIsNone(row["severity"])
        self.assertIn("not graded", mx.render(m))
        self.assertIn("SSB", row["remediation_en"])

    def test_severity_is_configurable(self):
        m = mx.generate([violated("R1")], severity_config={"R1": "minor"})
        self.assertEqual(m["rows"][0]["severity"], "minor")

    def test_severity_note_labels_convention_not_binding(self):
        m = mx.generate([violated("R1")])
        self.assertIn("CONFIGURABLE convention", m["severity_note"]["en"])
        self.assertIn("NOT a binding AAOIFI scale", m["severity_note"]["en"])

    def test_render_bilingual(self):
        out = mx.render(mx.generate([violated("R3")]))
        self.assertIn("Non-Compliance Matrix", out)
        self.assertIn("مصفوفة عدم المطابقة", out)


if __name__ == "__main__":
    unittest.main()
