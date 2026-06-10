# STATE — Mizan Stage 1a

> Per `foundation/MEMORY_ARCHITECTURE.md`: externalized at every milestone, not banked for the end. The live context is volatile.

**Project:** Mizan (ميزان) — a Sharia-review *copilot* for Islamic-finance contracts. It researches, drafts, and documents for a qualified human scholar; it **never rules**.
**Stage:** 1a only — the bilingual Rule Registry (Murabaha scope), built and verified as a standalone artifact before any pipeline code.
**Workspace:** `/Users/musaed/mizan/` (own git repo, local only, no remote).
**Foundry root:** `/Users/musaed/v0/foundry-v0/` — READ-ONLY. Baseline SHA-256 over all 29 files: `8e71b7a3f64d0b6ce13ec59f6f65107c4df128015cd0b4cb68dd7e9426d33062` (captured at birth; re-verified at checkpoint).

## Inputs (both read fully before writing)
- **Input #1** — `~/Downloads/Kuwait Banking.pdf` (7pp): problem-discovery diagnostic. Satisfies the problem-discovery birth question externally.
- **Input #2** — `~/Downloads/Mizan_Input2_Domain_Grounding_Report.md` (200 lines): domain-grounding research report. Source of R1–R6, the L1/L2/L3 hierarchy, memo formats, contested matters. Carries its own established-vs-provisional discipline + AAOIFI copyright boundary — **preserved when encoding** (provisional in → provisional out; never promoted).

## Hard rules carried into the build
- Every rule/citation/claim ← the two inputs OR a public authoritative source fetched + cited. **Never from recall.** Cannot ground → do not encode (admitted gap > confident guess).
- Arabic canonical text composed **natively** in formal MSA (not translated from English), at full capability, then routed to the principal as the final calibration layer (expert-judgment principle, `RELIABILITY.md` §2).
- NEVER reproduce AAOIFI clause text — reference by number/topic/principle only (length-bounded citations).
- L2 (bank SSB fatwas) is a **SYNTHETIC** corpus in this demo — labelled synthetic everywhere, asserted at load.
- The tool never issues rulings. Contested matters surfaced, never adjudicated.

## Deliverables (checkpoint a–g)
| # | Artifact | Status |
|---|---|---|
| (1) | Rule Registry (data + rendered), R1–R6, bilingual | done |
| (2) | Defer-on-disagreement register | done |
| (3) | Terminology glossary (seed + growth protocol + demo) | done |
| (4) | Validation tooling (compartmentalized, isolated tests) | done |
| (5) | Project memory (BIRTH_CERTIFICATE, STATE, LESSONS, FAULTS) + README | done |
| a | Birth certificate | done |
| b | Registry rendered human-readable | done |
| c | Defer register rendered | done |
| d | Glossary seed + growth-protocol demo (unseeded term end-to-end) | done |
| e | Validation suite passing + no-reproduced-text guard + collision fail-closed demonstrated | done |
| f | Consolidated Arabic review list | done |
| g | Confirm only ~/mizan written; Foundry byte-untouched | done |

## Calibration applied (2026-06-10)
Principal accepted all Arabic review items as-is. Changes made:
- All rule `arabic_review_status` and all glossary lifecycle statuses → `locked` (rules v1.1.0, glossary v1.2.0, defer v1.1.0).
- **Amendment 1:** R1's Kuwaiti-judiciary source reclassified L1 → new **LJ** layer (judicial practice, outside the L1/L2/L3 Sharia-standards hierarchy); guardrail I6 added (L1 = CBK/Higher Committee only). See `FAULTS.md` F-002.
- **Amendment 2:** provenance axis relabelled `established_or_provisional`(established|provisional) → `grounding_basis`(grounded|unverified), container unified to `provenance` across registry+defer+glossary; integrity I5 now asserts the three axes' vocabularies are pairwise-disjoint so "established" can only mean rule status. G-013 grounding_basis = `unverified`.
- Suite green (5/5 checks, 36 unit tests, both fail-closed guards); Foundry byte-untouched; only `~/mizan/` written.

