"""Lab 14 portfolio baselines for the Meridian Foundation.

Returns and volatilities are decimals; displayed percentages are derived from
them. Edit the inputs below to explore different assumptions.
"""

import math
from itertools import product
from pathlib import Path

import pandas as pd


# Course-authored training values, not observed market estimates.
ASSETS = (
    "Treasury bills",
    "Treasury 10-year note",
    "Investment-grade bond fund",
    "Global equity index fund",
)
EXPECTED_RETURNS = (0.035, 0.043, 0.050, 0.080)
VOLATILITIES = (0.005, 0.070, 0.060, 0.160)
CORRELATIONS = (
    (1.00, 0.10, 0.05, 0.00),
    (0.10, 1.00, 0.80, -0.10),
    (0.05, 0.80, 1.00, 0.25),
    (0.00, -0.10, 0.25, 1.00),
)
CPI_ESTIMATE = 0.025
REAL_RETURN_SPREAD = 0.040
OBJECTIVE_RETURN = CPI_ESTIMATE + REAL_RETURN_SPREAD
RESERVE_ELIGIBLE = frozenset(("Treasury bills", "Treasury 10-year note"))


def validate_correlations(correlations):
    """Reject malformed, asymmetric, or out-of-range correlation matrices."""
    n = len(correlations)
    if n == 0 or any(len(row) != n for row in correlations):
        raise ValueError("Correlation matrix must be nonempty and square.")
    for i in range(n):
        for j in range(n):
            value = correlations[i][j]
            if not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"Correlation at [{i}][{j}] must be finite.")
            if not -1.0 <= value <= 1.0:
                raise ValueError(f"Correlation at [{i}][{j}] must be within [-1, 1].")
            if not math.isclose(value, correlations[j][i], abs_tol=1e-12):
                raise ValueError(f"Correlation matrix must be symmetric at [{i}][{j}].")
        if not math.isclose(correlations[i][i], 1.0, abs_tol=1e-12):
            raise ValueError(f"Correlation diagonal at [{i}][{i}] must equal 1.")


def covariance_matrix(volatilities, correlations):
    """Return cov(i,j) = volatility(i) * volatility(j) * correlation(i,j)."""
    validate_correlations(correlations)
    if len(volatilities) != len(correlations):
        raise ValueError("Volatility and correlation dimensions must match.")
    if any(not math.isfinite(v) or v <= 0 for v in volatilities):
        raise ValueError("Each volatility must be finite and positive.")
    return tuple(
        tuple(volatilities[i] * volatilities[j] * correlations[i][j]
              for j in range(len(volatilities)))
        for i in range(len(volatilities))
    )


def expected_portfolio_return(weights, expected_returns):
    """Weighted sum of the individual expected returns."""
    if len(weights) != len(expected_returns):
        raise ValueError("Weight and return dimensions must match.")
    return sum(w * r for w, r in zip(weights, expected_returns))


def portfolio_variance_and_volatility(weights, covariances):
    """Compute w'Σw, including every pairwise covariance term, and its root."""
    if len(weights) != len(covariances) or any(
        len(row) != len(weights) for row in covariances
    ):
        raise ValueError("Weight and covariance dimensions must match.")
    variance = sum(
        weights[i] * weights[j] * covariances[i][j]
        for i in range(len(weights))
        for j in range(len(weights))
    )
    if variance < -1e-12:
        raise ValueError("Portfolio variance is negative; check covariance inputs.")
    return max(variance, 0.0), math.sqrt(max(variance, 0.0))


def reserve_eligible_allocation(weights, assets=ASSETS, eligible=RESERVE_ELIGIBLE):
    """Sum weights assigned to reserve-eligible assets."""
    if len(weights) != len(assets):
        raise ValueError("Weight and asset dimensions must match.")
    return sum(w for asset, w in zip(assets, weights) if asset in eligible)


def inverse_volatility_weights(volatilities):
    """Normalize reciprocals of positive volatilities to weights summing to 1."""
    if not volatilities or any(not math.isfinite(v) or v <= 0 for v in volatilities):
        raise ValueError("Each volatility must be finite and positive.")
    reciprocals = [1.0 / v for v in volatilities]
    total = sum(reciprocals)
    return tuple(value / total for value in reciprocals)


