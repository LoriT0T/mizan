#!/usr/bin/env bash
# Mizan full test suite — Stage 1a (registry validation) + Stage 1b (pipeline).
# Fails (non-zero) if anything is red. No network is touched.
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
fail=0

echo "================= STAGE 1a — registry validation ================="
( cd "$ROOT/validation" && python3 run_all.py ) || fail=1
echo
echo "--- 1a isolated unit tests ---"
for t in schema_validator_test integrity_checks_test citation_guard_test glossary_checks_test synthetic_corpus_guard_test; do
  ( cd "$ROOT/validation" && python3 -m unittest "$t" ) 2>&1 | tail -1 || fail=1
done
echo
echo "--- 1a fail-closed demo ---"
( cd "$ROOT/validation" && python3 demo_failclosed.py >/dev/null && echo "fail-closed demo OK" ) || fail=1

echo
echo "================= STAGE 1b — pipeline ================="
echo "--- 1b isolated unit tests ---"
for t in input_rail_test model_seam_test extractor_test never_rules_guard_test corpus_loader_test glossary_growth_test checker_test orchestrator_test; do
  ( cd "$ROOT/pipeline" && python3 -m unittest "$t" ) 2>&1 | tail -1 || fail=1
done
echo
echo "--- 1b pipeline smoke (NO-KEY, full corpus) ---"
( cd "$ROOT/pipeline" && python3 run_pipeline.py >/dev/null && echo "pipeline ran end-to-end OK" ) || fail=1

echo
echo "================= STAGE 1c — memo + matrix generation ================="
echo "--- 1c isolated + structural tests ---"
for t in memo_generator_test matrix_generator_test structural_tests; do
  ( cd "$ROOT/pipeline" && python3 -m unittest "$t" ) 2>&1 | tail -1 || fail=1
done
echo
echo "--- 1c generation smoke (NO-KEY, full corpus -> rendered/memos) ---"
( cd "$ROOT/pipeline" && python3 run_generate.py >/dev/null && echo "memo+matrix generation ran end-to-end OK" ) || fail=1

echo
echo "================= STAGE 2 — scope-awareness + Ijara ================="
echo "--- 2 isolated + structural tests ---"
for t in contract_type_classifier_test scope_test extractor_ijara_test checker_ijara_test stage2_structural_test; do
  ( cd "$ROOT/pipeline" && python3 -m unittest "$t" ) 2>&1 | tail -1 || fail=1
done

echo
echo "================= STAGE 3 — local frontend + GCC corpus ================="
echo "--- WALL: the engine suite passes with web/ ABSENT ---"
mv "$ROOT/web" "$ROOT/web_OFF" 2>/dev/null
( cd "$ROOT/pipeline" && python3 -m unittest checker_test orchestrator_test checker_ijara_test stage2_structural_test ) 2>&1 | tail -1 || fail=1
mv "$ROOT/web_OFF" "$ROOT/web" 2>/dev/null
echo "  (web/ restored)"
echo "--- web-layer tests (routes · wall · key-never-served · serve-time guard) ---"
( cd "$ROOT/web" && python3 -m unittest web_test ) 2>&1 | tail -1 || fail=1
echo "--- GCC corpus T1–T5 end-to-end (NO-KEY) ---"
( cd "$ROOT" && python3 run_stage3.py >/dev/null && echo "T1–T5 bundles written" ) || fail=1

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL GREEN (Stage 1a + Stage 1b + Stage 1c + Stage 2 + Stage 3)."
else
  echo "SUITE RED — see above."
fi
exit "$fail"
