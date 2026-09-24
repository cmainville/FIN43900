# Lab 10 — IBM Pro-Forma

## 1. Company and Model Question

Company: International Business Machines Corporation  
Ticker: IBM

**Question:** What are five years of IBM's statements worth, built from assumptions I can defend?

The Python model forecasts FY2026E–FY2030E in USD millions and directly discounts FCFE to common equity. It retains the useful Lab 09 discipline—operations first, linked balance sheet and cash, financing only when needed, annual balance checks, then valuation—but removes retail/floor-plan logic. This is a **screen-grade educational model**, not investment advice.

## 2. IBM-Specific Driver

The driver is **software-led mix and productivity**. IBM reported FY2025 Software revenue of $29.962bn, up 9.1% at constant currency, versus Consulting up 0.4% and Infrastructure up 10.0%. Software is modeled separately and grows faster than the other segments in the forecast; that mix, together with productivity, drives the cash gross-margin and cash-SG&A assumptions.

This affects segment revenue, gross profit, SG&A, EBIT, working capital, cash, FCFE, and value. It is practical because IBM discloses segment revenue but not a full segment cost-of-revenue schedule suitable for a complete segment-margin model.

## 3. Three-Year Historical Financials

All values are **IBM-reported GAAP figures**, USD millions—not data-provider figures. FY2025 10-K comparatives were cross-checked to the FY2024 and FY2023 IBM 10-Ks. No material historical item remains UNRESOLVED.

| Metric | Fiscal year | Value | Filing / source | Location / notes |
| --- | ---: | ---: | --- | --- |
| Revenue | 2023 | 61,860 | IBM FY2025 10-K | Exhibit 13, p. 42 comparative |
| Revenue | 2024 | 62,753 | IBM FY2025 10-K | Exhibit 13, p. 42 comparative |
| Revenue | 2025 | 67,535 | IBM FY2025 10-K | Exhibit 13, p. 42 |
| Gross profit | 2023 | 34,300 | IBM FY2025 10-K | Exhibit 13, p. 42 |
| Gross profit | 2024 | 35,551 | IBM FY2025 10-K | Exhibit 13, p. 42 |
| Gross profit | 2025 | 39,297 | IBM FY2025 10-K | Exhibit 13, p. 42 |
| SG&A | 2023 | 19,003 | IBM FY2025 10-K | Exhibit 13, p. 42 |
| SG&A | 2024 | 19,688 | IBM FY2025 10-K | Exhibit 13, p. 42 |
| SG&A | 2025 | 20,123 | IBM FY2025 10-K | Exhibit 13, p. 42 |
| Net income | 2023 | 7,502 | IBM FY2025 10-K | Exhibit 13, p. 42 |
| Net income | 2024 | 6,023 | IBM FY2025 10-K | Exhibit 13, p. 42 |
| Net income | 2025 | 10,593 | IBM FY2025 10-K | Exhibit 13, p. 42 |
| Inventory | 2023 | 1,161 | IBM FY2023 10-K | Consolidated Balance Sheet; cross-checked to later XBRL |
| Inventory | 2024 | 1,289 | IBM FY2025 10-K | Exhibit 13, p. 44 |
| Inventory | 2025 | 1,220 | IBM FY2025 10-K | Exhibit 13, p. 44 |
| PP&E, net | 2023 | 5,492 | IBM FY2025 10-K | Note L, conventional PP&E excluding finance-lease ROU |
| PP&E, net | 2024 | 5,726 | IBM FY2025 10-K | Note L |
| PP&E, net | 2025 | 5,894 | IBM FY2025 10-K | Note L |
| IBM stockholders' equity | 2023 | 22,533 | IBM FY2023 10-K | Consolidated Balance Sheet |
| IBM stockholders' equity | 2024 | 27,307 | IBM FY2024 10-K | Consolidated Balance Sheet |
| IBM stockholders' equity | 2025 | 32,648 | IBM FY2025 10-K | Exhibit 13, p. 44 |

## 4. Historical Ratios

