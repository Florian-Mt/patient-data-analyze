import pandas

from functions.compute_adherence_numerator import compute_adherence_numerator
from functions.compute_average_days import compute_average_days
from functions.compute_delays import compute_delays
from functions.compute_follow_up_persistency import compute_follow_up_persistency
from functions.compute_minsan_changes import compute_minsan_changes
from functions.compute_persistency import compute_persistency
from functions.first_prod import first_prod
from functions.round_n import round_n
from functions.sum_importomov import sum_importomov


def compute_dataframe_for_minsan(input_data, mixed_minsan=False):
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
    adherence = round_n(100 * (adherence_numerator / adherence_denominator))

    # Compute the adherence
    output_data["ADERENZA"] = adherence
    output_data["NUMERATORE ADERENZA(GIORNI DI TERAPIA)"] = adherence_numerator
    output_data["DENOMINATORE ADERENZA(NUM GIORNI TRA PRIMA E ULTIMA CONSEGNA)"] = adherence_denominator

    # Compute shift if minsan data is mixed
    if mixed_minsan:
        output_data["SHIFT"] = input_data_grouped_by_user.apply(compute_minsan_changes).values

    # Determine the adherence and cast the boolean into an int
    output_data["BASSA ADERENZA"] = (adherence < 40).astype(int)
    output_data["INTERMEDIA ADERENZA"] = ((40 <= adherence) & (adherence < 80)).astype(int)
    output_data["ALTA ADERENZA"] = (adherence >= 80).astype(int)

    output_data["PERSISTENZA"] = input_data_grouped_by_user.apply(compute_persistency).values
    output_data["Persistenza di Follow-up"] = input_data_grouped_by_user.apply(compute_follow_up_persistency).values

    output_data["IMPORTOMOV"] = input_data_grouped_by_user.apply(sum_importomov, include_groups=False).values

    output_data["PRIMO_PROD"] = input_data_grouped_by_user.apply(first_prod).values

    # Format dates before exporting data
    output_data["DT_NAS"] = output_data["DT_NAS"].dt.strftime("%d/%m/%Y")
    output_data["DATA PRIMA CONSEGNA"] = output_data["DATA PRIMA CONSEGNA"].dt.strftime("%d/%m/%Y")
    output_data["DATA ULTIMA CONSEGNA"] = output_data["DATA ULTIMA CONSEGNA"].dt.strftime("%d/%m/%Y")

    # Remove rows having adherence too high
    unacceptable_rows_indices = output_data[output_data["ADERENZA"] >= 560].index
    output_data.drop(unacceptable_rows_indices, inplace=True)

    return output_data
