"""Concern: ContractStructure x locked registry -> FINDINGS. Deterministic. No model.

Each finding: rule id · the implicated contract element + VERBATIM quote (Arabic
preserved) · status in {satisfied, violated, indeterminate, deferral} · the
registry citations WITH layer labels (L1/L2/L3/LJ) · for violations, the
registry violation-pattern matched · for deferrals, the defer-register positions
+ routing · for indeterminate, the named missing fact.

Discipline (enforced by `never_rules_guard`, run on this output by the
orchestrator): findings FLAG/IDENTIFY/CITE — never rule. Contested matters
(R6, and any structure flagged as touching D1–D3) emit a DEFERRAL only; they are
never marked satisfied or violated. The checker NEVER mutates the registry.

Stdlib only. No sibling imports. Entry point:
  `check(structure, rules_data, defer_data) -> list[finding]`
"""

NOT_A_RULING = "Flagged for the qualified scholar (SSB); this is an identification, not a ruling."


def _rule(rules_data, rid):
    for r in rules_data["rules"]:
        if r["id"] == rid:
            return r
    raise KeyError(rid)


def _citations(rule):
    return [{"layer": s["layer"], "ref": s["ref"]} for s in rule["sources"]]


def _defer(defer_data, did):
    for e in defer_data["entries"]:
        if e["id"] == did:
            return e
    raise KeyError(did)


def _base(rule):
    return {
        "rule_id": rule["id"],
        "rule_title_ar": rule["title_ar"],
        "rule_title_en": rule["title_en"],
        "citations": _citations(rule),
        "violation_pattern": None,
        "positions": None,
        "routing_en": None,
        "routing_ar": None,
        "missing_fact": None,
    }


def _deferral(rule, defer_data, element, quote, note):
    e = _defer(defer_data, rule["defer_ref"])
    f = _base(rule)
    f.update({
        "status": "deferral",
        "contract_element": element,
        "quote": quote,
        "positions": [{"authority": p["authority"], "position_ar": p["position_ar"],
                       "position_en": p["position_en"], "citation": p["citation"]} for p in e["positions"]],
        "routing_en": e["routing_en"],
        "routing_ar": e["routing_ar"],
        "note": note,
    })
    return f


def _r1(s, rule, _defer_data):
    o, ag = s["ownership"], s["agency"]
    f = _base(rule)
    if ag["customer_is_buying_agent"] is True:
        f.update({"status": "violated", "contract_element": "agency / ownership-risk",
                  "quote": ag["quote"], "violation_pattern": rule["violated_by"][0],
                  "note": "Customer acts as buying agent; the bank does not take possession or bear ownership risk before resale. " + NOT_A_RULING})
    elif o["sale_before_possession"] is True:
        f.update({"status": "violated", "contract_element": "ownership sequence",
                  "quote": o["sale_before_quote"], "violation_pattern": rule["violated_by"][1],
                  "note": "Sale executed before the bank takes title/possession. " + NOT_A_RULING})
    elif o["bank_acquires_before_sale"] is True:
        f.update({"status": "satisfied", "contract_element": "ownership sequence",
                  "quote": o["acquire_quote"],
                  "note": "The bank takes ownership and possession (bearing risk) before resale. " + NOT_A_RULING})
    else:
        f.update({"status": "indeterminate", "contract_element": "ownership sequence", "quote": "",
                  "missing_fact": "whether the bank takes ownership and possession, bearing risk, before resale",
                  "note": "Could not establish the ownership/possession sequence. " + NOT_A_RULING})
    return f