| Metric | FY2023 | FY2024 | FY2025 | Formula / treatment |
| --- | ---: | ---: | ---: | --- |
| Gross margin | 55.45% | 56.65% | 58.19% | Gross profit / revenue |
| SG&A / gross profit | 55.40% | 55.38% | 51.21% | GAAP SG&A / gross profit |
| Inventory days | 15.38 | 17.29 | 15.76 | Ending inventory / (revenue − gross profit) × 365 |
| Depreciation / average PP&E | 39.06% | 38.65% | 39.31% | Depreciation / average beginning-and-ending PP&E |
| Physical PP&E capital spending | 1,245 | 1,048 | 1,091 | Cash-flow line “Payments for PP&E” |
| Investment in software | 565 | 637 | 647 | Separate cash-flow line “Investment in software” |
| Total modeled capital spending | 1,810 | 1,685 | 1,738 | Physical PP&E capital spending + investment in software |
| Effective tax rate | 13.53% | -3.76% | -2.34% | Tax expense/(benefit) / pretax income; negative rates are not extrapolated |
| Reported revenue growth | 2.20% | 1.44% | 7.62% | (Current revenue / prior revenue) − 1; FY2022 revenue was $60.530bn |
| IBM constant-currency revenue growth | 3% | 3% | 6% | IBM-reported underlying growth measure |

FY2025 constant-currency segment growth was Software 9.1%, Consulting 0.4%, and Infrastructure 10.0%. Constant-currency and segment growth are more useful than a retail-style same-store-sales concept because they isolate operating momentum from FX and identify IBM’s mix shift.

## 5. Opening Balance-Sheet Mapping

| Model variable | IBM filing account(s) | Amount | Mapping rationale |
| --- | --- | ---: | --- |
| Cash | Cash and cash equivalents | 13,587 | FY2025 balance sheet |
| Trade AR | Notes and accounts receivable—trade | 8,112 | Working-capital receivable |
| Financing AR | Short-term financing receivables plus long-term financing receivables | 16,183 | Separate from trade AR because it is IBM Financing-cycle dependent |
| Other AR | Other accounts receivable | 1,052 | Separate operating asset |
| Inventory | Inventory | 1,220 | Direct mapping |
| PP&E | Note L PP&E, net | 5,894 | Excludes immaterial finance-lease ROU component |
| Finite-lived intangibles | Intangible assets—net | 11,391 | Separate amortizable asset class |
| Other assets | Residual reported assets after mapped accounts | 94,441 | Includes goodwill, pension assets, deferred taxes, leases, deferred costs, investments; held static absent a specific forecast |
| Accounts payable | Accounts payable | 4,756 | Direct mapping |
| Deferred revenue | Current and noncurrent deferred income | 20,372 | Contracted/recurring-revenue cash-flow liability |
| Financing debt | IBM Financing debt | 15,093 | Funding tied to Financing receivables |
| Corporate debt | Total debt less Financing debt | 46,167 | Corporate borrowing schedule |
| Other liabilities | Residual reported liabilities | 32,752 | Includes $1m rounding reconciliation so opening balance sheet exactly balances |
| Equity | IBM stockholders’ equity plus NCI | 32,740 | Model uses total reported equity for accounting identity |

Opening assets equal opening liabilities plus equity. The $1m difference is a disclosed rounding reconciliation, not a cash or equity plug.

## 6. Forecast Assumptions

Every variable used as an input in `lab10_proforma_IBM.py` is documented below. “Guidance” means an authoritative future company disclosure; “History” means a filed result or directly calculated filed ratio; all remaining forward views are “Judgment.”

