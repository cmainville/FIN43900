# IBM DCF Inputs

## Important legal notice: educational use only

This document and the related `dcf.py` model are academic valuation exercises
for general informational and educational purposes only. They are not
financial or investment advice, personalized investment advice, legal advice,
tax advice, accounting advice, a recommendation to buy, sell, or hold IBM or
any other security, or an offer or solicitation.

No investment-adviser, broker-client, advisory, or fiduciary relationship is
created by preparing, distributing, receiving, or using this material. The
analysis does not consider any person's objectives, financial situation, risk
tolerance, or needs. Inputs may be incomplete, inaccurate, outdated, or
placeholders, and modeled outcomes are hypothetical estimates, not guarantees.

Users must independently verify the information and consult appropriately
licensed financial, tax, and legal professionals before making decisions.
Nothing in this notice waives or limits any duty or liability that cannot
lawfully be waived or limited.

This file documents the inputs used by `dcf.py`. Financial-statement amounts
are in USD millions. Per-share values are in USD per diluted share.

## Quick reference

- Company: International Business Machines Corporation
- Ticker: IBM
- Valuation date: September 9, 2026
- Current share price: $239.94
- Forecast period: 2027 through 2031
- Base revenue growth: 5.0%, 4.5%, 4.0%, 3.5%, 3.0%
- Base WACC: 7.52%
- Base terminal growth: 2.5%

## How inputs are labeled

- `sourced`: Taken directly from an identified external source.
- `derived`: Calculated from other documented inputs.
- `user-provided`: Specified by the user for this model.
- `model-convention`: A modeling choice rather than an IBM fact.
- `placeholder`: An existing value without adequate source support.

## Placeholders requiring review

These values remain in `dcf.py` so the model runs. They should not be treated
as verified IBM facts.

1. Pre-tax cost of debt
   - Python variable: `PRE_TAX_COST_OF_DEBT`
   - Current value: 5.75%
   - Status: `placeholder`
   - Needed: A current maturity-matched IBM bond yield or documented marginal
     borrowing-cost estimate.

2. Marginal tax rate
   - Python variable: `MARGINAL_TAX_RATE`
   - Current value: 21.0%
   - Status: `placeholder`
   - Needed: A normalized forward cash-tax rate for IBM.

3. Base EBIT margins
   - Current values: 17.5%, 18.0%, 18.3%, 18.5%, 18.5%
   - Status: `placeholder`
   - Needed: Historical and forward IBM operating-margin support.

4. Depreciation and amortization
   - Python variable: `DA_PERCENT_OF_REVENUE`
   - Current value: 7.5% of revenue
   - Status: `placeholder`
   - Needed: A normalized IBM depreciation and amortization forecast.

5. Capital expenditures
   - Python variable: `CAPEX_PERCENT_OF_REVENUE`
   - Current value: 2.3% of revenue
   - Status: `placeholder`
   - Needed: A normalized IBM capital-expenditure forecast.

6. Change in net working capital
   - Python variable: `INCREMENTAL_NWC_PERCENT`
   - Current value: 0.5% of incremental revenue
   - Status: `placeholder`
   - Needed: A normalized IBM operating working-capital requirement.

7. Terminal growth
   - Current value: 2.5%
   - Status: `placeholder`
   - Needed: A documented long-run nominal growth assumption.

## Sources

### S1: IBM 2025 Form 10-K

- Period: Year ended December 31, 2025
- Type: Primary source
- Link: [IBM 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/51143/000005114326000010/ibm-20251231_d2.htm)

### S2: IBM Q2 2026 Form 10-Q

- Date: June 30, 2026
- Type: Primary source
- Link: [IBM Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/51143/000005114326000078/ibm-20260630.htm)

### S3: IBM Q2 2026 earnings release

