from torch import nn

from tgen.common.util.supported_enum import SupportedEnum
from tgen.core.trainers.st.st_weighted_loss import WeightedBCELoss


class SupportedMLPLosses(SupportedEnum):
    MSE = nn.MSELoss
    MAE = nn.L1Loss
    CROSS_ENTROPY = nn.BCELoss
    WEIGHTED_CROSS_ENTROPY = WeightedBCELoss
