"""
Summarize the three adherence columns into a single value
"""


def summarize_adherence_columns(row):
    """
    Summarize the three adherence columns into a single value representing which one is active
    0 for low adherence, 1 for intermediate adherence and 2 for high adherence
    :param row: dataframe row
    :return: adherence value
    """

    if row["BASSA ADERENZA"] == 1:
        return 0

    if row["INTERMEDIA ADERENZA"] == 1:
        return 1

    if row["ALTA ADERENZA"] == 1:
        return 2

    return -1
