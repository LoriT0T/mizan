"""Run the five GCC/Kuwait test contracts (corpus/stage3/) through the engine +
the web renderer, saving each result bundle (findings.json + memo.md + matrix.md
+ result.html) under rendered/stage3/ for the principal's review. NO-KEY by
default; uses the live seam if a key is present.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
sys.path.insert(0, os.path.join(ROOT, "web"))

import orchestrator
import views

CORPUS = os.path.join(ROOT, "corpus", "stage3")
OUT = os.path.join(ROOT, "rendered", "stage3")


def main():
    os.makedirs(OUT, exist_ok=True)
    cal = orchestrator.calibration_status()
    files = sorted(fn for fn in os.listdir(CORPUS) if fn.endswith(".txt"))
    for i, fn in enumerate(files, 1):
        text = open(os.path.join(CORPUS, fn), encoding="utf-8").read()
        res = orchestrator.generate_for_text(text, source_label=fn, seam=orchestrator.model_seam.make_seam())
        base = fn.replace(".txt", "")
        with open(os.path.join(OUT, base + ".memo.md"), "w", encoding="utf-8") as f:
            f.write(res["memo"]["render_md"])
        with open(os.path.join(OUT, base + ".matrix.md"), "w", encoding="utf-8") as f:
            f.write(res["matrix"]["render_md"])
        findings = [{k: v for k, v in fnd.items() if k != "citations"} | {"citations": fnd.get("citations", [])}
                    for fnd in res["findings"]]
        with open(os.path.join(OUT, base + ".findings.json"), "w", encoding="utf-8") as f:
            json.dump({"file": fn, "classification": res["classification"],
                       "covered_types": res["covered_types"], "seam_mode": res["seam_mode"],
                       "findings": findings}, f, ensure_ascii=False, indent=2)
        html, _ui = views.render_result(res, cal, f"r{i}")
        with open(os.path.join(OUT, base + ".result.html"), "w", encoding="utf-8") as f:
            f.write(html)
        summ = " ".join(f"{x['rule_id'] or 'OOS'}:{x['status'][:3]}" for x in res["findings"])
        print(f"  {fn}: [{res['seam_mode']}] types={res['classification']['types']} -> {summ}")
    print(f"\nWrote T1–T5 bundles (findings.json · memo.md · matrix.md · result.html) to {OUT}")


if __name__ == "__main__":
    main()
