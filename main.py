import pandas

from functions.compute_ouptput_data import compute_dataframe_for_minsan


EXPORT_MINSAN_FILES = False

if __name__ == "__main__":
    input_file = "V3 estrazione dati antiemicranici al 9-5-24 con PDD.xlsx"

    # Read the input file
    input_data = pandas.read_excel(input_file, parse_dates=["DT_EROG", "DT_NAS"], date_format="%d/%m/%Y")

    if EXPORT_MINSAN_FILES:
        # For each MINSAN code, compute resulting data and generate a CSV file
        for minsan_code in input_data["MINSAN"]:
            output_data = compute_dataframe_for_minsan(input_data[input_data["MINSAN"] == minsan_code])
            output_data.to_csv(f"output_{minsan_code}.csv", index=False)

    # Then do the same for all data
    output_data = compute_dataframe_for_minsan(input_data, mixed_minsan=True)
    output_data.to_csv(f"output_global.csv", index=False)
