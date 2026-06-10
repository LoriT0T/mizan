"""Concern: a Murabaha contract document (ar / en / mixed, plain text) ->
a structured ContractStructure.

Deterministic-first: bilingual cue detection with Arabic NORMALISATION (strip
tashkīl/tatweel, fold alef/ya/ta-marbuta) and NEGATION awareness (a clean
"is not owned by the customer" / "لا تُعَدّ إيراداً" yields False, not a false
positive). Arabic is read natively and quoted VERBATIM (the raw line) into the
fields — detection runs on a normalised copy, quotes come from the original.

The model seam (injected) is reserved for genuinely messy interpretation and is
consulted only when the deterministic pass is incomplete AND a key is present;
in NO-KEY mode the result fails closed to "requires human review".

Dependency-injected (`rail`, `seam`, `glossary_terms`, `watchlist`) — imports no
sibling. Entry point:
  `extract(text, rail, seam, glossary_terms=(), watchlist=()) -> dict`
"""
import re

INCOMPLETE_MSG = "extraction incomplete — requires human review"

_DIAC = re.compile(r"[ً-ْٰـ]")  # tashkīl + superscript alef + tatweel


def _norm(s):
    s = _DIAC.sub("", s)
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ٱ", "ا"),
                 ("ى", "ي"), ("ة", "ه"), ("ؤ", "و"), ("ئ", "ي")):
        s = s.replace(a, b)
    return s.lower()


