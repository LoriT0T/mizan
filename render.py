"""Render human-readable Markdown views from the registry JSON (the source of
truth). Rendered files are DERIVED — never hand-edited — so they cannot drift
from the data. Run: python3 render.py  (writes into rendered/).

The consolidated Arabic review list (rendered/ARABIC_REVIEW_LIST.md) is authored
separately because it carries the agent's grounding notes and alternatives
considered, which are not stored in the data.
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))


def load(name):
    with open(os.path.join(ROOT, "registry", name), encoding="utf-8") as f:
        return json.load(f)


def w(name, text):
    path = os.path.join(ROOT, "rendered", name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def render_registry(rules):
    L = rules["source_layers"]
    out = []
    out.append(f"# {rules['registry']} — Rendered View\n")
    out.append(f"_Version {rules['version']} · scope: {rules['scope']} · DERIVED from `registry/rules.json` — do not hand-edit._\n")
    out.append("> **Mizan is a copilot, never a mufti.** It researches, drafts, and documents for a qualified human scholar (SSB); it never issues a ruling. Contested matters are surfaced, never adjudicated.\n")
    out.append("## Source layers\n")
    for key, desc in L.items():
        out.append(f"- **{key}** — {desc}\n")
    out.append(f"\n> **Copyright boundary.** {rules['copyright_boundary']}\n")
    out.append(f"\n> **Language authority.** {rules['language_authority']}\n")
    out.append("\n---\n")
    for r in rules["rules"]:
        badge = "🟢 established" if r["status"] == "established" else "🟠 contested"
        out.append(f"\n## {r['id']} — {r['title_en']}  ·  {badge}\n")
        out.append(f"**العنوان:** {r['title_ar']}\n")
        out.append(f"\n**Arabic (canonical):**\n\n> {r['rule_ar']}\n")
        out.append(f"\n**English (parallel):**\n\n> {r['rule_en']}\n")
        out.append(f"\n_Arabic review status: **{r['arabic_review_status']}** · provenance: {r['provenance']['input']} · grounding: {r['provenance']['grounding_basis']}_\n")
        out.append("\n**What satisfies it:**\n")
        for s in r["satisfied_by"]:
            out.append(f"- {s['en']}\n  - {s['ar']}\n")
        out.append("\n**What violates it (concrete contract patterns):**\n")
        for v in r["violated_by"]:
            out.append(f"- {v['en']}\n  - {v['ar']}\n")
        out.append("\n**Sources (layer · citation · principle):**\n")
        for s in r["sources"]:
            synth = " · **SYNTHETIC**" if s["synthetic"] else ""
            out.append(f"- **{s['layer']}**{synth} — {s['ref']}\n  - _{s['principle']}_\n")
        if r.get("defer_ref"):
            out.append(f"\n↪ **Contested / cross-listed in the defer register:** {r['defer_ref']}\n")
        if r.get("notes"):
            out.append(f"\n_Note: {r['notes']}_\n")
        out.append("\n---\n")
    return "".join(out)


def render_defer(defer):
    out = []
    out.append(f"# {defer['register']} — Rendered View\n")
    out.append(f"_Version {defer['version']} · DERIVED from `registry/defer_register.json` — do not hand-edit._\n")
    out.append(f"\n> **Principle.** {defer['principle']}\n\n---\n")
    for e in defer["entries"]:
        scope = "within Murabaha scope" if e["scope_status"] == "in-murabaha-scope" else "OUT of Murabaha scope"
        out.append(f"\n## {e['id']}  ·  _{scope}_")
        if e.get("related_rule"):
            out.append(f"  ·  related rule: {e['related_rule']}")
        out.append("\n")
        out.append(f"\n**The question (EN):** {e['question_en']}\n")
        out.append(f"\n**السؤال (AR):** {e['question_ar']}\n")
        out.append("\n**Divergent authoritative positions:**\n")
        for p in e["positions"]:
            out.append(f"\n- **{p['authority']}**\n")
            out.append(f"  - EN: {p['position_en']}\n")
            out.append(f"  - AR: {p['position_ar']}\n")
            out.append(f"  - _Citation: {p['citation']}_\n")
        out.append(f"\n**Routing (EN):** {e['routing_en']}\n")
        out.append(f"\n**التوجيه (AR):** {e['routing_ar']}\n")
        out.append(f"\n_Provenance: {e['provenance']['input']} · grounding: {e['provenance']['grounding_basis']}_\n")
        out.append("\n---\n")
    return "".join(out)


def render_glossary(gloss):
    gp = gloss["growth_protocol"]
    out = []
    out.append(f"# {gloss['glossary']} — Rendered View\n")
    out.append(f"_Version {gloss['version']} · DERIVED from `registry/glossary.json` — do not hand-edit._\n")
    out.append(f"\n> **Discipline.** {gloss['discipline']}\n")
    out.append(f"\n## Growth protocol\n\n_{gp['summary']}_\n\n")
    for s in gp["steps"]:
        out.append(f"- {s}\n")
    out.append("\n---\n\n## Entries\n")
    for status_filter, heading in [("seed", "### Seed terms (status: locked-pending-calibration)"),
                                    ("growth-protocol", "### Growth-protocol terms")]:
        out.append(f"\n{heading}\n\n")
        out.append("| ID | Arabic (canonical) | English (canonical) | Status | Grounding basis | Sources |\n")
        out.append("|---|---|---|---|---|---|\n")
        for g in gloss["entries"]:
            if g["origin"] != status_filter:
                continue
            src = "; ".join(g["provenance"]["sources"])
            out.append(f"| {g['term_id']} | {g['canonical_ar']} | {g['canonical_en']} | {g['status']} | {g['provenance']['grounding_basis']} | {src} |\n")
    out.append("\n### Definitions\n")
    for g in gloss["entries"]:
        note = f" _(scope: {g['scope_note']})_" if g.get("scope_note") else ""
        out.append(f"\n- **{g['term_id']} · {g['canonical_ar']} — {g['canonical_en']}**{note}\n")
        out.append(f"  - AR: {g['definition_ar']}\n")
        out.append(f"  - EN: {g['definition_en']}\n")
        if g.get("review_routing"):
            out.append(f"  - ↪ _Routed: {g['review_routing']}_\n")
    return "".join(out)


def render_scope(scope):
    out = [f"# {scope['scope_registry']} — Rendered View\n",
           f"_Version {scope['version']} · DERIVED from `registry/scope_registry.json` — do not hand-edit._\n",
           f"\n> **Purpose.** {scope['purpose']}\n",
           f"\n**[ع]** {scope['statement_ar']}\n",
           f"\n**[EN]** {scope['statement_en']}\n",
           "\n## Coverage\n\n| Type | Status | Rule-set | Depth |\n|---|---|---|---|\n"]
    for c in scope["coverage"]:
        out.append(f"| {c['type']} | {c['status']} ({c.get('label_en','')}) | {c.get('rule_set') or '—'} | {c['depth']} |\n")
    out.append(f"\n## Out-of-scope finding text\n\n**[ع]** {scope['out_of_scope_finding_text']['ar']}\n\n"
               f"**[EN]** {scope['out_of_scope_finding_text']['en']}\n")
    return "".join(out)


def main():
    rules = load("rules.json")
    defer = load("defer_register.json")
    gloss = load("glossary.json")
    paths = [
        w("REGISTRY.md", render_registry(rules)),
        w("DEFER_REGISTER.md", render_defer(defer)),
        w("GLOSSARY.md", render_glossary(gloss)),
    ]
    import os
    if os.path.exists(os.path.join(ROOT, "registry", "rules_ijara.json")):
        paths.append(w("REGISTRY_IJARA.md", render_registry(load("rules_ijara.json"))))
        paths.append(w("DEFER_REGISTER_IJARA.md", render_defer(load("defer_register_ijara.json"))))
        paths.append(w("SCOPE.md", render_scope(load("scope_registry.json"))))
    for p in paths:
        print(f"wrote {p}")


if __name__ == "__main__":
    main()
