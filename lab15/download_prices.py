"""Download 60 completed month-end adjusted ETF closes from Yahoo Finance.

Run from the repository root: python lab15/download_prices.py
The app never invokes this script at startup.
"""
from pathlib import Path

import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup

TICKERS = ("VTI", "VXUS", "XLE", "IWM", "IAU")
START, END = "2021-10-01", "2026-10-01"
OUTPUT = Path(__file__).with_name("prices_growth.csv")


def yahoo_prices():
    columns = {}
    for ticker in TICKERS:
        history = yf.Ticker(ticker).history(start=START, end=END, interval="1d",
                                            auto_adjust=False, actions=False)
        if history.empty or "Adj Close" not in history:
            raise RuntimeError(f"Yahoo has no adjusted close history for {ticker}")
        series = history["Adj Close"]
        if series.isna().any() or (series <= 0).any():
            raise RuntimeError(f"Invalid Yahoo adjusted closes for {ticker}")
        series.index = pd.to_datetime(series.index).tz_localize(None)
        columns[ticker] = series.resample("ME").last()
    return pd.DataFrame(columns)


def digrin_prices():
    """Fallback: Digrin's labeled monthly adjusted-price table, all tickers.

    Digrin publishes only two decimals and does not establish equivalence to
    Yahoo Adj Close. A fallback output must be reported as Digrin sourced.
    """
    columns = {}
    for ticker in TICKERS:
        url = f"https://www.digrin.com/stocks/detail/{ticker}/price"
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = next((t for t in soup.find_all("table") if "Adjusted price" in t.get_text(" ", strip=True)), None)
        if table is None:
            raise RuntimeError(f"Digrin adjusted-price table missing for {ticker}")
        observations = {}
        for row in table.find_all("tr"):
            cells = [cell.get_text(" ", strip=True) for cell in row.find_all(("th", "td"))]
            if len(cells) < 3:
                continue
            try:
                month = pd.to_datetime(cells[0], format="%B %Y")
                price = float(cells[1].replace("$", "").replace(",", ""))
            except ValueError:
                continue
            if month in observations:
                raise RuntimeError(f"Duplicate Digrin month for {ticker}: {month}")
            observations[month] = price
        columns[ticker] = pd.Series(observations).sort_index().resample("ME").last()
    return pd.DataFrame(columns)


def validate_window(frame, source):
    frame = frame.loc["2021-10-31":"2026-09-30"]
    wanted = pd.date_range("2021-10-31", "2026-09-30", freq="ME")
    if not frame.index.equals(wanted) or frame.isna().any().any() or len(frame) != 60 or not (frame > 0).all().all():
        raise RuntimeError(f"{source} history is incomplete or invalid")
    return frame


def main():
    try:
        frame = validate_window(yahoo_prices(), "Yahoo")
        source = "Yahoo Finance Adj Close"
    except Exception as yahoo_error:
        print(f"Yahoo retrieval failed ({yahoo_error}); attempting Digrin for all tickers")
        frame = validate_window(digrin_prices(), "Digrin")
        source = "Digrin Adjusted price (two-decimal; methodology differs/unspecified)"
    frame.index.name = "Date"
    frame.to_csv(OUTPUT, float_format="%.12g", date_format="%Y-%m-%d")
    print(f"Saved {len(frame)} monthly adjusted observations from {source} to {OUTPUT}")


if __name__ == "__main__":
    main()
