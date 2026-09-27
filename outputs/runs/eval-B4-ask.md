# Ask: What IRR do venture investors typically expect over a five-year investment?

- **Mode:** ask (standalone research, no chat history) · **Execution:** local · **Network:** offline (no route to internet)
- **Model:** `mlx-community/gemma-4-e2b-it-4bit` · **Runtime:** mlx-lm 0.31.3 / mlx 0.32.2 · **Device:** arm64 · macOS 15.6.1
- **Timing:** retrieval 1 ms · generation 4.5s (2216 prompt + 69 generated tokens, 36 tok/s)
- **Memory:** peak MLX 3.33 GB · process max RSS 2.85 GB
- **Timestamp:** 2026-09-27T11:53:12

## Answer (verbatim Gemma output)

Investors typically anticipate a 20-30 percent internal rate of return (IRR) over a 5-year investment time horizon [S1]. This return range lands between 2.5-4.0x, which is described as "two and a half to four times" the original money invested [S1].

## Citations

- [S1] Break Into VC Book — `raw/Break Into VC - Bradley Miles.epub`, Chapter 12: Returns and Valuation › Returns

Automatic check:

- cited passages: 1
- citation check: PASS

## Retrieved passages (top 6, BM25 over original sources)

**[S1] Break Into VC Book, Chapter 12: Returns and Valuation › Returns** — `raw/Break Into VC - Bradley Miles.epub` · score 22.53 · coverage 73% · id `breakintovc-book:147`

> A venture capitalist is expecting a certain return over a time horizon when they invest in a company. Over a 5-year investment time horizon, investors typically anticipate a 20-30 percent internal rate of return (IRR) which lands anywhere between 2.5-4.0x, or “two and a half to four times” the original money invested. The internal rate of return is an annualized growth rate that accounts for cash inflows and outflows within the period.
> 
> Compared to simply compounding the annual growth rate of an investment, IRR is considered a better way to measure profitability over time expressly because it accounts for all cashflows, or in other words makes the net present value (NPV) of all cash inflows and outflows equal to zero.
> 
> While it is difficult and unnecessary to know how to calculate IRR in an interview given the proper inputs, there are a few quick numbers you can memorize and put to use that may benefit you greatly in an interview.

**[S2] Haas Venture Valuation Slides, pp. 48–50** — `raw/Haas VCPE 295B - Venture Valuation.pdf` · score 17.64 · coverage 53% · id `haas-venture-valuation:015`

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

**[S3] Break Into VC Book, Chapter 12: Returns and Valuation › Returns** — `raw/Break Into VC - Bradley Miles.epub` · score 12.52 · coverage 37% · id `breakintovc-book:148`

> If ever IRR is discussed in an interview, investors are usually referring to a 5-year time horizon. The chart below is a standard IRR table which tells us the return multiples for a given IRR as long as we know the years invested.38
> 
> The shaded green cells represent the IRRs that are at or above the desired return given the years invested. If we want 4 times our investment in 5 years we need about a 30 percent IRR.
> 
> These questions are common in private equity interviews and may arise in venture capital interviews as well, however they will usually associate with a 5-year time horizon.
> 
> When an interviewer discusses IRR over a 5-year period, they may associate a 1.5x return with ~10 percent IRR, 2x with 15 percent IRR, 3x with 25 percent IRR, 4x with ~30 percent IRR, 5x with 40 percent IRR and 6x with 45 percent IRR. Given any amount invested and any IRR, we can now easily find the money returned or ROI. We’ll take a closer look during the rapid-fire questions.

**[S4] Break Into VC Book, Chapter 12: Returns and Valuation › Rapid-Fire Questions** — `raw/Break Into VC - Bradley Miles.epub` · score 11.44 · coverage 38% · id `breakintovc-book:192`

> Q. Besides the VC method, are there any other ways to value a company pre-revenue?
> 
> A. Sure, there are a number of methods developed by angel investors like Bill Payne and Dave Berkus. These are based on the management team and other risk factors. Typically these early stage pre-money valuations are between $2M and $3M.
> 
> Q. What does the football field tell us?
> 
> A. It gives us a range for each valuation method, allowing us to pinpoint an average valuation for the given company.
> 
> Q. If I invested $1M at a 25 percent IRR over a 5-year period what is my return?
> 
> A. About 2.5x, so $2.5M.
> 
> Q. Let’s take that same amount and say we did a little better when we invested it over the next five years at a 30 percent IRR. What is my return?
> 
> A. A little more than 4x, so a little more than $10M.
> 
> Q. What is the difference between a pre and post-money valuation?

**[S5] Break Into VC Book, Chapter 5: Growth Equity › Investment Thesis** — `raw/Break Into VC - Bradley Miles.epub` · score 11.19 · coverage 40% · id `breakintovc-book:049`

> A venture capital firm invests under the premise of an upside scenario, this is to say that if the firm invests in 10 companies through the fund, they only expect one or two companies to hit a home run (an 8-10x return or more), and couple solid returns ( >1x), while the other six or seven companies may fail (no return) or simply return the amount invested (a 1x return). Of course, they’d like to see more successes but typically a venture capital firm only gains a return from a small portion of their investments.
> 
> Since these firms are investing at an earlier stage and have a high risk profile, early stage venture firms seek higher returns than growth equity firms. A target or anticipated cash-on-cash return on investment (ROI), or multiple of the amount of cash invested, is typically 8-10x for early stage venture capital investors.4, 5
> 
> A quick seven-figure exit may suffice in venture capital, but it is simply not enough to generate positive returns in growth equity. In this space, late-stage investors will act only if they see the potential for a firm to become a market leader in their industry. In other words, while both venture capital and growth equity firms are looking for the next Seamless, Uber or Netflix, the evidence of a startup becoming a market leader needs to be much stronger in growth equity. Since the risk profile is relatively lower compared to traditional venture capital, target ROI here is a little lower and typically exists in the 3-5x range.6

**[S6] Haas Venture Valuation Slides, pp. 51–52** — `raw/Haas VCPE 295B - Venture Valuation.pdf` · score 11.05 · coverage 41% · id `haas-venture-valuation:016`

> Future Capital Influences Answer
> Investment
> Expected PV =Ownership
> required
> Future Value
> (1+Necessary IRR)n(years)=
> =Future Value Revenue (year n)X Revenue multiple
> How much ownership will the investor want/require?
> 62
> $250m future market value (according to Krusty)
> $250m Future Value
> =Expected 
> Present Value (1 + 50% IRR)7 years = $14.6m
> $5m
> $14.6m
> = 34%
> Example: Next round investor needs 15% ownership (based on similar VC method) 
> $5m
> * (1 - .15)
> $12.4m
> $12.4m
> 40%
> $12.4 - $5 = $7.4m premoney
> 
> VC Method
> • Pros: Includes growth, current and future cash 
> needs, fundraising environment
> – Future cash flow projections are difficult to determine, 
> notional, or fictitious
> – “No plan survives first contact with the enemy.” 
>  - Helmuth von Molke, (paraphrased)
> – Terminal value equally difficult
> – Single number (discount rate) struggles to incorporate all 
> aspects of risk
> – Disconnected from cost of capital
> – 60%? 50%? 40%? 80%? 
> – Decision overwhelms cash flow assumptions
> • Cons: NPV, etc. challenging at early stages
