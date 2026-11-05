"""Three-investor panel over the Lab 18 SEC financial analysis."""

import importlib.util
import os
from pathlib import Path

import streamlit as st

from memo import generate_memo, panel_memo, unsupported_numbers

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "warren-buffett-sec" / "scripts" / "sec_analysis.py"
spec = importlib.util.spec_from_file_location("sec_analysis", SCRIPT)
sec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sec)

st.set_page_config(page_title="Three-Investor SEC Panel", layout="wide")
st.title("Three-Investor SEC Panel")
st.write("SEC EDGAR 10-K facts. Python calculates every check; the memos are investor-style simulations, not investment advice.")
st.caption("VTI's largest underlying holding: NVIDIA (NVDA), September 30, 2026, per [Vanguard's official holdings feed](https://advisors.vanguard.com/investments/products/api/funds/0970/holdings/latest).")

ticker = st.text_input("Stock ticker", "COST").strip().upper()
if not ticker:
    st.stop()
try:
    offline = not os.environ.get("SEC_CONTACT_EMAIL")
    result = sec.analyze_snapshot(ticker) if offline else sec.analyze(ticker)
except Exception as error:
    st.error(str(error))
    st.stop()

printed = sec.printed_results(result)
if offline:
    st.info("Using the committed SEC company-facts extract dated November 5, 2026. Set SEC_CONTACT_EMAIL for live EDGAR data and other tickers.")
st.subheader(f"{result['company']} ({ticker})")
st.caption("USD millions except ratios. Annual 10-K facts only; missing values are not estimated or replaced with zero.")

chart, table = [], []
labels = {
    "revenue": "Revenue", "net_income": "Net income", "operating_cash_flow": "Operating cash flow",
    "capital_spending": "Capital spending", "stockholders_equity": "Stockholders' equity",
    "liabilities": "Total liabilities", "research_and_development": "R&D expense",
    "roe": "ROE", "owner_earnings": "Owner earnings", "liabilities_equity_ratio": "Liabilities / equity",
}
for row in result["rows"]:
    values = row["values"]
    chart.append({"Fiscal year end": row["fiscal_year_end"],
                  "Owner earnings": None if values["owner_earnings"] is None else values["owner_earnings"] / 1_000_000,
                  "Net income": None if values["net_income"] is None else values["net_income"] / 1_000_000})
    for key, label in labels.items():
        value = values[key]
        shown = "not found" if value is None else f"{value:.1f}%" if key == "roe" else f"{value:.2f}x" if key == "liabilities_equity_ratio" else f"{value / 1_000_000:,.0f}"
        table.append({"Fiscal year end": row["fiscal_year_end"], "Metric": label,
                      "Value": shown, "XBRL tag / source tags": row["tags"][key]})

st.subheader("Owner earnings and net income")
st.line_chart(chart, x="Fiscal year end", y=["Owner earnings", "Net income"])
st.subheader("Five-year financial metrics")
st.dataframe(table, hide_index=True, width="stretch")

st.subheader("Seven investor checks")
check_rows = [{"Investor": investor, "Check": name, "Calculated value": result["details"][name], "Result": result["checks"][name].upper()}
              for investor, names in sec.INVESTOR_CHECKS.items() for name in names]
st.dataframe(check_rows, hide_index=True, width="stretch")
st.write("Individual verdicts: " + " · ".join(f"**{name}: {status.upper()}**" for name, status in result["verdicts"].items()))

st.subheader("Investment memos")
memo_dir = ROOT / "memos"
columns = st.columns(3)
for column, investor in zip(columns, sec.INVESTOR_CHECKS):
    slug = investor.lower().replace(" ", "-")
    memo_path = memo_dir / f"{ticker}-{slug}.md"
    with column:
        if st.button(f"Generate AI memo: {investor}", key=f"generate_{slug}"):
            try:
                with st.spinner("Writing memo with Codex..."):
                    text = generate_memo(ticker, printed, ROOT, investor)
                    memo_dir.mkdir(exist_ok=True)
                    memo_path.write_text(text)
                    st.session_state[f"memo_{ticker}_{slug}"] = text
            except Exception as error:
                st.error(f"Could not generate memo: {error}")
        if investor == "Warren Buffett" and not memo_path.exists():
            memo_path = memo_dir / f"{ticker}.md"
        saved = memo_path.read_text() if memo_path.exists() else panel_memo(result, investor)
        memo_text = st.text_area(f"{investor} memo Markdown (editable)", saved, height=220, key=f"memo_{ticker}_{slug}")
        if st.button(f"Save {investor} memo", key=f"save_{slug}"):
            target = memo_dir / f"{ticker}-{slug}.md"
            memo_dir.mkdir(exist_ok=True)
            target.write_text(memo_text)
            st.success(f"Saved {target.name}")
        flagged = unsupported_numbers(memo_text, printed)
        if flagged:
            st.error("Unsupported financial number(s): " + ", ".join(flagged))
        else:
            st.success("Numerical-claim flag: clear; every numeric token appears in Python output.")
        st.markdown(memo_text)
        if investor == "Cathie Wood" and ticker == "COST":
            experiment, _ = sec.cathie_checks(result["rows"], growth_threshold=0.05)
            st.caption(f"Threshold experiment: at 5%, growth is {experiment['Revenue CAGR >= 15%'].upper()} and R&D is {experiment['Latest R&D / revenue >= 5%'].upper()}; the default 15% threshold remains in use.")

with st.expander("Python script output used for memo validation"):
    st.code(printed, language="text")
