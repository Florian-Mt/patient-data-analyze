"""
Load model and create configuration
"""

import torch
from peft import prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, BitsAndBytesConfig


def load_model_config(base_model_id: str):
    """
    Load model and create configuration
    :param base_model_id: model id
    :return: configured model
    """

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    model = AutoModelForCausalLM.from_pretrained(base_model_id, quantization_config=bnb_config)

    model.gradient_checkpointing_enable()
    model = prepare_model_for_kbit_training(model)

    return model
