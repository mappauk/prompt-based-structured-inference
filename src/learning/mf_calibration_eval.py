import sys
import src.helpers.scoring.mf_scoring as mf_scoring
from src.learning.models.logistic_regression import LogisticRegression
from src.learning.loss.structured_hinge_loss import StructuredHingeLoss
from src.learning.loss.joint_cross_entropy_loss import JointCrossEntropyLoss
import torch

def load_checkpoint(models, folder):
    for i in range(len(models)):
        models[i].load_state_dict(torch.load(folder + f'model_{i}.pth'))    

def main():
    data_input_path = sys.argv[1]
    rule_groundings_path = sys.argv[2]
    rule_type = sys.argv[3]
    model_checkpoint_path = sys.argv[4]

    rule_names = ['rule_one', 'rule_two', 'rule_three', 'rule_four']

    rule_groundings = mf_scoring.get_scored_groundings(rule_groundings_path, rule_names, rule_type)
    train_groundings = mf_scoring.get_training_groundings(rule_groundings, data_input_path)
    rules = mf_scoring.get_rule_info()
    constraints = mf_scoring.get_mf_constraints(data_input_path)
    #joint_ce_loss = JointCrossEntropyLoss()
    structured_hinge_loss = StructuredHingeLoss(rules, constraints, 10)

    for i in range(len(train_groundings)):
        # models
        foundation_model = LogisticRegression(5, 5)
        foundation_model_w_context = LogisticRegression(5, 5)
        role_model = LogisticRegression(16, 16)
        role_model_w_context = LogisticRegression(16, 16)
        checkpoint_path = model_checkpoint_path + f'cross_validation_{i}_'
        load_checkpoint([foundation_model, foundation_model_w_context, role_model, role_model_w_context], checkpoint_path)

        # set models to eval
        foundation_model.eval()
        foundation_model_w_context.eval()
        role_model.eval()
        role_model_w_context.eval()

        with torch.no_grad():
            # get validation predictions
            val_groundings = train_groundings[i]['val']
            val_outputs = {
                'rule_one': foundation_model(torch.tensor(val_groundings['rule_one']['Score'].tolist())),
                'rule_two': role_model(torch.tensor(val_groundings['rule_two']['Score'].tolist())),
                'rule_three': foundation_model_w_context(torch.tensor(val_groundings['rule_three']['Score'].tolist())),
                'rule_four': role_model_w_context(torch.tensor(val_groundings['rule_four']['Score'].tolist()))
            }

            # validation set evaluation pre-training
            print(f'############ Validation Pretraining Results (Fold {i}) ############')
            mf_scoring.model_eval(rules, constraints, val_groundings)

            # validation set evaluation calibrated
            print(f'############ Validation Finetuned Results (Fold {i}) ############')
            val_loss = structured_hinge_loss(val_groundings, val_outputs)
            print(f'Validation Loss: {val_loss}')
            mf_scoring.model_eval(rules, constraints, val_groundings, val_outputs)
            # get test predictions
            test_groundings = train_groundings[i]['test']
            test_outputs = {
                'rule_one': foundation_model(torch.tensor(test_groundings['rule_one']['Score'].tolist())),
                'rule_two': role_model(torch.tensor(test_groundings['rule_two']['Score'].tolist())),
                'rule_three': foundation_model_w_context(torch.tensor(test_groundings['rule_three']['Score'].tolist())),
                'rule_four': role_model_w_context(torch.tensor(test_groundings['rule_four']['Score'].tolist()))
            }

            # test set evaluation pre-training
            mf_scoring.model_eval(rules, constraints, test_groundings)
            # test set evaluation calibrated
            mf_scoring.model_eval(rules, constraints, test_groundings, test_outputs)


if __name__ == "__main__":
    main()