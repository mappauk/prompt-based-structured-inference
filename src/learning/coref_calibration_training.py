import sys
import src.helpers.scoring.coref_scoring as coref_scoring
from src.learning.models.logistic_regression import LogisticRegression
from src.learning.loss.coref_structured_hinge_loss import CorefStructuredHingeLoss
from src.learning.loss.mf_structured_hinge_loss import MFStructuredHingeLoss

from src.learning.loss.cross_entropy_loss import CrossEntropyLoss
from src.learning.loss.early_stopping import EarlyStopping
import torch

def checkpoint(model, folder):
    torch.save(model.state_dict(), folder + f'model.pth')

def load_checkpoint(model, folder):
    model.load_state_dict(torch.load(folder + f'model.pth'))  

def training_loop(
        rules, 
        custom_rule_constraints, 
        model, 
        learning_rate,
        batched_train_groundings,
        val_groundings,
        output_path,
        optimized_hot_start,
        only_ce_loss,
        structured_alone,
        eval_steps):
    # hyper params
    epochs = 100000000
    num_solutions = 1
    best_f1 = 0
    
    # optimizers
    model_optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # loss functions and early stopping definitions
    joint_ce_loss = CrossEntropyLoss()
    structured_hinge_loss = CorefStructuredHingeLoss(rules, custom_rule_constraints, num_solutions)
    ce_only_early_stopping = EarlyStopping(20, 0, True)
    structured_hinge_early_stopping = EarlyStopping(10, 0, True)
    loaded_best_ce_model = False

    for epoch in range(epochs):
        if (not ce_only_early_stopping.training_flag and only_ce_loss) or not structured_hinge_early_stopping.training_flag:
            break
        batch_losses = []
        # set models to train
        model.train()


        print(f"############ epoch {epoch} ############")
        for i in range(len(batched_train_groundings)):
            use_structured_loss = (
                (optimized_hot_start and  not ce_only_early_stopping.training_flag) or
                structured_alone
            )
            if use_structured_loss and not loaded_best_ce_model and not structured_alone:
                load_checkpoint(model, output_path)
                loaded_best_ce_model = True
            batch = batched_train_groundings[i]

            # zero gradients
            model_optimizer.zero_grad()

            # get predictions
            model_logits = model(torch.tensor(batch['rule_one']['Score'].tolist()).unsqueeze(1))

            outputs = {
                'rule_one': model_logits,
            }

            loss = None
            if use_structured_loss:
                loss = structured_hinge_loss(batch, outputs)
            else:
                loss = joint_ce_loss(batch, outputs)
            loss.backward()
            # update weights
            model_optimizer.step()
            batch_losses.append(loss.item())

            if (i + 1) % eval_steps == 0:
                # Estimate the f1 score for the development set
                print(f"Training Loss: {sum(batch_losses)/len(batch_losses)}")
                # set models to eval
                model.eval()
                # evaluate on validation set
                print(f'####################### Model Performance (Val) epoch: {epoch} step: {i} #######################')
                with torch.no_grad():
                    val_outputs = {
                        'rule_one': model(torch.tensor(val_groundings['rule_one']['Score'].tolist()).unsqueeze(1)),
                    }
                    val_loss = None
                    if use_structured_loss:
                        #val_loss = structured_hinge_loss(val_groundings, val_outputs)
                        macro_f1 = coref_scoring.model_eval(rules, custom_rule_constraints, val_groundings, val_outputs)
                        structured_hinge_early_stopping.check_early_stopping(macro_f1, i)
                    else:
                        val_loss = joint_ce_loss(val_groundings, val_outputs)
                        macro_f1 = coref_scoring.model_eval(rules, custom_rule_constraints, val_groundings, val_outputs, inference_score=False)
                        if macro_f1 >= 0.5  or best_f1 >= 0.5: 
                            ce_only_early_stopping.check_early_stopping(macro_f1, i)
                        print(f'Validation Loss: {val_loss}')

                    should_update_best_loss = (
                        only_ce_loss or 
                        (optimized_hot_start and not ce_only_early_stopping.training_flag and structured_hinge_early_stopping.best_step != 0) or
                        structured_alone
                    )
                    if macro_f1 > best_f1:
                        checkpoint(model, output_path)
                        best_f1 = macro_f1

                    print('\n\n\n')

                    if (not ce_only_early_stopping.training_flag and only_ce_loss) or not structured_hinge_early_stopping.training_flag:
                        break
                model.train()

def main():
    rule_type = sys.argv[1]
    model_checkpoint_path = sys.argv[2]
    optimized_hot_start = True
    only_ce_loss = False
    batch_size = 32
    learning_rate = 0.01
    structured_alone = False
    eval_steps = 100

    train_groundings = []

    data_input_paths = {
        'train': 'C:\\src\\MoralDistillation\\data\\coref\\GENIA_MedCo_coreference_corpus_1.0\\train',
        'val': 'C:\\src\\MoralDistillation\\data\\coref\\GENIA_MedCo_coreference_corpus_1.0\\dev'
    }

    grounding_paths = {
        'train': 'C:\\Users\\mpauk\\Downloads\\mistral_genia_mc_sft_train\\',
        'val': 'C:\\Users\\mpauk\\Downloads\\mistral_genia_mc_sft_dev\\'
    }

    train_groundings = coref_scoring.get_training_groundings(data_input_paths, grounding_paths, rule_type, batch_size, document_batching=True)
    rules = coref_scoring.get_rule_info()
    constraints = coref_scoring.get_constraints()
    # models
    model = LogisticRegression(1, 1)
    batched_train_groundings = train_groundings['train']
    val_groundings = train_groundings['val']
    output_path = model_checkpoint_path + f'log_reg_'
    training_loop(
        rules,
        constraints,
        model,
        learning_rate,
        batched_train_groundings,
        val_groundings,
        output_path,
        optimized_hot_start,
        only_ce_loss,
        structured_alone,
        eval_steps
    )

if __name__ == "__main__":
    main()