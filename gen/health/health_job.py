import random
from typing import List, Type, Union

from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.jobs.abstract_job import AbstractJob
from gen_common.jobs.job_args import JobArgs
from gen_common.pipeline.state import State
from gen_common.util.dataclass_util import DataclassUtil

from gen.health.concepts.extraction.concept_extraction_pipeline import ConceptExtractionPipeline
from gen.health.concepts.matching.concept_matching_pipeline import ConceptMatchingPipeline
from gen.health.contradiction.contradiction_pipeline import ContradictionPipeline
from gen.health.health_args import HealthArgs
from gen.health.health_state import HealthState
from gen.health.health_util import expand_query_selection
from gen.health.types.health_tasks import HealthTask
from gen_test.health.concepts.matching.constants import CONCEPT_TYPE

HealthPipeline = Union[ContradictionPipeline, ConceptExtractionPipeline, ConceptMatchingPipeline]
HealthStateProperties = []


class HealthJob(AbstractJob):
    random.seed(0)

    def __init__(self,
                 job_args: JobArgs,
                 query_ids: Union[List[str], str],
                 tasks: List[HealthTask],
                 context_doc_path: str = None,
                 use_llm_for_entity_extraction: bool = True,
                 concept_layer_id: str = CONCEPT_TYPE):
        """
        Initializes the job to run health checks on the query artifact.
        :param job_args: Contains dataset and other common arguments to jobs in general.
        :param query_ids: The id of the query artifact under inspection.
        :param concept_layer_id: The id of the layer containing concept artifacts.
        :param additional_args: Any additional arguments to the concept or contradictions detectors.
        :param entity_layer_id: Layer ID to given extracted entities.
        :param context_doc_path:If provided, is used for defining unknown entities.
        :param use_llm_for_entity_extraction: If True, uses the llm for entity extraction instead of the standford analysis.
        """
        super().__init__(job_args, require_data=True)
        dataset: PromptDataset = job_args.dataset
        self.tasks = tasks
        self.query_ids = expand_query_selection(dataset.artifact_df, query_ids)
        self.concept_layer_id = concept_layer_id
        self.context_doc_path = context_doc_path
        self.use_llm_for_entity_extraction = use_llm_for_entity_extraction

    def _run(self) -> HealthState:
        """
        Runs health checks on the query artifact.
        :return: Results from each health check.
        """
        health_kwargs = self.job_args.get_args_for_pipeline(HealthArgs)
        args = HealthArgs(
            query_ids=self.query_ids,
            concept_layer_id=self.concept_layer_id,
            context_doc_path=self.context_doc_path,
            **health_kwargs,
        )
        state = HealthState()

        for task in self.tasks:
            pipeline_class = self._get_pipeline_class(task)
            pipeline = pipeline_class(args)
            pipeline.run()
            self.add_result_to_state(pipeline.state, state)

        return state

    @staticmethod
    def _get_pipeline_class(task: HealthTask) -> Type[HealthPipeline]:
        """
        Returns the pipeline class associated with given task.
        :param task: The health task to perform.
        :return: Health pipeline.
        """
        if task == HealthTask.CONTRADICTION:
            return ContradictionPipeline
        elif task == HealthTask.CONCEPT_MATCHING:
            return ConceptMatchingPipeline
        elif task == HealthTask.CONCEPT_EXTRACTION:
            return ConceptExtractionPipeline
        else:
            raise Exception(f"Unknown task: {task}")

    @staticmethod
    def add_result_to_state(new_state: State, existing_state: HealthState):
        """
        Saves any intersecting properties from new state to existing one.
        :param new_state: The state containing values to copy.
        :param existing_state: The state to copy values into.
        :return: None
        """
        new_state_dict = DataclassUtil.convert_to_dict(new_state)
        existing_state_dict = DataclassUtil.convert_to_dict(existing_state)

        intersection_properties = set(new_state_dict.keys()).intersection(set(existing_state_dict.keys()))
        for intersection_property in intersection_properties:
            new_state_value = getattr(new_state, intersection_property)
            setattr(existing_state, intersection_property, new_state_value)
