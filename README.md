# Patient data analyze

This project aims to determine if an LLM can predict data on patients' treatment.

## Install

* Use a recent version of Python (3.12 recommended)
* Create a Python virtual environment: `python -m venv venv`
* Activate your virtual environment: `source ./venv/bin/activate`

## Computing data on patients

* Install required dependencies: `pip install ".[compute]"` (or `python -m pip install ".[computation]"`)
* `python src/generate_datasheets.py -f <YOUR_DATA_FILE.xlsx> [-o <output_directory>]`
  * For example, with the provided training file: `python src/generate_datasheets.py -f "./data/V3 estrazione dati antiemicranici al 9-5-24 con PDD.xlsx"`

The generated datasheets will be in the `output` folder by default. Use `-o <path>` or `--output-dir <path>` to change output directory. The path is created if necessary.

Use `-g` (`--only-global`) to only output the datasheet for all drugs.

## Fine-tuning the model

A fine-tuned version of Mistral 7B has been trained on Google Colab, see `predict_patient_data/llm_finetuning.ipynb`.

To run it again, upload the `output_global.csv` to your Drive home directory and add a HuggingFace personal token as a *secret* named `HF_TOKEN`, with notebook access checked.

An equivalent non-Colab version is available (GPU required):

* Install required dependencies: `pip install ".[llm]"`
* Provide `HF_TOKEN` as an environment variable
  * For example with Bash: `export HF_TOKEN=<your_token>`
  * Or as an IDE environment configuration
* Run `python src/finetune_llm.py -f <input_file> [-o <output_directory>]`
  * For example, with the previously generated output file: `python src/finetune_llm.py -f output/output_global.csv`

## Using the fine-tuned model to make predictions

* Provide `HF_TOKEN` as an environment variable (see instructions in previous section)
* Provide the fine-tuned model in `mistralai/Mistral-7B-v0.1-patient-data-analyze/`
* Run `python src/predict_with_llm.py -f <input_file> [-o <output_file>]`
  * For example, with the previously generated output file: `python src/predict_with_llm.py -f output/output_global.csv -o output/predictions.json`

## Evaluate the predictions

* Install required dependencies `pip install ".[compare]"`
* Run `python src/compare_results.py -f <input_file> -p <predictions_file>`
  * For example, with the previously generated output and result files: `python src/compare_results.py -f output/output_global.csv -p output/predictions.json`

## Code quality commands

First run `pip install ".[quality]"`.

* `black --diff .`
* `flake8 --exclude=venv --max-line-length=120 .`
* `isort --check --diff .`
* `MYPYPATH=src mypy .`
* `pylint src`

Default configurations are provided in `pyproject.toml` for most of those tools.
