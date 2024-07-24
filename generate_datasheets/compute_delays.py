from datetime import datetime


def compute_delays(group):
    count = 0

    for i in range(len(group["DT_EROG"]) - 1):
        end_date = group["DT_EROG"].iloc[i + 1]
        start_date = group["DT_EROG"].iloc[i]
        interval_days = (datetime.fromisoformat(end_date) - datetime.fromisoformat(start_date)).days

        if interval_days >= (35 * group["QTA"].iloc[i]):
            count += 1

    return count
