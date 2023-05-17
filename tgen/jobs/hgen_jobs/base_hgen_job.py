from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager


class BaseHGenJob(AbstractJob):

    def __init__(self, llm_manager: AbstractLLMManager, job_args: JobArgs = None, **hgen_params):
        """
        Initializes the job with args needed for hierarchy generator
        :param llm_manager: Model Manager in charge of generating artifacts
        :param job_args: The arguments need for the job
        :param hgen_params: Any additional parameters for the hgen args
        """
        self.llm_manager = llm_manager
        self.hgen_params = hgen_params
        super().__init__(job_args)

    def _run(self) -> TraceDataset:
        """
        Runs the hierarchy generator and exports the resulting dataset
        :return: The result of the job
        """
        hgen = HierarchyGenerator(self.get_hgen_args(), self.llm_manager)
        generated_dataset = hgen.run()
        return generated_dataset

    def get_hgen_args(self) -> HGenArgs:
        """
        Gets the arguments used for the hierarchy generation
        :return: The arguments used for the hierarchy generation
        """
        return HGenArgs(**self.hgen_params)
