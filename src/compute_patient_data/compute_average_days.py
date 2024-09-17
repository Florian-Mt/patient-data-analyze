"""
Compute the average duration of a treatment for each patient in the group
"""

from datetime import datetime

from pandas import DataFrame


def compute_average_days(group: DataFrame):
    """
    Compute the average duration of a treatment for each patient in the group
    :param group: group
    :return: average duration of a treatment for each patient in the group
    """
    total_days = 0
    total_intervals = 0

    for i in range(len(group["DT_EROG"]) - 1):
        end_date = group["DT_EROG"].iloc[i + 1]
        start_date = group["DT_EROG"].iloc[i]
        interval_days = (datetime.fromisoformat(end_date) - datetime.fromisoformat(start_date)).days
        weighted_days = interval_days / group["QTA"].iloc[i]
        total_days += weighted_days
        total_intervals += 1

    average_days = total_days / total_intervals if total_intervals > 0 else 0
    return int(average_days)
