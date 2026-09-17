# Lab 08 — Deal Evidence and Valuation Triangulation

## Target Company and Valuation Date

The target is International Business Machines Corporation (NYSE: IBM). This lab uses **September 9, 2026** as the valuation and comparison-price date because it is the valuation date in the existing Week 3 IBM DCF. All three stock prices below are NYSE closing prices on that same date and are in U.S. dollars.

## How IBM Makes Money

IBM's strategy is software-led hybrid cloud and AI, executed through Software, Consulting, Infrastructure, and Financing. In FY2025, IBM reported $67.5 billion of revenue; Software revenue grew 10.6%, Consulting grew 1.8%, and Infrastructure grew 12.1%. Its economics therefore combine recurring software, enterprise implementation and managed-services work, cyclical infrastructure product demand, and client financing. Peer selection should not treat IBM as a pure software company or as a pure consulting company. [S1]

## Initial Peer Selection Policy

**INITIAL POLICY — written before the final peer decisions:** A peer should be a listed operating company with meaningful enterprise-customer exposure and a positive, annual, reported diluted EPS. It should have a material share of software, contracted/recurring services, enterprise infrastructure, or a combination of those activities. Its business should be mature enough that annual GAAP P/E is informative, even if the peer has a different mix.

I will qualify rather than automatically exclude a candidate when it has only one major portion of IBM's model, such as enterprise software/infrastructure or enterprise consulting/managed services. I will exclude a candidate if it is principally consumer technology, hardware without a meaningful enterprise software/services relationship, has negative or unusually distorted reported EPS, or has a growth and earnings profile so different that P/E is not a useful reference.

## Independent AI Candidate Check

I independently used both ChatGPT and Gemini with the same IBM target, September 9, 2026 valuation date, and initial peer-selection policy to generate peer ideas. I used both tools only as independent research aids, did not treat their suggestions as final evidence, and verified the final Oracle and Accenture decisions using the primary sources cited later in this report.

## Peer Candidates and Evidence

**Oracle Corporation (NYSE: ORCL).** Oracle's FY2026 10-K describes Cloud and Software, Services, and Hardware businesses. The Cloud and Software business includes cloud services and license support, while its Hardware business includes engineered systems. That makes Oracle a reasonable enterprise-software and infrastructure reference for IBM. The important difference is that Oracle's cloud-infrastructure investment and growth profile are more prominent, while IBM has a much larger consulting component and an IBM Financing business. Oracle reported FY2026 GAAP diluted EPS of $5.83. [S2]

**Accenture plc (NYSE: ACN).** Accenture reported FY2025 revenue split between Consulting ($35.1 billion) and Managed Services ($34.6 billion). Its 10-K explains that managed services are ongoing, repeatable services and are typically multi-year contracts. This makes it a reasonable reference for IBM Consulting and for enterprise-client, contracted-service economics. The important difference is that Accenture does not have IBM's meaningful software, infrastructure-product, or financing mix. Accenture reported FY2025 GAAP diluted EPS of $12.15. [S3]

## Peer Decision Table

| Candidate | Business-model evidence and locator | Similarity to IBM | Important difference / comparability problem | Decision | Reason |
|---|---|---|---|---|---|
| Oracle (ORCL) | FY2026 Form 10-K, Item 1 — Business; Cloud and Software, Services, and Hardware businesses | Enterprise customers; software, cloud, support, and infrastructure economics | More cloud-infrastructure-growth exposure and materially less consulting; its P/E may reflect a faster-growth mix | **QUALIFY** | Relevant enterprise software/infrastructure comparator, but not a full IBM model match |
| Accenture (ACN) | FY2025 Form 10-K, Item 7, “Type of Work” and “New Bookings”; consulting and managed-services revenue; managed-services contracts typically span several years | Enterprise clients, consulting, technology integration, and recurring contracted managed services | Lacks IBM's software, infrastructure-product, and financing businesses | **QUALIFY** | Relevant services comparator, but its service-heavy mix limits direct P/E comparability |

