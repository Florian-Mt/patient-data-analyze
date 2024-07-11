from functions.round_n import round_n


def sum_importomov(group):
    result = group["IMPORTOMOV"].sum()
    return round_n(result, 3)
