"""Concern: citations are references, never reproduced standard text.

The AAOIFI Sharia Standards text is copyrighted. A citation must point to a
standard by number/topic/principle — it must NOT carry a reproduced clause /
passage. This guard fails closed on any citation field that looks like
reproduced text.

Two tests per field:
  C1  length bound — a reference is short; a passage is long. Per-field word
      and character caps.
  C2  no long verbatim quoted span — a quoted run over QUOTE_CAP characters is
      treated as reproduced clause text and rejected.

Checked fields: rule sources `ref` and `principle`; defer position `citation`;
glossary grounding `sources`.

Stdlib only. No sibling imports. Entry points:
  `check(rules_data, defer_data, glossary_data) -> list[str]`
  `check_field(text, kind) -> list[str]`   (reusable by a future appender)
"""
import re

# Per-kind caps: (max_chars, max_words). A reference is terse; a passage is not.
CAPS = {
    "ref":       (160, 28),
    "principle": (320, 55),
    "citation":  (200, 32),
    "gloss_src": (240, 42),
}
QUOTE_CAP = 100  # a quoted span longer than this is reproduced clause text
_QUOTED = re.compile(r"[\"“”«»]([^\"“”«»]{%d,})[\"“”«»]" % (QUOTE_CAP + 1))


def check_field(text, kind, where=""):
    errors = []
    max_chars, max_words = CAPS[kind]
    if len(text) > max_chars:
        errors.append(f"C1 {where}: {kind} over {max_chars} chars (len={len(text)}) — looks like a passage, not a reference")
    if len(text.split()) > max_words:
        errors.append(f"C1 {where}: {kind} over {max_words} words — looks like a passage, not a reference")
    if _QUOTED.search(text):
        errors.append(f"C2 {where}: {kind} contains a quoted span >{QUOTE_CAP} chars — possible reproduced standard text")
    return errors


def check(rules_data, defer_data, glossary_data):
    errors = []
    for r in rules_data.get("rules", []):
        rid = r.get("id", "<no-id>")
        for i, s in enumerate(r.get("sources", [])):
            errors += check_field(s.get("ref", ""), "ref", f"{rid}.sources[{i}].ref")
            errors += check_field(s.get("principle", ""), "principle", f"{rid}.sources[{i}].principle")
    for e in defer_data.get("entries", []):
        eid = e.get("id", "<no-id>")
        for i, p in enumerate(e.get("positions", [])):
            errors += check_field(p.get("citation", ""), "citation", f"{eid}.positions[{i}].citation")
    for g in glossary_data.get("entries", []):
        gid = g.get("term_id", "<no-id>")
        for i, src in enumerate(g.get("provenance", {}).get("sources", [])):
            errors += check_field(src, "gloss_src", f"{gid}.grounding.sources[{i}]")
    return errors
