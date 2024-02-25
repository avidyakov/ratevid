import decimal


def exchange(
    *,
    from_: decimal.Decimal,
    to: decimal.Decimal,
    amount: decimal.Decimal,
) -> decimal.Decimal:
    return round(amount / from_ * to, 2)
