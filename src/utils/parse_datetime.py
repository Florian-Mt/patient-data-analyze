"""
Parse string datetime into pandas Timestamp object
"""

import pandas


def parse_datetime(dt):
    """
    Parse string datetime to pandas.Timestamp object if not already parsed
    :param dt: datetime as str or pandas.Timestamp
    :return: pandas.Timestamp object
    """
    if isinstance(dt, str):
        return pandas.Timestamp.fromisoformat(dt)

    return dt
