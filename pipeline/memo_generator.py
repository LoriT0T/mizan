"""Concern: findings -> a bilingual Sharia-review MEMO (Input #2, Part 4 shape).

Arabic-FIRST: the Arabic memo is composed natively in formal MSA (fiqh register,
glossary-locked terms); the English is the parallel rendered FROM the Arabic.
The OPINION/RULING field is STRUCTURALLY EMPTY — reserved for a named human SSB
member; its setter refuses content (a structural lock, not a convention). Every
section carries the bilingual watermark. Deferral findings render as their own
section: the contested question, cited positions, routing — presented, never
resolved.

CONNECTIVE vs ATTRIBUTED (the gate boundary): each section separates
`connective_*` prose (authored/model-drafted — goes into `generated_prose` for
the never-rules generation gate) from `attributed_*` content (verbatim contract
quotes, registry citations, cited positions, the opinion placeholder — EXEMPT,
never placed in `generated_prose`). The model seam may draft connective prose
only; a verdict it emits lands in `generated_prose` and is caught.

NO-KEY mode assembles the same memo deterministically (less fluent, complete).
Dependency-injected (`seam`); imports no sibling. Entry point:
  `generate(structure, findings, rules, defer, glossary, seam=None,
            authoritative_lang="ar", contract_file="") -> dict`
"""

WATERMARK_AR = "أداة بحث وصياغة — ليست فتوى. للعرض على عالم شرعي مؤهّل."
WATERMARK_EN = "Research and drafting aid — not a fatwa. For review by a qualified Sharia scholar."

_STATUS_AR = {"satisfied": "مستوفاة", "violated": "ينطبق عليها نمطُ مخالفةِ القاعدة",
              "indeterminate": "غير محدَّدة (نقصُ بيان)", "deferral": "مُحالة إلى الهيئة الشرعية"}
_STATUS_EN = {"satisfied": "satisfied", "violated": "matches the rule's violation pattern",
              "indeterminate": "indeterminate (missing fact)", "deferral": "referred to the SSB"}


class OpinionField:
    """Structural lock: the opinion is reserved for a named human SSB member.
    No code path can write content — the setter always refuses."""
    PLACEHOLDER_AR = ("[يُترك هذا الحقل فارغاً عمداً. الرأيُ/الحكمُ الشرعيُّ من اختصاص "
                      "عضوٍ مُسمّى من الهيئة الشرعية وحده، ولا يُصدره هذا النظام.]")
    PLACEHOLDER_EN = ("[This field is intentionally left empty. The Sharia opinion/ruling is the "
                      "sole prerogative of a named SSB member and is never produced by this system.]")

    def set(self, *args, **kwargs):
        raise PermissionError("opinion field is reserved for a named human SSB member; the system cannot fill it")

    fill = set        # any alias also refuses

    def render_ar(self):
        return self.PLACEHOLDER_AR

    def render_en(self):
        return self.PLACEHOLDER_EN


def _desc_connective(structure, contract_type="murabaha"):
    if contract_type == "ijara":
        return ("هذه مراجعةٌ لعقد إجارةٍ (وقد تكون منتهيةً بالتمليك) بين المؤسسة المالية بوصفها مؤجِّراً والعميل بوصفه مستأجِراً؛ محلُّ الإجارة مبيَّنٌ نصّاً أدناه.",
                "This is a review of an Ijara (possibly Ijara Muntahia Bittamleek) between the institution as lessor and "
                "the customer as lessee; the leased asset is quoted verbatim below.")
    return ("هذه مراجعةٌ لعقد مرابحةٍ للآمر بالشراء بين المؤسسة المالية والعميل ومورّدٍ طرفٍ ثالث؛ محلُّ العقد مبيَّنٌ نصّاً أدناه.",
            "This is a review of a Murabaha-to-the-Purchase-Orderer contract between the institution, the customer, "
            "and a third-party supplier; the subject of the contract is quoted verbatim below.")


