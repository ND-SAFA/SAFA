import random
from typing import List, Union

from common_resources.data.keys.structure_keys import TraceKeys, TraceRelationshipType
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.tools.util.reflection_util import ReflectionUtil

from tgen.concepts.types.undefined_concept import UndefinedConcept
from tgen.health.contradictions_args import ContradictionsArgs
from tgen.health.contradictions_detector import ContradictionsDetector
from tgen.health.contradictions_result import ContradictionsResult
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.health_check_jobs.health_check_results import HealthCheckResults
from tgen.jobs.health_check_jobs.util import expand_query_selection


class HealthCheckJob(AbstractJob):
    random.seed(0)

    def __init__(self, job_args: JobArgs, query_ids: Union[List[str], str], concept_layer_id: str,
                 entity_layer_id="Entity", context_doc_path: str = None, use_llm_for_entity_extraction: bool = True,
                 **additional_args):
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
        self.query_ids = expand_query_selection(query_ids)
        self.concept_layer_id = concept_layer_id
        self.entity_layer_id = entity_layer_id
        self.context_doc_path = context_doc_path
        self.use_llm_for_entity_extraction = use_llm_for_entity_extraction
        self.additional_args = additional_args

    def _run(self) -> HealthCheckResults:
        """
        Runs health checks on the query artifact.
        :return: Results from each health check.
        """
        dataset: PromptDataset = self.job_args.dataset
        contradictions_result = self._run_contradictions_detector()
        related_traces = dataset.trace_dataset.trace_df.get_relationships(artifact_ids=self.query_ids,
                                                                          artifact_key=TraceKeys.child_label())
        context_traces = [trace for trace in related_traces if trace[TraceKeys.RELATIONSHIP_TYPE] == TraceRelationshipType.CONTEXT]
        results = HealthCheckResults(context_traces=context_traces,
                                     contradictions=contradictions_result)
        return results

    def _run_contradictions_detector(self, **kwargs) -> List[ContradictionsResult]:
        """
        Runs contradictions detector to identify any conflicting artifacts with the query artifact.
        :return: Any ids of conflicting artifacts and an explanation as to why if some were found.
        """
        pipeline_params = self.job_args.get_args_for_pipeline(ContradictionsArgs)
        additional_params = ReflectionUtil.get_constructor_params(ContradictionsArgs, self.additional_args)
        kwargs.update(additional_params)
        args = ContradictionsArgs(**pipeline_params, **kwargs)
        detector = ContradictionsDetector(args)
        contradictions_result = detector.detect(self.query_ids)
        return contradictions_result

    def _run_find_missing_concepts(self) -> List[UndefinedConcept]:
        """
        Finds any concepts missing in query ids.
        :return: List of undefined concepts across query ids.
        """
        raise NotImplementedError()
