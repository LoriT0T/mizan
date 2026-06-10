# قائمة المراجعة العربية الموحَّدة — Consolidated Arabic Review List

> **✅ CALIBRATED — 2026-06-10.** The principal accepted ALL items below as-is: R1–R6 canonical texts, seed glossary G-001…G-012, and provisional G-013. Statuses were flipped to `locked`; the glossary was versioned to v1.2.0; the suite re-ran green. This document is retained as the record of what was reviewed and the grounding/alternatives behind each item.


> **For the principal (qualified native-Arabic scholar).** Per the foundation's expert-calibration principle (`RELIABILITY.md` §2): the Arabic below was composed at full capability, natively in formal MSA (not translated from English), and grounded in the two inputs + the public sources cited. It is **not** self-certified. Every item is labelled `awaiting-expert-judgment` / `provisional`. Your native-Arabic and domain judgment is the **final calibration layer** — your calibration flips these to `locked`. This is one consolidated list at delivery, not scattered mid-build interruptions.
>
> **Scope of your review:** wording, fiqh precision, and term-of-art choice. This does **not** ask you to adjudicate any contested matter (R6 / D1–D3 remain deferred to the SSB by design).

**How to use this list:** for each item — ✅ accept · ✏️ amend (write your preferred form) · ❓ flag for discussion.

---

## Part A — Canonical Arabic rule texts (R1–R6)

### R1 — التملّك والقبض قبل إعادة البيع
> يجب أن تتملّك المؤسسةُ الأصلَ تملّكاً حقيقياً وتقبضه قبضاً حقيقياً أو حكمياً، فتتحمّل تبعةَ هلاكه ومخاطرَ ملكيته ولو يسيراً من الزمن، قبل بيعه للعميل؛ فلا يصحّ أن تبيع المؤسسةُ ما لم تملكه وتقبضه.

- **Grounding:** Input #2 Part 2 (Murabaha conditions a/b; red flag "no genuine ownership/possession"); doctrine of *qabd* before resale and *al-kharaj bil-daman*.
- **Choices I weighed:** used **القبض** (the fiqh term of art, pairing with القبض الحقيقي/الحكمي) over الحيازة/التسلّم; kept **"ولو يسيراً من الزمن"** to encode the report's "even for a very short time"; **تبعة الهلاك** for ownership risk. Alternative considered: "وتدخل في ضمانها" instead of "فتتحمّل تبعةَ هلاكه".

### R2 — الإفصاح عن التكلفة والربح وتثبيت الثمن
> يجب الإفصاحُ للعميل عن ثمن التكلفة وهامش الربح إفصاحاً تامّاً، وأن يكون الثمنُ — وهو التكلفة مضافاً إليها الربحُ — وجدولُ الأقساط محدَّداً مثبَّتاً عند العقد، فلا يتغيّر بعد إبرامه.

- **Grounding:** Input #2 Part 2 (Murabaha conditions c/d); disclosure distinguishes Murabaha from musawamah.
- **Choices I weighed:** **هامش الربح** (per prompt seed) over نسبة الربح / الزيادة; **محدَّداً مثبَّتاً** to carry both "determined" and "fixed". Alternative: "معلوماً مقطوعاً به".

### R3 — وجود الأصل وإباحته
> يجب أن يكون الأصلُ محلَّ المرابحة موجوداً مملوكاً معيَّناً، وأن يكون مالاً متقوَّماً مباحاً شرعاً؛ فلا تصحّ المرابحةُ في محرَّمٍ ولا في معدوم.

- **Grounding:** Input #2 Part 2 (condition a); Part 1 (haram subject matter; bar on selling the non-existent).
- **Choices I weighed:** **مالاً متقوَّماً** (property of recognised value — precise fiqh term) added to **مباحاً شرعاً**; the closing **"في محرَّمٍ ولا في معدوم"** mirrors two distinct defects (impermissible vs non-existent). Alternative: drop متقوَّماً for plainer "مالاً مباحاً".

### R4 — ألّا يكون الأصلُ مملوكاً للعميل أصلاً (منع بيع العِينة)
> يجب ألّا يكون الأصلُ محلَّ المرابحة مملوكاً للعميل قبل العقد ولا عائداً إليه بإعادة شرائه منه؛ فإن بيعَ الأصلِ ثمّ إعادةَ شرائه من العميل يقع في بيع العِينة الممنوع في دول الخليج.

- **Grounding:** Input #2 Part 2 (condition e; red flag "customer's own property"); GCC prohibition of bai' al-inah.
- **Choices I weighed:** spelled out both forms (already-owned **and** buy-back) since the report flags both; **يقع في بيع العِينة** as the consequence. Note the boundary itself is contested → routed to **D2** (I did not encode a sharp line, by design).

### R5 — غرامةُ التأخّر للخير لا للإيراد، ومنعُ زيادة الربح
> لا يجوز زيادةُ هامش الربح أو الثمن عند تأخّر العميل في السداد؛ وإن اشتُرطت غرامةٌ على المماطلة فيجب صرفُها في وجوه الخير، ولا تُعَدّ إيراداً للمؤسسة.

