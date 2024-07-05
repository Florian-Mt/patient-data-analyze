from datetime import datetime
import pandas


def round_n(x, n=2):
    factor = 10 ** n
    return round(x * factor) / factor


def compute_average_days(group):
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


def compute_delays(group):
    count = 0

    for i in range(len(group["DT_EROG"]) - 1):
        end_date = group["DT_EROG"].iloc[i + 1]
        start_date = group["DT_EROG"].iloc[i]
        interval_days = (datetime.fromisoformat(end_date) - datetime.fromisoformat(start_date)).days

        condition_for_date1_p_1 = (group["QTA"].iloc[i] == 1 and (interval_days <= 27 or interval_days >= 33))
        condition_for_date1_p_2 = (group["QTA"].iloc[i] == 2 and (interval_days <= 55 or interval_days >= 65))
        if condition_for_date1_p_1 or condition_for_date1_p_2:
            count += 1

    return count


def compute_adherence_numerator(group):
    if len(group) > 1:
        return group["giorni di terapia reali (PDD)"][:-1].sum()
    else:
        return 0


def compute_dataframe_for_minsan(input_data, keep_minsan_column=False):
    # Group input_data for each user
    input_data_grouped_by_user = input_data.groupby("CODICE PAZIENTE UNIVOCO")

    output_data = input_data_grouped_by_user.agg({
        "SESSO": "first",
        "DT_NAS": "first",
        "COMUNE NASCITA": "first",
        "COMUNE_RESIDENZA": "first",
        "ASL_APPARTENENZA": "first",
    }).reset_index()

    # Rename the columns
    output_data.columns = [
        "CODICE PAZIENTE UNIVOCO",
        "SESSO",
        "DT_NAS",
        "COMUNE NASCITA",
        "COMUNE_RESIDENZA",
        "ASL_APPARTENENZA",
    ]

    if keep_minsan_column:
        output_data["MINSAN"] = input_data_grouped_by_user["MINSAN"].first().values

    # Retrieve the first and last delivery for DT_EROG and cast them to datetimes
    output_data["DATA PRIMA CONSEGNA"] = pandas.to_datetime(input_data_grouped_by_user["DT_EROG"].min().values)
    output_data["DATA ULTIMA CONSEGNA"] = pandas.to_datetime(input_data_grouped_by_user["DT_EROG"].max().values)

    # Compute the average days
    output_data["MEDIA GIORNI"] = input_data_grouped_by_user.apply(compute_average_days, include_groups=False).values

    # Retrieve the count of distinct values
    output_data["NUMERO CONSEGNE TOTALI"] = input_data_grouped_by_user["DT_EROG"].nunique().values

    # Compute the number of delays
    output_data["NUMERO RITARDI"] = input_data_grouped_by_user.apply(compute_delays, include_groups=False).values

    # Compute adherence numerator and denominator
    adherence_numerator = input_data_grouped_by_user.apply(compute_adherence_numerator, include_groups=False).values
    adherence_denominator = (output_data["DATA ULTIMA CONSEGNA"] - output_data["DATA PRIMA CONSEGNA"]).dt.days

    # Compute the adherence
    output_data["ADERENZA"] = round_n(100 * (adherence_numerator / adherence_denominator))
    output_data["NUMERATORE ADERENZA(GIORNI DI TERAPIA)"] = adherence_numerator
    output_data["DENOMINATORE ADERENZA(NUM GIORNI TRA PRIMA E ULTIMA CONSEGNA)"] = adherence_denominator

    # Format dates before exporting data
    output_data["DT_NAS"] = output_data["DT_NAS"].dt.strftime("%d/%m/%Y")
    output_data["DATA PRIMA CONSEGNA"] = output_data["DATA PRIMA CONSEGNA"].dt.strftime("%d/%m/%Y")
    output_data["DATA ULTIMA CONSEGNA"] = output_data["DATA ULTIMA CONSEGNA"].dt.strftime("%d/%m/%Y")

    return output_data


if __name__ == "__main__":
    input_file = "V3 estrazione dati antiemicranici al 9-5-24 con PDD.xlsx"

    # Read the input file
    input_data = pandas.read_excel(input_file, parse_dates=["DT_EROG", "DT_NAS"], date_format="%d/%m/%Y")

    # For each MINSAN code, compute resulting data and generate a CSV file
    for minsan_code in input_data["MINSAN"]:
        output_data = compute_dataframe_for_minsan(input_data[input_data["MINSAN"] == minsan_code])
        output_data.to_csv(f"output_{minsan_code}.csv", index=False)

    # Then do the same for all data
    output_data = compute_dataframe_for_minsan(input_data, keep_minsan_column=True)
    output_data.to_csv(f"output_global.csv", index=False)
