"""Lab 09: ABG FY2026E-FY2030E three-statement pro-forma (USD millions)."""

from copy import deepcopy


YEARS = list(range(2026, 2031))
GROWTH = 0.018
GROSS_MARGIN = 0.1705
SGA_TO_GP = {2026: 0.665, 2027: 0.655, 2028: 0.645, 2029: 0.645, 2030: 0.645}
DEPRECIATION_RATE = 82.4 / 3070.4
IMPAIRMENT = 120.0
CAPEX = 250.0
TAX_RATE = 0.255
INVENTORY_DAYS = 2135.8 / (17999.0 - 3071.7) * 365.0
FLOOR_PLAN_TO_INVENTORY = 2027.0 / 2135.8
OTHER_WC_RATE = 0.008
MIN_CASH = 25.0
REVOLVER_LIMIT = 850.0
REVOLVER_RATE = 0.06
FLOOR_PLAN_RATE = 0.0467
TERM_DEBT_RATE = 0.0544
TERM_DEBT_REPAYMENT = 150.0
SHARE_BUYBACK = 150.0
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 17.951349

OPENING = {
    "revenue": 17999.0, "inventory": 2135.8, "ppe": 3070.4,
    "other_assets": 6371.6, "cash": 40.4, "floor_plan": 2027.0,
    "term_debt": 3572.0, "other_liabilities": 2127.5,
    "equity": 3891.7, "revolver": 0.0,
}


def assert_balanced(model):
    """Raise a descriptive error when a projected balance sheet is invalid."""
    for year in YEARS:
        row = model[year]
        assets = row["cash"] + row["inventory"] + row["ppe"] + row["other_assets"]
        liabilities = (row["floor_plan"] + row["term_debt"] +
                       row["other_liabilities"] + row["revolver"])
        gap = assets - liabilities - row["equity"]
        if abs(gap) > 1e-6:
            raise ValueError(f"FY{year}E is not balanced: balance-sheet gap = {gap:.1f}")
        if row["cash"] < MIN_CASH - 1e-6:
            raise ValueError(f"FY{year}E cash is below minimum: {row['cash']:.1f}")
        if not -1e-6 <= row["revolver"] <= REVOLVER_LIMIT + 1e-6:
            raise ValueError(f"FY{year}E revolver is outside 0.0-{REVOLVER_LIMIT:.1f}: "
                             f"{row['revolver']:.1f}")


def build_model():
    """Build projections. Cash is produced only by FCFE and revolver mechanics."""
    model = {}
    opening = OPENING.copy()

    for year in YEARS:
        revenue = opening["revenue"] * (1.0 + GROWTH)
        gross_profit = revenue * GROSS_MARGIN
        sga = gross_profit * SGA_TO_GP[year]
        depreciation = opening["ppe"] * DEPRECIATION_RATE
        operating_income = gross_profit - sga - depreciation - IMPAIRMENT
        interest = (opening["floor_plan"] * FLOOR_PLAN_RATE +
                    opening["term_debt"] * TERM_DEBT_RATE +
                    opening["revolver"] * REVOLVER_RATE)
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365.0
        floor_plan = inventory * FLOOR_PLAN_TO_INVENTORY
        other_working_capital = OTHER_WC_RATE * (revenue - opening["revenue"])
        ppe = opening["ppe"] + CAPEX - depreciation
        other_assets = opening["other_assets"] + other_working_capital - IMPAIRMENT
        term_debt = opening["term_debt"] - TERM_DEBT_REPAYMENT
        equity = opening["equity"] + net_income - SHARE_BUYBACK

        change_inventory = inventory - opening["inventory"]
        change_floor_plan = floor_plan - opening["floor_plan"]
        fcfe = (net_income + depreciation + IMPAIRMENT - CAPEX - change_inventory -
                other_working_capital + change_floor_plan - TERM_DEBT_REPAYMENT)
        cash_before_revolver = opening["cash"] + fcfe - SHARE_BUYBACK
        revolver = opening["revolver"]
        cash = cash_before_revolver

        if cash < MIN_CASH:
            draw = MIN_CASH - cash
            revolver += draw
            cash = MIN_CASH
        elif revolver > 0.0:
            repayment = min(revolver, cash - MIN_CASH)
            revolver -= repayment
            cash -= repayment

        model[year] = {
            "revenue": revenue, "gross_profit": gross_profit, "sga": sga,
            "depreciation": depreciation, "impairment": IMPAIRMENT,
            "operating_income": operating_income, "interest": interest,
            "pretax_income": pretax_income, "tax": tax, "net_income": net_income,
            "inventory": inventory, "ppe": ppe, "other_assets": other_assets,
            "cash": cash, "floor_plan": floor_plan, "term_debt": term_debt,
            "other_liabilities": opening["other_liabilities"], "revolver": revolver,
            "equity": equity, "other_working_capital": other_working_capital,
            "change_inventory": change_inventory, "change_floor_plan": change_floor_plan,
            "fcfe": fcfe, "cash_before_revolver": cash_before_revolver,
            "capex": CAPEX, "term_debt_repayment": TERM_DEBT_REPAYMENT,
            "share_buyback": SHARE_BUYBACK,
            "balance_sheet_gap": (cash + inventory + ppe + other_assets - floor_plan -
                                  term_debt - opening["other_liabilities"] - revolver - equity),
        }
        opening = {key: model[year][key] for key in OPENING}
    return model


