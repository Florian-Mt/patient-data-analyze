"""
Add accelerator to the provided model
"""

from accelerate import Accelerator, FullyShardedDataParallelPlugin
from torch.distributed.fsdp.fully_sharded_data_parallel import FullOptimStateDictConfig, FullStateDictConfig


def load_accelerator(model):
    """
    Add accelerator to the provided model
    :param model: model
    :return: model with accelerator added
    """

    fsdp_plugin = FullyShardedDataParallelPlugin(
        state_dict_config=FullStateDictConfig(offload_to_cpu=True, rank0_only=False),
        optim_state_dict_config=FullOptimStateDictConfig(offload_to_cpu=True, rank0_only=False),
    )

    accelerator = Accelerator(fsdp_plugin=fsdp_plugin)

    # Apply the accelerator
    return accelerator.prepare_model(model)
