---
wiki_id: topic:projection-reflection
type: concept
topic: Valuation
status: reviewed
description: Price today by discounting the likely next-round valuation.
sources:
- raw/Haas VCPE 295B - Venture Valuation.pdf
evidence_passages:
- haas-venture-valuation:017
- haas-venture-valuation:018
- haas-venture-valuation:019
- haas-venture-valuation:010
- haas-venture-valuation:016
- haas-venture-valuation:005
- breakintovc-book:295
- harlem-return-the-fund:007
evidence_hash: 667d6c23c974f6c5
generated_by: mlx-community/gemma-4-e2b-it-4bit
generated_at: '2026-09-25T22:59:56'
tags:
- vc/valuation
reviewed_at: '2026-09-25T23:06:04'
review_notes:
- removed scenario-analysis and Harlem bullets that belonged to other notes
- added the stage discount shorthand (p. 55) and the four seed scenarios (pp. 58–61)
---
# Projection Reflection

> Price today by discounting the likely next-round valuation.
> Topic: [[index#Valuation|Valuation]] · From: [[Haas Venture Valuation Slides]]

## Summary
Projection Reflection prices a seed or early round by starting from the likely next-round valuation and discounting it by a stage multiple (e.g. ÷2.5 at start-up) [^2]. It works because startup value jumps in step functions at milestones.

## Key points
* If the company is self-sufficient, run it for the best business results; if not, run it to maximise the probability and value of raising money [^1].
* Value changes in step functions, not linearly, and optimal financings happen right after major step functions [^1].
* The goal is shared understanding and shared expectations between investors and management [^1].
* Shorthand discounts to the next round by stage: start-up 2.5x, early stage 2.0x, expansion 1.75x, late/mezzanine 1.5x [^2].
* At seed you iterate with the team: e.g. a raw start-up looking for $5M to build product, team and business model [^3].

## Worked example
1. **Mekasutra:** next round likely $30m pre-money; seed stage → $30m ÷ 2.5 = $12m post-money; $12m − $5m = $7m pre-money [^4].
1. **Iterating the seed deal:** projection $10M ÷ 2.5 = $4.0M post, but needing $5.0M cash → −$1.0M pre-money: a non-starter [^5].
1. Cut cash to $3M, projection $9M → $3.6M post, $0.6M pre → 83% to VCs, 17% to founder: not good [^5].
1. Raise future value to $15M with $3.5M → $6.0M post, $2.5M pre → 58% VCs / 42% founder: better [^5].
1. Much less cash ($1M) at $10M → $4.0M post, $3.0M pre → 25% VCs / 75% founders: a "do-able deal" [^5].

## Related notes
- [[Venture Capital Method]] — the longer-horizon version of the same discounting idea
- [[Pre-Money and Post-Money Valuation]] — subtracts the cash needed to get pre-money

## Sources
Each footnote opens the original file in `raw/` at the cited page or section.

[^1]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=54|p. 54]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^2]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=55|p. 55]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^3]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=57|p. 57]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^4]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=56|p. 56]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
[^5]: [[Haas Venture Valuation Slides]] · [[raw/Haas VCPE 295B - Venture Valuation.pdf#page=58|pp. 58–61]] · `raw/Haas VCPE 295B - Venture Valuation.pdf`