## Next action
Stage 1a is closed.

---

# STAGE 1b — extractor + compliance checker (in progress)
**Branch-trigger check (honest):** untrusted document input → loaded `knowledge/guardrails`; model seam → loaded `knowledge/cost-routing`. Only those two. (Not RAG: single provided document, no corpus retrieval. Not orchestration/deployment/eval/memory/mcp/context-engineering.)

**Source of truth:** locked registry (rules v1.1.0, defer v1.1.0, glossary v1.2.0) — READ-ONLY to 1b code. The checker never mutates the registry; new terms enter only via the glossary growth protocol (provisional → review list). Rule logic not traceable to a registry entry does not exist.

**Architecture (compartmentalized; `pipeline/`):**
- `input_rail` — contract content is DATA never instructions (injection inert); wraps text for any model use, scans+records injection spans (non-blocking).
- `model_seam` — ONLY unit touching model/network. OpenRouter, key from env `OPENROUTER_API_KEY` only; per-language override; graceful NO-KEY mode. FakeSeam in tests.
- `extractor` — text → ContractStructure (deterministic-first, bilingual, Arabic verbatim; model reserved for messy interpretation). Fail-closed → "extraction incomplete — requires human review". Detects unknown terms → growth protocol.
- `checker` — ContractStructure × registry → findings (deterministic, no model). status ∈ {satisfied, violated, indeterminate, deferral}. Contested (R6/D1–D3) → DEFERRAL only.
- `never_rules_guard` — output guard: no verdict language (حلال/حرام/permissible/impermissible) in checker-authored fields; status never a permissibility word.
- `corpus_loader` — asserts SYNTHETIC label on every contract at load (extends the synthetic discipline).
- `glossary_growth` — thin: term + researched sources → provisional candidate, gated by Stage-1a `glossary_checks.check_candidate` (fail-closed). Live web research is the documented on-demand step.
- `orchestrator` — wiring only.

**Design call (NO-KEY mode):** the synthetic corpus is well-formed, so deterministic extraction covers it end-to-end with no key. The model seam is reserved for genuinely ambiguous interpretation; in NO-KEY mode such cases fail closed to "requires human review" rather than guessing.

**Design call (R4/D2):** the clear, unambiguous bai' al-inah pattern is an established R1–R5-class violation (R4 violated). D2 (boundary ambiguity) deferral fires only when the extractor flags the inah boundary as ambiguous — not on the textbook clear case.

## Stage 1b — COMPLETE and self-verified (2026-06-10)
- Units built (compartmentalized; orchestrator wiring-only): input_rail, model_seam, extractor, checker, never_rules_guard, corpus_loader, glossary_growth, orchestrator + run_pipeline.
- Synthetic corpus (9 contracts, all SYNTHETIC-labelled): clean ar+en, R1–R6 one-defect-each, injection. R6 defect yields DEFERRAL (not violation).
- Full suite GREEN: 1a 36 unit tests + registry validation + both fail-closed guards; 1b 41 unit tests + NO-KEY end-to-end pipeline run. `./run_tests.sh`.
- Every seeded defect caught with citation+layer; clean passes; R6 defers with positions; injection inert; never-rules guard fails closed (caught my own verdict-note → F-003).
- Registry + schemas BYTE-IDENTICAL to Stage 1a (checker never mutates). Foundry byte-untouched. Only ~/mizan written.
- New mistakes → F-003 (verdict in note), lessons L-008 (never-rules is a guard), L-009 (Arabic normalise-before-match).
- Consolidated Arabic review list (1b): `rendered/ARABIC_REVIEW_LIST_1b.md` — no new canonical/glossary Arabic locked; synthetic-contract Arabic offered for optional eyeballing.

## Next action
CHECKPOINT — STOP after 1b. Independent verifier report + workspace zip produced for the principal. Stages beyond 1b authorized only after the principal reviews this checkpoint.
