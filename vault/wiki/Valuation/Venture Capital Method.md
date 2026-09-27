---
wiki_id: topic:vc-method
type: concept
topic: Valuation
status: reviewed
description: Discount a hoped-for exit by the required return to price a round today.
sources:
- raw/Break Into VC - Bradley Miles.epub
- raw/Haas VCPE 295B - Venture Valuation.pdf
evidence_passages:
- breakintovc-book:174
- breakintovc-book:191
- breakintovc-book:175
- breakintovc-book:188
- haas-venture-valuation:015
- haas-venture-valuation:016
- breakintovc-book:190
- haas-venture-valuation:012
evidence_hash: bd8d326029cacc40
generated_by: mlx-community/gemma-4-e2b-it-4bit
generated_at: '2026-09-25T22:59:15'
tags:
- vc/valuation
reviewed_at: '2026-09-25T23:06:04'
review_notes:
- added both formulas and both worked examples (the draft had neither formula and only the $2.2M pre-money)
- removed off-topic precedent-transactions bullet
- added valuation divergence and method weaknesses
---
	# Venture Capital Method

> Discount a hoped-for exit by the required return to price a round today.
> Topic: [[index#Valuation|Valuation]] · From: [[Break Into VC Book]], [[Haas Venture Valuation Slides]]

## Summary
The Venture Capital Method prices a round today by working backwards from a hoped-for exit. Estimate the exit value, divide by the return the investor needs, and the result is the post-money valuation; subtract the investment to get pre-money.

## Key points
* Formula (book): post-money = exit value ÷ target ROI (cash-on-cash multiple); pre-money = post-money − investment [^1][^2].
* Formula (slides): post-money = future value ÷ (1 + required IRR)^years; ownership required = investment ÷ post-money [^3].
* Four steps: figure out how much money is needed today; estimate the final "enterprise value" if all goes well (comparables); use a high discount rate for the investor's required return; adjust for later rounds [^4].
* Exit value is often revenue in the exit year × an industry EV/sales multiple from comparable transactions or banker's reports [^5].
* Target seed ROI is typically ~30x, vs 5–7x at the growth stage, because early risk is higher [^1].
* Because of valuation divergence, the realistic early-stage ROI is more like 5–10x than the 30x target [^6].
* Weaknesses: forecasts and terminal values are hard to know, and one discount rate (60%? 50%? 40%?) struggles to capture all the risk [^7].

## Worked example
1. **Book: Syntax Health.** $30M exit-year revenue × 2.8x HCIT revenue multiple = $84M exit value [^5].
1. $84M ÷ 30x target ROI = $2.8M post-money; $500k investment → ~18% ownership; pre-money $2.2M [^1][^2].
1. **Slides: Mekasutra Games.** $250m future value ÷ (1 + 50%)^7 = $14.6m post-money [^3].
1. $5m ÷ $14.6m = 34% ownership; pre-money = $14.6m − $5m = $9.6m [^3].
1. Adjusting for a next-round investor who needs 15%: required ownership rises to 40%, post-money falls to $12.4m, and pre-money to $7.4m [^7].

## Related notes
- [[IRR and Return Multiples]] — supplies the required return used as the discount
- [[Comparables Valuation]] — estimates the exit value the method starts from
- [[Pre-Money and Post-Money Valuation]] — the method's output
- [[Projection Reflection]] — a shortcut that discounts the next round instead of the exit

## Sources
Each footnote opens the original file in `raw/` at the cited page or section.

[^1]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › Anticipated ROI in the VC Method … Using the VC Method]] · `raw/Break Into VC - Bradley Miles.epub`
[^2]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation]] · `raw/Break Into VC - Bradley Miles.epub`
[^3]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=48|pp. 48–50]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^4]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=44|p. 44]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^5]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › Enterprise Value and Multiples in the VC Method]] · `raw/Break Into VC - Bradley Miles.epub`
[^6]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › Valuation Divergence at the Early Stage]] · `raw/Break Into VC - Bradley Miles.epub`
[^7]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=51|pp. 51–52]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
