import uuid
from unittest import skip
import os
from unittest.mock import MagicMock

import mock

from test.hgen.hgen_test_utils import get_test_hgen_args
from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.common.util.status import Status
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.hgen.hgen_args import HGenState
from tgen.hgen.hgen_util import get_initials
from tgen.hgen.steps.step_create_dataset import CreateHGenDatasetStep
from tgen.hgen.steps.step_generate_artifact_content import GenerateArtifactContentStep
from tgen.hgen.steps.step_generate_inputs import GenerateInputsStep
from tgen.hgen.steps.step_initialize_dataset import InitializeDatasetStep
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.testprojects.mocking.mock_anthropic import mock_anthropic
from tgen.testres.testprojects.mocking.mock_libraries import mock_libraries
from tgen.testres.testprojects.mocking.test_response_manager import TestAIManager


class TestHierarchyGenerator(BaseTest):
    HGEN_ARGS = get_test_hgen_args()
    HGEN_STATE = HGenState()

    def test_run(self):
        self.assert_initialize_dataset_step()
        self.assert_generate_input_step()
        self.assert_generate_artifact_content_step()
        self.assert_create_dataset_step()

    def assert_initialize_dataset_step(self):
        orig_dataset = self.HGEN_ARGS.dataset_creator_for_sources.create()
        InitializeDatasetStep().run(self.HGEN_ARGS, self.HGEN_STATE)
        self.assertSetEqual(set(self.HGEN_STATE.original_dataset.artifact_df.index), set(orig_dataset.artifact_df.index))
        for id_, artifact in self.HGEN_STATE.source_dataset.artifact_df.itertuples():
            self.assertEqual(artifact[ArtifactKeys.LAYER_ID], "C++ Code")

    @mock_libraries
    def assert_generate_input_step(self, anthropic_ai_manager: TestAIManager, openai_ai_manager: TestAIManager):
        description = "A User story is a concise, informal description of a software feature or functionality, " \
                      "written from the perspective of the end user"
        example = "As a frequent traveler, I want to be able to filter hotel search results by distance " \
                  "so that I can find accommodations close to my desired location."
        format_ = "As a [type of user], I want to [action or goal] so that [reason or benefit]."
        questions = "What are the main classes/functions in the code?\n" \
                    "What are the inputs and outputs of the main functions?\n" \
                    "Is there any user interface code and what does it do?"
        anthropic_ai_manager.set_responses([PromptUtil.create_xml("questions", questions)])
        openai_ai_manager.set_responses([f'{PromptUtil.create_xml("description", description)}'
                                         f'{PromptUtil.create_xml("example", example)} '
                                         f'{PromptUtil.create_xml("format", format_)}'])

        step = GenerateInputsStep()
        step.run(self.HGEN_ARGS, self.HGEN_STATE)
        path = step._get_inputs_save_path(target_type=self.HGEN_ARGS.target_type, source_type=self.HGEN_ARGS.source_type)
        self.assertTrue(os.path.exists(path))
        self.assertEqual(self.HGEN_STATE.description_of_artifact, description)
        self.assertEqual(self.HGEN_STATE.format_of_artifacts, format_)
        self.assertEqual(self.HGEN_STATE.questions, questions.split("\n"))
        step.run(self.HGEN_ARGS, self.HGEN_STATE)
        self.assertEqual(openai_ai_manager.n_used, 1)
        self.assertEqual(anthropic_ai_manager.n_used, 1)
        os.remove(path)

    @mock_anthropic
    def assert_generate_artifact_content_step(self, anthropic_ai_manager: TestAIManager):
        self.HGEN_ARGS.target_type = "User Story"
        summary = "\nHere is a summary of the key technical details and design aspects of the system based on the provided code"
        user_stories = ["As a player, I want to move around in a 3D world so that I can explore the environment.",
                        "As a player, I want to place and remove blocks in the world so that I can modify the environment.",
                        "As a player, I want to copy the color of blocks so that I can reuse colors while building."]
        response = PromptUtil.create_xml("summary", summary)
        for us in user_stories:
            response += PromptUtil.create_xml("user-story", us)
        anthropic_ai_manager.set_responses([response])
        step = GenerateArtifactContentStep()
        step.run(self.HGEN_ARGS, self.HGEN_STATE)
        self.assertEqual(summary, self.HGEN_STATE.summary)
        for i, us in enumerate(user_stories):
            self.assertEqual(us, self.HGEN_STATE.generated_artifact_content[i])

    @mock_anthropic
    @mock.patch.object(RankingJob, "run")
    def assert_create_dataset_step(self, anthropic_ai_manager: TestAIManager, ranking_mock: MagicMock):
        names = [f"{i}" for i, _ in enumerate(self.HGEN_STATE.generated_artifact_content)]
        expected_names = [f"{name} {get_initials(self.HGEN_ARGS.target_type)}" for name in names]
        anthropic_ai_manager.set_responses([PromptUtil.create_xml("title", name) for name in names])
        prediction_entries = [{"source": source, "target": target, "score": 0.8, "label": 1, "explanation": "explanation"}
                              for target in expected_names
                              for source in self.HGEN_STATE.source_dataset.artifact_df.index]
        job_result = JobResult(status=Status.SUCCESS,
                               body=TracePredictionOutput(prediction_entries=prediction_entries),
                               job_id=uuid.uuid4())
        ranking_mock.return_value = job_result
        step = CreateHGenDatasetStep()
        step.run(self.HGEN_ARGS, self.HGEN_STATE)
        for id_, link in self.HGEN_STATE.original_dataset.trace_dataset.trace_df.itertuples():
            found_link = self.HGEN_STATE.dataset.trace_df.get_link(source_id=link[TraceKeys.SOURCE], target_id=link[TraceKeys.TARGET])
            self.assertIsNotNone(found_link)
        for name in expected_names:
            self.assertIn(name, self.HGEN_STATE.dataset.artifact_df.index)
            new_artifact = self.HGEN_STATE.dataset.artifact_df.get_artifact(artifact_id=name)
            self.assertEqual(new_artifact[ArtifactKeys.LAYER_ID], self.HGEN_ARGS.target_type)
            for orig_id, orig_artifact in self.HGEN_STATE.original_dataset.artifact_df.itertuples():
                self.assertIn(orig_id, self.HGEN_STATE.dataset.artifact_df.index)
                if orig_artifact[ArtifactKeys.LAYER_ID] == self.HGEN_ARGS.source_layer_id:
                    q = DataFrameUtil.query_df(self.HGEN_STATE.dataset.trace_df, {"source": orig_id, "target": name})
                    self.assertEqual(len(q), 1)
        for i, layer in self.HGEN_STATE.original_dataset.trace_dataset.layer_df.itertuples():
            q = DataFrameUtil.query_df(self.HGEN_STATE.dataset.layer_df, layer)
            self.assertEqual(len(q), 1)
        q = DataFrameUtil.query_df(self.HGEN_STATE.dataset.layer_df, {LayerKeys.SOURCE_TYPE.value: self.HGEN_ARGS.source_layer_id,
                                                                      LayerKeys.TARGET_TYPE.value: self.HGEN_ARGS.target_type})
        self.assertEqual(len(q), 1)
