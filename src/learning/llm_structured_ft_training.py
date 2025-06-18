import sys
import src.helpers.scoring.mf_scoring as mf_scoring
import src.helpers.prompting.mf_prompt_constants as constants
from src.learning.models.logistic_regression import LogisticRegression
from src.learning.loss.mf_structured_hinge_loss import MFStructuredHingeLoss
from src.learning.loss.joint_cross_entropy_loss import JointCrossEntropyLoss
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
    enable_log_reg,
    foundation_model,
    foundation_model_w_context,
    role_model,
    role_model_w_context,
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
    if enable_log_reg:
        foundation_model.eval()
        foundation_model_w_context.eval()
        role_model.eval()
        role_model_w_context.eval()
    llm_model.eval()

    with torch.no_grad():
        # scores output
        rule_one_batch_scores_list = []
        rule_two_batch_scores_list = []
        rule_three_batch_scores_list = []
        rule_four_batch_scores_list = []

        #grounding lists
        rule_one_grounding_list = []
        rule_two_grounding_list = []
        rule_three_grounding_list= []
        rule_four_grounding_list = []

        for val_batch in batched_val_groundings:
            # rule one scoring
            if rule_type == 'tf':
                rule_one_batch_scores = get_scored_rule_groundings_tf(
                    val_batch['rule_one'],
                    constants.MF_TF_SYSTEM_PROMPT,
                    constants.MORAL_FOUNDATION_PROMPT_EXAMPLE_FORMAT,
                    ['Tweet'],
                    constants.MORAL_FOUNDATIONS,
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer
                )
            elif rule_type == 'mc':
                rule_one_batch_scores = get_scored_rule_groundings_mc(
                    val_batch['rule_one'],
                    constants.MF_MC_SYSTEM_PROMPT,
                    constants.MF_MC_EXAMPLE_FORMAT,
                    ['Tweet'],
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer,
                    constants.MF_MC_CHOICES
                )
            if enable_log_reg:
                with torch.autocast(device_type='cuda'):
                    rule_one_batch_scores = foundation_model(rule_one_batch_scores)
            rule_one_batch_scores_list.append(rule_one_batch_scores.cpu())
            rule_one_grounding_list.append(val_batch['rule_one'])

            # rule two scoring
            if rule_type == 'tf':
                rule_two_batch_scores = get_scored_rule_groundings_tf(
                    val_batch['rule_two'],
                    constants.MR_TF_SYSTEM_PROMPT,
                    constants.MORAL_ROLE_PROMPT_EXAMPLE_FORMAT,
                    ['Tweet', 'Entity'],
                    constants.MORAL_FOUNDATION_ROLE,
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer,
                )
            elif rule_type == 'mc':
                rule_two_batch_scores = get_scored_rule_groundings_mc(
                    val_batch['rule_two'],
                    constants.MR_MC_SYSTEM_PROMPT,
                    constants.MR_MC_EXAMPLE_FORMAT,
                    ['Tweet', 'Entity'],
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer,
                    constants.MR_MC_CHOICES
                )
            if enable_log_reg:
                with torch.autocast(device_type='cuda'):
                    rule_two_batch_scores = role_model(rule_two_batch_scores)
            rule_two_batch_scores_list.append(rule_two_batch_scores.cpu())
            rule_two_grounding_list.append(val_batch['rule_two'])

            # rule three scoring
            if rule_type == "tf":
                rule_three_batch_scores = get_scored_rule_groundings_tf(
                    val_batch['rule_three'],
                    constants.MF_TF_SYSTEM_PROMPT,
                    constants.MORAL_FOUNDATION_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT,
                    ['Tweet', 'Ideology', 'Topic'],
                    constants.MORAL_FOUNDATIONS,
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer
                )
            elif rule_type == 'mc':
                rule_three_batch_scores = get_scored_rule_groundings_mc(
                    val_batch['rule_three'],
                    constants.MF_MC_SYSTEM_PROMPT,
                    constants.MF_MC_EXAMPLE_FORMAT_WITH_FEATURES,
                    ['Tweet', 'Ideology', 'Topic'],
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer,
                    constants.MF_MC_CHOICES
                )
            if enable_log_reg:
                with torch.autocast(device_type='cuda'):
                    rule_three_batch_scores = foundation_model_w_context(rule_three_batch_scores)
            rule_three_batch_scores_list.append(rule_three_batch_scores.cpu())
            rule_three_grounding_list.append(val_batch['rule_three'])

            # rule four scoring
            if rule_type == 'tf':
                rule_four_batch_scores = get_scored_rule_groundings_tf(
                    val_batch['rule_four'],
                    constants.MR_TF_SYSTEM_PROMPT,
                    constants.MORAL_ROLE_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT,
                    ['Tweet', 'Entity', 'Topic', 'Ideology'],
                    constants.MORAL_FOUNDATION_ROLE,
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer
                )
            elif rule_type == 'mc':
                rule_four_batch_scores = get_scored_rule_groundings_mc(
                    val_batch['rule_four'],
                    constants.MR_MC_SYSTEM_PROMPT,
                    constants.MR_MC_EXAMPLE_FORMAT_WITH_FEATURES,
                    ['Tweet', 'Entity', 'Topic', 'Ideology'],
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer,
                    constants.MR_MC_CHOICES
                )
            if enable_log_reg:
                with torch.autocast(device_type='cuda'):
                    rule_four_batch_scores = role_model_w_context(rule_four_batch_scores)
            rule_four_batch_scores_list.append(rule_four_batch_scores.cpu())
            rule_four_grounding_list.append(val_batch['rule_four'])

        val_groundings = {}
        val_groundings['rule_one'] = pd.concat(rule_one_grounding_list, axis=0)
        val_groundings['rule_two'] = pd.concat(rule_two_grounding_list, axis=0)
        val_groundings['rule_three'] = pd.concat(rule_three_grounding_list, axis=0)
        val_groundings['rule_four'] = pd.concat(rule_four_grounding_list, axis=0)

        val_outputs = {
            'rule_one': torch.vstack(rule_one_batch_scores_list),
            'rule_two': torch.vstack(rule_two_batch_scores_list),
            'rule_three': torch.vstack(rule_three_batch_scores_list),
            'rule_four': torch.vstack(rule_four_batch_scores_list)
        }
        val_loss = structured_hinge_loss(val_groundings, val_outputs)
        mf_macro_f1, mf_micro_f1, mr_macro_f1, mr_micro_f1 = mf_scoring.model_eval(rules, constraints, val_groundings, outputs=val_outputs, softmax_enabled=enable_log_reg)
        
        # set models to train
        if enable_log_reg:
            foundation_model.train()
            foundation_model_w_context.train()
            role_model.train()
            role_model_w_context.train()
        llm_model.train()
        return val_loss, (mf_macro_f1 + mr_macro_f1)/2


