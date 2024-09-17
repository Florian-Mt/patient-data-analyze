"""
Compute the number of delays between treatments for each patient in the group
"""

from datetime import datetime

from pandas import DataFrame


def compute_delays(group: DataFrame):
    """
    Compute the number of delays between treatments for each patient in the group
    :param group: group
    :return: number of delays between treatments for each patient in the group
    """
    count = 0

    for i in range(len(group["DT_EROG"]) - 1):
        end_date = group["DT_EROG"].iloc[i + 1]
        start_date = group["DT_EROG"].iloc[i]
        interval_days = (datetime.fromisoformat(end_date) - datetime.fromisoformat(start_date)).days

        if interval_days >= (35 * group["QTA"].iloc[i]):
            count += 1

    return count
