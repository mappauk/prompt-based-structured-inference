import torch
from src.inference.gurobi_inference_model import GurobiInferenceModel

class StructuredHingeLoss(torch.nn.Module):
    def __init__(self, rules, constraints, num_solutions):
        super(StructuredHingeLoss, self).__init__()
        self.rules = rules
        self.constraints = constraints
        self.num_solutions = num_solutions

    def forward(self, inputs, outputs):
        # get cross entropy loss
        exploded_groundings = {}
        delta = 0
        for rule, grounding in inputs.items():
            grounding_copy = grounding.copy()
            targets = torch.tensor(grounding['GroundTruth'].tolist())
            delta += torch.nn.functional.cross_entropy(outputs[rule], targets)
            softmax_output = torch.nn.functional.softmax(outputs[rule], dim=1)
            grounding_copy['Score'] = list(softmax_output.detach().numpy())
            exploded_groundings[rule] = grounding_copy.explode(['HeadVariable', 'RuleVariable', 'Score', 'label'])
        # get solutions
        inference_model = GurobiInferenceModel(self.rules, exploded_groundings, self.constraints, self.num_solutions)
        solutions = inference_model.inference()
        max_score = 0
        for solution in solutions:
            score = 0
            for rule, df in inputs.items():
                counter = 0
                for index, row in df.iterrows():
                    for i in range(len(row['RuleVariable'])):
                        if solution[row['RuleVariable'][i]] == 1:
                            score += outputs[rule][counter][i]
                            break
                    counter += 1
            if score > max_score:
                max_score = score
        gold_structure_score = 0
        for rule, df in inputs.items():
            counter = 0
            for index, row in df.iterrows():
                gold_structure_score += outputs[rule][counter][row['GroundTruth']]
                counter += 1
        return delta + max_score - gold_structure_score
