from datetime import datetime

PERSISTENCE_THRESHOLD_DATE = datetime.fromisoformat("2024-05-09")


def compute_follow_up_persistence(group):
    last_delivery_date = group["DT_EROG"].iloc[-1]
    last_delivery_qta = group["QTA"].iloc[-1]
    interval_days = (PERSISTENCE_THRESHOLD_DATE - datetime.fromisoformat(last_delivery_date)).days

    if interval_days > 30 * (1 + last_delivery_qta):
        return 1
    else:
        return 0
