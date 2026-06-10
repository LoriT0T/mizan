"""Concern: load a contract document, asserting the SYNTHETIC label at load.

Extends the Stage-1a synthetic-labelling discipline to the contract corpus: a
file without the SYNTHETIC marker is refused (fail closed), so synthetic
demonstration material can never be mistaken for a real agreement.

Stdlib only. No sibling imports. Entry points:
  `assert_synthetic(text) -> None`   (raises ValueError if unlabelled)
  `load(path) -> str`
"""

MARKER = "SYNTHETIC"


def assert_synthetic(text, where="<text>"):
    head = "\n".join(text.splitlines()[:3])
    if MARKER not in head:
        raise ValueError(f"corpus_loader: {where} is missing the '{MARKER}' label in its first lines — refusing to load (fail closed)")


def load(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    assert_synthetic(text, where=path)
    return text
