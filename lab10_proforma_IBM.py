"""IBM rebuilt FY2026E–FY2030E FCFE model; USD millions, educational only.
Sources: FY2025 10-K and Q2 2026 10-Q.  It separates IBM Financing,
finite-lived intangibles, debt funding, and the reported Confluent acquisition.
"""
from copy import deepcopy

YEARS = list(range(2026, 2031))
# IBM-reported GAAP history, USD millions. FY2025 10-K presents the three-year
# income-statement comparatives; FY2023/FY2024 10-Ks were used to cross-check
# balance-sheet amounts. This table is retained for Lab 10 traceability.
HISTORICAL_10K = {
    2023: {"revenue": 61860., "gross_profit": 34300., "sga": 19003., "net_income": 7502.,
           "inventory": 1161., "ppe": 5492., "equity": 22533., "depreciation": 2109.,
           "capex_ppe": 1245., "software_investment": 565., "pretax": 8690., "tax": 1176.},
    2024: {"revenue": 62753., "gross_profit": 35551., "sga": 19688., "net_income": 6023.,
           "inventory": 1289., "ppe": 5726., "equity": 27307., "depreciation": 2168.,
           "capex_ppe": 1048., "software_investment": 637., "pretax": 5797., "tax": -218.},
    2025: {"revenue": 67535., "gross_profit": 39297., "sga": 20123., "net_income": 10593.,
           "inventory": 1220., "ppe": 5894., "equity": 32648., "depreciation": 2284.,
           "capex_ppe": 1091., "software_investment": 647., "pretax": 10328., "tax": -242.},
}
SEGMENT_BASE = {"software": 29962., "consulting": 21055., "infrastructure": 15718., "financing": 737., "other": 63.}
SEGMENT_GROWTH = {
    2026: {"software": .08, "consulting": .02, "infrastructure": -.01, "financing": .05, "other": 0},
    2027: {"software": .07, "consulting": .03, "infrastructure": .02, "financing": .03, "other": 0},
    2028: {"software": .06, "consulting": .035, "infrastructure": .025, "financing": .03, "other": 0},
    2029: {"software": .055, "consulting": .035, "infrastructure": .025, "financing": .025, "other": 0},
    2030: {"software": .05, "consulting": .03, "infrastructure": .02, "financing": .02, "other": 0},
}
# FY2025 balance sheet, reclassified for model schedules. Other assets excludes receivables and finite-lived intangibles.
OPENING = {"cash": 13587., "trade_ar": 8112., "finance_ar": 16183., "other_ar": 1052., "inventory": 1220., "ppe": 5894.,
           "intangibles": 11391., "other_assets": 94441., "payables": 4756., "deferred_revenue": 20372.,
           "finance_debt": 15093., "corporate_debt": 46167., "other_liabilities": 32752., "equity": 32740., "revolver": 0.}
# FY2025 10-K Note N's disclosed amortization schedule, split between capitalized software and acquired intangibles.
SOFTWARE_AMORT = {2026: 490., 2027: 333., 2028: 141., 2029: 0., 2030: 0.}
ACQUIRED_AMORT = {2026: 2283., 2027: 2245., 2028: 1939., 2029: 1254., 2030: 812.}
# Q2 2026: Confluent acquisition cash spending and increase in reported net intangibles.
ACQUISITION_CASH = {2026: 10480., 2027: 0., 2028: 0., 2029: 0., 2030: 0.}
ACQUIRED_INTANGIBLES = {2026: 2564., 2027: 0., 2028: 0., 2029: 0., 2030: 0.}

# Forecast assumptions. Cash gross profit and cash SG&A exclude finite-lived intangible amortization,
# allowing the filed amortization schedule to affect reported margins and FCFE consistently.
CASH_GROSS_MARGIN = {2026: .605, 2027: .608, 2028: .611, 2029: .613, 2030: .615}
CASH_SGA_RATE = {2026: .279, 2027: .278, 2028: .277, 2029: .276, 2030: .275}
RND_RATE, TAX_RATE, DEPR_RATE = .122, .160, .390
PPE_CAPEX_RATE, SOFTWARE_INVEST_RATE = .017, .010
TRADE_AR_RATE, OTHER_AR_RATE, INVENTORY_DAYS = .120, .016, 15.76
PAYABLES_TO_COGS, DEFERRED_REV_RATE = .1684, .3016
# Separately forecast Financing receivables: Q2 2026 was $13.782bn, down from $16.183bn at FY2025.
FINANCE_AR = {2026: 14000., 2027: 14500., 2028: 15000., 2029: 15500., 2030: 16000.}
FINANCE_DEBT_RATIO = 15093. / 16183.
CORPORATE_DEBT = {2026: 49000., 2027: 48000., 2028: 47500., 2029: 47000., 2030: 46500.}
INTEREST_RATE, DIVIDENDS, MIN_CASH = .033, 6350., 5000.
REVOLVER_LIMIT, REVOLVER_RATE = 10000., .055
# FY2025 reported weighted-average diluted shares, in millions. The Q2 2026
# 942.134m figure is shares outstanding (basic), not a current diluted count.
COST_OF_EQUITY, TERMINAL_GROWTH, DILUTED_SHARES = .090, .025, 948.675228

