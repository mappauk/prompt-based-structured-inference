import torch
from src.inference.gurobi_inference_model import GurobiInferenceModel

class MFStructuredHingeLoss(torch.nn.Module):
    def __init__(self, rules, constraints, num_solutions, softmax_enabled=True):
        super(MFStructuredHingeLoss, self).__init__()
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
            if outputs[rule] != None:
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

        predicted_structures = {}
        gold_structures = {}

        # get structure scores
        solution = solutions[0]
        for rule, df in inputs.items():
            counter = 0
            for index, row in df.iterrows():
                id = row['Id']
                for i in range(len(row['HeadVariable'])):
                    if solution[row['HeadVariable'][i]] == 1:
                        if id in predicted_structures:
                            predicted_structures[id].append(softmax_outputs[rule][counter][i])
                        else:
                            predicted_structures[id] = [softmax_outputs[rule][counter][i]]
                    if i == row['GroundTruth']:
                        if id in gold_structures:
                            gold_structures[id].append(softmax_outputs[rule][counter][i])
                        else:
                            gold_structures[id] = [softmax_outputs[rule][counter][i]]
                counter += 1
        # compute hinge loss
        example_losses = []
        for id in predicted_structures.keys():
            predicted_structures_score = sum(predicted_structures[id])
            gold_structure_score = sum(gold_structures[id])
            example_structured_hinge_loss = max(torch.tensor(0.0, requires_grad=True), predicted_structures_score - gold_structure_score)
            example_losses.append(example_structured_hinge_loss)
        
        structured_hinge_loss = sum(example_losses)/len(example_losses)
        return structured_hinge_loss
