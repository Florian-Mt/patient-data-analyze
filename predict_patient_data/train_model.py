from datetime import datetime
import os

from datasets import Dataset
from transformers import DataCollatorForLanguageModeling, Trainer, TrainingArguments
import torch


def train_model(
    base_model_id: str,
    model,
    tokenizer,
    tokenized_train_dataset: Dataset,
    tokenized_eval_dataset: Dataset,
    output_directory: str,
):
    if torch.cuda.device_count() > 1: # If more than 1 GPU
        model.is_parallelizable = True
        model.model_parallel = True

    run_name = base_model_id + "-" + "finetuned"
    output_dir = os.path.join(output_directory, run_name)

    tokenizer.pad_token = tokenizer.eos_token

    trainer = Trainer(
        model=model,
        train_dataset=tokenized_train_dataset,
        eval_dataset=tokenized_eval_dataset,
        args=TrainingArguments(
            output_dir=output_dir,
            warmup_steps=5,
            per_device_train_batch_size=4,
            gradient_checkpointing=True,
            gradient_accumulation_steps=4,
            max_steps=750,
            learning_rate=2.5e-4,
            logging_steps=50,
            # bf16=True,
            optim="paged_adamw_8bit",
            logging_dir="./logs",  # Directory for storing logs
            save_strategy="steps",  # Save the model checkpoint every logging step
            save_steps=50,  # Save checkpoints every 50 steps
            eval_strategy="steps",  # Evaluate the model every logging step
            eval_steps=50,  # Evaluate and save checkpoints every 50 steps
            do_eval=True,  # Perform evaluation at the end of training
            run_name=f"{run_name}-{datetime.now().strftime('%Y-%m-%d-%H-%M')}",  # Name of the W&B run (optional)
        ),
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )

    model.config.use_cache = False  # silence the warnings. Please re-enable for inference!
    trainer.train(resume_from_checkpoint=True)

    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