No candidate is excluded. Both qualified peers remain in the valuation so the result displays the range created by IBM's mixed business model rather than disguising that uncertainty.

## Valuation Inputs

| Company | Ticker | Sept. 9, 2026 close | Annual reported diluted EPS | Fiscal year-end | EPS publication/filing date | EPS source and locator | Price source |
|---|---:|---:|---:|---|---|---|---|
| International Business Machines | IBM | $239.94 | $11.17 | Dec. 31, 2025 | Feb. 24, 2026 | 2025 Form 10-K / Annual Report, Financial Performance Summary: “Consolidated earnings per share—assuming dilution” | IBM Historical Stock Lookup, Sept. 9, 2026 [S4] |
| Oracle | ORCL | $161.63 | $5.83 | May 31, 2026 | June 22, 2026 | FY2026 Form 10-K, Consolidated Statements of Operations: “Earnings per share attributable to common shareholders—Diluted” | StockAnalysis historical price table, Sept. 9, 2026 [S5] |
| Accenture | ACN | $175.80 | $12.15 | Aug. 31, 2025 | Oct. 10, 2025 | FY2025 Form 10-K, Note 3 — Earnings Per Share, p. F-20 | StockAnalysis historical price table, Sept. 9, 2026 [S6] |

Checks: all prices are closes on September 9, 2026; all amounts are USD per common share; and all EPS figures are annual, reported GAAP diluted EPS that were public before the valuation date. IBM's $11.17 is consolidated reported diluted EPS, not the $11.14 continuing-operations EPS and not the $11.59 operating (non-GAAP) EPS. [S1]

## Peer P/E Valuation

The calculator preserves the Lab 07 approach: peer P/E equals price divided by annual reported diluted EPS, and that multiple is applied to IBM's annual reported diluted EPS. QUALIFY peers are admitted; EXCLUDE peers would remain visible in the program but would not affect the calculation.

Calculator output from `python3 -B lab08_ibm_comps.py`:

```text
P/E Comparable-Company Valuation: International Business Machines (IBM)
Target closing price: $239.94
Target diluted EPS: $11.17

Peer P/E multiples
ORCL (qualify): 27.723842x; IBM implied price $309.68
ACN (qualify): 14.469136x; IBM implied price $161.62

Implied target prices
Minimum peer P/E: 14.469136x
Minimum implied price: $161.62
Median peer P/E: 21.096489x
Median implied price: $235.65
Maximum peer P/E: 27.723842x
Maximum implied price: $309.68

Leave-one-peer-out test
Remove ORCL: remaining median-implied price $161.62; change -$74.03
Remove ACN: remaining median-implied price $309.68; change +$74.03
```

The defendable P/E output is a **qualified peer reference range of $161.62 to $309.68 per IBM share**, with a two-peer median reference of **$235.65**. It is not a precise target price because each peer represents a different part of IBM's model.

## Manual Validation

I manually checked Accenture, an admitted peer:

`P/E = $175.80 / $12.15 = 14.469136x`

The calculator reports 14.469136x for ACN, so the hand calculation matches, subject only to displayed rounding. Applying that P/E to IBM's $11.17 reported diluted EPS gives `$161.620247`, or **$161.62** after rounding.

## Changed-Peer Validation

**Prediction before recalculation:** Oracle has the higher P/E and the higher IBM implied value. Removing Oracle should lower the two-peer median reference to Accenture's single-peer implied value.

The normal two-peer median is $235.65. Removing ORCL leaves ACN alone and produces a $161.62 single-peer reference, a **$74.03 decrease**. Oracle has the higher 27.723842x P/E, and IBM's implied value is calculated by applying each peer P/E to IBM's $11.17 EPS. Removing Oracle therefore eliminates the higher implied value and leaves Accenture's lower 14.469136x P/E as the reference. This does not justify excluding Oracle; it shows the valuation is sensitive to peer selection. The normal calculator file restores both qualified peers.

## Week 3 DCF Comparison

