# Mizan Terminology Glossary — Rendered View
_Version 1.3.0-stage2 · DERIVED from `registry/glossary.json` — do not hand-edit._

> **Discipline.** Exactly ONE canonical Arabic form (the canonical side) and ONE canonical English rendering per term. The glossary must never silently contain two renderings of one term. A term is never invented from recall without a fetched, cited grounding. Append-only in history. Two independent axes (never conflated): lifecycle 'status' (locked-pending-calibration -> provisional -> locked) tracks human calibration; provenance 'grounding_basis' (grounded | unverified) tracks sourcing strength.

## Growth protocol

_The documented procedure every future component invokes on encountering an Islamic-finance term of art NOT in the glossary._

- (a) research the term on demand against public authoritative sources
- (b) propose a bilingual entry with its grounding cited
- (c) append with status: provisional — usable immediately, but routed into the principal's consolidated review list at the next checkpoint; his calibration flips it to locked
- (d) validation: no entry may conflict with a locked (or locked-pending-calibration) rendering; collisions fail closed and surface for human resolution; the glossary is versioned and append-only in history

---

## Entries

### Seed terms (status: locked-pending-calibration)

| ID | Arabic (canonical) | English (canonical) | Status | Grounding basis | Sources |
|---|---|---|---|---|---|
| G-001 | المرابحة | Murabaha | locked | grounded | Input #2, Part 2 (Murabaha) |
| G-002 | القبض الحقيقي | actual (physical) possession | locked | grounded | Input #2, Part 1 (qabd); Part 2 (Murabaha condition b) |
| G-003 | القبض الحكمي | constructive possession | locked | grounded | Input #2, Part 2 (Murabaha condition b — actual or constructive possession) |
| G-004 | الوعد الملزم | binding promise (wa'd mulzim) | locked | grounded | Input #2, Part 2 (Murabaha — wa'd) |
| G-005 | بيع العينة | bai' al-inah (sale-and-buyback) | locked | grounded | Input #2, Part 2 (Murabaha condition e); Caveats |
| G-006 | هامش الربح | profit markup | locked | grounded | Input #2, Part 2 (Murabaha conditions c/d) |
| G-007 | الذمة | dhimmah (liability / debt obligation) | locked | grounded | Input #2, Part 2 (Murabaha — deferred sale price as a debt); Tawarruq (financial obligation) |
| G-008 | الربا | riba (usury / interest) | locked | grounded | Input #2, Part 1 (Riba) |
| G-009 | الغرر | gharar (excessive uncertainty) | locked | grounded | Input #2, Part 1 (Gharar) |
| G-010 | بيع المساومة | musawamah (bargaining sale) | locked | grounded | Input #2, Part 2 (Murabaha condition c — distinguished from musawamah) |
| G-011 | البيع المؤجّل | deferred-payment sale (bai' muajjal) | locked | grounded | Input #2, Part 2 (Murabaha mechanics — bai' muajjal) |
| G-012 | التورق المنظّم | organized tawarruq | locked | grounded | Input #2, Part 2 (Tawarruq) |

### Growth-protocol terms

