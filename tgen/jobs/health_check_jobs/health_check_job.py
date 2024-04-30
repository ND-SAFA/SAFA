import random
from typing import List

from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_pipeline import ConceptPipeline
from tgen.concepts.types.concept_pipeline_response import ConceptPipelineResponse
from tgen.contradictions.contradictions_args import ContradictionsArgs
from tgen.contradictions.contradictions_detector import ContradictionsDetector
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.health_check_jobs.health_check_results import HealthCheckResults


class HealthCheckJob(AbstractJob):
    RANDOM_SELECTION = "RANDOM"
    random.seed(0)

    def __init__(self, job_args: JobArgs, req_id: str, concept_layer_id: str):
        """
        Initializes the job to run health checks on the requirement.
        :param job_args: Contains dataset and other common arguments to jobs in general.
        """
        super().__init__(job_args, require_data=True)
        self.req_id = req_id if req_id.upper() != self.RANDOM_SELECTION else random.choice(self.job_args.dataset.artifact_df.index)
        self.concept_layer_id = concept_layer_id

    def _run(self) -> HealthCheckResults:
        """
        Runs health checks on the requirement.
        :return: Results from each health check.
        """
        dataset: PromptDataset = self.job_args.dataset
        conflicting_ids = self._run_contradictions_detector()
        concept_matches = self._run_concept_matching(dataset.artifact_df)
        related_traces = dataset.trace_dataset.trace_df.get_relationships(artifact_id=self.req_id,
                                                                          artifact_key=TraceKeys.child_label())
        results = HealthCheckResults(related_traces=related_traces, concept_matches=concept_matches,
                                     conflicting_ids=conflicting_ids)
        return results

    def _run_concept_matching(self, artifact_df: ArtifactDataFrame) -> ConceptPipelineResponse:
        """
        Runs concept pipeline to identify matches in the artifact.
        :param artifact_df: Contains all project artifacts.
        :return: The response from the concept pipeline.
        """
        pipeline_params = self.job_args.get_args_for_pipeline(ConceptArgs)
        requirement = artifact_df.get_artifact(self.req_id)
        args = ConceptArgs(concept_layer_id=self.concept_layer_id, artifact=requirement, **pipeline_params)
        pipeline = ConceptPipeline(args)
        pipeline.run()
        return pipeline.state.response

    def _run_contradictions_detector(self) -> List[str]:
        """
        Runs contradictions detector to identify any conflicting requirements with the artifact.
        :return: Any ids of conflicting requirements.
        """
        pipeline_params = self.job_args.get_args_for_pipeline(ContradictionsArgs)
        args = ContradictionsArgs(**pipeline_params)
        detector = ContradictionsDetector(args)
        conflicting_ids = detector.detect(self.req_id)
        return conflicting_ids
