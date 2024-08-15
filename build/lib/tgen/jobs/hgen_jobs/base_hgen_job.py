from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs


class BaseHGenJob(AbstractJob):

    def __init__(self, hgen_args: HGenArgs = None, job_args: JobArgs = None, **hgen_params):
        """
        Initializes the job with args needed for hierarchy generator
        :param llm_manager: Model Manager in charge of generating artifacts
        :param job_args: The arguments need for the job
        :param hgen_args: The hgen args to use if created prior to start of the job
        :param hgen_params: Any additional parameters for the hgen args
        """
        self.hgen_params = hgen_params
        self.hgen_args = hgen_args
        self.hgen = HierarchyGenerator(self.get_hgen_args())
        super().__init__(job_args)

    def _run(self) -> TraceDataset:
        """
        Runs the hierarchy generator and exports the resulting dataset
        :return: The result of the job
        """
        generated_dataset: PromptDataset = self.hgen.run()
        return generated_dataset.trace_dataset if isinstance(generated_dataset, PromptDataset) else generated_dataset

    def get_hgen_args(self) -> HGenArgs:
        """
        Gets the arguments used for the hierarchy generation
        :return: The arguments used for the hierarchy generation
        """
        if self.hgen_args is None:
            self.hgen_args = HGenArgs(**self.hgen_params)
        return self.hgen_args
