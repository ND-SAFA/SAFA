import random
from typing import List

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

    def __init__(self, job_args: JobArgs, query_ids: List[str], concept_layer_id: str):
        """
        Initializes the job to run health checks on the query artifact.
        :param job_args: Contains dataset and other common arguments to jobs in general.
        :param query_ids: The id of the query artifact under inspection.
        :param concept_layer_id: The id of the layer containing concept artifacts.
        """
        super().__init__(job_args, require_data=True)
        self.query_ids = self._expand_query_selection(query_ids)
        self.concept_layer_id = concept_layer_id

    def _run(self) -> HealthCheckResults:
        """
        Runs health checks on the query artifact.
        :return: Results from each health check.
        """
        dataset: PromptDataset = self.job_args.dataset
        concept_matches = self._run_concept_matching(dataset.artifact_df)
        contradictions_result = self._run_contradictions_detector()
        related_traces = dataset.trace_dataset.trace_df.get_relationships(artifact_ids=self.query_ids,
                                                                          artifact_key=TraceKeys.child_label())
        context_traces = [trace for trace in related_traces if trace[TraceKeys.RELATIONSHIP_TYPE] == TraceRelationshipType.CONTEXT]
        results = HealthCheckResults(context_traces=context_traces, concept_matches=concept_matches,
                                     contradictions=contradictions_result)
        return results

    def _run_concept_matching(self, artifact_df: ArtifactDataFrame) -> ConceptPipelineResponse:
        """
        Runs concept pipeline to identify matches in the artifact.
        :param artifact_df: Contains all project artifacts.
        :return: The response from the concept pipeline.
        """
        pipeline_params = self.job_args.get_args_for_pipeline(ConceptArgs)
        query_artifact = artifact_df.filter_by_index(self.query_ids).to_artifacts()
        args = ConceptArgs(concept_layer_id=self.concept_layer_id, artifacts=query_artifact, **pipeline_params)
        pipeline = ConceptPipeline(args)
        pipeline.run()
        return pipeline.state.response

    def _run_contradictions_detector(self) -> ContradictionsResult:
        """
        Runs contradictions detector to identify any conflicting artifacts with the query artifact.
        :return: Any ids of conflicting artifacts and an explanation as to why if some were found.
        """
        pipeline_params = self.job_args.get_args_for_pipeline(ContradictionsArgs)
        args = ContradictionsArgs(**pipeline_params)
        detector = ContradictionsDetector(args)
        contradictions_result = detector.detect(self.query_ids)
        return contradictions_result

    def _expand_query_selection(self, query_ids: List[str]) -> List[str]:
        """
        Expands query ids if a selection command is found.
        :param query_ids: List of query ids which may contain selection commands.
        :return: List of artifacts ids in query.
        """
        if len(query_ids) == 1:
            command = query_ids[0].upper()
            if command == self.RANDOM_SELECTION:
                return random.choice(self.job_args.dataset.artifact_df.index)
            if command == self.ALL_SELECTION:
                return list(self.job_args.dataset.artifact_df.index)
        return query_ids
