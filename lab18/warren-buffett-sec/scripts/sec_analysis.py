"""Five-year SEC 10-K financial analysis for the three-investor panel."""

import argparse
import json
import os
import re
import ssl
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

import certifi


TAGS = {
    "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"),
    "net_income": ("NetIncomeLoss",),
    "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",),
    "capital_spending": ("PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"),
    "stockholders_equity": ("StockholdersEquity",),
    "liabilities": ("Liabilities",),
    "research_and_development": ("ResearchAndDevelopmentExpense",),
}
MONEY = ("revenue", "net_income", "operating_cash_flow", "capital_spending", "stockholders_equity", "liabilities", "research_and_development", "owner_earnings")
INVESTOR_CHECKS = {
    "Warren Buffett": ("ROE >= 15% in all five years", "Positive owner earnings in all five years", "Owner earnings increased first to last"),
    "Cathie Wood": ("Revenue CAGR >= 15%", "Latest R&D / revenue >= 5%"),
    "Michael Burry": ("Operating cash flow >= net income in all five years", "Latest liabilities / equity <= 2"),
}


def fetch_json(url):
    email = os.environ.get("SEC_CONTACT_EMAIL", "").strip()
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        raise ValueError("Set SEC_CONTACT_EMAIL to your email address before contacting SEC EDGAR.")
    request = Request(url, headers={"User-Agent": f"FIN439 Lab 19 {email}", "Accept-Encoding": "identity"})
    with urlopen(request, timeout=30, context=ssl.create_default_context(cafile=certifi.where())) as response:
        return json.load(response)


def cik_for_ticker(ticker):
    ticker = ticker.upper().strip()
    if not re.fullmatch(r"[A-Z0-9.-]{1,12}", ticker):
        raise ValueError("Enter a valid stock ticker.")
    companies = fetch_json("https://www.sec.gov/files/company_tickers.json")
    for item in companies.values():
        if item["ticker"].upper() == ticker:
            return str(item["cik_str"]).zfill(10), item["title"]
    raise ValueError(f"Ticker {ticker} was not found in the SEC ticker list.")


def annual_fact(fact):
    if fact.get("form") != "10-K" or "start" not in fact:
        return False
    try:
        days = (date.fromisoformat(fact["end"]) - date.fromisoformat(fact["start"])).days
    except (KeyError, ValueError):
        return False
    return 330 <= days <= 400


def pick(facts, tags, end, duration):
    gaap = facts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        candidates = [f for f in gaap.get(tag, {}).get("units", {}).get("USD", [])
                      if f.get("form") == "10-K" and f.get("end") == end
                      and (annual_fact(f) if duration else "start" not in f)]
        if candidates:
            best = max(candidates, key=lambda f: (f.get("filed", ""), f.get("accn", "")))
            return best["val"], f"us-gaap:{tag}"
    return None, "not found"


def check(values, rule):
    if len(values) != 5 or any(value is None for value in values):
        return "Not Known"
    return "Pass" if rule(values) else "Fail"


def cathie_checks(rows, growth_threshold=0.15):
    """Return statuses and calculated values; None always means unknown."""
    revenues = [r["values"]["revenue"] for r in rows]
    cagr = None if len(revenues) != 5 or any(v is None for v in revenues) or revenues[0] <= 0 or revenues[-1] < 0 else (revenues[-1] / revenues[0]) ** (1 / 4) - 1
    latest = rows[-1]["values"] if len(rows) == 5 else {}
    revenue, rd = latest.get("revenue"), latest.get("research_and_development")
    rd_ratio = None if revenue is None or revenue <= 0 or rd is None else rd / revenue
    return ({"Revenue CAGR >= 15%": "Not Known" if cagr is None else ("Pass" if cagr >= growth_threshold else "Fail"),
             "Latest R&D / revenue >= 5%": "Not Known" if rd_ratio is None else ("Pass" if rd_ratio >= 0.05 else "Fail")},
            {"revenue_cagr": cagr, "rd_revenue_ratio": rd_ratio})


def verdict(statuses):
    if "Fail" in statuses:
        return "Fail"
    if "Not Known" in statuses:
        return "Not Known"
    return "Pass"


