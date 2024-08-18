from typing import List

from gen_common.constants.symbol_constants import UNDERSCORE


class DataKey:
    """
    Expected dictionary keys for the trace data
    """
    SOURCE_PRE = 's'
    TARGET_PRE = 't'
    ID_KEY = 'id'
    LABEL_KEY = 'label'
    LABELS_KEY = "labels"
    INPUT_IDS = "input_ids"
    TOKEN_TYPE_IDS = "token_type_ids"
    ATTEN_MASK = "attention_mask"
    SOURCE_TARGET_PAIRS = "source_target_pairs"
    SEP = UNDERSCORE

    @staticmethod
    def get_feature_entry_keys() -> List[str]:
        """
        Returns the list of keys to extract required feature info for creating a feature entry
        :return: list of keys
        """
        return [DataKey.INPUT_IDS, DataKey.TOKEN_TYPE_IDS, DataKey.ATTEN_MASK]
