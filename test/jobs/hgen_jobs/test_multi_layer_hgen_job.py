import math
import random
import re
import uuid
from unittest import mock, skip

from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerKeys
from tgen.data.summarizer.summarizer import Summarizer
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.hgen_jobs.generate_artifacts_job import GenerateArtifactsJob
from tgen.jobs.hgen_jobs.multi_layer_hgen_job import MultiLayerHGenJob
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.test_anthropic_responses import mock_openai
from tgen.testres.testprojects.generation_test_project import GenerationTestProject


def get_res(prompt, **kwargs):
    artifacts = [artifact.replace(")", "") for artifact in re.findall(r'\d+\)', prompt)]
    n_groups = random.randint(1, len(artifacts) - 1) if len(artifacts) - 2 > 0 else 1
    n_per_group = math.ceil(len(artifacts) / n_groups)
    random.shuffle(artifacts)
    group_tags = []
    for group_num in range(n_groups):
        group_artifacts = []
        for i in range(n_per_group):
            if i < len(artifacts):
                group_artifacts.append(artifacts.pop(i))
        group_tags.append(f'<group>\n<feature>{uuid.uuid4()}{group_num + 1}</feature>\n ' \
                          f'<artifacts>{",".join(group_artifacts)}</artifacts>\n</group>\n\n')
    return [{"completion": "".join(group_tags)}]


@skip("Skipping hgen tests until can fix for update")
class TestMultiLayerHGenJob(BaseJobTest):
    project = GenerationTestProject()

    @mock_openai
    @mock.patch.object(AnthropicManager, "make_completion_request_impl", side_effect=get_res)
    def test_run_success(self, fake_open_ai_completion_mock: mock.MagicMock, fake_anthropic_completion_mock: mock.MagicMock):
        """
        Tests that job is completed succesfully.
        """
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        dataset: TraceDataset = job_result.body
        layers = ["source_layer", "User_story", "Epic", "Requirement"]
        n_expected_links = 0
        for i, layer in enumerate(layers):
            target_artifacts = dataset.artifact_df.filter_by_row(lambda row: row[ArtifactKeys.LAYER_ID.value] == layer)
            if layer == "source_layer":
                self.assertSize(len(self.project.ARTIFACTS), target_artifacts)
            else:
                self.assertGreater(len(target_artifacts), 0)
                as_target = dataset.layer_df.filter_by_row(lambda row: row[LayerKeys.TARGET_TYPE.value] == layer
                                                                       and row[LayerKeys.SOURCE_TYPE.value] == layers[i - 1])
                source_artifacts = dataset.artifact_df.filter_by_row(lambda row: row[ArtifactKeys.LAYER_ID.value] == layers[i - 1])
                self.assertGreater(len(as_target), 0)
                n_expected_links += len(target_artifacts) * len(source_artifacts)
            if layer != layers[len(layers) - 1]:
                as_source = dataset.layer_df.filter_by_row(lambda row: row[LayerKeys.SOURCE_TYPE.value] == layer
                                                                       and row[LayerKeys.TARGET_TYPE.value] == layers[i + 1])
                self.assertGreater(len(as_source), 0)
        self.assertEqual(n_expected_links, len(dataset.trace_df))

    def _get_job(self):
        starting_hgen_job = GenerateArtifactsJob(self.project.ARTIFACTS, "user_story", hgen_llm_manager=OpenAIManager(),
                                                 hgen_summarizer=Summarizer(OpenAIManager()))
        return MultiLayerHGenJob(starting_hgen_job, ["epic", "requirement"])
