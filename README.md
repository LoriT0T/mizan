# Mizan (ميزان) — Sharia-Review Copilot · Stage 1a

**Mizan is a working demonstration, not a certified product.** It is a Sharia-review **copilot** for Islamic-finance contracts in Kuwait's regulatory context: it researches, drafts, and documents for a qualified human Sharia scholar (the SSB). **It never issues a ruling (fatwa), and it never adjudicates a contested matter.**

## Honest framing (read this first)
- **Built on publicly documented principles.** Every rule, citation, and claim traces to one of two input documents or a fetched, cited public source — never to model recall.
- **Not certified.** This artifact has **not** been validated by a Sharia scholar or any bank. The canonical Arabic and all domain content are labelled `awaiting-expert-judgment` and await the principal's calibration (see `rendered/ARABIC_REVIEW_LIST.md`).
- **Clause-level AAOIFI verification is a required next step.** The full AAOIFI Sharia Standards text is copyrighted; this registry references standard numbers, topics, and widely-cited principles **only** — never reproduced clause text. Before any real-world use, every L3 reference must be verified against the purchased AAOIFI texts.
- **The L2 corpus is SYNTHETIC.** The bank-SSB-fatwa layer here is a clearly-labelled stand-in for demonstration; it is not, and must never be read as, a real ruling.
- **The tool never rules.** The Sharia opinion is structurally reserved to the human SSB.

## What this stage produced (Murabaha scope only)
| Artifact | Path |
|---|---|
| Rule Registry (data) — R1–R6, bilingual, layered, cited | `registry/rules.json` |
| Defer-on-disagreement register (data) | `registry/defer_register.json` |
| Terminology glossary + growth protocol (data) | `registry/glossary.json` · history `registry/glossary_history.json` |
| Rendered human-readable views | `rendered/REGISTRY.md` · `DEFER_REGISTER.md` · `GLOSSARY.md` |
| Consolidated Arabic review list (for the principal) | `rendered/ARABIC_REVIEW_LIST.md` |
| JSON schemas | `schemas/*.schema.json` |
| Validation suite (compartmentalized, isolated tests) | `validation/` |
| Project memory | `project/` · identity `identity/SOUL.md` |

## The rules (R1–R6, Murabaha)
1. **R1** — ownership + (actual/constructive) possession before resale · *established*
2. **R2** — cost + markup disclosed, price fixed at contract · *established*
3. **R3** — asset exists and is permissible · *established*
4. **R4** — asset not already the customer's (bar on *bai' al-inah*) · *established*
5. **R5** — late-payment charge to charity, never income; no markup increase · *established*
6. **R6** — the promise (*wa'd*) bindingness in MPO · **contested** → deferred (D1)

## Source-layer hierarchy (Kuwait)
- **L1** — CBK instructions / Higher Committee of Shari'ah Supervision (binding in Kuwait)
- **L2** — the institution's own SSB fatwas (binding per-bank; **SYNTHETIC** here)
- **L3** — AAOIFI Sharia Standards (persuasive reference in Kuwait)

## Run it
```bash
# Full validation suite — fails closed (exit 1) on any violation
python3 validation/run_all.py

# Each unit's isolated test (runs without the orchestrator or its siblings)
cd validation && python3 -m unittest schema_validator_test integrity_checks_test \
  citation_guard_test glossary_checks_test synthetic_corpus_guard_test

# Demonstrate the fail-closed guards (no-reproduced-text + glossary collision)
python3 validation/demo_failclosed.py

# Re-render the human-readable views from the JSON source of truth
python3 render.py
```

## Status
**Stage 1a — complete and self-verified, awaiting the principal's Arabic + domain calibration.** No extractor, no checker, no memo generator, no web app, no remote. Stage 1b (extractor + checker) is authorized only after the consolidated Arabic review list is returned and applied.

_This project inherits the Foundry foundation (read-only at `/Users/musaed/v0/foundry-v0/`). It is local-only; nothing was written outside `/Users/musaed/mizan/`._
