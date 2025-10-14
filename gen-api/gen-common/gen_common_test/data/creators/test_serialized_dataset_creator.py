from gen_common.data.creators.prompt_dataset_creator import PromptDatasetCreator
from gen_common.llm.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from gen_common.llm.prompts.multi_artifact_prompt import MultiArtifactPrompt
from gen_common.llm.prompts.prompt_builder import PromptBuilder
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.testprojects.prompt_test_project import PromptTestProject


class TestSerializedDatasetCreator(BaseTest):

    def test_trace_dataset_creator(self):
        trace_dataset_creator = PromptTestProject.get_trace_dataset_creator()
        dataset_creator = self.get_prompt_dataset_creator(trace_dataset_creator=trace_dataset_creator)
        trace_df = dataset_creator.trace_dataset_creator.create().trace_df
        prompt = BinaryChoiceQuestionPrompt(choices=["yes", "no"], question="Are these two artifacts related?")
        prompt2 = MultiArtifactPrompt(data_type=MultiArtifactPrompt.DataType.TRACES)
        prompt_builder = PromptBuilder(prompts=[prompt, prompt2])
        PromptTestProject.verify_dataset_creator(self, dataset_creator, prompt_builder=prompt_builder, trace_df=trace_df)

    @staticmethod
    def get_prompt_dataset_creator(ensure_code_is_summarized=False, **params):
        return PromptDatasetCreator(**params, ensure_code_is_summarized=ensure_code_is_summarized)
