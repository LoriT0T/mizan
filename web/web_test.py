"""Web-layer tests: routes, the WALL, key-never-served, serve-time guard.

Starts a real loopback server on an ephemeral port (threaded) and exercises it
over HTTP. No network beyond loopback. Run: python3 -m unittest web_test
"""
import os
import re
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer

import server
import views

HERE = os.path.dirname(os.path.abspath(__file__))


def _free_server():
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd, httpd.server_address[1]


def _get(port, path):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=10) as r:
        return r.status, r.read().decode("utf-8", "replace")


def _post_text(port, text):
    boundary = "----mizantest"
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"text\"\r\n\r\n{text}\r\n--{boundary}--\r\n").encode("utf-8")
    req = urllib.request.Request(f"http://127.0.0.1:{port}/run", data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status, r.read().decode("utf-8", "replace")


SAMPLE = open(os.path.join(os.path.dirname(HERE), "corpus", "stage3",
                           "T4_tawarruq_commodity_en.txt"), encoding="utf-8").read()


class TestRoutesAndWall(unittest.TestCase):
    def setUp(self):
        self.httpd, self.port = _free_server()

    def tearDown(self):
        self.httpd.shutdown()

    def test_index_and_scope_render(self):
        s, body = _get(self.port, "/")
        self.assertEqual(s, 200)
        self.assertIn("NO-KEY mode", body)
        self.assertIn("not a fatwa", body)
        s2, scope = _get(self.port, "/scope")
        self.assertIn("what Mizan covers", scope)

    def test_run_routes_through_engine(self):
        s, body = _post_text(self.port, SAMPLE)
        self.assertEqual(s, 200)
        self.assertIn("OUT OF SCOPE", body)          # tawarruq -> out of scope, no rule
        self.assertIn("نتيجة المراجعة", body)         # bilingual result page

    def test_wall_no_forbidden_imports(self):
        # web/ contains zero rule logic / registry reads / checker code.
        for fn in ("server.py", "views.py", "__init__.py"):
            src = open(os.path.join(HERE, fn), encoding="utf-8").read()
            self.assertNotIn("import checker", src, fn)
            self.assertNotIn("import extractor", src, fn)
            self.assertNotIn("registry/rules", src, fn)
            self.assertNotIn("rules.json", src, fn)
            self.assertNotIn("_EVALUATORS", src, fn)
        # but it DOES import the orchestrator (engine as a library)
        self.assertIn("import orchestrator", open(os.path.join(HERE, "server.py"), encoding="utf-8").read())

    def test_wall_engine_runs_without_web(self):
        # The engine is fully usable with no web import at all.
        import orchestrator as o
        res = o.run_text(SAMPLE, "(t)", seam=o.model_seam.NoKeySeam())
        self.assertTrue(any(f["status"] == "out_of_scope" for f in res["findings"]))


class TestKeyNeverServed(unittest.TestCase):
    def setUp(self):
        self._saved = os.environ.get("OPENROUTER_API_KEY")
        os.environ["OPENROUTER_API_KEY"] = "FAKEKEYDONOTLEAK0000"
        self.httpd, self.port = _free_server()

    def tearDown(self):
        self.httpd.shutdown()
        if self._saved is None:
            os.environ.pop("OPENROUTER_API_KEY", None)
        else:
            os.environ["OPENROUTER_API_KEY"] = self._saved

    def test_key_absent_from_every_served_response(self):
        sentinel = "FAKEKEYDONOTLEAK0000"
        for path in ("/", "/scope"):
            _, body = _get(self.port, path)
            self.assertNotIn(sentinel, body, path)
            self.assertNotIn("SENTINEL", body, path)
        _, run = _post_text(self.port, SAMPLE)
        self.assertNotIn(sentinel, run)
        self.assertNotIn("SENTINEL", run)


class TestServeTimeGuard(unittest.TestCase):
    def setUp(self):
        self.httpd, self.port = _free_server()
        self._orig = views.render_index

    def tearDown(self):
        views.render_index = self._orig
        self.httpd.shutdown()

    def test_poisoned_template_fails_closed(self):
        # Poison the UI chrome with a verdict -> the serve-time guard must block.
        def poisoned(seam_available, calibration):
            return "<h1>this contract is permissible — حلال</h1>", ["this contract is permissible — حلال"]
        views.render_index = poisoned
        import urllib.error
        with self.assertRaises(urllib.error.HTTPError) as cm:
            _get(self.port, "/")
        self.assertEqual(cm.exception.code, 500)
        self.assertIn("serve-time guard tripped", cm.exception.read().decode("utf-8", "replace"))


if __name__ == "__main__":
    unittest.main()
