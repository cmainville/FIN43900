# Lab 09 — Pro-Forma Build

**Question:** What are five years of a company's statements worth, built from assumptions you can defend, and how do you know the statements are right?

`proforma.py` builds a five-year, linked three-statement model for Asbury Automotive Group (ABG), beginning with the FY2025 opening balance sheet. It projects the income statement first, then all non-cash balance-sheet accounts, derives FCFE, and determines cash last through cash generation and revolver mechanics. `assert_balanced` checks every projected year before valuation.

The central judgment assumptions are 1.8% annual organic revenue growth, a 17.05% gross margin, and SG&A as a share of gross profit declining from 66.5% in 2026 to 64.5% from 2028 onward. The model otherwise applies the supplied operating, working-capital, financing, and valuation assumptions directly.

## Known-answer verification

| Line (USD millions except per share) | FY2026E | FY2030E |
| --- | ---: | ---: |
| Revenue | 18,323.0 | 19,678.3 |
| Operating income | 844.2 | 971.4 |
| Net income | 413.6 | 527.5 |
| FCFE | 211.4 | 342.3 |
| Cash, year end | 101.8 | 719.8 |
| Assets − liabilities − equity | 0.0 | 0.0 |

The FCFE valuation produces an equity value of $5,237.3 million, or **$291.75 per share**. Value after 2030 represents 79.8% of total equity value (approximately 80%). All annual balance-sheet checks equal zero. The built-in failure test changes FY2026E cash to 40.4 and confirms that `assert_balanced` rejects it with an FY2026E balance-sheet gap of approximately -61.4.

## Reflections

1. **Why does the model compute cash last?** Cash is the accumulated result of operating cash generation, investment, financing, share repurchases, and any revolver draw or repayment. Calculating it last preserves the causal links rather than treating cash as an arbitrary plug.

2. **What does the `-61.4` balance-sheet gap tell you when FY2026 cash is incorrectly held at 40.4?** It shows that the balance sheet is short $61.4 million of assets because the calculated cash generation was discarded. The error identifies an unrecorded cash-flow effect, not a problem to solve by forcing a balance-sheet plug.

3. **What is floor-plan financing and why does it rise with inventory?** Floor-plan financing is short-term borrowing used by auto dealers to finance vehicle inventory. More vehicles held for sale require more inventory funding, so the balance rises with inventory under the specified ratio.

4. **Why is floor-plan borrowing included in FCFE in this model?** The change in floor-plan borrowing supplies or consumes cash available to common equity after operations and investment. Treating it as financing linked to inventory captures that working-capital funding effect in FCFE.
