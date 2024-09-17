"""
Sum up all importomov values for each patient in the group
"""

from pandas import DataFrame


def sum_importomov(group: DataFrame):
    """
    Sum up all importomov values for each patient in the group
    :param group: group
    :return: importomov summed-up values for each patient in the group, rounded to three decimal places
    """
    result = group["IMPORTOMOV"].sum()
    return round(result, 3)
