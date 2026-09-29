"""Lab 11 one-at-a-time sensitivities for the existing IBM Lab 10 model.

This file imports ``lab10_proforma_IBM`` and changes only one existing model
input at a time.  It does not duplicate or rebuild the pro-forma logic.
All currency outputs are USD millions except per-share value.
"""

from copy import deepcopy
from dataclasses import dataclass

import lab10_proforma_IBM as lab10


FORECAST_YEARS = tuple(lab10.YEARS)

# Simple judgment ranges around the Lab 10 paths.  The software range is
# plus/minus 2 percentage points of annual growth; the cash-gross-margin range
# is plus/minus 100 basis points in every forecast year.
SOFTWARE_GROWTH_CASES = {
    "Lower": {year: lab10.SEGMENT_GROWTH[year]["software"] - 0.02 for year in FORECAST_YEARS},
    "Base": {year: lab10.SEGMENT_GROWTH[year]["software"] for year in FORECAST_YEARS},
    "Higher": {year: lab10.SEGMENT_GROWTH[year]["software"] + 0.02 for year in FORECAST_YEARS},
}

CASH_GROSS_MARGIN_CASES = {
    "Lower": {year: lab10.CASH_GROSS_MARGIN[year] - 0.01 for year in FORECAST_YEARS},
    "Base": {year: lab10.CASH_GROSS_MARGIN[year] for year in FORECAST_YEARS},
    "Higher": {year: lab10.CASH_GROSS_MARGIN[year] + 0.01 for year in FORECAST_YEARS},
}

PREDICTIONS = (
    (
        "Software revenue growth",
        "YoY growth, FY2026E-FY2030E: base 8.0% / 7.0% / 6.0% / 5.5% / 5.0% to "
        "lower 6.0% / 5.0% / 4.0% / 3.5% / 3.0% or higher 10.0% / 9.0% / 8.0% / "
        "7.5% / 7.0%.",
        "Lower case: EBIT, FCFE, and value/share down. Higher case: all three up.",
        "Material but not extreme: roughly $0.8bn of FY2030 EBIT and FCFE, and about "
        "$10 per share, in either direction.",
        "AI can lift demand if workloads convert from pilots to production and support renewals, "
        "pricing, and cross-sell; it can detract if AI budgets displace existing software spend "
        "or competition pressures price and retention.",
    ),
    (
        "Cash gross margin",
        "Cash gross profit as a percent of revenue, FY2026E-FY2030E: base 60.5% / "
        "60.8% / 61.1% / 61.3% / 61.5% to lower 59.5% / 59.8% / 60.1% / 60.3% / "
        "60.5% or higher 61.5% / 61.8% / 62.1% / 62.3% / 62.5%.",
        "Lower case: EBIT, FCFE, and value/share down. Higher case: all three up.",
        "Material: roughly $0.8bn of FY2030 EBIT, $0.7bn of FCFE, and about $10 per "
        "share, in either direction.",
        "AI can improve margin through higher-value software mix and lower delivery/support costs; "
        "it can detract if cloud/GPU inference, data, security, partner, or support costs exceed "
        "the revenue and price captured from AI offerings.",
    ),
)


def _snapshot_inputs():
    """Capture all uppercase Lab 10 inputs so every case starts from base."""
    return {
        name: deepcopy(value)
        for name, value in vars(lab10).items()
        if name.isupper() and isinstance(value, (dict, list, tuple, int, float, str))
    }


ORIGINAL_INPUTS = _snapshot_inputs()


def _restore_inputs():
    for name, value in ORIGINAL_INPUTS.items():
        setattr(lab10, name, deepcopy(value))


@dataclass
class CaseResult:
    driver: str
    case: str
    input_path: dict
    valid: bool
    ebit_2030: float | None = None
    fcfe_2030: float | None = None
    value_per_share: float | None = None
    max_abs_balance_gap: float | None = None
    minimum_cash: float | None = None
    maximum_revolver: float | None = None
    error: str | None = None


def _run_case(driver, case, input_path):
    """Restore the model, apply one input path, and validate the result."""
    _restore_inputs()

    if driver == "Software revenue growth":
        for year, value in input_path.items():
            lab10.SEGMENT_GROWTH[year]["software"] = value
    elif driver == "Cash gross margin":
        lab10.CASH_GROSS_MARGIN = deepcopy(input_path)
    else:
        raise ValueError(f"Unknown driver: {driver}")

    try:
        model = lab10.build_model()
        lab10.assert_balanced(model)
        value_per_share = lab10.valuation(model)[-1]
        return CaseResult(
            driver=driver,
            case=case,
            input_path=deepcopy(input_path),
            valid=True,
            ebit_2030=model[2030]["ebit"],
            fcfe_2030=model[2030]["fcfe"],
            value_per_share=value_per_share,
            max_abs_balance_gap=max(abs(model[year]["balance_gap"]) for year in FORECAST_YEARS),
            minimum_cash=min(model[year]["cash"] for year in FORECAST_YEARS),
            maximum_revolver=max(model[year]["revolver"] for year in FORECAST_YEARS),
        )
    except (AssertionError, ValueError, ZeroDivisionError) as exc:
        return CaseResult(
            driver=driver,
            case=case,
            input_path=deepcopy(input_path),
            valid=False,
            error=str(exc),
        )