| Method | IBM result and date | Main assumption or limitation |
|---|---|---|
| Week 3 DCF | **$270.45 per diluted share**, September 9, 2026 | Forecast growth, margins, WACC, terminal growth, and enterprise-to-equity bridge; several documented inputs are placeholders |
| Peer P/E | **$161.62–$309.68 qualified range; $235.65 two-peer median**, September 9, 2026 | Peer choice and comparability of annual reported earnings |

The Week 3 DCF is above the two-peer P/E median but inside the broad qualified-peer range. The methods are therefore directionally compatible only at a high level, not tightly convergent. The DCF can capture IBM-specific cash-flow forecasts, its capital structure, Financing debt treatment, and a long-run terminal value. P/E captures how the market valued two different enterprise-technology business models on the same date, including market sentiment and peer-specific growth expectations that the DCF may not reflect.

The most important uncertainties are the DCF's placeholder cost of debt, tax rate, margins, D&A, capex, working capital, and terminal-growth inputs, plus the wide difference between Oracle's growth-oriented software/infrastructure P/E and Accenture's services-oriented P/E. The results are deliberately not averaged.

## AI Skeptical Review

The weakest-supported assumption is that two qualified peers can bracket IBM's blended software, consulting, infrastructure, and financing economics. Oracle is more cloud-infrastructure-growth oriented, while Accenture is predominantly services oriented; neither is a full business-model match. There is no price-date mismatch: all closes are September 9, 2026. There is no identified earnings-definition mismatch: the calculation uses annual reported diluted EPS throughout. The main valuation-object mismatch is that IBM's P/E includes consolidated earnings, while the peer businesses omit or emphasize different components of IBM's mix.

One material risk is that IBM's FY2025 reported EPS includes a tax-audit benefit. That benefit can make a trailing reported P/E look lower and implied values look higher than a normalized earnings comparison would indicate. [S1]

**Question that could change the conclusion:** If IBM's FY2025 tax-audit benefit is removed using a source-supported normalization, does IBM's normalized P/E remain attractive relative to Oracle and Accenture?

## Judgment of AI Criticism

**UNRESOLVED.** The criticism about business-model mismatch is supported by the peer evidence: IBM has four operating segments, Oracle emphasizes cloud/software and hardware, and Accenture is consulting and managed services. The tax-audit-benefit concern is also supported by IBM's FY2025 annual-report disclosure. However, the repository and the gathered sources do not provide a comparable, source-supported normalized IBM EPS calculation. I therefore cannot determine whether the conclusion remains attractive after normalization without inventing an adjustment.

## Final Investment Conclusion

Oracle and Accenture are admitted as **QUALIFY** peers because they each match an economically relevant part of IBM—Oracle for enterprise software/infrastructure and Accenture for enterprise consulting/managed services—but neither matches IBM's full mix. The P/E comparison contributes a market-based reference that the Week 3 DCF does not provide. Its $161.62–$309.68 span is wide, which is itself evidence that IBM's mix makes a simple P/E conclusion fragile.

The saved Week 3 DCF is $270.45 per share, above the $235.65 P/E median but within the qualified-peer range. That difference is reasonable because the DCF embeds IBM-specific cash-flow, capital-structure, and terminal assumptions, while the peer multiples reflect different growth and mix profiles. Neither result should be averaged with the other.

The provisional action is **WATCH-DEFER**. A defensible conclusion is that IBM is not clearly overvalued on this evidence, but the sources do not support a confident initiation: the DCF contains documented placeholder inputs, the peer range is wide, and FY2025 reported EPS includes a disclosed tax benefit. The skeptical question cannot yet be answered; evidence that could change the conclusion is a source-supported normalized IBM EPS, support for the DCF placeholders, and evidence that IBM's software growth, consulting demand, infrastructure cycle, and free-cash-flow conversion can support the applicable peer multiple.

## Sources

