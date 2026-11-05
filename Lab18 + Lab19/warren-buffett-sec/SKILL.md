---
name: warren-buffett-sec
description: Analyze a stock ticker in Warren Buffett's style using five years of SEC 10-K financial facts. Use when asked for a Buffett analysis or Buffett investment memo for a ticker.
---

# Warren Buffett SEC analysis

Run `scripts/sec_analysis.py TICKER` to retrieve the latest five fiscal years from SEC EDGAR. Set `SEC_CONTACT_EMAIL` to the user's own email first. The shared Lab 19 script prints every financial figure, its XBRL source tags, all seven panel checks, and the three investor verdicts. Buffett's original three checks and owner-earnings definition remain unchanged. Treat printed results as the sole source of financial numbers. Never infer, estimate, or replace missing values.

Write a short Markdown memo headed `Recommendation: Own`, `Watch`, or `Pass`. Speak in Buffett's first-person investment voice as a clearly labeled simulation. Discuss the understandable business, possible durable competitive advantage, profitability, cash generation, consistency, and what the printed figures cannot establish. Distinguish evidence from qualitative judgment. Acknowledge missing data explicitly. Do not discuss share price, valuation, intrinsic value, or margin of safety because this lab does not supply price data. Save the memo as `memos/TICKER.md` beside the project app, with a final `My trust in this verdict: ____ because ____` line for the student.

The philosophy is adapted from [the Buffett expert page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md): favor businesses one understands, durable moats, consistently strong returns, cash that owners could receive, and prudent management. Do not use FAskills or its data sources. For this lab, owner earnings means operating cash flow minus all capital spending, a simplified proxy. Do not claim the analysis verifies a moat or management quality from numbers alone.
