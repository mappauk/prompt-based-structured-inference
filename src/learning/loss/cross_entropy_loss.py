import torch

class CrossEntropyLoss(torch.nn.Module):
    def __init__(self):
        super(CrossEntropyLoss, self).__init__()


    def forward(self, inputs, outputs):
        # get cross entropy loss
        targets = torch.tensor(inputs['rule_one']['GroundTruth'].tolist()).float()
        delta = torch.nn.functional.binary_cross_entropy_with_logits(torch.squeeze(outputs['rule_one'], 1), targets)
        return delta