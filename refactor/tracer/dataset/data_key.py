from typing import List


class DataKey:
    """
    Expected dictionary keys for the trace dataset
    """
    SOURCE_PRE = 's'
    TARGET_PRE = 't'
    ID_KEY = 'id'
    LABEL_KEY = 'label'
    INPUT_IDS = "input_ids"
    TOKEN_TYPE_IDS = "token_type_ids"
    ATTEN_MASK = "attention_mask"
    SOURCE_TARGET_PAIRS = "source_target_pairs"
    SEP = "_"

    @staticmethod
    def get_feature_entry_keys() -> List[str]:
        """
        Returns the list of keys to extract required feature info for creating a feature entry
        :return: list of keys
        """
        return [DataKey.INPUT_IDS, DataKey.TOKEN_TYPE_IDS, DataKey.ATTEN_MASK]
