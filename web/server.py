"""Mizan local web server — stdlib http.server only (zero external deps,
consistent with the engine's dependency-free discipline; Python 3.14 removed
`cgi`, so multipart is hand-parsed).

Security posture (local-only, built like it matters):
  - binds 127.0.0.1 ONLY; refuses 0.0.0.0 / any non-loopback host;
  - OPENROUTER_API_KEY read from server env at startup ONLY; every served byte
    is scanned for the key pattern and the run aborts if it ever appears;
  - NO-KEY mode is first-class (visible badge);
  - uploads untrusted: size-capped, .txt/paste only, run through the engine's
    input rail (injection-inert), held in RAM for the session only (never
    persisted to disk), no telemetry, no external calls except the model seam;
  - the never-rules guard runs over UI-authored chrome at serve time.

The WALL: this file imports the orchestrator as a library + the never_rules
guard. It contains no rule logic, no registry reads, no checker code.
"""
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))

import orchestrator                 # engine, as a library
import never_rules_guard            # the guard utility (no rule logic)
sys.path.insert(0, HERE)
import views

MAX_UPLOAD = 256 * 1024             # 256 KB cap on untrusted input
_RUNS = {}                          # run_id -> {memo_md, matrix_md}; RAM only, not persisted
_RUN_SEQ = [0]
# Belt-and-suspenders key scan: the live key value + the OpenRouter key shape.
_KEY_RX = re.compile(r"sk-or-[A-Za-z0-9_\-]{8,}")


def _seam():
    return orchestrator.model_seam.make_seam()


def _scan_for_key(data: bytes) -> bool:
    key = os.environ.get("OPENROUTER_API_KEY") or None     # read live so it is never stale
    if key and key.encode("utf-8") in data:
        return True
    return bool(_KEY_RX.search(data.decode("utf-8", "replace")))


def _parse_multipart(body: bytes, boundary: bytes):
    fields, files = {}, {}
    for part in body.split(b"--" + boundary):
        part = part.strip(b"\r\n")
        if not part or part == b"--" or b"\r\n\r\n" not in part:
            continue
        head, _, content = part.partition(b"\r\n\r\n")
        headers = head.decode("utf-8", "replace")
        name = re.search(r'name="([^"]*)"', headers)
        fname = re.search(r'filename="([^"]*)"', headers)
        if not name:
            continue
        content = content.rstrip(b"\r\n")
        if fname:
            files[name.group(1)] = (fname.group(1), content)
        else:
            fields[name.group(1)] = content.decode("utf-8", "replace")
    return fields, files


class Handler(BaseHTTPRequestHandler):
    server_version = "MizanLocal/1.0"

    def log_message(self, fmt, *args):
        # Minimal logging; NEVER log request bodies or the key.
        sys.stderr.write("[mizan] %s %s\n" % (self.command, self.path.split("?")[0]))

    # ---- serve helpers (key scan + serve-time guard run here) ----
    def _serve(self, html_str, ui_strings, status=200, content_type="text/html; charset=utf-8",
               raw_bytes=None, headers=None):
        gate = never_rules_guard.check_prose(ui_strings or [])
        if gate:
            status, html_str, raw_bytes = 500, "<h1>serve-time guard tripped (fail closed)</h1>", None
        data = raw_bytes if raw_bytes is not None else html_str.encode("utf-8")
        if _scan_for_key(data):
            status, data = 500, b"<h1>blocked: response would expose the API key (fail closed)</h1>"
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            html_str, ui = views.render_index(_seam().available(), orchestrator.calibration_status())
            self._serve(html_str, ui)
        elif u.path == "/scope":
            html_str, ui = views.render_scope(orchestrator.scope_info(), orchestrator.calibration_status())
            self._serve(html_str, ui)
        elif u.path == "/download":
            q = parse_qs(u.query)
            run = (q.get("run") or [""])[0]
            doc = (q.get("doc") or [""])[0]
            bundle = _RUNS.get(run)
            if not bundle or doc not in ("memo", "matrix"):
                html_str, ui = views.render_error("download not found (session expired)")
                return self._serve(html_str, ui, status=404)
            md = bundle["memo_md"] if doc == "memo" else bundle["matrix_md"]
            self._serve(None, [], content_type="text/markdown; charset=utf-8",
                        raw_bytes=md.encode("utf-8"),
                        headers={"Content-Disposition": f'attachment; filename="mizan_{doc}.md"'})
        else:
            html_str, ui = views.render_error("not found")
            self._serve(html_str, ui, status=404)

    def do_POST(self):
        u = urlparse(self.path)
        if u.path != "/run":
            html_str, ui = views.render_error("not found")
            return self._serve(html_str, ui, status=404)
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_UPLOAD:
            html_str, ui = views.render_error(f"input too large (cap {MAX_UPLOAD // 1024} KB)")
            return self._serve(html_str, ui, status=413)
        body = self.rfile.read(length)
        ctype = self.headers.get("Content-Type", "")
        text = ""
        if ctype.startswith("multipart/form-data"):
            m = re.search(r"boundary=(.+)$", ctype)
            if m:
                fields, files = _parse_multipart(body, m.group(1).strip('"').encode("utf-8"))
                text = (fields.get("text") or "").strip()
                if not text and "file" in files:
                    fname, content = files["file"]
                    if not fname.lower().endswith(".txt"):
                        html_str, ui = views.render_error("only .txt uploads are accepted")
                        return self._serve(html_str, ui, status=415)
                    text = content.decode("utf-8", "replace").strip()
        else:
            text = parse_qs(body.decode("utf-8", "replace")).get("text", [""])[0].strip()

        if not text:
            html_str, ui = views.render_error("no contract text provided")
            return self._serve(html_str, ui, status=400)

        try:
            result = orchestrator.generate_for_text(text, source_label="(uploaded)", seam=_seam())
        except Exception as e:                       # engine fail-closed surfaces as an error page
            html_str, ui = views.render_error(f"engine could not process this input: {type(e).__name__}")
            return self._serve(html_str, ui, status=500)

        _RUN_SEQ[0] += 1
        run_id = f"r{_RUN_SEQ[0]}"
        _RUNS[run_id] = {"memo_md": result["memo"]["render_md"], "matrix_md": result["matrix"]["render_md"]}
        for old in list(_RUNS)[:-8]:                 # keep only the last few; RAM only
            _RUNS.pop(old, None)
        html_str, ui = views.render_result(result, orchestrator.calibration_status(), run_id)
        self._serve(html_str, ui)


def serve(host="127.0.0.1", port=8765):
    if host not in ("127.0.0.1", "localhost", "::1"):
        raise SystemExit(f"refusing to bind non-loopback host {host!r} — Mizan is local-only (no public hosting)")
    httpd = ThreadingHTTPServer((host, port), Handler)
    mode = "model available" if _seam().available() else "NO-KEY (deterministic)"
    sys.stderr.write(f"[mizan] local server on http://{host}:{port}  ·  seam: {mode}\n")
    sys.stderr.write("[mizan] local demonstration — not deployed, not certified. Ctrl-C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


if __name__ == "__main__":
    h = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    p = int(sys.argv[2]) if len(sys.argv) > 2 else 8765
    serve(h, p)
