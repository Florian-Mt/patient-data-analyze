"""
Load the tokenizer from the provided model id
"""

from transformers import AutoTokenizer


def load_tokenizer(base_model_id: str, local_files_only = False):
    """
    Load the tokenizer from the provided model id
    :param base_model_id: model id
    :param local_files_only: load tokenizer from local model (defaults to False)
    :return: model's tokenizer
    """
    tokenizer = AutoTokenizer.from_pretrained(
        base_model_id,
        padding_side="right",
        add_eos_token=True,
        local_files_only=local_files_only,
    )
    tokenizer.pad_token = tokenizer.eos_token

    return tokenizer
