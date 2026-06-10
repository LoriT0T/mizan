"""Isolated test for the Ijara extension of the extractor. FakeRail/FakeSeam — no network."""
import unittest
import extractor as ex


class FakeRail:
    def scan_injection(self, text):
        return []

    def wrap_as_data(self, text):
        return text


class FakeSeam:
    def available(self):
        return False

    def interpret(self, p, l="en"):
        return None


CLEAN_IJARA = """### SYNTHETIC ###
العين المؤجَّرة: عقارٌ سكنيٌّ معيَّن (أصلٌ غيرُ مستهلَك) مباحُ الاستعمال.
البند 1: يملك المؤجِّرُ العينَ ويقبضها قبل الإجارة.
البند 2: الأجرةُ محدَّدةٌ قدرها 500 دينار، ومدّةُ الإجارة محدَّدةٌ بعشر سنوات؛ ولا يجوز للمؤجِّر زيادةُ الأجرة انفراداً.
البند 3: يتحمّل المؤجِّرُ الصيانةَ الأساسية والتأمينَ التكافليَّ وتبعةَ الهلاك الكلّي.
البند 4: لا تستحقّ الأجرةُ إلا بعد تسليم العين.
البند 5: ينتقل الملكُ بوعدٍ مستقلٍّ منفصلٍ عن عقد الإجارة."""


class TestExtractorIjara(unittest.TestCase):
    def test_clean_ijara_facts(self):
        s = ex.extract(CLEAN_IJARA, FakeRail(), FakeSeam())
        ij = s["ijara"]
        self.assertTrue(s["extraction_complete"])
        self.assertTrue(ij["lessor_owns_before_lease"])
        self.assertTrue(ij["rent_defined"])
        self.assertTrue(ij["term_defined"])
        self.assertIs(ij["unilateral_increase"], False)
        self.assertTrue(ij["lessor_bears_ownership_risk"])
        self.assertIs(ij["rent_before_delivery"], False)
        self.assertTrue(ij["is_imb"])
        self.assertIs(ij["transfer_fused"], False)

    def test_risk_shift_detected(self):
        t = CLEAN_IJARA.replace("يتحمّل المؤجِّرُ الصيانةَ الأساسية والتأمينَ التكافليَّ وتبعةَ الهلاك الكلّي.",
                                "يتحمّل المستأجرُ الصيانةَ الأساسية والتأمينَ التكافليَّ وتبعةَ الهلاك الكلّي.")
        s = ex.extract(t, FakeRail(), FakeSeam())
        self.assertTrue(s["ijara"]["risk_shifted_to_lessee"])

    def test_fusion_detected_even_with_no_separate_phrase(self):
        t = CLEAN_IJARA.replace("ينتقل الملكُ بوعدٍ مستقلٍّ منفصلٍ عن عقد الإجارة.",
                                "Sale and lease are bound into one contract with automatic ownership transfer; no separate transfer instrument.")
        s = ex.extract(t, FakeRail(), FakeSeam())
        self.assertIs(s["ijara"]["transfer_fused"], True)

    def test_arabic_quote_verbatim(self):
        s = ex.extract(CLEAN_IJARA, FakeRail(), FakeSeam())
        self.assertIn("المؤجِّر", s["ijara"]["lessor_risk_quote"])


if __name__ == "__main__":
    unittest.main()
