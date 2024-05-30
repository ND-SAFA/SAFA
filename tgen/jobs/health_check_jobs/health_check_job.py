import random
from typing import List, Union

from tgen.common.constants.deliminator_constants import UNDERSCORE
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_pipeline import ConceptPipeline
from tgen.concepts.types.concept_pipeline_response import ConceptPipelineResponse
from tgen.contradictions.contradictions_args import ContradictionsArgs
from tgen.contradictions.contradictions_detector import ContradictionsDetector
from tgen.contradictions.contradictions_result import ContradictionsResult
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import TraceKeys, TraceRelationshipType
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.health_check_jobs.health_check_results import HealthCheckResults


class HealthCheckJob(AbstractJob):
    RANDOM_SELECTION = "RANDOM"
    ALL_SELECTION = "ALL"
    random.seed(0)

    def __init__(self, job_args: JobArgs, query_ids: Union[List[str], str], concept_layer_id: str, **additional_args):
        """
        Initializes the job to run health checks on the query artifact.
        :param job_args: Contains dataset and other common arguments to jobs in general.
        :param query_ids: The id of the query artifact under inspection.
        :param concept_layer_id: The id of the layer containing concept artifacts.
        :param additional_args: Any additional arguments to the concept or contradictions detectors.
        """
        super().__init__(job_args, require_data=True)
        self.query_ids = self._expand_query_selection(query_ids)
        self.concept_layer_id = concept_layer_id
        self.additional_args = additional_args

    def _run(self) -> HealthCheckResults:
        """
        Runs health checks on the query artifact.
        :return: Results from each health check.
        """
        dataset: PromptDataset = self.job_args.dataset
        contradictions_result = None  # self._run_contradictions_detector()
        concept_matches = self._run_concept_matching(dataset.artifact_df)
        related_traces = dataset.trace_dataset.trace_df.get_relationships(artifact_ids=self.query_ids,
                                                                          artifact_key=TraceKeys.child_label())
        context_traces = [trace for trace in related_traces if trace[TraceKeys.RELATIONSHIP_TYPE] == TraceRelationshipType.CONTEXT]
        results = HealthCheckResults(context_traces=context_traces,
                                     concept_matches=concept_matches,
                                     contradictions=contradictions_result)
        return results

    def _run_concept_matching(self, artifact_df: ArtifactDataFrame) -> ConceptPipelineResponse:
        """
        Runs concept pipeline to identify matches in the artifact.
        :param artifact_df: Contains all project artifacts.
        :return: The response from the concept pipeline.
        """
        pipeline_params = self.job_args.get_args_for_pipeline(ConceptArgs)
        additional_params = ReflectionUtil.get_constructor_params(ConceptArgs, self.additional_args)
        pipeline_params.update(additional_params)
        query_artifacts = artifact_df.filter_by_index(self.query_ids).to_artifacts()
        assert len(query_artifacts) > 0, f"Unknown query ids : {self.query_ids}"

        args = ConceptArgs(concept_layer_id=self.concept_layer_id, artifacts=query_artifacts, **pipeline_params)
        pipeline = ConceptPipeline(args)
        pipeline.run()
        return pipeline.state.response

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

    def _expand_query_selection(self, query_ids: List[str]) -> List[str]:
        """
        Expands query ids if a selection command is found.
        :param query_ids: List of query ids which may contain selection commands.
        :return: List of artifacts ids in query.
        """
        if isinstance(query_ids, list) and len(query_ids) == 1:
            command = query_ids[0]
        elif isinstance(query_ids, str):
            command = query_ids
        else:
            return query_ids

        artifact_ids = list(self.job_args.dataset.artifact_df.index)
        command = command.upper()
        if command == self.ALL_SELECTION:
            return list(artifact_ids)
        if command == self.RANDOM_SELECTION:
            return random.choice(artifact_ids)

        if self.RANDOM_SELECTION in command:
            try:
                k = int(command.split(UNDERSCORE)[-1])
                return random.sample(artifact_ids, k)
            except Exception as e:
                return query_ids
