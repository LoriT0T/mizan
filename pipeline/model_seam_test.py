"""Isolated test for model_seam. Imports only the unit + stdlib. No network."""
import os
import unittest
import model_seam as ms


class TestModelSeam(unittest.TestCase):
    def test_nokey_seam_unavailable(self):
        s = ms.NoKeySeam()
        self.assertFalse(s.available())
        self.assertIsNone(s.interpret("anything", "en"))

    def test_make_seam_is_nokey_without_env(self):
        saved = os.environ.pop("OPENROUTER_API_KEY", None)
        try:
            self.assertIsInstance(ms.make_seam(), ms.NoKeySeam)
        finally:
            if saved is not None:
                os.environ["OPENROUTER_API_KEY"] = saved

    def test_real_seam_available_with_key_but_key_not_leaked(self):
        saved = os.environ.get("OPENROUTER_API_KEY")
        os.environ["OPENROUTER_API_KEY"] = "SECRET-TEST-KEY-123"
        try:
            s = ms.Seam()
            self.assertTrue(s.available())
            self.assertNotIn("SECRET-TEST-KEY-123", repr(s))  # never in repr/logs
        finally:
            if saved is None:
                os.environ.pop("OPENROUTER_API_KEY", None)
            else:
                os.environ["OPENROUTER_API_KEY"] = saved

    def test_fake_seam_records_calls_and_returns_canned(self):
        fake = ms.FakeSeam(canned={"en": {"complete": True}})
        out = fake.interpret("prompt", "en")
        self.assertEqual(out, {"complete": True})
        self.assertEqual(fake.calls[0]["language"], "en")

    def test_per_language_model_override(self):
        s = ms.Seam(models_by_language={"ar": "x/ar-model", "en": "x/en-model"})
        self.assertEqual(s.model_for("ar"), "x/ar-model")
        self.assertEqual(s.model_for("en"), "x/en-model")


if __name__ == "__main__":
    unittest.main()
