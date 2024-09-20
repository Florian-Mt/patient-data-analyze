"""
Create PEFT config and attach to a model
"""

from peft import LoraConfig, get_peft_model


def load_peft_config(model):
    """
    Attach PEFT config to model
    :param model: model
    :return: PEFT-configured model
    """

    config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
            "lm_head",
        ],
        bias="none",
        lora_dropout=0.05,  # Conventional
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, config)

    return model
