"""Simple Streamlit dashboard for SEC 10-K Buffett analysis."""

import importlib.util
from pathlib import Path

import streamlit as st

from memo import generate_memo, unsupported_numbers


ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "warren-buffett-sec" / "scripts" / "sec_analysis.py"
spec = importlib.util.spec_from_file_location("sec_analysis", SCRIPT)
sec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sec)

st.set_page_config(page_title="Buffett SEC Analysis", layout="wide")
st.title("Buffett SEC Analysis")
st.write("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")

ticker = st.text_input("Stock ticker", "COST").strip().upper()
if not ticker:
    st.stop()

try:
    result = sec.analyze(ticker)
except Exception as error:
    st.error(str(error))
    st.stop()

printed = sec.printed_results(result)
st.subheader(f"{result['company']} ({ticker})")
st.caption("USD millions except ROE. Values come from annual 10-K facts; missing values are not estimated.")

chart = []
table = []
labels = {
    "revenue": "Revenue", "net_income": "Net income", "operating_cash_flow": "Operating cash flow",
    "capital_spending": "Capital spending", "stockholders_equity": "Stockholders' equity",
    "roe": "ROE", "owner_earnings": "Owner earnings",
}
for row in result["rows"]:
    values = row["values"]
    chart.append({"Fiscal year end": row["fiscal_year_end"],
                  "Owner earnings": None if values["owner_earnings"] is None else values["owner_earnings"] / 1_000_000,
                  "Net income": None if values["net_income"] is None else values["net_income"] / 1_000_000})
    for key, label in labels.items():
        value = values[key]
        shown = ("not known" if key == "roe" and values["stockholders_equity"] is not None
                 and values["stockholders_equity"] <= 0 else "not found") if value is None else (
                     f"{value:.1f}%" if key == "roe" else f"{value / 1_000_000:,.0f}")
        table.append({"Fiscal year end": row["fiscal_year_end"], "Metric": label,
                      "Value": shown, "XBRL tag / source tags": row["tags"][key]})

st.subheader("Owner earnings and net income")
st.line_chart(chart, x="Fiscal year end", y=["Owner earnings", "Net income"])
st.subheader("Five-year financial metrics")
st.dataframe(table, hide_index=True, width="stretch")
st.subheader("Buffett's three checks")
for name, status in result["checks"].items():
    st.write(f"**{name}: {status}**")

memo_dir = ROOT / "memos"
memo_path = memo_dir / f"{ticker}.md"
st.subheader("AI investment memo")
if st.button("Generate AI memo with Codex"):
    try:
        with st.spinner("Writing memo with Codex..."):
            text = generate_memo(ticker, printed, ROOT)
            memo_dir.mkdir(exist_ok=True)
            memo_path.write_text(text)
            st.session_state[f"memo_{ticker}"] = text
        st.success(f"Saved {memo_path.name}")
    except Exception as error:
        st.error(f"Could not generate memo: {error}")

saved = memo_path.read_text() if memo_path.exists() else ""
memo_text = st.text_area("Memo Markdown (editable for validation)", saved, height=300, key=f"memo_{ticker}")
if st.button("Save memo"):
    memo_dir.mkdir(exist_ok=True)
    memo_path.write_text(memo_text)
    st.success(f"Saved {memo_path.name}")
if memo_text:
    flagged = unsupported_numbers(memo_text, printed)
    if flagged:
        st.error("Unsupported financial number(s) in memo: " + ", ".join(flagged))
    else:
        st.success("Memo validation: every numeric token appears in the Python results.")
    st.markdown(memo_text)
else:
    st.info("Generate a Codex memo for this ticker to display it here.")

with st.expander("Python script output used for memo validation"):
    st.code(printed, language="text")
