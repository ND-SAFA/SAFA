import os

from common.models.base_models.supported_base_model import SupportedBaseModel
from common.models.model_generator import ModelGenerator
from experiment.common.experiment_run import ExperimentRun
from experiment.common.pretraining_data import PretrainingData
from experiment.common.run_mode import RunMode
from experiment.domains.automotive import METRICS
from experiment.gan.constants import BASE_MODEL_NAME, TEST_EXPORT_PATH, TRAINING_DATA_PATH, TRAIN_EXPORT_PATH
from trace.data.trace_dataset_creator import TraceDatasetCreator

BASE_OUTPUT_DIR = os.path.join(TRAINING_DATA_PATH, "baseline")

if __name__ == "__main__":
    model_generator = ModelGenerator(SupportedBaseModel.NL_BERT, BASE_MODEL_NAME)
    trace_dataset_creator = TraceDatasetCreator(model_generator=model_generator,
                                                data_path=TEST_EXPORT_PATH)
    train_dataset_creator = TraceDatasetCreator(model_generator=model_generator,
                                                data_path=TRAIN_EXPORT_PATH)
    experiment = ExperimentRun(
        model_state_path=BASE_MODEL_NAME,
        pretraining=PretrainingData.AUTOMOTIVE,
        metrics=METRICS,
        training_project=train_dataset_creator,
        validation_project=trace_dataset_creator,
    )
    experiment.perform_run(
        BASE_OUTPUT_DIR,
        RunMode.TRAINEVAL.value
    )
