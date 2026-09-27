---
wiki_id: topic:dilution
type: concept
topic: Returns Math
status: reviewed
description: How later rounds shrink ownership, and what pro-rata does about it.
sources:
- raw/Break Into VC - Bradley Miles.epub
- raw/Harlem Capital - Return the Fund.pdf
evidence_passages:
- harlem-return-the-fund:004
- breakintovc-book:178
- harlem-return-the-fund:007
- breakintovc-book:296
- haas-venture-valuation:009
- haas-venture-valuation:019
- haas-venture-valuation:021
- breakintovc-book:300
evidence_hash: 24c777a3645d612c
generated_by: mlx-community/gemma-4-e2b-it-4bit
generated_at: '2026-09-25T22:58:20'
tags:
- vc/returns-math
reviewed_at: '2026-09-25T23:06:04'
review_notes:
- 'removed an incorrect claim that early-stage investors target 3x–5x ROI (book: real early-stage ROI is 5–10x)'
- made the first bullet concrete
- added the 40%+ no-pro-rata point and the founder dilution comparison (p. 6)
- 'reframed firm-specific wording: general principle first, Harlem Capital named as one fund''s example'
- 'wiki verify: cited p. 2 for the $40mm fund size; quoted the 0.9% ownership increase as the source words it'
---
# Dilution

> How later rounds shrink ownership, and what pro-rata does about it.
> Topic: [[index#Returns Math|Returns Math]] · From: [[Break Into VC Book]], [[Harlem Capital Return the Fund Post]]

## Summary
Dilution is the drop in your percentage ownership each time a company sells new shares in a later round. Investors assume a dilution path to estimate ownership at exit, and use pro-rata follow-on checks to limit it.

## Key points
* The dilution assumption is the first BIG guess in the return model [^1].
* A typical assumption (from one seed fund's model): the seed round is 25% (midpoint of 20–30%) and each later round steps down 5%: Series A 20%, B 15%, C 10%, and a 5% floor for Series D+ [^1].
* That fund reserves 30–40% of its money to take its pro-rata at the Series A, so its model has 0% dilution in that round; overall it assumes 25–30% dilution by exit [^1].
* Without that Series A pro-rata check, total dilution is 40%+, so funds that don't follow on need larger exits [^1].
* Founders can't take pro-rata: in the post's founder example total dilution is 38.8% vs 23.5% for the investor; co-founders typically own ~30% each after seed [^2].
* Valuation divergence: as a company's valuation rises, early private shares rise much more slowly, cutting early investors' cash-on-cash ROI by as much as 3–5x [^3][^4].
* Pro-rata means taking part in future rounds to keep the same ownership stake [^4].

## Worked example
1. Base case: 23.5% total dilution by exit → 5.7% ownership → a $700mm exit needed to return the $40mm fund [^1][^5].
1. Halve Series B and C dilution → 12.1% total dilution → 6.6% ownership at exit [^1].
1. That 0.9% ownership increase means only a $605mm exit is needed instead of $700mm, $95mm less [^1].

## Related notes
- [[Return the Fund]] — less ownership at exit means a bigger exit is needed
- [[Check Size and Reserves]] — follow-on reserves are how funds defend ownership
- [[Scenario Analysis]] — scenario tables apply dilution round by round

## Sources
Each footnote opens the original file in `raw/` at the cited page or section.

[^1]: [[Harlem Capital Return the Fund Post]] · [[raw/Harlem Capital - Return the Fund.pdf#page=4|p. 4]] · `raw/Harlem Capital - Return the Fund.pdf`
[^2]: [[Harlem Capital Return the Fund Post]] · [[raw/Harlem Capital - Return the Fund.pdf#page=6|p. 6]] · `raw/Harlem Capital - Return the Fund.pdf`
[^3]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Chapter 12: Returns and Valuation › Valuation Divergence at the Early Stage]] · `raw/Break Into VC - Bradley Miles.epub`
[^4]: [[Break Into VC Book]] · [[raw/Break Into VC - Bradley Miles.epub|Glossary]] · `raw/Break Into VC - Bradley Miles.epub`
[^5]: [[Harlem Capital Return the Fund Post]] · [[raw/Harlem Capital - Return the Fund.pdf#page=2|p. 2]] · `raw/Harlem Capital - Return the Fund.pdf`