def _mech_connective(contract_type="murabaha"):
    if contract_type == "ijara":
        return ("العقدُ إجارةٌ؛ وفيما يلي الوقائعُ المُستخلَصةُ من العقد نصّاً (العينُ المؤجَّرة، الأجرةُ والمدّة، تبعةُ الملكية، التسليمُ، أداةُ التمليك).",
                "The aqd is an Ijara; below are the facts extracted verbatim from the contract "
                "(the leased asset, rent and term, ownership-risk allocation, delivery, transfer instrument).")
    return ("العقدُ مرابحةٌ للآمر بالشراء؛ وفيما يلي تسلسلُ الوقائع المُستخلَصةُ من العقد نصّاً (تملّكٌ وقبضٌ، وكالةٌ، ثمنٌ وإفصاح).",
            "The aqd is a Murabaha to the Purchase Orderer; below is the sequence extracted verbatim from the contract "
            "(ownership/possession, agency, price and disclosure).")


def _mech_attributed(structure, contract_type="murabaha"):
    ar, en = [], []
    if contract_type == "ijara":
        ij = structure.get("ijara", {})
        pairs = [("العينُ والأجرة", "Asset and rent", structure["asset"].get("quote") or ij.get("rent_quote")),
                 ("تبعةُ الملكية", "Ownership-risk allocation", ij.get("lessor_risk_quote") or ij.get("risk_shift_quote")),
                 ("توقيتُ الأجرة", "Rent timing", ij.get("rent_timing_quote")),
                 ("أداةُ التمليك (الإجارة المنتهية بالتمليك)", "Transfer instrument (IMB)", ij.get("transfer_quote"))]
        for lab_ar, lab_en, q in pairs:
            if q:
                ar.append(f"- {lab_ar}: «{q}»")
                en.append(f"- {lab_en}: «{q}»")
        return "\n".join(ar), "\n".join(en)
    o = structure["ownership"]
    if o.get("acquire_quote"):
        ar.append(f"- تسلسلُ التملّك والقبض: «{o['acquire_quote']}»")
        en.append(f"- Ownership/possession: «{o['acquire_quote']}»")
    if structure["agency"].get("quote"):
        ar.append(f"- ترتيبُ الوكالة: «{structure['agency']['quote']}»")
        en.append(f"- Agency: «{structure['agency']['quote']}»")
    if structure["price_terms"].get("cost_quote"):
        ar.append(f"- الثمنُ والإفصاح: «{structure['price_terms']['cost_quote']}»")
        en.append(f"- Price/disclosure: «{structure['price_terms']['cost_quote']}»")
    return "\n".join(ar), "\n".join(en)


