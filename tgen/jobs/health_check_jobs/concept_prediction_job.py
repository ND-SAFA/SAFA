import random
from typing import List, Union

from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.keys.structure_keys import TraceKeys, TraceRelationshipType
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.tools.util.reflection_util import ReflectionUtil

from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_pipeline import ConceptPipeline
from tgen.concepts.types.concept_pipeline_response import ConceptPipelineResponse
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.health_check_jobs.health_check_results import ConceptPredictionResponse
from tgen.jobs.health_check_jobs.util import expand_query_selection


class ConceptPredictionJob(AbstractJob):
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
        self.query_ids = expand_query_selection(self.job_args.dataset.artifact_df, query_ids)
        self.concept_layer_id = concept_layer_id
        self.additional_args = additional_args

    def _run(self) -> ConceptPredictionResponse:
        """
        Runs health checks on the query artifact.
        :return: Results from each health check.
        """
        dataset: PromptDataset = self.job_args.dataset
        concept_matches = self._run_concept_matching(dataset.artifact_df)
        related_traces = dataset.trace_dataset.trace_df.get_relationships(artifact_ids=self.query_ids,
                                                                          artifact_key=TraceKeys.child_label())
        context_traces = [trace for trace in related_traces if trace[TraceKeys.RELATIONSHIP_TYPE] == TraceRelationshipType.CONTEXT]
        results = ConceptPredictionResponse(context_traces=context_traces,
                                            concept_matches=concept_matches, )
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
