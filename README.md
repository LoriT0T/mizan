# Mizan (ميزان) — Sharia-Review Copilot

_License: [MIT](LICENSE) · a working demonstration — local-only, **not deployed, not certified**, and it **never issues a ruling**._


**Mizan is a working demonstration, not a certified product.** It is a Sharia-review **copilot** for Islamic-finance contracts in Kuwait's regulatory context: it researches, drafts, and documents for a qualified human Sharia scholar (the SSB). **It never issues a ruling (fatwa), and it never adjudicates a contested matter.**

## Honest framing (read this first)
- **Built on publicly documented principles.** Every rule, citation, and claim traces to one of two input documents or a fetched, cited public source — never to model recall.
- **Not certified.** The canonical Arabic has been reviewed and **locked** by the principal (a qualified native-Arabic reviewer) — see the consolidated review lists in `rendered/ARABIC_REVIEW_LIST*.md`. The system as a whole is still a **demonstration**: it has **not** been certified by any bank, it is not a substitute for the SSB's ruling, and clause-level AAOIFI verification (below) remains required before any real-world use.
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

## Stage 2 — scope-awareness + honest deferral + the Ijara rule-set
Mizan is now honest about **what it does not cover**, and adds **Ijara** as a second grounded, calibrated contract type. Breadth grows one grounded type at a time; ungrounded rules are forbidden.

- **Scope registry** (`registry/scope_registry.json`, rendered `rendered/SCOPE.md`) is the single source of truth for coverage — this README and the memos read from it so the stated limits never drift:
  - **covered + calibrated:** Murabaha (R1–R6), Ijara (I1–I7)
  - **recognized but not covered:** Tawarruq (classifier knows it; **no rule-set** — routed to defer **D3** with positions surfaced)
  - **unrecognized:** everything else → flagged out-of-scope, routed to the scholar
- **Contract-type classifier** (`pipeline/contract_type_classifier.py`) types a contract (murabaha / ijara / tawarruq / unrecognized) by structure cues; it classifies, it does not rule; it fails to "unrecognized" rather than guessing.
- **Out-of-scope behavior** (`pipeline/scope.py`): for any uncovered component Mizan emits an explicit out-of-scope finding — it never fabricates a rule, never applies one type's rules to another, never stays silent. A **mixed** contract gets covered parts checked **and** uncovered parts flagged.
- **Ijara rules** (`registry/rules_ijara.json`, I1–I7; rendered `rendered/REGISTRY_IJARA.md`): asset eligibility · rent/term defined · lessor owns before lease · **I4 lessor bears ownership risk (the headline test)** · rent after delivery · IMB transfer separate (→ defer D1) · sale-and-leaseback interval (→ defer D2). New contested matters D4 (rate-benchmarking), D5 (AITAB) in `registry/defer_register_ijara.json`.

```bash
python3 pipeline/run_pipeline.py            # classify + check every contract (corpus/ + corpus/stage2/)
python3 pipeline/run_generate.py            # memo + matrix for every contract
./run_tests.sh                              # full suite: 1a + 1b + 1c + 2
```

## Stage 3 — local web frontend + GCC/Kuwait test corpus
A **local-only** web UI (`web/`, stdlib `http.server` — zero external deps) wraps the engine behind a hard architectural wall: `web/` holds **zero rule logic, zero registry reads, zero checker code** — it calls `orchestrator.run_text` / `generate_for_text` and renders. The engine runs and tests fully with `web/` absent (proven in the suite).

**Running locally**
```bash
python3 web/server.py                 # binds 127.0.0.1:8877 (loopback only; refuses 0.0.0.0)
# open http://127.0.0.1:8877  → paste or upload a .txt contract → Run review

# the port is configurable (default 8877): --port flag or MIZAN_PORT env take precedence
python3 web/server.py --port 9001
MIZAN_PORT=9001 python3 web/server.py
# if the port is taken it exits with a clear message ("port N in use — set MIZAN_PORT or --port"), not a traceback
```
- **NO-KEY mode is first-class:** with no `OPENROUTER_API_KEY` the UI runs the full deterministic pipeline and shows a *"NO-KEY mode — deterministic extraction only"* badge. With a key set in the **server env only**, the model seam is used; the key never appears in any served byte (scanned on every response), log, or error.
- **Untrusted uploads:** size-capped (256 KB), `.txt`/paste only, run through the injection-inert input rail, held in RAM for the session only (never persisted to disk), no telemetry, no external calls except the seam.
- **The UI never rules:** the not-a-fatwa watermark sits at the top of every page (both languages); status labels come from the engine's vocabulary only; the never-rules guard runs over the UI chrome at serve time and fails closed; deferral and out-of-scope items are shown prominently **not graded**; a calibration badge reads `arabic_review_status` from the engine (with all Arabic now locked it shows *"All Arabic calibrated"*; it would show *"Arabic pending expert calibration"* for any not-yet-locked content).
- A `/scope` page renders exactly what Mizan covers and to what depth.

**GCC/Kuwait test corpus** (`corpus/stage3/`, researched then authored — see `corpus/stage3/PROVENANCE.md`): T1 clean Kuwaiti vehicle Murabaha · T2 Murabaha with a *subtle* buried R1 defect · T3 home IMB with the I4 ownership-risk-shift *dressed* in an "obligations of the customer" schedule · T4 commodity tawarruq (recognized, no rule, D3) · T5 Murabaha + investment-wakala (covered checked, uncovered out-of-scope). Result bundles (findings · memo · matrix · rendered HTML) in `rendered/stage3/`.

> **This is a local demonstration — not deployed, not certified.** No public hosting, no tunnel, no remote.

## Status
**Stage 1a — locked.** **1b / 1c / 2 — self-verified.** **Stage 3 — self-verified (local frontend + GCC corpus).** No remote, no push, no public hosting. Generated memos are **drafts for a qualified scholar**; the opinion is the scholar's alone; Mizan **does not and cannot determine Sharia compliance** and is honest about the types it does not cover; the corpus is synthetic; not certified. The Murabaha **and Ijara** registries are unmodified by Stage 3 (the frontend reads the engine, not the registry); the glossary grew only via the documented growth protocol.

_This project was built on a private "Foundry" agent foundation (inherited read-only, not part of this repo). It is local-only by design._
