"""
Print information on the trainable parameters of the model
"""


def print_trainable_parameters(model):
    """
    Print information on the trainable parameters of the model
    :param model: model
    """
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()

    trainable_ratio = trainable_params / all_param * 100
    print(f"trainable params: {trainable_params} || all params: {all_param} || trainable%: {trainable_ratio}")
    print(model)
