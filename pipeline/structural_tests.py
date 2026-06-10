"""The THREE corpus-wide STRUCTURAL tests (now they bite).

Runs generation across the ENTIRE corpus via the orchestrator (no network —
NoKeySeam). Imports orchestrator (wiring) + units. These are the gates the
original design promised:
  1. opinion never auto-filled (across the whole corpus, and structurally);
  2. watermark always present (every memo + matrix, both languages);
  3. the never-rules generation gate catches verdict language a model emits.
"""
import os
import unittest

import orchestrator
import model_seam
import memo_generator
import matrix_generator

CORPUS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "corpus")
FILES = sorted(fn for fn in os.listdir(CORPUS) if fn.endswith(".txt"))


class FakeVerdictSeam:
    """A model that tries to smuggle a permissibility verdict into connective prose."""
    def available(self):
        return True

    def interpret(self, prompt, language="en"):
        return {"ar": "هذا العقد حلال وجائز.", "en": "This contract is permissible and compliant."}


class TestStructural(unittest.TestCase):
    def test_opinion_never_autofilled_across_corpus(self):
        rules, defer, glossary = orchestrator.load_registry()
        for fn in FILES:
            res = orchestrator.generate_for_contract(os.path.join(CORPUS, fn), rules, defer, glossary,
                                                     seam=model_seam.NoKeySeam())
            op = next(s for s in res["memo"]["sections"] if s["key"] == "opinion")
            self.assertEqual(op["attributed_ar"], memo_generator.OpinionField.PLACEHOLDER_AR, fn)
            self.assertEqual(op["attributed_en"], memo_generator.OpinionField.PLACEHOLDER_EN, fn)
            self.assertEqual(op["connective_ar"], "", fn)  # nothing generated into opinion
            self.assertTrue(res["memo"]["opinion_is_placeholder"], fn)

    def test_opinion_setter_is_structural_lock(self):
        op = memo_generator.OpinionField()
        with self.assertRaises(PermissionError):
            op.set("permissible")
        with self.assertRaises(PermissionError):
            op.fill("anything at all")

    def test_watermark_always_present_memo_and_matrix(self):
        rules, defer, glossary = orchestrator.load_registry()
        for fn in FILES:
            res = orchestrator.generate_for_contract(os.path.join(CORPUS, fn), rules, defer, glossary,
                                                     seam=model_seam.NoKeySeam())
            for doc in (res["memo"]["render_md"], res["matrix"]["render_md"]):
                self.assertIn(memo_generator.WATERMARK_AR, doc, fn)
                self.assertIn(memo_generator.WATERMARK_EN, doc, fn)
            # matrix uses the same canonical text
            self.assertEqual(matrix_generator.WATERMARK_AR, memo_generator.WATERMARK_AR)

    def test_generation_gate_catches_model_verdict(self):
        rules, defer, glossary = orchestrator.load_registry()
        # A model that emits verdict language must fail the generation CLOSED.
        with self.assertRaises(RuntimeError):
            orchestrator.generate_for_contract(os.path.join(CORPUS, "contract_clean_en.txt"),
                                               rules, defer, glossary, seam=FakeVerdictSeam())

    def test_no_finding_uses_verdict_status_across_corpus(self):
        rules, defer, glossary = orchestrator.load_registry()
        allowed = {"satisfied", "violated", "indeterminate", "deferral"}
        for fn in FILES:
            res = orchestrator.generate_for_contract(os.path.join(CORPUS, fn), rules, defer, glossary,
                                                     seam=model_seam.NoKeySeam())
            for f in res["findings"]:
                self.assertIn(f["status"], allowed, fn)


if __name__ == "__main__":
    unittest.main()
