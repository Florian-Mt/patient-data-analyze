"""
Retrieve the first prod for each patient in the group
"""

from pandas import DataFrame


def first_prod(group: DataFrame):
    """
    Retrieve the first prod for each patient in the group
    :param group: group
    :return: first prod for each patient in the group
    """
    result = group["PROD"].iloc[0]
    return result
