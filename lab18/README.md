# FIN439 Lab 19 — Three-Investor SEC Panel

This builds on Lab 18's Buffett script and Streamlit app. Python computes seven checks for Buffett, Cathie Wood, and Michael Burry from five fiscal years of SEC 10-K facts. Missing facts remain not found or not known. Owner earnings retain Lab 18's simplified definition: operating cash flow less all capital spending.

## Run

```bash
cd FIN43900/lab18
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Without an SEC contact email, the app uses the committed November 5, 2026 SEC fact extracts for `COST` and `NVDA`. To fetch live EDGAR data for any ticker, set your own contact email, then restart the app:

```bash
export SEC_CONTACT_EMAIL="your.email@example.com"
python warren-buffett-sec/scripts/sec_analysis.py COST
streamlit run app.py
```

The shared script prints all source-tagged financial values, seven checks, and three verdicts. The two added skill guides are `cathie-wood-sec/SKILL.md` and `michael-burry-sec/SKILL.md`; the Buffett guide remains in place. The three default memos require no LLM. The optional **Generate AI memo** buttons require an installed, signed-in Codex CLI. Each memo's editable text is checked for numbers absent from the script output. Saving writes `memos/TICKER-investor.md`; the existing Lab 18 `memos/TICKER.md` still loads for Buffett when present.

## Test

```bash
python -m unittest -v test_lab18.py test_lab19.py
# With SEC_CONTACT_EMAIL set and network access:
python -m unittest -v test_live_sec.py
```

See [Lab19_Report.md](Lab19_Report.md) for Costco validation, the VTI holding selection, NVIDIA's panel results, and the written lab answers. This is a learning screen, not investment advice; it does not include price or valuation data.
