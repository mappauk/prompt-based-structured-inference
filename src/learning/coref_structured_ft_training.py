import sys
import src.helpers.scoring.coref_scoring as coref_scoring
import src.helpers.prompting.coref_prompt_constants as constants
from src.learning.loss.coref_structured_hinge_loss import CorefStructuredHingeLoss
from src.learning.loss.early_stopping import EarlyStopping
import torch
import src.helpers.scoring.scoring as scoring
import src.helpers.loaders.model_loader as model_loader
from peft import LoraConfig, get_peft_model
from peft import PeftModel
import pandas as pd
import numpy as np

tindex = 1904
findex = 3934

def checkpoint(models, folder):
    for i in range(len(models)):
        torch.save(models[i].state_dict(), folder + f'model_{i}.pth')

def load_checkpoint(models, folder):
    for i in range(len(models)):
        models[i].load_state_dict(torch.load(folder + f'model_{i}.pth'))

def get_tf_prompts(rule_groundings, system_prompt, example_prompt, features, labels, tokenizer):
    prompts = []
    for index, row in rule_groundings.iterrows():
        dict = {}
        for feature in features:
            dict[feature] = row[feature]
        for label in labels:
            dict['label'] = label
            formatted_example_prompt = example_prompt.format(**dict)
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": formatted_example_prompt
                }
            ]
            prompts.append(tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
    return prompts

def get_mc_prompts(rule_groundings, system_prompt, example_prompt, features, tokenizer):
    prompts = []
    for index, row in rule_groundings.iterrows():
        dict = {}
        for feature in features:
            dict[feature] = row[feature]
        formatted_example_prompt = example_prompt.format(**dict)
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": formatted_example_prompt
            }
        ]
        prompts.append(tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
    return prompts


def get_scored_rule_groundings_tf(batch, system_prompt, example_prompt, features, labels, llm_batch_size, device_type, model, tokenizer):
    # remove in prod model
    #model_2, tokenizer_2 = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    prompts = get_tf_prompts(
        batch, 
        system_prompt, 
        example_prompt, 
        features, 
        labels,
        #tokenizer_2,
        tokenizer
    )
    scores = []
    for i in range(0, len(prompts), llm_batch_size):
        curr_prompts = tokenizer(prompts[i: min(i + llm_batch_size, len(prompts))], padding=True, return_tensors='pt').to(device_type)
        outputs = model(**curr_prompts)
        tf_logits = torch.flatten(outputs.logits[:, -1, [tindex, findex]])
        scores.append(tf_logits)
    scores = torch.stack(scores, dim=0)
    scores = torch.nn.functional.softmax(scores, dim=1)
    scores = scores[:, 0]
    scores = torch.reshape(scores, (batch.shape[0], len(labels)))
    scores_norm = scores.sum(dim=1)
    scores = scores/scores_norm.unsqueeze(-1)
    return scores

def get_scored_rule_groundings_mc(batch, system_prompt, example_prompt, features, llm_batch_size, device_type, model, tokenizer, choices):
    if batch.shape[0] == 0:
        return None
    # remove in prod model
    #model_2, tokenizer_2 = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    prompts = get_mc_prompts(
        batch, 
        system_prompt, 
        example_prompt, 
        features, 
        #tokenizer_2,
        tokenizer
    )
    choice_token_indicies = []
    for choice in choices:
        choice_token_indicies.append(tokenizer.encode(choice)[1])
    scores = []
    for i in range(0, len(prompts), llm_batch_size):
        curr_prompts = tokenizer(prompts[i: min(i + llm_batch_size, len(prompts))], padding=True, return_tensors='pt').to(device_type)
        outputs = model(**curr_prompts)
        mc_logits = torch.flatten(outputs.logits[:, -1, [choice_token_indicies]])
        scores.append(mc_logits)
    scores = torch.stack(scores, dim=0)
    scores = torch.nn.functional.softmax(scores, dim=1)
    return scores

def eval(
    rules,
    constraints,
    llm_model,
    tokenizer,
    batched_val_groundings,
    llm_batch_size,
    device_type,
    structured_hinge_loss,
    val_step,
    rule_type
):
    # evaluate on validation set
    print(f'####################### Model Performance (Val) Val Step: {val_step} #######################')
    # set models to eval
    llm_model.eval()

    with torch.no_grad():
        # scores output
        rule_one_batch_scores_list = []

        #grounding lists
        rule_one_grounding_list = []

        for val_batch in batched_val_groundings:
            # rule one scoring
            if rule_type == 'tf':
                rule_one_batch_scores = get_scored_rule_groundings_tf(
                    val_batch['rule_one'],
                    constants.COREF_TF_SYSTEM_PROMPT,
                    constants.COREF_TF_PROMPT_EXAMPLE,
                    ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
                    ['coreferent', 'distinct'],
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer
                )
            elif rule_type == 'mc':
                rule_one_batch_scores = get_scored_rule_groundings_mc(
                    val_batch['rule_one'],
                    constants.COREF_MC_SYSTEM_PROMPT,
                    constants.COREF_MC_PROMPT_EXAMPLE,
                    ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer,
                    constants.COREF_CHOICES
                )

            rule_one_batch_scores_list.append(rule_one_batch_scores.cpu())
            rule_one_grounding_list.append(val_batch['rule_one'])

        val_groundings = {}
        val_groundings['rule_one'] = pd.concat(rule_one_grounding_list, axis=0)

        val_outputs = {
            'rule_one': torch.vstack(rule_one_batch_scores_list),
        }
        val_loss = structured_hinge_loss(val_groundings, val_outputs)
        macro_f1  = coref_scoring.model_eval(rules, constraints, val_groundings, outputs=val_outputs, softmax_enabled=False)
        
        # set models to train
        llm_model.train()
        return val_loss, macro_f1


