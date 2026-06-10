# Stage 3 GCC/Kuwait Test Corpus — Provenance Note

> **All five contracts are SYNTHETIC** (labelled in every file) and authored for Mizan testing. **No bank's text is reproduced** — only widely-documented *structural conventions* are imitated, each traceable to a consulted public source below. Hard rule honored: no convention is from recalled "this is probably how they write it"; every imitated convention traces to a source here or to the grounding reports (Inputs #2/#3).

## Sources consulted (public)
1. **Kuwait International Bank (KIB)** — Murabaha & Vehicle Financing product pages (kib.com.kw/.../islamic-finance/Murabaha). Confirms the Kuwaiti retail vehicle/goods Murabaha product framing and parties.
2. **Kuwait Finance House (KFH)** — Auto Murabaha & Ijara product pages (kfh.com). Confirms Murabaha+Ijara retail products (auto up to KWD 35,000, tenor to 7 years) and the wa'd-then-credit-sale framing.
3. **Institute of Islamic Banking and Insurance** — Murabaha structure (islamic-banking.com): three-party structure (seller/bank, buyer, supplier), bank as legal owner, disclosed profit margin.
4. **LexisNexis** — "The structure and required elements of a Murabaha transaction": IFI purchases the identified goods from the seller then sells to the customer at cost + pre-agreed markup.
5. **islamicbankers.center** — public Murabaha Facility Agreement (specimen): the **agency-appointment clause** (the Institution appoints the Client/agent to receive/transfer purchased items from the vendor on the Institution's behalf).
6. **Marifa / AIMS** — Ijara Muntahia Bittamleek home financing: bank purchases the property, **takes possession**, executes the Ijara and delivers; ownership-transfer at term end; and the **separate agency agreement** appointing the customer (lessee) as agent for **major maintenance + takaful**, with **the bank (Muwakkil) paying those costs** (lessor bears ownership risk).
7. **ScienceDirect** — "Reconstructing lease-to-own contracts… Islamic banking standards": IMB ownership-transfer and the lessor/lessee liability split.
8. **Inputs #2 & #3** (the Mizan grounding reports) — for the rule structure (R1–R6, I1–I7), the Arabic terms of art, the late-payment-to-charity convention, and the tawarruq positions.

## Structural conventions imitated (each → source)
- **Recitals (تمهيد) → parties (الأطراف) → numbered clauses (البنود) → acknowledgements (إقرارات)** Arabic legal register — standard GCC instrument layout (composed natively; layout per the specimen [5] and IMB write-ups [6,7]).
- **Three-party Murabaha** with an **agency-to-receive clause on the BANK's behalf** [3,4,5] — and, in the defect contract, the *for-the-customer / bank-merely-finances* variant that removes the bank's ownership window (the R1 defect per Input #2).
- **Promise (wa'd) to purchase** as a preliminary [2,3].
- **Disclosed cost + markup, fixed deferred instalments** [3,4].
- **Late-payment charge to charity** [Inputs #2/#3].
- **IMB**: bank acquires + possesses + delivers; **separate** transfer instrument; **"obligations of the customer/lessee" schedule** [6] — used in the defect contract to *dress* the I4 ownership-risk-shift (maintenance/takaful/total-loss pushed to the lessee at his own expense, without lessor reimbursement).
- **Commodity tawarruq** chain (bank sells commodity deferred → customer monetizes for cash) [Input #2].
- **Investment-wakala leg** as an uncovered component [Input #2 context].

## The five contracts
| # | File | Type | Intent |
|---|---|---|---|
| T1 | `T1_murabaha_vehicle_clean_ar.txt` | Murabaha (AR) | Realistic clean Kuwaiti vehicle Murabaha → R1–R5 pass, R6 wa'd deferral |
| T2 | `T2_murabaha_subtle_r1_ar.txt` | Murabaha (AR) | Realistic, ONE subtle buried defect: agency-for-customer / bank merely finances → R1 violated |
| T3 | `T3_ijara_imb_dressed_i4_ar.txt` | Ijara IMB (AR) | Realistic IMB; I4 ownership-risk-shift dressed in an "obligations of the customer" schedule |
| T4 | `T4_tawarruq_commodity_en.txt` | Tawarruq (EN) | Realistic commodity tawarruq → recognized, NO rule applied, D3 positions surfaced |
| T5 | `T5_mixed_murabaha_wakala_ar.txt` | Murabaha + investment-wakala (AR) | Covered Murabaha part checked; uncovered wakala-investment leg flagged out-of-scope |

_Not validated by any scholar or bank. Demonstration material only._
