"""Concern: findings -> the non-compliance MATRIX (Input #2, Part 4).

Row: finding -> contract clause (VERBATIM quote, Arabic preserved) -> rule
breached with layer + citation -> severity (CONFIGURABLE tiers, labelled in-file
as a convention, NOT a binding scale) -> risk type -> recommended remediation
(from the registry's remediation types) -> status (open) -> owner (blank).
DEFERRAL rows carry NO severity — contested matters are not graded. Only
non-satisfied findings populate the matrix. Bilingual parallel.

Imports no sibling. Entry point:
  `generate(findings, authoritative_lang="ar", severity_config=None) -> dict`
"""

# Same canonical watermark as the memo (each document carries it independently).
WATERMARK_AR = "أداة بحث وصياغة — ليست فتوى. للعرض على عالم شرعي مؤهّل."
WATERMARK_EN = "Research and drafting aid — not a fatwa. For review by a qualified Sharia scholar."

SEVERITY_NOTE_AR = ("تصنيفُ الخطورة (طفيف/متوسّط/جسيم) اصطلاحٌ قابلٌ للضبط (مخطَّطٌ أكاديميٌّ من دراسة ISRA)، "
                    "وليس سُلَّماً مُلزِماً من AAOIFI. المسائلُ الخلافيةُ لا تُصنَّف.")
SEVERITY_NOTE_EN = ("The severity tiers (minor/moderate/major) are a CONFIGURABLE convention (an ISRA academic "
                    "scheme), NOT a binding AAOIFI scale. Contested matters are not graded.")

# Default convention (configurable via severity_config).
DEFAULT_SEVERITY = {"R1": "major", "R2": "moderate", "R3": "major", "R4": "major", "R5": "moderate",
                    "I1": "major", "I2": "moderate", "I3": "major", "I4": "major", "I5": "major",
                    "I6": "major", "I7": "major"}
SEV_AR = {"minor": "طفيف", "moderate": "متوسّط", "major": "جسيم"}
RISK = {
    "R1": ("تنظيميّ/ماليّ", "regulatory/financial"),
    "R2": ("تنظيميّ", "regulatory"),
    "R3": ("سمعيّ/تنظيميّ", "reputational/regulatory"),
    "R4": ("تنظيميّ", "regulatory"),
    "R5": ("تنظيميّ", "regulatory"),
    "I1": ("سمعيّ/تنظيميّ", "reputational/regulatory"),
    "I2": ("تنظيميّ", "regulatory"),
    "I3": ("تنظيميّ", "regulatory"),
    "I4": ("تنظيميّ/ماليّ", "regulatory/financial"),
    "I5": ("تنظيميّ/ماليّ", "regulatory/financial"),
    "I6": ("تنظيميّ", "regulatory"),
    "I7": ("تنظيميّ", "regulatory"),
}
REMEDIATION = {
    "R1": ("تصحيحُ الهيكل بحيث يتملّك المصرفُ الأصلَ ويقبضه قبل البيع؛ والعرضُ على الهيئة الشرعية.",
           "Rectify the structure so the bank takes ownership and possession before sale; escalate to the SSB."),
    "R2": ("الإفصاحُ عن التكلفة وهامش الربح وتثبيتُ الثمن عند العقد؛ تصحيحُ البند.",
           "Disclose cost and markup and fix the price at contract; rectify the clause."),
    "R3": ("الامتناعُ عن تمويل الأصل المحرَّم؛ وتطهيرُ أيِّ إيرادٍ متحقّق؛ والعرضُ على الهيئة.",
           "Do not finance the prohibited-category asset; purify any income realised; escalate to the SSB."),
    "R4": ("إعادةُ الهيكلة بأصلٍ من طرفٍ ثالث لا من العميل؛ والعرضُ على الهيئة.",
           "Restructure with a third-party asset (not the customer's); escalate to the SSB."),
    "R5": ("توجيهُ غرامة التأخّر إلى جهةٍ خيرية (تطهيرُ الإيراد)؛ ومنعُ زيادة الربح؛ تصحيحُ البند.",
           "Direct the late-payment penalty to charity (income purification); bar markup increase; rectify the clause."),
}
REMEDIATION.update({
    "I1": ("قصرُ الإجارة على عينٍ غيرِ مستهلكةٍ معيَّنةٍ مباحةِ الاستعمال؛ والعرضُ على الهيئة.",
           "Restrict the lease to an identified non-consumable asset put to a lawful use; escalate to the SSB."),
    "I2": ("تحديدُ الأجرة والمدّة عند العقد وإلغاءُ حقّ الزيادة المنفردة؛ تصحيحُ البند.",
           "Define rent and term at contract and remove the unilateral-increase right; rectify the clause."),
    "I3": ("تأخيرُ عقد الإجارة حتى يتملّك المصرفُ العين ويقبضها؛ والعرضُ على الهيئة.",
           "Defer the lease until the bank acquires and possesses the asset; escalate to the SSB."),
    "I4": ("إعادةُ تبعة الملكية (الصيانة الأساسية والتكافل والتلف الكلّي) إلى المؤجِّر؛ تصحيحُ البنود؛ والعرضُ على الهيئة.",
           "Return ownership risk (basic maintenance, takaful, total-loss) to the lessor; rectify the clauses; escalate to the SSB."),
    "I5": ("ربطُ استحقاق الأجرة بالتسليم لا بتاريخ العقد؛ وإسقاطُها عند تعطّل المنفعة بلا تعدٍّ؛ تصحيحُ البند.",
           "Tie rent accrual to delivery, not the contract date; abate it on non-negligent loss of use; rectify the clause."),
    "I6": ("إفرادُ نقل الملكية بأداةٍ مستقلّةٍ عن عقد الإجارة؛ تصحيحُ الهيكل؛ والعرضُ على الهيئة.",
           "Set the ownership transfer in an instrument separate from the lease; restructure; escalate to the SSB."),
    "I7": ("إيجادُ فاصلٍ زمنيٍّ معتبرٍ بين البيع والاستئجار؛ والعرضُ على الهيئة.",
           "Introduce a genuine interval between sale and leaseback; escalate to the SSB."),
})
INDET_REMEDIATION = ("استكمالُ الواقعة الناقصة ثم إعادةُ الفحص؛ مراجعةٌ بشرية.",
                     "Obtain the missing fact then re-check; human review.")