def _detect_language(text):
    arabic = len(re.findall(r"[؀-ۿ]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    if arabic and latin > arabic * 0.5:
        return "mixed"
    return "ar" if arabic else "en"


def _quote(raw_text, *patterns):
    """First VERBATIM line whose normalised form matches any (normalised) pattern."""
    for line in raw_text.splitlines():
        n = _norm(line)
        for p in patterns:
            if re.search(p, n):
                return line.strip()
    return ""


def _decide(norm_text, raw_text, neg, pos):
    """Negation-aware boolean: explicit-negative FIRST, then positive.
    Returns (value|None, verbatim_quote)."""
    if neg and re.search(neg, norm_text):
        return False, _quote(raw_text, neg)
    if pos and re.search(pos, norm_text):
        return True, _quote(raw_text, pos)
    return None, ""


def _ijara_facts(nt, text):
    """Ijara-specific facts (I1–I7), negation-aware; quotes verbatim from raw text."""
    asset_consumable, _ = _decide(nt, text, neg=r"غير قابل للاستهلاك|non-consumable",
                                  pos=r"قابل للاستهلاك|يستهلك بالاستعمال|\bconsumable\b")
    permissible_use, pu_q = _decide(nt, text,
        neg=r"مباح الاستعمال|permissible use|استعمال مباح",
        pos=r"لمنفعه محرمه|impermissible use|riba-based|ربويه|لتخزين .{0,12}محرم")  # pos here = the VIOLATION
    rent_defined, rent_q = _decide(nt, text, neg=r"اجره غير محدده|undefined rent",
        pos=r"الاجره .{0,14}محدده|اجره .{0,8}قدرها|اجره سنويه قدرها|rent .{0,14}defined|annual rent of|rent of kwd")
    term_defined, term_q = _decide(nt, text, neg=r"مده غير محدده|undefined term",
        pos=r"مده الاجاره .{0,14}محدده|لمده .{0,10}سنه|lease term .{0,14}defined|term of .{0,8}years|for a term of")
    unilateral_increase, ui_q = _decide(nt, text,
        neg=r"لا .{0,12}زياده الاجره انفرادا|may not .{0,12}unilaterally|لا يجوز .{0,16}زياده الاجره انفرادا",
        pos=r"زياده الاجره انفرادا|رفع الاجره انفرادا|unilaterally .{0,12}(raise|increase) the rent|raise the rent unilaterally")
    lease_before_acq, lba_q = _decide(nt, text, neg=None,
        pos=r"الاجاره قبل .{0,12}تملك|leased before .{0,12}acqui|lease .{0,16}before the bank acquires")
    lessor_owns_before, low_q = _decide(nt, text, neg=None,
        pos=r"يملك الموجر العين .{0,24}قبل الاجاره|الموجر .{0,16}قبل الاجاره|owns the asset .{0,24}before .{0,10}leas|acquires the asset before leasing")

    # I4 — the headline test
    risk_shifted = None
    rs_q = ""
    if re.search(r"المستاجر .{0,28}الصيانه الاساسيه|lessee .{0,24}(basic|major|structural) maintenance|"
                 r"المستاجر .{0,24}(التكافل|التامين)|lessee .{0,24}(insurance|takaful)|"
                 r"المستاجر .{0,28}(الهلاك|التلف) الكلي|lessee .{0,24}total[- ]loss|"
                 r"تستمر الاجره .{0,20}الهلاك|rent .{0,16}continues? .{0,16}destr", nt):
        risk_shifted = True
        rs_q = _quote(text, r"المستاجر|lessee")
    lessor_bears_risk, lbr_q = _decide(nt, text, neg=None,
        pos=r"الموجر .{0,24}الصيانه الاساسيه|lessor bears .{0,24}(basic|major|structural) maintenance|"
            r"التكافل .{0,12}على الموجر|takaful at the lessor|الموجر .{0,16}تبعه (الهلاك|التلف)")
    if risk_shifted:
        lessor_bears_risk = False if lessor_bears_risk is None else lessor_bears_risk

    rent_before_delivery, rbd_q = _decide(nt, text,
        neg=r"الاجره .{0,20}بعد .{0,4}تسليم|rent .{0,16}after .{0,10}deliver|accrues from .{0,12}delivery|only after delivery",
        pos=r"الاجره .{0,28}قبل .{0,4}تسليم|تستحق الاجره من تاريخ (توقيع|العقد|دفع)|rent .{0,24}before delivery|rent accrues from the .{0,16}(contract|signing|payment) date")

    is_imb, _ = _decide(nt, text, neg=None,
        pos=r"المنتهيه بالتمليك|lease-to-own|ijara muntahia|نقل الملكيه|ينتقل الملك|ownership transfer|transfer of ownership")
    # Fusion (the violation) is checked FIRST so a phrase like "no separate
    # transfer instrument" reads as fusion, not as separation.
    _fuse_pos = (r"دمج البيع والاجاره|انتقال تلقائي للملكيه|"
                 r"sale and lease are bound into (one|a single|the same) contract|"
                 r"sale and lease .{0,16}(bound|fused|combined)|automatic .{0,14}(title|ownership) transfer|"
                 r"fused into the lease|no separate transfer")
    _sep_pos = (r"وعد مستقل|اداه مستقله|باداه مستقله|بيع منفصل|"
                r"separate (promise|instrument|sale)|separate from the lease|independent instrument")
    if re.search(_fuse_pos, nt):
        transfer_fused, tf_q = True, _quote(text, _fuse_pos)
    elif re.search(_sep_pos, nt):
        transfer_fused, tf_q = False, _quote(text, _sep_pos)
    else:
        transfer_fused, tf_q = None, ""

    sale_leaseback, _ = _decide(nt, text, neg=None,
        pos=r"بيع .{0,12}ثم .{0,12}استئجار|البيع مع الاستئجار|sale-?and-?leaseback|sells .{0,16}then leases? .{0,6}back")
    sl_interval, sli_q = _decide(nt, text,
        neg=r"في ان واحد|دون فاصل|simultaneous|instantly|no interval|same time",
        pos=r"فاصل زمني|مده معتبره|بعد مده|reasonable interval")

    return {
        "asset_consumable": asset_consumable,
        "permissible_use_violation": permissible_use, "use_quote": pu_q,
        "rent_defined": rent_defined, "rent_quote": rent_q,
        "term_defined": term_defined, "term_quote": term_q,
        "unilateral_increase": unilateral_increase, "increase_quote": ui_q,
        "lessor_owns_before_lease": lessor_owns_before, "owns_quote": low_q,
        "lease_before_acquisition": lease_before_acq, "lba_quote": lba_q,
        "risk_shifted_to_lessee": risk_shifted, "risk_shift_quote": rs_q,
        "lessor_bears_ownership_risk": lessor_bears_risk, "lessor_risk_quote": lbr_q,
        "rent_before_delivery": rent_before_delivery, "rent_timing_quote": rbd_q,
        "is_imb": is_imb,
        "transfer_fused": transfer_fused, "transfer_quote": tf_q,
        "sale_leaseback": sale_leaseback, "sale_leaseback_interval": sl_interval, "sl_quote": sli_q,
    }


def extract(text, rail, seam, glossary_terms=(), watchlist=()):
    injection_spans = rail.scan_injection(text)   # recorded, non-blocking (inert)
    language = _detect_language(text)
    nt = _norm(text)

    asset_quote = _quote(text, r"^\s*asset:", r"^\s*الاصل:", r"^\s*العين", r"^\s*leased asset:")
    asset_present = bool(asset_quote)

    # R3 — permissibility / existence
    permissible, perm_q = _decide(
        nt, text,
        neg=r"alcohol|wine|liquor|pork|brewery|interest-based|خمر|خنزير|مسكر|ربوي",
        pos=r"permissible asset|اصل مباح|مباح شرع")
    exists_neg = re.search(r"no underlying asset|general liquidity|for cash needs|salaries|utility bills|does not exist|لا يوجد اصل|سيوله|حاجه نقديه|رواتب|فواتير", nt)
    if exists_neg:
        exists, exists_q = False, _quote(text, r"no underlying asset|general liquidity|for cash needs|salaries|utility bills|does not exist|لا يوجد اصل|سيوله|حاجه نقديه|رواتب|فواتير")
    else:
        exists, exists_q = (True, asset_quote) if asset_present else (None, "")

    # R1 — ownership / possession vs agency / sale-before-possession
    bank_acquires_before_sale, acq_q = _decide(
        nt, text,
        neg=r"لا يقبض|does not take possession|never takes possession",
        pos=r"يقبضه|قبضا حقيقيا|قبل بيعه|takes ownership and possession|bearing all risks of ownership|before any sale")
    bears_risk, risk_q = _decide(
        nt, text,
        neg=r"لا يتحمل المصرف مخاطر|never bears ownership risk|does not bear",
        pos=r"يتحمل مخاطر الملكيه|تبعه الهلاك|bearing all risks of ownership")
    customer_is_buying_agent, agent_q = _decide(
        nt, text, neg=None,
        pos=r"نيابه عن العميل|وكيلا? بالشراء|buying agent|on the customer's behalf|pays the supplier on behalf")
    sale_before_possession, sbp_q = _decide(
        nt, text, neg=None,
        pos=r"بيع قبل القبض|before taking possession|before the bank takes title")

    # R2 — disclosure + price fixity
    cost_disclosed, cost_q = _decide(
        nt, text,
        neg=r"cost .{0,12}not disclosed|not disclosed to the customer|only the total price|دون الافصاح عن التكلفه",
        pos=r"تكلفه مفصح|تكلفه عنها قدرها|disclosed cost|cost of kwd")
    markup_disclosed, mk_q = _decide(
        nt, text,
        neg=r"markup .{0,12}not disclosed|profit .{0,12}not disclosed|not disclosed to the customer|دون الافصاح عن .{0,6}الربح",
        pos=r"هامش ربح مفصح|هامش ربح .{0,6}قدره|disclosed profit markup|profit markup of")
    price_fixed, pf_q = _decide(
        nt, text,
        neg=r"re-?priced|markup increases after|اعاده تسعير",
        pos=r"مثبت عند العقد|لا يتغير بعد|fixed at contract|does not change after")

    # R5 — late-payment treatment
    penalty_to_charity, char_q = _decide(
        nt, text, neg=None,
        pos=r"وجوه الخير|donated to charity|to charity|جهه خيريه|صدقه")
    penalty_to_income, inc_q = _decide(
        nt, text,
        neg=r"لا تعد ايراد|shall not be taken as income|not be taken as income",
        pos=r"retained as income|taken as income|as income of the bank|ايرادا? للمصرف|ايراد المصرف|دخل المصرف")
    markup_increase_on_late, mkl_q = _decide(
        nt, text,
        neg=r"shall not increase|does not increase|not be increased|لا يزاد|لا تزاد",
        pos=r"markup .{0,20}increase|increase .{0,15}on late|يزاد .{0,8}الربح")

    # R6 — promise (wa'd) structure
    wad_present = bool(re.search(r"\bpromise\b|wa'?d|وعد", nt))
    bilateral_neg = bool(re.search(r"no bilateral binding|no .{0,12}binding promise|لا يوجد.{0,20}ملزم", nt))
    bilateral_pos = re.search(r"ثنائي ملزم|ملزم للطرفين|يلتزم الطرفان|bilateral binding|mutually bound|both parties are bound", nt)
    unilateral_pos = re.search(r"احادي|من طرف واحد|unilateral|one-?sided", nt)
    binding_token = bool(re.search(r"ملزم|binding|bound", nt))
    wad_type, wad_q, binding_language = None, "", None
    if bilateral_pos and not bilateral_neg:
        wad_type = "bilateral"
        binding_language = True
        wad_q = _quote(text, r"ثنائي ملزم|ملزم للطرفين|يلتزم الطرفان|bilateral binding|mutually bound|both parties are bound")
    elif unilateral_pos:
        wad_type = "unilateral"
        binding_language = binding_token and not bilateral_neg
        wad_q = _quote(text, r"احادي|من طرف واحد|unilateral|one-?sided")
    elif wad_present:
        binding_language = binding_token and not bilateral_neg
        wad_q = _quote(text, r"\bpromise\b|wa'?d|وعد")

    # R4 — prior customer ownership / bai' al-inah
    asset_already_customers, own_q = _decide(
        nt, text,
        neg=r"not owned by the customer|ليس مملوك للعميل|ليس مملوكا للعميل",
        pos=r"owned by the customer prior|was owned by the customer|كان مملوك للعميل|كان مملوكا للعميل")
    inah_buyback, inah_q = _decide(
        nt, text,
        neg=r"not bought back|is not bought back|لا يعاد شراوه",
        pos=r"buys the asset from the customer|bought back from the customer|يشتري المصرف.{0,8}الاصل.{0,8}من العميل|اشتراه المصرف.{0,8}من العميل|اعاده? بيعه|بيع العينه|العينه")
    inah_boundary_ambiguous = False  # set True only for genuinely borderline structures (none in this corpus)

    # Unknown terms of art -> glossary growth protocol trigger
    g_norm = {_norm(t) for t in glossary_terms}
    unknown_terms = []
    for term in watchlist:
        if _norm(term) in nt and not any(_norm(term) in g or g in _norm(term) for g in g_norm if g):
            unknown_terms.append(term)

    structure = {
        "language": language,
        "asset": {"present": asset_present, "quote": asset_quote,
                  "permissible": permissible, "permissible_quote": perm_q,
                  "exists": exists, "exists_quote": exists_q},
        "ownership": {"bank_acquires_before_sale": bank_acquires_before_sale, "acquire_quote": acq_q,
                      "bank_bears_ownership_risk": bears_risk, "risk_quote": risk_q,
                      "sale_before_possession": sale_before_possession, "sale_before_quote": sbp_q},
        "agency": {"customer_is_buying_agent": customer_is_buying_agent, "quote": agent_q},
        "price_terms": {"cost_disclosed": cost_disclosed, "cost_quote": cost_q,
                        "markup_disclosed": markup_disclosed, "markup_quote": mk_q,
                        "price_fixed_at_contract": price_fixed, "fixed_quote": pf_q},
        "late_payment": {"penalty_to_charity": penalty_to_charity, "charity_quote": char_q,
                         "penalty_to_income": penalty_to_income, "income_quote": inc_q,
                         "markup_increase_on_late": markup_increase_on_late, "increase_quote": mkl_q,
                         "penalty_destination": ("bank_income" if penalty_to_income else
                                                 "charity" if penalty_to_charity else None)},
        "wad_promise": {"present": wad_present, "type": wad_type, "binding_language": binding_language, "quote": wad_q},
        "prior_ownership": {"asset_already_customers": asset_already_customers, "owned_quote": own_q,
                            "inah_buyback": inah_buyback, "inah_quote": inah_q,
                            "inah_boundary_ambiguous": inah_boundary_ambiguous},
        "ijara": _ijara_facts(nt, text),
        "unknown_terms": unknown_terms,
        "injection_spans": injection_spans,
        "extraction_method": "deterministic",
    }

    # Completeness (fail-closed): asset + >= 4 resolved groups of EITHER type.
    groups = {
        "R1": any(v is not None for v in (bank_acquires_before_sale, customer_is_buying_agent, sale_before_possession)),
        "R2": any(v is not None for v in (cost_disclosed, markup_disclosed, price_fixed)),
        "R3": (permissible is not None) or (exists is not None),
        "R4": any(v is not None for v in (asset_already_customers, inah_buyback)),
        "R5": any(v is not None for v in (penalty_to_charity, penalty_to_income, markup_increase_on_late)),
        "R6": wad_present is not False,
    }
    ij = structure["ijara"]
    ijara_groups = {
        "I1": any(v is not None for v in (ij["asset_consumable"], ij["permissible_use_violation"])) or asset_present,
        "I2": any(v is not None for v in (ij["rent_defined"], ij["term_defined"], ij["unilateral_increase"])),
        "I3": any(v is not None for v in (ij["lessor_owns_before_lease"], ij["lease_before_acquisition"])),
        "I4": any(v is not None for v in (ij["risk_shifted_to_lessee"], ij["lessor_bears_ownership_risk"])),
        "I5": ij["rent_before_delivery"] is not None,
        "I6": any(v is not None for v in (ij["is_imb"], ij["transfer_fused"])),
        "I7": any(v is not None for v in (ij["sale_leaseback"], ij["sale_leaseback_interval"])),
    }
    murabaha_resolved = sum(1 for v in groups.values() if v)
    ijara_resolved = sum(1 for v in ijara_groups.values() if v)
    resolved = max(murabaha_resolved, ijara_resolved)
    complete = asset_present and resolved >= 4

    # Model seam reserved for messy input: only if incomplete AND a key is present.
    if not complete and seam is not None and seam.available():
        filled = seam.interpret(rail.wrap_as_data(text), language)
        if isinstance(filled, dict):
            structure["extraction_method"] = "deterministic+model"
            structure["model_fields"] = filled
            complete = bool(filled.get("complete"))

    structure["extraction_complete"] = bool(complete)
    if not complete:
        structure["status"] = INCOMPLETE_MSG
        structure["unresolved"] = [g for g, ok in groups.items() if not ok] or (["asset"] if not asset_present else [])
    return structure
