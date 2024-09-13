from datetime import datetime
import os

from datasets import Dataset
from peft import LoraConfig, get_peft_model
from peft import prepare_model_for_kbit_training
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

from predict_patient_data.generate_prompt import generate_prompt
from predict_patient_data.print_trainable_parameters import print_trainable_parameters
from predict_patient_data.retrieve_output_data import retrieve_output_data
from predict_patient_data.tokenize_input import tokenize_input

input_file = "output_global.csv"

if __name__ == "__main__":
    # Retrieve the output data as a dataframe with unused columns filtered out
    output_data = retrieve_output_data(input_file)

    # Convert the pandas dataframe into a pytorch tensor
    dataset = Dataset.from_pandas(output_data)

    # Split the dataset into train and eval datasets
    train_test_split = dataset.train_test_split(test_size=0.2)
    train_dataset = train_test_split["train"]
    eval_dataset = train_test_split["test"]

    # Then create and configure the tokenizer
    base_model_id = "mistralai/Mistral-7B-v0.1"
    tokenizer = AutoTokenizer.from_pretrained(
        base_model_id,
        padding_side="right",
        add_eos_token=True,
    )
    tokenizer.pad_token = tokenizer.eos_token

    # Prepare our data for the fine-tuning
    generate_and_tokenize_prompt = lambda patient: tokenize_input(tokenizer, generate_prompt(patient))
    tokenized_train_dataset = train_dataset.map(generate_and_tokenize_prompt)
    tokenized_eval_dataset = eval_dataset.map(generate_and_tokenize_prompt)
    print(tokenized_train_dataset[0]["input_ids"])

    # And the model
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    model = AutoModelForCausalLM.from_pretrained(base_model_id, quantization_config=bnb_config)

    # Operate the fine-tuning
    model.gradient_checkpointing_enable()
    model = prepare_model_for_kbit_training(model)

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
    print_trainable_parameters(model)

    # Uncomment to apply the accelerator
    # model = accelerator.prepare_model(model)

    if torch.cuda.device_count() > 1: # If more than 1 GPU
        model.is_parallelizable = True
        model.model_parallel = True

    run_name = base_model_id + "-" + "finetuned"
    output_dir = os.path.join(os.getcwd(), run_name)

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
