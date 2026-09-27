---
wiki_id: topic:comparables
type: concept
topic: Valuation
status: reviewed
description: Pricing a company from multiples of similar public firms or deals.
sources:
- raw/Break Into VC - Bradley Miles.epub
- raw/Haas VCPE 295B - Venture Valuation.pdf
evidence_passages:
- breakintovc-book:170
- breakintovc-book:169
- haas-venture-valuation:008
- breakintovc-book:191
- breakintovc-book:167
- haas-venture-valuation:009
- breakintovc-book:174
- breakintovc-book:188
evidence_hash: eaf03db361932115
generated_by: mlx-community/gemma-4-e2b-it-4bit
generated_at: '2026-09-25T22:59:27'
tags:
- vc/valuation
reviewed_at: '2026-09-25T23:06:04'
review_notes:
- added the slides' definition, advantages and disadvantages (pp. 29–32), which the draft skipped
- removed the off-topic 'six concepts' bullet
- added the EV/sales point for EBITDA-negative startups
---
# Comparables Valuation

> Pricing a company from multiples of similar public firms or deals.
> Topic: [[index#Valuation|Valuation]] · From: [[Break Into VC Book]], [[Haas Venture Valuation Slides]]

## Summary
Comparables value a company from the multiples of similar companies: public peers or recent private deals. It is quick and market-based, but startups rarely have true peers, so VCs usually apply revenue multiples rather than earnings multiples.

## Key points
* Look at similar private deals and/or ratios of similar public firms (market value/sales, P/E, market value of equity/book value), then apply [discounted] multiples to get a projected market value [^1].
* Advantages: easy, market-based, frequently used; the "real estate" method ("the house down the street sold for $1m, and this house has an extra bathroom!") [^1].
* Disadvantages: public firms may not be similar, it is unclear what business the startup is in now vs at exit, private deal prices are often unobservable (deal knowledge is a VC advantage), and it is hard to pick a fair discount [^1].
* Startups also get priced on non-financial ratios: price per patent, per employee, per subscriber, per user or unique visitor, per unit of revenue [^2].
* EV/EBITDA shows how many times the market values a company's earnings; EBITDA allows an "apples to apples" comparison [^3].
* Early-stage companies are usually EBITDA-negative, so VCs use sales as a proxy and build an EV/sales multiple [^4].
* Precedent transactions analysis uses deals that actually closed (within the past five years). It tends to give higher values because of the control premium [^4].

## Worked example
1. EV/EBITDA: enterprise value $100 ÷ EBITDA $20 = 5x, i.e. each $1 of earnings is valued at $5 [^3].
1. EV/sales in the VC method: $30M exit-year revenue × 2.8x sector multiple = $84M enterprise value [^5].

## Related notes
- [[Venture Capital Method]] — comparables estimate the exit value the VC method discounts
- [[Scenario Analysis]] — comparables anchor the exit values in each scenario
- [[Valuation Fundamentals]] — why market-based methods break down for startups

## Sources
Each footnote opens the original file in `raw/` at the cited page or section.

[^1]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=29|pp. 29–31]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^2]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=32|p. 32]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^3]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › EBITDA … The Multiple: How to Calculate (EV/EBITDA)]] · `raw/Break Into VC - Bradley Miles.epub`
[^4]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › Use Cases in Venture Capital … Precedent Transactions Analysis]] · `raw/Break Into VC - Bradley Miles.epub`
[^5]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › Enterprise Value and Multiples in the VC Method]] · `raw/Break Into VC - Bradley Miles.epub`