def _r2(s, rule, _defer_data):
    p = s["price_terms"]
    f = _base(rule)
    if p["cost_disclosed"] is False or p["markup_disclosed"] is False:
        q = p["cost_quote"] or p["markup_quote"]
        f.update({"status": "violated", "contract_element": "price terms / disclosure",
                  "quote": q, "violation_pattern": rule["violated_by"][0],
                  "note": "Cost and/or markup not disclosed; resembles musawamah, not Murabaha. " + NOT_A_RULING})
    elif p["price_fixed_at_contract"] is False:
        f.update({"status": "violated", "contract_element": "price terms / fixity",
                  "quote": p["fixed_quote"], "violation_pattern": rule["violated_by"][1],
                  "note": "Price/markup not fixed at contract (re-priced later). " + NOT_A_RULING})
    elif p["cost_disclosed"] is True and p["markup_disclosed"] is True:
        f.update({"status": "satisfied", "contract_element": "price terms",
                  "quote": p["cost_quote"] or p["markup_quote"],
                  "note": "Cost and markup disclosed; price fixed at contract. " + NOT_A_RULING})
    else:
        f.update({"status": "indeterminate", "contract_element": "price terms", "quote": "",
                  "missing_fact": "cost disclosure, markup disclosure, and price fixity",
                  "note": "Could not establish disclosure/price terms. " + NOT_A_RULING})
    return f


def _r3(s, rule, _defer_data):
    a = s["asset"]
    f = _base(rule)
    if a["permissible"] is False:
        f.update({"status": "violated", "contract_element": "asset / permissibility",
                  "quote": a["permissible_quote"], "violation_pattern": rule["violated_by"][0],
                  "note": "Asset is of a prohibited kind. " + NOT_A_RULING})
    elif a["exists"] is False:
        f.update({"status": "violated", "contract_element": "asset / existence",
                  "quote": a["exists_quote"], "violation_pattern": rule["violated_by"][1],
                  "note": "No real underlying asset (pure-cash use). " + NOT_A_RULING})
    elif a["permissible"] is True:
        f.update({"status": "satisfied", "contract_element": "asset",
                  "quote": a["quote"],
                  "note": "Asset is specified and existing; no prohibited-category cue (e.g. alcohol/pork/riba) was found. " + NOT_A_RULING})
    else:
        f.update({"status": "indeterminate", "contract_element": "asset", "quote": "",
                  "missing_fact": "asset existence and permissibility",
                  "note": "Could not establish the asset's existence/permissibility. " + NOT_A_RULING})
    return f


def _r4(s, rule, defer_data):
    po = s["prior_ownership"]
    if po["inah_boundary_ambiguous"] is True:
        return _deferral(rule, defer_data, "prior ownership / inah boundary", po["inah_quote"] or po["owned_quote"],
                         "The structure is near the bai' al-inah boundary; routed to the SSB. " + NOT_A_RULING)
    f = _base(rule)
    if po["asset_already_customers"] is True or po["inah_buyback"] is True:
        f.update({"status": "violated", "contract_element": "prior ownership / bai' al-inah",
                  "quote": po["inah_quote"] or po["owned_quote"], "violation_pattern": rule["violated_by"][0],
                  "note": "Asset bought from then resold to the same customer (bai' al-inah pattern). " + NOT_A_RULING})
    elif po["asset_already_customers"] is False:
        f.update({"status": "satisfied", "contract_element": "prior ownership",
                  "quote": po["owned_quote"],
                  "note": "Asset sourced from a third party, not the customer; no buy-back. " + NOT_A_RULING})
    else:
        f.update({"status": "indeterminate", "contract_element": "prior ownership", "quote": "",
                  "missing_fact": "whether the asset was the customer's / is bought back from the customer",
                  "note": "Could not establish the asset's prior ownership. " + NOT_A_RULING})
    return f


