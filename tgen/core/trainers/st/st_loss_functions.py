from typing import Union

from sentence_transformers.losses import CosineSimilarityLoss, MultipleNegativesRankingLoss, OnlineContrastiveLoss

from tgen.common.util.supported_enum import SupportedEnum


class SupportedLossFunctions(SupportedEnum):
    """
    Enumerates the different loss functions available for sentence embedding models.
    """
    COSINE = CosineSimilarityLoss
    CONTRASTIVE = OnlineContrastiveLoss
    MNRL = MultipleNegativesRankingLoss

    def is_name(self, n: Union[str, "SupportedLossFunctions"]):
        """
        Checks if given name matches that of loss function.
        :param n: Either name or supported loss function.
        :return: True if names match.
        """
        if isinstance(n, SupportedLossFunctions):
            n = n.name
        return n.upper() == self.name.upper()
