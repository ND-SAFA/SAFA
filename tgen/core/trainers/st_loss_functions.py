from torch import nn

from tgen.common.util.supported_enum import SupportedEnum


class SupportedMLPLosses(SupportedEnum):
    MSE = nn.MSELoss
    MAE = nn.L1Loss
    CROSS_ENTROPY = nn.BCELoss
