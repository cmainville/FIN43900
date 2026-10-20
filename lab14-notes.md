# FIN 43900 — Lab 14 Portfolio Baselines

## Status and source limits

The numerical work below was executed on 2026-10-20 with Python 3.14.7. The [instructor's Lab 14 assignment](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md), [student handout](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/student-handout.md), and [prework](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/student-prework.md) were reviewed in their public FIN 43900 course repository. The Lab 13 files here match the student's `cmainville/FIN43900` repository.

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

   MY ANSWER: Diversification is a way to reduce portfolio risk by spreading investments across different assets. Combining investments that do not move exactly together can help smooth out overall portfolio volatility.

2. How does diversification work? Why can a correlation below +1 lower portfolio risk?

   MY ANSWER: Diversification works by combining investments whose returns are not perfectly correlated. When one investment performs poorly, another may perform better or decline less. A correlation below +1 creates opportunities to reduce overall portfolio volatility because the assets do not move perfectly together.

3. Calculate the benchmark's portfolio volatility by hand using the professor's supplied numbers.

   MY ANSWER: The two-asset portfolio-volatility formula is:

   $$\sigma_p = \sqrt{w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\sigma_1\sigma_2\rho}$$

   Using the benchmark's weights, volatilities, and correlation:

   $$\sigma_p = \sqrt{(0.40^2 \times 0.06^2) + (0.60^2 \times 0.16^2) + 2(0.40)(0.60)(0.06)(0.16)(0.25)}$$

   $$\sigma_p = \sqrt{0.000576 + 0.009216 + 0.001152}$$

   $$\sigma_p = \sqrt{0.010944}$$

   **Portfolio volatility = 10.46%**

## Part B — Reflection

**Where the assignment appears:** Open [the instructor's `lab-14-portfolio-baselines.md`](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md#reflect) and find `## Reflect`. Read the two prompts. Use the verified portfolio table above as supporting material. The assignment says to explain these to your partner.

1. Why does the inverse-volatility portfolio allocate such a large percentage to Treasury bills?

   MY ANSWER: Inverse-volatility weighting allocates more capital to investments with lower volatility. Since Treasury bills have the lowest volatility at 0.5%, compared with 6% for investment-grade bonds and 16% for equities, they receive the largest allocation at approximately 84.3%.

2. Which of the three portfolio baselines would I present to Meridian's CIO first, and why?

   MY ANSWER: I would present the benchmark first because it is the only portfolio with an expected return above Meridian's 6.5% objective, at 6.8%. However, it fails the 3% reserve requirement because it has no allocation to reserve-eligible assets. I would use it as a starting point and explain that the portfolio needs to be adjusted to satisfy the mandate before it could be recommended.

## Part C — Code understanding

**Where the assignment appears:** Open `lab-14-portfolio-baselines.md` and find the instructions beginning `Explain the code`. In `portfolio.py`, find `portfolio_variance_and_volatility(weights, covariances)`. `weights` are portfolio allocations; `volatilities` are individual asset standard deviations in `covariance_matrix`; `correlations` are pairwise coefficients in that function; `covariances` is the resulting matrix passed to the volatility function. The nested sum uses each weight pair and covariance; the square root converts variance to volatility.

**Question to answer aloud:** Why does the double sum include both `(IG, equity)` and `(equity, IG)`, and how does that relate to the `2` in the two-asset formula?

MY ANSWER: The double sum includes both combinations because it calculates the covariance contribution for every pair of assets. Since covariance is symmetric, the IG-equity and equity-IG terms are equal. Adding both terms is equivalent to multiplying their shared covariance contribution by 2 in the two-asset portfolio-volatility formula.

## MUST COMPLETE MYSELF — IN-CLASS ACTIVITIES

The oral and partner activities below still require your participation. The student-provided written answers are marked complete.

- [ ] Paste the instructor's D question from the original assignment into your Lab 13 chat and respond there as directed.
- [ ] Explain to your partner why two risky assets can have lower combined volatility, using the benchmark's verified **10.46%** volatility.
- [ ] Ask AI to quiz you on the line of code you understand least; answer the quiz before receiving its explanation.
- [ ] Explain `portfolio_variance_and_volatility` line by line to your partner without AI assistance.
- [ ] Run your partner's `portfolio.py`; set an IG/equity correlation to **1.3**, verify rejection, then restore their original inputs.
- [x] Six finalized diversification, reflection, and code-understanding responses supplied by the student and inserted above. The oral explanations and partner exercises remain open.

## THURSDAY PREPARATION — separate from Tuesday checkout

The student has selected **BIL, IEF, LQD, and VT** as the four-fund universe for the **young professional's five-year home-purchase mandate in `lab13-defense.md`**. The funds cover Treasury-bill reserves, intermediate government bonds, investment-grade corporate bonds, and global equity. The mandate's existing hard constraints remain: at least 30% in cash or short-term U.S. Treasuries, five-business-day liquidity, no leverage/short sales/derivatives, a 5% non-exempt corporate issuer limit, and annual rebalancing. A future optimizer must enforce these constraints. IEF's duration risk matters for a five-year purchase horizon. The personal return objective remains qualitative; **the student must decide its numeric target**. No target was invented here.

| Ticker | Fund name | Portfolio role | Verified fund source |
|---|---|---|---|
| BIL | SPDR Bloomberg 1-3 Month T-Bill ETF | Cash equivalent and Treasury-bill reserves | [State Street fund page](https://www.ssga.com/us/en/individual/etfs/state-street-spdr-bloomberg-1-3-month-t-bill-etf-bil) |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government bonds | [iShares fund page](https://www.ishares.com/us/products/239456/ishares-710-year-treasury-bond-etf) |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Investment-grade corporate bonds | [iShares fund page](https://www.ishares.com/us/products/239566/lqd-ishares-iboxx-investment-grade-corporate-bond-etf) |
| VT | Vanguard Total World Stock ETF | Global equities | [Vanguard fund page](https://advisors.vanguard.com/investments/products/new/vt/vanguard-total-world-stock-etf) |

### Historical adjusted prices — incomplete

**Target:** 60 completed months, October 2021 through September 2026 inclusive, with USD adjusted closes for all four ETFs. The output dates would be calendar month-ends (`2021-10-31` through `2026-09-30`); these labels can differ from the source's final trading dates. October 2026 is excluded.

**Retrieval attempt: 2026-10-20.** The instructor specifies Yahoo Finance **Historical Data → Monthly → Adj Close**. A normal request to [Yahoo's BIL monthly chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/BIL?range=5y&interval=1mo&events=history&includeAdjustedClose=true) returned HTTP **429**. No BIL, IEF, LQD, or VT adjusted-price file was downloaded. The fund pages above establish fund identities and roles, not historical adjusted-price observations. [Yahoo's definition of Adj Close](https://in.help.yahoo.com/kb/finance/adjusted-close-sln28256.html) accounts for splits and dividends. That methodology would be comparable if all four series came from Yahoo's same `Adj Close` field, but the actual four series have **not** been obtained or compared.

| Ticker | Yahoo historical-data page | Price download date | Verified monthly Adj Close observations |
|---|---|---|---:|
| BIL | [Yahoo BIL](https://finance.yahoo.com/quote/BIL/history/) | None | 0 of 60 |
| IEF | [Yahoo IEF](https://finance.yahoo.com/quote/IEF/history/) | None | 0 of 60 |
| LQD | [Yahoo LQD](https://finance.yahoo.com/quote/LQD/history/) | None | 0 of 60 |
| VT | [Yahoo VT](https://finance.yahoo.com/quote/VT/history/) | None | 0 of 60 |

Documented alternatives include [Alpha Vantage's `TIME_SERIES_MONTHLY_ADJUSTED`](https://www.alphavantage.co/documentation/), [Tiingo's adjusted end-of-day prices](https://www.tiingo.com/documentation/end-of-day), and [EODHD's adjusted close](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes). They identify dividend/split-adjusted fields but require account credentials or entitlements for these four complete histories; none was available for this work. No ordinary `Close` values were substituted.

**Validation report (2026-10-20):** source prices unavailable; output `prices.csv` absent; observation count **0/60**; requested date range **2021-10-31 to 2026-09-30**; valid observations **BIL 0, IEF 0, LQD 0, VT 0**; missing months **60 per ETF**; duplicate months **not assessable**; shared monthly index **not established**; overall **FAIL / incomplete**. This is an availability failure, not a claim that a bad dataset was validated.

[`import_prices.py`](https://github.com/cmainville/FIN43900/blob/main/import_prices.py) is a standard-library importer for four **manually downloaded Yahoo CSV files**. It requires the `Adj Close` column, accepts either monthly files or daily files (selecting the final available trading-day observation of each month), rejects invalid or missing values and months, labels output rows at calendar month-end, and writes `prices.csv` only after all 60 months pass validation. Run it after obtaining the four authentic files:

```bash
python import_prices.py --frequency monthly --bil BIL.csv --ief IEF.csv --lqd LQD.csv --vt VT.csv --output prices.csv
python import_prices.py --validate-only prices.csv
```

If Yahoo exports daily data instead, use `--frequency daily`. Download the same October 2021–September 2026 span for each ETF, confirm all four source files show Yahoo's `Adj Close`, record **each actual download date** here, then run the importer and review its printed source, count, range, per-ticker valid counts, missing/duplicate months, and PASS/FAIL. The script cannot authenticate a file's provenance from its column name alone; keep the original four downloads for audit. **Do not submit `prices.csv` until it exists and the importer reports PASS.**

## READY FOR SUBMISSION — GitHub links and checkout

The instructor's actual `## Checkout — on GitHub` instruction is: **GitHub links of your files: md, py and/or other files as needed.** The Tuesday implementation files are [portfolio.py](https://github.com/cmainville/FIN43900/blob/main/portfolio.py), [mandate.py](https://github.com/cmainville/FIN43900/blob/main/mandate.py), [test_portfolio.py](https://github.com/cmainville/FIN43900/blob/main/test_portfolio.py), and [lab14-notes.md](https://github.com/cmainville/FIN43900/blob/main/lab14-notes.md). The source assignment is [Lab 14 → Checkout](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md#checkout--on-github). The six student-provided written responses are now present; the in-class oral and partner activities remain open. `prices.csv` is Thursday preparation and remains incomplete. The importer is published as a way to finish it from authentic files.
