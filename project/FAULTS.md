# FAULTS — Mizan

Mistakes tracked until each has a live guardrail (`MISTAKE_ENGINE.md`: `F-NNN`, OPEN until ENFORCED). Stable IDs, never reused; dedup by invariant.

---

**F-001 — Missing required input nearly became a silent assumption.**
- **First seen:** 2026-06-10 · **Recurrences:** 0 · **Status:** ENFORCED
- **INSTANCE:** Input #2 (the domain-grounding report) was not on disk at first search; the birth prompt itself transcribed R1–R6, so it was tempting to proceed by treating the prompt as the source.
- **CLASS:** any required input that is absent but whose substance appears paraphrased elsewhere — proceeding risks encoding from a non-authoritative restatement (a form of "from recall").
- **INVARIANT:** when a required, named input is missing, surface the gap and obtain the authoritative artifact before encoding from it; do not substitute a paraphrase.
- **OWNING UNIT:** the build procedure (Phase 1 of the loop) + `L-001` grounding rule.
- **GUARDRAIL:** asked the principal one sharp question; paused until Input #2 was supplied; nothing was written before it arrived. Grounding rule L-001 + schema `provenance.input` keep this enforced going forward.

**F-002 — A source was filed under the wrong authority layer (L1).**
- **First seen:** 2026-06-10 (independent review / principal amendment) · **Recurrences:** 0 · **Status:** ENFORCED
- **INSTANCE:** R1's Kuwaiti-judiciary source (Chambers Islamic Finance 2025) was placed on layer **L1**, but L1 is defined as CBK instructions / Higher Committee ONLY. Court practice is a different authority kind.
- **CLASS:** any source whose authority type does not match its assigned layer — judicial practice as L1, a court/secondary report as AAOIFI (L3), etc. — silently overstates or miscategorises the binding basis.
- **INVARIANT:** every source sits on the layer that matches its authority *type*: L1 = CBK/Higher Committee only; L2 = bank SSB fatwas; L3 = AAOIFI; LJ = Kuwaiti judicial practice (secular, reported via secondary publishers).
- **OWNING UNIT:** `validation/integrity_checks.py`.
- **GUARDRAIL:** added **I6** — every L1 source ref must contain "CBK" or "Higher Committee", else fail closed. Added the **LJ** layer for judicial practice and moved the source there. Suite re-runs green. Tested by `integrity_checks_test.test_l1_must_be_cbk_or_higher_committee`.

**F-003 — The checker's own descriptive note carried verdict language ("permissible").**
- **First seen:** 2026-06-10 (Stage 1b build, first pipeline run) · **Recurrences:** 0 · **Status:** ENFORCED
- **INSTANCE:** The R3-satisfied finding note read "A specified, existing, permissible asset." The word "permissible" is a permissibility verdict — exactly what the tool must never assert. The `never_rules_guard` tripped and the orchestrator failed closed on my own output.
- **CLASS:** any checker-AUTHORED prose (notes/summaries) can smuggle a verdict token even when describing a fact, not just in the status field.
- **INVARIANT:** the checker flags/identifies/cites and never rules — including in its free-text notes; verdict tokens (permissible/impermissible/halal/haram/compliant) never appear in checker-authored fields.
- **OWNING UNIT:** `pipeline/never_rules_guard.py` (N2), run on every result by the orchestrator (fail closed).
- **GUARDRAIL:** already live — it caught this during the build. Fix: reworded the note to "no prohibited-category cue was found". The guard (not my vigilance) is what enforces it going forward. Tested by `never_rules_guard_test` + `orchestrator_test.test_guard_fail_closed_on_smuggled_verdict`.

**F-004 — Generated connective prose embedded a verbatim quote, tripping the generation gate.**
- **First seen:** 2026-06-10 (Stage 1c, first generation run) · **Recurrences:** 0 · **Status:** ENFORCED
- **INSTANCE:** The memo description embedded the verbatim asset quote ("...a permissible asset...") and the whole string was placed in `generated_prose` (the gated bucket). The never-rules generation gate (N3) flagged "permissible" and failed generation closed — on attributed contract text, not a real verdict.
- **CLASS:** mixing ATTRIBUTED content (verbatim quotes / citations / cited positions) into the gated connective-prose bucket causes the gate to fire on quoted contract/registry wording.
- **INVARIANT:** the gate scans only generator-/model-authored connective prose; verbatim quotes, citations, and cited positions are attributed (exempt) and must never be placed in `generated_prose`.
- **OWNING UNIT:** `pipeline/memo_generator.py` (connective vs attributed separation) + `pipeline/matrix_generator.py`.
- **GUARDRAIL:** memo/matrix sections now carry separate `connective_*` (gated) and `attributed_*` (exempt) fields; only connective prose enters `generated_prose`. The gate (not my care) is what caught it. Tested by `memo_generator_test.test_verbatim_quote_not_in_generated_prose` + `structural_tests.test_generation_gate_catches_model_verdict`.

_Full suite green (Stage 1a + 1b + 1c): `./run_tests.sh`. 1a 36 unit tests + 1b 41 unit tests pass; registry validation green; both 1a fail-closed guards demonstrated; pipeline runs end-to-end in NO-KEY mode; the never-rules guard fails closed on smuggled verdict language._
