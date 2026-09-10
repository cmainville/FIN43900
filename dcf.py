"""IBM five-year FCFF discounted cash-flow model.

All financial statement amounts are USD millions except per-share values.
Reported figures are dated June 30, 2026. Market data are dated September 9,
2026. Forecasts are analyst assumptions, not reported facts or investment
advice. The model is intentionally dependency-free and can be run with:

    python3 dcf.py

Primary sources:
* IBM 2025 Form 10-K:
  https://www.sec.gov/Archives/edgar/data/51143/000005114326000010/
* IBM Q2 2026 Form 10-Q:
  https://www.sec.gov/Archives/edgar/data/51143/000005114326000078/
* IBM Q2 2026 earnings release:
  https://newsroom.ibm.com/2026-07-22-IBM-RELEASES-SECOND-QUARTER-RESULTS
* U.S. Treasury daily rates for September 2026:
  https://home.treasury.gov/resource-center/data-chart-center/interest-rates/
* Damodaran implied U.S. equity risk premium, September 1, 2026:
  https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm

Important IBM-specific treatment:
IBM manages its Financing receivables as income-producing assets funded by
matched Financing debt. This simplified operating-company DCF therefore uses
non-Financing debt in the enterprise-to-equity bridge. It should not be read as
a full sum-of-the-parts valuation of IBM Financing.
"""

from datetime import date


DISCLAIMER = """IMPORTANT LEGAL NOTICE — EDUCATIONAL USE ONLY
NOT FINANCIAL OR INVESTMENT ADVICE

This model is an academic valuation exercise for general informational and
educational purposes only. It is not personalized investment, legal, tax,
accounting, or other professional advice; a recommendation to buy, sell, or
hold IBM or any other security; or an offer or solicitation.

No investment-adviser, broker-client, advisory, or fiduciary relationship is
created by preparing, distributing, receiving, or using this model. The model
does not consider any person's objectives, financial situation, risk tolerance,
or needs. Inputs may be incomplete, inaccurate, outdated, or placeholders, and
modeled outcomes are hypothetical estimates, not guarantees.

Users must independently verify the information and consult appropriately
licensed financial, tax, and legal professionals before making decisions.
Nothing in this notice waives or limits any duty or liability that cannot
lawfully be waived or limited."""


# ---------------------------------------------------------------------------
# Reported and market inputs
# ---------------------------------------------------------------------------

VALUATION_DATE = date(2026, 9, 9)
CURRENT_SHARE_PRICE = 239.94  # Market data; IBM close on 2026-09-09

# IBM reported $67.5 billion of 2025 revenue. The rounded figure is sufficient
# for this screen-grade model because the forecast assumptions are less precise.
REVENUE_2025 = 67_500.0

# June 30, 2026 balance sheet and share data from IBM's Q2 2026 Form 10-Q.
CASH_AND_EQUIVALENTS = 7_172.0
MARKETABLE_SECURITIES = 960.0
NON_OPERATING_CASH = CASH_AND_EQUIVALENTS + MARKETABLE_SECURITIES
TOTAL_DEBT = 61_987.0
IBM_FINANCING_DEBT = 13_047.0
NON_FINANCING_DEBT = TOTAL_DEBT - IBM_FINANCING_DEBT
NET_PENSION_DEFICIT = 8_603.0 - 7_645.0
NONCONTROLLING_INTEREST = 89.0
BASIC_SHARES_OUTSTANDING = 942.134390
DILUTED_SHARES = 953.3

# WACC inputs. Risk-free rate and ERP are observed as of the dates above.
# The raw beta is a current five-year beta; the adjusted beta is pulled one
# third toward 1.0 to reduce measurement noise. The debt spread is an analyst
# assumption consistent with IBM's A-/A3/A- senior ratings at June 30, 2026.
RISK_FREE_RATE = 0.0483
EQUITY_RISK_PREMIUM = 0.0414
RAW_BETA = 0.71
ADJUSTED_BETA = (2.0 / 3.0) * RAW_BETA + (1.0 / 3.0) * 1.0
PRE_TAX_COST_OF_DEBT = 0.0575
MARGINAL_TAX_RATE = 0.21