- **Grounding:** Input #2 Part 2 (red flag "markup re-priced on late payment"); Part 4 (KFH late-penalty rectification — penalty-to-charity practice).
- **Choices I weighed:** **المماطلة** (the fiqh framing of culpable delay) for "late payment"; **وجوه الخير** for charity over الصدقة / أوجه البِرّ; explicit **"ولا تُعَدّ إيراداً"** to bar income recognition. Alternative: "تُصرَف في وجوه البِرّ والإحسان".

### R6 — بنيةُ الوعد في المرابحة للآمر بالشراء — مسألة خلافية (CONTESTED)
> في المرابحة للآمر بالشراء، مسألةُ إلزام الوعد بالشراء محلُّ خلافٍ معتبر بين الجهات العلمية: فبينما يُمنع الوعدُ الثنائي الملزم (إذ يؤول إلى عقدٍ مؤجَّلِ العوضين)، يجوز عند بعضهم إلزامُ الوعد الأحادي. لا يبتّ النظامُ في هذه المسألة، بل يَعرض المواقفَ المنسوبةَ إلى مصادرها ويحيلها إلى الهيئة الشرعية للبتّ.

- **Grounding:** Input #2 Part 2 (Murabaha — Scholarly disagreement); Recommendations Stage 1 check (6) "flag, don't adjudicate". Positions detailed in **D1**.
- **Choices I weighed:** framed R6 as a **rule about deferral** (the tool's behaviour), not a fiqh ruling; **عقدٍ مؤجَّلِ العوضين** to render "a contract with both counter-values deferred". I deliberately did **not** assert which view is correct. Please check the rendering of "bilateral binding promise" = **الوعد الثنائي الملزم** and "unilateral" = **الأحادي** (alt: المنفرد).

---

## Part B — Seed glossary renderings (G-001 … G-012, locked-pending-calibration)

| ID | Arabic (canonical) | English (canonical) | Alternative I considered |
|---|---|---|---|
| G-001 | المرابحة | Murabaha | — (transliteration standard) |
| G-002 | القبض الحقيقي | actual (physical) possession | القبض الفعلي |
| G-003 | القبض الحكمي | constructive possession | القبض التقديري |
| G-004 | الوعد الملزم | binding promise (wa'd mulzim) | الوعد المُلزِم (diacritic) |
| G-005 | بيع العينة | bai' al-inah (sale-and-buyback) | بيع العِينة (with kasra) |
| G-006 | هامش الربح | profit markup | نسبة الربح / الربح المضاف |
| G-007 | الذمة | dhimmah (liability / debt obligation) | الذمّة المالية |
| G-008 | الربا | riba (usury / interest) | — |
| G-009 | الغرر | gharar (excessive uncertainty) | — |
| G-010 | بيع المساومة | musawamah (bargaining sale) | المساومة |
| G-011 | البيع المؤجّل | deferred-payment sale (bai' muajjal) | بيع التقسيط / بيع الأجل |
| G-012 | التورق المنظّم | organized tawarruq | التورّق المصرفي (out-of-scope marker) |

**Note on diacritics:** the canonical forms are stored without full tashkīl for matching robustness; where a kasra/ḍamma changes the term of art (e.g. العِينة), please confirm the intended reading.

---

## Part C — Growth-protocol provisional entry (status: provisional → your calibration locks it)

### G-013 · بيع التولية — tawliyah (sale at cost)
> **AR:** بيعٌ بثمنٍ يساوي تكلفةَ الاقتناء دون زيادةٍ ولا ربح، مع الإفصاح التامّ عن التكلفة؛ أحدُ بيوع الأمانة الثلاثة إلى جانب المرابحة (تكلفة + ربح) والوضيعة (بيعٌ بخسارة).
> **EN:** A sale at a price equal to the acquisition cost with no markup or profit, with full cost disclosure; one of the three trust sales (buyu' al-amanah) alongside Murabaha (cost + profit) and wadiah (sale at a loss).

- **How it got here:** demonstration of the **growth protocol** end-to-end — an unseeded term was encountered, researched on demand against public authoritative sources, proposed as a bilingual entry, and appended as `provisional`, then routed here.
- **Grounding (fetched, cited):** Fincyclopedia "Tawliyah" (par-value/at-cost sale, full disclosure, no markup); Ijara CDC glossary "Bayu al-amanah" (three trust sales: murabaha / tawliyah / wadiah); Wikipedia "Murabaha" (trust sales requiring honest cost declaration).
- **Choices I weighed:** **بيع التولية** as the headword (vs التولية alone); English headword **tawliyah (sale at cost)** vs "cost-price sale"; mentioned the sister term **الوضيعة / wadiah** in the definition for placement, but did **not** auto-seed it (only the encountered term is appended).
- **Your call:** ✅ lock as-is · ✏️ amend the Arabic/English · ❓ discuss whether الوضيعة should also be added.

---

_When you return this list, your acceptances/amendments are applied to `registry/rules.json` and `registry/glossary.json`, statuses flip `awaiting-expert-judgment`/`provisional` → `locked`, the validation suite re-runs (must stay green), and the glossary history appends a new version. Only then does Stage 1a close and Stage 1b (extractor + checker) become authorized._