DEFER_REMEDIATION = ("الإحالةُ إلى الهيئة الشرعية للبتّ (مسألةٌ خلافية).",
                     "Escalation to the SSB for determination (contested matter).")
OOS_REMEDIATION = ("الإحالةُ إلى عالمٍ شرعيٍّ مؤهّل (خارجَ نطاق التغطية المعايَرة لميزان).",
                   "Route to a qualified Sharia scholar (outside Mizan's calibrated coverage).")


def generate(findings, authoritative_lang="ar", severity_config=None):
    sev = dict(DEFAULT_SEVERITY)
    if severity_config:
        sev.update(severity_config)
    rows = []
    generated_prose = [SEVERITY_NOTE_AR, SEVERITY_NOTE_EN]
    for f in findings:
        status = f.get("status")
        if status == "satisfied":
            continue   # non-compliance matrix lists only non-satisfied findings
        rid = f.get("rule_id") or "—"
        citations = [f"[{c['layer']}] {c['ref']}" for c in f.get("citations", [])]
        if status == "deferral":
            severity = None
            rem_ar, rem_en = DEFER_REMEDIATION
        elif status == "indeterminate":
            severity = None
            rem_ar, rem_en = INDET_REMEDIATION
        elif status == "out_of_scope":
            severity = None
            rem_ar, rem_en = OOS_REMEDIATION
        else:  # violated
            severity = sev.get(rid)
            rem_ar, rem_en = REMEDIATION.get(rid, ("—", "—"))
        risk_ar, risk_en = RISK.get(rid, ("—", "—"))
        if status == "out_of_scope":
            comp = f.get("component", "unrecognized")
            rule_ar = f"مكوِّن خارج النطاق: {comp}"
            rule_en = f"out-of-scope component: {comp}"
            clause = f.get("note_en", "") or f.get("note", "")
        else:
            rule_ar, rule_en = f.get("rule_title_ar", ""), f.get("rule_title_en", "")
            clause = f.get("quote", "") or (f.get("missing_fact", "") if status == "indeterminate" else "")
        rows.append({
            "rule_id": rid or "—",
            "status": status,
            "rule_ar": rule_ar, "rule_en": rule_en,
            "clause_quote": clause,
            "citations": citations,
            "severity": severity, "severity_ar": (SEV_AR.get(severity) if severity else None),
            "risk_ar": risk_ar, "risk_en": risk_en,
            "remediation_ar": rem_ar, "remediation_en": rem_en,
            "status_field": "open", "owner": "",
        })
        generated_prose += [rem_ar, rem_en]
    matrix = {"rows": rows, "authoritative_language": authoritative_lang,
              "severity_note": {"ar": SEVERITY_NOTE_AR, "en": SEVERITY_NOTE_EN},
              "generated_prose": generated_prose}
    matrix["render_md"] = render(matrix)
    return matrix


def _sev_cell(row):
    if row["status"] == "deferral":
        return "— (لا تُصنَّف / not graded)"
    if row["status"] == "out_of_scope":
        return "— (خارج النطاق / out of scope)"
    if row["severity"] is None:
        return "— (—)"
    return f"{row['severity_ar']} / {row['severity']}"


def render(matrix):
    wm = f"> **{WATERMARK_AR}**\n> **{WATERMARK_EN}**\n"
    out = ["# مصفوفة عدم المطابقة — Non-Compliance Matrix\n", wm,
           f"\n> {matrix['severity_note']['ar']}\n> {matrix['severity_note']['en']}\n"]
    if not matrix["rows"]:
        out.append("\n_لا توجد بنودٌ غير مستوفاة. / No non-satisfied findings._\n")
        out.append("\n" + wm)
        return "".join(out)
    out.append("\n| القاعدة Rule | الحالة Status | البند (نصٌّ حرفيّ) Clause (verbatim) | القاعدة المخالَفة + الطبقة Rule + layer | الخطورة Severity | نوع الخطر Risk | المعالجة الموصى بها Remediation | الحالة Status | الجهة Owner |\n")
    out.append("|---|---|---|---|---|---|---|---|---|\n")
    for r in matrix["rows"]:
        cites = "<br>".join(r["citations"])
        clause = (r["clause_quote"] or "—").replace("\n", " ")
        out.append(f"| {r['rule_id']} | {r['status']} | {clause} | {r['rule_ar']} / {r['rule_en']}<br>{cites} "
                   f"| {_sev_cell(r)} | {r['risk_ar']} / {r['risk_en']} "
                   f"| {r['remediation_ar']} <br> {r['remediation_en']} | {r['status_field']} | {r['owner'] or '____'} |\n")
    out.append("\n" + wm)
    return "".join(out)
