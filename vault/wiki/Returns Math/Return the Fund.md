---
wiki_id: topic:return-the-fund
type: concept
topic: Returns Math
status: reviewed
description: The fund-returner test and why fund size changes the exit a VC needs.
sources:
- raw/Harlem Capital - Return the Fund.pdf
evidence_passages:
- harlem-return-the-fund:006
- harlem-return-the-fund:002
- harlem-return-the-fund:003
- haas-venture-valuation:003
- harlem-return-the-fund:004
- harlem-return-the-fund:005
- breakintovc-book:023
- harlem-return-the-fund:007
evidence_hash: f122423da77fe905
generated_by: mlx-community/gemma-4-e2b-it-4bit
generated_at: '2026-09-25T22:57:40'
tags:
- vc/returns-math
reviewed_at: '2026-09-25T23:06:04'
review_notes:
- added the actual fund-returner definition and 53.3x example (p. 2), missing from the draft
- removed '34x required multiple' stated without context (it is the Haas portfolio example; now in Power Law)
- corrected a bullet that mislabelled 23.5% as seed dilution
- added the 36% ($250mm exit) and no-unicorn-modelling points
- 'reframed firm-specific wording: general principle first, Harlem Capital named as one fund''s example'
- 'wiki verify: cited p. 2 for the $40mm fund size'
---
# Return the Fund

> The fund-returner test and why fund size changes the exit a VC needs.
> Topic: [[index#Returns Math|Returns Math]] · From: [[Harlem Capital Return the Fund Post]]

## Summary
A "fund returner" is a single investment that pays back the entire fund on its own. VCs ask "can this return the fund?" because most startups fail. The exit a company needs to return the fund depends on the fund's size and on how much the VC still owns at exit.

## Key points
* Fund returner: invest an amount and get back 100% of the TOTAL fund from that one investment. In the post's worked example, a $750k check in a $40mm fund needs a 53.3x return [^1].
* Fund returners are rare, but critical, because the startup failure rate is high (75%–90%, depending on who you ask) [^1].
* In the same example, 23.5% total dilution leaves 5.7% ownership at exit, so a $700mm exit is needed to return the $40mm fund [^1][^2].
* Fund size drives the required exit: the same $750k check needs a $350mm exit to return a $20mm fund, but a $4.3bn exit for a $250mm fund ("VERY UNLIKELY") [^3].
* A $250mm exit returns only 36% of that $40mm fund, which is why "big" exits can still be too small for a VC [^4].
* Seed funds typically target a 3x–5x gross return, i.e. $120mm–$200mm for a $40mm fund; at ~5% average ownership at exit that implies $2.4bn–$4.0bn of total exit value [^3].
* Not every fund counts on IPOs or unicorns: the example fund models neither, because most exits are M&A under $1bn, and it wants to be able to return the fund without them [^4].

## Worked example
1. Check: $750k × 53.3 ≈ $40mm, so one investment returns the whole fund [^1].
1. Ownership at exit 5.7% × $700mm exit ≈ $40mm (my arithmetic on the example's numbers [^2]).
1. Halve the fund to $20mm → the exit needed halves to $350mm; a $250mm fund would need $4.3bn [^3].

## Related notes
- [[Power Law of Venture Returns]] — most companies fail, so a few must each return the fund
- [[Dilution]] — ownership lost before exit raises the exit needed to return the fund
- [[Ownership Targets]] — entry ownership is the starting point of the calculation
- [[Check Size and Reserves]] — check size relative to fund size sets the return multiple required

## Sources
Each footnote opens the original file in `raw/` at the cited page or section.

[^1]: [[Harlem Capital Return the Fund Post]] · [[raw/Harlem Capital - Return the Fund.pdf#page=2|p. 2]] · `raw/Harlem Capital - Return the Fund.pdf`
[^2]: [[Harlem Capital Return the Fund Post]] · [[raw/Harlem Capital - Return the Fund.pdf#page=4|p. 4]] · `raw/Harlem Capital - Return the Fund.pdf`
[^3]: [[Harlem Capital Return the Fund Post]] · [[raw/Harlem Capital - Return the Fund.pdf#page=6|p. 6]] · `raw/Harlem Capital - Return the Fund.pdf`
[^4]: [[Harlem Capital Return the Fund Post]] · [[raw/Harlem Capital - Return the Fund.pdf#page=5|p. 5]] · `raw/Harlem Capital - Return the Fund.pdf`