def calculate_wacc():
    """Return IBM's WACC and its supporting market-value components."""
    cost_of_equity = RISK_FREE_RATE + ADJUSTED_BETA * EQUITY_RISK_PREMIUM
    after_tax_cost_of_debt = PRE_TAX_COST_OF_DEBT * (1.0 - MARGINAL_TAX_RATE)
    market_value_equity = CURRENT_SHARE_PRICE * BASIC_SHARES_OUTSTANDING
    invested_capital = market_value_equity + NON_FINANCING_DEBT
    equity_weight = market_value_equity / invested_capital
    debt_weight = NON_FINANCING_DEBT / invested_capital
    wacc = (
        equity_weight * cost_of_equity
        + debt_weight * after_tax_cost_of_debt
    )
    return {
        "cost_of_equity": cost_of_equity,
        "after_tax_cost_of_debt": after_tax_cost_of_debt,
        "market_value_equity": market_value_equity,
        "equity_weight": equity_weight,
        "debt_weight": debt_weight,
        "wacc": wacc,
    }


WACC_BUILD = calculate_wacc()
BASE_WACC = WACC_BUILD["wacc"]


# ---------------------------------------------------------------------------
# Forecast assumptions
# ---------------------------------------------------------------------------

# 2026E revenue uses the midpoint of IBM's updated 4%-5% constant-currency
# revenue-growth guidance. This is the base from which 2027-2031 are forecast.
REVENUE_2026_ESTIMATE = REVENUE_2025 * 1.045

# D&A and capex are modeled as percentages of revenue. Change in NWC is modeled
# as a percentage of incremental revenue, which prevents IBM's seasonal working
# capital movements from being capitalized into the terminal value.
DA_PERCENT_OF_REVENUE = 0.075
CAPEX_PERCENT_OF_REVENUE = 0.023
INCREMENTAL_NWC_PERCENT = 0.005

SCENARIOS = {
    "Bear": {
        "revenue_growth": [0.030, 0.030, 0.025, 0.020, 0.020],
        "ebit_margin": [0.162, 0.164, 0.165, 0.165, 0.165],
        "wacc": 0.085,
        "terminal_growth": 0.015,
    },
    "Base": {
        "revenue_growth": [0.050, 0.045, 0.040, 0.035, 0.030],
        "ebit_margin": [0.175, 0.180, 0.183, 0.185, 0.185],
        "wacc": BASE_WACC,
        "terminal_growth": 0.025,
    },
    "Bull": {
        "revenue_growth": [0.065, 0.060, 0.055, 0.050, 0.045],
        "ebit_margin": [0.180, 0.187, 0.192, 0.195, 0.197],
        "wacc": 0.070,
        "terminal_growth": 0.030,
    },
}

FORECAST_YEARS = list(range(2027, 2032))


def years_between(start, end):
    """Convert calendar days to years for stub-period discounting."""
    return (end - start).days / 365.25


def build_forecast(revenue_growth, ebit_margin):
    """Build a revenue-to-FCFF forecast for 2027-2031."""
    if len(revenue_growth) != len(FORECAST_YEARS):
        raise ValueError("Revenue growth must contain one value per forecast year.")
    if len(ebit_margin) != len(FORECAST_YEARS):
        raise ValueError("EBIT margin must contain one value per forecast year.")

    rows = []
    prior_revenue = REVENUE_2026_ESTIMATE
    for year, growth, margin in zip(FORECAST_YEARS, revenue_growth, ebit_margin):
        revenue = prior_revenue * (1.0 + growth)
        ebit = revenue * margin
        cash_taxes = ebit * MARGINAL_TAX_RATE
        nopat = ebit - cash_taxes
        depreciation_and_amortization = revenue * DA_PERCENT_OF_REVENUE
        capex = revenue * CAPEX_PERCENT_OF_REVENUE
        change_in_nwc = (revenue - prior_revenue) * INCREMENTAL_NWC_PERCENT
        fcff = (
            nopat
            + depreciation_and_amortization
            - capex
            - change_in_nwc
        )
        rows.append(
            {
                "year": year,
                "revenue": revenue,
                "growth": growth,
                "ebit_margin": margin,
                "ebit": ebit,
                "nopat": nopat,
                "d_and_a": depreciation_and_amortization,
                "capex": capex,
                "change_in_nwc": change_in_nwc,
                "fcff": fcff,
            }
        )
        prior_revenue = revenue
    return rows