def run_sensitivities():
    """Run low/base/high OAT cases and finish with the original base restored."""
    _restore_inputs()
    original_base_model = lab10.build_model()
    lab10.assert_balanced(original_base_model)
    original_base_value = lab10.valuation(original_base_model)[-1]

    results = {}
    case_sets = {
        "Software revenue growth": SOFTWARE_GROWTH_CASES,
        "Cash gross margin": CASH_GROSS_MARGIN_CASES,
    }
    for driver, cases in case_sets.items():
        results[driver] = [
            _run_case(driver, case, input_path)
            for case, input_path in cases.items()
        ]

    # Restore and rerun, rather than merely assuming the module is back at base.
    _restore_inputs()
    restored_base_model = lab10.build_model()
    lab10.assert_balanced(restored_base_model)
    restored_base_value = lab10.valuation(restored_base_model)[-1]

    broken = deepcopy(restored_base_model)
    broken[2026]["cash"] -= 1.0
    broken_cash_detected = False
    try:
        lab10.assert_balanced(broken)
    except ValueError:
        broken_cash_detected = True

    restored_check = {
        "inputs_match": _snapshot_inputs() == ORIGINAL_INPUTS,
        "outputs_match": restored_base_model == original_base_model
        and restored_base_value == original_base_value,
        "accounting_checks_pass": True,
        "broken_cash_detected": broken_cash_detected,
        "base_ebit_2030": restored_base_model[2030]["ebit"],
        "base_fcfe_2030": restored_base_model[2030]["fcfe"],
        "base_value_per_share": restored_base_value,
        "max_abs_balance_gap": max(
            abs(restored_base_model[year]["balance_gap"]) for year in FORECAST_YEARS
        ),
    }
    return results, restored_check


def _format_path(path):
    return " / ".join(f"{path[year]:.1%}" for year in FORECAST_YEARS)


def _print_driver(driver, results):
    base = next(
        (result for result in results if result.case == "Base" and result.valid),
        None,
    )
    print(f"\n{driver.upper()}")
    print("Years: " + " / ".join(f"FY{year}E" for year in FORECAST_YEARS))
    print(
        "Case | Actual input path | FY2030 EBIT | Delta EBIT | FY2030 FCFE | "
        "Delta FCFE | Value/share | Delta value/share | Checks"
    )
    for result in results:
        if not result.valid:
            print(f"{result.case} | {_format_path(result.input_path)} | INVALID: {result.error}")
            continue
        delta_ebit = (
            f"${result.ebit_2030-base.ebit_2030:+,.1f}m" if base else "N/A"
        )
        delta_fcfe = (
            f"${result.fcfe_2030-base.fcfe_2030:+,.1f}m" if base else "N/A"
        )
        delta_value = (
            f"${result.value_per_share-base.value_per_share:+,.2f}" if base else "N/A"
        )
        print(
            f"{result.case} | {_format_path(result.input_path)} | "
            f"${result.ebit_2030:,.1f}m | {delta_ebit} | "
            f"${result.fcfe_2030:,.1f}m | {delta_fcfe} | "
            f"${result.value_per_share:,.2f} | {delta_value} | PASS"
        )

    low = next((result for result in results if result.case == "Lower" and result.valid), None)
    high = next((result for result in results if result.case == "Higher" and result.valid), None)
    if low and high:
        print(
            "Low-to-high spans: "
            f"EBIT ${high.ebit_2030-low.ebit_2030:,.1f}m; "
            f"FCFE ${high.fcfe_2030-low.fcfe_2030:,.1f}m; "
            f"value/share ${high.value_per_share-low.value_per_share:,.2f}."
        )
    else:
        print("Low-to-high spans: INVALID because a boundary case failed.")
    print(
        "Accounting visibility: "
        f"max absolute balance gap ${max(r.max_abs_balance_gap for r in results if r.valid):,.4f}m; "
        f"minimum cash ${min(r.minimum_cash for r in results if r.valid):,.1f}m; "
        f"maximum revolver ${max(r.maximum_revolver for r in results if r.valid):,.1f}m."
    )


def main():
    print("PREDICTION FRAMEWORK")
    for driver, input_change, direction, rough_size, reason in PREDICTIONS:
        print(f"{driver}: {input_change}")
        print(f"Expected direction: {direction}")
        print(f"Expected size: {rough_size}")
        print(f"Reason: {reason}")

    results, restored = run_sensitivities()
    for driver, driver_results in results.items():
        _print_driver(driver, driver_results)

    print("\nRESTORED BASE CHECK")
    for key, value in restored.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
