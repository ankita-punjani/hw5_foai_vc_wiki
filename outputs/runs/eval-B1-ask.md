# Ask: What is the difference between pre-money and post-money valuation?

- **Mode:** ask (standalone research, no chat history) · **Execution:** local · **Network:** offline (no route to internet)
- **Model:** `mlx-community/gemma-4-e2b-it-4bit` · **Runtime:** mlx-lm 0.31.3 / mlx 0.32.2 · **Device:** arm64 · macOS 15.6.1
- **Timing:** retrieval 54 ms · generation 5.8s (1763 prompt + 55 generated tokens, 22 tok/s) · model load 4.6s
- **Memory:** peak MLX 3.34 GB · process max RSS 2.19 GB
- **Timestamp:** 2026-09-26T15:01:09

## Answer (verbatim Gemma output)

The pre-money valuation is the value of a company before an investment, while the post-money valuation is the value of the company after an investment [S2]. The key differences between the two are the timing of the valuation and the ownership stake [S2].

## Citations

- [S2] Break Into VC Book — `raw/Break Into VC - Bradley Miles.epub`, Chapter 12: Returns and Valuation › Pre-Money and Post-Money Valuation

Automatic check:

- cited passages: 2
- citation check: PASS

## Retrieved passages (top 6, BM25 over original sources)

**[S1] Break Into VC Book, Chapter 12: Returns and Valuation › Rapid-Fire Questions** — `raw/Break Into VC - Bradley Miles.epub` · score 17.62 · coverage 100% · id `breakintovc-book:193`

> Q. What is the difference between a pre and post-money valuation?
> 
> A. The pre-money valuation is the value of a company before we invest while the post-money valuation is the value of a company after we invest.
> 
> Q. If a company had a $500k post-money valuation and we invested $250k, how much of the company do we own?
> 
> A. We own 50 percent since the post-money valuation implies that the money was already invested.
> 
> Q. If a company had a $500k pre-money valuation and we invested $250k, how much of the company do we own?
> 
> A. We own ~33.3 percent of the company, since the company is now valued at $750k and we invested $250k.

**[S2] Break Into VC Book, Chapter 12: Returns and Valuation › Pre-Money and Post-Money Valuation** — `raw/Break Into VC - Bradley Miles.epub` · score 17.12 · coverage 100% · id `breakintovc-book:150`

> Before we dive into pre- and post-money valuation let’s define “money” as the amount of venture capital invested in a round of financing. Now we can understand post-money valuation as the value of a company, immediately after the latest amount of venture capital is invested.
> 
> Therefore, pre-money valuation is the value of a company before that latest round of capital has been invested. This is typically the value of the idea, opportunity, the management team and perhaps any patents or intellectual property that comes with the founders. Distilling our understanding of pre- and post-money valuation, it must be that:
> 
> Key differences between the two are the timing of the valuation and ownership stake.

**[S3] Break Into VC Book, Chapter 12: Returns and Valuation › In an Interview** — `raw/Break Into VC - Bradley Miles.epub` · score 14.46 · coverage 81% · id `breakintovc-book:154`

> If the pre-money investment represents 20 percent of the total or 1/5th, the post-money investment should represent 25 percent or 1/4th of the total.
> 
> For instance, if we invest $250k at a pre-money valuation of $1M this gives the company $1.25M in total capital and we get 20 percent ownership as investors. As a post-money question, if we invested $250k at a post-money valuation of $1M we own 25 percent of the company.
> 
> Alternatively, if we invest $500k at a pre-money valuation of $1M, the company now has $1.5M in total capital and we as investors own ~33.3 percent or 1/3rd of the company. If asked as a post-money question with the same investment amount, the post-money valuation is $1M and the $500k investment now represents 50 percent investor ownership of the company. Huge difference.
> 
> These are fundamental questions that may be posed very early in the interview, so try to create quick little pre- and post-money valuation questions to ace this part of the process!

**[S4] Break Into VC Book, Chapter 12: Returns and Valuation › Rapid-Fire Questions** — `raw/Break Into VC - Bradley Miles.epub` · score 13.50 · coverage 100% · id `breakintovc-book:192`

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

**[S5] Break Into VC Book, Chapter 12: Returns and Valuation › In an Interview** — `raw/Break Into VC - Bradley Miles.epub` · score 11.63 · coverage 55% · id `breakintovc-book:153`

> In the simple universe of these interview examples, let npre equal the number of times the investment amount in a pre-money example can factor into the pre-money valuation—any whole number from 2 to 5—where 1/npre equals the proportion of the company that the investor owns after adding the investment amount to the pre-money valuation (e.g. 1/5 means 20 percent investor ownership etc.).
> 
> All else being equal, the same amount invested in the post-money valuation example represents a greater proportion of investor ownership. If the pre- and post-money valuations are the same in a given question and the amount invested is the same as well, you can think of investor ownership in the post-money valuation example as 1/(npre-1).
> 
> If the pre-money investment represents 20 percent of the total or 1/5th, the post-money investment should represent 25 percent or 1/4th of the total.

**[S6] Break Into VC Book, Chapter 12: Returns and Valuation › In an Interview** — `raw/Break Into VC - Bradley Miles.epub` · score 10.98 · coverage 55% · id `breakintovc-book:155`

> Here is a quick table to summarize, where “Pre” represents the investment amount as a proportion of the pre-money valuation and “Post” represents the investment amount as a proportion of the post-money valuation. In the table below any pre-money investment amount represents 1/n of the total committed capital or paid-in capital (PIC). That same investment considered in a post-money valuation scenario makes up 1/(npre-1) of the total committed capital.
