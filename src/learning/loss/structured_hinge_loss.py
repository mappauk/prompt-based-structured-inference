import torch
from src.inference.gurobi_inference_model import GurobiInferenceModel

class StructuredHingeLoss(torch.nn.Module):
    def __init__(self, rules, constraints, num_solutions, softmax_enabled=True):
        super(StructuredHingeLoss, self).__init__()
        self.rules = rules
        self.constraints = constraints
        self.num_solutions = num_solutions
        self.softmax_enabled = softmax_enabled

    def forward(self, inputs, outputs):
        # get cross entropy loss
        exploded_groundings = {}
        softmax_outputs = {}
        for rule, grounding in inputs.items():
            grounding_copy = grounding.copy()
            if self.softmax_enabled:
                softmax_output = torch.nn.functional.softmax(outputs[rule], dim=1)
            else:
                softmax_output = outputs[rule]
            softmax_outputs[rule] = softmax_output
            grounding_copy['Score'] = list(softmax_output.cpu().detach().numpy())
            exploded_groundings[rule] = grounding_copy.explode(['HeadVariable', 'RuleVariable', 'Score', 'label'])
        # get solutions
        inference_model = GurobiInferenceModel(self.rules, exploded_groundings, self.constraints, self.num_solutions)
        solutions = inference_model.inference()
        best_imposter_score = 0
        for solution in solutions:
            imposter_hamming_distance = 0
            imposter_score = 0
            for rule, df in inputs.items():
                counter = 0
                for index, row in df.iterrows():
                    for i in range(len(row['RuleVariable'])):
                        if solution[row['RuleVariable'][i]] == 1:
                            imposter_score += softmax_outputs[rule][counter][i]
                            if i != row['GroundTruth']:
                                imposter_hamming_distance += 1
                            break
                    counter += 1
            best_imposter_score = max(best_imposter_score, imposter_hamming_distance + imposter_score)

        gold_structure_score = 0
        for rule, df in inputs.items():
            counter = 0
            for index, row in df.iterrows():
                gold_structure_score += softmax_outputs[rule][counter][row['GroundTruth']]
                counter += 1

        return best_imposter_score - gold_structure_score
