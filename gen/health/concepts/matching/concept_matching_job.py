import random
from typing import List, Union

from gen_common.jobs.abstract_job import AbstractJob
from gen_common.jobs.job_args import JobArgs
from gen_common.util.reflection_util import ReflectionUtil

from gen.health.concepts import ConceptPipeline, ConceptPipelineResponse, CreateResponseStep
from gen.health.concepts.concept_args import ConceptArgs
from gen.health.health_util import expand_query_selection
from gen_test.health.concepts.matching.constants import CONCEPT_TYPE


class ConceptPredictionJob(AbstractJob):
    random.seed(0)

    def __init__(self, job_args: JobArgs, query_ids: Union[List[str], str], concept_layer_id: str = CONCEPT_TYPE, **additional_args):
        """
        Initializes the job to run health checks on the query artifact.
        :param job_args: Contains dataset and other common arguments to jobs in general.
        :param query_ids: The id of the query artifact under inspection.
        :param concept_layer_id: The id of the layer containing concept artifacts.
        :param additional_args: Any additional arguments to the concept or contradictions detectors.
        """
        super().__init__(job_args, require_data=True)
        artifact_df = self.job_args.dataset.trace_dataset.artifact_df
        self.query_ids = expand_query_selection(artifact_df, query_ids)
        self.concept_layer_id = concept_layer_id
        self.additional_args = additional_args

    def _run(self) -> ConceptPipelineResponse:
        """
        Runs health checks on the query artifact.
        :return: Results from each health check.
        """
        pipeline_params = self.job_args.get_args_for_pipeline(ConceptArgs)
        additional_params = ReflectionUtil.get_constructor_params(ConceptArgs, self.additional_args)
        pipeline_params.update(additional_params)

        args = ConceptArgs(
            concept_layer_id=self.concept_layer_id,
            query_ids=self.query_ids,
            **pipeline_params
        )
        pipeline = ConceptPipeline(args)
        pipeline.run()

        state = pipeline.state
        direct_matches, multi_matches = CreateResponseStep.analyze_matches(state.direct_matches)
        response = ConceptPipelineResponse(
            matches=direct_matches,
            multi_matches=multi_matches,
            predicted_matches=state.predicted_matches,
        )
        return response
