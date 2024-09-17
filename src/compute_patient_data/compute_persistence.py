"""
Compute persistence of a treatment for each patient in the group
"""

from datetime import datetime

from pandas import DataFrame


def compute_persistence(group: DataFrame):
    """
    Compute persistence of a treatment for each patient in the group
    :param group: group
    :return: persistence of a treatment for each patient in the group
    """
    count = 0

    for i in range(1, len(group["DT_EROG"])):
        previous_delivery = group["DT_EROG"].iloc[i - 1]
        current_delivery = group["DT_EROG"].iloc[i]
        interval_days = (datetime.fromisoformat(current_delivery) - datetime.fromisoformat(previous_delivery)).days

        # If the current delivery is older of n days with n = 30 + 30 * QTA of previous delivery
        if interval_days > (30 * (1 + group["QTA"].iloc[i - 1])):
            count += 1

    return count
