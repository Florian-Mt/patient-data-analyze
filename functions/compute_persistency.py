from datetime import datetime


def compute_persistency(group):
    count = 0
    previous_delivery = group["DT_EROG"].iloc[0]

    for i in range(1, len(group["DT_EROG"])):
        current_delivery = group["DT_EROG"].iloc[i]
        interval_days = (datetime.fromisoformat(current_delivery) - datetime.fromisoformat(previous_delivery)).days

        # If the current delivery is older of n days with n = 30 + 30 * QTA of previous delivery
        if interval_days > (30 + 30 * group["QTA"].iloc[i - 1]):
            count += 1
            previous_delivery = current_delivery

    return count
