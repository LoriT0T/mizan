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

## Stage 1b — COMPLETE (see above).

---

# STAGE 1c — memo & matrix generator (COMPLETE, self-verified 2026-06-10)
- Branch-trigger: prose via model seam → cost-routing (already loaded); no new untrusted-input class. Minimum loaded.
- Units (compartmentalized; orchestrator wiring-only): memo_generator (Arabic-first; OpinionField structural lock; watermark; deferral section; connective/attributed separation) · matrix_generator (configurable severity, deferrals not graded, registry remediation types, watermark) · never_rules_guard.check_prose (generation gate) · run_generate (CLI).
- Renders: bilingual memo + matrix for every corpus contract → rendered/memos/ (*.memo.md, *.matrix.md).
- THREE structural tests bite (corpus-wide): opinion never auto-filled (+ structural setter lock); watermark always present (memo+matrix, both langs); generation gate catches a FakeSeam verdict. Plus memo(7)/matrix(6) unit tests, never_rules(8).
- Full suite GREEN (1a+1b+1c): `./run_tests.sh`.
- Registry + glossary unmodified (generators read-only). Foundry byte-untouched. Only ~/mizan written.
- Mistakes → F-004 (verbatim quote embedded in gated prose, caught by the gate); lessons L-010 (opinion lock / watermark gate), L-011 (gate scans connective only).
- New canonical Arabic (template) → rendered/ARABIC_REVIEW_LIST_1c.md. No new glossary terms created.

## Stage 1c — COMPLETE (see above).

---

# STAGE 2 — scope-awareness + honest deferral + Ijara rule-set (in progress)
**Branch-trigger:** classifier may use model seam for ambiguous docs → cost-routing (loaded); contract docs = same untrusted class as 1b (no new knowledge file).
**Input #3:** `inputs/Mizan_Input3_Ijara_Grounding_Report.md` (copied from Downloads; required, present). Establishes I1–I7 (all **established**) + contested matters. Every Ijara rule traces to Input #3 or fetched+cited public source — never recall.

