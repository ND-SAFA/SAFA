from torch import nn

from tgen.common.util.supported_enum import SupportedEnum
from tgen.core.trainers.st.st_weighted_loss import WeightedMSE


class SupportedSTLossFunctions(SupportedEnum):
    MSE = nn.MSELoss
    WEIGHTED_MSE = WeightedMSE
    MAE = nn.L1Loss
    CROSS_ENTROPY = nn.BCELoss
