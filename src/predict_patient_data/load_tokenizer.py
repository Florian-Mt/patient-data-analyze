"""
Load the tokenizer from the provided model id
"""

from transformers import AutoTokenizer


def load_tokenizer(base_model_id: str):
    """
    Load the tokenizer from the provided model id
    :param base_model_id: model id
    :return: model's tokenizer
    """
    tokenizer = AutoTokenizer.from_pretrained(
        base_model_id,
        padding_side="right",
        add_eos_token=True,
    )
    tokenizer.pad_token = tokenizer.eos_token

    return tokenizer
