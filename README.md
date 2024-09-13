# Patient data analyze

This project aims to determine if an LLM can predict data on patients' treatment.

## Install

* Use a recent version of Python (3.12 recommended)
* Create a Python virtual environment: `python -m venv venv`
* Install required dependencies: `pip install .` (or `python -m pip install .`)

## Computing data on patients

Run `python generate_datasheets.py -f <YOUR_DATA_FILE.xlsx>`. For example, with the provided training file: `python generate_datasheets.py -f "./data/V3 estrazione dati antiemicranici al 9-5-24 con PDD.xlsx"`

The generated datasheets will be in the `output` folder by default. Use `-o <path>` or `--output-dir <path>` to change output directory. The path is created if necessary.

Use `--only-global` to only output the datasheet for all drugs.

## Fine-tuning the model

A fine-tuned version of Mistral 7B has been trained on Google Colab, see `predict_patient_data/llm_finetuning.ipynb`.

To run it again, upload the `output_global.csv` to your Drive home directory and add a HuggingFace personal token as a *secret* named `HF_TOKEN`, with notebook access checked.

An equivalent non-Colab version is available (GPU required):

* Install required dependencies: `pip install .[llm]`
* Provide `HF_TOKEN` as an environment variable
  * For example with Bash: `export HF_TOKEN=<your_token>`
  * Or as an IDE environment configuration
* Run `python finetune_llm.py`
  * Output file required

## Using the fine-tuned model
