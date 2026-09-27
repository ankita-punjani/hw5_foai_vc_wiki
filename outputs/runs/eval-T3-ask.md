# Ask: How does the Venture Capital Method turn an expected exit value into a post-money and pre-money valuation? Use the examples in my notes.

- **Mode:** ask (standalone research, no chat history) · **Execution:** local · **Network:** offline (no route to internet)
- **Model:** `mlx-community/gemma-4-e2b-it-4bit` · **Runtime:** mlx-lm 0.31.3 / mlx 0.32.2 · **Device:** arm64 · macOS 15.6.1
- **Timing:** retrieval 2 ms · generation 8.4s (1988 prompt + 209 generated tokens, 35 tok/s)
- **Memory:** peak MLX 3.30 GB · process max RSS 2.32 GB
- **Timestamp:** 2026-09-27T11:51:58

## Answer (verbatim Gemma output)

To determine a post-money and pre-money valuation using the Venture Capital Method, the process involves the following steps [S6]:

1. Determine what a firm thinks a company will be worth at exit (anticipated post-money valuation) through market conditions and industry multiples [S6].
2. Divide this number by the anticipated return on investment (ROI) to arrive at a current post-money valuation [S6].
3. After subtracting the investment amount requested, the investor can arrive at an appropriate pre-money valuation [S6].

Examples from the evidence include:

*   For a healthcare startup, Syntax Health, an investment of $500,000 results in a pre-money valuation of $2.2 million [S2].
*   In a case, the required ownership was 20% of the company, and the post-money valuation was $14.6 million, leading to a pre-money valuation of $9.6 million [S4].

## Citations

- [S2] Break Into VC Book — `raw/Break Into VC - Bradley Miles.epub`, Chapter 12: Returns and Valuation › Anticipated ROI in the VC Method … Using the VC Method
- [S4] Haas Venture Valuation Slides — `raw/Haas VCPE 295B - Venture Valuation.pdf`, pp. 48–50
- [S6] Break Into VC Book — `raw/Break Into VC - Bradley Miles.epub`, Glossary

Automatic check:

- cited passages: 2, 4, 6
- citation check: PASS

## Retrieved passages (top 6, BM25 over original sources)

**[S1] Break Into VC Book, Chapter 12: Returns and Valuation › Rapid-Fire Questions** — `raw/Break Into VC - Bradley Miles.epub` · score 18.19 · coverage 60% · id `breakintovc-book:191`

> Q. What is precedent transactions analysis?
> 
> A. Similar to comps, except here you create a universe of completed deals within the past five years to find an industry average multiple. The product of that multiple and the target company’s EBITDA or sales will give us enterprise value.
> 
> Q. Which technique will give us the highest valuation?
> 
> A. Likely precedent transactions analysis since there is a built-in control premium when a company is purchased.
> 
> Q. How do you value a company without cash flows?
> 
> A. If the company has assets on hand we can use the asset-backed valuation method, if not we can use the venture capital method to back out a post-money valuation based on the anticipated enterprise value and ROI in the exit year. Once we have post-money valuation we can simply subtract the amount they are asking for to arrive at a pre-money valuation.
> 
> Q. Besides the VC method, are there any other ways to value a company pre-revenue?

**[S2] Break Into VC Book, Chapter 12: Returns and Valuation › Anticipated ROI in the VC Method … Using the VC Method** — `raw/Break Into VC - Bradley Miles.epub` · score 17.44 · coverage 53% · id `breakintovc-book:175`

> [Anticipated ROI in the VC Method]
> As discussed earlier, ROIs are cash-on-cash multiples of the money VCs or angels originally invested. Since the method skews towards very early stage companies, the anticipated ROIs are much higher because there is more risk towards the beginning of the business. An anticipated seed stage ROI is typically in the ballpark of 30x, compared to maybe 5-7x at the growth stage. I’ll talk about why the ROI is so large towards the end of the section.
> 
> [Using the VC Method]
> Now that we have an enterprise value at an exit of $84M and a target ROI at an exit of 30x, we can use our formula.
> 
> Now that we have the post-money valuation and know the investment amount, we can arrive at a pre-money valuation for our health care startup.
> 
> Since our healthcare startup, Syntax Health is asking for an investment of $500k this gives them a pre-money valuation of $2.2M.

