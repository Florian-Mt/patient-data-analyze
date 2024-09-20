"""
Compute persistence of a treatment for each patient in the group
"""

from pandas import DataFrame

from utils.parse_datetime import parse_datetime


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

        # If pandas has not already parsed the dates, then parse it
        current_delivery = parse_datetime(current_delivery)
        previous_delivery = parse_datetime(previous_delivery)

        # If the current delivery is older of n days with n = 30 + 30 * QTA of previous delivery
        interval_days = (current_delivery - previous_delivery).days
        if interval_days > (30 * (1 + group["QTA"].iloc[i - 1])):
            count += 1

    return count
