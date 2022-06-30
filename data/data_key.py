class DataKey:
    SOURCE_PRE = 's'
    TARGET_PRE = 't'
    ID_KEY = 'id'
    LABEL_KEY = 'label'
    INPUT_IDS = "input_ids"
    TOKEN_TYPE_IDS = "token_type_ids"
    ATTENTION_MASK = "attention_mask"

    @staticmethod
    def get_feature_info_keys():
        return [DataKey.INPUT_IDS, DataKey.TOKEN_TYPE_IDS, DataKey.ATTENTION_MASK]