def training_loop(
        rules, 
        custom_rule_constraints,
        tokenizer,
        llm_model,
        foundation_model, 
        foundation_model_w_context, 
        role_model, 
        role_model_w_context, 
        log_reg_learning_rate,
        llm_learning_rate,
        batched_train_groundings,
        llm_batch_size,
        device_type,
        batched_val_groundings,
        output_path,
        enable_log_reg,
        gradient_accumulation_steps,
        eval_steps,
        rule_type):
    # hyper params
    epochs = 100000000
    num_solutions = 1
    best_val_f1 = 0
    

    # optimizers
    if enable_log_reg:
        foundation_model_optimizer = torch.optim.Adam(foundation_model.parameters(), lr=log_reg_learning_rate)
        foundation_model_w_context_optimizer = torch.optim.Adam(foundation_model_w_context.parameters(), lr=log_reg_learning_rate)
        role_model_optimizer = torch.optim.Adam(role_model.parameters(), lr=log_reg_learning_rate)
        role_model_w_context_optimizer = torch.optim.Adam(role_model_w_context.parameters(), lr=log_reg_learning_rate)
    llm_model_optimizer = torch.optim.Adam(llm_model.parameters(), lr=llm_learning_rate)

    # loss functions and early stopping definitions
    structured_hinge_loss = MFStructuredHingeLoss(rules, custom_rule_constraints, num_solutions, softmax_enabled=enable_log_reg)
    structured_hinge_early_stopping = EarlyStopping(5, 0)

    # set models to train
    if enable_log_reg:
        foundation_model.train()
        foundation_model_w_context.train()
        role_model.train()
        role_model_w_context.train()
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
                    constants.MF_TF_SYSTEM_PROMPT,
                    constants.MORAL_FOUNDATION_PROMPT_EXAMPLE_FORMAT,
                    ['Tweet'],
                    constants.MORAL_FOUNDATIONS,
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer
                )
            elif rule_type == 'mc':
                rule_one_batch_scores = get_scored_rule_groundings_mc(
                    batch['rule_one'],
                    constants.MF_MC_SYSTEM_PROMPT,
                    constants.MF_MC_EXAMPLE_FORMAT,
                    ['Tweet'],
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer,
                    constants.MF_MC_CHOICES
                )
            # rule two scoring
            if rule_type == 'tf':
                rule_two_batch_scores = get_scored_rule_groundings_tf(
                    batch['rule_two'],
                    constants.MR_TF_SYSTEM_PROMPT,
                    constants.MORAL_ROLE_PROMPT_EXAMPLE_FORMAT,
                    ['Tweet', 'Entity'],
                    constants.MORAL_FOUNDATION_ROLE,
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer,
                )
            elif rule_type == 'mc':
                rule_two_batch_scores = get_scored_rule_groundings_mc(
                    batch['rule_two'],
                    constants.MR_MC_SYSTEM_PROMPT,
                    constants.MR_MC_EXAMPLE_FORMAT,
                    ['Tweet', 'Entity'],
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer,
                    constants.MR_MC_CHOICES
                )
            # rule three scoring
            if rule_type == "tf":
                rule_three_batch_scores = get_scored_rule_groundings_tf(
                    batch['rule_three'],
                    constants.MF_TF_SYSTEM_PROMPT,
                    constants.MORAL_FOUNDATION_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT,
                    ['Tweet', 'Ideology', 'Topic'],
                    constants.MORAL_FOUNDATIONS,
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer
                )
            elif rule_type == 'mc':
                rule_three_batch_scores = get_scored_rule_groundings_mc(
                    batch['rule_three'],
                    constants.MF_MC_SYSTEM_PROMPT,
                    constants.MF_MC_EXAMPLE_FORMAT_WITH_FEATURES,
                    ['Tweet', 'Ideology', 'Topic'],
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer,
                    constants.MF_MC_CHOICES
                )
            # rule four scoring
            if rule_type == 'tf':
                rule_four_batch_scores = get_scored_rule_groundings_tf(
                    batch['rule_four'],
                    constants.MR_TF_SYSTEM_PROMPT,
                    constants.MORAL_ROLE_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT,
                    ['Tweet', 'Entity', 'Topic', 'Ideology'],
                    constants.MORAL_FOUNDATION_ROLE,
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer
                )
            elif rule_type == 'mc':
                rule_four_batch_scores = get_scored_rule_groundings_mc(
                    batch['rule_four'],
                    constants.MR_MC_SYSTEM_PROMPT,
                    constants.MR_MC_EXAMPLE_FORMAT_WITH_FEATURES,
                    ['Tweet', 'Entity', 'Topic', 'Ideology'],
                    llm_batch_size,
                    device_type,
                    llm_model,
                    tokenizer,
                    constants.MR_MC_CHOICES
                )
            # get predictions
            if enable_log_reg:
                with torch.autocast(device_type='cuda'):
                    foundation_model_logits = foundation_model(rule_one_batch_scores)
                    foundation_model_w_context_logits = foundation_model_w_context(rule_three_batch_scores)
                    if rule_two_batch_scores != None:    
                        role_model_logits = role_model(rule_two_batch_scores)
                        role_model_w_context_logits = role_model_w_context(rule_four_batch_scores)    
                    else:
                        role_model_logits = rule_two_batch_scores
                        role_model_w_context_logits = rule_four_batch_scores             
            else:
                foundation_model_logits = rule_one_batch_scores
                foundation_model_w_context_logits = rule_three_batch_scores
                role_model_logits = rule_two_batch_scores
                role_model_w_context_logits = rule_four_batch_scores           
            
            outputs = {
                'rule_one': foundation_model_logits,
                'rule_two': role_model_logits,
                'rule_three': foundation_model_w_context_logits,
                'rule_four': role_model_w_context_logits
            }

            loss = structured_hinge_loss(batch, outputs)
            print(loss)
            batch_losses.append(loss.item())
            loss.backward()

            # accumulate gradient
            if (i + 1) % gradient_accumulation_steps == 0:
                # update weights
                if enable_log_reg:
                    foundation_model_optimizer.step()
                    foundation_model_w_context_optimizer.step()
                    role_model_optimizer.step()
                    role_model_w_context_optimizer.step()
                llm_model_optimizer.step()

                # zero gradients
                if enable_log_reg:
                    foundation_model_optimizer.zero_grad()
                    foundation_model_w_context_optimizer.zero_grad()
                    role_model_optimizer.zero_grad()
                    role_model_w_context_optimizer.zero_grad()
                llm_model_optimizer.zero_grad()
                print(f"Training Loss (Batch): {sum(batch_losses)/len(batch_losses)}")

            # eval model
            if (i + 1) % eval_steps == 0:
                eval_step = int((i + 1)/ eval_steps)
                val_loss, val_f1 = eval(
                    rules, 
                    custom_rule_constraints,
                    enable_log_reg,
                    foundation_model,
                    foundation_model_w_context,
                    role_model,
                    role_model_w_context,
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
                    if enable_log_reg:
                        checkpoint([foundation_model, foundation_model_w_context, role_model, role_model_w_context], output_path)
                    llm_model.save_pretrained(output_path)
                    best_val_f1 = val_f1
                structured_hinge_early_stopping.check_early_stopping(val_f1, eval_step)
                if not structured_hinge_early_stopping.training_flag:
                    return
        print(f"Training Loss (Epoch): {sum(batch_losses)/len(batch_losses)}")



def main():
    # inputs
    data_input_path = sys.argv[1]
    rule_groundings_path = sys.argv[2]
    logreg_checkpoint_path = sys.argv[3]
    rule_type = sys.argv[4]
    sft_path = sys.argv[5]
    new_model_checkpoint_path = sys.argv[6]
    device_type = 'cuda'

    # hyperparams
    logreg_learning_rate = 2e-6
    llm_learning_rate = 2e-6
    llm_batch_size = 1
    gradient_accumulation_steps = 16
    num_folds = 5
    use_log_reg = True
    batch_size = 1
    eval_steps = 80
    eval_batch_size = 4

    # load training data
    rule_names = ['rule_one', 'rule_two', 'rule_three', 'rule_four']
    rules = mf_scoring.get_rule_info()
    constraints = mf_scoring.get_mf_constraints(data_input_path)
    rule_groundings = mf_scoring.get_scored_groundings(rule_groundings_path, rule_names, rule_type)
    train_groundings = mf_scoring.get_training_groundings(rule_groundings, data_input_path, batch_size, True, eval_batch_size)

    for i in range(num_folds):
        # load log reg models
        foundation_model, foundation_model_w_context, role_model, role_model_w_context = None, None, None, None
        if use_log_reg:
            foundation_model = LogisticRegression(5, 5).to(device_type)
            foundation_model_w_context = LogisticRegression(5, 5).to(device_type)
            role_model = LogisticRegression(16, 16).to(device_type)
            role_model_w_context = LogisticRegression(16, 16).to(device_type)
            checkpoint_path = logreg_checkpoint_path + f'cross_validation_{i}_'
            load_checkpoint([foundation_model, foundation_model_w_context, role_model, role_model_w_context], checkpoint_path)    

        # load llm model
        model, tokenizer = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
        model = PeftModel.from_pretrained(model, sft_path + f'{i}-final-model/', is_trainable=True).to(device_type)
        #model = model.merge_and_unload()

        batched_train_groundings = train_groundings[i]['train']
        val_groundings = train_groundings[i]['val']
        output_path = new_model_checkpoint_path + f'{i}/'

        training_loop(
            rules,
            constraints,
            tokenizer,
            model,
            foundation_model,
            foundation_model_w_context,
            role_model,
            role_model_w_context,
            logreg_learning_rate,
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
        #return


if __name__ == "__main__":
    main()