def meets_return_objective(portfolio_return, objective=OBJECTIVE_RETURN):
    """Whether expected return meets the stated planning objective."""
    return portfolio_return >= objective - 1e-12


def evaluate_portfolio(weights, expected_returns=EXPECTED_RETURNS,
                       volatilities=VOLATILITIES, correlations=CORRELATIONS):
    """Calculate all comparison metrics from editable inputs."""
    if len(weights) != len(ASSETS) or any(w < 0 or not math.isfinite(w) for w in weights):
        raise ValueError("Provide one finite, nonnegative weight per asset.")
    if not math.isclose(sum(weights), 1.0, abs_tol=1e-12):
        raise ValueError("Portfolio weights must sum to 100%.")
    covariances = covariance_matrix(volatilities, correlations)
    variance, volatility = portfolio_variance_and_volatility(weights, covariances)
    portfolio_return = expected_portfolio_return(weights, expected_returns)
    return {
        "weights": tuple(weights),
        "return": portfolio_return,
        "variance": variance,
        "volatility": volatility,
        "reserve": reserve_eligible_allocation(weights),
        "objective_pass": meets_return_objective(portfolio_return),
    }


def baseline_portfolios(expected_returns=EXPECTED_RETURNS,
                        volatilities=VOLATILITIES, correlations=CORRELATIONS):
    """Evaluate the benchmark, equal weight, and inverse volatility baselines."""
    allocations = {
        "Benchmark": (0.0, 0.0, 0.4, 0.6),
        "Equal Weight": (0.25, 0.25, 0.25, 0.25),
        "Inverse Volatility": inverse_volatility_weights(volatilities),
    }
    return {
        name: evaluate_portfolio(weights, expected_returns, volatilities, correlations)
        for name, weights in allocations.items()
    }


def display_portfolio_comparison(portfolios):
    """Print allocations and metrics at the assignment's displayed precision."""
    print("Meridian Foundation portfolio baselines")
    print("Returns, volatilities, and correlations: course-authored training values")
    print(f"CPI estimate: {CPI_ESTIMATE:.1%}; objective: CPI + 4.0% = {OBJECTIVE_RETURN:.1%}")
    print("Weights in order: " + " / ".join(ASSETS))
    for name, result in portfolios.items():
        weights = " / ".join(f"{weight:.1%}" for weight in result["weights"])
        status = "PASS" if result["objective_pass"] else "FAIL"
        print(f"\n{name}")
        print(f"  Weights: {weights}")
        print(f"  Expected return: {result['return']:.2%}")
        print(f"  Volatility: {result['volatility']:.2%}")
        print(f"  Reserve eligible: {result['reserve']:.1%}")
        print(f"  Expected-return objective: {status}")


def main():
    display_portfolio_comparison(baseline_portfolios())


if __name__ == "__main__":
    main()


# Lab 15 additions. The Lab 14 entry point above is intentionally preserved.
def allocation_units(asset_count, remaining=20):
    """Yield each fully invested 5-point allocation once, in stable order."""
    if asset_count == 1:
        yield (remaining,)
    else:
        for first in range(remaining + 1):
            for rest in allocation_units(asset_count - 1, remaining - first):
                yield (first,) + rest