| ID | Arabic (canonical) | English (canonical) | Status | Grounding basis | Sources |
|---|---|---|---|---|---|
| G-013 | بيع التولية | tawliyah (sale at cost) | locked | unverified | Fincyclopedia, 'Tawliyah' (fincyclopedia.net/islamic-finance/t/tawliyah) — par-value/at-cost sale, full cost disclosure, no markup; Ijara CDC glossary, 'Bayu al-amanah' (ijaracdc.com) — three trust sales: murabaha, tawliyah, wadiah; Wikipedia, 'Murabaha' — murabaha as one of three buyu' al-amanah requiring honest cost declaration |
| G-014 | الإجارة | Ijara (leasing) | provisional | grounded | Input #3, Part 1 + TL;DR |
| G-015 | المنفعة | usufruct (manfa'ah) | provisional | grounded | Input #3, Part 1 |
| G-016 | الإجارة المنتهية بالتمليك | Ijara Muntahia Bittamleek (lease-to-own) | provisional | grounded | Input #3, Part 1 + Key Findings 1/4 |
| G-017 | العين المؤجَّرة | the leased asset | provisional | grounded | Input #3, Part 2 (I1) |
| G-018 | الأجرة | rent (ujrah) | provisional | grounded | Input #3, Part 2 (I2) |
| G-019 | الصيانة الأساسية | basic (structural) maintenance | provisional | grounded | Input #3, Part 2 (I4) |
| G-020 | الصيانة التشغيلية | operational maintenance | provisional | grounded | Input #3, Part 2 (I4) |
| G-021 | التكافل | takaful (Islamic cooperative insurance) | provisional | grounded | Input #3, Part 2 (I4) |
| G-022 | البيع مع الاستئجار | sale-and-leaseback | provisional | grounded | Input #3, Part 2 (I7) |

### Definitions

- **G-001 · المرابحة — Murabaha**
  - AR: بيعٌ بثمنٍ يساوي التكلفةَ مضافاً إليها ربحٌ معلوم، مع الإفصاح التامّ عن التكلفة والربح (أحد بيوع الأمانة).
  - EN: A sale at a price equal to cost plus a known profit, with full disclosure of cost and markup (one of the trust sales, buyu' al-amanah).

- **G-002 · القبض الحقيقي — actual (physical) possession**
  - AR: تسلّمُ الأصل تسلّماً مادياً فعلياً.
  - EN: Physical, actual receipt and taking of the asset.

- **G-003 · القبض الحكمي — constructive possession**
  - AR: قبضٌ تقديريٌّ بالتمكين والتخلية ونقلِ تبعةِ الهلاك دون تسلّمٍ مادّيٍّ مباشر.
  - EN: Constructive possession by enablement, clearing of the asset, and transfer of the risk of loss, without direct physical receipt.

- **G-004 · الوعد الملزم — binding promise (wa'd mulzim)**
  - AR: وعدٌ يُلزَم به الواعدُ بإتمام المعاملة؛ وإلزامُه في المرابحة للآمر بالشراء محلُّ خلاف (انظر D1).
  - EN: A promise by which the promisor is held bound to complete the transaction; its bindingness in MPO is contested (see D1).

- **G-005 · بيع العينة — bai' al-inah (sale-and-buyback)**
  - AR: بيعُ سلعةٍ بثمنٍ مؤجّلٍ ثمّ إعادةُ شرائها نقداً بأقلَّ من بائعها الأصلي؛ ممنوعٌ في دول الخليج.
  - EN: Selling a good on deferred terms then buying it back for cash at a lower price from its original seller; prohibited across the GCC.

- **G-006 · هامش الربح — profit markup**
  - AR: الزيادةُ المعلومةُ على التكلفة التي يتّفق عليها بوصفها ربحَ المرابحة.
  - EN: The known increment over cost agreed as the Murabaha profit.

- **G-007 · الذمة — dhimmah (liability / debt obligation)**
  - AR: المحلُّ المعنويُّ الذي يثبت فيه الدَّينُ والالتزامُ في ذمّة المدين.
  - EN: The legal locus in which a debt and obligation are established as a charge on the debtor.

- **G-008 · الربا — riba (usury / interest)**
  - AR: كلُّ زيادةٍ مشروطةٍ مضمونةٍ على قرضٍ أو دَين (ربا النسيئة)، أو تفاضلٍ في مبادلةِ جنسٍ ربويٍّ واحدٍ يداً بيد (ربا الفضل).
  - EN: Any stipulated, guaranteed increase on a loan or debt (riba al-nasiah), or an unequal hand-to-hand exchange of the same riba-bearing genus (riba al-fadl).

- **G-009 · الغرر — gharar (excessive uncertainty)**
  - AR: الغموضُ أو المخاطرةُ في أركان العقد؛ يُفسِدُ العقدَ إذا كان فاحشاً، ويُغتفَر إذا كان يسيراً.
  - EN: Ambiguity or hazard in the essential elements of a contract; it vitiates the contract when excessive (fahish) and is tolerated when minor (yasir).

- **G-010 · بيع المساومة — musawamah (bargaining sale)**
  - AR: بيعٌ لا يُفصَح فيه عن التكلفة، بخلاف المرابحة.
  - EN: A sale in which the cost is not disclosed, unlike Murabaha.

- **G-011 · البيع المؤجّل — deferred-payment sale (bai' muajjal)**
  - AR: بيعٌ يُؤجَّل فيه دفعُ الثمن إلى أجلٍ أو يُقسَّط، وهو الصورةُ المعتادةُ للمرابحة المصرفية.
  - EN: A sale in which payment of the price is deferred or paid in instalments — the usual form of banking Murabaha.

- **G-012 · التورق المنظّم — organized tawarruq** _(scope: Out-of-Murabaha-scope; seeded as a boundary marker only.)_
  - AR: تمويلٌ بالسلع للحصول على نقدٍ يرتّب المصرفُ سلسلتَه كاملةً ويتوكّل في طرفيه؛ مسألةٌ خلافية خارج نطاق المرابحة (انظر D3).
  - EN: Commodity financing to obtain cash where the bank arranges the whole chain and acts as agent on both legs; a contested matter outside Murabaha scope (see D3).

- **G-013 · بيع التولية — tawliyah (sale at cost)** _(scope: Encountered on demand (not seeded). Demonstrates the growth protocol running end-to-end: researched → provisional entry → routed to the consolidated review list.)_
  - AR: بيعٌ بثمنٍ يساوي تكلفةَ الاقتناء دون زيادةٍ ولا ربح، مع الإفصاح التامّ عن التكلفة؛ أحدُ بيوع الأمانة الثلاثة إلى جانب المرابحة (تكلفة + ربح) والوضيعة (بيعٌ بخسارة).
  - EN: A sale at a price equal to the acquisition cost with no markup or profit, with full cost disclosure; one of the three trust sales (buyu' al-amanah) alongside Murabaha (cost + profit) and wadiah (sale at a loss).
  - ↪ _Routed: Was routed to the consolidated Arabic review list (rendered/ARABIC_REVIEW_LIST.md); the principal accepted it on 2026-06-10, flipping status provisional -> locked. grounding_basis remains 'unverified' (tertiary web glossaries; confirm against primary sources before production)._

- **G-014 · الإجارة — Ijara (leasing)**
  - AR: عقدٌ على منفعةٍ مقصودةٍ من عينٍ مع بقاء ملكِها للمؤجِّر، بأجرةٍ ومدّةٍ معلومتين.
  - EN: A contract over the usufruct of an asset for a known rent and term, the lessor retaining ownership.
  - ↪ _Routed: Consolidated Arabic review list (Stage 2) — provisional; awaiting the principal's calibration to lock._

- **G-015 · المنفعة — usufruct (manfa'ah)**
  - AR: حقُّ الانتفاع بالعين مع بقاء عينها، وهو محلُّ عقد الإجارة.
  - EN: The right to use an asset while its corpus survives; the subject of an Ijara.
  - ↪ _Routed: Consolidated Arabic review list (Stage 2) — provisional._

- **G-016 · الإجارة المنتهية بالتمليك — Ijara Muntahia Bittamleek (lease-to-own)**
  - AR: إجارةٌ تقترن بترتيبٍ مستقلٍّ ينقل الملكيةَ للمستأجر في نهايتها (وعدٌ، هبةٌ، أو بيع).
  - EN: A lease coupled with a separate arrangement transferring ownership to the lessee at its end (promise, gift, or sale).
  - ↪ _Routed: Consolidated Arabic review list (Stage 2) — provisional._

- **G-017 · العين المؤجَّرة — the leased asset**
  - AR: العينُ غيرُ المستهلَكةِ محلُّ الإجارة، يجب تعيينُها وإباحةُ استعمالها.
  - EN: The non-consumable asset that is the subject of the lease; it must be identified and of permissible use.
  - ↪ _Routed: Consolidated Arabic review list (Stage 2) — provisional._

- **G-018 · الأجرة — rent (ujrah)**
  - AR: العوضُ المعلومُ في عقد الإجارة مقابلَ المنفعة، يُحدَّد عند العقد.
  - EN: The known consideration in an Ijara for the usufruct, determined at contract.
  - ↪ _Routed: Consolidated Arabic review list (Stage 2) — provisional._

- **G-019 · الصيانة الأساسية — basic (structural) maintenance**
  - AR: الصيانةُ المتعلّقةُ بأصل العين وبقائها، وتبعتُها على المؤجِّر بوصفه مالكاً.
  - EN: Maintenance relating to the corpus and survival of the asset; its liability rests on the lessor as owner.
  - ↪ _Routed: Consolidated Arabic review list (Stage 2) — provisional._

- **G-020 · الصيانة التشغيلية — operational maintenance**
  - AR: الصيانةُ المتعلّقةُ بالاستعمال المعتاد، وتبعتُها على المستأجر.
  - EN: Maintenance relating to ordinary use; its liability rests on the lessee.
  - ↪ _Routed: Consolidated Arabic review list (Stage 2) — provisional._

- **G-021 · التكافل — takaful (Islamic cooperative insurance)**
  - AR: التأمينُ التعاونيُّ القائمُ على التبرّع؛ وفي الإجارة تكون كلفتُه على المؤجِّر بوصفه مالكاً.
  - EN: Cooperative, donation-based insurance; in Ijara its cost rests on the lessor as owner.
  - ↪ _Routed: Consolidated Arabic review list (Stage 2) — provisional._

- **G-022 · البيع مع الاستئجار — sale-and-leaseback**
  - AR: أن يبيعَ العميلُ عيناً للمصرف ثم يستأجرَها؛ ويُشترَط فاصلٌ زمنيٌّ معتبرٌ منعاً من العِينة.
  - EN: The customer sells an asset to the bank then leases it back; a genuine interval is required to avoid bai' al-inah.
  - ↪ _Routed: Consolidated Arabic review list (Stage 2) — provisional._
