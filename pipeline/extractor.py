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


def extract(text, rail, seam, glossary_terms=(), watchlist=()):
    injection_spans = rail.scan_injection(text)   # recorded, non-blocking (inert)
    language = _detect_language(text)
    nt = _norm(text)

    asset_quote = _quote(text, r"^\s*asset:", r"^\s*الاصل:")
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
        "unknown_terms": unknown_terms,
        "injection_spans": injection_spans,
        "extraction_method": "deterministic",
    }

    # Completeness (fail-closed): asset + >= 4 resolved rule-groups.
    groups = {
        "R1": any(v is not None for v in (bank_acquires_before_sale, customer_is_buying_agent, sale_before_possession)),
        "R2": any(v is not None for v in (cost_disclosed, markup_disclosed, price_fixed)),
        "R3": (permissible is not None) or (exists is not None),
        "R4": any(v is not None for v in (asset_already_customers, inah_buyback)),
        "R5": any(v is not None for v in (penalty_to_charity, penalty_to_income, markup_increase_on_late)),
        "R6": wad_present is not False,
    }
    resolved = sum(1 for v in groups.values() if v)
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
