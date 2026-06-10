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
    return os.path.basename(fn).replace(".txt", "")


def _corpus_paths():
    paths = []
    for d in (CORPUS, os.path.join(CORPUS, "stage2")):
        if os.path.isdir(d):
            paths += [os.path.join(d, fn) for fn in os.listdir(d) if fn.endswith(".txt")]
    return sorted(paths, key=os.path.basename)


def _find(fn):
    for d in (CORPUS, os.path.join(CORPUS, "stage2")):
        p = os.path.join(d, fn)
        if os.path.exists(p):
            return p
    return os.path.join(CORPUS, fn)


def run_all():
    os.makedirs(OUT, exist_ok=True)
    rules, defer, glossary = orchestrator.load_registry()
    for path in _corpus_paths():
        res = orchestrator.generate_for_contract(path, rules, defer, glossary)
        base = _slug(path)
        with open(os.path.join(OUT, base + ".memo.md"), "w", encoding="utf-8") as f:
            f.write(res["memo"]["render_md"])
        with open(os.path.join(OUT, base + ".matrix.md"), "w", encoding="utf-8") as f:
            f.write(res["matrix"]["render_md"])
        n_rows = len(res["matrix"]["rows"])
        print(f"  {base}.txt: memo + matrix written  [{res['seam_mode']}] · "
              f"matrix rows: {n_rows} · opinion placeholder: {res['memo']['opinion_is_placeholder']}")
    print(f"\nWrote bilingual memos + matrices to {OUT}")


def run_one(fn):
    res = orchestrator.generate_for_contract(_find(fn))
    print(res["memo"]["render_md"])
    print("\n\n" + "=" * 78 + "\n\n")
    print(res["matrix"]["render_md"])


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        run_one(sys.argv[1])
    else:
        run_all()