- Date: July 22, 2026
- Type: Primary source
- Link: [IBM Q2 2026 earnings release](https://newsroom.ibm.com/2026-07-22-IBM-RELEASES-SECOND-QUARTER-RESULTS)

### S4: IBM historical stock lookup

- Date used: September 9, 2026
- Type: Company-hosted market data
- Link: [IBM Historical Stock Lookup](https://ibm.gcs-web.com/stock-information/historic-stock-lookup)

### S5: U.S. Treasury daily rates

- Date used: September 9, 2026
- Type: Primary government data
- Link: [U.S. Treasury daily rates](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202609&type=daily_treasury_yield_curve)

### S6: Damodaran implied equity-risk premium

- Date used: September 1, 2026
- Type: Academic market estimate
- Link: [Damodaran Online](https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm)

### S7: IBM beta

- Date used: September 9, 2026
- Type: Secondary market data
- Link: [StockAnalysis IBM statistics](https://stockanalysis.com/stocks/ibm/statistics/)
- Note: The page identifies S&P Global Market Intelligence as its data source.

## Market and timing inputs

### Valuation date

- Python variable: `VALUATION_DATE`
- Value: September 9, 2026
- Status: `model-convention`
- Reason: Matches the share-price date.

### Current IBM share price

- Python variable: `CURRENT_SHARE_PRICE`
- Value: $239.94
- Status: `sourced`
- Date: September 9, 2026
- Source: S4

### Forecast period

- Python variable: `FORECAST_YEARS`
- Value: 2027 through 2031
- Status: `model-convention`
- Discounting: Dated midyear convention

## Revenue inputs

### 2025 revenue

- Python variable: `REVENUE_2025`
- Value: $67,500.0 million
- Status: `sourced`
- Source: S1
- Note: Rounded from IBM's reported $67.5 billion.

### 2026 revenue growth

- Value: 4.5%
- Status: `derived`
- Source: S3
- Calculation: Midpoint of IBM's 4% to 5% constant-currency guidance.

### 2026 estimated revenue

- Python variable: `REVENUE_2026_ESTIMATE`
- Value: $70,537.5 million
- Status: `derived`
- Calculation: 2025 revenue multiplied by 1.045.

### Base forecast

- 2027 revenue growth: 5.0%; status: `user-provided`
- 2027 EBIT margin: 17.5%; status: `placeholder`
- 2028 revenue growth: 4.5%; status: `user-provided`
- 2028 EBIT margin: 18.0%; status: `placeholder`
- 2029 revenue growth: 4.0%; status: `user-provided`
- 2029 EBIT margin: 18.3%; status: `placeholder`
- 2030 revenue growth: 3.5%; status: `user-provided`
- 2030 EBIT margin: 18.5%; status: `placeholder`
- 2031 revenue growth: 3.0%; status: `user-provided`
- 2031 EBIT margin: 18.5%; status: `placeholder`

Python mapping:

```text
SCENARIOS["Base"]["revenue_growth"] = [0.050, 0.045, 0.040, 0.035, 0.030]
SCENARIOS["Base"]["ebit_margin"] = [0.175, 0.180, 0.183, 0.185, 0.185]
```

## FCFF inputs

The model calculates FCFF as:

```text
FCFF = EBIT × (1 - tax rate) + D&A - capex - change in NWC
```

### Marginal tax rate

- Python variable: `MARGINAL_TAX_RATE`
- Value: 21.0%
- Status: `placeholder`

### Depreciation and amortization

- Python variable: `DA_PERCENT_OF_REVENUE`
- Value: 7.5% of revenue
- Status: `placeholder`

### Capital expenditures

- Python variable: `CAPEX_PERCENT_OF_REVENUE`
- Value: 2.3% of revenue
- Status: `placeholder`

### Change in net working capital

- Python variable: `INCREMENTAL_NWC_PERCENT`
- Value: 0.5% of incremental revenue
- Status: `placeholder`

## WACC inputs

The model calculates WACC as:

```text
Cost of equity = risk-free rate + adjusted beta × equity-risk premium
After-tax cost of debt = pre-tax cost of debt × (1 - tax rate)
WACC = equity weight × cost of equity + debt weight × after-tax cost of debt
```

### Risk-free rate

- Python variable: `RISK_FREE_RATE`
- Value: 4.83%
- Status: `sourced`
- Date: September 9, 2026
- Source: S5

### Equity-risk premium

- Python variable: `EQUITY_RISK_PREMIUM`
- Value: 4.14%
- Status: `sourced`
- Date: September 1, 2026
- Source: S6

### Raw beta

- Python variable: `RAW_BETA`
- Value: 0.71
- Status: `sourced`
- Source: S7

### Adjusted beta

- Python variable: `ADJUSTED_BETA`
- Value: 0.81
- Status: `derived`
- Calculation: Two-thirds of 0.71 plus one-third of 1.0.

### Pre-tax cost of debt

- Python variable: `PRE_TAX_COST_OF_DEBT`
- Value: 5.75%
- Status: `placeholder`

### Calculated WACC components

- Cost of equity: 8.17%; status: `derived`
- After-tax cost of debt: 4.54%; status: `derived from placeholders`
- Equity weight: 82.2%; status: `derived`
- Debt weight: 17.8%; status: `derived`
- Base WACC: 7.52%; status: `derived from placeholders`

The base WACC is provisional because its cost-of-debt and tax-rate inputs are
placeholders.

## Enterprise-to-equity bridge

The model calculates equity value as:

```text
Equity value = enterprise value
             + non-operating cash
             - non-Financing debt
             - net pension deficit
             - noncontrolling interest

Value per share = equity value / diluted shares
```

### Cash and securities

- `CASH_AND_EQUIVALENTS`: $7,172.0 million; `sourced`; S2
- `MARKETABLE_SECURITIES`: $960.0 million; `sourced`; S2
- `NON_OPERATING_CASH`: $8,132.0 million; `derived`; cash plus marketable
  securities, excluding restricted cash

### Debt

- `TOTAL_DEBT`: $61,987.0 million; `sourced`; S2
- `IBM_FINANCING_DEBT`: $13,047.0 million; `sourced`; S2
- `NON_FINANCING_DEBT`: $48,940.0 million; `derived`; total debt less IBM
  Financing debt

### Other claims

- Retirement obligations: $8,603.0 million; `sourced`; S2
- Prepaid pension assets: $7,645.0 million; `sourced`; S2
- `NET_PENSION_DEFICIT`: $958.0 million; `derived`; retirement obligations less
  prepaid pension assets
- `NONCONTROLLING_INTEREST`: $89.0 million; `sourced`; S2

### Share counts

- `BASIC_SHARES_OUTSTANDING`: 942.134390 million; `sourced`; S2
- `DILUTED_SHARES`: 953.3 million; `sourced`; S2

The model uses basic shares to calculate market equity value for WACC. It uses
diluted shares to calculate DCF value per share.

### IBM Financing treatment

The model subtracts non-Financing debt rather than total debt. IBM states that
its Financing receivables are income-producing assets supported by related
Financing debt. This is a simplified operating-company treatment, not a full
sum-of-the-parts valuation of IBM Financing.

## Terminal value

- Python location: `SCENARIOS["Base"]["terminal_growth"]`
- Value: 2.5%
- Status: `placeholder`
- Formula: Terminal FCFF divided by WACC minus terminal growth.

The model treats terminal growth greater than or equal to WACC as invalid.

## Sensitivity and reverse-DCF controls

These controls were specified by the user. They are not IBM company facts.

- WACC sensitivity: 9%, 10%, 11%
- Terminal-growth sensitivity: 2%, 3%, 4%
- Reverse-DCF lower shift: negative 5 percentage points
- Reverse-DCF upper shift: positive 10 percentage points
- Reverse-DCF target: $239.94 per share

## Notes for AI systems

- Python variable names match `dcf.py` exactly.
- A percentage displayed as 5.0% is stored in Python as `0.050`.
- Financial-statement values are USD millions unless stated otherwise.
- `placeholder` means the value is unresolved, not zero.
- Each derived value identifies its calculation or component inputs.
- Source labels S1 through S7 refer to the source descriptions above.
