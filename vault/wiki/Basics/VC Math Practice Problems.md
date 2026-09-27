---
wiki_id: topic:vc-math-practice
type: concept
topic: Basics
status: reviewed
description: Worked problems with answers — ownership, IRR, return the fund, VC method.
sources:
- raw/Break Into VC - Bradley Miles.epub
- raw/Haas VCPE 295B - Venture Valuation.pdf
- raw/Harlem Capital - Return the Fund.pdf
evidence_passages:
- breakintovc-book:148
- breakintovc-book:192
- breakintovc-book:193
- breakintovc-book:147
- breakintovc-book:154
- breakintovc-book:191
- breakintovc-book:179
- breakintovc-book:153
evidence_hash: 6c40ced9a4d08a9c
generated_by: mlx-community/gemma-4-e2b-it-4bit
generated_at: '2026-09-26T14:33:14'
tags:
- vc/basics
reviewed_at: '2026-09-26T14:35:29'
review_notes:
- replaced a draft that repeated one IRR step three times and copied the book's '$10M' arithmetic slip
- 12 problems across ownership, IRR, return-the-fund, VC method, scenario value, rule of thirds, EV/EBITDA and CAC, each with its source
- answers folded in Obsidian callouts for self-testing; the book's slip in problem 4 is flagged, not repeated
- 'wiki verify: added missing citations for $40mm (p. 2) and the $2.8M / 18% figures (book ch. 12)'
---
# VC Math Practice Problems

