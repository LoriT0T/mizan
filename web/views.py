"""Pure rendering for the Mizan web UI. No rule logic, no registry reads.

Every function returns (html_str, ui_strings) where ui_strings is the list of
UI-AUTHORED text fragments (chrome, headings, status labels) — the server runs
the never-rules guard over these as a serve-time gate. ALL engine-derived
content (quotes, citations, memo/matrix) is HTML-escaped (untrusted upload =
no XSS) and is attributed/exempt from the verdict gate.

UI status labels come from the engine's status vocabulary ONLY — the UI never
invents a verdict. Arabic renders RTL via dir="auto"/bidi isolation.
"""
import html

# Bilingual UI labels for the engine's status vocabulary (the ONLY statuses the
# UI shows). None of these are permissibility verdicts.
STATUS_LABEL = {
    "satisfied":     ("satisfied", "مستوفاة"),
    "violated":      ("matches a violation pattern", "ينطبق عليها نمطُ مخالفة"),
    "indeterminate": ("indeterminate (missing fact / not engaged)", "غير محدَّدة"),
    "deferral":      ("DEFERRED to the SSB — not graded", "مُحالة إلى الهيئة — لا تُصنَّف"),
    "out_of_scope":  ("OUT OF SCOPE — not assessed, routed to scholar", "خارج النطاق — لا يُقيَّم، يُحال للعالِم"),
}
STATUS_CLASS = {"satisfied": "ok", "violated": "bad", "indeterminate": "warn",
                "deferral": "defer", "out_of_scope": "oos"}

WATERMARK_AR = "أداة بحث وصياغة — ليست فتوى. للعرض على عالم شرعي مؤهّل."
WATERMARK_EN = "Research and drafting aid — not a fatwa. For review by a qualified Sharia scholar."

_CSS = """
:root{--bad:#b00020;--ok:#0a7d28;--warn:#9a6700;--defer:#5a3fb0;--oos:#7a4a00;}
*{box-sizing:border-box} body{font-family:system-ui,Segoe UI,Arial;margin:0;background:#f6f7f9;color:#111}
.wrap{max-width:1000px;margin:0 auto;padding:16px}
.wm{background:#1d1f23;color:#fff;padding:10px 14px;border-radius:8px;margin:10px 0;font-weight:600;line-height:1.5}
.badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:13px;margin:4px 6px 4px 0}
.badge.nokey{background:#fde68a;color:#7a4a00} .badge.key{background:#bbf7d0;color:#0a7d28}
.badge.cal{background:#e0e7ff;color:#3730a3}
.card{background:#fff;border:1px solid #e3e6ea;border-radius:10px;padding:14px;margin:12px 0}
h1{font-size:22px} h2{font-size:18px;margin:14px 0 8px}
table{width:100%;border-collapse:collapse;font-size:14px} th,td{border:1px solid #e3e6ea;padding:7px;vertical-align:top;text-align:start}
th{background:#f0f2f5}
.st{font-weight:700;padding:2px 8px;border-radius:6px;color:#fff;white-space:nowrap}
.st.ok{background:var(--ok)} .st.bad{background:var(--bad)} .st.warn{background:var(--warn)}
.st.defer{background:var(--defer)} .st.oos{background:var(--oos)}
.q{background:#fafbfc;border-inline-start:3px solid #cbd5e1;padding:6px 9px;border-radius:4px;white-space:pre-wrap}
textarea{width:100%;height:240px;font-family:ui-monospace,monospace;padding:8px}
pre{white-space:pre-wrap;background:#fafbfc;border:1px solid #e3e6ea;border-radius:8px;padding:10px;max-height:420px;overflow:auto}
.btn{background:#1d4ed8;color:#fff;border:0;padding:9px 16px;border-radius:8px;font-size:15px;cursor:pointer;text-decoration:none;display:inline-block}
.muted{color:#555;font-size:13px} a{color:#1d4ed8}
[dir=auto]{unicode-bidi:plaintext}
"""


def _page(title, body_html):
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{html.escape(title)}</title><style>{_CSS}</style></head>"
            f"<body><div class='wrap'>{body_html}</div></body></html>")


def _watermark_html():
    return (f"<div class='wm'><div dir='auto'>{html.escape(WATERMARK_AR)}</div>"
            f"<div>{html.escape(WATERMARK_EN)}</div></div>")


def render_index(seam_available, calibration):
    ui = ["Mizan — local Sharia-review copilot", "Paste a contract or upload a .txt file",
          "Run review", "Scope: what Mizan covers", WATERMARK_AR, WATERMARK_EN,
          STATUS_LABEL["deferral"][0], STATUS_LABEL["out_of_scope"][0]]
    keybadge = ("<span class='badge key'>model available</span>" if seam_available
                else "<span class='badge nokey'>NO-KEY mode — deterministic extraction only</span>")
    cal = (f"<span class='badge cal'>{html.escape(calibration['summary_en'])}</span>")
    body = (f"{_watermark_html()}"
            f"<h1>Mizan — local Sharia-review copilot <span class='muted'>ميزان</span></h1>"
            f"<p class='muted'>Local demonstration. Mizan flags, identifies and cites for a qualified scholar; "
            f"it does <b>not</b> determine Sharia compliance and never issues a fatwa.</p>"
            f"<div>{keybadge} {cal}</div>"
            f"<div class='card'><form method='POST' action='/run' enctype='multipart/form-data'>"
            f"<h2>Paste a contract (Arabic / English / mixed)</h2>"
            f"<textarea name='text' dir='auto' placeholder='Paste contract text here…'></textarea>"
            f"<h2>…or upload a .txt file</h2><input type='file' name='file' accept='.txt,text/plain'>"
            f"<p><button class='btn' type='submit'>Run review · ابدأ المراجعة</button></p></form></div>"
            f"<p><a href='/scope'>Scope: what Mizan covers, and to what depth →</a></p>")
    return _page("Mizan — local copilot", body), ui


