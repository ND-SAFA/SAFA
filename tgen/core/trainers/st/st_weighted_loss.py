import torch


class WeightedMSE(torch.nn.Module):
    def __init__(self, device: torch.device = None, weight_positive=.1):
        """
        Creates a loss function that adds extra penalty for false negatives.
        :param device: The device to use to store memory.
        :param weight_positive: The loss to return for a false negative.
        """
        super().__init__()
        self.device = device
        self.weight_positive = weight_positive

    def forward(self, predictions: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        Computes MSE between predictions and targets, with extra weight added to false negatives.
        :param predictions: The predicted scores.
        :param targets: The actual labels.
        :return: Average loss of samples weight the extra penalty.
        """
        losses = (predictions - targets) ** 2
        weights = torch.Tensor([1 + self.calculate_extra_weight(p, l) for p, l in zip(predictions, targets)]).to(self.device)
        weighted_losses = weights * losses
        loss = torch.mean(weighted_losses)
        return loss

    def calculate_extra_weight(self, pred: float, label: int):
        """
        Calculates the extra weight to add to the loss.
        :param pred: The prediction for the label.
        :param label: THe label of the datum.
        :return:
        """
        if label == 1:
            if pred >= 0.5:
                return 0
            else:
                return self.weight_positive
        else:
            if pred >= 0.5:
                return 0
            else:
                return 0

    def __repr__(self) -> str:
        """
        :return: Display name for loss containing class name and weight of positive class.
        """
        return f"{str(self.__class__)}({self.weight_positive})"