def assets(r):
    return sum(r[k] for k in ("cash", "trade_ar", "finance_ar", "other_ar", "inventory", "ppe", "intangibles", "other_assets"))

def l_and_e(r):
    return sum(r[k] for k in ("payables", "deferred_revenue", "finance_debt", "corporate_debt", "other_liabilities", "equity", "revolver"))

def assert_balanced(model):
    for y, r in model.items():
        if abs(assets(r) - l_and_e(r)) > 1e-6: raise ValueError(f"FY{y}E does not balance: {assets(r)-l_and_e(r):.4f}")
        if r["cash"] < MIN_CASH - 1e-6: raise ValueError(f"FY{y}E cash below minimum")
        if not 0 <= r["revolver"] <= REVOLVER_LIMIT: raise ValueError(f"FY{y}E revolver out of bounds")

def build_model():
    if abs(assets(OPENING) - l_and_e(OPENING)) > 1e-6: raise ValueError("Opening balance sheet does not balance")
    model, op, segments = {}, OPENING.copy(), SEGMENT_BASE.copy()
    for y in YEARS:
        segments = {k: v * (1 + SEGMENT_GROWTH[y][k]) for k, v in segments.items()}
        revenue = sum(segments.values())
        amort = SOFTWARE_AMORT[y] + ACQUIRED_AMORT[y]
        cash_gp = revenue * CASH_GROSS_MARGIN[y]
        gross_profit = cash_gp - SOFTWARE_AMORT[y]
        cogs = revenue - gross_profit
        cash_sga = revenue * CASH_SGA_RATE[y]
        sga, rnd = cash_sga + ACQUIRED_AMORT[y], revenue * RND_RATE
        ebit = gross_profit - sga - rnd
        finance_debt, corporate_debt = FINANCE_AR[y] * FINANCE_DEBT_RATIO, CORPORATE_DEBT[y]
        interest = (op["finance_debt"] + op["corporate_debt"]) * INTEREST_RATE + op["revolver"] * REVOLVER_RATE
        pretax = ebit - interest; tax = max(0., pretax) * TAX_RATE; net_income = pretax - tax
        trade_ar, other_ar = revenue * TRADE_AR_RATE, revenue * OTHER_AR_RATE
        finance_ar, inventory = FINANCE_AR[y], cogs * INVENTORY_DAYS / 365.
        payables, deferred_revenue = cogs * PAYABLES_TO_COGS, revenue * DEFERRED_REV_RATE
        depreciation, ppe_capex = op["ppe"] * DEPR_RATE, revenue * PPE_CAPEX_RATE
        ppe = op["ppe"] + ppe_capex - depreciation
        software_investment = revenue * SOFTWARE_INVEST_RATE
        intangibles = op["intangibles"] + software_investment + ACQUIRED_INTANGIBLES[y] - amort
        other_assets = op["other_assets"] + ACQUISITION_CASH[y] - ACQUIRED_INTANGIBLES[y]
        debt_change = finance_debt + corporate_debt - op["finance_debt"] - op["corporate_debt"]
        equity = op["equity"] + net_income - DIVIDENDS
        fcfe_pre = (net_income + depreciation + amort - ppe_capex - software_investment - ACQUISITION_CASH[y]
                    - (trade_ar-op["trade_ar"]) - (finance_ar-op["finance_ar"]) - (other_ar-op["other_ar"])
                    - (inventory-op["inventory"]) + (payables-op["payables"]) + (deferred_revenue-op["deferred_revenue"]) + debt_change)
        cash = op["cash"] + fcfe_pre - DIVIDENDS
        revolver, revolver_change = op["revolver"], 0.
        if cash < MIN_CASH:
            revolver_change = MIN_CASH - cash; revolver += revolver_change; cash = MIN_CASH
        elif revolver > 0:
            revolver_change = -min(revolver, cash-MIN_CASH); revolver += revolver_change; cash += revolver_change
        r = {"revenue": revenue, "software": segments["software"], "consulting": segments["consulting"], "infrastructure": segments["infrastructure"], "financing": segments["financing"], "gross_profit": gross_profit, "sga": sga, "rnd": rnd, "ebit": ebit, "interest": interest, "tax": tax, "net_income": net_income, "cash": cash, "trade_ar": trade_ar, "finance_ar": finance_ar, "other_ar": other_ar, "inventory": inventory, "ppe": ppe, "intangibles": intangibles, "other_assets": other_assets, "payables": payables, "deferred_revenue": deferred_revenue, "finance_debt": finance_debt, "corporate_debt": corporate_debt, "other_liabilities": op["other_liabilities"], "equity": equity, "revolver": revolver, "depreciation": depreciation, "amortization": amort, "ppe_capex": ppe_capex, "software_investment": software_investment, "acquisition_cash": ACQUISITION_CASH[y], "debt_change": debt_change, "fcfe": fcfe_pre+revolver_change, "dividends": DIVIDENDS}
        # Totals are calculated outputs, shown so the printed balance sheet is complete.
        r["cogs"] = cogs
        r["pretax_income"] = pretax
        r["total_assets"] = assets(r)
        r["total_liabilities_equity"] = l_and_e(r)
        r["balance_gap"] = r["total_assets"] - r["total_liabilities_equity"]
        model[y] = r; op = {k:r[k] for k in OPENING}
    return model