## Key design decisions (to keep Murabaha registry byte-identical + 1a/1b/1c tests green untouched)
- **Murabaha `rules.json`, `defer_register.json` stay BYTE-IDENTICAL.** Ijara rules → NEW `registry/rules_ijara.json`. New Ijara contested matters → NEW `registry/defer_register_ijara.json` (D4 rate-benchmarking, D5 AITAB). Ijara reuses D1 (wa'd, IMB transfer promise) + D2 (inah, sale-leaseback interval) from the existing register.
- **Glossary changes ONLY via growth protocol** (sanctioned): append Ijara terms (G-014+) as `provisional`/`grounded`, bump glossary version, history append. (This is the one locked-registry file that changes, and only via the documented protocol.)
- **Checker is generic** (evaluates whatever rules are passed); orchestrator selects rule-set by classified type. Existing tests pass `rules.json` (Murabaha) → unchanged 6 findings. New I-evaluators added to checker.py are not invoked by Murabaha calls → 1b/1c tests stay green.
- **rule.schema scope enum** extended to ["murabaha","ijara"] (schema is ours; doesn't break inline-schema unit tests).
- **never_rules_guard ALLOWED_STATUS** += "out_of_scope" (new honest status; existing guard tests still pass).

## Units (compartmentalized)
- `contract_type_classifier.py` — structure/text → {murabaha|ijara|tawarruq|unrecognized} (deterministic cues; seam for ambiguous; fails to unrecognized). Classifies structure, not ruling.
- `scope.py` + `registry/scope_registry.json` — single source of truth for coverage; assess(types) → (covered_types, out_of_scope_findings). README + memos read from it.
- Ijara facts in extractor (reuse Arabic normalize + negation machinery).
- checker I1–I7 evaluators + D1 deferral when IMB (wa'd) — never-rules discipline.
- memo/matrix type-aware (Ijara mechanics; I-rule severity/remediation config). Structural locks unchanged.
- Out-of-scope finding (status out_of_scope): covered parts checked, uncovered flagged, nothing fabricated.

## Ijara rules (I1–I7, all established, grounded Input #3 Part 2)
I1 asset eligibility (non-consumable/identified/permissible use) · I2 rent+term defined, no unilateral increase · I3 lessor owns, lease preceded by acquisition · **I4 ownership risk stays with lessor (HEADLINE, most common defect)** · I5 rent after delivery + only while usable · I6 IMB transfer SEPARATE from lease (→D1 wa'd) · I7 sale-leaseback interval (→D2 inah).

## Stage 2 — COMPLETE, self-verified (2026-06-10)
- Part A (honesty): `contract_type_classifier` (murabaha/ijara/tawarruq/unrecognized; fails to unrecognized) · `registry/scope_registry.json` + `scope.py` (single source of truth; out_of_scope findings) · out-of-scope behavior wired + tested (mixed: covered checked + uncovered flagged; tawarruq → D3 no rule).
- Part B (Ijara): `registry/rules_ijara.json` I1–I7 (grounded Input #3; I4 headline) · `registry/defer_register_ijara.json` D4/D5 (reuses D1/D2) · extractor Ijara facts · checker I1–I7 + IMB→D1 deferral · memo/matrix type-aware. Glossary grew G-014..G-022 via growth protocol (v1.3.0, provisional/grounded).
- Renders: `rendered/REGISTRY_IJARA.md`, `DEFER_REGISTER_IJARA.md`, `SCOPE.md`; memos+matrices for corpus/stage2 in `rendered/memos/`.
- Corpus: `corpus/stage2/` (Ijara clean + I4/I5/I6 defects + tawarruq + mixed-OOS). Kept separate so 1c structural tests (corpus/) stay green untouched; `stage2_structural_test` covers the new corpus.
- Full suite GREEN (1a+1b+1c+2): `./run_tests.sh`. Schema enum extended (scope +ijara, id +I, defer scope_status +ijara); validation validates both registries.
- **Murabaha rules.json + defer_register.json BYTE-IDENTICAL to Stage 1** (Ijara is separate files); glossary changed ONLY via growth protocol; Foundry byte-untouched; only ~/mizan written.
- Mistakes → F-005 (negation-matched-affirmative), F-006 (tawarruq mis-class), F-007 (verdict-in-note recurrence); lessons L-012 (grow one type, scope honesty), L-013 (negation-first / precedence).
- New canonical Arabic → `rendered/ARABIC_REVIEW_LIST_2.md`.

## Stage 2 — COMPLETE (see above).

---

# STAGE 3 — local frontend + GCC/Kuwait corpus (COMPLETE, self-verified 2026-06-10)
- Branch-trigger: web surface (guardrails) + live seam (cost-routing) + deployment (local-hosting hygiene only). Loaded deployment; nothing public.
- **PART A — frontend** (`web/`, stdlib `http.server`, zero deps): wall-enforced (zero rule logic/registry/checker; engine runs with web/ absent — proven in suite). 127.0.0.1 only (refuses 0.0.0.0). Key from server env only, scanned out of every served byte. NO-KEY first-class badge. Untrusted uploads: 256KB cap, .txt/paste, injection-inert input rail, RAM-only (not persisted). Bilingual RTL UI; watermark top; status labels = engine vocabulary only; serve-time never-rules guard over UI chrome; calibration badge from `arabic_review_status`; `/scope` page. Additive engine interface: `run_text`, `generate_for_text`, `scope_info`, `calibration_status`.
- **PART B — corpus** (`corpus/stage3/`, researched → `PROVENANCE.md`): T1 clean Murabaha (AR) · T2 subtle R1 (AR) · T3 dressed I4 (AR) · T4 tawarruq (EN, recognized/no-rule/D3) · T5 mixed Murabaha+investment-wakala (AR). All five behave per spec under REALISTIC drafting. Bundles (findings·memo·matrix·result.html) in `rendered/stage3/`.
- Extractor BROADENED for realistic phrasing (defect-specific agency/I4 qualifiers, asset-by-noun, article-tolerant cost/markup/imb, ليس/ليست negation). All prior suites stay green untouched.
- Full suite GREEN (1a+1b+1c+2+3): `./run_tests.sh` incl. WALL step + web tests.
- Registries (Murabaha + Ijara + glossary + scope) UNMODIFIED by Stage 3; Foundry byte-untouched; only ~/mizan written.
- Mistakes/lessons → L-014 (benign-vs-defective by qualifier), L-015 (frontend-behind-wall).
- UI canon Arabic → `rendered/ARABIC_REVIEW_LIST_3.md`.

## Next action
CHECKPOINT — STOP after Stage 3. Independent verifier (incl. key-extraction + verdict-injection attempts) + zip. Principal tests the frontend BY HAND with T1–T5 before anything further. No remote, no push, no public hosting.
