# Lab 11 — IBM One-at-a-Time Sensitivity Analysis

## Question and method

**Question:** Which assumptions drive IBM's forecast and value, and what explains their effects?

This analysis uses the existing Lab 10 IBM pro-forma and FCFE valuation model without rebuilding it. For every case, the runner restores the Lab 10 base inputs, changes only the named driver, runs the linked statements and valuation, and applies the existing accounting checks. Currency amounts are USD millions except per-share value.

## Operating drivers and ranges

| Driver | Units and years | Lower | Base | Higher | Range reason |
| --- | --- | --- | --- | --- | --- |
| Software revenue growth | YoY growth; FY2026E–FY2030E | 6.0% / 5.0% / 4.0% / 3.5% / 3.0% | 8.0% / 7.0% / 6.0% / 5.5% / 5.0% | 10.0% / 9.0% / 8.0% / 7.5% / 7.0% | Judgment: ±2.0 percentage points around base. It brackets IBM's FY2025 9.1% constant-currency Software growth and Q2 2026 5% growth while preserving the base fade. |
| Cash gross margin | Cash gross profit / revenue; FY2026E–FY2030E | 59.5% / 59.8% / 60.1% / 60.3% / 60.5% | 60.5% / 60.8% / 61.1% / 61.3% / 61.5% | 61.5% / 61.8% / 62.1% / 62.3% / 62.5% | Judgment: ±100 bps around base. It is a simple range around software-mix and productivity expectations; IBM gave no multi-year GAAP gross-margin guidance. |

## Prediction framework

This table states the prediction used for comparison; it does not assert an execution timestamp.

| Driver | Base → changed input and units | Expected direction | Rough expected size | Short reason |
| --- | --- | --- | --- | --- |
| Software revenue growth | Base 8.0% / 7.0% / 6.0% / 5.5% / 5.0% → lower 6.0% / 5.0% / 4.0% / 3.5% / 3.0% or higher 10.0% / 9.0% / 8.0% / 7.5% / 7.0% YoY growth in FY2026E–FY2030E | Lower: EBIT, FCFE, and value/share down. Higher: all up. | About ±$0.8bn FY2030 EBIT and FCFE; about ±$10/share. | Incremental software revenue has a positive operating margin. AI can help if workloads convert to production and support renewal, pricing, and cross-sell; it can hurt if spend is displaced or competition pressures price and retention. |
| Cash gross margin | Base 60.5% / 60.8% / 61.1% / 61.3% / 61.5% → lower 59.5% / 59.8% / 60.1% / 60.3% / 60.5% or higher 61.5% / 61.8% / 62.1% / 62.3% / 62.5% of revenue in FY2026E–FY2030E | Lower: EBIT, FCFE, and value/share down. Higher: all up. | About ±$0.8bn FY2030 EBIT, ±$0.7bn FCFE, and ±$10/share. | More gross profit reaches EBIT. AI can help through higher-value mix and lower support/delivery costs; it can hurt if cloud/GPU, data, security, partner, or support costs outpace monetization. |

AI can affect both drivers together in the real business. The one-at-a-time runs below deliberately hold the other driver at base so each effect is isolated. Cash gross margin excludes finite-lived software amortization; the model also holds R&D and cash-SG&A rates constant in these runs.

## One-at-a-time results

### Software revenue growth

| Case | Actual input, FY2026E / 2027E / 2028E / 2029E / 2030E | FY2030 EBIT | Change vs. base | FY2030 FCFE | Change vs. base | Value/share | Change vs. base | Checks |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Lower | 6.0% / 5.0% / 4.0% / 3.5% / 3.0% | $16,477.5 | $(803.1) | $12,127.4 | $(789.0) | $170.00 | $(10.38) | PASS |
| Base | 8.0% / 7.0% / 6.0% / 5.5% / 5.0% | $17,280.5 | $0.0 | $12,916.4 | $0.0 | $180.39 | $0.00 | PASS |
| Higher | 10.0% / 9.0% / 8.0% / 7.5% / 7.0% | $18,146.4 | $865.8 | $13,778.4 | $862.0 | $191.66 | $11.28 | PASS |

**Low-to-high span:** EBIT $1,668.9m; FCFE $1,651.1m; value/share $21.66.

### Cash gross margin

| Case | Actual input, FY2026E / 2027E / 2028E / 2029E / 2030E | FY2030 EBIT | Change vs. base | FY2030 FCFE | Change vs. base | Value/share | Change vs. base | Checks |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Lower | 59.5% / 59.8% / 60.1% / 60.3% / 60.5% | $16,450.6 | $(829.9) | $12,223.0 | $(693.4) | $170.41 | $(9.97) | PASS |
| Base | 60.5% / 60.8% / 61.1% / 61.3% / 61.5% | $17,280.5 | $0.0 | $12,916.4 | $0.0 | $180.39 | $0.00 | PASS |
| Higher | 61.5% / 61.8% / 62.1% / 62.3% / 62.5% | $18,110.5 | $829.9 | $13,609.8 | $693.4 | $190.36 | $9.97 | PASS |

**Low-to-high span:** EBIT $1,659.9m; FCFE $1,386.8m; value/share $19.95.

## Accounting and restored-base checks

The Lab 10 check requires a balanced balance sheet, at least $5,000m of cash, and a revolver within its limit. Every usable run passed.

| Driver | Lower / Base / Higher max balance-sheet gap | Lower / Base / Higher minimum cash | Lower / Base / Higher maximum revolver |
| --- | --- | --- | --- |
| Software revenue growth | $0.0000 / $0.0000 / $0.0000 | $11,126.5 / $11,341.8 / $11,557.2 | $0.0 / $0.0 / $0.0 |
| Cash gross margin | $0.0000 / $0.0000 / $0.0000 | $10,839.8 / $11,341.8 / $11,843.8 | $0.0 / $0.0 / $0.0 |

After all runs, the original Lab 10 base was restored and rebuilt: base inputs match exactly; base outputs match exactly; restored FY2030 EBIT is $17,280.5m, FCFE is $12,916.4m, value/share is $180.39, and the maximum balance-sheet gap is $0.0000m. The existing broken-cash check was also detected successfully.

## Prediction versus actual and conclusion

| Driver | Prediction | Actual lower / higher change from base | Comparison |
| --- | --- | --- | --- |
| Software revenue growth | All outputs down / up; roughly ±$0.8bn FY2030 EBIT and FCFE and ±$10/share | EBIT $(803.1) / $865.8; FCFE $(789.0) / $862.0; value/share $(10.38) / $11.28 | Direction and rough size matched. |
| Cash gross margin | All outputs down / up; roughly ±$0.8bn EBIT, ±$0.7bn FCFE, and ±$10/share | EBIT $(829.9) / $829.9; FCFE $(693.4) / $693.4; value/share $(9.97) / $9.97 | Direction and rough size matched. |

**Software revenue growth is the larger driver over these tested ranges.** Its low-to-high span is $1,668.9m of FY2030 EBIT, $1,651.1m of FCFE, and $21.66/share, versus $1,659.9m, $1,386.8m, and $19.95/share for cash gross margin. The EBIT spans are nearly tied, but Software growth compounds through every forecast year and also changes revenue-linked working capital and investment, producing the larger FCFE and valuation effect. Cash gross margin changes gross profit directly at fixed revenue; tax and COGS-linked working-capital effects temper what reaches FCFE.
