"""
Compare the predicted values with the real values with F1 and accuracy criteria if the values match
"""

import argparse
import json
import logging
import re

from sklearn.metrics import f1_score, accuracy_score

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
    # output_data = output_data.to_dict(orient="records")
    logger.info("Output file loaded successfully.")

    # Extract useful data
    expected_adherence = output_data["ADERENZA"].to_list()
    expected_follow_up_persistence = output_data["Persistenza di Follow-up"].to_list()

    # Retrieve the predictions file
    predictions_data = json.load(args.predictions_file)
    logger.info("Predictions file loaded successfully.")

    # Collect adherence and follow-up persistence for each patient
    predicted_adherence = []
    predicted_follow_up_persistence = []

    # Evaluate predictions
    pattern = re.compile(r"adherence: (\d+)\n\s+persistence follow-up: (\d+)")
    for i, prediction in enumerate(predictions_data):
        match = pattern.match(prediction)
        if match:
            predicted_adherence.append(int(match[1]))
            predicted_follow_up_persistence.append(int(match[2]))

        else:
            expected_adherence.pop(i)
            expected_follow_up_persistence.pop(i)

    adherence_f1_score = f1_score(expected_adherence, predicted_adherence, average="macro")
    adherence_accuracy_score = accuracy_score(expected_adherence, predicted_adherence)
    print("Adherence")
    print("F1 score: ", round(adherence_f1_score, 3))
    print("Accuracy score: ", round(adherence_accuracy_score, 3))

    print()

    follow_up_persistence_f1_score = f1_score(expected_follow_up_persistence, predicted_follow_up_persistence, average="macro")
    follow_up_persistence_accuracy_score = accuracy_score(expected_follow_up_persistence, predicted_follow_up_persistence)
    print("Follow-up persistence")
    print("F1 score: ", round(follow_up_persistence_f1_score, 3))
    print("Accuracy score: ", round(follow_up_persistence_accuracy_score, 3))
