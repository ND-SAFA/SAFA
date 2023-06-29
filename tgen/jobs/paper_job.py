from typing import Dict, Union

from tgen.data.exporters.dataframe_exporter import DataFrameExporter
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.processing.trace_link_filter import TraceLinkFilter
from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.trainer_jobs.llm_job import LLMJob
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.train.args.abstract_llm_args import AbstractLLMArgs
from tgen.train.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.train.trainers.trainer_task import TrainerTask


class PaperJob(LLMJob):
    def __init__(self, trainer_dataset_manager: TrainerDatasetManager,
                 trainer_args: AbstractLLMArgs = None,
                 task: TrainerTask = TrainerTask.PREDICT, job_args: JobArgs = None, prompt_creator: AbstractPromptCreator = None,
                 llm_manager: AbstractLLMManager = None, trace_link_filter: TraceLinkFilter = None):
        self.trace_link_filter = trace_link_filter
        super().__init__(trainer_dataset_manager=trainer_dataset_manager, trainer_args=trainer_args, task=task,
                         job_args=job_args, prompt_creator=prompt_creator, llm_manager=llm_manager)

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        eval_dataset = self.trainer_dataset_manager[DatasetRole.EVAL]
        if self.trace_link_filter:
            eval_dataset.trace_df = self.trace_link_filter.filter(eval_dataset.trace_df)
        result = super()._run(**kwargs)
        eval_dataset = self.trainer_dataset_manager[DatasetRole.EVAL]
        exporter = DataFrameExporter(export_path=self.job_args.output_dir, dataset=eval_dataset)
        exporter.export()
        return result
