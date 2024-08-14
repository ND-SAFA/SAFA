import mock

from common_resources.tools.constants.symbol_constants import SPACE
from common_resources.tools.util.enum_util import EnumDict
from common_resources.tools.util.prompt_util import PromptUtil
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.dataframes.layer_dataframe import LayerDataFrame
from common_resources.data.dataframes.trace_dataframe import TraceDataFrame
from common_resources.data.keys.structure_keys import TraceKeys, ArtifactKeys, LayerKeys
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from tgen.delta.change_type import ChangeType
from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_state import DeltaState
from tgen.delta.steps.impact_analysis_step import ImpactAnalysisStep
from tgen.delta.steps.individual_diff_summary_step import IndividualDiffSummaryStep
from tgen.delta.steps.overview_change_summary_step import OverviewChangeSummaryStep
from tgen.summarizer.project.project_summarizer import ProjectSummarizer
from tgen.summarizer.summary import Summary
from tgen.testres.base_tests.base_test import BaseTest
from common_resources.mocking.mock_anthropic import mock_anthropic
from common_resources.mocking.test_response_manager import TestAIManager

added_file = "new_file.py"
modified_file = "existing_file.py"
deleted_file = "obsolete_file.py"
DIFFS = EnumDict({
    ChangeType.ADDED: {
        added_file: "+ This is a new file.\n+ It contains some content."
    },
    ChangeType.MODIFIED: {
        modified_file: "- This is the old content.\n+ This is the new content."
    },
    ChangeType.DELETED
    : {
        deleted_file: "- This file is no longer needed.\n - Removing its content."
    }})


def get_delta_args():
    ids = []
    for val in DIFFS.values():
        ids.extend(val.keys())
    content = ["content" for _ in ids]
    layer = ["code" for _ in ids]
    ids.append("p1")
    content.append("context for child")
    layer.append("parent")
    artifact_df = ArtifactDataFrame({ArtifactKeys.ID: ids,
                                     ArtifactKeys.CONTENT: content,
                                     ArtifactKeys.LAYER_ID: layer})
    trace_df = TraceDataFrame({TraceKeys.SOURCE: ["existing_file.py"], TraceKeys.TARGET: ["p1"], TraceKeys.LABEL: [1]})
    layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: ["code"], LayerKeys.TARGET_TYPE: ["parent"]})
    return DeltaArgs(change_type_to_diffs=DIFFS, dataset=PromptDataset(trace_dataset=TraceDataset(artifact_df, trace_df, layer_df)))


