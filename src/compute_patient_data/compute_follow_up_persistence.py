"""
Compute the follow-up persistence for each patient in the group
"""

from datetime import datetime

from pandas import DataFrame

from utils.parse_datetime import parse_datetime

PERSISTENCE_THRESHOLD_DATE = datetime.fromisoformat("2024-05-09")


def compute_follow_up_persistence(group: DataFrame):
    """
    Compute the follow-up persistence for each patient in the group
    :param group: group
    :return: follow-up persistence
    """
    last_delivery_date = group["DT_EROG"].iloc[-1]
    last_delivery_qta = group["QTA"].iloc[-1]

    # If pandas has not already parsed the dates, then parse it
    last_delivery_date = parse_datetime(last_delivery_date)

    interval_days = (PERSISTENCE_THRESHOLD_DATE - last_delivery_date).days

    if interval_days > 30 * (1 + last_delivery_qta):
        return 1

    return 0