| Assumption | Value | Label | Reason |
| --- | ---: | --- | --- |
| FY2025 segment revenue base | Software 29,962; Consulting 21,055; Infrastructure 15,718; Financing 737; Other 63 | History | IBM FY2025 segment disclosure; forecast base. |
| FY2026 segment growth | Software 8%; Consulting 2%; Infrastructure -1%; Financing 5%; Other 0% | Judgment | Consistent in aggregate with IBM’s 4–5% FY2026 constant-currency guidance and Q2 segment trends, but individual segment rates are analyst choices. |
| FY2027–30 segment growth | Software 7%→5%; Consulting 3%→3%; Infrastructure 2%→2%; Financing 3%→2%; Other 0% | Judgment | Growth fades as the software mix remains more favorable than Consulting and Infrastructure. |
| Cash gross margin | 60.5%→61.5% | Judgment | Software mix and productivity can improve cash economics; IBM did not issue multi-year GAAP gross-margin guidance. |
| Cash SG&A / revenue | 27.9%→27.5% | Judgment | Calibrated from FY2025 SG&A less acquired-intangible amortization, with modest productivity leverage. |
| R&D / revenue | 12.2% | History | FY2025 R&D / FY2025 revenue, rounded. |
| Tax rate | 16.0% | Judgment | Normalizes FY2024–25 discrete tax benefits instead of capitalizing negative tax rates. |
| Software amortization | 490; 333; 141; 0; 0 | Guidance | FY2025 10-K Note N schedule for existing capitalized software. |
| Acquired-intangible amortization | 2,283; 2,245; 1,939; 1,254; 812 | Guidance | FY2025 10-K Note N schedule for existing acquired intangibles. |
| FY2026 acquisition cash | 10,480 | History | Q2 2026 10-Q first-half cash acquisition of Confluent. |
| FY2026 acquired intangibles | 2,564 | History | Q2 2026 increase in reported net intangibles; attributed to Confluent in the filing. |
| Physical PP&E capex / revenue | 1.7% | History | FY2025 PP&E capital spending / revenue, rounded. |
| Software investment / revenue | 1.0% | History | FY2025 investment in software / revenue, rounded. |
| Depreciation / beginning PP&E | 39.0% | History | FY2025 depreciation / average PP&E, rounded and applied to beginning PP&E. |
| Trade AR / revenue | 12.0% | Judgment | Near FY2025 trade AR / revenue; separated from IBM Financing receivables. |
| Other AR / revenue | 1.6% | Judgment | Near FY2025 other AR / revenue. |
| Inventory days | 15.76 days | History | FY2025 inventory / COGS × 365. |
| AP / COGS | 16.84% | History | FY2025 AP / COGS. |
| Deferred revenue / revenue | 30.16% | History | FY2025 current plus noncurrent deferred income / revenue. |
| Financing receivables | 14,000→16,000 | Judgment | Q2 2026 balance was $13.782bn, down from $16.183bn; forecast separately rather than as a revenue percentage. |
| Financing debt / Financing receivables | 93.3% | History | FY2025 Financing debt / Financing receivables; preserves matched funding. |
| Corporate debt | 49,000→46,500 | Judgment | FY2026 starts near Q2 2026 corporate debt of $48.940bn and declines gradually. |
| Interest rate | 3.3% | Judgment | FY2025 interest-paid/average-debt proxy; must be revisited for refinancings. |
| Dividends | 6,350 annually | Judgment | $1.69 quarterly dividend × roughly 940m shares, rounded. |
| Minimum cash | 5,000 | Judgment | Conservative global-operating liquidity floor; no IBM policy was identified. |
| Revolver limit / rate | 10,000 / 5.5% | Judgment | Emergency model backstop only, not represented as an identified IBM facility. |
| Cost of equity | 9.0% | Judgment | Classroom FCFE discount-rate assumption; high valuation sensitivity. |
| Terminal growth | 2.5% | Judgment | Below nominal long-run economy-like growth. |
| Diluted shares | 952.697m | History | IBM's latest filed diluted weighted-average shares: six months ended June 30, 2026. This is the appropriate diluted EPS denominator; the 942.134m June 30 point-in-time figure is basic shares outstanding and is not used. |

## 7. Five-Year Forecast

| USD millions | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
| --- | ---: | ---: | ---: | ---: | ---: |
| Revenue | 70,232.7 | 73,476.6 | 76,748.9 | 79,996.1 | 82,993.3 |
| Gross profit | 42,000.8 | 44,340.8 | 46,752.6 | 49,037.6 | 51,040.9 |
| SG&A | 21,877.9 | 22,671.5 | 23,198.5 | 23,332.9 | 23,635.2 |
| R&D | 8,568.4 | 8,964.1 | 9,363.4 | 9,759.5 | 10,125.2 |
| EBIT | 11,554.5 | 12,705.1 | 14,190.8 | 15,945.2 | 17,280.5 |
| Net income | 8,007.6 | 8,952.1 | 10,214.8 | 11,689.4 | 12,812.1 |
| Cash | 11,341.8 | 16,022.6 | 21,637.7 | 27,696.8 | 34,263.2 |
| Trade receivables | 8,427.9 | 8,817.2 | 9,209.9 | 9,599.5 | 9,959.2 |
| Financing receivables | 14,000.0 | 14,500.0 | 15,000.0 | 15,500.0 | 16,000.0 |
| PP&E | 4,789.3 | 4,170.6 | 3,848.8 | 3,707.7 | 3,672.6 |
| Finite-lived intangibles | 11,884.3 | 10,041.1 | 8,728.6 | 8,274.5 | 8,292.5 |
| Financing debt | 13,057.0 | 13,523.4 | 13,989.7 | 14,456.0 | 14,922.3 |
| Corporate debt | 49,000.0 | 48,000.0 | 47,500.0 | 47,000.0 | 46,500.0 |
| Equity | 34,397.6 | 36,999.7 | 40,864.5 | 46,204.0 | 52,666.1 |
| FCFE | 4,104.8 | 11,030.7 | 11,965.1 | 12,409.1 | 12,916.4 |

