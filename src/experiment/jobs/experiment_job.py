from typing import Dict

from common.jobs.abstract_args_builder import AbstractArgsBuilder
from experiment.common.run_mode import RunMode
from trace.data.datasets.safa_dataset_creator import SafaDatasetCreator
from trace.jobs.abstract_trace_job import AbstractTraceJob


class ExperimentJob(AbstractTraceJob):

    def __init__(self, args_builder: AbstractArgsBuilder):
        """
        Represents the job for creating and running experiments.
        """
        super().__init__(args_builder)

    def _run(self) -> Dict:
        validation_project_creator = self.validation_project if self.validation_project \
            else SafaDatasetCreator(trace_args.model_generator, self.validation_project_path)

        if run_mode in [RunMode.EVAL, RunMode.TRAINEVAL]:
            eval_dataset = validation_project_creator.get_prediction_dataset()
            predictions = trace_trainer.perform_prediction(eval_dataset)
            print("Predictions", "-" * 25)
            for metric in self.metrics:
                print(metric, ":", predictions["metrics"][metric])
