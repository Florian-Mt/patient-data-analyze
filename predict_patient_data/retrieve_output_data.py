import pandas

from predict_patient_data.summarize_adherence_columns import summarize_adherence_columns


def retrieve_output_data(input_file):
    # Read the input file keeping only the relevant fields for the fine-tuning
    output_data = pandas.read_csv(
        input_file,
        parse_dates=["DT_NAS"],
        date_format="%d/%m/%Y",
        usecols=[
            # Sex
            "SESSO",
            # Date of birth
            "DT_NAS",
            # City of birth
            "COMUNE NASCITA",
            # City of residence
            "COMUNE_RESIDENZA",
            # First drug to take
            "PRIMO_PROD",
            # Adherence
            "BASSA ADERENZA",
            "INTERMEDIA ADERENZA",
            "ALTA ADERENZA",
            # Follow-up persistence
            "Persistenza di Follow-up",
        ],
    )

    # Convert adherence into a single value: 0 for low, 1 for middle, 2 for high, and then remove these columns
    output_data["ADERENZA"] = output_data.apply(summarize_adherence_columns, axis=1)
    output_data.drop(columns=["BASSA ADERENZA", "INTERMEDIA ADERENZA", "ALTA ADERENZA"], inplace=True)

    return output_data
