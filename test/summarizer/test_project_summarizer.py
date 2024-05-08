from tgen.common.constants.project_summary_constants import PS_OVERVIEW_TITLE, PS_DATA_FLOW_TITLE, CUSTOM_TITLE_TAG, PS_NOTES_TAG
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.summarizer.project.project_summarizer import ProjectSummarizer
from tgen.summarizer.project.supported_project_summary_sections import PROJECT_SUMMARY_MAP
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summary import SummarySectionKeys, Summary
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.mock_responses import MockResponses, create, TEST_PROJECT_SUMMARY
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.testres.testprojects.safa_test_project import SafaTestProject


class TestProjectSummarizer(BaseTest):
    PROJECT_SUMMARY_SECTIONS = [PS_DATA_FLOW_TITLE, PS_OVERVIEW_TITLE]
    NEW_TITLE = "new_title"
    NEW_SECTION_TITLE = "NEW_SECTION"
    NEW_SECTIONS = {NEW_SECTION_TITLE: QuestionnairePrompt(question_prompts=[
        QuestionPrompt("Notes", response_manager=PromptResponseManager(response_tag=PS_NOTES_TAG)),
        QuestionPrompt("Title", response_manager=PromptResponseManager(response_tag=CUSTOM_TITLE_TAG)),
        QuestionPrompt("A Prompt", response_manager=PromptResponseManager(response_tag="new")),
    ])}
    SECTION_ORDER = [PS_OVERVIEW_TITLE, NEW_SECTION_TITLE]
    ARGS = SummarizerArgs(project_summary_sections=PROJECT_SUMMARY_SECTIONS,
                          new_sections=NEW_SECTIONS,
                          section_display_order=SECTION_ORDER)
    N_SECTIONS = len(SECTION_ORDER) + 1

    @mock_anthropic
    def test_summarize_with_no_sections(self, ai_manager: TestAIManager):
        ai_manager.mock_summarization()
        args = SummarizerArgs(project_summary_sections=[])
        summarizer = ProjectSummarizer(args, self._get_dataset())
        summary = summarizer.summarize()
        self.assertEqual(len(summary), 0)

    @mock_anthropic
    def test_summarize(self, ai_manager: TestAIManager):
        ai_manager.mock_summarization()
        res = self._project_responses()
        ai_manager.set_responses(res)

        existing_summary = Summary(existing_section=EnumDict({"title": "existing_section", "chunks": ["existing_section"]}))
        summarizer = self.get_project_summarizer(project_summary=existing_summary)
        summary = summarizer.summarize()
        self._assert_summary(summary)
        self.assertEqual(ai_manager.mock_calls, self.N_SECTIONS)

        ai_manager.mock_calls = 0
        summary.pop(PS_DATA_FLOW_TITLE)  # summarize with all sections already summarized except dataflow
        summarizer = self.get_project_summarizer(project_summary=summary)
        summary = summarizer.summarize()
        self._assert_summary(summary)
        self.assertEqual(ai_manager.mock_calls, 1)

    def test_create_prompt_builder(self):
        def prompt_builder_test(summarizer: ProjectSummarizer):
            prompt_builder = summarizer._create_prompt_builder(PS_OVERVIEW_TITLE,
                                                               PROJECT_SUMMARY_MAP.get(PS_OVERVIEW_TITLE).value)
            artifact_df = summarizer.dataset.artifact_df
            prompt = prompt_builder.build(artifacts=[artifact for _, artifact in artifact_df.itertuples()],
                                          model_format_args=AnthropicManager.prompt_args)[PromptKeys.PROMPT]
            for i, artifact in artifact_df.itertuples():
                self.assertIn(artifact[ArtifactKeys.ID], prompt)
            self.assertIn("Write a set of bullet points indicating what is important in the system.", prompt)
            return prompt

        summarizer_no_summary = self.get_project_summarizer()
        prompt = prompt_builder_test(summarizer_no_summary)
        self.assertNotIn("# Current Document", prompt)

        summarizer_with_summary = self.get_project_summarizer(project_summary=TEST_PROJECT_SUMMARY)
        prompt = prompt_builder_test(summarizer_with_summary)
        self.assertIn("# Current Document", prompt)
        self.assertIn(TEST_PROJECT_SUMMARY.to_string(), prompt)

    def _project_responses(self):
        new_section_response = create(self.NEW_SECTION_TITLE, tag="new") + PromptUtil.create_xml(CUSTOM_TITLE_TAG, self.NEW_TITLE)
        res = [MockResponses.project_title_to_response[PS_DATA_FLOW_TITLE],
               new_section_response,
               MockResponses.project_title_to_response[PS_OVERVIEW_TITLE],
               MockResponses.project_title_to_response[PS_DATA_FLOW_TITLE],
               ]
        return res

    def _assert_summary(self, summary):
        self.assertEqual(list(summary.keys()), self.SECTION_ORDER + [PS_DATA_FLOW_TITLE])
        new_title_found = False
        for val in summary.values():
            if val[SummarySectionKeys.TITLE] == self.NEW_TITLE:
                expected_text = "_".join(self.NEW_SECTION_TITLE.lower().split())
                self.assertIn(expected_text, val[SummarySectionKeys.CHUNKS][0])
                new_title_found = True
            else:
                expected_text = "_".join(val[SummarySectionKeys.TITLE].lower().split())
                self.assertIn(expected_text, val[SummarySectionKeys.CHUNKS][0])
        self.assertTrue(new_title_found)

    def test_get_section_prompt_by_id(self):
        summarizer = self.get_project_summarizer()
        new_section_prompt = summarizer.get_section_prompt_by_id(self.NEW_SECTION_TITLE)
        self.assertEqual(self.NEW_SECTIONS[self.NEW_SECTION_TITLE], new_section_prompt)

        existing_section_prompt = summarizer.get_section_prompt_by_id(PS_DATA_FLOW_TITLE)
        self.assertEqual(PROJECT_SUMMARY_MAP[PS_DATA_FLOW_TITLE].value.args.prompt_id, existing_section_prompt.args.prompt_id)

    def test_all_project_sections(self):
        section_order = ProjectSummarizer._get_all_project_sections(self.ARGS)
        self.assertListEqual(section_order, self.PROJECT_SUMMARY_SECTIONS + list(self.NEW_SECTIONS.keys()))

    def test_get_section_order(self):
        section_order = ProjectSummarizer._get_section_display_order(self.SECTION_ORDER,
                                                                     self.PROJECT_SUMMARY_SECTIONS + list(self.NEW_SECTIONS.keys()))
        self.assertListEqual(section_order, self.SECTION_ORDER + [PS_DATA_FLOW_TITLE])

    def _get_dataset(self):
        creator = PromptDatasetCreator(trace_dataset_creator=TraceDatasetCreator(SafaTestProject.get_project_reader()))
        dataset = creator.create()
        return dataset

    def get_project_summarizer(self, project_summary=None):
        dataset = self._get_dataset()
        dataset.project_summary = project_summary

        return ProjectSummarizer(self.ARGS, dataset)
