# Ask: What is dilution, and how can an early investor limit it?

- **Mode:** ask (standalone research, no chat history) · **Execution:** local · **Network:** offline (no route to internet)
- **Model:** `mlx-community/gemma-4-e2b-it-4bit` · **Runtime:** mlx-lm 0.31.3 / mlx 0.32.2 · **Device:** arm64 · macOS 15.6.1
- **Timing:** retrieval 2 ms · generation 8.8s (1999 prompt + 103 generated tokens, 23 tok/s)
- **Memory:** peak MLX 3.31 GB · process max RSS 2.19 GB
- **Timestamp:** 2026-09-26T15:01:29

## Answer (verbatim Gemma output)

Dilution is a factor in the return model, and it is the first major assumption in the return model [S2]. Dilution can be varied by industry and company [S2]. Investors may limit dilution by taking a pro-rata in their winners in the Series A to prevent dilution [S2]. Overall, investors typically assume 25 to 30% dilution by exit, and this total dilution can be 40% or more without the Series A pro-rata [S2].

## Citations

- [S2] Harlem Capital Return the Fund Post — `raw/Harlem Capital - Return the Fund.pdf`, p. 4

Automatic check:

- cited passages: 2
- citation check: PASS

## Retrieved passages (top 6, BM25 over original sources)

**[S1] Harlem Capital Return the Fund Post, p. 6** — `raw/Harlem Capital - Return the Fund.pdf` · score 9.18 · coverage 51% · id `harlem-return-the-fund:007`

> A fund may not need unicorns to
> return the fund, but it will need billions in value creation to meet the 3x-5x return
> goals.
> 
> Conclusion For Founders
> So…if you know an investors initial ownership and you make some dilution
> assumptions, you can back into what exit they are assuming for you to return the
> fund.
> 
> We encourage founders to think through some of this math because investors
> are taking a piece of your baby and you want to be aligned.
> 
> We also encourage
> founders to run this math for THEMSELVES.
> 
> You can replace the above analysis
> with founder equity.
> 
> We generally see co-founders after Seed rounds owning ~30%
> each.
> 
> Note the Series A dilution below as founders do not have pro-rata to prevent
> dilution, this leads to 38.8% total dilution instead of 23.5% for the investor.
> 
> Still not
> bad for a founder to take home $129mm though ;)

**[S2] Harlem Capital Return the Fund Post, p. 4** — `raw/Harlem Capital - Return the Fund.pdf` · score 8.83 · coverage 51% · id `harlem-return-the-fund:004`

> Step 3 — Dilution
> The dilution assumption is the first BIG guess in the return model. The previous
> example shows 23.5% total dilution by exit, which leads to 5.7% ownership at exit.
> Let’s look at the example of cutting the Series B and Series C round’s dilution by
> 50.0%, table on the right below. That leads to 12.1% dilution and 6.6% ownership at
> exit. That 0.9% ownership increase leads to an investor only needing a $605mm exit
> instead of a $700mm exit to return the fund, that’s $95mm (AKA a lot of money).
> Dilution Comparison
> So how does Harlem Capital think about dilution? It varies by industry and company
> (every VC answer), but we typically assume the Seed round is 25% (midpoint of 20 –
> 30%) and steps down 5% each round. Meaning, 20% for the Series A, 15% for the
> Series B, 10% for the Series C and 5% is the floor for Series D+ rounds. However, we
> reserve 30 – 40% of our fund for follow-ons to take our pro-rata in our winners in the
> Series A to prevent dilution. This is why there is 0% dilution in the Series A round
> above. Every fund has different follow-on reserves so ask them upfront. Overall, we
> usually assume 25 – 30% dilution by exit with our Series A pro-rata check. Note this
> total dilution is 40%+ without the Series A pro-rata so funds that don’t follow-on will
> require larger exits from founders. It is important to manage your dilution.

**[S3] Break Into VC Book, Chapter 12: Returns and Valuation › Valuation Divergence at the Early Stage** — `raw/Break Into VC - Bradley Miles.epub` · score 8.74 · coverage 66% · id `breakintovc-book:178`

> So, as early stage investors we won’t receive $15M on the Syntax Health deal, we’ll likely make somewhere between $3M and $5M or 6-10x our original investment.47
> 
> Due to the fund economics of early stage investing it may not make sense to do a pro-rata, or follow-on investment with a $5M Series A in order to maintain our 20 percent. As the entrepreneur continues to raise capital, the early stage investors will continue to experience a valuation dilution or divergence in their investor shares, effectively changing their ROI from investment to exit. The 30x ROI that early stage investors are gunning for actually doesn’t account for valuation divergence; the real ROI is something like 5-10x.48
> 
> Here’s a quick look at an early stage IRR table to see where angels and early stage investors need to target returns. We can see that the returns are much higher than what is typical at the growth stage because the risk profile of early stage investing is much higher as well.49

**[S4] Break Into VC Book, Chapter 2: Early Stage Investing › How Does It Work?** — `raw/Break Into VC - Bradley Miles.epub` · score 7.01 · coverage 49% · id `breakintovc-book:023`

> The average fund size of all venture capital stages is about $400M and the average venture capital deal size is $18M.1
> 
> The larger the firm’s stake in the company as shown in the account of all major shareholders, or capitalization table, the larger CynMerc’s returns are when the company makes an exit either through an initial public offering (IPO) or any mergers & acquisitions (M&A) activity.
> 
> Since Cynthia and Mercedes are partners at CynMerc, they will charge a management fee of about 2 percent to the limited partners in order to pay their own salaries, and the salaries of the associates and the support staff (you).
> 
> Once the limited partners receive 100 percent of their money back, Cynthia and Mercedes receive 20 percent of any additional profits while the limited partners receive 80 percent. The 20 percent that Cynthia and Mercedes receive is referred to as carried interest.

**[S5] Break Into VC Book, Chapter 4: Early Steps: Overall Research › Fabrice Grinda** — `raw/Break Into VC - Bradley Miles.epub` · score 6.99 · coverage 62% · id `breakintovc-book:037`

> Fabrice Grinda is a French entrepreneur and investor with over $300M in exits and 200 investments. He often blogs about venture investing and emerging tech trends. His “Macro perspective: The startup party is far from over!” article made me realize that venture-backed startups are staying private twice as long as they did in the 1990s because the cost to stay private these days has greatly decreased as capital becomes more accessible. He goes on to say that compliance burdens limit liquidity for small companies, and have also increased the cost of going public.

**[S6] Break Into VC Book, Chapter 2: Early Stage Investing › What Is Venture Capital?** — `raw/Break Into VC - Bradley Miles.epub` · score 6.80 · coverage 62% · id `breakintovc-book:020`

> Let’s say you and I decided to start a gluten-free grocery delivery service. We would likely need the support and financial resources of investors with domain expertise in our field to become successful.
> 
> If those investors received their money from several different sources who did not directly own a percentage of the portfolio companies, then those individuals are venture capitalists and they are receiving money from limited partners (these are endowments, foundations, public pensions, high net worth individuals etc.). In chapter 14, I will dive into what precisely makes a venture-backable business.
> 
> In this case, we can call venture capital the money we are receiving in order to grow our early stage business. When I use the term early stage, I am referring to both private businesses at ground zero, as well as mid-level private businesses that need assistance in order to reach further milestones.
> 
> The venture capital industry invests in businesses like our little ‘startup that could’—companies with huge risk and little-to-no proven track record—as well as growing businesses like Uber and Seamless that need help in any number of areas like continued branding or international expansion.
