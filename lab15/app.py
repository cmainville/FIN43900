"""Interactive Lab 15 dashboard. Run from repo root with Streamlit."""
import hashlib
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from lab15 import portfolio as engine  # noqa: E402

# Read and compile the actual engine source on every Streamlit rerun. Python's
# timestamp-based bytecode cache can otherwise miss rapid source edits.
exec(compile(Path(engine.__file__).read_bytes(), engine.__file__, "exec"), engine.__dict__)
DEFAULT_CSV = Path(__file__).with_name("prices_growth.csv")


def solve(assets, returns, vols, correlations, objective, eligible, reserve):
    return engine.optimize_portfolio(assets, returns, vols, correlations,
                                     objective, eligible, reserve)


def show_result(label, result, assets):
    st.subheader(label)
    if not result["feasible"]:
        st.error("no mix meets the objective")
        st.caption(f"0 feasible of {result['candidate_count']:,} candidate allocations")
        return
    st.write({asset: f"{weight:.0%}" for asset, weight in zip(assets, result["weights"])})
    st.metric("Expected annual return", f"{result['return']:.2%}")
    st.metric("Annualized volatility", f"{result['volatility']:.2%}")
    st.metric("Reserve-eligible allocation", f"{result['reserve']:.2%}")
    st.caption(f"Feasible: {result['feasible_count']:,} of {result['candidate_count']:,} allocations")


def main():
    st.set_page_config(page_title="Portfolio Stability Dashboard", layout="wide")
    st.title("Portfolio Stability Dashboard")
    st.write("Built with AI help. A learning demonstration, not investment advice.")
    st.sidebar.header("Scenario")
    mode = st.sidebar.radio("Application mode", ("Meridian Foundation Training",
                                             "Long-Term Growth Portfolio"), key="mode")
    is_meridian = mode.startswith("Meridian")
    if st.session_state.get("last_mode") != mode:
        for key in list(st.session_state):
            if key.startswith(("return_", "eligible_")) or key in ("objective", "reserve_minimum", "last36"):
                del st.session_state[key]
        st.session_state["last_mode"] = mode
    if is_meridian:
        assets = engine.ASSETS
        full = {"assets": assets, "expected_returns": engine.EXPECTED_RETURNS,
                "volatilities": engine.VOLATILITIES, "correlations": engine.CORRELATIONS}
        baseline_objective, baseline_reserve = engine.OBJECTIVE_RETURN, 0.03
        baseline_eligible = engine.RESERVE_ELIGIBLE
        st.sidebar.file_uploader("Monthly price CSV", type="csv", disabled=True,
                                 help="Meridian uses fixed course assumptions. Switch modes to upload prices.")
        st.sidebar.toggle("Last 36 monthly returns", disabled=True,
                          help="Meridian has no historical price series.")
    else:
        uploaded = st.sidebar.file_uploader("Monthly price CSV", type="csv")
        source = uploaded if uploaded is not None else DEFAULT_CSV
        last36 = st.sidebar.toggle("Last 36 monthly returns", value=False, key="last36")
        signature = (hashlib.sha256(uploaded.getvalue()).hexdigest() if uploaded is not None
                     else hashlib.sha256(DEFAULT_CSV.read_bytes()).hexdigest(), last36)
        if st.session_state.get("data_signature") != signature:
            for key in list(st.session_state):
                if key.startswith("return_"):
                    del st.session_state[key]
            st.session_state["data_signature"] = signature
        try:
            if uploaded is not None:
                uploaded.seek(0)
            full = engine.estimate_from_monthly_prices(source)
            if uploaded is not None:
                uploaded.seek(0)
            current_estimates = engine.estimate_from_monthly_prices(source, last_36=last36)
        except (ValueError, OSError) as exc:
            st.error(f"Price data error: {exc}")
            st.stop()
        assets = full["assets"]
        baseline_objective, baseline_reserve = 0.06, 0.0
        baseline_eligible = frozenset()
        st.caption(f"{current_estimates['observation_count']} monthly returns, "
                   f"{current_estimates['start_date']} to {current_estimates['end_date']}; annual estimates")
    objective = st.sidebar.number_input("Required annual return (%)", value=baseline_objective * 100,
                                         step=0.5, key="objective") / 100
    reserve = st.sidebar.number_input("Minimum reserve (%)", min_value=0.0, max_value=100.0,
                                       value=baseline_reserve * 100, step=1.0,
                                       key="reserve_minimum") / 100
    baseline = solve(assets, full["expected_returns"], full["volatilities"],
                     full["correlations"], baseline_objective, baseline_eligible, baseline_reserve)
    st.subheader("Current inputs")
    assumptions = full if is_meridian else current_estimates
    edited_returns, eligible = [], []
    for i, asset in enumerate(assets):
        left, middle, right = st.columns((2, 1, 1))
        left.write(asset)
        value = middle.number_input(f"Expected annual return (%) — {asset}",
                                    value=float(assumptions["expected_returns"][i] * 100),
                                    step=0.1, key=f"return_{i}")
        edited_returns.append(value / 100)
        if right.checkbox(f"Reserve eligible — {asset}", value=asset in baseline_eligible,
                          key=f"eligible_{i}"):
            eligible.append(asset)
    try:
        current = solve(assets, edited_returns, assumptions["volatilities"],
                        assumptions["correlations"], objective, eligible, reserve)
    except ValueError as exc:
        st.error(f"Invalid portfolio inputs: {exc}")
        st.stop()
    left, right = st.columns(2)
    with left:
        show_result("Baseline as loaded", baseline, assets)
    with right:
        show_result("Current adjusted portfolio", current, assets)
    change = engine.largest_weight_change(baseline, current)
    if change is not None:
        st.metric("Largest individual weight change", f"{change:.0f} percentage points")
    else:
        st.info("Weight change unavailable because at least one scenario is infeasible.")
    if not is_meridian and tuple(assets) == ("VTI", "VXUS", "XLE", "IWM", "IAU"):
        benchmark = (0.45, 0.25, 0.10, 0.10, 0.10)
        covariance = engine.covariance_matrix(full["volatilities"], full["correlations"])
        _, risk = engine.portfolio_variance_and_volatility(benchmark, covariance)
        ret = engine.expected_portfolio_return(benchmark, full["expected_returns"])
        st.subheader("Student starting benchmark (45 / 25 / 10 / 10 / 10)")
        st.write(f"Estimated return: {ret:.2%}; annualized volatility: {risk:.2%}")


if __name__ == "__main__":
    main()
