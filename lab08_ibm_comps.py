"""Lab 08: P/E comparable-company valuation for IBM.

All prices are NYSE closing prices on September 9, 2026. EPS values are
annual, reported GAAP diluted EPS; they are not adjusted or annualized
quarterly figures. A peer marked ``exclude`` remains visible in the output but
does not enter the implied-value calculation.
"""

from decimal import Decimal, InvalidOperation


# ---------------------------------------------------------------------------
# Editable inputs
# Use strings for numeric inputs so Decimal retains all entered precision.
# Use None for a missing price or EPS.
# ---------------------------------------------------------------------------
TARGET = {
    "ticker": "IBM",
    "name": "International Business Machines",
    "price": "239.94",
    "diluted_eps": "11.17",
}

PEERS = [
    {
        "ticker": "ORCL",
        "name": "Oracle",
        "price": "161.63",
        "diluted_eps": "5.83",
        "status": "qualify",
    },
    {
        "ticker": "ACN",
        "name": "Accenture",
        "price": "175.80",
        "diluted_eps": "12.15",
        "status": "qualify",
    },
]


def positive_decimal(value):
    """Return a positive, finite Decimal, or None when not meaningful."""
    if value is None or isinstance(value, bool):
        return None
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None
    if not number.is_finite() or number <= 0:
        return None
    return number


def normalized_ticker(company):
    """Return a normalized ticker for comparisons and deduplication."""
    ticker = company.get("ticker")
    return "" if ticker is None else str(ticker).strip().upper()


def unique_non_target_peers(peers, target_ticker):
    """Keep the first occurrence of each peer and remove the target."""
    result = []
    seen = set()
    normalized_target = str(target_ticker).strip().upper()

    for peer in peers:
        ticker = normalized_ticker(peer)
        if ticker == normalized_target or ticker in seen:
            continue
        seen.add(ticker)
        result.append(peer)
    return result


def median(values):
    """Compute a median without rounding any intermediate values."""
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return (ordered[midpoint - 1] + ordered[midpoint]) / Decimal("2")


def peer_multiple(peer):
    """Return the peer P/E, or None when price or EPS is not meaningful."""
    price = positive_decimal(peer.get("price"))
    eps = positive_decimal(peer.get("diluted_eps"))
    if price is None or eps is None:
        return None
    return price / eps


def peer_status(peer):
    """Return an allowed peer status, defaulting undocumented entries to use."""
    status = str(peer.get("status", "use")).strip().lower()
    return status if status in {"use", "qualify", "exclude"} else "exclude"


def money(value):
    return f"${value:.2f}"


def signed_money(value):
    sign = "+" if value >= 0 else "-"
    return f"{sign}${abs(value):.2f}"


def main():
    target_ticker = normalized_ticker(TARGET)
    target_name = TARGET.get("name") or target_ticker
    target_eps = positive_decimal(TARGET.get("diluted_eps"))
    target_price = positive_decimal(TARGET.get("price"))
    peers = unique_non_target_peers(PEERS, target_ticker)

    print(f"P/E Comparable-Company Valuation: {target_name} ({target_ticker})")
    if target_price is None or target_eps is None:
        print("Target price or diluted EPS: not meaningful")
    else:
        print(f"Target closing price: {money(target_price)}")
        print(f"Target diluted EPS: {money(target_eps)}")

    print("\nPeer P/E multiples")
    valid_peers = []
    for peer in peers:
        ticker = normalized_ticker(peer) or "(missing ticker)"
        status = peer_status(peer)
        multiple = peer_multiple(peer)
        if status == "exclude":
            print(f"{ticker} ({status}): excluded from valuation")
        elif multiple is None:
            print(f"{ticker} ({status}): not meaningful")
        else:
            valid_peers.append((peer, multiple))
            implied_price = multiple * target_eps if target_eps is not None else None
            print(f"{ticker} ({status}): {multiple:.6f}x; "
                  f"IBM implied price {money(implied_price)}")

    print("\nImplied target prices")
    if not valid_peers:
        print("No usable peers.")
        full_median_price = None
    elif target_eps is None:
        print("Target diluted EPS is not meaningful; implied prices are not meaningful.")
        full_median_price = None
    else:
        multiples = [multiple for _, multiple in valid_peers]
        minimum_multiple = min(multiples)
        median_multiple = median(multiples)
        maximum_multiple = max(multiples)
        full_median_price = median_multiple * target_eps

        if len(valid_peers) == 1:
            print("Reference estimate (only one valid peer remains):")
            print(f"Peer P/E: {median_multiple:.6f}x")
            print(f"Implied price: {money(full_median_price)}")
        else:
            print(f"Minimum peer P/E: {minimum_multiple:.6f}x")
            print(f"Minimum implied price: {money(minimum_multiple * target_eps)}")
            print(f"Median peer P/E: {median_multiple:.6f}x")
            print(f"Median implied price: {money(full_median_price)}")
            print(f"Maximum peer P/E: {maximum_multiple:.6f}x")
            print(f"Maximum implied price: {money(maximum_multiple * target_eps)}")

    print("\nLeave-one-peer-out test")
    for removed_peer, _ in valid_peers:
        removed_ticker = normalized_ticker(removed_peer) or "(missing ticker)"
        remaining_multiples = [
            multiple
            for peer, multiple in valid_peers
            if peer is not removed_peer
        ]
        if not remaining_multiples or target_eps is None or full_median_price is None:
            print(f"Remove {removed_ticker}: no estimate")
            continue

        remaining_price = median(remaining_multiples) * target_eps
        dollar_change = remaining_price - full_median_price
        print(
            f"Remove {removed_ticker}: remaining median-implied price "
            f"{money(remaining_price)}; change {signed_money(dollar_change)}"
        )

    if not valid_peers:
        print("No estimate.")


if __name__ == "__main__":
    main()