def _findings_table(findings):
    rows = []
    for f in findings:
        st = f.get("status", "")
        en, ar = STATUS_LABEL.get(st, (st, st))
        cls = STATUS_CLASS.get(st, "warn")
        rid = html.escape(str(f.get("rule_id") or f.get("component") or "—"))
        cites = "<br>".join(f"<b>[{html.escape(c['layer'])}]</b> {html.escape(c['ref'])}"
                            for c in f.get("citations", [])) or "—"
        quote = html.escape(f.get("quote") or f.get("note_en") or f.get("missing_fact") or "—")
        positions = ""
        if f.get("positions"):
            positions = "<div class='muted'>Positions surfaced (not adjudicated):<ul>" + "".join(
                f"<li dir='auto'>{html.escape(p['authority'])}: {html.escape(p['position_en'])} "
                f"[{html.escape(p['citation'])}]</li>" for p in f["positions"]) + "</ul></div>"
        rows.append(
            f"<tr><td>{rid}</td><td><span class='st {cls}'>{html.escape(en)}</span><br>"
            f"<span dir='auto' class='muted'>{html.escape(ar)}</span></td>"
            f"<td>{cites}{positions}</td><td><div class='q' dir='auto'>{quote}</div></td></tr>")
    return ("<table><thead><tr><th>Rule / component</th><th>Status (engine vocabulary)</th>"
            "<th>Citation · layer</th><th>Verbatim clause</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table>")


def render_result(result, calibration, run_id):
    cls = result["classification"]
    ui = ["Review result", "Classification", "Scope decision", "Findings",
          "Memo (download .md)", "Matrix (download .md)", "Run another",
          "Mizan does not determine Sharia compliance; the opinion is the scholar's alone.",
          WATERMARK_AR, WATERMARK_EN] + [v for pair in STATUS_LABEL.values() for v in pair]
    keybadge = ("<span class='badge key'>model available</span>" if result["seam_mode"].startswith("model")
                else "<span class='badge nokey'>NO-KEY mode — deterministic extraction only</span>")
    calbadge = f"<span class='badge cal' dir='auto'>{html.escape(calibration['summary_en'])}</span>"
    covered = ", ".join(result["covered_types"]) or "(none covered)"
    unrec = ", ".join(cls.get("unrecognized_components", [])) or "—"
    scope_html = (f"<p><b>Classified type(s):</b> {html.escape(', '.join(cls['types']))} · "
                  f"<b>unrecognized component(s):</b> {html.escape(unrec)}</p>"
                  f"<p><b>Checked (covered + calibrated):</b> {html.escape(covered)}. "
                  f"Uncovered/unrecognized components are flagged out-of-scope and routed to the scholar — "
                  f"no rule is fabricated or applied to them.</p>")
    memo_md = html.escape(result["memo"]["render_md"])
    matrix_md = html.escape(result["matrix"]["render_md"])
    body = (f"{_watermark_html()}"
            f"<h1>Review result <span class='muted'>نتيجة المراجعة</span></h1>"
            f"<div>{keybadge} {calbadge}</div>"
            f"<p class='muted'>Mizan does not determine Sharia compliance; the opinion is the scholar&#39;s alone. Findings are a research/drafting aid.</p>"
            f"<div class='card'><h2>Classification &amp; scope · التصنيف والنطاق</h2>{scope_html}</div>"
            f"<div class='card'><h2>Findings · النتائج</h2>{_findings_table(result['findings'])}</div>"
            f"<div class='card'><h2>Sharia-review memo · المذكّرة "
            f"<a class='btn' href='/download?run={html.escape(run_id)}&amp;doc=memo'>download .md</a></h2>"
            f"<pre dir='auto'>{memo_md}</pre></div>"
            f"<div class='card'><h2>Non-compliance matrix · المصفوفة "
            f"<a class='btn' href='/download?run={html.escape(run_id)}&amp;doc=matrix'>download .md</a></h2>"
            f"<pre dir='auto'>{matrix_md}</pre></div>"
            f"<p><a class='btn' href='/'>Run another · مراجعة أخرى</a></p>")
    return _page("Mizan — result", body), ui


def render_scope(scope, calibration):
    ui = ["Scope: what Mizan covers", "Back to home", WATERMARK_AR, WATERMARK_EN,
          html.escape(scope["statement_en"])]
    rows = "".join(
        f"<tr><td>{html.escape(c['type'])}</td><td>{html.escape(c['status'])}</td>"
        f"<td>{html.escape(c.get('rule_set') or '—')}</td><td>{html.escape(c['depth'])}</td></tr>"
        for c in scope["coverage"])
    body = (f"{_watermark_html()}<h1>Scope — what Mizan covers</h1>"
            f"<div class='card'><p dir='auto'><b>[ع]</b> {html.escape(scope['statement_ar'])}</p>"
            f"<p><b>[EN]</b> {html.escape(scope['statement_en'])}</p>"
            f"<table><thead><tr><th>Type</th><th>Status</th><th>Rule-set</th><th>Depth</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>"
            f"<p class='muted' dir='auto'>Out-of-scope finding text: {html.escape(scope['out_of_scope_finding_text']['en'])}</p>"
            f"</div><p><a href='/'>← Back</a></p>")
    return _page("Mizan — scope", body), ui


def render_error(msg):
    ui = ["Error", msg]
    return _page("Mizan — error", f"{_watermark_html()}<h1>Could not process</h1>"
                 f"<div class='card'><p>{html.escape(msg)}</p><p><a href='/'>← Back</a></p></div>"), ui
