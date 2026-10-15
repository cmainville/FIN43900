"""Meridian Foundation mandate checker for FIN 43900 Lab 13.

All values are editable inputs. Percentages are expressed as percentage points
of the $100 million reserve, rather than as decimal portfolio weights.
"""

from collections import defaultdict


# ----- Editable mandate inputs -----
RESERVE_SIZE_MILLIONS = 100.0
QUARTERLY_DISTRIBUTION_MILLIONS = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_DAYS = 5
MINIMUM_LIQUID_SHARE = 90.0
ISSUER_CONCENTRATION_LIMIT = 8.0

# Each holding defines its issuer, redemption time, reserve qualification, and
# whether its issuer is exempt from the single-company issuer limit.
HOLDINGS = {
    "Cash": {
        "issuer": "None",
        "redemption_days": 0,
        "reserve_eligible": True,
        "issuer_exempt": True,
    },
    "Treasury bills": {
        "issuer": "U.S. Treasury",
        "redemption_days": 1,
        "reserve_eligible": True,
        "issuer_exempt": True,
    },
    "Treasury 10-year note": {
        "issuer": "U.S. Treasury",
        "redemption_days": 1,
        "reserve_eligible": True,
        "issuer_exempt": True,
    },
    "Global equity index fund": {
        "issuer": "Diversified fund",
        "redemption_days": 2,
        "reserve_eligible": False,
        "issuer_exempt": True,
    },
    "Investment-grade bond fund": {
        "issuer": "Diversified fund",
        "redemption_days": 3,
        "reserve_eligible": False,
        "issuer_exempt": True,
    },
    "Private real estate fund": {
        "issuer": "Diversified fund",
        "redemption_days": 90,
        "reserve_eligible": False,
        "issuer_exempt": True,
    },
    "Acme Corp bonds": {
        "issuer": "Acme Corp",
        "redemption_days": 4,
        "reserve_eligible": False,
        "issuer_exempt": False,
    },
    "Acme Corp stock": {
        "issuer": "Acme Corp",
        "redemption_days": 1,
        "reserve_eligible": False,
        "issuer_exempt": False,
    },
}

# Original A/B/C inputs are preserved. D is deliberately mechanically compliant
# while raising a suitability question about the return objective (S2).
CANDIDATES = {
    "A": {
        "Cash": 2.0,
        "Treasury bills": 2.0,
        "Treasury 10-year note": 10.0,
        "Global equity index fund": 60.0,
        "Investment-grade bond fund": 26.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
    "B": {
        "Cash": 1.0,
        "Treasury bills": 0.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 55.0,
        "Investment-grade bond fund": 20.0,
        "Private real estate fund": 15.0,
        "Acme Corp bonds": 5.0,
        "Acme Corp stock": 4.0,
    },
    "C": {
        "Cash": 1.0,
        "Treasury bills": 1.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 70.0,
        "Investment-grade bond fund": 20.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 8.0,
    },
    "D": {
        "Cash": 90.0,
        "Treasury bills": 10.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 0.0,
        "Investment-grade bond fund": 0.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
}


def minimum_reserve_allocation() -> float:
    """Return the reserve allocation needed for scheduled distributions."""
    return (
        QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION_MILLIONS
        / RESERVE_SIZE_MILLIONS
        * 100
    )


def assess_portfolio(weights: dict[str, float]) -> dict[str, float | bool]:
    """Calculate the five checkable mandate rules for one candidate."""
    if set(weights) != set(HOLDINGS):
        raise ValueError("Each candidate must provide a weight for every holding.")

    total_weight = sum(weights.values())
    minimum_weight = min(weights.values())
    reserve_weight = sum(
        weights[name] for name, data in HOLDINGS.items() if data["reserve_eligible"]
    )
    liquid_weight = sum(
        weights[name]
        for name, data in HOLDINGS.items()
        if data["redemption_days"] <= LIQUIDITY_WINDOW_DAYS
    )

    company_exposure = defaultdict(float)
    for name, weight in weights.items():
        data = HOLDINGS[name]
        if not data["issuer_exempt"]:
            company_exposure[data["issuer"]] += weight
    largest_company_issuer = max(company_exposure.values(), default=0.0)

    required_reserve = minimum_reserve_allocation()
    results = {
        "total_weight": total_weight,
        "minimum_weight": minimum_weight,
        "reserve_weight": reserve_weight,
        "liquid_weight": liquid_weight,
        "largest_company_issuer": largest_company_issuer,
        "total_pass": abs(total_weight - 100.0) < 1e-9,
        "long_only_pass": minimum_weight >= 0.0,
        "reserve_pass": reserve_weight >= required_reserve,
        "liquidity_pass": liquid_weight >= MINIMUM_LIQUID_SHARE,
        "issuer_pass": largest_company_issuer <= ISSUER_CONCENTRATION_LIMIT,
    }
    results["failed_rules"] = sum(
        not results[key]
        for key in (
            "total_pass",
            "long_only_pass",
            "reserve_pass",
            "liquidity_pass",
            "issuer_pass",
        )
    )
    return results


def pass_fail(passed: bool) -> str:
    return "pass" if passed else "FAIL"


def print_candidate(name: str, weights: dict[str, float]) -> dict[str, float | bool]:
    """Print a candidate's checkable results and return them for reuse/tests."""
    result = assess_portfolio(weights)
    print(f"\nPortfolio {name}")
    print(f"Total weights: {result['total_weight']:.1f} — {pass_fail(result['total_pass'])}")
    print(f"Minimum weight: {result['minimum_weight']:.1f} — {pass_fail(result['long_only_pass'])}")
    print(f"Reserve eligible: {result['reserve_weight']:.1f} — {pass_fail(result['reserve_pass'])}")
    print(f"Five-day liquidity: {result['liquid_weight']:.1f} — {pass_fail(result['liquidity_pass'])}")
    print(f"Largest company issuer: {result['largest_company_issuer']:.1f} — {pass_fail(result['issuer_pass'])}")
    print("Calendar-year loss: requires CIO clarification")
    if result["failed_rules"] == 0:
        print("passes every checkable rule")
    else:
        print(f"fails {result['failed_rules']} rule(s)")
    return result


def main() -> None:
    print(f"Minimum reserve allocation: {minimum_reserve_allocation():.1f}%")
    print("Not mechanically tested: annual turnover, future return objective, or S9 calendar-year loss promise.")
    for name, weights in CANDIDATES.items():
        print_candidate(name, weights)


if __name__ == "__main__":
    main()
