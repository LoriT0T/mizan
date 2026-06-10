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
**Stage 1b (extractor + checker) is authorized** upon the principal's confirmation of this calibration result. Stage 1a is closed.
