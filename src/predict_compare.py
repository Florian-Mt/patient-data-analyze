"""
Compute adherence and follow-up persistence for each patient in the base file
Then predict the same values via LLM and compare with F1 and accuracy criterias if the values match
"""

import argparse
import logging

from datasets import Dataset
from peft import PeftModel
import torch

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

    # Load the model from the base model ID and load last PEFT checkpoint
    model = load_model_config(BASE_MODEL_ID)
    model = PeftModel.from_pretrained(model, FINETUNED_MODEL_ID)

    # Load the tokenizer
    tokenizer = load_tokenizer(FINETUNED_MODEL_ID, local_files_only=True)

    # Prepare the data for predictions
    inputs = dataset.map(generate_prediction_prompt)
    logger.info("Dataset tokenized successfully.")

    # Make predictions with the fine-tuned model
    results = []
    for input in inputs:
        #model_input = tokenizer(eval_prompt, return_tensors="pt").to("cuda")
        model_input = tokenizer(input, return_tensors="pt").to("cuda")
        model.eval()
        with torch.no_grad():
            result = tokenizer.decode(model.generate(**model_input, max_new_tokens=512)[0], skip_special_tokens=True)
        result.append(result)

    # Evaluate predictions
    #output_data["result"] = results
    #output_data.
