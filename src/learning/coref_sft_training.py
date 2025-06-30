import sys
import src.helpers.loaders.model_loader as model_loader
from peft import LoraConfig, get_peft_model
from transformers import TrainingArguments, EarlyStoppingCallback, IntervalStrategy, Trainer
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM, SFTConfig
from src.helpers.loaders.coref_training_data_loader import get_training_data
from datasets import Dataset
import wandb
import numpy as np
import sklearn.metrics as sk
from transformers import AutoTokenizer


def main():
    data_input_path = sys.argv[1]
    val_data_input_path = sys.argv[2]
    rule_type = sys.argv[3]
    output_path = sys.argv[4]
    device_type='cuda:0'
    mistral_response_format = '[/INST]'
    llama_response_format = '<|start_header_id|>assistant<|end_header_id|>'
    wandb.login(key='')
    ### Lora Hyperparams ###
    lora_alpha = 256 # alpha to try: 32, 64, 128 (match rank)
    rank = 256  # ranks to try: 32, 64, 128
    lora_dropout = 0.05
    modules = 'all-linear' # modules = ['q_proj','k_proj','v_proj','dense']

    ### Training Argument Hyperparams ###
    learning_rate = 2e-5
    batch_size = 2

    model, tokenizer = model_loader.load_mistral_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    #model, tokenizer = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    training_prompts, validation_prompts = get_training_data(data_input_path, val_data_input_path, tokenizer, rule_type)

    lora_config = LoraConfig(
        bias="none",
        lora_alpha=lora_alpha,
        #target_modules=modules,
        task_type='CAUSAL_LM',
        lora_dropout=lora_dropout,
        r=rank,
    )

    model, tokenizer = model_loader.load_test_model(device_type)

    peft_model = get_peft_model(model, lora_config)
    # training arguments
    training_args = SFTConfig(
        output_dir=output_path,
        eval_strategy=IntervalStrategy.STEPS,
        eval_steps = 5,
        save_steps = 5,
        #eval_steps = 40,
        #save_steps = 40,
        num_train_epochs=10,
        dataset_text_field='text',
        max_seq_length=8192,
        per_device_eval_batch_size=batch_size,
        per_device_train_batch_size=batch_size,
        save_total_limit = 5,
        gradient_accumulation_steps=2,
        #gradient_accumulation_steps=8,
        learning_rate=learning_rate,
        load_best_model_at_end=True,
        metric_for_best_model='eval_loss',
        push_to_hub=False,
        packing=False,
        eval_packing=None
    )
    # get training and eval data
    train_dataset = Dataset.from_dict({
        "text": training_prompts
    })
    train_dataset = train_dataset.shuffle(seed=92)
    eval_dataset = Dataset.from_dict({
        "text": validation_prompts
    })
    eval_dataset = eval_dataset.shuffle(seed=92)
    collator = DataCollatorForCompletionOnlyLM(response_template=tokenizer.encode(mistral_response_format, add_special_tokens=False)[2:], tokenizer=tokenizer)
    trainer = SFTTrainer(
        model=peft_model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        #processing_class=tokenizer,
        data_collator=collator,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )
    trainer.train()
    trainer.save_model(output_path + f'\\final_model\\')

if __name__ == "__main__":
    main()