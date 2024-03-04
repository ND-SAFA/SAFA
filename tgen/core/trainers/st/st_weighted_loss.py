import torch


class WeightedBCELoss(torch.nn.Module):
    def __init__(self, weight_positive=1.1):
        super().__init__()
        self.weight_positive = weight_positive

    def forward(self, predictions, targets):
        # Ensure the predictions are in a valid range
        predictions = torch.clamp(predictions, min=1e-7, max=1 - 1e-7)

        # Calculate the weighted loss
        loss = -1 * (self.weight_positive * targets * torch.log(predictions) +
                     (1 - targets) * torch.log(1 - predictions))

        return torch.mean(loss)