def _r5(s, rule, _defer_data):
    lp = s["late_payment"]
    f = _base(rule)
    if lp["penalty_to_income"] is True:
        f.update({"status": "violated", "contract_element": "late-payment clause",
                  "quote": lp["income_quote"], "violation_pattern": rule["violated_by"][1],
                  "note": "Late-payment penalty retained as bank income rather than charity. " + NOT_A_RULING})
    elif lp["markup_increase_on_late"] is True:
        f.update({"status": "violated", "contract_element": "late-payment clause",
                  "quote": lp["increase_quote"], "violation_pattern": rule["violated_by"][0],
                  "note": "Markup increased on late payment. " + NOT_A_RULING})
    elif lp["penalty_destination"] == "charity":
        f.update({"status": "satisfied", "contract_element": "late-payment clause",
                  "quote": lp["charity_quote"],
                  "note": "Late-payment charge directed to charity; markup not increased. " + NOT_A_RULING})
    else:
        f.update({"status": "indeterminate", "contract_element": "late-payment clause", "quote": "",
                  "missing_fact": "late-payment penalty destination and markup-on-late treatment",
                  "note": "Could not establish the late-payment treatment. " + NOT_A_RULING})
    return f


def _r6(s, rule, defer_data):
    w = s["wad_promise"]
    found = []
    if w["type"]:
        found.append(f"a {w['type']} promise")
    if w["binding_language"]:
        found.append("binding language present")
    descr = "; ".join(found) if found else "a promise (wa'd)"
    note = (f"Promise structure found: {descr}. The bindingness of the wa'd in MPO is a contested matter; "
            "the divergent authoritative positions are surfaced and the determination is routed to the SSB. " + NOT_A_RULING)
    return _deferral(rule, defer_data, "promise (wa'd) structure", w["quote"], note)


def _i1(s, rule, _d):
    ij = s["ijara"]
    f = _base(rule)
    if ij["permissible_use_violation"] is True:
        f.update({"status": "violated", "contract_element": "leased asset / use",
                  "quote": ij["use_quote"], "violation_pattern": rule["violated_by"][2],
                  "note": "Asset leased to a prohibited use. " + NOT_A_RULING})
    elif ij["asset_consumable"] is True:
        f.update({"status": "violated", "contract_element": "leased asset / consumability",
                  "quote": "", "violation_pattern": rule["violated_by"][0],
                  "note": "Leased asset is a consumable. " + NOT_A_RULING})
    elif s["asset"]["present"]:
        f.update({"status": "satisfied", "contract_element": "leased asset",
                  "quote": s["asset"]["quote"],
                  "note": "Identified non-consumable asset; no prohibited-use cue found. " + NOT_A_RULING})
    else:
        f.update({"status": "indeterminate", "contract_element": "leased asset", "quote": "",
                  "missing_fact": "asset eligibility (non-consumable, identified, lawful use)",
                  "note": "Could not establish asset eligibility. " + NOT_A_RULING})
    return f


def _i2(s, rule, _d):
    ij = s["ijara"]
    f = _base(rule)
    if ij["unilateral_increase"] is True:
        f.update({"status": "violated", "contract_element": "rent terms",
                  "quote": ij["increase_quote"], "violation_pattern": rule["violated_by"][1],
                  "note": "Lessor's unilateral post-contract rent increase. " + NOT_A_RULING})
    elif ij["rent_defined"] is False or ij["term_defined"] is False:
        f.update({"status": "violated", "contract_element": "rent/term definition",
                  "quote": ij["rent_quote"] or ij["term_quote"], "violation_pattern": rule["violated_by"][0],
                  "note": "Rent or term not defined at contract. " + NOT_A_RULING})
    elif ij["rent_defined"] is True and ij["term_defined"] is True:
        f.update({"status": "satisfied", "contract_element": "rent terms",
                  "quote": ij["rent_quote"] or ij["term_quote"],
                  "note": "Rent and term defined at contract; no unilateral-increase right. " + NOT_A_RULING})
    else:
        f.update({"status": "indeterminate", "contract_element": "rent terms", "quote": "",
                  "missing_fact": "rent and term definition", "note": "Could not establish rent/term. " + NOT_A_RULING})
    return f


