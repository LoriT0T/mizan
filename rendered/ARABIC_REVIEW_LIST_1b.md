# قائمة المراجعة العربية الموحَّدة — Stage 1b — Consolidated Arabic Review List

> **For the principal (qualified native-Arabic scholar).** Per the expert-calibration principle (`RELIABILITY.md` §2): this is ONE consolidated list at the 1b checkpoint, not mid-build interruptions. Your native-Arabic judgment is the final calibration layer.

## A. No new *canonical* registry Arabic or glossary terms were locked in Stage 1b
Stage 1b is code (extractor + checker) over the **already-locked** registry (rules v1.1.0, glossary v1.2.0). It composed **no** new canonical rule text and locked **no** new glossary terms.
- All checker finding **templates / notes are English** (e.g. "Flagged for the qualified scholar (SSB); this is an identification, not a ruling."), by design — they carry no Sharia verdict.
- All Arabic that appears in a finding's `quote` field is **verbatim from the contract**, and all Arabic in a deferral's `positions` is **verbatim from the already-reviewed registry/defer entries** — nothing newly composed.
- The glossary **growth protocol** wired into 1b produces only `provisional` candidates routed here; **none were created** during this build (the corpus uses already-seeded terms). If a future run proposes one, it will appear in this list as `provisional / unverified` for your calibration.

## B. New Arabic I authored as TEST FIXTURES (for your optional eyeballing — not canonical, not locked)
These are synthetic contract texts under `corpus/`, clearly labelled SYNTHETIC. They are demonstration data, not terminology of record, so they need no "locking" — but since I composed the Arabic, here it is for your eye:

1. **`corpus/contract_clean_ar.txt`** — a clean Murabaha contract in MSA (acquisition+possession, disclosed cost/markup, late-charge-to-charity, unilateral wa'd, clean ownership history).
2. **`corpus/contract_r1_agency_ar.txt`** — seeded R1 defect: *"يدفع المصرفُ الثمنَ للمورّد نيابةً عن العميل بينما يتصرّف العميلُ وكيلاً بالشراء، فلا يتحمّل المصرفُ مخاطرَ الملكية ولا يقبض الأصل…"*
3. **`corpus/contract_r4_inah_ar.txt`** — seeded R4 (bai' al-inah) defect: *"يشتري المصرفُ الأصلَ من العميل نفسه ثم … أعاد بيعه له"* / *"كان مملوكاً للعميل قبل المعاملة"*.

- **Your call:** ✅ the synthetic Arabic reads correctly for its purpose · ✏️ amend any phrasing · ❓ flag. (These do not gate the registry; they only make the Arabic-extraction demonstration faithful.)

## C. Confirmation of discipline
- Arabic is read **natively** and quoted **verbatim** (normalisation is applied only to the matching copy, never to the stored quote).
- The checker **never rules**; contested matters defer to you; the never-rules guard fails closed on any verdict language — it caught one of my own notes during the build (see `FAULTS.md` F-003).

_Nothing in this list changes the locked registry. Returning it is optional for Stage 1b; it is provided for transparency and your calibration of the synthetic Arabic._
