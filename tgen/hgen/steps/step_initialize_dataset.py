from typing import Any

from tgen.common.constants.project_summary_constants import PS_OVERVIEW_TITLE, PS_ENTITIES_TITLE, PS_SUBSYSTEM_TITLE, \
    PS_DATA_FLOW_TITLE
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.hgen_util import save_dataset_checkpoint
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.summarizer.summarizer import Summarizer
from tgen.summarizer.summarizer_args import SummarizerArgs


class InitializeDatasetStep(AbstractPipelineStep[HGenArgs, HGenState]):
    HGEN_SECTION_TITLE = "Hgen"

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Gets the original source datasets used for the generation
        :param args: The arguments and current state of HGEN.
        :param state: The state of HGEN.
        :return: The original dataset and a dataset with only the source layer
        """
        export_path = state.export_dir
        original_dataset_complete = args.dataset_for_sources
        if not state.summary:
            original_dataset_complete = self._summarize(args)
            state.summary = original_dataset_complete.project_summary
        save_dataset_checkpoint(original_dataset_complete, export_path, filename="initial_dataset_with_sources")

        source_layer_only_dataset = self._create_dataset_with_single_layer(original_dataset_complete.artifact_df,
                                                                           args.source_layer_id)
        state.source_dataset = source_layer_only_dataset
        state.original_dataset = original_dataset_complete

    def _summarize(self, args: HGenArgs) -> PromptDataset:
        """
        Summarizes the project and artifacts
        :param args: The arguments to hgen
        :return: The summarized dataset
        """
        dataset = args.dataset_for_sources
        hgen_section_questionnaire: QuestionnairePrompt = SupportedPrompts.HGEN_SUMMARY_QUESTIONNAIRE.value
        hgen_section_questionnaire.format_value(target_type=args.target_type)
        new_sections = {self.HGEN_SECTION_TITLE: hgen_section_questionnaire}

        code_layers = dataset.artifact_df.get_code_layers()
        summarizer_args = SummarizerArgs(dataset=dataset,
                                         project_summary=args.system_summary,
                                         summarize_code_only=True,
                                         do_resummarize_project=True,
                                         summarize_artifacts=args.create_new_code_summaries
                                                             or not dataset.artifact_df.is_summarized(code_layers),
                                         project_summary_sections=[PS_ENTITIES_TITLE,
                                                                   PS_SUBSYSTEM_TITLE,
                                                                   PS_DATA_FLOW_TITLE,
                                                                   PS_OVERVIEW_TITLE,
                                                                   self.HGEN_SECTION_TITLE],
                                         new_sections=new_sections,
                                         )
        summarized_dataset = Summarizer(summarizer_args).summarize()
        return summarized_dataset

    @staticmethod
    def _create_dataset_with_single_layer(original_artifact_df: ArtifactDataFrame, layer_id: Any) -> PromptDataset:
        """
        Creates a trace dataset for a single layer
        :param original_artifact_df: A dataframe containing artifacts including those for the layer
        :param layer_id: ID of the layer to construct a dataset for
        :return: The trace dataset
        """
        layer_artifact_df = original_artifact_df.get_type(layer_id)
        if len(layer_artifact_df) == 0:
            raise NameError(f"source_layer_id: {layer_id} does not match any artifacts in the dataset")
        return PromptDataset(artifact_df=layer_artifact_df)
