from typing import Dict

from util.supported_enum import SupportedEnum


class PredictionJobTypes(SupportedEnum):
    OPENAI = "openai"
    BASE = "base"


class ExperimentCreator:
    """
    Creates experiment definitions for endpoints.
    """

    @staticmethod
    def create_prediction_definition(dataset: Dict, output_dir: str, prediction_job_type: PredictionJobTypes,
                                     model_path: str = None) -> Dict:
        """
        Creates experiment definition for predicting on dataset using defined job type.
        :param dataset: The dataset to predict on.
        :param output_dir: The output directory to store logs and other job information.
        :param prediction_job_type: The type of job to run prediction on (e.g. OPENAI / Model)
        :param model_path: The path to the model used for prediction.
        :return: Definition defining prediction job.
        """
        base_definition = {
            "trainer_dataset_manager": {
                "eval_dataset_creator": dataset
            }
        }
        if prediction_job_type == PredictionJobTypes.OPENAI:
            definition = {
                **base_definition,
                "object_type": "OPEN_AI",
                "task": "PREDICT",
                "data_output_path": output_dir
            }
        elif prediction_job_type == PredictionJobTypes.BASE:
            assert model_path is not None, "Expected model_path to be defined for prediction job."
            definition = {
                **base_definition,
                "job_args": {},
                "model_manager": {
                    "model_path": model_path
                },
                "trainer_args": {},
            }
        else:
            raise NotImplementedError(f"Prediction job is not supported for job type:{prediction_job_type.name}")
        return ExperimentCreator.create_job_experiment(definition, output_dir)

    @staticmethod
    def create_job_experiment(job_definition: Dict, output_dir: str) -> Dict:
        """
        Wraps job definition in experiment definition.
        :param job_definition: The job to wrap.
        :param output_dir: The directory to output job materials.
        :return: Experiment definition for job.
        """
        return {
            "output_dir": output_dir,
            "steps": [{
                "jobs": [job_definition]
            }]
        }
