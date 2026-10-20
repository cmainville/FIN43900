# FIN 41350 — Lab 14 Portfolio Baselines

## Status and source limits

The numerical work below was executed on 2026-10-20 with Python 3.14.7. The [instructor's Lab 14 assignment](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md), [student handout](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/student-handout.md), and [prework](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/student-prework.md) were reviewed in their public course repository because they were absent from this local folder. The instructor's repository identifies the course as **FIN 43900**, whereas the task heading says FIN 41350; the Lab 13 files here match the user's connected `cmainville/FIN43900` repository.

## COMPLETED BY CODEX — implemented and successfully tested

### Lab objective

The risk engine compares three transparent allocations using expected returns, individual volatilities, and all pairwise covariances. It shows whether each baseline meets Meridian's planning return objective and how much is in reserve-eligible Treasury securities. The CPI assumption of **2.5% is an estimate**, not an observed market figure. The objective is **CPI + 4.0% = 6.5%** using that estimate.

### Portfolio results

Executed `python3 portfolio.py` on 2026-10-20. All values below are actual displayed output, calculated from the inputs in `portfolio.py`.

| Portfolio | Weights: bills / 10-year / IG / equity | Expected return | Volatility | Reserve eligible | 6.5% objective |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0% / 0.0% / 40.0% / 60.0% | 6.80% | 10.46% | 0.0% | PASS |
| Equal Weight | 25.0% / 25.0% / 25.0% / 25.0% | 5.20% | 5.21% | 50.0% | FAIL |
| Inverse Volatility | 84.3% / 6.0% / 7.0% / 2.6% | 3.77% | 1.05% | 90.3% | FAIL |

Displayed inverse-volatility weights can total 99.9% because each is rounded to one decimal; the underlying weights sum to 100%.

### Test results

Executed `python3 -X pycache_prefix=/tmp/fin41350-pycache test_portfolio.py`: **6 tests passed (OK)**. The cache option bypassed an existing cloud-backed `mandate.py` bytecode file that stalled a first import attempt; it does not change the program or test inputs.

| Test | Actual result | Status |
|---|---|---|
| A — Known answers | All three displayed returns, volatilities, reserves, weights, and objective verdicts match the supplied answers. Output labels and precision checked. | PASS |
| B — Correlation sensitivity | Both IG/equity cells set to 0.50 in a copied matrix; benchmark volatility rounded to **11.00%**. Base matrix remains 0.25 in both cells. | PASS |
| C — Invalid correlation | Both copied IG/equity cells set to 1.3; `ValueError` reports correlation must be within `[-1, 1]`. | PASS |
| D — Matrix symmetry | Only one copied IG/equity cell set to 0.50; `ValueError` reports the matrix must be symmetric. | PASS |
| E — Dynamic calculations | A 1 percentage point increase in equity expected return raised benchmark expected return by **0.60 percentage points**; a 10% relative rise in equity volatility increased benchmark volatility and changed inverse-volatility weights. Base inputs remain 8.0% return and 16.0% volatility. | PASS |
| F — Regression | Original inputs still produced all three known answers; mandate candidates A–E also checked. | PASS |

### Candidate E — Meridian Benchmark

Executed `python3 mandate.py` after adding E. Its weights total 100.0%; minimum weight 0.0%; reserve eligible **0.0% — FAIL** against the unchanged 3.0% minimum; five-day liquidity 100.0% — pass; largest company issuer 0.0% — pass. It **fails one checkable rule**, the reserve requirement. A and D still pass all checkable rules; B still fails three (reserve, liquidity, issuer); C still fails one (reserve). The checker does not mechanically test future returns, turnover, or the S9 calendar-year-loss promise.

### Code explanation

`portfolio_variance_and_volatility(weights, covariances)` computes portfolio variance and volatility. Its nested `sum` visits every asset pair `(i, j)` and adds `weights[i] * weights[j] * covariances[i][j]`. Diagonal terms are each asset's weighted variance; off-diagonal terms incorporate co-movement. The function checks for a materially negative result and returns both variance and `math.sqrt(variance)` as volatility. `covariance_matrix(volatilities, correlations)` constructs each covariance as `volatilities[i] * volatilities[j] * correlations[i][j]` after validating the matrix. For the benchmark, the nonzero weights are 0.40 in IG bonds and 0.60 in global equity.

# STUDENT QUESTIONS — COMPLETE BEFORE SUBMISSION

## Part A — Diversification

**Where the assignment appears:** Open [the instructor's `lab-14-portfolio-baselines.md`](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md#diversification--learn-on-your-own) and find `## Diversification — Learn on your own`. Read its three questions. For the hand calculation, open [the student handout](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/student-handout.md#the-digits-once) and find the actual heading `## The digits, once` (the comma is in the source); use its benchmark values. If relevant, review the diversification reading in [student prework](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/student-prework.md).

1. What is diversification?

   MY ANSWER: [Complete this myself]

2. How does diversification work? Why can a correlation below +1 lower portfolio risk?

   MY ANSWER: [Complete this myself]

3. Calculate the benchmark's portfolio volatility by hand using the professor's supplied numbers.

   MY ANSWER: [Complete this myself]

   Blank calculation template (fill the professor's supplied values yourself):

   `σₚ = √(w_IG² σ_IG² + w_EQ² σ_EQ² + 2 w_IG w_EQ σ_IG σ_EQ ρ_IG,EQ)`

   `w_IG = ____` (investment-grade bond weight); `w_EQ = ____` (global equity weight)

   `σ_IG = ____` (bond volatility); `σ_EQ = ____` (equity volatility); `ρ_IG,EQ = ____` (their correlation)

   `σₚ = √(____________________________) = __________`

## Part B — Reflection

**Where the assignment appears:** Open [the instructor's `lab-14-portfolio-baselines.md`](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md#reflect) and find `## Reflect`. Read the two prompts. Use the verified portfolio table above as supporting material. The assignment says to explain these to your partner.

1. Why does the inverse-volatility portfolio allocate such a large percentage to Treasury bills?

   MY ANSWER: [Complete this myself]

2. Which of the three portfolio baselines would I present to Meridian's CIO first, and why?

   MY ANSWER: [Complete this myself]

## Part C — Code understanding

**Where the assignment appears:** Open `lab-14-portfolio-baselines.md` and find the instructions beginning `Explain the code`. In `portfolio.py`, find `portfolio_variance_and_volatility(weights, covariances)`. `weights` are portfolio allocations; `volatilities` are individual asset standard deviations in `covariance_matrix`; `correlations` are pairwise coefficients in that function; `covariances` is the resulting matrix passed to the volatility function. The nested sum uses each weight pair and covariance; the square root converts variance to volatility.

**Question to answer aloud:** Why does the double sum include both `(IG, equity)` and `(equity, IG)`, and how does that relate to the `2` in the two-asset formula?

MY ANSWER: [Complete this myself]

## Part D — Completion instructions

1. Open **`lab14-notes.md`** to type the personal answers.
2. Navigate to **`# STUDENT QUESTIONS — COMPLETE BEFORE SUBMISSION`**, then **`## Part A — Diversification`**, **`## Part B — Reflection`**, and **`## Part C — Code understanding`**. The source assignment headings are `## Diversification — Learn on your own`, `## Reflect`, and the instructions beginning `Explain the code` in `lab-14-portfolio-baselines.md`.
3. Replace each `MY ANSWER: [Complete this myself]` marker with your answer. Check the source files for the exact professor wording.
4. Part A, Question 3 requires the hand calculation using `student-handout.md` → `The digits once`.
5. The explanations in Part A, the choice and reasons in Part B, and the code explanation in Part C require your own understanding and judgment.
6. The instructor explicitly calls for individual submission, learning the diversification concept, working the benchmark by hand, and explaining reflection answers and code to a partner. The `## Checkout — on GitHub` section asks for **GitHub links of your files: md, py and/or other files as needed**. It does **not** explicitly say to submit these written conceptual responses. The answer spaces in this notes file are an additional organizational aid requested for this task; complete them personally before submission or discussion.

## MUST COMPLETE MYSELF — IN-CLASS ACTIVITIES

The following require your participation and are **not marked complete**:

- [ ] Paste the instructor's D question from the original assignment into your Lab 13 chat and respond there as directed.
- [ ] Explain to your partner why two risky assets can have lower combined volatility, using the benchmark's verified **10.46%** volatility.
- [ ] Ask AI to quiz you on the line of code you understand least; answer the quiz before receiving its explanation.
- [ ] Explain `portfolio_variance_and_volatility` line by line to your partner without AI assistance.
- [ ] Run your partner's `portfolio.py`; set an IG/equity correlation to **1.3**, verify rejection, then restore their original inputs.
- [ ] Complete your own diversification and reflection responses in the answer spaces under Parts A and B above; complete the code-understanding response under Part C.

## THURSDAY PREPARATION — separate from Tuesday checkout

These four funds form a coherent, investable starting universe for the **young professional's five-year home-purchase mandate proposed in `lab13-defense.md`**: short-term government exposure, intermediate Treasury duration, corporate credit, and global equity. The funds launched before the proposed five-year data window, and the selected sleeves can support the mandate's 30% short-term Treasury allocation and five-day liquidity in a proposed portfolio. A future optimizer still needs to enforce that 30% floor, issuer rule, and no-leverage rule. The 10-year Treasury sleeve has duration risk that matters for a five-year purchase horizon. The instructor specifically says the example tickers are for practice, not recommendations; choose or confirm this universe yourself for Project 2. Your Lab 13 home-purchase objective is qualitative, so **you must set its numeric return objective and identify the hard constraint** for Thursday's prework.

| Ticker | Fund name | Portfolio role | Verified fund source |
|---|---|---|---|
| BIL | State Street SPDR Bloomberg 1-3 Month T-Bill ETF | Treasury-bill exposure and short-term reserve sleeve | [State Street fund page](https://www.ssga.com/us/en/individual/etfs/state-street-spdr-bloomberg-1-3-month-t-bill-etf-bil) |
| IEF | iShares 7-10 Year Treasury Bond ETF | Intermediate Treasury bond exposure | [iShares fund page](https://www.ishares.com/us/products/239456/ishares-710-year-treasury-bond-etf) |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Investment-grade corporate bond exposure | [iShares fund page](https://www.ishares.com/us/products/239566/lqd-ishares-iboxx-investment-grade-corporate-bond-etf) |
| VT | Vanguard Total World Stock ETF | Global equity exposure | [Vanguard fund page](https://advisors.vanguard.com/investments/products/new/vt/vanguard-total-world-stock-etf) |

**Historical data status (2026-10-20): INCOMPLETE.** `prices.csv` was not created. The instructor specifies [Yahoo Finance → Historical Data → Monthly → Adj Close](https://finance.yahoo.com/). A Yahoo Finance adjusted-close chart request for BIL, using a five-year monthly interval, returned HTTP **429** on 2026-10-20. No adjusted-price rows were downloaded or verified for any of the four funds, so neither five-year completeness nor date alignment can be claimed. The fund pages verify the tickers and roles, but do not establish an aligned five-year adjusted-close series. An alternative documented source is [Alpha Vantage's monthly adjusted series](https://www.alphavantage.co/documentation/), which requires an API key. To finish: use Yahoo's Historical Data interface (or another legitimate adjusted-price source) to obtain dividend/split-adjusted monthly closes for **BIL, IEF, LQD, and VT**; export about five years through the latest common completed month; align on shared month-end dates; sort oldest first; verify no missing/nonpositive prices and roughly 60 monthly rows; then save `prices.csv` with columns `Date,BIL,IEF,LQD,VT`. Record each ticker's exact source, download date, adjustment definition, date range, and row count here. Do not substitute unadjusted market closes for the specified Adj Close series.

## READY FOR SUBMISSION — GitHub links and checkout

The instructor's actual `## Checkout — on GitHub` instruction is: **GitHub links of your files: md, py and/or other files as needed.** The Tuesday files for this implementation are `portfolio.py`, `mandate.py`, `test_portfolio.py`, and `lab14-notes.md`. Use direct links to the relevant `.md` and `.py` files once published to the course repository; `prices.csv` is Thursday preparation, not the Tuesday checkout. The source assignment is [Lab 14 → Checkout](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md#checkout--on-github).
