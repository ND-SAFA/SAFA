import pandas as pd
from sklearn.model_selection import train_test_split

from experiment.gan.constants import DATA_FILE_PATH, LABEL_PARAM, SOFTWARE_DATA_PATH, SOURCE_PARAM, TARGET_PARAM, \
    TEST_EXPORT_PATH, TEST_SIZE, TRAIN_EXPORT_PATH
from experiment.gan.data.safa_port import read_safa_project
from experiment.gan.data.traceability_port import read_traceability_projects
from pre_processing.pre_processing_options import PreProcessingOptions
from pre_processing.pre_processor import PreProcessor

if __name__ == "__main__":
    software_df = read_traceability_projects(SOFTWARE_DATA_PATH)
    software_df.to_csv(DATA_FILE_PATH, index=False)
    lhp_df = read_safa_project([
        ("swr.json", "SYS.json", "swr2SYS.json"),
        ("hwr.json", "SYS.json", "hwr2SYS.json"),
        ("SYS.json", "fsr.json", "SYS2fsr.json"),
        ("fsr.json", "sg.json", "fsr2sg.json")
    ])
    train_df, test_df = train_test_split(lhp_df, test_size=TEST_SIZE)

    train_df = pd.concat([train_df.sample(n=100), software_df])
    """
    Pre-process
    """
    pre_processor_options = {
        PreProcessingOptions.REMOVE_UNWANTED_CHARS: True,
        PreProcessingOptions.REPLACE_WORDS: True
    }
    word_replace_mappings = {
        "HVCH": "high voltage coolant heater",
        "�": " "
    }
    pre_processor = PreProcessor(pre_processor_options, word_replace_mappings=word_replace_mappings)
    train_df[SOURCE_PARAM] = pre_processor.run(train_df[SOURCE_PARAM])
    train_df[TARGET_PARAM] = pre_processor.run(train_df[TARGET_PARAM])
    test_df[SOURCE_PARAM] = pre_processor.run(test_df[SOURCE_PARAM])
    test_df[TARGET_PARAM] = pre_processor.run(test_df[TARGET_PARAM])
    """
    Export
    """

    train_df.to_csv(TRAIN_EXPORT_PATH, index=False)
    test_df.to_csv(TEST_EXPORT_PATH, index=False)

    print("Train", "-" * 25)
    print(len(train_df))
    print(train_df[LABEL_PARAM].value_counts())