class TestProjectSummaryStep(BaseTest):
    DELTA_STATE = DeltaState(project_summary=Summary(overview=EnumDict({"chunks": ["summary of project"],
                                                                        "title": "overview"})))
    DELTA_ARGS = get_delta_args()

    def test_steps(self):
        self.assert_individual_diff_summary_step()
        self.assert_create_diff_artifact_df()
        self.assert_overview_change_summary_step()
        self.assert_impact_analysis_step()

    @mock_anthropic
    def assert_impact_analysis_step(self, anthropic_manager: TestAIManager):
        anthropic_manager.set_responses([PromptUtil.create_xml("potential-impact", "This is the potential impact")])
        ImpactAnalysisStep().run(self.DELTA_ARGS, self.DELTA_STATE)
        for title in [OverviewChangeSummaryStep.OVERVIEW_TITLE,
                      OverviewChangeSummaryStep.USER_LEVEL_SUMMARY_TITLE,
                      OverviewChangeSummaryStep.CHANGE_DETAILS_TITLE,
                      OverviewChangeSummaryStep.IMPACT_TAG_ID]:
            self.assertIn(title, self.DELTA_STATE.final_summary)

    @mock_anthropic
    def assert_overview_change_summary_step(self, anthropic_manager: TestAIManager):
        group1 = [PromptUtil.create_xml("filenames", "new_file.py, existing_file.py"),
                  PromptUtil.create_xml("change", "These files relate to the same new functionality."),
                  PromptUtil.create_xml("type", "New functionality, Bug fixes")]
        group2 = [PromptUtil.create_xml("filenames", deleted_file),
                  PromptUtil.create_xml("change", "This file is the only one related to this change."),
                  PromptUtil.create_xml("type", "Removed functionality")]
        response = [PromptUtil.create_xml("group", SPACE.join(group1)),
                    PromptUtil.create_xml("group", SPACE.join(group2)),
                    PromptUtil.create_xml("low-level-summary", "This is a technical summary."),
                    PromptUtil.create_xml("user-level-summary", "This is a user-focused summary.")
                    ]
        anthropic_manager.set_responses([SPACE.join(response)])
        OverviewChangeSummaryStep().run(self.DELTA_ARGS, self.DELTA_STATE)
        groups = self.DELTA_STATE.change_summary_output['group']
        self.assertSize(2, groups)
        for group in groups:
            for key, val in group.items():
                group[key] = val[0]
        self.assertIn(added_file, groups[0]["filenames"])
        self.assertIn("existing_file.py", groups[0]["filenames"])
        self.assertIn("New functionality", groups[0]["type"])
        self.assertIn("Bug fixes", groups[0]["type"])
        self.assertEqual("These files relate to the same new functionality.", groups[0]["change"])
        self.assertIn(deleted_file, groups[1]["filenames"])
        self.assertIn("Removed functionality", groups[1]["type"])
        self.assertEqual("This file is the only one related to this change.", groups[1]["change"])
        self.assertEqual("This is a technical summary.", self.DELTA_STATE.change_summary_output["low-level-summary"][0])
        self.assertEqual("This is a user-focused summary.", self.DELTA_STATE.change_summary_output["user-level-summary"][0])

        self.assertIsNotNone(self.DELTA_STATE.change_details_section)

    @mock_anthropic
    def assert_individual_diff_summary_step(self, anthropic_manager: TestAIManager):
        modified_response = [PromptUtil.create_xml("dependencies-imports", "no"),
                             PromptUtil.create_xml("modified-func", "Yes, this was modified."),
                             PromptUtil.create_xml("new-func", "no"),
                             PromptUtil.create_xml("bug-fixes", "Yes, there was a bug fix."),
                             PromptUtil.create_xml("summary", "This is a summary of the modified func."),
                             PromptUtil.create_xml("impact", "This modified code had an impact on the system."),
                             ]
        add_response = [PromptUtil.create_xml("new-func", "This was all new."),
                        PromptUtil.create_xml("summary", "This is a summary of the added func."),
                        PromptUtil.create_xml("impact", "This added code had an impact on the system."),
                        ]
        deleted_response = [PromptUtil.create_xml("removed-func", "This was all deleted"),
                            PromptUtil.create_xml("summary", "This is a summary of the deleted func."),
                            PromptUtil.create_xml("impact", "This deleted code had an impact on the system."),
                            ]
        anthropic_manager.set_responses([SPACE.join(modified_response),
                                         SPACE.join(add_response),
                                         SPACE.join(deleted_response)])
        IndividualDiffSummaryStep().run(self.DELTA_ARGS, self.DELTA_STATE)
        modified_summary = self.DELTA_STATE.diff_summaries["existing_file.py"]
        self._assert_modified_file_summary(modified_summary)
        added_summary = self.DELTA_STATE.diff_summaries[added_file]
        self._assert_new_file_summary(added_summary)
        deleted_summary = self.DELTA_STATE.diff_summaries[deleted_file]
        self._assert_deleted_file_summary(deleted_summary)
        for summary in [modified_summary, added_summary, deleted_summary]:
            self.assertIn("summary", summary)
            self.assertIn("impact", summary)

    def assert_create_diff_artifact_df(self):
        df = OverviewChangeSummaryStep._create_diff_artifact_df(self.DELTA_STATE)
        self.assertIn("existing_file.py", df)
        modified_content = df.get_artifact("existing_file.py")[ArtifactKeys.CONTENT].lower()
        self._assert_modified_file_summary(modified_content)

        self.assertIn(added_file, df)
        new_content = df.get_artifact(added_file)[ArtifactKeys.CONTENT].lower()
        self._assert_new_file_summary(new_content)

        self.assertIn(deleted_file, df)
        deleted_content = df.get_artifact(deleted_file)[ArtifactKeys.CONTENT].lower()
        self._assert_deleted_file_summary(deleted_content)

        for content in [modified_content, new_content, deleted_content]:
            self.assertIn("summary", content)
            self.assertNotIn("impact", content)

        df_with_impact = OverviewChangeSummaryStep._create_diff_artifact_df(self.DELTA_STATE, include_impact=True)
        for i, artifact in df_with_impact.itertuples():
            self.assertIn("impact", artifact[ArtifactKeys.CONTENT].lower())

    def _assert_deleted_file_summary(self, deleted_summary):
        self.assertNotIn(ChangeType.NEW_FUNC.value, deleted_summary)
        self.assertIn(ChangeType.REMOVED_FUNC.value, deleted_summary)

    def _assert_new_file_summary(self, added_summary):
        self.assertIn(ChangeType.NEW_FUNC.value, added_summary)
        self.assertNotIn(ChangeType.REMOVED_FUNC.value, added_summary)

    def _assert_modified_file_summary(self, modified_summary):
        self.assertIn(ChangeType.MODIFIED_FUNC.value, modified_summary)
        self.assertIn(ChangeType.BUG_FIXES.value, modified_summary, )
        self.assertNotIn(ChangeType.DEPENDENCIES_IMPORTS.value, modified_summary)
        self.assertNotIn(ChangeType.RENAMED.value, modified_summary)

    def test_get_parent_artifact_content(self):
        content = IndividualDiffSummaryStep._get_parent_artifact_content(child_id="existing_file.py",
                                                                         original_dataset=self.DELTA_ARGS.dataset)
        lines = content.splitlines()
        self.assertSize(2, lines)
        self.assertEqual(lines[1], "context for child")

    def test_match_change_type(self):
        change_type_mappings = {ChangeType.BUG_FIXES.value: {"change": ["file1", "file2"]}}
        change_type = OverviewChangeSummaryStep._match_change_type([ChangeType.BUG_FIXES.value], change_type_mappings)
        self.assertEqual(change_type, ChangeType.BUG_FIXES.value)
        unknown_change_type = OverviewChangeSummaryStep._match_change_type(["unknown"], change_type_mappings)
        self.assertEqual(unknown_change_type, OverviewChangeSummaryStep.UNKNOWN_CHANGE_TYPE_KEY)

    def test_create_artifact_df_from_diff(self):
        modified_filename = modified_file
        modified_df = IndividualDiffSummaryStep._create_artifact_df_from_diff(self.DELTA_ARGS,
                                                                              ids=[modified_filename],
                                                                              filename2diffs=DIFFS[ChangeType.MODIFIED.value])
        self.assertIn(modified_filename, modified_df)
        content = modified_df.get_artifact(modified_filename)[ArtifactKeys.CONTENT]
        self.assertIn(f"{IndividualDiffSummaryStep.CONTEXT_TITLE}\ncontext for child", content)
        self.assertIn(f"{IndividualDiffSummaryStep.ORIGINAL_TITLE}\ncontent", content)
        self.assertIn(f"{IndividualDiffSummaryStep.DIFF_TITLE}\n{DIFFS[ChangeType.MODIFIED.value][modified_filename]}", content)

        added_filename = added_file
        added_df = IndividualDiffSummaryStep._create_artifact_df_from_diff(self.DELTA_ARGS,
                                                                           ids=[added_filename],
                                                                           filename2diffs=DIFFS[ChangeType.ADDED.value],
                                                                           include_original=False)
        self.assertIn(added_filename, added_df)
        content = added_df.get_artifact(added_filename)[ArtifactKeys.CONTENT]
        self.assertNotIn(f"{IndividualDiffSummaryStep.CONTEXT_TITLE}", content)
        self.assertNotIn(f"{IndividualDiffSummaryStep.ORIGINAL_TITLE}", content)
        self.assertIn(f"{IndividualDiffSummaryStep.DIFF_TITLE}\n{DIFFS[ChangeType.ADDED.value][added_filename]}", content)
