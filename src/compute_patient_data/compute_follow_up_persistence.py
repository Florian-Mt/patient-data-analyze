"""
Compute the follow-up persistence for each patient in the group
"""

from pandas import DataFrame, Timestamp

from utils.parse_datetime import parse_datetime


def compute_follow_up_persistence(max_delivery_date: Timestamp, group: DataFrame):
    """
    Compute the follow-up persistence for each patient in the group
    :param max_delivery_date: maximum delivery date to compute difference
    :param group: group
    :return: follow-up persistence
    """
    last_delivery_date = group["DT_EROG"].iloc[-1]
    last_delivery_qta = group["QTA"].iloc[-1]

    # If pandas has not already parsed the dates, then parse it
    max_delivery_date = parse_datetime(max_delivery_date)
    last_delivery_date = parse_datetime(last_delivery_date)

    interval_days = (max_delivery_date - last_delivery_date).days

    if interval_days > 30 * (1 + last_delivery_qta):
        return 1

    return 0
