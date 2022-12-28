import random

from jobs.components.job_result import JobResult
from jobs.supported_job_type import SupportedJobType
from test.base_test import BaseTest
from test.paths.paths import TEST_OUTPUT_DIR
from util.variables.definition_variable import DefinitionVariable
from util.variables.experimental_variable import ExperimentalVariable
from util.variables.multi_variable import MultiVariable
from util.variables.typed_definition_variable import TypedDefinitionVariable
from util.variables.undetermined_variable import UndeterminedVariable
from util.variables.variable import Variable


class BaseExperimentTest(BaseTest):
    accuracies = []
    EXPERIMENT_DEFINITION = DefinitionVariable({
        "steps": MultiVariable([
            DefinitionVariable({"jobs": MultiVariable([TypedDefinitionVariable({
                TypedDefinitionVariable.OBJECT_TYPE_KEY: SupportedJobType.TRAIN.name,
                "job_args": DefinitionVariable({
                }),
                "model_manager": DefinitionVariable({
                    "model_path": ExperimentalVariable([Variable("roberta-base"), Variable("bert-base")]),
                }),
                "trainer_dataset_manager": DefinitionVariable({
                    "train_dataset_creator":
                        TypedDefinitionVariable({
                            "object_type": "Safa",
                            "project_path": ExperimentalVariable([Variable("safa1"), Variable("safa2")])
                        })
                }),
                "trainer_args": DefinitionVariable({
                    "output_dir": Variable(TEST_OUTPUT_DIR),
                    "num_train_epochs": ExperimentalVariable([Variable(100), Variable(200)])
                })
            })]),
                "comparison_metric": "accuracy"
            }),
            DefinitionVariable({"jobs": MultiVariable([TypedDefinitionVariable({
                TypedDefinitionVariable.OBJECT_TYPE_KEY: SupportedJobType.PREDICT.name,
                "job_args": DefinitionVariable({
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
                    "output_dir": Variable(TEST_OUTPUT_DIR),
                })
            })])
            })
        ]),
        "output_dir": TEST_OUTPUT_DIR,

    })

    def setUp(self):
        super(BaseExperimentTest, self).setUp()
        self.accuracies = []

    def job_fake_run(self):
        accuracy = random.randint(1, 100) / 100
        self.accuracies.append(accuracy)
        return JobResult({JobResult.METRICS: {"accuracy": accuracy}})
