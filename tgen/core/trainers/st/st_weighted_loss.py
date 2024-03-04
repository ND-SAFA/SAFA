import torch


class WeightedMSE(torch.nn.Module):
    def __init__(self, device: torch.device = None, weight_positive=.1):
        super().__init__()
        self.device = device
        self.weight_positive = weight_positive

    def forward(self, predictions, targets):
        # Calculate the weighted loss
        losses = (predictions - targets) ** 2
        weights = torch.Tensor([1 + self.calculate_extra_weight(p, l) for p, l in zip(predictions, targets)]).to(self.device)
        weighted_losses = weights * losses
        loss = torch.mean(weighted_losses)
        return loss

    def calculate_extra_weight(self, pred, label):
        if label == 1:
            if pred >= 0.5:
                return 0
            else:
                return self.weight_positive
        else:
            if pred >= 0.5:
                return self.weight_positive
            else:
                return 0

    def __repr__(self) -> str:
        return f"{str(self.__class__)}({self.weight_positive})"
