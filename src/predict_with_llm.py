"""
Predict adherence and follow-up persistence for each patient in the base file via LLM
"""

import argparse
import json
import logging
import os

import torch
from datasets import Dataset
from peft import PeftModel

from constants import BASE_MODEL_ID, FINETUNED_MODEL_ID
from predict_patient_data.generate_prediction_prompt import generate_prediction_prompt
from predict_patient_data.load_model_config import load_model_config
from predict_patient_data.load_tokenizer import load_tokenizer
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
        "-o", "--output",
        required=False,
        type=argparse.FileType("w"),
        default=os.path.join(os.getcwd(), "prediction_results.json"),
        dest="output_file",
        metavar="<output results file>",
        help="Predictions made by the LLM for each patient",
    )
    return parser.parse_args()


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # Based on https://colab.research.google.com/drive/1JrtztfW1qryP790WmAhvkRm3qh4n2Ae6
    args = getargs()
    logger.info("Arguments parsed successfully.")

    # Retrieve the output data as a dataframe with unused columns filtered out
    output_data = retrieve_output_data(args.input_file)
    logger.info("Output file loaded successfully.")

    # Convert the pandas dataframe into a pytorch tensor
    dataset = Dataset.from_pandas(output_data)

    # Load the model from the base model ID and the PEFT result
    model = load_model_config(BASE_MODEL_ID)
    model = PeftModel.from_pretrained(model, FINETUNED_MODEL_ID)

    # Load the tokenizer
    tokenizer = load_tokenizer(FINETUNED_MODEL_ID, local_files_only=True)
    logger.info("Model and tokenizer loaded successfully.")

    # Retrieve prediction results file
    try:
        data_file = open(args.output_file, "r", encoding="utf-8")
        results = json.loads(data_file.read())
        data_file.close()
    except FileNotFoundError:
        results = []

    # Make predictions with the fine-tuned model
    logger.info(f"{len(dataset)} patients to predict adherence and follow-up persistence.")
    logger.info(f"Skipping {len(results)} patients: prediction already done.")
    model.eval()
    with torch.no_grad():
        for i, patient in enumerate(dataset):
            if i < len(results):
                continue

            patient_input = generate_prediction_prompt(patient)
            model_input = tokenizer(patient_input, return_tensors="pt").to("cuda")
            result = tokenizer.decode(model.generate(**model_input, max_new_tokens=512)[0], skip_special_tokens=True)
            results.append(result)

            # Save this patient result
            with open(args.output_file, "w", encoding="utf-8") as json_file:
                print(json.dumps(results), file=json_file)
