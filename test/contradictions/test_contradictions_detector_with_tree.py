from test.contradictions.data_test_requirements import REQUIREMENTS, get_artifact_content, get_response_for_req, R2, R3, R1, R4, R5
from tgen.common.objects.artifact import Artifact
from tgen.common.util.prompt_util import PromptUtil
from tgen.contradictions.common_choices import CommonChoices
from tgen.contradictions.with_decision_tree.contradiction_decision_nodes import SupportedContradictionDecisionNodes
from tgen.contradictions.with_decision_tree.contradictions_detector_with_tree import ContradictionsDetectorWithTree
from tgen.contradictions.with_decision_tree.contradictions_tree_builder import ContradictionsTreeBuilder
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys, LayerKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestContradictionsDetectorWithTree(BaseTest):
    LAYER_ID = "requirement"

    @mock_anthropic
    def test_detect_all(self, test_ai_manager: TestAIManager):
        responses = [get_response_for_req(r) for r in REQUIREMENTS]
        responses.extend([self.fake_question_answers for i in range(8)])
        test_ai_manager.set_responses(responses)
        content = [get_artifact_content(r) for r in REQUIREMENTS]
        artifact_df = ArtifactDataFrame({ArtifactKeys.ID: [str(i + 1) for i in range(len(content))],
                                         ArtifactKeys.CONTENT: content,
                                         ArtifactKeys.LAYER_ID: [self.LAYER_ID for _ in range(len(content))]})
        links = [("1", "2"), ("2", "3"), ("1", "4"), ("4", "5")]
        expected_outcomes = [SupportedContradictionDecisionNodes.IDEM_CONTRADICTION,
                             SupportedContradictionDecisionNodes.SIMPLEX_CONTRADICTION,
                             SupportedContradictionDecisionNodes.NONE,
                             SupportedContradictionDecisionNodes.ALIUS_CONTRADICTION,
                             ]
        trace_df = TraceDataFrame({TraceKeys.SOURCE: [link[0] for link in links], TraceKeys.TARGET: [link[1] for link in links]})
        trace_dataset = TraceDataset(artifact_df, trace_df, LayerDataFrame({LayerKeys.SOURCE_TYPE: [self.LAYER_ID],
                                                                            LayerKeys.TARGET_TYPE: [self.LAYER_ID]}))
        detector = ContradictionsDetectorWithTree(trace_dataset)
        results = detector.detect_all()
        for i, link in enumerate(links):
            expected_outcome = expected_outcomes[i]
            trace_id = trace_df.get_link(source_id=link[0], target_id=link[1])[TraceKeys.LINK_ID]
            if expected_outcome != SupportedContradictionDecisionNodes.NONE:
                self.assertIn(trace_id,
                              results[expected_outcome.value.description])
            else:
                self.assertFalse(any([trace_id in contradictions for contradictions in results.values()]))

    @mock_anthropic
    def test_single(self, test_ai_manager: TestAIManager):
        responses = [get_response_for_req(r) for r in [R1, R2]]
        responses.extend([self.fake_question_answers for i in range(2)])
        test_ai_manager.set_responses(responses)
        path = ContradictionsDetectorWithTree.detect_single_pair(
            Artifact(id="1", content=get_artifact_content(R1), layer_id=self.LAYER_ID),
            Artifact(id="2", content=get_artifact_content(R2), layer_id=self.LAYER_ID))
        self.assertEqual(path.get_final_decision(), SupportedContradictionDecisionNodes.IDEM_CONTRADICTION.value.description)

    def fake_question_answers(self, prompt: str):
        q1: LLMNode = ContradictionsTreeBuilder().get_question_node(1).select_branch(CommonChoices.NO)
        q2: LLMNode = ContradictionsTreeBuilder().get_question_node(2).select_branch(CommonChoices.NO)
        q3: LLMNode = ContradictionsTreeBuilder().get_question_node(3)
        q5: LLMNode = ContradictionsTreeBuilder().get_question_node(5).select_branch(CommonChoices.NO)
        q6: LLMNode = ContradictionsTreeBuilder().get_question_node(6)
        if q1.get_formatted_question((R2, R3)) in prompt:
            return PromptUtil.create_xml("answer", CommonChoices.YES)
        elif q2.get_formatted_question((R1, R2)) in prompt:
            return PromptUtil.create_xml("answer", CommonChoices.NO)
        elif q2.get_formatted_question((R2, R3)) in prompt:
            return PromptUtil.create_xml("answer", CommonChoices.NO)
        elif q3.get_formatted_question((R1, R2)) in prompt:
            return PromptUtil.create_xml("answer", CommonChoices.YES)
        elif q3.get_formatted_question((R2, R3)) in prompt:
            return PromptUtil.create_xml("answer", CommonChoices.YES)
        elif q1.get_formatted_question((R1, R4)) in prompt:
            return PromptUtil.create_xml("answer", CommonChoices.NO)
        elif q2.get_formatted_question((R4, R5)) in prompt:
            return PromptUtil.create_xml("answer", CommonChoices.NO)
        elif q3.get_formatted_question((R4, R5)) in prompt:
            return PromptUtil.create_xml("answer", CommonChoices.YES)
        elif q5.get_formatted_question((R4, R5)) in prompt:
            return PromptUtil.create_xml("answer", CommonChoices.NO)
        elif q6.get_formatted_question((R4, R5)) in prompt:
            return PromptUtil.create_xml("answer", CommonChoices.YES)
        else:
            print("hi")
