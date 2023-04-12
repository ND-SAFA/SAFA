import json
import os
import random

from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.constants import OUTPUT_FILENAME
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.supported_job_type import SupportedJobType
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.variables.definition_variable import DefinitionVariable
from tgen.variables.experimental_variable import ExperimentalVariable
from tgen.variables.multi_variable import MultiVariable
from tgen.variables.typed_definition_variable import TypedDefinitionVariable
from tgen.variables.undetermined_variable import UndeterminedVariable
from tgen.variables.variable import Variable


class BaseExperimentTest(BaseTest):
    accuracies = []
    EXPERIMENT_DEFINITION = DefinitionVariable({
        "steps": MultiVariable([
            DefinitionVariable({
                "jobs": MultiVariable([TypedDefinitionVariable({
                    TypedDefinitionVariable.OBJECT_TYPE_KEY: SupportedJobType.HUGGING_FACE.name,
                    "task": TrainerTask.TRAIN,
                    "job_args": DefinitionVariable({
                    }),
                    "model_manager": DefinitionVariable({
                        "model_path": ExperimentalVariable([Variable("roberta-base"), Variable("bert-base-uncased")]),
                    }),
                    "trainer_dataset_manager": DefinitionVariable({
                        "train_dataset_creator": TypedDefinitionVariable({
                            TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
                            "project_reader": TypedDefinitionVariable({
                                TypedDefinitionVariable.OBJECT_TYPE_KEY: "STRUCTURE",
                                "project_path": ExperimentalVariable([Variable("safa1"), Variable("safa2")])
                            })
                        })
                    }),
                    "trainer_args": DefinitionVariable({
                        "output_dir": Variable(TEST_OUTPUT_DIR),
                        "num_train_epochs": ExperimentalVariable([Variable(100), Variable(200)])
                    })
                })]),
                "comparison_criterion": DefinitionVariable({
                    "metrics": Variable(["accuracy"])
                })
            }),
            DefinitionVariable({"jobs": MultiVariable([TypedDefinitionVariable({
                TypedDefinitionVariable.OBJECT_TYPE_KEY: SupportedJobType.HUGGING_FACE.name,
                "task": TrainerTask.PREDICT,
                "job_args": DefinitionVariable({
                }),
                "model_manager": DefinitionVariable({
                    "model_path": UndeterminedVariable(),
                }),
                "trainer_dataset_manager": DefinitionVariable({
                    "eval_dataset_creator":
                        TypedDefinitionVariable({
                            TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
                            "project_reader": TypedDefinitionVariable({
                                TypedDefinitionVariable.OBJECT_TYPE_KEY: "STRUCTURE",
                                "project_path": "SAFA"
                            })
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

    @staticmethod
    def _load_step_output(output_file_path=None):
        if not output_file_path:
            output_file_path = os.path.join(TEST_OUTPUT_DIR, OUTPUT_FILENAME)
        with open(output_file_path) as out_file:
            output = json.load(out_file)
        return output

    def job_fake_run(self):
        accuracy = random.randint(1, 100) / 100
        self.accuracies.append(accuracy)
        return JobResult({JobResult.METRICS: {"accuracy": accuracy}})