def generate(structure, findings, rules, defer, glossary, seam=None, authoritative_lang="ar", contract_file="", contract_type="murabaha"):
    opinion = OpinionField()
    generated_prose = []

    # ---- connective prose (gated) ----
    desc_ar, desc_en = _desc_connective(structure, contract_type)
    model_used = False
    if seam is not None and seam.available():
        out = seam.interpret("Draft a neutral bilingual description (keys ar,en) of this contract DATA; "
                             "describe only; assert no permissibility.", authoritative_lang)
        if isinstance(out, dict) and out.get("ar"):
            desc_ar, desc_en, model_used = out["ar"], out.get("en", desc_en), True
        elif isinstance(out, str) and out:
            desc_ar, model_used = out, True
    mech_ar, mech_en = _mech_connective(contract_type)
    issues_intro = ("المسائلُ المثارةُ قاعدةً بقاعدة (تحديدٌ لا حكم):",
                    "Issues identified rule by rule (identification, not a ruling):")
    evidence_intro = ("الأدلةُ والمراجعُ بطبقاتها (L1 تعليمات بنك الكويت المركزي/الهيئة العليا · L2 فتاوى الهيئة الشرعية للمصرف [اصطناعية في هذا العرض] · L3 معايير AAOIFI · LJ القضاء الكويتي):",
                      "References by layer (L1 CBK/Higher Committee · L2 the bank's SSB fatwas [SYNTHETIC in this demo] · L3 AAOIFI · LJ Kuwaiti judicial practice):")
    conditions = ("لا يجوز الاعتمادُ على هذه المذكّرة بوصفها فتوى. النصُّ الكامل لمعايير AAOIFI محميٌّ بحقوق النشر؛ يُشار إليه بالرقم والمبدأ المنشور فقط، ويلزم التحقّقُ على مستوى البنود من النصوص المُشتراة قبل أيِّ استعمالٍ واقعي. وطبقةُ L2 في هذا العرض اصطناعيةٌ وليست فتوى حقيقية.",
                  "This memo may not be relied upon as a fatwa. The full AAOIFI Standards text is copyrighted; it is referenced by number and published principle only, and clause-level verification against the purchased texts is required before any real-world use. The L2 layer in this demo is SYNTHETIC, not a real fatwa.")
    implementation = ("يخضع المنتجُ لمراجعة الهيئة الشرعية واعتمادها قبل الطرح؛ ويختبر التدقيقُ الشرعيُّ الخارجيُّ كلَّ نوعٍ من المعاملات؛ وتُتابَع البنودُ المُشار إليها حتى المعالجة والإقفال.",
                      "The product is subject to SSB review and approval before launch; the external Sharia audit tests each transaction type; the flagged clauses are tracked to remediation and closure.")
    deferrals_intro = ("تُعرَض المسألةُ الخلافيةُ بمواقفها ولا يَبتُّ فيها النظام:",
                       "The contested matter is presented with its positions; the system does not resolve it:")
    generated_prose += [desc_ar, desc_en, mech_ar, mech_en, issues_intro[0], issues_intro[1],
                        evidence_intro[0], evidence_intro[1], conditions[0], conditions[1],
                        implementation[0], implementation[1], deferrals_intro[0], deferrals_intro[1]]

    # ---- attributed content (exempt: verbatim quotes / citations / positions / placeholder) ----
    asset_q = structure["asset"]["quote"] or "—"
    desc_att = (f"محلُّ العقد (نصّاً): «{asset_q}»", f"Subject of the contract (verbatim): «{asset_q}»")
    mech_att = _mech_attributed(structure, contract_type)

    issue_lines_ar, issue_lines_en = [], []
    for f in findings:
        rid = f.get("rule_id") or "—"
        issue_lines_ar.append(f"- {rid} ({f.get('rule_title_ar','')}): {_STATUS_AR.get(f['status'], f['status'])}."
                              + (f" نصُّ البند: «{f['quote']}»" if f.get("quote") else "")
                              + (f" الواقعةُ الناقصة: {f['missing_fact']}." if f.get("missing_fact") else ""))
        issue_lines_en.append(f"- {rid} ({f.get('rule_title_en','')}): {_STATUS_EN.get(f['status'], f['status'])}."
                              + (f" Clause: «{f['quote']}»" if f.get("quote") else "")
                              + (f" Missing fact: {f['missing_fact']}." if f.get("missing_fact") else ""))
    issues_att = ("\n".join(issue_lines_ar), "\n".join(issue_lines_en))

    ev_ar, ev_en = [], []
    for f in findings:
        cits = [f"[{c['layer']}] {c['ref']}" for c in f.get("citations", [])]
        if cits:
            ev_ar.append(f"- {f.get('rule_id') or '—'}: " + " · ".join(cits))
            ev_en.append(f"- {f.get('rule_id') or '—'}: " + " · ".join(cits))
    evidence_att = ("\n".join(ev_ar), "\n".join(ev_en))

    d_findings = [f for f in findings if f["status"] == "deferral"]
    if d_findings:
        ba, be = [], []
        for f in d_findings:
            rid = f.get("rule_id") or "—"
            pa = "\n".join(f"    • {p['authority']}: {p['position_ar']} [{p['citation']}]" for p in (f.get("positions") or []))
            pe = "\n".join(f"    • {p['authority']}: {p['position_en']} [{p['citation']}]" for p in (f.get("positions") or []))
            ba.append(f"  {rid} — {f.get('rule_title_ar','')}\n  السؤال: {f.get('rule_title_ar','')}\n  المواقفُ المنسوبةُ إلى مصادرها:\n{pa}\n  التوجيه: {f.get('routing_ar','')}")
            be.append(f"  {rid} — {f.get('rule_title_en','')}\n  Question: {f.get('rule_title_en','')}\n  Positions attributed to source:\n{pe}\n  Routing: {f.get('routing_en','')}")
        deferrals_att = ("\n\n".join(ba), "\n\n".join(be))
    else:
        deferrals_att = ("لا توجد مسائلُ خلافيةٌ في هذا العقد.", "No contested matters in this contract.")

    signoff_att = ("عضو الهيئة الشرعية (الاسم): ____________________   التوقيع: ____________   التاريخ: __________\n"
                   "عضو الهيئة الشرعية (الاسم): ____________________   التوقيع: ____________   التاريخ: __________",
                   "SSB member (name): ____________________   Signature: ____________   Date: __________\n"
                   "SSB member (name): ____________________   Signature: ____________   Date: __________")

    sections = [
        {"key": "description", "heading_ar": "وصف المنتج والمعاملة", "heading_en": "Product and transaction description",
         "connective_ar": desc_ar, "connective_en": desc_en, "attributed_ar": desc_att[0], "attributed_en": desc_att[1]},
        {"key": "mechanics", "heading_ar": "هيكل العقد وآليّته (العقد وتسلسل نقل الملكية)", "heading_en": "Contract structure and mechanics (the aqd and the ownership-transfer sequence)",
         "connective_ar": mech_ar, "connective_en": mech_en, "attributed_ar": mech_att[0], "attributed_en": mech_att[1]},
        {"key": "issues", "heading_ar": "المسائل الشرعية المثارة", "heading_en": "Shariah issues identified",
         "connective_ar": issues_intro[0], "connective_en": issues_intro[1], "attributed_ar": issues_att[0], "attributed_en": issues_att[1]},
        {"key": "evidence", "heading_ar": "الأدلة والمراجع المُستشهَد بها", "heading_en": "Evidence and references cited",
         "connective_ar": evidence_intro[0], "connective_en": evidence_intro[1], "attributed_ar": evidence_att[0], "attributed_en": evidence_att[1]},
        {"key": "opinion", "heading_ar": "الرأي/الحكم الشرعي", "heading_en": "Sharia opinion/ruling",
         "connective_ar": "", "connective_en": "", "attributed_ar": opinion.render_ar(), "attributed_en": opinion.render_en()},
        {"key": "conditions", "heading_ar": "الشروط والملاحظات", "heading_en": "Conditions and caveats",
         "connective_ar": conditions[0], "connective_en": conditions[1], "attributed_ar": "", "attributed_en": ""},
        {"key": "implementation", "heading_ar": "متطلبات التنفيذ والمتابعة", "heading_en": "Implementation and monitoring requirements",
         "connective_ar": implementation[0], "connective_en": implementation[1], "attributed_ar": "", "attributed_en": ""},
        {"key": "deferrals", "heading_ar": "المسائل الخلافية المُحالة إلى الهيئة الشرعية", "heading_en": "Contested matters referred to the SSB",
         "connective_ar": deferrals_intro[0], "connective_en": deferrals_intro[1], "attributed_ar": deferrals_att[0], "attributed_en": deferrals_att[1]},
        {"key": "signoff", "heading_ar": "اعتماد الهيئة الشرعية", "heading_en": "SSB sign-off",
         "connective_ar": "", "connective_en": "", "attributed_ar": signoff_att[0], "attributed_en": signoff_att[1]},
    ]

    memo = {
        "contract_file": contract_file,
        "authoritative_language": authoritative_lang,
        "watermark": {"ar": WATERMARK_AR, "en": WATERMARK_EN},
        "sections": sections,
        "opinion_is_placeholder": True,
        "opinion_placeholder_ar": OpinionField.PLACEHOLDER_AR,
        "model_used": model_used,
        "generated_prose": [p for p in generated_prose if p],
    }
    memo["render_md"] = render(memo)
    return memo


def render(memo):
    auth = memo["authoritative_language"]
    wm = f"> **{memo['watermark']['ar']}**\n> **{memo['watermark']['en']}**\n"
    out = ["# مذكّرة المراجعة الشرعية — Sharia-Review Memo\n",
           f"_ملف العقد / contract: {memo['contract_file']} · اللغة المعتمدة / authoritative language: {auth} (Arabic-first)_\n",
           wm, "\n---\n"]
    for i, s in enumerate(memo["sections"], 1):
        out.append(f"\n## {i}. {s['heading_ar']} — {s['heading_en']}\n")
        ar = (s["connective_ar"] + ("\n\n" + s["attributed_ar"] if s["attributed_ar"] else "")).strip()
        en = (s["connective_en"] + ("\n\n" + s["attributed_en"] if s["attributed_en"] else "")).strip()
        out.append(f"\n**[ع]**\n\n{ar}\n")
        out.append(f"\n**[EN]**\n\n{en}\n")
        out.append(f"\n{wm}")
    out.append("\n---\n")
    out.append(wm)
    return "".join(out)