def training_loop(
        rules, 
        custom_rule_constraints,
        tokenizer,
        llm_model,
        llm_learning_rate,
        batched_train_groundings,
        llm_batch_size,
        device_type,
        batched_val_groundings,
        output_path,
        gradient_accumulation_steps,
        eval_steps,
        rule_type):
    # hyper params
    epochs = 100000000
    num_solutions = 1
    best_val_f1 = 0
    
    llm_model_optimizer = torch.optim.Adam(llm_model.parameters(), lr=llm_learning_rate)

    # loss functions and early stopping definitions
    structured_hinge_loss = CorefStructuredHingeLoss(rules, custom_rule_constraints, num_solutions, softmax_enabled=False)
    structured_hinge_early_stopping = EarlyStopping(5, 0)

    # set models to train
    llm_model.train()

    for epoch in range(epochs):
        batch_losses = []
        for i in range(len(batched_train_groundings)):
            print(f"############ epoch {epoch}, batch: {i} ############")
            batch = batched_train_groundings[i]
            # rule one scoring
            if rule_type == 'tf':
                rule_one_batch_scores = get_scored_rule_groundings_tf(
                    batch['rule_one'],
                    constants.COREF_TF_SYSTEM_PROMPT,
                    constants.COREF_TF_PROMPT_EXAMPLE,
                    ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
                    ['coreferent', 'distinct'],
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer
                )
            elif rule_type == 'mc':
                rule_one_batch_scores = get_scored_rule_groundings_mc(
                    batch['rule_one'],
                    constants.COREF_MC_SYSTEM_PROMPT,
                    constants.COREF_MC_PROMPT_EXAMPLE,
                    ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer,
                    constants.COREF_CHOICES
                )
            # get predictions
            outputs = {
                'rule_one': rule_one_batch_scores,
            }

            loss = structured_hinge_loss(batch, outputs)
            print(loss)
            batch_losses.append(loss.item())
            loss.backward()

            # accumulate gradient
            if (i + 1) % gradient_accumulation_steps == 0:
                # update weights
                llm_model_optimizer.step()
                # zero gradients
                llm_model_optimizer.zero_grad()
                print(f"Training Loss (Batch): {sum(batch_losses)/len(batch_losses)}")

            # eval model
            if (i + 1) % eval_steps == 0:
                eval_step = int((i + 1)/ eval_steps)
                val_loss, val_f1 = eval(
                    rules, 
                    custom_rule_constraints,
                    llm_model,
                    tokenizer,
                    batched_val_groundings,
                    llm_batch_size,
                    device_type,
                    structured_hinge_loss,
                    eval_step,
                    rule_type
                )
                print(f'Validation Loss: {val_loss}')
                print('\n\n\n')

                if val_f1 > best_val_f1:
                    llm_model.save_pretrained(output_path)
                    best_val_f1 = val_f1
                structured_hinge_early_stopping.check_early_stopping(val_f1, eval_step)
                if not structured_hinge_early_stopping.training_flag:
                    return
        print(f"Training Loss (Epoch): {sum(batch_losses)/len(batch_losses)}")



def main():
    # inputs
    rule_type = sys.argv[1]
    sft_path = sys.argv[2]
    new_model_checkpoint_path = sys.argv[3]
    device_type = 'cuda'

    # hyperparams
    llm_learning_rate = 2e-6
    llm_batch_size = 1
    gradient_accumulation_steps = 16
    use_log_reg = True
    batch_size = 1
    eval_steps = 80
    eval_batch_size = 4

    data_input_paths = {
        'train': 'C:\\src\\MoralDistillation\\data\\coref\\GENIA_MedCo_coreference_corpus_1.0\\train',
        'val': 'C:\\src\\MoralDistillation\\data\\coref\\GENIA_MedCo_coreference_corpus_1.0\\dev',
    }

    grounding_paths = {
        'train': 'C:\\Users\\mpauk\\Downloads\\llama_genia_mc\\train',
        'val': 'C:\\Users\\mpauk\\Downloads\\llama_genia_mc\\dev',
    }


    # load training data
    rules = coref_scoring.get_rule_info()
    constraints = coref_scoring.get_constraints()
    train_groundings = coref_scoring.get_training_groundings(data_input_paths, grounding_paths, rule_type, batch_size, batch_val_groundings=True, val_batch_size=eval_batch_size)

    # load llm model
    model, tokenizer = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    model = PeftModel.from_pretrained(model, sft_path, is_trainable=True).to(device_type)
    #model = model.merge_and_unload()

    batched_train_groundings = train_groundings['train']
    val_groundings = train_groundings['val']
    output_path = new_model_checkpoint_path

    training_loop(
        rules,
        constraints,
        tokenizer,
        model,
        llm_learning_rate,
        batched_train_groundings,
        llm_batch_size,
        device_type,
        val_groundings,
        output_path,
        use_log_reg,
        gradient_accumulation_steps,
        eval_steps,
        rule_type
    )

if __name__ == "__main__":
    main()