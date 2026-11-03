"""Five-year SEC 10-K financial analysis for the Buffett skill and dashboard."""

import argparse
import json
import os
import re
import ssl
from datetime import date
from urllib.request import Request, urlopen

import certifi


TAGS = {
    "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"),
    "net_income": ("NetIncomeLoss",),
    "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",),
    "capital_spending": ("PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"),
    "stockholders_equity": ("StockholdersEquity",),
}
MONEY = ("revenue", "net_income", "operating_cash_flow", "capital_spending", "stockholders_equity", "owner_earnings")


def fetch_json(url):
    email = os.environ.get("SEC_CONTACT_EMAIL", "").strip()
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        raise ValueError("Set SEC_CONTACT_EMAIL to your email address before contacting SEC EDGAR.")
    request = Request(url, headers={"User-Agent": f"FIN439 Lab 18 {email}", "Accept-Encoding": "identity"})
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


def analyze_facts(facts, ticker, company):
    gaap = facts.get("facts", {}).get("us-gaap", {})
    ends = set()
    for tags in TAGS.values():
        for tag in tags:
            for fact in gaap.get(tag, {}).get("units", {}).get("USD", []):
                if annual_fact(fact):
                    ends.add(fact["end"])
    years = sorted(ends, reverse=True)[:5]
    rows = []
    for end in reversed(years):
        row = {"fiscal_year_end": end, "values": {}, "tags": {}}
        for metric, tags in TAGS.items():
            value, tag = pick(facts, tags, end, metric != "stockholders_equity")
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
        rows.append(row)
    roes = [r["values"]["roe"] for r in rows]
    earnings = [r["values"]["owner_earnings"] for r in rows]
    checks = {
        "ROE >= 15% in all five years": check(roes, lambda v: all(x >= 15 for x in v)),
        "Positive owner earnings in all five years": check(earnings, lambda v: all(x > 0 for x in v)),
        "Owner earnings increased first to last": check(earnings, lambda v: v[-1] > v[0]),
    }
    return {"ticker": ticker.upper(), "company": company, "cik": facts.get("cik"), "rows": rows, "checks": checks}


def analyze(ticker):
    cik, company = cik_for_ticker(ticker)
    facts = fetch_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json")
    return analyze_facts(facts, ticker, company)


def printed_results(result):
    lines = [f"{result['company']} ({result['ticker']}) | SEC 10-K | USD millions except ROE"]
    labels = ("revenue", "net_income", "operating_cash_flow", "capital_spending", "stockholders_equity", "roe", "owner_earnings")
    for row in result["rows"]:
        lines.append(f"Fiscal year end: {row['fiscal_year_end']}")
        for metric in labels:
            value = row["values"][metric]
            if value is None:
                shown = "not known" if metric == "roe" and row["values"]["stockholders_equity"] is not None and row["values"]["stockholders_equity"] <= 0 else "not found"
            elif metric == "roe":
                shown = f"{value:.1f}%"
            else:
                shown = f"{value / 1_000_000:,.0f}"
            lines.append(f"  {metric}: {shown} | XBRL: {row['tags'][metric]}")
    lines.extend(f"{name}: {status}" for name, status in result["checks"].items())
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ticker")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = analyze(args.ticker)
    print(json.dumps(result, indent=2) if args.json else printed_results(result))
