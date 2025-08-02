import sys
import src.helpers.scoring.coref_scoring as coref_scoring
from src.learning.models.logistic_regression import LogisticRegression
from src.learning.loss.coref_structured_hinge_loss import CorefStructuredHingeLoss
from src.helpers.loaders.prompt_data_loader import load_rule_groundings
from src.learning.loss.joint_cross_entropy_loss import JointCrossEntropyLoss
import torch
import pandas as pd
import numpy as np

def load_checkpoint(model, folder):
    model.load_state_dict(torch.load(folder + f'log_reg_model.pth'))    

def main():
    rule_type = sys.argv[1]
    model_checkpoint_path = sys.argv[2]
    
    # added for fine-tuned models
    data_input_paths = {
        'val': 'C:\\src\\MoralDistillation\\data\\coref\\GENIA_MedCo_coreference_corpus_1.0\\dev\\',
        #'test': 'C:\\src\\MoralDistillation\\data\\coref\\GENIA_MedCo_coreference_corpus_1.0\\test\\'
    }

    grounding_paths = {
        'val': 'C:\\Users\\mpauk\\Downloads\\mistral_genia_mc_sft_dev\\',
        #'test': 'C:\\Users\\mpauk\\Downloads\\mistral_genia_mc\\5\\'
    }

    train_groundings = coref_scoring.get_training_groundings(data_input_paths, grounding_paths, rule_type, 32)

    rules = coref_scoring.get_rule_info()
    constraints = coref_scoring.get_constraints()
    # models
    model = LogisticRegression(1, 1)
    load_checkpoint(model, model_checkpoint_path)
    # set models to eval
    model.eval()
    with torch.no_grad():
        val_groundings = train_groundings['val']
        #test_groundings = train_groundings['test']
        # validation set evaluation pre-training
        print(f'############ Validation Pretraining Results ############')
        #coref_scoring.model_eval(rules, constraints, val_groundings)
        # get validation predictions
        val_outputs = {
            'rule_one': model(torch.tensor(val_groundings['rule_one']['Score'].tolist()).unsqueeze(1)),
        }
        # validation set evaluation calibrated
        print(f'############ Validation Finetuned Results ############')
        coref_scoring.model_eval(rules, constraints, val_groundings, val_outputs)
        return
        # get test predictions
        test_outputs = {
            'rule_one': model(torch.tensor(test_groundings['rule_one']['Score'].tolist()).unsqueeze(1)),
        }
        # test set evaluation pre-training
        coref_scoring.model_eval(rules, constraints, test_groundings)
        # test set evaluation calibrated
        coref_scoring.model_eval(rules, constraints, test_groundings, test_outputs)

if __name__ == "__main__":
    main()