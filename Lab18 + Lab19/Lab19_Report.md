# Lab 19 — Three-Investor Panel

## Costco validation

The panel used [Costco's SEC 10-K company facts](https://data.sec.gov/api/xbrl/companyfacts/CIK0000909832.json) for fiscal years ending in 2022–2026. Buffett passed all three checks: ROE was at least 15% each year, owner earnings were positive each year, and owner earnings rose from $3,501 million to $9,382 million. Wood's revenue CAGR was **7.51%**, so her growth check **failed** the 15% threshold; R&D/revenue was **not known** because the R&D fact was not found. Burry passed both checks: operating cash flow exceeded net income each year, and latest liabilities/equity was **1.49x**. The liabilities/equity ratios by year were **2.11x, 1.75x, 1.96x, 1.64x, and 1.49x**.

**Threshold experiment:** Changing only Wood's growth threshold to 5% changed Costco's growth result from FAIL to PASS; R&D stayed NOT KNOWN. The default 15% threshold was restored. The CAGR itself did not change, only the comparison threshold.

## Project 2 company: NVIDIA

[Vanguard's official VTI holdings feed](https://advisors.vanguard.com/investments/products/api/funds/0970/holdings/latest), dated **September 30, 2026**, lists **NVIDIA Corp. (NVDA)** first at 7.13% of the fund. NVIDIA has usable EDGAR 10-K company facts, so no substitution was needed. The panel uses its five fiscal years ending January 2022–January 2026, sourced from [SEC company facts](https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json).

| Investor | Check | Calculated value | Result |
| --- | --- | --- | --- |
| Buffett | ROE ≥ 15% each year | 36.6%, 19.8%, 69.2%, 91.9%, 76.3% | PASS |
| Buffett | Owner earnings positive each year | 8,132; 3,808; 27,021; 60,853; 96,676 USD millions | PASS |
| Buffett | Owner earnings grew first to last | 8,132 to 96,676 USD millions | PASS |
| Wood | Revenue CAGR ≥ 15% | 68.30% | PASS |
| Wood | Latest R&D/revenue ≥ 5% | 8.57% | PASS |
| Burry | Operating cash flow ≥ net income each year | no, yes, no, no, no | FAIL |
| Burry | Latest liabilities/equity ≤ 2 | 0.31x | PASS |

**Individual verdicts:** Buffett **PASS**; Wood **PASS**; Burry **FAIL**. Buffett and Wood agree that their chosen financial screens pass. Burry disagrees because the annual cash conversion test fails, although the latest balance-sheet ratio passes. A pass is a screen result, not a buy recommendation or a valuation judgment.

**Bull case:** NVIDIA's owner earnings were positive in every year and increased from $8,132 million to $96,676 million. Revenue CAGR of 68.30% and latest R&D/revenue of 8.57% support Wood's growth and reinvestment screen.

**Bear case:** Operating cash flow was below net income in four of the five years, failing Burry's cash-quality screen. The financial panel cannot establish whether that gap is temporary or what the shares are worth.

**Decision:** Only with a condition: use the panel to shortlist Project 2 companies, then review filing footnotes and valuation before an investment decision.

## How the panel works

A panel of AI agents applies different investor viewpoints to the same evidence. Here, Python retrieves 10-K facts, calculates each check, and fixes the verdict; three persona memos interpret those results. They can disagree because Buffett emphasizes return on equity and owner earnings, Wood emphasizes growth and R&D, and Burry emphasizes cash conversion and liabilities. The personas do not change the numbers.

Wood's Python function reads five revenue values and the latest R&D expense and revenue. If all needed values exist and starting revenue is positive, it computes `(last / first) ** (1 / 4) - 1` and compares it with 15%; if latest R&D and revenue exist, it divides R&D by revenue and compares with 5%. A missing input returns **NOT KNOWN**, never zero or an estimate. Her overall verdict is FAIL if a known check fails, otherwise NOT KNOWN if any check is unknown, otherwise PASS.

The app displays every check and its source-linked metric, lets the student edit or generate investor memos, and flags numeric tokens absent from Python's printed output. It also retains the Lab 18 owner-earnings chart, financial table, and Buffett memo workflow. The committed SEC extracts in `data/` permit offline reproduction for COST and NVDA as of November 5, 2026; setting `SEC_CONTACT_EMAIL` uses live EDGAR for any ticker. Source data can be revised by later filings.
