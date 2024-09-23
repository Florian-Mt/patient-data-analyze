"""
Compare the predicted values with the real values with F1 and accuracy criteria if the values match
"""

import argparse
import json
import logging

from predict_patient_data.retrieve_output_data import retrieve_output_data


def getargs():
    """
    Define and parse command line arguments
    :return: command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file",
        required=True,
        type=argparse.FileType("r"),
        dest="input_file",
        metavar="<input data file>",
        help="Generated datasheet file (with patient adherence and follow-up persistence)",
    )
    parser.add_argument(
        "-p", "--predictions",
        required=True,
        type=argparse.FileType("r"),
        dest="predictions_file",
        metavar="<input predictions file>",
        help="Generated predictions from the LLM",
    )
    return parser.parse_args()


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    args = getargs()
    logger.info("Arguments parsed successfully.")

    # Retrieve the output data as a dataframe with unused columns filtered out
    output_data = retrieve_output_data(args.input_file)
    logger.info("Output file loaded successfully.")

    # Retrieve the predictions file
    predictions_data = json(args.predictions_file)
    logger.info("Predictions file loaded successfully.")

    # Evaluate predictions
    #output_data["result"] = results
    #output_data.
