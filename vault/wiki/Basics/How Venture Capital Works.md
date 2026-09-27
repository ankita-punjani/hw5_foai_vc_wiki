---
wiki_id: topic:how-vc-works
type: concept
topic: Basics
status: reviewed
description: What VC is, who puts the money in, and how everyone gets paid back.
sources:
- raw/Break Into VC - Bradley Miles.epub
- raw/Haas VCPE 295B - Venture Valuation.pdf
- raw/Harlem Capital - Return the Fund.pdf
evidence_passages:
- breakintovc-book:023
- breakintovc-book:049
- haas-venture-valuation:013
- breakintovc-book:025
- breakintovc-book:183
- breakintovc-book:046
- harlem-return-the-fund:005
- breakintovc-book:176
evidence_hash: 606eb3ca6a559b85
generated_by: mlx-community/gemma-4-e2b-it-4bit
generated_at: '2026-09-26T14:32:20'
tags:
- vc/basics
reviewed_at: '2026-09-26T14:35:29'
review_notes:
- 'rewrote the draft: it cited an off-topic risk-factor method and an angel-stake statistic, and never said what VC is'
- added what VC is, whose money it is, the funding path, fund life and fees, exits, and the power-law logic
- added a 'follow $1 of a fund' worked example from the Haas slides (p. 6)
---
# How Venture Capital Works

> What VC is, who puts the money in, and how everyone gets paid back.
> Topic: [[index#Basics|Basics]] · From: [[Break Into VC Book]], [[Haas Venture Valuation Slides]], [[Harlem Capital Return the Fund Post]]

## Summary
Venture capital is money invested in young, risky private companies in exchange for a share of ownership (equity). VC firms invest money they raise from institutions (limited partners). They get it back only when a company is sold or goes public, and because most startups fail, a few big winners have to pay for everything.

## Key points
* **What it is:** venture capital is the money an early-stage business receives in order to grow. The industry backs companies with huge risk and little-to-no proven track record, and also growing businesses (e.g. Uber, Seamless) that need help with expansion [^1].
* **Whose money:** venture capitalists invest money received from limited partners (endowments, foundations, public pensions, high-net-worth individuals), not their own. Angel investors are individuals investing their own money, often before a sellable product exists [^1][^2].
* **Why LPs invest:** to diversify beyond stocks, bonds and real estate. Usually under 15% of a portfolio goes to alternative investments such as VC. VC firms return 25% on average vs about 8% a year for the stock market, but more than half of an early-stage portfolio may fail within 10 years [^3].
* **The funding path:** angels and accelerators (e.g. Y Combinator, Techstars) are usually the first money in. Seed and Series A investors (e.g. First Round Capital, 500 Startups) step in once the product gains traction. Growth equity firms come in at Series C or D, when the company is a top-two player heading for an IPO or acquisition [^4].
* **How a fund runs:** it invests over 3–5 years and returns the money over 8 to 10 years in total. The partners charge LPs a management fee of about 2% and keep 20% of profits (carried interest) once LPs have their money back [^5].
* **How investors get paid back:** at an exit, meaning an IPO or a merger/acquisition. The larger the firm's ownership stake, the larger its return [^5]. At seed, founders typically give up 20%–30% of the company [^6].
* **Why VCs think in outliers:** startup failure rates are very high (75%–90%, depending on who you ask), so each investment must have a shot at returning the entire fund on its own [^7].

## Worked example
**Follow $1 of a venture fund** (Haas slide example, goal = 3x gross return) [^8]:
1. The fund raises 1x from LPs; 0.2x goes to fees, so 0.8x is invested across 10 companies [^8].
1. 5 companies go bankrupt (worth 0x); 4 barely return their capital (0.32x in, 0.32x out) [^8].
1. To reach 3x overall, the single winner must be worth 2.68x of the fund, a 34x return on the 0.08x it received [^8].
1. That is why VCs ask whether a startup can "return the fund"; see [[Power Law of Venture Returns]] and [[Return the Fund]].

## Related notes
- [[Venture Fund Structure]] — the fund behind the investor, and who its money comes from
- [[Management Fees and Carried Interest]] — how the people running the fund get paid
- [[Power Law of Venture Returns]] — why VCs chase a few huge winners instead of many safe bets
- [[Pre-Money and Post-Money Valuation]] — the first piece of math in every funding round
- [[VC Glossary]] — definitions for every term used here

## Sources
Each footnote opens the original file in `raw/` at the cited page or section.

[^1]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 2: Early Stage Investing › What Is Venture Capital?]] · `raw/Break Into VC - Bradley Miles.epub`
[^2]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 2: Early Stage Investing › Venture Capital and Angel Investing]] · `raw/Break Into VC - Bradley Miles.epub`
[^3]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 2: Early Stage Investing › Why People Invest in Venture Capital]] · `raw/Break Into VC - Bradley Miles.epub`
[^4]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 5: Growth Equity › What is Growth Equity?]] · `raw/Break Into VC - Bradley Miles.epub`
[^5]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 2: Early Stage Investing › How Does It Work?]] · `raw/Break Into VC - Bradley Miles.epub`
[^6]: [[Harlem Capital Return the Fund Post]] · [[raw/Harlem Capital - Return the Fund.pdf#page=3|p. 3]] · `raw/Harlem Capital - Return the Fund.pdf`
[^7]: [[Harlem Capital Return the Fund Post]] · [[raw/Harlem Capital - Return the Fund.pdf#page=2|p. 2]] · `raw/Harlem Capital - Return the Fund.pdf`
[^8]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=6|p. 6]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
