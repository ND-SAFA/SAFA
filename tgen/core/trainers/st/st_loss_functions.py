from typing import Union

from sentence_transformers.losses import ContrastiveLoss, CosineSimilarityLoss

from tgen.common.util.supported_enum import SupportedEnum


class SupportedSTLossFunctions(SupportedEnum):
    """
    Enumerates the different loss functions available for sentence embedding models.
    """
    COSINE = CosineSimilarityLoss
    CONTRASTIVE = ContrastiveLoss

    def is_name(self, n: Union[str, "SupportedSTLossFunctions"]):
        """
        Checks if given name matches that of loss function.
        :param n: Either name or supported loss function.
        :return: True if names match.
        """
        if isinstance(n, SupportedSTLossFunctions):
            n = n.name
        return n.upper() == self.name.upper()