| ID | Company | Fact/input supported | Source name | Publication/filing date | Section or locator | URL |
|---|---|---|---|---|---|---|
| S1 | IBM | Business segments; FY2025 revenue and segment growth; $11.17 consolidated reported diluted EPS; tax-audit benefit | IBM 2025 Form 10-K / Annual Report | Feb. 24, 2026 | Financial Performance Summary; Business overview; Consolidated earnings per share—assuming dilution | https://www.sec.gov/Archives/edgar/data/51143/000005114326000010/ibm-20251231_d2.htm |
| S2 | Oracle | Business mix; FY2026 $5.83 GAAP diluted EPS | Oracle FY2026 Form 10-K | June 22, 2026 | Item 1 — Business; Consolidated Statements of Operations, “Earnings per share attributable to common shareholders—Diluted” | https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm |
| S3 | Accenture | Consulting and managed-services mix; multi-year managed-services contracts; FY2025 $12.15 GAAP diluted EPS | Accenture FY2025 Form 10-K | Oct. 10, 2025 | Item 7, “Type of Work” and “New Bookings”; Note 3 — Earnings Per Share, p. F-20 | https://www.sec.gov/Archives/edgar/data/1467373/000146737325000217/acn-20250831.htm |
| S4 | IBM | Sept. 9, 2026 NYSE close of $239.94 | IBM Historical Stock Lookup | Sept. 9, 2026 | Historical close for Sept. 9, 2026 | https://ibm.gcs-web.com/stock-information/historic-stock-lookup |
| S5 | Oracle | Sept. 9, 2026 NYSE close of $161.63 | StockAnalysis Oracle Price History | Accessed Sept. 16, 2026 | Daily historical table, Sept. 9, 2026 | https://stockanalysis.com/stocks/orcl/history/ |
| S6 | Accenture | Sept. 9, 2026 NYSE close of $175.80 | StockAnalysis Accenture Price History | Accessed Sept. 16, 2026 | Daily historical table, Sept. 9, 2026 | https://stockanalysis.com/stocks/acn/history/ |
| S7 | IBM | Existing Week 3 DCF result, valuation date, assumptions and documented placeholders | IBM DCF model and input memorandum in repository | Existing work | `IBM Report/IBM DCF/dcf.py`; `IBM Report/IBM DCF/ibm_inputs.md` | Local repository |

## Quality Control

- [x] IBM and the September 9, 2026 valuation date are explicit.
- [x] The initial peer policy precedes the peer decisions.
- [x] Exactly two listed operating-company candidates were investigated.
- [x] Each candidate has primary-source business-model and annual reported diluted-EPS evidence.
- [x] Both candidates have a documented QUALIFY judgment and comparability limitation.
- [x] Annual reported diluted EPS—not adjusted EPS or annualized quarterly EPS—is used throughout.
- [x] Each annual EPS was public before September 9, 2026.
- [x] IBM, ORCL, and ACN use the same September 9, 2026 closing-price date.
- [x] The adapted calculator supports an EXCLUDE status and omits excluded peers from valuation.
- [x] No Asbury, AutoNation, or Group 1 valuation inputs remain in the IBM calculator or Lab 08 analysis.
- [x] One admitted peer P/E is manually validated.
- [x] The changed-peer test is predicted, calculated, and interpreted.
- [x] The existing Week 3 DCF result is preserved, not rebuilt or averaged with P/E.
- [x] DCF/P-E comparison, skeptical review, judgment, conditional conclusion, sources, and locators are included.
- [x] Known limitations are identified rather than filled with unsupported values.

## Remaining Unresolved Items

1. A source-supported normalized IBM EPS that removes the disclosed FY2025 tax-audit benefit is not present. The impact can be identified, but an appropriate normalized EPS cannot be calculated without a documented tax normalization.
2. The existing Week 3 DCF identifies cost of debt, tax rate, EBIT margins, D&A, capex, working capital, and terminal growth as placeholders. This lab preserves rather than rebuilds that DCF, so those inputs remain unresolved.
3. No single listed operating-company peer found here matches IBM's combined Software, Consulting, Infrastructure, and Financing mix. The peer P/E range should therefore remain a qualified triangulation reference rather than a precise value.
