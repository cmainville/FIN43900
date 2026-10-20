"""Import four Yahoo Finance Adj Close CSV downloads into monthly prices.csv.

This script does not download data. Download BIL, IEF, LQD, and VT separately
from Yahoo Finance Historical Data with the Adj Close column present. Use the
same provider and adjustment definition for all four files. Monthly exports
are preferred; daily exports are accepted with --frequency daily.

Example:
    python import_prices.py --frequency monthly --bil BIL.csv --ief IEF.csv \
        --lqd LQD.csv --vt VT.csv --output prices.csv

The importer creates no output unless every ETF has exactly one valid adjusted
price for each month from October 2021 through September 2026.
"""

import argparse
import calendar
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import sys


TICKERS = ("BIL", "IEF", "LQD", "VT")
HEADER = ("Date",) + TICKERS
START = (2021, 10)
END = (2026, 9)


def months_in_scope():
    year, month = START
    while (year, month) <= END:
        yield year, month
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)


EXPECTED_MONTHS = tuple(months_in_scope())


def month_end(year, month):
    return date(year, month, calendar.monthrange(year, month)[1])


def read_yahoo_adjusted_csv(path, frequency):
    """Read authentic Adj Close observations; use the final dated row per month."""
    observations = {}
    seen_dates = set()
    with Path(path).open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or "Date" not in reader.fieldnames or "Adj Close" not in reader.fieldnames:
            raise ValueError(f"{path}: expected Yahoo columns 'Date' and 'Adj Close'; ordinary 'Close' is not accepted")
        for line_number, row in enumerate(reader, start=2):
            try:
                observed_date = date.fromisoformat(row["Date"])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"{path}:{line_number}: invalid date") from exc
            month = (observed_date.year, observed_date.month)
            if month not in EXPECTED_MONTHS:
                continue
            try:
                price = Decimal(row["Adj Close"])
            except (TypeError, InvalidOperation) as exc:
                raise ValueError(f"{path}:{line_number}: invalid Adj Close") from exc
            if not price.is_finite() or price <= 0:
                raise ValueError(f"{path}:{line_number}: Adj Close must be finite and positive")
            if observed_date in seen_dates:
                raise ValueError(f"{path}:{line_number}: duplicate source date {observed_date}")
            seen_dates.add(observed_date)
            if frequency == "monthly" and month in observations:
                raise ValueError(f"{path}: duplicate monthly observations for {month[0]}-{month[1]:02d}")
            if month not in observations or observed_date > observations[month][0]:
                observations[month] = (observed_date, price)
    missing = [f"{year}-{month:02d}" for year, month in EXPECTED_MONTHS if (year, month) not in observations]
    if missing:
        raise ValueError(f"{path}: missing {len(missing)} month(s): {', '.join(missing)}")
    if frequency == "daily":
        for (year, month), (observed_date, _) in observations.items():
            if (month_end(year, month) - observed_date).days > 4:
                raise ValueError(
                    f"{path}: final observed trading date {observed_date} is too early "
                    f"for {year}-{month:02d}; check that the daily download is complete"
                )
    return observations


def validate_prices_csv(path):
    """Check the delivered CSV's schema, chronology, coverage and prices."""
    rows = []
    with Path(path).open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if tuple(reader.fieldnames or ()) != HEADER:
            raise ValueError(f"Expected columns exactly {','.join(HEADER)}")
        for line_number, row in enumerate(reader, start=2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"Row {line_number}: malformed or missing value")
            try:
                observed_date = date.fromisoformat(row["Date"])
            except ValueError as exc:
                raise ValueError(f"Row {line_number}: invalid ISO date") from exc
            for ticker in TICKERS:
                try:
                    price = Decimal(row[ticker])
                except InvalidOperation as exc:
                    raise ValueError(f"Row {line_number}: {ticker} is not numeric") from exc
                if not price.is_finite() or price <= 0:
                    raise ValueError(f"Row {line_number}: {ticker} must be finite and positive")
            rows.append(observed_date)
    expected_dates = [month_end(*month) for month in EXPECTED_MONTHS]
    if rows != expected_dates:
        missing = [str(day) for day in expected_dates if day not in rows]
        duplicates = sorted({str(day) for day in rows if rows.count(day) > 1})
        raise ValueError(
            f"Expected 60 continuous, sorted calendar month-ends from {expected_dates[0]} "
            f"to {expected_dates[-1]}; missing={missing}, duplicates={duplicates}"
        )
    return len(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frequency", choices=("monthly", "daily"), default="monthly")
    for ticker in TICKERS:
        parser.add_argument(f"--{ticker.lower()}", type=Path,
                            help=f"Yahoo Finance CSV download for {ticker}")
    parser.add_argument("--output", type=Path, default=Path("prices.csv"))
    parser.add_argument("--validate-only", type=Path,
                        help="Validate an existing prices.csv without importing")
    args = parser.parse_args(argv)
    if args.validate_only:
        print("Source: CSV provenance must be checked against the original downloads and notes")
        try:
            count = validate_prices_csv(args.validate_only)
        except (OSError, ValueError) as exc:
            print(f"Overall: FAIL — {exc}", file=sys.stderr)
            return 1
        print(f"Observation count: {count}; date range: 2021-10-31 to 2026-09-30")
        print("Valid observations per ETF: " + ", ".join(f"{ticker}={count}" for ticker in TICKERS))
        print("Missing months: none; duplicate months: none")
        print("Overall: PASS for structure and values; verify provenance from source downloads")
        return 0
    missing_inputs = [ticker for ticker in TICKERS if getattr(args, ticker.lower()) is None]
    if missing_inputs:
        parser.error("provide all four Yahoo downloads: " + ", ".join(missing_inputs))
    inputs = {ticker: getattr(args, ticker.lower()) for ticker in TICKERS}
    print("Source: Yahoo Finance Historical Data CSV, Adj Close (one source per ticker)")
    print(f"Frequency: {args.frequency}; required range: 2021-10 through 2026-09")
    try:
        series = {ticker: read_yahoo_adjusted_csv(path, args.frequency)
                  for ticker, path in inputs.items()}
        print("Source observation count: " + ", ".join(
            f"{ticker}={len(series[ticker])}" for ticker in TICKERS
        ))
        rows = [
            [month_end(year, month).isoformat()] +
            [str(series[ticker][(year, month)][1]) for ticker in TICKERS]
            for year, month in EXPECTED_MONTHS
        ]
        # Stage and validate before replacing an existing output file.
        staged = args.output.with_name(args.output.name + ".pending")
        try:
            with staged.open("w", newline="", encoding="utf-8") as target:
                writer = csv.writer(target)
                writer.writerow(HEADER)
                writer.writerows(rows)
            count = validate_prices_csv(staged)
            staged.replace(args.output)
        finally:
            staged.unlink(missing_ok=True)
    except (OSError, ValueError) as exc:
        print(f"Overall: FAIL — {exc}", file=sys.stderr)
        return 1
    print(f"Observation count: {count}; date range: {rows[0][0]} to {rows[-1][0]}")
    print("Valid observations per ETF: " + ", ".join(f"{ticker}={count}" for ticker in TICKERS))
    print("Missing months: none; duplicate months: none")
    print("Date labels are calendar month-ends; source prices remain unchanged.")
    print("Overall: PASS for structure and values; verify provenance from source downloads")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