def analyze_facts(facts, ticker, company):
    gaap = facts.get("facts", {}).get("us-gaap", {})
    ends = set()
    for tags in (TAGS["revenue"],):
        for tag in tags:
            for fact in gaap.get(tag, {}).get("units", {}).get("USD", []):
                if annual_fact(fact):
                    ends.add(fact["end"])
    years = sorted(ends, reverse=True)[:5]
    rows = []
    for end in reversed(years):
        row = {"fiscal_year_end": end, "values": {}, "tags": {}}
        for metric, tags in TAGS.items():
            value, tag = pick(facts, tags, end, metric not in ("stockholders_equity", "liabilities"))
            row["values"][metric], row["tags"][metric] = value, tag
        income = row["values"]["net_income"]
        equity = row["values"]["stockholders_equity"]
        row["values"]["roe"] = None if income is None or equity is None or equity <= 0 else income / equity * 100
        row["tags"]["roe"] = "us-gaap:NetIncomeLoss / us-gaap:StockholdersEquity"
        cash = row["values"]["operating_cash_flow"]
        capex = row["values"]["capital_spending"]
        row["values"]["owner_earnings"] = None if cash is None or capex is None else cash - capex
        capex_tag = row["tags"]["capital_spending"]
        if capex_tag == "not found":
            capex_tag = "not found (tried us-gaap:PaymentsToAcquirePropertyPlantAndEquipment / us-gaap:PaymentsToAcquireProductiveAssets)"
        row["tags"]["owner_earnings"] = "us-gaap:NetCashProvidedByUsedInOperatingActivities - " + capex_tag
        liabilities = row["values"]["liabilities"]
        row["values"]["liabilities_equity_ratio"] = None if liabilities is None or equity is None or equity <= 0 else liabilities / equity
        row["tags"]["liabilities_equity_ratio"] = "us-gaap:Liabilities / us-gaap:StockholdersEquity"
        rows.append(row)
    roes = [r["values"]["roe"] for r in rows]
    earnings = [r["values"]["owner_earnings"] for r in rows]
    checks = {
        "ROE >= 15% in all five years": check(roes, lambda v: all(x >= 15 for x in v)),
        "Positive owner earnings in all five years": check(earnings, lambda v: all(x > 0 for x in v)),
        "Owner earnings increased first to last": check(earnings, lambda v: v[-1] > v[0]),
    }
    wood, derived = cathie_checks(rows)
    cash_gaps = [None if r["values"]["operating_cash_flow"] is None or r["values"]["net_income"] is None else r["values"]["operating_cash_flow"] - r["values"]["net_income"] for r in rows]
    cash_checks = "Fail" if any(gap is not None and gap < 0 for gap in cash_gaps) else "Not Known" if len(cash_gaps) != 5 or any(gap is None for gap in cash_gaps) else "Pass"
    ratio = rows[-1]["values"]["liabilities_equity_ratio"] if len(rows) == 5 else None
    burry = {"Operating cash flow >= net income in all five years": cash_checks,
             "Latest liabilities / equity <= 2": "Not Known" if ratio is None else ("Pass" if ratio <= 2 else "Fail")}
    checks.update(wood)
    checks.update(burry)
    details = {
        "ROE >= 15% in all five years": ", ".join("not known" if v is None else f"{v:.1f}%" for v in roes),
        "Positive owner earnings in all five years": ", ".join("not found" if v is None else f"{v / 1_000_000:,.0f}" for v in earnings) + " USD millions",
        "Owner earnings increased first to last": "not known" if len(earnings) != 5 or earnings[0] is None or earnings[-1] is None else f"{earnings[0] / 1_000_000:,.0f} to {earnings[-1] / 1_000_000:,.0f} USD millions",
        "Revenue CAGR >= 15%": "not known" if derived["revenue_cagr"] is None else f"{derived['revenue_cagr'] * 100:.2f}%",
        "Latest R&D / revenue >= 5%": "not found" if derived["rd_revenue_ratio"] is None else f"{derived['rd_revenue_ratio'] * 100:.2f}%",
        "Operating cash flow >= net income in all five years": ", ".join("not known" if r["values"]["operating_cash_flow"] is None or r["values"]["net_income"] is None else "yes" if r["values"]["operating_cash_flow"] >= r["values"]["net_income"] else "no" for r in rows),
        "Latest liabilities / equity <= 2": "not known" if ratio is None else f"{ratio:.2f}x",
    }
    verdicts = {investor: verdict([checks[name] for name in names]) for investor, names in INVESTOR_CHECKS.items()}
    return {"ticker": ticker.upper(), "company": company, "cik": facts.get("cik"), "rows": rows, "checks": checks, "details": details, "verdicts": verdicts, "derived": derived}


def analyze(ticker):
    cik, company = cik_for_ticker(ticker)
    facts = fetch_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json")
    return analyze_facts(facts, ticker, company)


def analyze_snapshot(ticker):
    """Analyze committed SEC fact extracts when live EDGAR access is unavailable."""
    ticker = ticker.upper().strip()
    path = Path(__file__).resolve().parents[2] / "data" / f"{ticker}.json"
    if not path.exists():
        raise ValueError(f"No offline SEC snapshot for {ticker}; set SEC_CONTACT_EMAIL for live EDGAR data.")
    facts = json.loads(path.read_text())
    return analyze_facts(facts, ticker, facts["entityName"])


def printed_results(result):
    lines = [f"{result['company']} ({result['ticker']}) | SEC 10-K | USD millions except ratios"]
    labels = ("revenue", "net_income", "operating_cash_flow", "capital_spending", "stockholders_equity", "liabilities", "research_and_development", "roe", "owner_earnings", "liabilities_equity_ratio")
    for row in result["rows"]:
        lines.append(f"Fiscal year end: {row['fiscal_year_end']}")
        for metric in labels:
            value = row["values"][metric]
            if value is None:
                shown = "not known" if metric == "roe" and row["values"]["stockholders_equity"] is not None and row["values"]["stockholders_equity"] <= 0 else "not found"
            elif metric == "roe":
                shown = f"{value:.1f}%"
            elif metric == "liabilities_equity_ratio":
                shown = f"{value:.2f}x"
            else:
                shown = f"{value / 1_000_000:,.0f}"
            lines.append(f"  {metric}: {shown} | XBRL: {row['tags'][metric]}")
    lines.extend(f"{name}: {result['details'][name]} | {status}" for name, status in result["checks"].items())
    lines.extend(f"{name} verdict: {status}" for name, status in result["verdicts"].items())
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ticker")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = analyze(args.ticker)
    print(json.dumps(result, indent=2) if args.json else printed_results(result))
