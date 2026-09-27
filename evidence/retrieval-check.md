# Retrieval check before any model answers (2026-09-25)

Following "inspect retrieval first", the four pre-registered questions were run through the
retrieval tool alone (`BM25`, top 6, original-source passages only) before Gemma was involved.

## Run 1: one passage per PDF page / per book sub-heading (441 passages)

| Test | Expected passage | Rank found | Verdict |
|---|---|---|---|
| T1 check size | Harlem post p. 3 | **1** | pass |
| T2 how partners get paid | Book ch. 2 "How Does It Work?" | **1** (via query synonyms *paid → fee, salary, profit, carried interest*) | pass |
| T3 VC method, two sources | Book ch. 12 VC-method sections + Haas slides pp. 48–50 | book "Using the VC Method" rank 1; **slides p. 50 rank 22, p. 49 not in top 40; book "The Venture Capital Method" rank 16** | **FAIL (second source missing)** |
| T4 unsupported | none | Harlem pp. 1, 2, 5, 6 + book ch. 2 (related, none answer it) | as expected |

Run 1 top 6 for T3 (verbatim from the retrieval tool):

```
S1 18.43 cov 51% Break Into VC Book, Chapter 12: Returns and Valuation › Using the VC Method
S2 17.20 cov 58% Break Into VC Book, Chapter 12: Returns and Valuation › Rapid-Fire Questions
S3 16.52 cov 40% Break Into VC Book, Chapter 12: Returns and Valuation › Pre-Money and Post-Money Valuation
S4 15.67 cov 58% Break Into VC Book, Glossary
S5 15.54 cov 37% Break Into VC Book, Chapter 12: Returns and Valuation › In an Interview
S6 14.72 cov 50% Break Into VC Book, Chapter 12: Returns and Valuation › Where Is the Value?
```

**Cause.** A slide is a fragment. Slide p. 50 says only "Post money [post-investment] valuation …
$14.6m • Pre-money valuation is ……. $9.6m"; the words *VC Method* and *Mekasutra* are on slide
p. 48, and the formula is on p. 49. As single-page passages none of them matched the whole
question. Short book sub-sections ("Anticipated ROI in the VC Method", 75 words) had the same
problem. The slides also say "VC Method" while the question says "Venture Capital Method", and
the synonym list only expanded acronyms → words, not words → acronyms.

## Change

1. `retrieval.merge_short_sections`: merge runs of neighbouring short sections from the same PDF
   or the same book chapter until ~180 words, with range locators such as `pp. 48–50` and
   `Anticipated ROI in the VC Method … Using the VC Method`. (441 → 340 passages.)
2. `retrieval.PHRASES`: spelled-out phrases also add their acronym at half weight
   (*venture capital → vc*, *limited partner → lp*, …).

## Run 2 (after the change, same questions)

```
T1  S1 Harlem Capital Return the Fund Post, p. 3                          ← expected, rank 1
T2  S1 Break Into VC Book, Chapter 2: Early Stage Investing › How Does It Work?   ← expected, rank 1
T3  S1 Break Into VC Book, Chapter 12 › Rapid-Fire Questions
    S2 Break Into VC Book, Chapter 12 › Anticipated ROI in the VC Method … Using the VC Method   ← expected
    S3 Haas Venture Valuation Slides, pp. 80–82
    S4 Haas Venture Valuation Slides, pp. 48–50                            ← expected (Mekasutra)
    S5 Break Into VC Book, Chapter 12 › Pre-Money and Post-Money Valuation
    S6 Break Into VC Book, Glossary
T4  book ch. 2, Harlem pp. 1, 5, 2, 6, book ch. 2 "Why People Invest"     (none answer it; p. 6 holds the 3x–5x *target* trap)
```

T3 now retrieves both expected sources. T1, T2, and T4 were unaffected. The final ask-mode runs
in [evidence/ask/](ask/) use this index.

**Still imperfect:** the book passage that states the Syntax Health **post-money of $2.8M** is an
untitled continuation section (locator `Chapter 12: Returns and Valuation`) and is not in T3's
top 6. The `Using the VC Method` passage gives the $2.2M pre-money, but its formula was an image
in the EPUB and did not survive text extraction.

---

# Retrieval check for test set v2 and the beginner questions (2026-09-26)

Before any model answer, the new questions (T1 v2, T4 v2, B1–B8, and the fee question used in the
chat/ask separation check) were run through BM25 alone, top 6:

| Question | Expected passage | Found? |
|---|---|---|
| T1 v2: founder ownership given up at seed | seed-fund post p. 3 | **rank 1** |
| T2: how partners get paid | book ch. 2 "How Does It Work?" | rank 1 |
| T3: VC method, two sources | book "Using the VC Method" + slides pp. 48–50 | ranks 2 and 4 |
| T4 v2: hurdle rate before carry (unsupported) | none ("hurdle"/"preferred return" appear nowhere) | book ch. 2 return-of-capital rule at rank 1, as related material |
| B1: pre- vs post-money | book "Pre-Money and Post-Money Valuation" | rank 2 (rank 1 is the rapid-fire Q&A on the same topic) |
| B2: why "return the fund" | post p. 2 (fund-returner definition) | rank 1 |
| B3: dilution and how to limit it | post p. 4 (reserves for pro-rata) **and** glossary "Dilution" | p. 4 at rank 2; **glossary definition MISSED** (the question's other words pull in dilution-assumption passages instead) |
| B4: IRR over five years | book "Returns" (20–30% IRR) | rank 1 |
| B5: venture debt vs equity | book ch. 6 "Benefits" | rank 1 |
| B6: angel vs VC | book "Venture Capital and Angel Investing" | rank 2 (rank 1 is the glossary entry) |
| B7: SAFE (unsupported) | none ("SAFE"/"convertible note" appear nowhere) | only unrelated debt/equity passages, as expected |
| B8: why not value a startup like a mature company | slides pp. 22–26 (regular vs VC-funded company) **and/or** book "DCF Use Case in Venture Capital" | **book passage at rank 4; the slides are MISSED** |
| Fee question (chat/ask separation) | book ch. 2 "How Does It Work?" ("about 2 percent") | rank 1 |

**B8 is a paraphrase miss.** The question says "mature company"; the slides say "Regular Company"
vs "VC Funded Company". BM25 cannot bridge words that never co-occur.

## Experiment: model-based query expansion (tried, not adopted)

Idea: before searching, have Gemma rewrite the question into textbook keywords, search with both
the original and the rewrite, and merge the rankings with reciprocal rank fusion (the original
query at weight 1, the rewrite at weight *w*). Search mode would stay model-free.

Result over the 12 expected passages for the 10 answerable questions:

| Retrieval | Expected passages found | Missing |
|---|---|---|
| **BM25 only (current)** | **11 / 12** (top 6 or top 8) | B8 slides (B3's glossary entry was not in this experiment's list) |
| fusion, *w* = 0.5 or 0.7 | 10 / 12 | T3 slides pp. 48–50, B8 slides |
| fusion, *w* = 1.0 | 11 / 12 | T3 slides pp. 48–50 |

The expansions were sensible (e.g. "Valuation discrepancy, early-stage risk profile, discounted cash
flow modeling, comparable transactions"). At equal weight they did fix B8, but they pushed the
Mekasutra slides out of T3's evidence, and they add ~2 s and a model call before every answer. With
no net gain, **I kept plain BM25**. A local embedding model is the better next step for paraphrases
(see README → Reflection). The exact expansions Gemma produced are in [query-expansion-experiment.json](query-expansion-experiment.json).
