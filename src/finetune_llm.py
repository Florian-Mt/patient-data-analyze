"""
Fine-tune a LLM on patient's data
"""

import argparse
import logging
import os

from datasets import Dataset

from predict_patient_data.generate_prompt import generate_prompt
from predict_patient_data.load_accelerator import load_accelerator
from predict_patient_data.load_model_config import load_model_config
from predict_patient_data.load_tokenizer import load_tokenizer
from predict_patient_data.print_trainable_parameters import print_trainable_parameters
from predict_patient_data.retrieve_output_data import retrieve_output_data
from predict_patient_data.tokenize_input import tokenize_input
from predict_patient_data.train_model import train_model
from utils.dir_path import dir_path

BASE_MODEL_ID = "mistralai/Mistral-7B-v0.1"


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
        help="Number of individuals in each population",
    )
    parser.add_argument(
        "-o", "--output-dir",
        required=False,
        type=dir_path,
        default=os.path.join(os.getcwd(), "trained_llm"),
        dest="output_directory",
        metavar="<output directory>",
        help="Output directory to save progression steps and final model",
    )
    return parser.parse_args()


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # Based on https://colab.research.google.com/drive/1EbjBoSCTLW23b-9Ls0p5XiifOsTWuVul
    args = getargs()
    logger.info("Arguments parsed successfully.")

    # Retrieve the output data as a dataframe with unused columns filtered out
    output_data = retrieve_output_data(args.input_file)
    logger.info("Output file loaded successfully.")

    # Convert the pandas dataframe into a pytorch tensor
    dataset = Dataset.from_pandas(output_data)

    # Split the dataset into train and eval datasets
    train_test_split = dataset.train_test_split(test_size=0.2)
    train_dataset = train_test_split["train"]
    eval_dataset = train_test_split["test"]
    logger.info("Train and eval datasets created successfully.")

    # Load the tokenizer
    tokenizer = load_tokenizer(BASE_MODEL_ID)

    # Prepare the data for the fine-tuning
    generate_and_tokenize_prompt = lambda patient: tokenize_input(tokenizer, generate_prompt(patient))

    tokenized_train_dataset = train_dataset.map(generate_and_tokenize_prompt)
    tokenized_eval_dataset = eval_dataset.map(generate_and_tokenize_prompt)
    logger.info("Train and eval datasets tokenized successfully.")

    # Load the model from the base model ID
    model = load_model_config(BASE_MODEL_ID)
    print_trainable_parameters(model)

    # Apply the accelerator
    model = load_accelerator(model)

    # Operate the fine-tuning
    train_model(BASE_MODEL_ID, model, tokenizer, tokenized_train_dataset, tokenized_eval_dataset, args.output_directory)
    logger.info("Base model fine-tuned successfully.")
