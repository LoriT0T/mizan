"""Isolated test for corpus_loader. Imports only the unit + stdlib."""
import unittest
import corpus_loader as cl


class TestCorpusLoader(unittest.TestCase):
    def test_labelled_text_passes(self):
        cl.assert_synthetic("### SYNTHETIC CONTRACT ###\nbody")  # no raise

    def test_unlabelled_text_refused(self):
        with self.assertRaises(ValueError):
            cl.assert_synthetic("Murabaha Contract\nbody with no marker")

    def test_marker_must_be_near_top(self):
        buried = "line1\nline2\nline3\nline4 SYNTHETIC appears too late"
        with self.assertRaises(ValueError):
            cl.assert_synthetic(buried)


if __name__ == "__main__":
    unittest.main()
