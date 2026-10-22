# Lab 15 Portfolio Stability Dashboard

From the repository root:

```bash
python -m pip install -r lab15/requirements.txt
python lab15/portfolio.py
python -m streamlit run lab15/app.py
```

On systems where the executable is named `python3` (as on the development machine), use:

```bash
python3 -m pip install -r lab15/requirements.txt
python3 lab15/portfolio.py
python3 -m streamlit run lab15/app.py
```

The app starts in Meridian training mode. Switch to Long-Term Growth Portfolio for the committed ETF history. Upload any valid CSV with `Date` and 3–6 asset columns, one chronological observation per consecutive month, to test another universe. The default five-ETF history is `lab15/prices_growth.csv`; the financial engine is `lab15/portfolio.py`. The app uses this local CSV and performs no live request at startup.

To refresh the five ETF prices after verifying the desired completed-month window, edit the date constants in `lab15/download_prices.py` and run `python3 lab15/download_prices.py`. It requests Yahoo daily `Adj Close` explicitly, takes the last available trading day's adjusted close per month, and writes calendar month-end labels. If Yahoo fails or is incomplete, it tries Digrin's monthly “Adjusted price” tables for all five funds. Digrin has lower precision and an insufficiently documented adjustment convention; identify it explicitly in the report if used. Review the resulting CSV and update the report before committing new data. Do not run the downloader as part of app startup.

Run the original and Lab 15 tests from the repository root:

```bash
python3 -m unittest test_portfolio lab15.test_lab15 -v
python3 -m compileall -q lab15
```

For Streamlit Community Cloud, connect this repository and branch, set the entrypoint to `lab15/app.py`, and retain `lab15/requirements.txt` beside it. [Streamlit's file organization guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization) explicitly permits a dependency file beside a subdirectory entrypoint. No secrets, notebook state, or live download are needed for startup. This repository has not been publicly deployed by this work.

The root Lab 13/14 files stay unchanged. This directory is a new amendment for the 15-year growth exercise; see `lab15-notes.md` for sources, assumptions, tests, and student-only activities.
