# LESSONS — Mizan

Durable rules graduated from this project (`MISTAKE_ENGINE.md` format: `L-NNN`, recorded at the **invariant** level, each wired to a guardrail).

---

**L-001 — Ground every encoded rule; never from recall.**
- **Invariant:** every rule/citation/claim in the registry traces to an input document or a fetched, cited public source. If it cannot be grounded, it is not encoded.
- **Guardrail:** `provenance.input` is required on every rule (schema) and on every defer entry; glossary entries require `grounding.sources` (schema + `integrity_checks`). The growth protocol forbids inventing a term from recall (it must research-then-propose).
- **Why:** an admitted gap beats a confident guess (`RED_LINES.md`). The whole tool's trustworthiness rests on provenance.

**L-002 — Preserve the source's sourcing discipline; keep it on its own axis.**
- **Invariant:** sourcing strength (`provenance.grounding_basis ∈ {grounded, unverified}`) is tracked separately from the rule-status axis (`established|contested`) and the glossary lifecycle axis (`locked-pending-calibration|provisional|locked`). A claim that is single-source / not-yet-verified-against-primary is `unverified`, regardless of its lifecycle status (e.g. G-013 is `locked` by calibration yet `unverified` in sourcing).
- **Guardrail:** `integrity_checks` I5 asserts the three axes use pairwise-disjoint vocabularies and every value sits on its own axis. The growth protocol appends as lifecycle `provisional` and routes to human calibration.
- **Why:** the word "established" must mean exactly one thing (rule status). Conflating sourcing with status let "established" read two ways (independent-review amendment, 2026-06-10).

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
- **Invariant:** compose the Arabic at full capability, label `awaiting-expert-judgment`, and consolidate every item needing the scholar's eye into ONE review list at delivery — never block mid-build, never self-certify as scholar-approved. The principal's acceptance flips `awaiting-expert-judgment`→`locked` (rules) and lifecycle `provisional`/`locked-pending-calibration`→`locked` (glossary).
- **Guardrail:** `arabic_review_status` field on every rule; the single `rendered/ARABIC_REVIEW_LIST.md`. (`RELIABILITY.md` §2.) Applied 2026-06-10: all items accepted as-is.

**L-010 — The opinion field is a structural lock; the watermark is a generation gate.**
- **Invariant:** the memo's Sharia opinion/ruling is reserved for a named human SSB member — its setter refuses all content (no code path fills it); every generated memo AND matrix carries the bilingual watermark or generation fails closed; contested matters render as a deferral section (positions + routing), never resolved.
- **Guardrail:** `memo_generator.OpinionField.set` raises; the orchestrator gate asserts the watermark on both renders; corpus-wide `pipeline/structural_tests.py` proves all three across the whole corpus.

**L-011 — The generation gate scans connective prose only; attributed text is exempt by construction.**
- **Invariant:** verbatim contract quotes, registry citations, and cited positions are attributed (exempt) and are never placed in the gated `generated_prose` bucket; only generator-/model-authored connective prose is gated for verdict language.
- **Guardrail:** `memo_generator`/`matrix_generator` keep `connective_*` and `attributed_*` separate; `never_rules_guard.check_prose` runs over connective only. See `FAULTS.md` F-004.

**L-008 — The "never rules" guarantee is an output guard, not a coding convention.**
- **Invariant:** the checker FLAGS/IDENTIFIES/CITES, never rules; no checker-authored field carries a verdict token, and status is never a permissibility word. Contested matters (R6/D1–D3) emit DEFERRAL only. Untrusted contract content is DATA, never instructions.
- **Guardrail:** `pipeline/never_rules_guard.py` (N1 status enum, N2 verdict-token scan of authored fields) run on every result by the orchestrator, fail closed; `pipeline/input_rail.py` (injection inert) with the inertness proof in `extractor_test`. See `FAULTS.md` F-003.
- **Why:** during the build the guard caught my own note saying "permissible". Vigilance is not a boundary; the wired guard is.

**L-009 — Arabic matching must normalise before it matches.**
- **Invariant:** Arabic cue detection strips tashkīl/tatweel and folds alef/ya/ta-marbuta/hamza before regex, and is negation-aware (explicit-negative pattern checked first), while quotes remain VERBATIM from the raw text.
- **Guardrail:** `pipeline/extractor._norm` + `_decide`; regression covered by `extractor_test.test_arabic_native_extraction_verbatim` (caught the "لا تُعَدّ إيراداً" false-positive and the diacritic-broken wa'd match during the build).

**L-012 — Breadth grows one grounded type at a time; honesty about non-coverage is load-bearing.**
- **Invariant:** Mizan covers only contract types with a grounded, calibrated rule-set (Murabaha, Ijara). It classifies structure (never rules), recognizes-but-does-not-cover (tawarruq → D3), and flags everything else out-of-scope; it never fabricates a rule, never applies one type's rules to another, never stays silent about an uncovered component. The scope registry is the single source of truth (README + memos read from it).
- **Guardrail:** `registry/scope_registry.json` + `pipeline/scope.py` (out_of_scope findings) + `contract_type_classifier` (fails to "unrecognized"). Proven by `stage2_structural_test.test_unrecognized_component_yields_out_of_scope_finding` + `test_tawarruq_recognized_not_covered_no_rule_applied`. New Ijara rules in a SEPARATE registry file so the locked Murabaha registry stays byte-identical.

**L-013 — Negation-first for violation cues; precedence for subset-structured types.**
- **Invariant:** when a violation phrase contains the affirmative cue ("no separate" contains "separate"), detect the violation first; when one covered type's cues are a structural subset of another type (tawarruq ⊃ commodity-murabaha), the more specific type takes precedence.
- **Guardrail:** `extractor` fusion-before-separation; `contract_type_classifier` tawarruq-precedence. See `FAULTS.md` F-005, F-006.

**L-007 — Each source sits on the layer that matches its authority TYPE.**
- **Invariant:** L1 = CBK/Higher Committee only; L2 = bank SSB fatwas (synthetic here); L3 = AAOIFI; LJ = Kuwaiti judicial practice (secular, secondary-publisher-reported). A source's layer must never overstate its authority kind.
- **Guardrail:** `integrity_checks` I6 (L1 ref must be CBK/Higher Committee) + `synthetic_corpus_guard` S3 (no non-L2 layer synthetic). See `FAULTS.md` F-002.
