"""
Compute the adherence for each patient in the group
"""

from pandas import DataFrame


def compute_adherence_numerator(group: DataFrame):
    """
    Compute the adherence for each patient in the group
    Adherence for a patient is the sum of each real therapy duration but the last one
    :param group: group
    :return: adherence for each patient
    """
    if len(group) > 1:
        return group["giorni di terapia reali (PDD)"][:-1].sum()

    return 0
