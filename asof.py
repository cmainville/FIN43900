"""Build an as-of panel and compare its signals with hindsight signals."""

from datetime import date, datetime


# Edit these inputs to run the lab with another decision date or dataset.
DECISION_DATE = "2026-03-31"
DATA = [
    ("AAA", "2026-01", "2026-02-10", 101.0),
    ("AAA", "2026-02", "2026-03-10", 104.0),
    ("AAA", "2026-03", "2026-04-10", 109.0),
    ("AAA", "2026-02", "2026-03-25", 103.0),
    ("BBB", "2026-01", "2026-02-10", 98.0),
    ("BBB", "2026-02", "2026-03-10", 97.0),
    ("BBB", "2026-02", "2026-03-10", 97.0),
    ("BBB", "2026-03", "2026-04-10", 92.0),
    ("CCC", "2026-01", "2026-02-10", 110.0),
    ("CCC", "2026-02", "2026-04-05", 112.0),
    ("", "2026-02", "2026-03-10", 99.0),
    ("CCC", "2026-02", "2026-03-10", 111.0),
]


def print_removed(label, rows):
    numbers = ", ".join(str(row[0]) for row in rows) or "none"
    print(f"{label}: {len(rows)} removed (original rows: {numbers})")


def latest_publications(rows):
    """Keep the last publication for each ticker and measured month."""
    chosen = {}
    for row in rows:
        _, ticker, month, published, _ = row
        key = (ticker, month)
        if key not in chosen or published > chosen[key][3]:
            chosen[key] = row
    return sorted(chosen.values())


def print_signals(label, rows, source_rows=None):
    print(f"\n{label}:")
    tickers = sorted({row[1] for row in rows})
    for ticker in tickers:
        history = sorted((row for row in rows if row[1] == ticker), key=lambda row: row[2])
        if len(history) < 2:
            print(f"  {ticker}: insufficient monthly history")
            continue
        previous, latest = history[-2:]
        change = ((latest[4] / previous[4]) - 1) * 100
        month_name = datetime.strptime(latest[2], "%Y-%m").strftime("%b %Y")
        revised = source_rows is not None and any(
            row[1:3] == latest[1:3] and row[3] < latest[3]
            for row in source_rows
        )
        suffix = ", revised" if revised else ""
        print(f"  {ticker}: {change:+.2f}% ({month_name}{suffix})")


def main():
    decision_date = date.fromisoformat(DECISION_DATE)
    rows = [(number, *values) for number, values in enumerate(DATA, start=1)]

    quarantined = [row for row in rows if not row[1] or not row[1].strip()]
    valid = [row for row in rows if row not in quarantined]

    seen = set()
    duplicates = []
    deduplicated = []
    for row in valid:
        if row[1:] in seen:
            duplicates.append(row)
        else:
            seen.add(row[1:])
            deduplicated.append(row)

    too_late = [row for row in deduplicated if date.fromisoformat(row[3]) > decision_date]
    available = [row for row in deduplicated if row not in too_late]

    panel = latest_publications(available)
    kept_numbers = {row[0] for row in panel}
    revisions = [row for row in available if row[0] not in kept_numbers]

    print(f"Decision date: {decision_date}")
    print("Row funnel:")
    print_removed("Quarantined (missing ticker)", quarantined)
    print_removed("Exact duplicates", duplicates)
    print_removed("Published too late", too_late)
    print_removed("Replaced by revision", revisions)

    print("\nAs-of panel:")
    print("  Row  Ticker  Month    Published   Index")
    for number, ticker, month, published, index in panel:
        print(f"  {number:>3}  {ticker:<6}  {month}  {published}  {index:.1f}")

    print_signals("As-of signals", panel)
    print_signals("Naive signals", latest_publications(deduplicated), deduplicated)


if __name__ == "__main__":
    main()
