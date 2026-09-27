---
wiki_id: topic:power-law
type: concept
topic: Returns Math
status: reviewed
description: Why one outlier has to pay for the whole portfolio.
sources:
- raw/Break Into VC - Bradley Miles.epub
- raw/Haas VCPE 295B - Venture Valuation.pdf
- raw/Harlem Capital - Return the Fund.pdf
evidence_passages:
- haas-venture-valuation:003
- haas-venture-valuation:010
- harlem-return-the-fund:006
- breakintovc-book:113
- breakintovc-book:131
- breakintovc-book:115
- breakintovc-book:281
- breakintovc-book:252
evidence_hash: b11d633b490dc1fb
generated_by: mlx-community/gemma-4-e2b-it-4bit
generated_at: '2026-09-25T22:57:52'
tags:
- vc/returns-math
reviewed_at: '2026-09-25T23:06:04'
review_notes:
- rewrote the two portfolio scenarios, which the draft garbled ('cost of 0.2x' for the same scenario)
- added the arithmetic behind 34x and 21x
- added failure-rate evidence from Harlem p. 2 and book ch. 2
---
# Power Law of Venture Returns

> Why one outlier has to pay for the whole portfolio.
> Topic: [[index#Returns Math|Returns Math]] · From: [[Break Into VC Book]], [[Haas Venture Valuation Slides]], [[Harlem Capital Return the Fund Post]]

## Summary
Most startups in a venture portfolio fail or just return their money, so one outlier has to produce almost all of the fund's return. The Haas slides make this concrete with a 10-company portfolio.

## Key points
* Goal in the example: a 3x gross return for an early-stage fund; after fees (0.2x) the fund has 0.8x to invest across 10 companies [^1].
* Equal weighting (0.08x per company): 5 companies go bankrupt (cost 0.4x, value 0x), 4 barely return capital (cost 0.32x, value 0.32x), and 1 company must be worth 2.68x, a **34x** multiple on its 0.08x cost [^1].
* Half initial check + 200% reserve for non-losers: bankrupt 5 cost 0.2x; the 4 survivors cost 0.16x + 0.32x = 0.48x; the winner costs 0.04x + 0.08x = 0.12x and must be worth 2.52x, a **21x** multiple [^1].
* Startup failure rates are high (75%–90% depending on definition), which is why fund returners are critical [^2].
* The book notes that in an early-stage portfolio over half of the companies may fail within 10 years [^3].
* A fund may not need unicorns to return the fund once, but it needs billions in value creation to reach 3x–5x [^4].

## Worked example
1. Target: 3.0x of the fund [^1].
1. Value from losers + break-evens: 0x + 0.32x = 0.32x, so the winner must supply 3.0x − 0.32x = 2.68x [^1].
1. Winner's cost 0.08x → 2.68 ÷ 0.08 ≈ 34x [^1].

## Related notes
- [[Return the Fund]] — the per-company version of the same logic
- [[IRR and Return Multiples]] — the fund-level multiple that the outlier has to deliver
- [[Scenario Analysis]] — puts probabilities on the outlier and failure outcomes for one deal

## Sources
Each footnote opens the original file in `raw/` at the cited page or section.

[^1]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=6|p. 6]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^2]: [[Harlem Capital Return the Fund Post]] · [[raw/Harlem Capital - Return the Fund.pdf#page=2|p. 2]] · `raw/Harlem Capital - Return the Fund.pdf`
[^3]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 2: Early Stage Investing › Why People Invest in Venture Capital]] · `raw/Break Into VC - Bradley Miles.epub`
[^4]: [[Harlem Capital Return the Fund Post]] · [[raw/Harlem Capital - Return the Fund.pdf#page=6|p. 6]] · `raw/Harlem Capital - Return the Fund.pdf`
