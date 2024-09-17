"""
Tokenize the prompt with the provided tokenizer
"""


def tokenize_input(tokenizer, prompt):
    """
    Tokenize the prompt with the provided tokenizer
    :param tokenizer: tokenizer
    :param prompt: prompt
    :return: tokenized prompt
    """
    result = tokenizer(
        prompt,
        truncation=True,
        max_length=512,
        padding="max_length",
    )
    result["labels"] = result["input_ids"].copy()
    return result
