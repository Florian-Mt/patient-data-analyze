import argparse
import logging
import os
import time

import pandas

from generate_datasheets.compute_ouptput_data import compute_dataframe_for_minsan
from functions.dir_path import dir_path
from functions.round_n import round_n

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file",
        required=True,
        type=argparse.FileType("r"),
        dest="input_file",
        metavar="<input data file>",
        help="Number of individuals in each population"
    )
    parser.add_argument(
        "-o", "--output-dir",
        required=False,
        type=dir_path,
        default=os.path.join(os.getcwd(), "output"),
        dest="output_directory",
        metavar="<output directory>",
        help="Output directory for computed datasheets"
    )
    parser.add_argument(
        "-m",
        action="store_true",
        dest="export_minsan_files",
        help="Also export a specific datasheet for each drug"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = getargs()
    logger.info("Arguments parsed successfully.")

    # Read the input file
    input_data = pandas.read_excel(args.input_file.name, parse_dates=["DT_EROG", "DT_NAS"], date_format="%d/%m/%Y")
    logger.info("Input file read successfully.")

    # Then do the same for all data
    logger.info("")
    start = time.time()
    output_data = compute_dataframe_for_minsan(input_data, mixed_minsan=True)
    output_file = os.path.join(args.output_directory, "output_global.csv")
    output_data.to_csv(output_file, index=False)
    end = time.time()
    logger.info(f"Output computed for all drugs in {round_n(end - start, 3)} s.")
    logger.info(f"Results written in {output_file}.")

    if args.export_minsan_files:
        # For each MINSAN code, compute resulting data and generate a CSV file
        for minsan_code in input_data["MINSAN"].unique():
            logger.info("")
            start = time.time()
            output_data = compute_dataframe_for_minsan(input_data[input_data["MINSAN"] == minsan_code])
            output_file = os.path.join(args.output_directory, f"output_{minsan_code}.csv")
            output_data.to_csv(output_file, index=False)
            end = time.time()
            logger.info(f"Output computed for {minsan_code} drug in {round_n(end - start, 3)} s.")
            logger.info(f"Results written in {output_file}.")
