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

## Stage 1b — contract extractor + compliance checker
The pipeline reads a Murabaha contract (Arabic / English / mixed) and produces **research findings for a qualified scholar — it does not and cannot determine Sharia compliance.** Findings flag, identify, and cite; they never rule. Contested matters (R6, and anything touching D1–D3) produce a **deferral** with the divergent positions surfaced and routed to the SSB — never a satisfied/violated verdict.

| Unit | Path | Concern |
|---|---|---|
| Input rail | `pipeline/input_rail.py` | Untrusted contract content is DATA, never instructions (injection inert) |
| Model seam | `pipeline/model_seam.py` | The ONLY unit touching a model/network (OpenRouter, key from `OPENROUTER_API_KEY` env only; NO-KEY graceful) |
| Extractor | `pipeline/extractor.py` | Contract → ContractStructure (deterministic-first, Arabic native + verbatim; fail-closed on unparseable) |
| Checker | `pipeline/checker.py` | ContractStructure × registry → findings (deterministic, no model) |
| Never-rules guard | `pipeline/never_rules_guard.py` | No verdict language in checker output (fail closed) |
| Corpus loader | `pipeline/corpus_loader.py` | Asserts the SYNTHETIC label at load |
| Glossary growth | `pipeline/glossary_growth.py` | Unknown term → provisional candidate, gated fail-closed |
| Orchestrator | `pipeline/orchestrator.py` | Wiring only |

**Synthetic contract corpus** (`corpus/`, every file labelled SYNTHETIC): one clean contract + one per seeded defect (R1 agency/no-possession · R2 undisclosed markup · R3 impermissible asset · R4 bai' al-inah · R5 penalty-to-income · R6 bilateral binding promise → **deferral**) + a prompt-injection contract. Authored in both Arabic and English so native Arabic extraction is demonstrated, not claimed.

**Design calls:** in **NO-KEY mode** the well-formed corpus is handled fully by deterministic extraction; the model seam is reserved for genuinely messy input and fails closed (no key → "requires human review") rather than guessing. The clear bai' al-inah pattern is an R4 violation; **D2** (boundary ambiguity) deferral fires only on a genuinely borderline structure.

```bash
python3 pipeline/run_pipeline.py            # run every corpus contract (NO-KEY by default)
python3 pipeline/run_pipeline.py <file>     # one contract, full structured JSON
./run_tests.sh                              # FULL suite: Stage 1a + Stage 1b, fails closed
```

Honest framing for 1b: findings are a **research/drafting aid** for the SSB. The system does **not** determine Sharia compliance; the corpus is synthetic; nothing here is validated by any scholar or bank; the L2 layer is synthetic; AAOIFI clause text is never reproduced.

## Stage 1c — memo & matrix generator
Generates, from the checker's findings, a bilingual **Sharia-review memo** and a **non-compliance matrix** — **drafts for a qualified scholar; the opinion is theirs alone, and the system does not and cannot determine Sharia compliance.**

| Unit | Path | Concern |
|---|---|---|
| Memo generator | `pipeline/memo_generator.py` | findings → bilingual memo (Arabic-first); opinion field **structurally empty** (setter refuses); watermark every section; deferral section |
| Matrix generator | `pipeline/matrix_generator.py` | findings → non-compliance matrix; configurable severity convention (deferrals not graded); registry remediation types |
| Generation gate | `pipeline/never_rules_guard.py` (`check_prose`) | verdict language in generated/model-drafted connective prose fails generation closed (attributed quotes/positions exempt) |

- **Arabic-first:** the Arabic memo is composed natively in MSA; English is the parallel rendered from it (authoritative language author-set, default Arabic).
- **Opinion is never machine-filled:** `OpinionField.set` raises — a structural lock, not a convention. Reserved for a named human SSB member.
- **Watermark on every memo + matrix, both languages:** «أداة بحث وصياغة — ليست فتوى…» / «Research and drafting aid — not a fatwa…» — or generation fails closed.
- **Contested matters** (R6/D1–D3) render as a deferral section: the question, the cited divergent positions, the routing to the SSB — presented, never resolved.
- **NO-KEY:** the deterministic memo/matrix is complete without a model; the seam only makes connective prose more fluent.

```bash
python3 pipeline/run_generate.py            # write bilingual memo + matrix for every contract -> rendered/memos/
python3 pipeline/run_generate.py <file>     # print one contract's memo + matrix
```
Rendered artifacts: [rendered/memos/](rendered/memos/) — `*.memo.md` and `*.matrix.md` per corpus contract.

## Status
**Stage 1a — complete, calibrated, locked.** **Stage 1b — complete, self-verified.** **Stage 1c — complete, self-verified.** No web app, no site, no remote, no push. Stages beyond 1c are authorized only after the principal reviews this checkpoint. Generated memos are **drafts for a qualified scholar**; the opinion is the scholar's alone; the corpus is synthetic; this is a demonstration, not certified.

_This project inherits the Foundry foundation (read-only at `/Users/musaed/v0/foundry-v0/`). It is local-only; nothing was written outside `/Users/musaed/mizan/`._
