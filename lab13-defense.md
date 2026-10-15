# Lab 13 — Portfolio Mandate Defense

## 1. Assignment identification

| Item | Detail |
|---|---|
| Lab | Lab 13 — Portfolio Mandate Defense |
| Token | CFA Investment |
| Partner and tools | ChatGPT (GPT-6), OpenAI Codex, Python. Confirm this disclosure reflects the tools actually used. |
| Submission method | GitHub links and Lab 13 quiz (student action required). |

## 2. Meridian Foundation case overview

Meridian Foundation manages a $100.0 million reserve and distributes $0.75 million each quarter. The task is to convert only measurable mandate restrictions into checks before any optimization. Twelve months of distributions require a reserve allocation of 3.0%: 4 × $0.75 million ÷ $100.0 million × 100. The checker evaluates total allocation, long-only status, reserve coverage, five-day liquidity, and non-exempt issuer concentration. It does not optimize a portfolio or forecast returns.

## 3. S1–S10 classifications

| Statement | Classification | Justification |
|---|---|---|
| S1 — Horizon seven years; annual rebalancing. | Hard constraint | Establishes a seven-year investment horizon and specifies annual portfolio rebalancing. It combines investment context with a management requirement. |
| S2 — CPI + 4% net of costs over rolling five-year periods. | Objective | Defines the portfolio's target return of CPI + 4% annually, net of costs, over rolling five-year periods. |
| S3 — $0.75 million quarterly payout; twelve months in cash or daily-liquid government securities. | Hard constraint | Requires liquid reserves sufficient to cover twelve months of quarterly distributions. |
| S4 — 60% global equities / 40% U.S. investment-grade bonds benchmark. | Preference | Establishes a performance benchmark without mandating an identical portfolio allocation. |
| S5 — Long-only; no borrowing, short sales, or derivatives. | Hard constraint | Prohibits borrowing, short selling, and derivatives. |
| S6 — No single issuer above 8%. | Hard constraint | Limits exposure to a single issuer to 8% of the portfolio. |
| S7 — Annual turnover at most 25% without approval. | Hard constraint | Limits annual turnover to 25% unless approved by the investment committee. |
| S8 — At least 90% redeemable within five business days. | Hard constraint | Requires at least 90% liquidity within five business days. |
| S9 — No calendar-year loss greater than 10%. | Unverifiable promise | The calendar-year loss limit cannot be guaranteed or properly tested without a defined measure and breach rule. |
| S10 — No sector, ESG, tax, or home-bias preference; optimization objective unspecified. | Missing | The CIO has not specified the optimization objective needed to guide portfolio construction. |

S4 is a reference benchmark, not a required 60/40 allocation. S9 is deliberately not coded as a pass/fail rule; it needs CIO clarification.

## 4. Investment Policy Statement

An investment policy statement (IPS) is the governing agreement that translates a client's goals, constraints, and decision rules into a portfolio mandate. It should establish what the client seeks to achieve and what the portfolio must or must not do.

Objectives and constraints work together. S2 supplies the return objective; S1 supplies the horizon; S3 and S8 specify liquidity; S5–S7 specify portfolio restrictions, issuer concentration, and turnover; and S4 provides a benchmark reference. S9 describes a loss outcome but lacks a measurement and breach definition, while S10 identifies missing optimization criteria. A portfolio must begin with this mandate because optimization cannot resolve an unspecified objective or choose among conflicting preferences.

Meeting the five coded checks establishes only mechanical compliance with inputs that can be measured today. It does not establish suitability, guarantee CPI + 4%, prevent investment losses, test turnover without transaction history, or determine how to optimize among eligible portfolios.

## 5. Python checker methodology

`mandate.py` keeps editable mandate inputs, holdings metadata, issuer exemptions, and candidate weights at the top of the file. `minimum_reserve_allocation()` computes the 3.0% reserve floor from distribution inputs. `assess_portfolio()` calculates the five supported rules:

1. Weights sum to 100.0%.
2. The lowest holding weight is at least 0.0%.
3. Reserve-eligible holdings meet the computed reserve floor.
4. Holdings redeemable within five business days total at least 90.0%.
5. Non-exempt securities are aggregated by company; the largest company total is at most 8.0%.

Cash, U.S. Treasury securities, and diversified funds are issuer-exempt. Acme Corp bonds and stock are aggregated. Annual turnover, future return performance, the benchmark, and S9 are disclosed as not mechanically tested because the supplied inputs do not support them.

## 6. Portfolios A/B/C compliance results

| Portfolio | Total | Minimum weight | Reserve eligible | Five-day liquidity | Largest company issuer | S9 | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| A | 100.0% pass | 0.0% pass | 14.0% pass | 100.0% pass | 0.0% pass | requires CIO clarification | passes every checkable rule |
| B | 100.0% pass | 0.0% pass | 1.0% FAIL | 85.0% FAIL | 9.0% FAIL | requires CIO clarification | fails 3 rule(s) |
| C | 100.0% pass | 0.0% pass | 2.0% FAIL | 100.0% pass | 8.0% pass | requires CIO clarification | fails 1 rule(s) |

These executed measurements match the assignment's reference results.

## 7. Negative-weight stress-test results

