# Patient data analyze

This project aims to determine if an LLM can predict data on patients' treatment.

## Install

* Use a recent version of Python (3.12 recommended)
* Create a Python virtual environment: `python -m venv venv`
* Install required dependencies: `pip install .`

## Computing data on patients

* Run `python generate_datasheets.py -f <YOUR_DATA_FILE.xlsx>`
  * For example, with the provided training file: `python generate_datasheets.py -f "./data/V3 estrazione dati antiemicranici al 9-5-24 con PDD.xlsx"`

The generated datasheets will be in the `output` folder by default. Use `-o <path>` or `--output-dir <path>` to change output directory. The path is created if necessary.

Use `--only-global` to only output the datasheet for all drugs.
