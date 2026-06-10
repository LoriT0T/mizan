"""CLI: generate the memo + matrix for every corpus contract and write the
bilingual Markdown renders to rendered/memos/. Wiring only (delegates to
orchestrator). NO-KEY by default.

Usage:
  python3 run_generate.py            # generate all corpus contracts -> rendered/memos/
  python3 run_generate.py <file>     # print one contract's memo + matrix to stdout
"""
import os
import sys

import orchestrator

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS = os.path.join(ROOT, "corpus")
OUT = os.path.join(ROOT, "rendered", "memos")


def _slug(fn):
    return fn.replace(".txt", "")


def run_all():
    os.makedirs(OUT, exist_ok=True)
    rules, defer, glossary = orchestrator.load_registry()
    files = sorted(fn for fn in os.listdir(CORPUS) if fn.endswith(".txt"))
    for fn in files:
        res = orchestrator.generate_for_contract(os.path.join(CORPUS, fn), rules, defer, glossary)
        base = _slug(fn)
        with open(os.path.join(OUT, base + ".memo.md"), "w", encoding="utf-8") as f:
            f.write(res["memo"]["render_md"])
        with open(os.path.join(OUT, base + ".matrix.md"), "w", encoding="utf-8") as f:
            f.write(res["matrix"]["render_md"])
        n_rows = len(res["matrix"]["rows"])
        print(f"  {fn}: memo + matrix written  [{res['seam_mode']}] · matrix rows: {n_rows} · "
              f"opinion placeholder: {res['memo']['opinion_is_placeholder']}")
    print(f"\nWrote bilingual memos + matrices to {OUT}")


def run_one(fn):
    res = orchestrator.generate_for_contract(os.path.join(CORPUS, fn))
    print(res["memo"]["render_md"])
    print("\n\n" + "=" * 78 + "\n\n")
    print(res["matrix"]["render_md"])


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        run_one(sys.argv[1])
    else:
        run_all()
