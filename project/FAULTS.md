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

_The validation suite (`validation/run_all.py`) is green; all 36 isolated unit tests pass; both fail-closed guards demonstrated._