def _i3(s, rule, _d):
    ij = s["ijara"]
    f = _base(rule)
    if ij["lease_before_acquisition"] is True:
        f.update({"status": "violated", "contract_element": "acquisition vs lease timing",
                  "quote": ij["lba_quote"], "violation_pattern": rule["violated_by"][0],
                  "note": "Lease executed before the lessor acquired the asset. " + NOT_A_RULING})
    elif ij["lessor_owns_before_lease"] is True:
        f.update({"status": "satisfied", "contract_element": "ownership before lease",
                  "quote": ij["owns_quote"],
                  "note": "Lessor owns/possesses the asset before leasing. " + NOT_A_RULING})
    else:
        f.update({"status": "indeterminate", "contract_element": "ownership before lease", "quote": "",
                  "missing_fact": "whether the lessor acquired the asset before the lease",
                  "note": "Could not establish acquisition-before-lease. " + NOT_A_RULING})
    return f


def _i4(s, rule, _d):
    ij = s["ijara"]
    f = _base(rule)
    if ij["risk_shifted_to_lessee"] is True:
        f.update({"status": "violated", "contract_element": "ownership-risk allocation",
                  "quote": ij["risk_shift_quote"], "violation_pattern": rule["violated_by"][0],
                  "note": "Ownership risk (maintenance/takaful/total-loss) shifted to the lessee. " + NOT_A_RULING})
    elif ij["lessor_bears_ownership_risk"] is True:
        f.update({"status": "satisfied", "contract_element": "ownership-risk allocation",
                  "quote": ij["lessor_risk_quote"],
                  "note": "Lessor bears basic maintenance, takaful and total-loss risk. " + NOT_A_RULING})
    else:
        f.update({"status": "indeterminate", "contract_element": "ownership-risk allocation", "quote": "",
                  "missing_fact": "allocation of major maintenance / takaful / total-loss risk",
                  "note": "Could not establish ownership-risk allocation. " + NOT_A_RULING})
    return f


def _i5(s, rule, _d):
    ij = s["ijara"]
    f = _base(rule)
    if ij["rent_before_delivery"] is True:
        f.update({"status": "violated", "contract_element": "rent timing",
                  "quote": ij["rent_timing_quote"], "violation_pattern": rule["violated_by"][0],
                  "note": "Rent accrues before delivery (rent on money). " + NOT_A_RULING})
    elif ij["rent_before_delivery"] is False:
        f.update({"status": "satisfied", "contract_element": "rent timing",
                  "quote": ij["rent_timing_quote"],
                  "note": "Rent accrues only after delivery and while usable. " + NOT_A_RULING})
    else:
        f.update({"status": "indeterminate", "contract_element": "rent timing", "quote": "",
                  "missing_fact": "when rent begins to accrue (delivery vs contract date)",
                  "note": "Could not establish rent timing. " + NOT_A_RULING})
    return f


def _i6(s, rule, _d):
    ij = s["ijara"]
    f = _base(rule)
    if ij["transfer_fused"] is True:
        f.update({"status": "violated", "contract_element": "IMB transfer separation",
                  "quote": ij["transfer_quote"], "violation_pattern": rule["violated_by"][0],
                  "note": "Sale/transfer fused into the lease; lessor ownership liability evaporates. " + NOT_A_RULING})
    elif ij["is_imb"] is True and ij["transfer_fused"] is False:
        f.update({"status": "satisfied", "contract_element": "IMB transfer separation",
                  "quote": ij["transfer_quote"],
                  "note": "Ownership transfer is by a separate instrument; the lease stays a genuine lease. " + NOT_A_RULING})
    elif ij["is_imb"] is True:
        f.update({"status": "indeterminate", "contract_element": "IMB transfer separation", "quote": "",
                  "missing_fact": "whether the transfer instrument is separate from the lease",
                  "note": "IMB detected but separation of the transfer instrument not established. " + NOT_A_RULING})
    else:
        f.update({"status": "indeterminate", "contract_element": "IMB transfer separation", "quote": "",
                  "missing_fact": "contract is not identified as lease-to-own (IMB); I6 engages only for IMB",
                  "note": "Not identified as IMB; the separation requirement is not engaged. " + NOT_A_RULING})
    return f