FCFE = net income + depreciation + intangible amortization − PP&E capex − capitalized-software investment − acquisition cash − changes in trade/Financing/other receivables and inventory + changes in payables and deferred revenue + net debt financing.

## 8. Model Checks

| Check, USD millions | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
| --- | ---: | ---: | ---: | ---: | ---: |
| Assets − liabilities − equity | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Ending cash | 11,341.8 | 16,022.6 | 21,637.7 | 27,696.8 | 34,263.2 |
| Required minimum cash | 5,000.0 | 5,000.0 | 5,000.0 | 5,000.0 | 5,000.0 |
| Revolver | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

Cash is produced by FCFE, dividends, and financing mechanics; it is not manually typed. The code deliberately reduces FY2026 cash by $1m in a copied model and confirms that the balance-check function rejects it. No revolver is used in the base case.

## 9. Valuation

| Valuation item | Value |
| --- | ---: |
| PV FY2026E–FY2030E FCFE | $39,475.2m |
| FY2031 terminal FCFE | $13,239.3m |
| Terminal value | $203,681.5m |
| PV terminal value | $132,379.1m |
| Implied equity value | $171,854.3m |
| Latest filed diluted weighted-average shares | 952.697m |
| **Implied value per share** | **$180.39** |

The value is directly an equity value because FCFE is after interest and net debt financing. Units are consistent: equity value and shares are both in millions.

## 10. Market Price Comparison

The model indicates approximately **$180.39 per share**, compared with IBM's market price of approximately **$227.66 as of September 24, 2026 at 2:48 PM Eastern**.

Neutral analytical question: **Does the market price assume more durable software-led margin expansion and cash conversion than the model’s 60.5%→61.5% cash-gross-margin path?**

## 11. Partner Questions and Responses

The following are two **hypothetical partner-review questions** and the modeler’s responses; they are not attributed to an actual classmate.

| Partner question | Response |
| --- | --- |
| “How does the model avoid treating the Confluent acquisition as an ordinary operating expense or ignoring its effect on FCFE?” | FY2026 FCFE includes the $10.480bn acquisition cash use reported in IBM’s Q2 2026 10-Q. The model separately adds the reported $2.564bn increase in acquired intangibles; the remaining consideration is included in other assets (principally goodwill and other acquired assets). No future acquisitions are assumed. |
| “What supports gross-margin and SG&A improvement when IBM has not issued a multi-year GAAP margin target?” | The 60.5%→61.5% cash-gross-margin and 27.9%→27.5% cash-SG&A paths are explicitly **Judgment**, not guidance. They reflect software-led mix and productivity, but the model should be stress-tested because PV of terminal value is about 77% of equity value. |

## 12. Sources

- [IBM FY2025 Form 10-K / Annual Report](https://www.sec.gov/Archives/edgar/data/51143/000005114326000010/ibm-20251231_d2.htm): historical GAAP statements, segment revenue, debt, and Note N amortization schedule.
- [IBM FY2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/51143/000005114325000015/ibm-20241231.htm): FY2024 historical cross-check.
- [IBM FY2023 Form 10-K](https://www.sec.gov/Archives/edgar/data/51143/000005114324000012/ibm-20231231.htm): FY2023 balance-sheet cross-check.
- [IBM Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/51143/000005114326000078/ibm-20260630.htm): current balance sheet, Confluent cash use, debt, segment performance, and 952.697m diluted weighted-average shares for the six months ended June 30, 2026 (Note 7).
- [IBM Q2 2026 earnings release](https://newsroom.ibm.com/2026-07-22-IBM-RELEASES-SECOND-QUARTER-RESULTS): FY2026 4–5% constant-currency revenue-growth guidance and about $1bn free-cash-flow growth guidance.
- [IBM intraday market quote](https://stockanalysis.com/stocks/ibm/): $227.66 at September 24, 2026, 2:48 PM Eastern.
- Course files reviewed: `proforma.py` and `lab09.md`; no ABG financial inputs, floor-plan assumptions, or retail drivers remain in the IBM model.
