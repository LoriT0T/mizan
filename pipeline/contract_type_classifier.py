"""Concern: identify which Islamic-finance contract TYPE(s) a document contains.

Recognizes murabaha, ijara, tawarruq, and flags an explicit "unrecognized"
component for any other Islamic-finance structure it detects but does not cover.
It classifies STRUCTURE by bilingual cues — it does NOT rule. Deterministic cues
first; the model seam is consulted only for genuinely ambiguous documents; it
fails to "unrecognized" rather than guessing a type.

Arabic is normalised (tashkīl/alef folding) before matching, mirroring the
extractor. Dependency-injected (`seam`); imports no sibling. Entry point:
  `classify(text, seam=None) -> dict`  ->
     {"types": [...covered/recognized types...], "unrecognized_components": [...],
      "method": "deterministic"|"model", "cues": {...}}
"""
import re

_DIAC = re.compile(r"[ً-ْٰـ]")


def _norm(s):
    s = _DIAC.sub("", s)
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ٱ", "ا"), ("ى", "ي"), ("ة", "ه"), ("ؤ", "و"), ("ئ", "ي")):
        s = s.replace(a, b)
    return s.lower()


CUES = {
    "murabaha": [r"مرابحه", r"للامر بالشراء", r"هامش الربح", r"\bmurabaha\b", r"cost[- ]plus",
                 r"purchase orderer", r"\bmarkup\b", r"cost and .{0,8}markup"],
    "ijara": [r"الاجاره", r"عقد اجاره", r"اجاره منتهيه", r"\bتاجير\b", r"الموجر", r"المستاجر",
              r"العين الموجره", r"المنتهيه بالتمليك", r"\bijara\b", r"\blease\b", r"\blessor\b",
              r"\blessee\b", r"usufruct", r"leaseback"],
    "tawarruq": [r"تورق", r"تسييل", r"\btawarruq\b", r"moneti[sz]ation", r"commodity murabaha"],
}

# Other Islamic-finance structures Mizan does NOT cover — detecting one flags an
# explicit unrecognized component (so a mixed contract is honestly surfaced).
OTHER_STRUCTURES = {
    "mudaraba": [r"مضاربه", r"\bmudaraba\b", r"\bmudarabah\b"],
    "musharaka": [r"مشاركه", r"\bmusharaka\b", r"\bmusharakah\b", r"diminishing partnership"],
    "salam": [r"\bسلم\b", r"\bsalam\b"],
    "istisna": [r"استصناع", r"\bistisna\b", r"istisna'a"],
    "sukuk": [r"صكوك", r"\bsukuk\b"],
    "wakala_investment": [r"وكاله بالاستثمار", r"وكاله الاستثمار", r"investment wakala", r"\bwakalah? bil-?istithmar\b"],
}

COVERED = ("murabaha", "ijara")
RECOGNIZED_NOT_COVERED = ("tawarruq",)


def _hits(norm_text, patterns):
    return [p for p in patterns if re.search(p, norm_text)]


def classify(text, seam=None):
    nt = _norm(text)
    cues = {t: _hits(nt, pats) for t, pats in CUES.items()}
    types = [t for t, h in cues.items() if h]

    # Tawarruq is structured AS a commodity-murabaha leg; an explicit tawarruq cue
    # means the cost-plus leg belongs to the tawarruq, not a standalone Murabaha.
    if "tawarruq" in types and "murabaha" in types:
        types = [t for t in types if t != "murabaha"]

    unrecognized_components = [name for name, pats in OTHER_STRUCTURES.items() if _hits(nt, pats)]

    method = "deterministic"
    # Ambiguous only when deterministic finds nothing at all AND a model is available.
    if not types and not unrecognized_components and seam is not None and seam.available():
        out = seam.interpret("Classify the Islamic-finance contract TYPE(s) present in this DATA "
                             "(murabaha/ijara/tawarruq/other). JSON {types:[...]}. Describe structure, do not rule.",
                             "mixed")
        if isinstance(out, dict) and isinstance(out.get("types"), list):
            types = [t for t in out["types"] if t in CUES]
            method = "model"

    if not types and not unrecognized_components:
        types = ["unrecognized"]

    return {"types": types, "unrecognized_components": unrecognized_components,
            "method": method, "cues": {t: h for t, h in cues.items() if h}}