def optimize_portfolio(assets, expected_returns, volatilities, correlations,
                       objective, reserve_eligible=(), reserve_minimum=0.0):
    """Search all 5-point long-only mixes and select lowest feasible volatility."""
    assets = tuple(assets)
    returns = tuple(expected_returns)
    vols = tuple(volatilities)
    eligible = frozenset(reserve_eligible)
    n = len(assets)
    if not 3 <= n <= 6 or len(set(assets)) != n or len(returns) != n or len(vols) != n:
        raise ValueError("Provide 3–6 distinct assets and one return/volatility per asset.")
    if any(not math.isfinite(x) for x in returns):
        raise ValueError("Expected returns must be finite.")
    if not math.isfinite(objective) or not math.isfinite(reserve_minimum) or not 0 <= reserve_minimum <= 1:
        raise ValueError("Objective must be finite and reserve minimum within [0, 1].")
    if not eligible.issubset(assets):
        raise ValueError("Reserve-eligible assets must be in the universe.")
    cov = covariance_matrix(vols, correlations)
    best = None
    feasible_count = 0
    candidate_count = 0
    for units in allocation_units(n):
        candidate_count += 1
        weights = tuple(unit / 20 for unit in units)
        ret = expected_portfolio_return(weights, returns)
        reserve = reserve_eligible_allocation(weights, assets, eligible)
        if ret < objective - 1e-12 or reserve < reserve_minimum - 1e-12:
            continue
        feasible_count += 1
        variance, vol = portfolio_variance_and_volatility(weights, cov)
        result = {"weights": weights, "return": ret, "variance": variance,
                  "volatility": vol, "reserve": reserve, "feasible": True}
        # Enumeration order resolves exact volatility ties deterministically.
        if best is None or vol < best["volatility"] - 1e-12:
            best = result
    if best is None:
        best = {"weights": None, "return": None, "variance": None,
                "volatility": None, "reserve": None, "feasible": False}
    return {**best, "feasible_count": feasible_count, "candidate_count": candidate_count}


def largest_weight_change(left, right):
    """Largest absolute individual weight movement, in percentage points."""
    if not left["feasible"] or not right["feasible"]:
        return None
    if len(left["weights"]) != len(right["weights"]):
        raise ValueError("Scenarios have different universes.")
    return 100 * max(abs(a - b) for a, b in zip(left["weights"], right["weights"]))


def estimate_from_monthly_prices(source, last_36=False):
    """Estimate annual arithmetic returns, sample risk, and Pearson correlation."""
    try:
        frame = pd.read_csv(source)
    except Exception as exc:
        raise ValueError(f"Cannot read monthly price CSV: {exc}") from exc
    if not 4 <= len(frame.columns) <= 7 or frame.columns[0] != "Date":
        raise ValueError("CSV needs Date first and 3–6 asset columns.")
    assets = tuple(frame.columns[1:])
    if len(set(assets)) != len(assets) or any(not name or name.startswith("Unnamed") for name in assets):
        raise ValueError("Asset columns must have distinct names.")
    try:
        dates = pd.to_datetime(frame["Date"], format="%Y-%m-%d", errors="raise")
    except Exception as exc:
        raise ValueError("Dates must be valid YYYY-MM-DD values.") from exc
    if dates.isna().any() or dates.duplicated().any() or not dates.is_monotonic_increasing:
        raise ValueError("Dates must be unique and chronological.")
    if dates.dt.to_period("M").duplicated().any():
        raise ValueError("Only one observation per calendar month is allowed.")
    if len(dates) < (37 if last_36 else 3):
        raise ValueError("Insufficient monthly prices for the selected window.")
    months = dates.dt.to_period("M")
    expected = pd.period_range(months.iloc[0], months.iloc[-1], freq="M")
    if list(months) != list(expected):
        raise ValueError("Monthly observations must be consecutive.")
    try:
        prices = frame.loc[:, assets].apply(pd.to_numeric, errors="raise")
    except Exception as exc:
        raise ValueError("Prices must be numeric.") from exc
    if prices.isna().any().any() or not (prices > 0).all().all() or not prices.map(math.isfinite).all().all():
        raise ValueError("Prices must be positive and finite with no missing cells.")
    returns = prices.pct_change(fill_method=None).iloc[1:]
    if last_36:
        returns = returns.tail(36)
    vols = returns.std(ddof=1) * math.sqrt(12)
    if (vols <= 0).any() or vols.isna().any():
        raise ValueError("Every asset needs nonzero sample volatility.")
    correlations = returns.corr()
    if correlations.isna().any().any():
        raise ValueError("Cannot estimate a complete correlation matrix.")
    return {"assets": assets,
            "expected_returns": tuple(float(x) for x in returns.mean() * 12),
            "volatilities": tuple(float(x) for x in vols),
            "correlations": tuple(tuple(float(x) for x in row) for row in correlations.to_numpy()),
            "observation_count": len(returns),
            "start_date": dates.iloc[returns.index[0]].date().isoformat(),
            "end_date": dates.iloc[returns.index[-1]].date().isoformat(),
            "price_observation_count": len(frame)}