def valuation(m):
    pv = sum(m[y]["fcfe"]/(1+COST_OF_EQUITY)**i for i,y in enumerate(YEARS,1))
    terminal_fcfe = m[2030]["fcfe"]*(1+TERMINAL_GROWTH)
    if terminal_fcfe <= 0: raise ValueError("Negative terminal FCFE")
    tv = terminal_fcfe/(COST_OF_EQUITY-TERMINAL_GROWTH); pvtv = tv/(1+COST_OF_EQUITY)**5
    ev = pv+pvtv; return pv,terminal_fcfe,tv,pvtv,ev,ev/DILUTED_SHARES

def print_table(title, lines, m):
    print(f"\n{title}\n{'USD millions':<33}"+''.join(f"FY{y}E".rjust(13) for y in YEARS))
    for label,key in lines: print(f"{label:<33}"+''.join(f"{m[y][key]:>13,.1f}" for y in YEARS))

def main():
    m=build_model(); assert_balanced(m)
    broken=deepcopy(m); broken[2026]["cash"]-=1
    try: assert_balanced(broken)
    except ValueError: pass
    else: raise AssertionError("Broken-cash test failed")
    print_table("SEGMENT REVENUE", [("Software","software"),("Consulting","consulting"),("Infrastructure","infrastructure"),("Financing","financing"),("Total revenue","revenue")],m)
    print_table("INCOME STATEMENT", [("Revenue","revenue"),("COGS","cogs"),("Gross profit","gross_profit"),("SG&A incl acquired amort.","sga"),("R&D","rnd"),("EBIT","ebit"),("Interest","interest"),("Pretax income","pretax_income"),("Tax","tax"),("Net income","net_income")],m)
    print_table("BALANCE SHEET", [("Cash","cash"),("Trade receivables","trade_ar"),("Financing receivables","finance_ar"),("Other receivables","other_ar"),("Inventory","inventory"),("PP&E","ppe"),("Finite-lived intangibles","intangibles"),("Other assets","other_assets"),("Total assets","total_assets"),("Accounts payable","payables"),("Deferred revenue","deferred_revenue"),("Financing debt","finance_debt"),("Corporate debt","corporate_debt"),("Other liabilities","other_liabilities"),("Revolver","revolver"),("Equity","equity"),("Total liabilities + equity","total_liabilities_equity")],m)
    print_table("FCFE / CHECKS", [("Depreciation","depreciation"),("Intangible amortization","amortization"),("PP&E capex","ppe_capex"),("Software investment","software_investment"),("Acquisition cash","acquisition_cash"),("Net debt financing","debt_change"),("FCFE","fcfe"),("Balance-sheet gap","balance_gap"),("Revolver","revolver")],m)
    pv,tf,tv,pvtv,ev,pps=valuation(m)
    print(f"\nVALUATION\nPV forecast FCFE: ${pv:,.1f}m\nTerminal FCFE: ${tf:,.1f}m\nPV terminal value: ${pvtv:,.1f}m\nImplied equity value: ${ev:,.1f}m\nImplied value/share: ${pps:,.2f}")
    print("Balance, minimum-cash, revolver, and broken-cash checks: PASSED")
if __name__ == "__main__": main()
