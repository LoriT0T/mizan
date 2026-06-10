"""Wiring test for the orchestrator. Imports orchestrator (which wires the
units) + model_seam. Uses a no-network seam; touches no model.
"""
import os
import unittest
import orchestrator
import model_seam

CORPUS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "corpus")


class TestOrchestrator(unittest.TestCase):
    def test_run_clean_contract_end_to_end_no_network(self):
        res = orchestrator.run_contract(os.path.join(CORPUS, "contract_clean_en.txt"),
                                        seam=model_seam.NoKeySeam())
        self.assertTrue(res["structure"]["extraction_complete"])
        self.assertEqual(len(res["findings"]), 6)
        statuses = {f["rule_id"]: f["status"] for f in res["findings"]}
        self.assertEqual(statuses["R6"], "deferral")
        self.assertTrue(all(statuses[r] == "satisfied" for r in ("R1", "R2", "R3", "R4", "R5")))

    def test_injection_contract_yields_no_verdict(self):
        res = orchestrator.run_contract(os.path.join(CORPUS, "contract_injection_en.txt"),
                                        seam=model_seam.NoKeySeam())
        # Injection inert end-to-end: normal findings, guard passed, no verdict status.
        self.assertTrue(res["structure"]["injection_spans"])
        for f in res["findings"]:
            self.assertIn(f["status"], {"satisfied", "violated", "indeterminate", "deferral"})

    def test_guard_fail_closed_on_smuggled_verdict(self):
        # If the checker ever emitted a verdict, the orchestrator must fail closed.
        original = orchestrator.checker.check
        orchestrator.checker.check = lambda s, r, d: [{"rule_id": "R3", "status": "permissible", "note": ""}]
        try:
            with self.assertRaises(RuntimeError):
                orchestrator.run_contract(os.path.join(CORPUS, "contract_clean_en.txt"),
                                          seam=model_seam.NoKeySeam())
        finally:
            orchestrator.checker.check = original

    def test_unlabelled_document_refused(self):
        # corpus_loader fail-closed is wired in.
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as fh:
            fh.write("Murabaha contract with no synthetic marker")
            path = fh.name
        try:
            with self.assertRaises(ValueError):
                orchestrator.run_contract(path, seam=model_seam.NoKeySeam())
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
