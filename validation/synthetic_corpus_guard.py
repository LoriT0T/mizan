"""Concern: the synthetic L2 corpus is labelled synthetic — asserted at load.

In this demonstration the L2 layer (the institution's own SSB fatwas) is a
SYNTHETIC stand-in. It must never be mistakable for a real ruling. This guard
asserts, at load:
  S1  every L2 source has synthetic == True;
  S2  every L2 source's ref carries the explicit 'SYNTHETIC' label;
  S3  no L1 or L3 source is marked synthetic (real layers must not be flagged
      synthetic, and synthetic content must not masquerade as a real layer).

Stdlib only. No sibling imports. Entry point: `check(rules_data) -> list[str]`.
"""

LABEL = "SYNTHETIC"


def check(rules_data):
    errors = []
    for r in rules_data.get("rules", []):
        rid = r.get("id", "<no-id>")
        for i, s in enumerate(r.get("sources", [])):
            layer = s.get("layer")
            synthetic = s.get("synthetic", False)
            ref = s.get("ref", "")
            where = f"{rid}.sources[{i}]"
            if layer == "L2":
                if synthetic is not True:
                    errors.append(f"S1 {where}: L2 source must have synthetic == true")
                if LABEL not in ref and LABEL not in s.get("principle", ""):
                    errors.append(f"S2 {where}: L2 source must carry the '{LABEL}' label")
            elif layer in ("L1", "L3"):
                if synthetic is True:
                    errors.append(f"S3 {where}: {layer} source must not be marked synthetic")
    return errors
