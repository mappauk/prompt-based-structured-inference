import sys
import src.helpers.scoring.mf_scoring as mf_scoring
from src.learning.models.logistic_regression import LogisticRegression
from src.learning.loss.structured_hinge_loss import StructuredHingeLoss
from src.learning.loss.joint_cross_entropy_loss import JointCrossEntropyLoss
from src.learning.loss.early_stopping import EarlyStopping
import torch
import src.helpers.loaders.model_loader as model_loader
from peft import LoraConfig, get_peft_model
from transformers import TrainingArguments, EarlyStoppingCallback, IntervalStrategy, Trainer
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM, SFTConfig
from src.helpers.loaders.mf_training_data_loader import get_training_data
from datasets import Dataset
import wandb

def compute_metrics():
    return None


def main():
    data_input_path = sys.argv[1]
    output_path = sys.argv[2]
    device_type='cuda'
    llama_response_format = '<|start_header_id|>assistant<|end_header_id|>'
    wandb.login(key='')
    ### Lora Hyperparams ###
    lora_alpha = 32 # alpha to try: 32, 64, 128 (match rank)
    rank = 32  # ranks to try: 32, 64, 128
    lora_dropout = 0.05
    modules = 'all-linear' # modules = ['q_proj','k_proj','v_proj','dense']

    ### Training Argument Hyperparams ###
    learning_rate = 2e-5
    batch_size = 8

    model, tokenizer = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    training_splits, ids_to_prompts = get_training_data(data_input_path, data_input_path + 'training_splits.json', tokenizer)
    
    lora_config = LoraConfig(
        bias="none",
        lora_alpha=lora_alpha,
        target_modules=modules,
        task_type='CAUSAL_LM',
        lora_dropout=lora_dropout,
        r=rank,
    )
    for i in range(len(training_splits)):
        model, tokenizer = model_loader.load_test_model(device_type)
        peft_model = get_peft_model(model, lora_config)
        # training arguments
        print(output_path + f'\\{i}\\')
        training_args = SFTConfig(
            output_dir=output_path + f'\\{i}\\',
            eval_strategy=IntervalStrategy.STEPS,
            eval_steps = 200,
            save_steps = 200,
            num_train_epochs=100,
            dataset_text_field='text',
            max_seq_length=8192,
            per_device_eval_batch_size=batch_size,
            per_device_train_batch_size=batch_size,
            save_total_limit = 5,
            learning_rate=learning_rate,
            load_best_model_at_end=True,
            metric_for_best_model='eval_loss',
            push_to_hub=False,
            packing=False,
            eval_packing=None
        )
        '''
        training_args = TrainingArguments(
            output_dir=output_path + f'/{i}/',
            eval_strategy=IntervalStrategy.STEPS,
            eval_steps = 200,
            num_train_epochs=100,
            per_device_eval_batch_size=batch_size,
            per_device_train_batch_size=batch_size,
            save_total_limit = 5,
            learning_rate=learning_rate,
            load_best_model_at_end=True,
            metric_for_best_model='eval_loss',
            push_to_hub=False
        )
        '''
        # get training and eval data
        train_ids = training_splits[i]['train']
        eval_ids = training_splits[i]['val']
        
        train_data = []
        eval_data = []
        for id in train_ids:
            train_data.extend(ids_to_prompts[id])
        for id in eval_ids:
            eval_data.extend(ids_to_prompts[id])
        train_dataset = Dataset.from_dict({
            "text": train_data
        })
        eval_dataset = Dataset.from_dict({
            "text": eval_data
        })
        collator = DataCollatorForCompletionOnlyLM(response_template=tokenizer.encode(llama_response_format, add_special_tokens=False)[2:], tokenizer=tokenizer)
        '''
        trainer = Trainer(
            model=peft_model,
            args=training_args,
            compute_metrics=compute_metrics,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=collator,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=5)]
        )
        '''
        trainer = SFTTrainer(
            model=peft_model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=collator,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
        )
        trainer.train()
        trainer.save_model(output_path + f'\\{i}\\final_model\\')

if __name__ == "__main__":
    main()