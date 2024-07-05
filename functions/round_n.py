def round_n(x, n=2):
    factor = 10 ** n
    return round(x * factor) / factor
