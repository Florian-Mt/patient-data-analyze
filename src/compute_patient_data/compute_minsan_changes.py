"""
Compute the number of changes of MINSAN for each patient in the group
"""

from pandas import DataFrame


def compute_minsan_changes(group: DataFrame):
    """
    Compute the number of changes of MINSAN for each patient in the group
    :param group: group
    :return: number of changes of MINSAN for each patient in the group
    """
    count = 0
    previous_minsan = group["MINSAN"].iloc[0]

    for i in range(1, len(group["MINSAN"])):
        current_minsan = group["MINSAN"].iloc[i]
        if current_minsan != previous_minsan:
            count += 1
            previous_minsan = current_minsan

    return count
