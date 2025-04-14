import sys
import src.helpers.scoring.mf_scoring as mf_scoring
from src.learning.models.logistic_regression import LogisticRegression
from src.learning.loss.structured_hinge_loss import StructuredHingeLoss
from src.learning.loss.joint_cross_entropy_loss import JointCrossEntropyLoss
from src.learning.loss.early_stopping import EarlyStopping
import torch

def checkpoint(models, folder):
    for i in range(len(models)):
        torch.save(models[i].state_dict(), folder + f'model_{i}.pth')

def load_checkpoint(models, folder):
    for i in range(len(models)):
        models[i].load_state_dict(torch.load(folder + f'model_{i}.pth'))    

def training_loop(
        rules, 
        custom_rule_constraints, 
        foundation_model, 
        foundation_model_w_context, role_model, 
        role_model_w_context, 
        learning_rate,
        batched_train_groundings,
        val_groundings,
        output_path,
        optimized_hot_start,
        only_ce_loss,
        structured_alone):
    # hyper params
    epochs = 100000000
    num_solutions = 10
    best_val_loss = 1000000000000000
    
    # optimizers
    foundation_model_optimizer = torch.optim.Adam(foundation_model.parameters(), lr=learning_rate)
    foundation_model_w_context_optimizer = torch.optim.Adam(foundation_model_w_context.parameters(), lr=learning_rate)
    role_model_optimizer = torch.optim.Adam(role_model.parameters(), lr=learning_rate)
    role_model_w_context_optimizer = torch.optim.Adam(role_model_w_context.parameters(), lr=learning_rate)

    # loss functions and early stopping definitions
    joint_ce_loss = JointCrossEntropyLoss()
    structured_hinge_loss = StructuredHingeLoss(rules, custom_rule_constraints, num_solutions)
    ce_only_early_stopping = EarlyStopping(10, 0.0001)
    structured_hinge_early_stopping = EarlyStopping(10, 0)


    for epoch in range(epochs):
        batch_losses = []
        # set models to train
        foundation_model.train()
        foundation_model_w_context.train()
        role_model.train()
        role_model_w_context.train()

        use_structured_loss = (
            (optimized_hot_start and  not ce_only_early_stopping.training_flag) or
            structured_alone
        )

        for i in range(len(batched_train_groundings)):
            print(f"############ epoch {epoch}, batch: {i} ############")
            batch = batched_train_groundings[i]

            # zero gradients
            foundation_model_optimizer.zero_grad()
            foundation_model_w_context_optimizer.zero_grad()
            role_model_optimizer.zero_grad()
            role_model_w_context_optimizer.zero_grad()

            # get predictions
            foundation_model_logits = foundation_model(torch.tensor(batch['rule_one']['Score'].tolist()))
            foundation_model_w_context_logits = foundation_model_w_context(torch.tensor(batch['rule_three']['Score'].tolist()))
            role_model_logits = role_model(torch.tensor(batch['rule_two']['Score'].tolist()))
            role_model_w_context_logits = role_model_w_context(torch.tensor(batch['rule_four']['Score'].tolist()))

            outputs = {
                'rule_one': foundation_model_logits,
                'rule_two': role_model_logits,
                'rule_three': foundation_model_w_context_logits,
                'rule_four': role_model_w_context_logits
            }

            loss = None
            if use_structured_loss:
                loss = structured_hinge_loss(batch, outputs)
            else:
                loss = joint_ce_loss(batch, outputs)
            loss.backward()
            # update weights
            foundation_model_optimizer.step()
            foundation_model_w_context_optimizer.step()
            role_model_optimizer.step()
            role_model_w_context_optimizer.step()
            batch_losses.append(loss.item())

        # Estimate the f1 score for the development set
        print(f"Training Loss: {sum(batch_losses)/len(batch_losses)}")
        print(f'####################### Model Performance (Val) epoch: {epoch} #######################')

        # set models to eval
        foundation_model.eval()
        foundation_model_w_context.eval()
        role_model.eval()
        role_model_w_context.eval()

        # evaluate on validation set
        with torch.no_grad():
            val_outputs = {
                'rule_one': foundation_model(torch.tensor(val_groundings['rule_one']['Score'].tolist())),
                'rule_two': role_model(torch.tensor(val_groundings['rule_two']['Score'].tolist())),
                'rule_three': foundation_model_w_context(torch.tensor(val_groundings['rule_three']['Score'].tolist())),
                'rule_four': role_model_w_context(torch.tensor(val_groundings['rule_four']['Score'].tolist()))
            }
            val_loss = None
            if use_structured_loss:
                val_loss = structured_hinge_loss(val_groundings, val_outputs)
                structured_hinge_early_stopping.check_early_stopping(val_loss, epoch)
            else:
                val_loss = joint_ce_loss(val_groundings, val_outputs)
                ce_only_early_stopping.check_early_stopping(val_loss, epoch)
            print(f'Validation Loss: {val_loss}')

            #mf_scoring.model_eval(rules, custom_rule_constraints, val_groundings, val_outputs)
            print('\n\n\n')

            should_update_best_loss = (
                only_ce_loss or 
                (optimized_hot_start and not ce_only_early_stopping.training_flag and structured_hinge_early_stopping.best_epoch != 0) or
                structured_alone
            )

            if best_val_loss > val_loss and should_update_best_loss:
                checkpoint([foundation_model, foundation_model_w_context, role_model, role_model_w_context], output_path)
                best_val_loss = val_loss

            if (not ce_only_early_stopping.training_flag and only_ce_loss) or not structured_hinge_early_stopping.training_flag:
                break

def main():
    data_input_path = sys.argv[1]
    rule_groundings_path = sys.argv[2]
    rule_type = sys.argv[3]
    model_checkpoint_path = sys.argv[4]
    optimized_hot_start = True
    only_ce_loss = False
    learning_rate = 0.001
    structured_alone = False

    rule_names = ['rule_one', 'rule_two', 'rule_three', 'rule_four']

    rule_groundings = mf_scoring.get_scored_groundings(rule_groundings_path, rule_names, rule_type)
    train_groundings = mf_scoring.get_training_groundings(rule_groundings, data_input_path)
    rules = mf_scoring.get_rule_info()
    constraints = mf_scoring.get_mf_constraints(data_input_path)
    for i in range(len(train_groundings)):
        # models
        foundation_model = LogisticRegression(5, 5)
        foundation_model_w_context = LogisticRegression(5, 5)
        role_model = LogisticRegression(16, 16)
        role_model_w_context = LogisticRegression(16, 16)

        batched_train_groundings = train_groundings[i]['train']
        val_groundings = train_groundings[i]['val']
        output_path = model_checkpoint_path + f'cross_validation_{i}_'
        training_loop(
            rules,
            constraints,
            foundation_model,
            foundation_model_w_context,
            role_model,
            role_model_w_context,
            learning_rate,
            batched_train_groundings,
            val_groundings,
            output_path,
            optimized_hot_start,
            only_ce_loss,
            structured_alone
        )


if __name__ == "__main__":
    main()