def _i7(s, rule, defer_data):
    ij = s["ijara"]
    if ij["sale_leaseback"] is not True:
        f = _base(rule)
        f.update({"status": "indeterminate", "contract_element": "sale-and-leaseback", "quote": "",
                  "missing_fact": "no sale-and-leaseback present; I7 engages only for sale-and-leaseback",
                  "note": "No sale-and-leaseback detected; the interval requirement is not engaged. " + NOT_A_RULING})
        return f
    if ij["sale_leaseback_interval"] is False:
        f = _base(rule)
        f.update({"status": "violated", "contract_element": "sale-and-leaseback interval",
                  "quote": ij["sl_quote"], "violation_pattern": rule["violated_by"][0],
                  "note": "Simultaneous sale-and-leaseback with no interval (inah pattern). " + NOT_A_RULING})
        return f
    if ij["sale_leaseback_interval"] is True:
        f = _base(rule)
        f.update({"status": "satisfied", "contract_element": "sale-and-leaseback interval",
                  "quote": ij["sl_quote"], "note": "A genuine interval separates sale and leaseback. " + NOT_A_RULING})
        return f
    # interval present-but-unquantified -> the sufficiency is contested -> defer to D2
    return _deferral(rule, defer_data, "sale-and-leaseback interval (sufficiency)", ij["sl_quote"],
                     "Sale-and-leaseback present; the sufficiency of the interval is contested. " + NOT_A_RULING)


_EVALUATORS = {"R1": _r1, "R2": _r2, "R3": _r3, "R4": _r4, "R5": _r5, "R6": _r6,
               "I1": _i1, "I2": _i2, "I3": _i3, "I4": _i4, "I5": _i5, "I6": _i6, "I7": _i7}


def _imb_wad_deferral(rule_i6, defer_data, quote):
    """Append a D1 deferral for the IMB ownership-transfer promise's bindingness."""
    f = _base(rule_i6)
    e = _defer(defer_data, "D1")
    f.update({
        "status": "deferral",
        "contract_element": "IMB ownership-transfer promise (wa'd) bindingness",
        "quote": quote,
        "positions": [{"authority": p["authority"], "position_ar": p["position_ar"],
                       "position_en": p["position_en"], "citation": p["citation"]} for p in e["positions"]],
        "routing_en": e["routing_en"], "routing_ar": e["routing_ar"],
        "note": "The bindingness of the IMB ownership-transfer promise is contested; positions surfaced, routed to the SSB. " + NOT_A_RULING,
    })
    return f


def check(structure, rules_data, defer_data):
    # Fail closed: an incomplete extraction is not checked rule-by-rule.
    if not structure.get("extraction_complete", False):
        return [{
            "rule_id": None, "status": "indeterminate",
            "contract_element": "whole document",
            "quote": "", "citations": [], "violation_pattern": None,
            "positions": None, "routing_en": None, "routing_ar": None,
            "missing_fact": ", ".join(structure.get("unresolved", [])) or "core contract structure",
            "note": structure.get("status", "extraction incomplete — requires human review") + ". " + NOT_A_RULING,
        }]
    findings = []
    i6_rule = None
    for r in rules_data["rules"]:
        rid = r["id"]
        if rid == "I6":
            i6_rule = r
        if r.get("status") == "contested":      # never satisfied/violated
            findings.append(_r6(structure, r, defer_data) if rid == "R6" else
                            _deferral(r, defer_data, "contested matter", "", NOT_A_RULING))
        else:
            findings.append(_EVALUATORS[rid](structure, r, defer_data))

    # Ijara IMB → surface the contested wa'd bindingness as a D1 deferral (never adjudicated).
    if i6_rule is not None and structure.get("ijara", {}).get("is_imb") is True:
        findings.append(_imb_wad_deferral(i6_rule, defer_data, structure["ijara"].get("transfer_quote", "")))
    return findings