def print_table(title, lines, model):
    print(f"\n{title}")
    print(f"{'USD millions':<30}" + "".join(f"{'FY' + str(year) + 'E':>12}" for year in YEARS))
    for label, key in lines:
        print(f"{label:<30}" + "".join(f"{model[year][key]:>12.1f}" for year in YEARS))


def valuation(model):
    pv_fcfe = sum(model[year]["fcfe"] / (1.0 + COST_OF_EQUITY) ** index
                  for index, year in enumerate(YEARS, start=1))
    terminal_value = ((model[2030]["fcfe"] + TERM_DEBT_REPAYMENT) *
                      (1.0 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH))
    pv_terminal_value = terminal_value / (1.0 + COST_OF_EQUITY) ** len(YEARS)
    equity_value = pv_fcfe + pv_terminal_value
    return equity_value, pv_terminal_value / equity_value, equity_value / SHARES_OUTSTANDING


def verify_known_answer(model):
    expected = {2026: (18323.0, 844.2, 413.6, 211.4, 101.8),
                2030: (19678.3, 971.4, 527.5, 342.3, 719.8)}
    for year, values in expected.items():
        actual = (model[year]["revenue"], model[year]["operating_income"],
                  model[year]["net_income"], model[year]["fcfe"], model[year]["cash"])
        if tuple(round(value, 1) for value in actual) != values:
            raise AssertionError(f"FY{year}E does not match the known answer")
    if round(valuation(model)[2], 2) != 291.75:
        raise AssertionError("Value per share does not match the known answer")


def run_failure_test(model):
    """Prove a manually incorrect FY2026E cash balance is rejected."""
    broken = deepcopy(model)
    broken[2026]["cash"] = 40.4
    try:
        assert_balanced(broken)
    except ValueError as error:
        if "FY2026E" not in str(error) or "-61.4" not in str(error):
            raise AssertionError("Failure test did not report the expected FY2026E gap") from error
        return
    raise AssertionError("Failure test unexpectedly passed")


def main():
    model = build_model()
    assert_balanced(model)  # Must pass before any valuation is performed.
    verify_known_answer(model)
    run_failure_test(model)

    print_table("INCOME STATEMENT", [
        ("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"),
        ("Depreciation", "depreciation"), ("Impairment", "impairment"),
        ("Operating income", "operating_income"), ("Interest expense", "interest"),
        ("Pretax income", "pretax_income"), ("Tax", "tax"), ("Net income", "net_income"),
    ], model)
    print_table("BALANCE SHEET", [
        ("Cash", "cash"), ("Inventory", "inventory"), ("PP&E", "ppe"),
        ("Other assets", "other_assets"), ("Floor plan", "floor_plan"),
        ("Revolver", "revolver"), ("Term debt", "term_debt"),
        ("Other liabilities", "other_liabilities"), ("Equity", "equity"),
    ], model)
    print_table("CASH FLOW / FCFE", [
        ("Net income", "net_income"), ("Depreciation", "depreciation"),
        ("Impairment", "impairment"), ("Capital spending", "capex"),
        ("Change in inventory", "change_inventory"), ("Other working capital", "other_working_capital"),
        ("Change in floor plan", "change_floor_plan"), ("Term-debt repayment", "term_debt_repayment"),
        ("FCFE", "fcfe"), ("Share buyback", "share_buyback"),
        ("Cash before revolver", "cash_before_revolver"),
    ], model)
    print_table("MODEL CHECKS", [
        ("Assets - liabilities - equity", "balance_sheet_gap"),
        ("Cash minimum", "cash"), ("Revolver balance", "revolver"),
    ], model)

    equity_value, after_2030_share, value_per_share = valuation(model)
    print("\nEQUITY VALUATION")
    print(f"Equity value: ${equity_value:,.1f} million")
    print(f"Share of value after 2030: {after_2030_share:.1%}")
    print(f"Value per share: ${value_per_share:,.2f}")
    print("Known-answer and intentional broken-cash failure tests: PASSED")


if __name__ == "__main__":
    main()