> Worked problems with answers — ownership, IRR, return the fund, VC method.
> Topic: [[index#Basics|Basics]] · From: [[Break Into VC Book]], [[Haas Venture Valuation Slides]], [[Harlem Capital Return the Fund Post]]

## Summary
Twelve short problems covering the math in this wiki, each with a worked answer taken from the sources. In Obsidian, each answer is folded; click the problem to reveal it. Try each one first.

## Key points
* Pre-money + money invested = post-money; your ownership = money invested ÷ post-money [^1][^2].
* Over 5 years, multiple ↔ IRR rules of thumb: 2x ≈ 15%, 3x ≈ 25%, 4x ≈ 30% (book) or 32% (slides table) [^3][^4]. Exact check: multiple = (1 + IRR)^years.
* Fund returner: the multiple needed = fund size ÷ check size; the exit needed = fund size ÷ ownership at exit [^5][^6].
* VC method: post-money = exit value ÷ target multiple (or ÷ (1 + IRR)^years); pre-money = post-money − investment [^7][^8].
* Expected (probable) value = Σ probability × value of each outcome [^9].

## Worked example
> [!question]- 1. A company has a **$500k post-money** valuation and you invest **$250k**. What do you own?
> **50%.** Post-money already includes your money: $250k ÷ $500k [^2].

> [!question]- 2. Same $250k, but at a **$500k pre-money** valuation?
> **~33.3%.** Post-money = $500k + $250k = $750k; $250k ÷ $750k [^2].

> [!question]- 3. You invest $250k at a **$1M pre-money**. What do you own? What if $1M were the **post-money**?
> Pre-money: total capital $1.25M → **20%**. Post-money: $250k ÷ $1M → **25%**. The same headline number gives the investor more ownership as a post-money figure [^10].

> [!question]- 4. You invest **$1M at a 25% IRR for 5 years**. What comes back? At a 30% IRR?
> 25%: 1.25^5 ≈ **3.05x ≈ $3.05M**, matching the rule of thumb 3x ≈ 25% [^3][^4]. 30%: 1.3^5 ≈ **3.7x ≈ $3.7M** (my arithmetic).
> ⚠️ The book's rapid-fire answers say "about 2.5x" for 25% and "a little more than 4x, so a little more than $10M" for 30% [^2]. Both disagree with the book's own table and with the formula; the $10M is also inconsistent with 4x of $1M. Trust the formula.

> [!question]- 5. A **$40mm fund** writes a **$750k** check. What multiple must that one company return to pay back the whole fund?
> **53.3x.** $40mm ÷ $750k ≈ 53.3, so $750k × 53.3 ≈ $40mm [^5].

> [!question]- 6. After dilution the fund owns **5.7%** at exit. What exit value returns the **$40mm** fund?
> **About $700mm.** $40mm ÷ 5.7% ≈ $700mm, which is the exit the example says is needed [^5][^6].

> [!question]- 7. VC method: expected exit value **$84M**, target return **30x**, investment **$500k**. Post-money, ownership, pre-money?
> Post-money = $84M ÷ 30x = **$2.8M**; ownership = $500k ÷ $2.8M ≈ **18%**; pre-money = $2.8M − $500k ≈ **$2.2M** [^7][^14].

> [!question]- 8. VC method with IRR: future value **$250m** in **7 years**, required IRR **50%**, investment **$5m**?
> Post-money = $250m ÷ (1 + 50%)^7 ≈ **$14.6m**; ownership = $5m ÷ $14.6m ≈ **34%**; pre-money = **$9.6m** [^8].

> [!question]- 9. Your stake is worth **$124m / $26m / $7m / $0** in four exits with probabilities **2% / 10% / 30% / 58%**. Expected value on a **$5m** investment?
> 2%×$124m ≈ $2.5m, 10%×$26m = $2.6m, 30%×$7m = $2.1m, 58%×$0 = $0 → **$7.2m ≈ 1.4x** [^9].

> [!question]- 10. Rule of thirds: angels raising **$800k** take one third of the company. Post-money?
> **$2.4M** ($800k × 3). Raising $1M would imply $3M [^11].

> [!question]- 11. A company's enterprise value is **$100** and its EBITDA is **$20**. What is its EV/EBITDA multiple?
> **5x**: the market values each $1 of EBITDA at $5 [^12].

> [!question]- 12. Sales and marketing spend is **$300,000** and it brings in **300** new customers. What is CAC?
> **$1,000** per customer ($300,000 ÷ 300); lower is better [^13].

## Related notes
- [[Pre-Money and Post-Money Valuation]] — the rules behind the ownership problems
- [[IRR and Return Multiples]] — the rules behind the return problems
- [[Return the Fund]] — the rules behind the fund-returner problem
- [[Venture Capital Method]] — the rules behind the valuation problem

## Sources
Each footnote opens the original file in `raw/` at the cited page or section.

[^1]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=38|p. 38]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^2]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › Rapid-Fire Questions]] · `raw/Break Into VC - Bradley Miles.epub`
[^3]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › Returns]] · `raw/Break Into VC - Bradley Miles.epub`
[^4]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=47|p. 47]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^5]: [[Harlem Capital Return the Fund Post]] · [[raw/Harlem Capital - Return the Fund.pdf#page=2|p. 2]] · `raw/Harlem Capital - Return the Fund.pdf`
[^6]: [[Harlem Capital Return the Fund Post]] · [[raw/Harlem Capital - Return the Fund.pdf#page=4|p. 4]] · `raw/Harlem Capital - Return the Fund.pdf`
[^7]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › Anticipated ROI in the VC Method … Using the VC Method]] · `raw/Break Into VC - Bradley Miles.epub`
[^8]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=48|pp. 48–50]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^9]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=66|p. 66]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^10]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › In an Interview]] · `raw/Break Into VC - Bradley Miles.epub`
[^11]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › Rule of Thirds]] · `raw/Break Into VC - Bradley Miles.epub`
[^12]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › EBITDA … The Multiple: How to Calculate (EV/EBITDA)]] · `raw/Break Into VC - Bradley Miles.epub`
[^13]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 7: Performance Metrics › Calculating Customer Acquisition Costs]] · `raw/Break Into VC - Bradley Miles.epub`
[^14]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation]] · `raw/Break Into VC - Bradley Miles.epub`
