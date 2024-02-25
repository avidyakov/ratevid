def exchange(
    *,
    from_,
    to,
    amount: float,
):
    return round(amount / from_.rate * to.rate, 2)