def value_forecast(forecast, wacc, terminal_growth):
    """Value FCFF using dated mid-year discounting and a perpetuity terminal."""
    if terminal_growth >= wacc:
        raise ValueError("Terminal growth must be less than WACC.")

    present_value_explicit_fcff = 0.0
    for row in forecast:
        midyear_date = date(row["year"], 7, 1)
        discount_period = years_between(VALUATION_DATE, midyear_date)
        row["discount_period"] = discount_period
        row["present_value_fcff"] = row["fcff"] / (
            (1.0 + wacc) ** discount_period
        )
        present_value_explicit_fcff += row["present_value_fcff"]

    terminal_fcff = forecast[-1]["fcff"] * (1.0 + terminal_growth)
    terminal_value = terminal_fcff / (wacc - terminal_growth)
    terminal_date = date(FORECAST_YEARS[-1], 12, 31)
    terminal_discount_period = years_between(VALUATION_DATE, terminal_date)
    present_value_terminal_value = terminal_value / (
        (1.0 + wacc) ** terminal_discount_period
    )

    enterprise_value = present_value_explicit_fcff + present_value_terminal_value
    equity_value = (
        enterprise_value
        + NON_OPERATING_CASH
        - NON_FINANCING_DEBT
        - NET_PENSION_DEFICIT
        - NONCONTROLLING_INTEREST
    )
    value_per_share = equity_value / DILUTED_SHARES
    terminal_value_share = present_value_terminal_value / enterprise_value

    return {
        "present_value_explicit_fcff": present_value_explicit_fcff,
        "terminal_value": terminal_value,
        "present_value_terminal_value": present_value_terminal_value,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "value_per_share": value_per_share,
        "terminal_value_share": terminal_value_share,
        "upside_downside": value_per_share / CURRENT_SHARE_PRICE - 1.0,
    }


def run_scenario(name):
    assumptions = SCENARIOS[name]
    forecast = build_forecast(
        assumptions["revenue_growth"], assumptions["ebit_margin"]
    )
    valuation = value_forecast(
        forecast, assumptions["wacc"], assumptions["terminal_growth"]
    )
    return forecast, valuation


def solve_growth_shift(target_price):
    """Solve for one shift applied to all five base revenue growth rates."""
    assumptions = SCENARIOS["Base"]
    base_growth_rates = assumptions["revenue_growth"]

    def value_at_shift(shift):
        adjusted_growth_rates = [growth + shift for growth in base_growth_rates]
        forecast = build_forecast(
            adjusted_growth_rates,
            assumptions["ebit_margin"],
        )
        valuation = value_forecast(
            forecast,
            assumptions["wacc"],
            assumptions["terminal_growth"],
        )
        return valuation["value_per_share"]

    low = -0.05
    high = 0.10
    low_difference = value_at_shift(low) - target_price
    high_difference = value_at_shift(high) - target_price

    if low_difference == 0:
        return low, [growth + low for growth in base_growth_rates], target_price
    if high_difference == 0:
        return high, [growth + high for growth in base_growth_rates], target_price
    if low_difference * high_difference > 0:
        return None

    for _ in range(100):
        midpoint = (low + high) / 2.0
        midpoint_difference = value_at_shift(midpoint) - target_price
        if abs(midpoint_difference) < 0.000001:
            low = high = midpoint
            break
        if low_difference * midpoint_difference <= 0:
            high = midpoint
        else:
            low = midpoint
            low_difference = midpoint_difference

    solved_shift = (low + high) / 2.0
    adjusted_growth_rates = [
        growth + solved_shift for growth in base_growth_rates
    ]
    implied_value = value_at_shift(solved_shift)
    return solved_shift, adjusted_growth_rates, implied_value


def print_forecast(forecast):
    print("\nBase-case operating forecast (USD millions)")
    print("Year    Revenue   Growth   EBIT Margin       FCFF     PV of FCFF")
    for row in forecast:
        print(
            f"{row['year']}  "
            f"{row['revenue']:>9,.1f}  "
            f"{row['growth']:>6.1%}  "
            f"{row['ebit_margin']:>11.1%}  "
            f"{row['fcff']:>9,.1f}  "
            f"{row['present_value_fcff']:>12,.1f}"
        )


