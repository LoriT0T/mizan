# Mizan Murabaha Rule Registry — Rendered View
_Version 1.1.0-stage1a · scope: murabaha · DERIVED from `registry/rules.json` — do not hand-edit._
> **Mizan is a copilot, never a mufti.** It researches, drafts, and documents for a qualified human scholar (SSB); it never issues a ruling. Contested matters are surfaced, never adjudicated.
## Source layers
- **L1** — CBK instructions / Higher Committee of Shari'ah Supervision — binding in Kuwait, and L1 contains ONLY these. NOTE: CBK mandates the governance function and binds the bank to its SSB's fatwas and to external Sharia audit; it does not itself adjudicate the Sharia conformity of a given financing (Input #2, Part 3).
- **L2** — The institution's own SSB fatwas — binding per-bank. In this demonstration the L2 corpus is SYNTHETIC and is labelled synthetic on every entry; it stands in for a real bank's fatwa history and must never be read as an actual ruling.
- **L3** — AAOIFI Sharia Standards — persuasive reference in Kuwait (used by reference/influence, not a full legal mandate, unlike Bahrain/Qatar/Oman/UAE). Cited by standard number, topic, and publicly-documented principle ONLY; proprietary clause text is never reproduced.
- **LJ** — Kuwaiti judicial practice — binding court precedent in Kuwait, sitting OUTSIDE the three-tier Sharia-standards hierarchy: it is secular judicial enforcement, not a CBK instrument (L1), an SSB fatwa (L2), or an AAOIFI standard (L3). Cited via secondary publishers (e.g. Chambers Islamic Finance) that REPORT the practice, not via a primary court instrument; treat as binding-practice-as-reported, to be confirmed against primary judgments before production use.

> **Copyright boundary.** The full AAOIFI Sharia Standards text is copyrighted and sold by AAOIFI. This registry references structure, standard numbers, topic coverage, and widely-cited public principles only. Clause-level verification against purchased AAOIFI texts is a required step before any real-world use.

> **Language authority.** Arabic is the canonical side; English is the parallel rendering. For Sharia pronouncements and onshore Kuwaiti instruments the Arabic prevails (Input #2, Part 3).

---

## R1 — Ownership and possession before resale  ·  🟢 established
**العنوان:** التملّك والقبض قبل إعادة البيع

**Arabic (canonical):**

> يجب أن تتملّك المؤسسةُ الأصلَ تملّكاً حقيقياً وتقبضه قبضاً حقيقياً أو حكمياً، فتتحمّل تبعةَ هلاكه ومخاطرَ ملكيته ولو يسيراً من الزمن، قبل بيعه للعميل؛ فلا يصحّ أن تبيع المؤسسةُ ما لم تملكه وتقبضه.

**English (parallel):**

> The institution must take genuine ownership of the asset and take actual or constructive possession of it — thereby bearing the risk of its loss and the risks of its ownership, even if only for a short time — before selling it to the customer; the institution may not sell what it has not owned and possessed.

_Arabic review status: **locked** · provenance: Input #2, Part 2 (Murabaha conditions a/b; red flags) + Recommendations Stage 1 check (1) · grounding: grounded_

**What satisfies it:**
- The institution buys the asset from the supplier, records it in its ownership, and bears the risk of loss before contracting the sale with the customer.
  - شراء المؤسسة الأصلَ من المورّد وقيدُه في ملكها وتحمّلها تبعةَ الهلاك قبل عقد البيع مع العميل.
- Actual possession (physical receipt) or constructive possession (enablement/clearing of the asset and transfer of risk) is established before resale.
  - ثبوت القبض الحقيقي (التسلّم) أو الحكمي (التمكين والتخلية ونقل التبعة) قبل إعادة البيع.

**What violates it (concrete contract patterns):**
- The bank pays the supplier on the customer's behalf while the customer acts as buying agent, so the bank never bears ownership risk (the single most common defect — converts the transaction into a disguised interest loan).
  - أن يدفع المصرفُ الثمنَ للمورّد نيابةً عن العميل بينما يتصرّف العميل وكيلاً بالشراء، فلا يتحمّل المصرفُ مخاطرَ الملكية أصلاً (وهو أشيع صور الخلل، ويحوّل العمليةَ إلى قرض بفائدة مستتر).
- Executing the sale to the customer before the bank takes title and possession (sale before possession / bai' qabl al-qabd).
  - تنفيذ بيع الأصل للعميل قبل أن يقبضه المصرفُ ويملكه (بيع قبل القبض).

**Sources (layer · citation · principle):**
- **LJ** — Kuwaiti judicial practice — reported in Chambers Islamic Finance 2025 (Kuwait), a secondary publisher
  - _Kuwaiti courts will not endorse artificial Murabaha and require proof the bank actually acquired the asset prior to its resale to the customer (binding court practice as reported; confirm against primary judgments before production)._
- **L1** — CBK Circular 2/IBS/369/2016
  - _Governance frame: the SSB inspects all contracts and its fatwas (which encode this condition) are binding on the bank; management is responsible for Sharia compliance._
- **L3** — AAOIFI Sharia Standard No. 8 (Murabaha); No. 18 (Possession / Qabd)
  - _Acquisition-and-possession requirement: the institution must own and possess the asset, bearing ownership risk, before reselling._
- **L2** · **SYNTHETIC** — SYNTHETIC SSB fatwa SSB-SYNTH-MUR-001
  - _Demonstration bank fatwa affirming that no Murabaha sale may precede the bank's documented acquisition and risk-bearing. SYNTHETIC — not a real ruling._

_Note: The doctrinal basis is qabd-before-resale and al-kharaj bil-daman (entitlement to return requires bearing ownership risk)._

---

## R2 — Disclosure of cost and markup; price fixed  ·  🟢 established
**العنوان:** الإفصاح عن التكلفة والربح وتثبيت الثمن

**Arabic (canonical):**

> يجب الإفصاحُ للعميل عن ثمن التكلفة وهامش الربح إفصاحاً تامّاً، وأن يكون الثمنُ — وهو التكلفة مضافاً إليها الربحُ — وجدولُ الأقساط محدَّداً مثبَّتاً عند العقد، فلا يتغيّر بعد إبرامه.

**English (parallel):**

> The cost price and the profit markup must be fully disclosed to the customer, and the price — cost plus profit — together with the instalment schedule must be determined and fixed at contract, not changing after conclusion.

_Arabic review status: **locked** · provenance: Input #2, Part 2 (Murabaha conditions c/d) · grounding: grounded_

**What satisfies it:**
- The actual cost and the profit markup are stated explicitly in the contract, and the total price and instalment terms remain fixed through to settlement.
  - بيانُ التكلفة الفعلية وهامش الربح صراحةً في العقد، وثباتُ مجموع الثمن وآجال الأقساط حتى السداد.

**What violates it (concrete contract patterns):**
- Concealing the cost or the markup — which turns the transaction into a musawamah, not a Murabaha.
  - إخفاء التكلفة أو الربح، فتؤول العمليةُ إلى مساومة لا مرابحة.
- Tying the price or markup to a variable index after contract, or re-pricing it later.
  - ربطُ الثمن أو الربح بمؤشّر متغيّر بعد العقد أو إعادةُ تسعيره لاحقاً.

**Sources (layer · citation · principle):**
- **L1** — CBK Circular 2/IBS/369/2016
  - _Governance frame: the bank is bound by its SSB's fatwa requiring disclosure and price certainty._
- **L3** — AAOIFI Sharia Standard No. 8 (Murabaha) — conditions of the contract and the price
  - _Full disclosure of cost and markup distinguishes Murabaha from musawamah; price and markup are determined and fixed at contract._
- **L2** · **SYNTHETIC** — SYNTHETIC SSB fatwa SSB-SYNTH-MUR-002
  - _Demonstration bank fatwa requiring written disclosure of cost and profit and prohibiting post-contract re-pricing. SYNTHETIC — not a real ruling._

_Note: Disclosure is the defining feature separating Murabaha (cost-plus, disclosed) from musawamah (cost not disclosed)._

---

## R3 — The asset exists and is permissible  ·  🟢 established
**العنوان:** وجود الأصل وإباحته

**Arabic (canonical):**

> يجب أن يكون الأصلُ محلَّ المرابحة موجوداً مملوكاً معيَّناً، وأن يكون مالاً متقوَّماً مباحاً شرعاً؛ فلا تصحّ المرابحةُ في محرَّمٍ ولا في معدوم.

**English (parallel):**

> The asset subject to the Murabaha must exist, be owned, and be specified, and must be lawful (halal) property of value; a Murabaha is valid neither in a prohibited thing nor in a non-existent one.

_Arabic review status: **locked** · provenance: Input #2, Part 2 (Murabaha condition a; red flag 'pure cash needs') · grounding: grounded_

**What satisfies it:**
- A specified, existing asset of permissible use (e.g. a car, real estate, a commodity) that can be owned and possessed.
  - تعيينُ أصلٍ قائمٍ مباحِ المنفعة (كسيّارة أو عقار أو سلعة)، يمكن تملّكه وقبضه.

**What violates it (concrete contract patterns):**
- Financing a prohibited good or activity (e.g. alcohol, pork, conventional interest-based financial services).
  - تمويلُ سلعةٍ أو نشاطٍ محرَّم (كالخمر أو لحم الخنزير أو الخدمات المالية الربوية).
- Using Murabaha for pure cash needs (salaries, utility bills, general liquidity) with no real underlying asset purchase.
  - استعمالُ المرابحة لحاجات نقدية بحتة (رواتب، فواتير، سيولة عامّة) دون شراء أصلٍ حقيقي.

**Sources (layer · citation · principle):**
- **L1** — CBK Circular 2/IBS/369/2016
  - _Governance frame: the bank is bound by its SSB's fatwa restricting Murabaha to existing, permissible assets._
- **L3** — AAOIFI Sharia Standard No. 8 (Murabaha)
  - _The asset must exist and be permissible (halal) to be a valid subject of Murabaha._
- **L2** · **SYNTHETIC** — SYNTHETIC SSB fatwa SSB-SYNTH-MUR-003
  - _Demonstration bank fatwa confirming the asset must be existing, identified and Sharia-permissible. SYNTHETIC — not a real ruling._

_Note: Roots in the prohibition of haram subject matter and the bar on selling the non-existent (gharar)._

---

## R4 — The asset is not already the customer's (bar on bai' al-inah)  ·  🟢 established
**العنوان:** ألّا يكون الأصلُ مملوكاً للعميل أصلاً (منع بيع العِينة)

**Arabic (canonical):**

> يجب ألّا يكون الأصلُ محلَّ المرابحة مملوكاً للعميل قبل العقد ولا عائداً إليه بإعادة شرائه منه؛ فإن بيعَ الأصلِ ثمّ إعادةَ شرائه من العميل يقع في بيع العِينة الممنوع في دول الخليج.

**English (parallel):**

> The asset must not be owned by the customer before the contract, nor return to him by being bought back from him; selling the asset and then repurchasing it from the customer falls into bai' al-inah, which is prohibited across the GCC.

_Arabic review status: **locked** · provenance: Input #2, Part 2 (Murabaha condition e; red flag 'customer's own property') · grounding: grounded_

**What satisfies it:**
- The asset's source is a third party (the supplier), not the customer, and the asset does not return to its original seller by prior arrangement.
  - أن يكون مصدرُ الأصل طرفاً ثالثاً (المورّد) لا العميلَ نفسه، وألّا يعود الأصلُ إلى بائعه الأصلي باتفاق مسبق.

**What violates it (concrete contract patterns):**
- The bank buys the asset from the customer then resells it back to him at a higher deferred price (bai' al-inah / sale-and-buyback).
  - شراءُ المصرف الأصلَ من العميل ثمّ إعادةُ بيعه له بثمنٍ مؤجّلٍ أعلى (بيع العِينة).

**Sources (layer · citation · principle):**
- **L1** — GCC prohibition of bai' al-inah; CBK Circular 2/IBS/369/2016 governance frame
  - _bai' al-inah is widely prohibited across the GCC; the bank is bound by its SSB's fatwa rejecting it._
- **L3** — AAOIFI Sharia Standard No. 8 (Murabaha)
  - _The asset must not already belong to the customer — otherwise the structure collapses into prohibited bai' al-inah._
- **L2** · **SYNTHETIC** — SYNTHETIC SSB fatwa SSB-SYNTH-MUR-004
  - _Demonstration bank fatwa prohibiting purchase-then-resale to the same customer. SYNTHETIC — not a real ruling._

↪ **Contested / cross-listed in the defer register:** D2

_Note: The boundary between an acceptable structure and bai' al-inah has genuine ambiguities — registered in the defer register (see defer_ref)._

---

## R5 — Late-payment charge to charity, never income; no markup increase  ·  🟢 established
**العنوان:** غرامةُ التأخّر للخير لا للإيراد، ومنعُ زيادة الربح

**Arabic (canonical):**

> لا يجوز زيادةُ هامش الربح أو الثمن عند تأخّر العميل في السداد؛ وإن اشتُرطت غرامةٌ على المماطلة فيجب صرفُها في وجوه الخير، ولا تُعَدّ إيراداً للمؤسسة.

**English (parallel):**

> It is not permissible to increase the profit markup or the price upon the customer's late payment; and if a penalty for delay is stipulated, it must be disbursed to charitable causes and must not be counted as income of the institution.

_Arabic review status: **locked** · provenance: Input #2, Part 2 (red flag 'markup re-priced on late payment'); Part 4 KFH late-penalty rectification example · grounding: grounded_

**What satisfies it:**
- The price stays fixed on delay, and any late-payment penalty is channelled to a documented charity, not to the bank's income.
  - ثباتُ الثمن عند التأخّر، وتوجيهُ أيّ غرامةِ مماطلةٍ إلى جهةٍ خيرية موثّقة لا إلى إيراد المصرف.

**What violates it (concrete contract patterns):**
- Re-pricing or increasing the markup on late payment (replicates compounding interest).
  - إعادةُ تسعير الربح أو زيادتُه عند التأخّر (محاكاةٌ للفائدة المركّبة).
- Retaining the late-payment penalty as bank income instead of disbursing it to charity.
  - احتجازُ غرامة التأخّر إيراداً للمصرف بدل صرفها في الخير.

**Sources (layer · citation · principle):**
- **L1** — CBK Circular 2/IBS/369/2016
  - _Governance frame: the bank is bound by its SSB's fatwa on late-payment treatment; external Sharia audit tests it._
- **L3** — AAOIFI Sharia Standard No. 8 (Murabaha) — default / late-payment treatment
  - _The markup may not increase on default; any late-payment charge is directed to charity, not income._
- **L2** · **SYNTHETIC** — SYNTHETIC SSB fatwa SSB-SYNTH-MUR-005
  - _Demonstration bank fatwa, mirroring widely-reported GCC SSB practice, directing late-payment penalties to charity and barring markup increase. SYNTHETIC — not a real ruling._

_Note: Penalty-to-charity is the standard remedy that prevents a late charge from becoming riba._

---

## R6 — The promise (wa'd) structure in MPO — contested  ·  🟠 contested
**العنوان:** بنيةُ الوعد (الوعد بالشراء) في المرابحة للآمر بالشراء — مسألة خلافية

**Arabic (canonical):**

> في المرابحة للآمر بالشراء، مسألةُ إلزام الوعد بالشراء محلُّ خلافٍ معتبر بين الجهات العلمية: فبينما يُمنع الوعدُ الثنائي الملزم (إذ يؤول إلى عقدٍ مؤجَّلِ العوضين)، يجوز عند بعضهم إلزامُ الوعد الأحادي. لا يبتّ النظامُ في هذه المسألة، بل يَعرض المواقفَ المنسوبةَ إلى مصادرها ويحيلها إلى الهيئة الشرعية للبتّ.

**English (parallel):**

> In Murabaha to the Purchase Orderer, the bindingness of the promise to purchase is a matter of considerable disagreement among scholarly bodies: while a mutually binding (bilateral) promise is impermissible (it amounts to a contract with both counter-values deferred), some hold a unilateral promise may be made binding. The system does not adjudicate this; it presents the positions attributed to their sources and refers the matter to the SSB.

_Arabic review status: **locked** · provenance: Input #2, Part 2 (Murabaha 'Scholarly disagreement'); Recommendations Stage 1 check (6) 'flag, don't adjudicate' · grounding: grounded_

**What satisfies it:**
- Presenting both bodies' positions (AAOIFI and the OIC International Islamic Fiqh Academy) attributed to source, and referring the determination of bindingness to the bank's SSB.
  - عرضُ موقفَي الجهتين (هيئة المحاسبة والمراجعة AAOIFI، ومجمع الفقه الإسلامي الدولي) منسوبَين إلى مصدرهما، وإحالةُ تحديد حكم الإلزام إلى الهيئة الشرعية للمصرف.

**What violates it (concrete contract patterns):**
- The system deciding the bindingness of the promise on its own, or treating a bilateral binding promise as the sale itself — which removes the bank's ownership-risk window.
  - أن يبتّ النظامُ في إلزام الوعد من تلقاء نفسه، أو أن يُعامَل الوعدُ الثنائي الملزم وكأنه البيعُ نفسه فتُلغى نافذةُ تحمّل المصرف لمخاطر الملكية.

**Sources (layer · citation · principle):**
- **L3** — AAOIFI Sharia Standard No. 8 (Murabaha) — procedures preceding the contract (the promise and its bindingness)
  - _The preliminary arrangement must not include a mutually binding bilateral promise; a unilateral promise may be made binding._
- **L3** — OIC International Islamic Fiqh Academy — resolutions on the promise (wa'd) in Murabaha to the Purchase Orderer
  - _A promise is morally binding, and legally binding where it is conditional and the promisee has incurred expense._
- **L2** · **SYNTHETIC** — SYNTHETIC SSB fatwa SSB-SYNTH-MUR-006
  - _Demonstration bank fatwa electing one position on wa'd bindingness as a configurable, SSB-determined parameter. SYNTHETIC — not a real ruling._

↪ **Contested / cross-listed in the defer register:** D1

_Note: Status: contested. Bindingness is a configurable, SSB-determined parameter — never adjudicated by the tool. Cross-listed in the defer register._

---
