"""Stage 2 corpus-wide structural + integration tests (wiring via orchestrator;
NoKeySeam — no network). Proves: the out-of-scope GUARANTEE, covered+uncovered
honesty on a mixed contract, no rule applied to a recognized-not-covered type,
the Ijara defects, and the structural locks (opinion/watermark) across the
Ijara corpus."""
import os
import unittest

import orchestrator
import model_seam
import memo_generator

CORPUS2 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "corpus", "stage2")
FILES = sorted(fn for fn in os.listdir(CORPUS2) if fn.endswith(".txt"))


def run(fn):
    return orchestrator.run_contract(os.path.join(CORPUS2, fn), seam=model_seam.NoKeySeam())


class TestStage2(unittest.TestCase):
    def test_unrecognized_component_yields_out_of_scope_finding(self):
        # THE load-bearing guarantee: a contract with an unrecognized component must
        # produce an explicit out-of-scope finding.
        res = run("contract_mixed_oos_en.txt")
        oos = [f for f in res["findings"] if f["status"] == "out_of_scope"]
        self.assertTrue(oos)
        self.assertEqual(oos[0]["component"], "mudaraba")

    def test_mixed_covered_checked_and_uncovered_flagged_nothing_fabricated(self):
        res = run("contract_mixed_oos_en.txt")
        ids = {f["rule_id"] for f in res["findings"]}
        self.assertTrue({"R1", "R2", "R3", "R4", "R5", "R6"}.issubset(ids))  # Murabaha part checked
        self.assertTrue(any(f["status"] == "out_of_scope" for f in res["findings"]))  # Mudaraba flagged
        # No Murabaha rule was applied to the Mudaraba part: every R-finding cites the Murabaha contract clauses, none invented.
        self.assertNotIn("ijara", res["covered_types"])

    def test_tawarruq_recognized_not_covered_no_rule_applied(self):
        res = run("contract_tawarruq_en.txt")
        self.assertEqual(res["covered_types"], [])
        statuses = [f["status"] for f in res["findings"]]
        self.assertIn("out_of_scope", statuses)
        # NO rule was applied — no satisfied/violated/deferral rule findings.
        self.assertFalse(any(s in ("satisfied", "violated", "deferral") for s in statuses))
        oos = res["findings"][0]
        self.assertTrue(oos["positions"])  # D3 positions surfaced

    def test_ijara_defects_each_caught(self):
        cases = {"contract_ijara_i4_riskshift_ar.txt": "I4",
                 "contract_ijara_i6_fusion_en.txt": "I6",
                 "contract_ijara_i5_rentbefore_en.txt": "I5"}
        for fn, rid in cases.items():
            res = run(fn)
            viol = [f for f in res["findings"] if f["rule_id"] == rid and f["status"] == "violated"]
            self.assertTrue(viol, f"{fn}: expected {rid} violated")

    def test_clean_ijara_no_violation(self):
        res = run("contract_ijara_clean_ar.txt")
        self.assertFalse(any(f["status"] == "violated" for f in res["findings"]))
        self.assertTrue(any(f["status"] == "deferral" for f in res["findings"]))  # IMB wa'd -> D1

    def test_structural_locks_across_ijara_corpus(self):
        rules, defer, glossary = orchestrator.load_registry()
        for fn in FILES:
            res = orchestrator.generate_for_contract(os.path.join(CORPUS2, fn), rules, defer, glossary,
                                                     seam=model_seam.NoKeySeam())
            op = next(s for s in res["memo"]["sections"] if s["key"] == "opinion")
            self.assertEqual(op["attributed_ar"], memo_generator.OpinionField.PLACEHOLDER_AR, fn)
            for doc in (res["memo"]["render_md"], res["matrix"]["render_md"]):
                self.assertIn(memo_generator.WATERMARK_AR, doc, fn)
                self.assertIn(memo_generator.WATERMARK_EN, doc, fn)

    def test_no_verdict_status_across_stage2_corpus(self):
        import never_rules_guard
        for fn in FILES:
            for f in run(fn)["findings"]:
                self.assertIn(f["status"], never_rules_guard.ALLOWED_STATUS, fn)


if __name__ == "__main__":
    unittest.main()
