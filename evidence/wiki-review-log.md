# Wiki review log

Every topic note was drafted by Gemma 4 E2B during `wiki ingest` (the drafts are unedited in
[gemma-drafts/](gemma-drafts/) and in the ingest logs in `outputs/runs/`), then checked claim by claim
against the source passages it cites. **Corrections were made in the wiki note; the original sources
were never edited.** Reviewed notes carry `status: reviewed` and a `review_notes` list in their
frontmatter; the table below is generated from those lists. `wiki ingest` never overwrites a reviewed
note: a redraft caused by changed evidence goes to `data/drafts/`.

**Most common draft problems:**
- off-topic bullets pulled from the glossary (churn in the IRR note, WACC in venture debt)
- two examples merged into one wrong statement (Power Law, Scenario Analysis)
- key facts that were in the evidence but missing from the note (a seed fund's actual check size, the fund-returner definition, both VC-method formulas)
- a number corrupted by an EPUB footnote marker ($480,000.14)
- a looping draft (practice problems)

**Errors found in the sources themselves, flagged rather than copied:** the book's rapid-fire answers
say 25% IRR for 5 years ≈ 2.5x (1.25⁵ ≈ 3.05x, and the book's own table says 3x ≈ 25%), and that
"a little more than 4x" on $1M is "a little more than $10M".

**Later passes:**
1. **Beginner framing** (2026-09-26): firm-specific wording was rewritten so each note states the general rule first and names Harlem Capital only as one fund's example.
2. **`wiki verify`** (automatic audit): found 6 citation gaps (correct numbers cited to an incomplete page, or not cited at all) and 2 notation mismatches. All were fixed. The final audit: 24 notes, 129 footnotes, 0 unresolved, 459 numbers, 0 unsupported.

| Folder | Note | Review notes (from frontmatter) |
|---|---|---|
| Basics | [How Venture Capital Works](../vault/wiki/Basics/How%20Venture%20Capital%20Works.md) | rewrote the draft: it cited an off-topic risk-factor method and an angel-stake statistic, and never said what VC is; added what VC is, whose money it is, the funding path, fund life and fees, exits, and the power-law logic; added a 'follow $1 of a fund' worked example from the Haas slides (p. 6) |
| Basics | [VC Glossary](../vault/wiki/Basics/VC%20Glossary.md) | replaced the draft (which defined 'interest payable' and 'liabilities' instead of VC terms) with 28 core VC terms; definitions taken from the book's glossary, or its chapters where the glossary has no entry (angel, management fee, fund returner, venture capital); flagged the book's inconsistent ROI targets (glossary 8–10x vs the VC-method example's ~30x); wiki verify: cited the VC-method chapter for the ~30x seed target |
| Basics | [VC Math Practice Problems](../vault/wiki/Basics/VC%20Math%20Practice%20Problems.md) | replaced a draft that repeated one IRR step three times and copied the book's '$10M' arithmetic slip; 12 problems across ownership, IRR, return-the-fund, VC method, scenario value, rule of thirds, EV/EBITDA and CAC, each with its source; answers folded in Obsidian callouts for self-testing; the book's slip in problem 4 is flagged, not repeated; wiki verify: added missing citations for $40mm (p. 2) and the $2.8M / 18% figures (book ch. 12) |
| Fund Structure | [Venture Fund Structure](../vault/wiki/Fund%20Structure/Venture%20Fund%20Structure.md) | clarified the alternative-investments bullet (LPs allocate <15%); added raising the next fund at ~75% committed; replaced a meaningless worked example ('a typical deal might be $18M') with the book's CynMerc fund-life example |
| Fund Structure | [Management Fees and Carried Interest](../vault/wiki/Fund%20Structure/Management%20Fees%20and%20Carried%20Interest.md) | merged two duplicate carry bullets; removed off-topic bullet about stake size; replaced 'no worked example' with the slides' fee example (p. 6) |
| Fund Structure | [Check Size and Reserves](../vault/wiki/Fund%20Structure/Check%20Size%20and%20Reserves.md) | added Harlem's actual check size ($500k–$1mm, avg $750k) which the draft omitted; removed ownership-target and 'billions of value' bullets (belong to other notes); fixed a bullet that merged seed dilution with total dilution; added the slides' reserve points (p. 5, p. 6) and a worked example; reframed firm-specific wording: general principle first, Harlem Capital named as one fund's example |
| Returns Math | [Return the Fund](../vault/wiki/Returns%20Math/Return%20the%20Fund.md) | added the actual fund-returner definition and 53.3x example (p. 2), missing from the draft; removed '34x required multiple' stated without context (it is the Haas portfolio example; now in Power Law); corrected a bullet that mislabelled 23.5% as seed dilution; added the 36% ($250mm exit) and no-unicorn-modelling points; reframed firm-specific wording: general principle first, Harlem Capital named as one fund's example; wiki verify: cited p. 2 for the $40mm fund size |
| Returns Math | [Power Law of Venture Returns](../vault/wiki/Returns%20Math/Power%20Law%20of%20Venture%20Returns.md) | rewrote the two portfolio scenarios, which the draft garbled ('cost of 0.2x' for the same scenario); added the arithmetic behind 34x and 21x; added failure-rate evidence from Harlem p. 2 and book ch. 2 |
| Returns Math | [IRR and Return Multiples](../vault/wiki/Returns%20Math/IRR%20and%20Return%20Multiples.md) | removed an off-topic customer-churn bullet; added the Haas stage return table (pp. 45–46) and IRR table (p. 47); added a worked example and flagged an arithmetic error in the book's rapid-fire answer; corrected the worked example: the book's rapid-fire '25% for 5 years ≈ 2.5x' conflicts with its own table and with 1.25^5 ≈ 3.05x |
| Returns Math | [Dilution](../vault/wiki/Returns%20Math/Dilution.md) | removed an incorrect claim that early-stage investors target 3x–5x ROI (book: real early-stage ROI is 5–10x); made the first bullet concrete; added the 40%+ no-pro-rata point and the founder dilution comparison (p. 6); reframed firm-specific wording: general principle first, Harlem Capital named as one fund's example; wiki verify: cited p. 2 for the $40mm fund size; quoted the 0.9% ownership increase as the source words it |
| Valuation | [Valuation Fundamentals](../vault/wiki/Valuation/Valuation%20Fundamentals.md) | added value vs price vs valuation (p. 16) and the regular-vs-VC-company data comparison (p. 24); listed the six concepts the draft only named; moved method-specific bullets to their own notes; added the three-method Mekasutra comparison as a worked example |
| Valuation | [Pre-Money and Post-Money Valuation](../vault/wiki/Valuation/Pre-Money%20and%20Post-Money%20Valuation.md) | replaced a confusing '1/npre' bullet with the core pre + money = post identity (slides p. 38) |
| Valuation | [Ownership Targets](../vault/wiki/Valuation/Ownership%20Targets.md) | removed dilution/reserves/'billions' bullets that belong to other notes; added lead vs co-invest targets; added the worked example from p. 3 and the slides' 20% requirement; reframed firm-specific wording: general principle first, Harlem Capital named as one fund's example |
| Valuation | [Venture Capital Method](../vault/wiki/Valuation/Venture%20Capital%20Method.md) | added both formulas and both worked examples (the draft had neither formula and only the $2.2M pre-money); removed off-topic precedent-transactions bullet; added valuation divergence and method weaknesses |
| Valuation | [Comparables Valuation](../vault/wiki/Valuation/Comparables%20Valuation.md) | added the slides' definition, advantages and disadvantages (pp. 29–32), which the draft skipped; removed the off-topic 'six concepts' bullet; added the EV/sales point for EBITDA-negative startups |
| Valuation | [Scenario Analysis](../vault/wiki/Valuation/Scenario%20Analysis.md) | replaced a wrong worked example (21/26/34% are post-round ownerships, not results of the $4.5m case); added the Mekasutra base case, probabilities and 1.4x result (p. 66) and what-ifs (pp. 67–68) |
| Valuation | [Projection Reflection](../vault/wiki/Valuation/Projection%20Reflection.md) | removed scenario-analysis and Harlem bullets that belonged to other notes; added the stage discount shorthand (p. 55) and the four seed scenarios (pp. 58–61) |
| Valuation | [Pre-Revenue Valuation Methods](../vault/wiki/Valuation/Pre-Revenue%20Valuation%20Methods.md) | replaced a vague worked example with the book's full scoring example and a rule-of-thirds example |
| Startup Metrics | [SaaS Metrics](../vault/wiki/Startup%20Metrics/SaaS%20Metrics.md) | fixed '$480,000.14' (a footnote number glued to the figure in the EPUB text); replaced an off-topic book-to-bill bullet with the book's CAC example |
| Startup Metrics | [Financial Statements Basics](../vault/wiki/Startup%20Metrics/Financial%20Statements%20Basics.md) | corrected an EBITDA bullet that said D&A is subtracted before EBITDA; made the depreciation example show the formula |
| Financing Types | [Growth Equity](../vault/wiki/Financing%20Types/Growth%20Equity.md) | checked all bullets against ch. 5 and the glossary; no factual errors found |
| Financing Types | [Venture Debt](../vault/wiki/Financing%20Types/Venture%20Debt.md) | removed an off-topic WACC glossary bullet; made the debt-vs-equity cost bullet specific |
| Careers | [Breaking Into VC](../vault/wiki/Careers/Breaking%20Into%20VC.md) | checked each bullet against the interview chapters; no factual errors found |
| Careers | [VC Interview Prep](../vault/wiki/Careers/VC%20Interview%20Prep.md) | checked each bullet against ch. 8–10 and 15; no factual errors found |
