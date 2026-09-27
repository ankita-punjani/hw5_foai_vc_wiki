---
wiki_id: topic:irr-and-multiples
type: concept
topic: Returns Math
status: reviewed
description: Cash-on-cash multiples, IRR, and return expectations by stage.
sources:
- raw/Break Into VC - Bradley Miles.epub
- raw/Haas VCPE 295B - Venture Valuation.pdf
evidence_passages:
- breakintovc-book:147
- breakintovc-book:148
- breakintovc-book:290
- haas-venture-valuation:013
- haas-venture-valuation:015
- haas-venture-valuation:012
- haas-venture-valuation:020
- breakintovc-book:067
evidence_hash: f872e790d5d92d6b
generated_by: mlx-community/gemma-4-e2b-it-4bit
generated_at: '2026-09-25T22:58:04'
tags:
- vc/returns-math
reviewed_at: '2026-09-25T23:06:04'
review_notes:
- removed an off-topic customer-churn bullet
- added the Haas stage return table (pp. 45–46) and IRR table (p. 47)
- added a worked example and flagged an arithmetic error in the book's rapid-fire answer
- 'corrected the worked example: the book''s rapid-fire ''25% for 5 years ≈ 2.5x'' conflicts with its own table and with 1.25^5 ≈ 3.05x'
---
# IRR and Return Multiples

> Cash-on-cash multiples, IRR, and return expectations by stage.
> Topic: [[index#Returns Math|Returns Math]] · From: [[Break Into VC Book]], [[Haas Venture Valuation Slides]]

## Summary
A multiple (cash-on-cash) says how many times your money you got back; IRR is the annualised growth rate that accounts for when cash went in and came out. VC targets are higher the earlier the stage, because the risk is higher.

## Key points
* IRR is an annualised growth rate that accounts for cash inflows and outflows within the period; it is usually used to evaluate portfolios over a 5–10 year horizon [^1][^2].
* Over a 5-year horizon investors typically expect a 20–30% IRR, which is about 2.5–4.0x the money invested [^1].
* 5-year rules of thumb from the book: 1.5x ≈ 10% IRR, 2x ≈ 15%, 3x ≈ 25%, 4x ≈ 30%, 5x ≈ 40%, 6x ≈ 45% [^1].
* Haas slides, expected annual returns by stage: seed 75–100% (5–8 years to liquidity), start-up 50–75% (4–7 years), 1st–3rd rounds 30–50% (3–5 years), mezzanine 24–30% (1–2 years), public offering 10–20% [^3].
* The slides' multiple-to-IRR table gives, for 5 years: 2x = 15%, 3x = 25%, 4x = 32%, 5x = 38%, 10x = 58% [^4].
* The VC method uses a high discount rate because investors don't believe forecasts, need a liquidity premium, and provide services; the discount rate is "the embodiment of all risks" [^3].

## Worked example
1. Exact rule: multiple = (1 + IRR)^years. $1M at a 25% IRR for 5 years → 1.25^5 ≈ 3.05x ≈ $3.05M (my arithmetic), matching the rules of thumb "3x ≈ 25%" in the book [^1] and in the Haas table [^4].
1. At a 30% IRR: 1.3^5 ≈ 3.7x (my arithmetic); the Haas table puts 4x over 5 years at 32% [^4].
1. ⚠️ The book's rapid-fire answers give "about 2.5x" for 25% and "a little more than 4x, so a little more than $10M" for 30% [^5]. Both conflict with the book's own table and with the formula, and $10M is not 4x of $1M. They are source errors, flagged here and left unchanged in the source.

## Related notes
- [[Venture Capital Method]] — the required IRR or multiple is the discount rate in the VC method
- [[Power Law of Venture Returns]] — why early-stage targets are so high

## Sources
Each footnote opens the original file in `raw/` at the cited page or section.

[^1]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › Returns]] · `raw/Break Into VC - Bradley Miles.epub`
[^2]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Glossary]] · `raw/Break Into VC - Bradley Miles.epub`
[^3]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=45|pp. 45–46]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^4]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=47|p. 47]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^5]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › Rapid-Fire Questions]] · `raw/Break Into VC - Bradley Miles.epub`
