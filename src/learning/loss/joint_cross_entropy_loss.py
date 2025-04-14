import torch

class JointCrossEntropyLoss(torch.nn.Module):
    def __init__(self, mf_weights = None, mr_weights = None):
        super(JointCrossEntropyLoss, self).__init__()
        self.mf_weights = mf_weights
        self.mr_weights = mr_weights


    def forward(self, inputs, outputs):
        # get cross entropy loss
        delta = 0
        for rule, grounding in inputs.items():
            targets = torch.tensor(grounding['GroundTruth'].tolist())
            if rule == 'rule_one' or rule == 'rule_three':
                delta += torch.nn.functional.cross_entropy(outputs[rule], targets, weight=self.mf_weights)
            else:
                delta += torch.nn.functional.cross_entropy(outputs[rule], targets, weight=self.mr_weights)
        return delta