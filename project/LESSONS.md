# LESSONS — Mizan

Durable rules graduated from this project (`MISTAKE_ENGINE.md` format: `L-NNN`, recorded at the **invariant** level, each wired to a guardrail).

---

**L-001 — Ground every encoded rule; never from recall.**
- **Invariant:** every rule/citation/claim in the registry traces to an input document or a fetched, cited public source. If it cannot be grounded, it is not encoded.
- **Guardrail:** `provenance.input` is required on every rule (schema) and on every defer entry; glossary entries require `grounding.sources` (schema + `integrity_checks`). The growth protocol forbids inventing a term from recall (it must research-then-propose).
- **Why:** an admitted gap beats a confident guess (`RED_LINES.md`). The whole tool's trustworthiness rests on provenance.

**L-002 — Preserve the source's established/provisional discipline; never silently promote.**
- **Invariant:** a claim grounded `provisional` in the source stays `provisional` in the registry; a glossary term grounded provisional must not be `locked`.
- **Guardrail:** `integrity_checks` I5 flags any glossary entry grounded provisional but marked locked. The growth protocol appends as `provisional` and routes to human calibration.

**L-003 — Copyright is a hard line: cite standards, never reproduce them.**
- **Invariant:** no citation field carries reproduced standard (AAOIFI) text — references by number/topic/principle only.
- **Guardrail:** `citation_guard` (C1 length/word caps, C2 quoted-span detection) fails closed on any field that looks like a reproduced passage. Demonstrated in `demo_failclosed.py`.

**L-004 — The synthetic L2 corpus must be unmistakable.**
- **Invariant:** L2 (bank SSB fatwas) in this demo is synthetic and labelled synthetic at every occurrence; no real layer (L1/L3) is ever marked synthetic.
- **Guardrail:** `synthetic_corpus_guard` (S1/S2/S3), asserted at load by the orchestrator.

**L-005 — The glossary never silently holds two renderings of one term.**
- **Invariant:** one canonical Arabic ↔ one canonical English; a candidate conflicting with a locked rendering fails closed and surfaces for human resolution.
- **Guardrail:** `glossary_checks.check` (G1 dedup) + `check_candidate` (fail-closed collision gate). Demonstrated in `demo_failclosed.py`.

**L-006 — Expert judgment calibrates quality at delivery, not mid-build.**
- **Invariant:** compose the Arabic at full capability, label `awaiting-expert-judgment`, and consolidate every item needing the scholar's eye into ONE review list at delivery — never block mid-build, never self-certify as scholar-approved.
- **Guardrail:** `arabic_review_status` field on every rule; the single `rendered/ARABIC_REVIEW_LIST.md`. (`RELIABILITY.md` §2.)
