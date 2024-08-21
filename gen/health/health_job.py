import random
from typing import List, Union

from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.jobs.abstract_job import AbstractJob
from gen_common.jobs.job_args import JobArgs
from gen_common.util.reflection_util import ReflectionUtil

from gen.health.concepts.concept_args import ConceptArgs
from gen.health.concepts.extraction.concept_extraction_pipeline import ConceptExtractionPipeline
from gen.health.concepts.extraction.concept_extraction_state import ConceptExtractionState
from gen.health.concepts.extraction.undefined_concept import UndefinedConcept
from gen.health.contradiction.contradiction_args import ContradictionsArgs
from gen.health.contradiction.contradiction_detector import ContradictionsDetector
from gen.health.contradiction.contradiction_result import ContradictionResult
from gen.health.health_results import HealthResults
from gen.health.health_util import expand_query_selection


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
        dataset: PromptDataset = job_args.dataset
        self.query_ids = expand_query_selection(dataset.artifact_df, query_ids)
        self.concept_layer_id = concept_layer_id
        self.entity_layer_id = entity_layer_id
        self.context_doc_path = context_doc_path
        self.use_llm_for_entity_extraction = use_llm_for_entity_extraction
        self.additional_args = additional_args

    def _run(self) -> HealthResults:
        """
        Runs health checks on the query artifact.
        :return: Results from each health check.
        """
        dataset: PromptDataset = self.job_args.dataset
        contradictions_result = self._run_contradictions_detector()
        undefined_entities = self._run_find_missing_concepts(dataset, query_ids=self.query_ids, concept_layer_id=self.concept_layer_id)
        results = HealthResults(contradictions=contradictions_result,
                                undefined_concepts=undefined_entities)
        return results

    def _run_contradictions_detector(self, **kwargs) -> List[ContradictionResult]:
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

    @staticmethod
    def _run_find_missing_concepts(dataset: PromptDataset, query_ids: List[str], concept_layer_id: str) -> List[UndefinedConcept]:
        """
        Finds any concepts missing in query ids.
        :param dataset: Dataset containing artifacts to extract concepts from.
        :param query_ids: Artifact Ids of artifacts to extract concepts from.
        :param concept_layer_id: Artifact type associated with concepts.
        :return: List of undefined concepts across query ids.
        """
        args = ConceptArgs(
            dataset=dataset,
            query_ids=query_ids,
            concept_layer_id=concept_layer_id
        )
        pipeline = ConceptExtractionPipeline(args)
        pipeline.run()

        final_state: ConceptExtractionState = pipeline.state
        return final_state.undefined_concepts