def print_sensitivity(base_forecast):
    wacc_values = [0.09, 0.10, 0.11]
    terminal_growth_values = [0.02, 0.03, 0.04]
    print("\nSENSITIVITY: VALUE PER DILUTED SHARE")
    print(
        "WACC \\ g "
        + " ".join(f"{growth:>11.1%}" for growth in terminal_growth_values)
    )
    grid = []
    for wacc in wacc_values:
        values = []
        cells = []
        for growth in terminal_growth_values:
            if growth >= wacc:
                values.append(None)
                cells.append(f"{'invalid':>11}")
            else:
                value = value_forecast(
                    base_forecast, wacc, growth
                )["value_per_share"]
                values.append(value)
                cells.append(f"${value:>10.2f}")
        grid.append(values)
        print(f"{wacc:>8.1%} " + " ".join(cells))

    for row in grid:
        valid_values = [value for value in row if value is not None]
        if valid_values != sorted(valid_values):
            raise AssertionError("Higher terminal growth should raise value.")
    for column in range(len(terminal_growth_values)):
        valid_values = [
            row[column] for row in grid if row[column] is not None
        ]
        if valid_values != sorted(valid_values, reverse=True):
            raise AssertionError("Higher WACC should lower value.")


def main():
    if NON_FINANCING_DEBT != TOTAL_DEBT - IBM_FINANCING_DEBT:
        raise AssertionError("Non-Financing debt bridge does not reconcile.")
    if DILUTED_SHARES < BASIC_SHARES_OUTSTANDING:
        raise AssertionError("Diluted share count cannot be below basic shares.")

    base_assumptions = SCENARIOS["Base"]
    base_forecast = build_forecast(
        base_assumptions["revenue_growth"],
        base_assumptions["ebit_margin"],
    )
    base_valuation = value_forecast(
        base_forecast,
        base_assumptions["wacc"],
        base_assumptions["terminal_growth"],
    )
    value_to_price = base_valuation["value_per_share"] / CURRENT_SHARE_PRICE
    within_reasonableness_range = 0.5 <= value_to_price <= 2.0

    print(DISCLAIMER)
    print("\nIBM DCF")
    print("=======")
    print("\nBASE DCF")
    print(f"Value per diluted share: ${base_valuation['value_per_share']:,.2f}")
    print(f"Current share price:      ${CURRENT_SHARE_PRICE:,.2f}")
    print(f"DCF value / current price: {value_to_price:.2f}x")
    print(
        "Class reasonableness range (0.5x to 2.0x): "
        + ("Within range" if within_reasonableness_range else "Outside range")
    )

    print_sensitivity(base_forecast)

    print("\nREVERSE DCF")
    print(f"Target share price: ${CURRENT_SHARE_PRICE:,.2f}")
    reverse_result = solve_growth_shift(CURRENT_SHARE_PRICE)
    if reverse_result is None:
        print("No solution in bracket")
    else:
        solved_shift, adjusted_growth_rates, implied_value = reverse_result
        rates_text = ", ".join(
            f"{growth:.2%}" for growth in adjusted_growth_rates
        )
        margins_text = ", ".join(
            f"{margin:.1%}" for margin in base_assumptions["ebit_margin"]
        )
        print(f"Solved growth shift: {solved_shift * 100:+.2f} percentage points")
        print(f"Adjusted growth rates: {rates_text}")
        print(f"Implied DCF value: ${implied_value:,.2f}")
        print("Major assumptions held fixed:")
        print(f"  WACC: {base_assumptions['wacc']:.2%}")
        print(f"  Terminal growth: {base_assumptions['terminal_growth']:.1%}")
        print(f"  EBIT margins: {margins_text}")
        print(f"  Tax rate: {MARGINAL_TAX_RATE:.1%}")
        print(f"  D&A / revenue: {DA_PERCENT_OF_REVENUE:.1%}")
        print(f"  Capex / revenue: {CAPEX_PERCENT_OF_REVENUE:.1%}")
        print(f"  Incremental NWC / revenue growth: {INCREMENTAL_NWC_PERCENT:.1%}")
        print("  Enterprise-to-equity bridge and diluted shares")


if __name__ == "__main__":
    main()