**[S3] Haas Venture Valuation Slides, pp. 80–82** — `raw/Haas VCPE 295B - Venture Valuation.pdf` · score 16.37 · coverage 60% · id `haas-venture-valuation:028`

> NanoChon
> premoney $ 100 
> money $ 20.0 
> post money 120
> ownership 27%
> Total
> Owner- Ownership Probable probable
> Exits Rounds ship value Multiple Time IRR Probability value value
> $ 500 3 10% $ 52 13.0 10 29% 10.0% $ 5.18 26.67 
> $ 500 2 16% $ 80 19.9 6 65% 10% $ 7.97 
> $ 500 1 27% $ 135 33.8 3 223% 10% $ 13.51 Multiple
> $ - 1 27% - - 2 70% $ - 6.67 
> Productive.ai
> 
> ? ?
> ? ?
> Methods of VC Valuation
> Stage of Growth
> Investment
> Type
> Late
> VC
> Traditional
> Early
> 94
> Venture Capital 
> Method
> Projection 
> Reflection
> Comparables
> Scenario Analysis
> 
> VC Valuation
> • To repeat:
> – Art, not science
> – There are no right answers
> – Methods are “precise” , but not “accurate”
> – Assumptions are key, can “overwhelm” the math

**[S4] Haas Venture Valuation Slides, pp. 48–50** — `raw/Haas VCPE 295B - Venture Valuation.pdf` · score 16.08 · coverage 56% · id `haas-venture-valuation:015`

> Case data
> • $250m future market value (according to Krusty)
>  
> • 50% IRR desired 
> • Over 7 years
> • $5,000,000 investment
> Mekasutra Games – VC Method
> 
> Investor Ownership 
> Expectations
> Investment
> Expected PV =Ownership
> required
> Future Value
> (1+Necessary IRR)n(years)=
> =Future Value Revenue (year n)X Revenue multiple
> How much ownership will the investor want/require?
> 60
> $250m future market value (according to Krusty)
> $250m Future Value
> =Expected 
> Present Value (1 + 50% IRR)7 years = $14.6m
> $5m
> $14.6m
> = 34%
> Requirement or negotiation?
> “We typically require 20% of the company…”
> 
> So the Company’s Valuation is…..
> • Post money [post- investment] valuation ……. $14.6m
> • Pre-money valuation is……. $9.6m
> 61
> Room to negotiate – anything below $9.6m is good for 
> investor

**[S5] Break Into VC Book, Chapter 12: Returns and Valuation › Pre-Money and Post-Money Valuation** — `raw/Break Into VC - Bradley Miles.epub` · score 15.97 · coverage 39% · id `breakintovc-book:150`

> Before we dive into pre- and post-money valuation let’s define “money” as the amount of venture capital invested in a round of financing. Now we can understand post-money valuation as the value of a company, immediately after the latest amount of venture capital is invested.
> 
> Therefore, pre-money valuation is the value of a company before that latest round of capital has been invested. This is typically the value of the idea, opportunity, the management team and perhaps any patents or intellectual property that comes with the founders. Distilling our understanding of pre- and post-money valuation, it must be that:
> 
> Key differences between the two are the timing of the valuation and ownership stake.

**[S6] Break Into VC Book, Glossary** — `raw/Break Into VC - Bradley Miles.epub` · score 15.94 · coverage 56% · id `breakintovc-book:300`

> Valuation Divergence
> 
> Popularized by the late angel investor, Luis Villalobos, the phenomena of a venture’s value increasing and its early stage private shares increasing at a much lower rate. Early stage investors will experience a cash-on-cash ROI decrease or valuation divergence of as much as 3-5x.
> 
> Venture Capital Method
> 
> Determining what a firm thinks a company will be worth at exit (anticipated post-money valuation) through market conditions and industry multiples, then dividing this number by the anticipated return on investment (ROI) to arrive at a current post-money valuation. After subtracting the investment amount requested, the investor can arrive at an appropriate pre-money valuation.
> 
> Venture Capitalists
> 
> A group of investors who receive their money from several different sources who do not share in direct ownership of the portfolio companies. Venture capitalists invest in early- to mid-stage private companies in order to earn large returns on the investment.
> 
> Venture Debt
