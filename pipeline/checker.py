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


_EVALUATORS = {"R1": _r1, "R2": _r2, "R3": _r3, "R4": _r4, "R5": _r5, "R6": _r6}


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
    for r in rules_data["rules"]:
        rid = r["id"]
        if r.get("status") == "contested":      # never satisfied/violated
            findings.append(_r6(structure, r, defer_data) if rid == "R6" else
                            _deferral(r, defer_data, "contested matter", "", NOT_A_RULING))
        else:
            findings.append(_EVALUATORS[rid](structure, r, defer_data))
    return findings