For the temporary probe only, portfolio A was changed to Cash = -2.0% and Global equity index fund = 64.0%; all other weights were unchanged. The computed results were total 100.0% pass, minimum weight -2.0% FAIL, reserve eligible 10.0% pass, five-day liquidity 100.0% pass, and largest company issuer 0.0% pass. The verdict was `fails 1 rule(s)`, so only long-only failed.

The submitted inputs were restored afterward: portfolio A contains Cash = 2.0% and Global equity index fund = 60.0%, and it again passes every checkable rule.

## 8. Candidate D portfolio and verification

Candidate D is intentionally very conservative. It demonstrates that present-tense rule compliance alone does not determine suitability; no expected return has been assumed or forecast.

| Holding | D allocation |
|---|---:|
| Cash | 90.0% |
| Treasury bills | 10.0% |
| Treasury 10-year note | 0.0% |
| Global equity index fund | 0.0% |
| Investment-grade bond fund | 0.0% |
| Private real estate fund | 0.0% |
| Acme Corp bonds | 0.0% |
| Acme Corp stock | 0.0% |

| Check | Measured result |
|---|---|
| Total allocation | 100.0% — pass |
| Minimum holding weight | 0.0% — pass |
| Reserve eligible | 100.0% — pass |
| Five-day liquidity | 100.0% — pass |
| Largest company issuer | 0.0% — pass |
| S9 | requires CIO clarification |
| Verdict | passes every checkable rule |

The suitability concern is S2: an all-cash-and-bills allocation may be inconsistent with the stated CPI + 4% return objective. That is an objection to be judged, not a forecast or an additional coded test.

## 9. Independent D assessment

Yes, the CIO has a reasonable basis to reject Portfolio D because allocating 90% to cash and 10% to Treasury bills may satisfy the measurable constraints without providing a credible path toward the foundation's return objective.

S2 supports this objection because the portfolio is intended to earn CPI + 4% annually, net of costs, over rolling five-year periods.

## 10. Skeptical partner review

**Skeptical-colleague challenge:** “Candidate D satisfies every measured restriction. Why should the CIO reject it instead of treating the return objective as merely aspirational?”

**Student response:** Passing every measurable constraint does not automatically make a portfolio suitable for the client. S2 establishes a return objective that must be considered during portfolio construction, even though achieving that return cannot be guaranteed.

## 11. One CIO question

My one question:

Should the portfolio optimization prioritize maximizing expected returns while respecting the mandate's constraints, or minimizing portfolio risk while targeting CPI + 4%?

The answer or decision that would change portfolio construction:

If the CIO prioritizes return maximization, the portfolio would likely take more exposure to growth-oriented assets. If minimizing risk is the priority, the allocation would generally favor more defensive assets while still seeking to satisfy the return objective.

## 12. Personal reflection

Question 1: Why can a portfolio pass every checkable rule but still be wrong for the client?

The checker only evaluates measurable restrictions such as liquidity, concentration, and allocation limits. A portfolio can satisfy all these requirements while taking an inappropriate level of risk or pursuing an allocation that does not align with the client's long-term investment objective.

Question 2: Which S1–S10 classification type was least clear?

S1 was the least clear because it combines a seven-year investment horizon with an annual rebalancing requirement. The horizon describes the client's investment circumstances, while the rebalancing frequency acts more like a portfolio management constraint.

## 13. Project 2 mandate

My client's identity or situation:

A young professional investing toward a home purchase in approximately five years.

My client's investment objective:

Grow invested capital to fund a future down payment while preserving sufficient liquidity as the purchase date approaches.

My client's hard constraints:

- Maintain at least 30% of the portfolio in cash or short-term U.S. Treasury securities.
- Hold only assets redeemable within five business days.
- Prohibit leverage, short selling, and derivatives.
- Limit exposure to any single non-exempt corporate issuer to 5%.
- Rebalance annually.

My one unresolved question for the client:

Is the home purchase date fixed or would the client be willing to delay purchasing if market conditions are unfavorable?

That answer would influence how much risk the portfolio can reasonably take as the anticipated withdrawal date approaches. This is the student's proposed client mandate; it is not an optimized or independently validated allocation.

## 14. Validation summary and submission checklist

- [x] S1–S10 classifications and justifications.
- [x] Python compliance checker and dynamic reserve minimum calculation.
- [x] Portfolio A/B/C validation.
- [x] Negative-weight stress test and restoration of original inputs.
- [x] Candidate D construction, verification, and independent assessment.
- [x] Skeptical-partner response.
- [x] One CIO question and portfolio-construction consequence.
- [x] Personal reflection and Project 2 client mandate.
- [x] Code-understanding exercise completed with ChatGPT. It correctly explained that `company_exposure[data["issuer"]] += weight` aggregates multiple securities issued by the same company for the issuer-concentration test; Acme bonds (5.0%) plus Acme stock (4.0%) equals 9.0%, exceeding the 8.0% limit for portfolio B.
- [x] Complete a final visual review of both files.
- [x] Confirm the partner/tools disclosure reflects actual use.
- [x] Commit and push the two files to the existing course repository, obtain direct GitHub links, and submit them with the token through the Lab 13 quiz.

The technical work and written responses are complete. Final student review and GitHub/quiz submission remain.
