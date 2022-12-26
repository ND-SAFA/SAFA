import random

from experiments.variables.definition_variable import DefinitionVariable
from experiments.variables.experimental_variable import ExperimentalVariable
from experiments.variables.multi_variable import MultiVariable
from experiments.variables.typed_definition_variable import TypedDefinitionVariable
from experiments.variables.undetermined_variable import UndeterminedVariable
from experiments.variables.variable import Variable
from jobs.components.job_result import JobResult
from jobs.supported_job_type import SupportedJobType
from test.base_test import BaseTest


class BaseExperimentTest(BaseTest):
    accuracies = []
    EXPERIMENT_DEFINITION = DefinitionVariable({
        "steps": MultiVariable([
            DefinitionVariable({"jobs": MultiVariable([TypedDefinitionVariable({
                TypedDefinitionVariable.OBJECT_TYPE_KEY: SupportedJobType.TRAIN.name,
                "job_args": DefinitionVariable({
                    "output_dir": Variable("TEST_OUTPUT_DIR"),
                }),
                "model_manager": DefinitionVariable({
                    "model_path": ExperimentalVariable([Variable("roberta-base"), Variable("bert-base")]),
                }),
                "trainer_dataset_manager": DefinitionVariable({
                    "train_dataset_creator": ExperimentalVariable([
                        TypedDefinitionVariable({
                            "object_type": "Safa",
                            "project_path": "safa"
                        }), TypedDefinitionVariable({
                            "object_type": "CSV",
                            "data_file_path": "csv"
                        })])
                }),
                "trainer_args": DefinitionVariable({
                    "output_dir": Variable("TEST_OUTPUT_DIR"),
                    "num_train_epochs": ExperimentalVariable([Variable(100), Variable(200)])
                })
            })]),
                "comparison_metric": "accuracy"
            }),
            DefinitionVariable({"jobs": MultiVariable([TypedDefinitionVariable({
                TypedDefinitionVariable.OBJECT_TYPE_KEY: SupportedJobType.PREDICT.name,
                "job_args": DefinitionVariable({
                    "output_dir": Variable("TEST_OUTPUT_DIR"),
                }),
                "model_manager": DefinitionVariable({
                    "model_path": UndeterminedVariable(),
                }),
                "trainer_dataset_manager": DefinitionVariable({
                    "eval_dataset_creator":
                        TypedDefinitionVariable({
                            "object_type": "Safa",
                            "project_path": "safa"
                        }),
                }),
                "trainer_args": DefinitionVariable({
                    "output_dir": Variable("TEST_OUTPUT_DIR"),
                })
            })])
            })
        ])

    })

    def job_fake_run(self):
        accuracy = random.randint(1, 100) / 100
        self.accuracies.append(accuracy)
        return JobResult({JobResult.METRICS: {"accuracy": accuracy}})
