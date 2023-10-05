import os
from copy import deepcopy
from typing import List, Set, Dict

from tqdm import tqdm

from tgen.common.util.enum_util import EnumDict
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs, PredictionStep
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.hgen_util import HGenUtil
from tgen.hgen.steps.step_generate_artifact_content import GenerateArtifactContentStep
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class RefineGenerationsStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Re-runs hgen to find the optimal artifacts across runs
        :param args: The arguments to Hierarchy Generator
        :param state: The current state for the generator
        :return: None
        """
        if not args.optimize_with_reruns:
            state.all_generated_content = state.generation_predictions
            state.refined_content = state.generation_predictions
            return
        all_generation_predictions = deepcopy(state.generation_predictions)
        refined_content = deepcopy(state.generation_predictions)
        generate_artifact_content_step = GenerateArtifactContentStep()
        for i in tqdm(range(max(state.n_generations, 1), args.n_reruns + 1),
                      desc=f"Re-running generations of {args.target_type}s"):
            generate_artifact_content_step.run(args, state, re_run=True)
            all_generation_predictions.update(state.generation_predictions)
            refined_content = self.perform_refinement(args, state.generation_predictions,
                                                      refined_content,
                                                      state.summary, state.export_dir)
        state.refined_content = refined_content
        state.all_generated_content = all_generation_predictions

    @staticmethod
    def perform_refinement(hgen_args: HGenArgs,
                           new_generated_artifact_content: Dict[str, List[str]],
                           refined_artifact_content: Dict[str, List[str]],
                           summary: str,
                           export_path: str) -> Dict[str, List[str]]:
        """
        Performs the refinement of the original generated artifact content
        :param hgen_args: The arguments for the hierarchy generation
        :param new_generated_artifact_content: The content originally generated
        :param refined_artifact_content: The artifact content that was selected from previous runs
        :param summary: The summary of the system
        :param export_path: The path to export the checkpoint to
        :return: The tag to retrieve the refinements and the refined content
        """
        try:
            logger.info(f"Refining {hgen_args.target_type}s\n")
            questionnaire = SupportedPrompts.HGEN_REFINE_TASKS.value
            prompt_builder = HGenUtil.get_prompt_builder_for_generation(hgen_args,
                                                                        questionnaire,
                                                                        base_prompt=SupportedPrompts.HGEN_REFINEMENT,
                                                                        artifact_type=f"V1 {hgen_args.target_type}",
                                                                        build_method=MultiArtifactPrompt.BuildMethod.NUMBERED)
            prompt_builder.add_prompt(Prompt(f"SUMMARY OF SYSTEM: {summary}"), 1)
            refined_artifacts = MultiArtifactPrompt(prompt_prefix=PromptUtil.as_markdown_header(f"V2 {hgen_args.target_type}"),
                                                    build_method=MultiArtifactPrompt.BuildMethod.NUMBERED,
                                                    include_ids=False, data_type=MultiArtifactPrompt.DataType.ARTIFACT,
                                                    starting_num=len(refined_artifact_content) + 1) \
                .build(artifacts=[EnumDict({ArtifactKeys.CONTENT: content}) for content in new_generated_artifact_content.keys()])
            prompt_builder.add_prompt(Prompt(refined_artifacts), -1)
            artifacts = HGenUtil.create_artifact_df_from_generated_artifacts(hgen_args,
                                                                             artifact_generations=list(
                                                                                 refined_artifact_content.keys()),
                                                                             target_layer_id=hgen_args.target_type,
                                                                             generate_names=False)
            generated_artifacts_tag: str = questionnaire.get_response_tags_for_question(-1)
            selected_artifact_nums = HGenUtil.get_predictions(prompt_builder, hgen_args=hgen_args,
                                                              prediction_step=PredictionStep.REFINEMENT,
                                                              dataset=PromptDataset(artifact_df=artifacts),
                                                              response_prompt_ids=questionnaire.id,
                                                              tags_for_response={generated_artifacts_tag}, return_first=True,
                                                              export_path=os.path.join(export_path, "gen_refinement_response.yaml"))[0]
            selected_artifact_nums = set(selected_artifact_nums)
            selected_artifacts = RefineGenerationsStep._get_selected_artifacts(refined_artifact_content, selected_artifact_nums)
            selected_artifacts.update(RefineGenerationsStep._get_selected_artifacts(new_generated_artifact_content,
                                                                                    selected_artifact_nums,
                                                                                    offset=len(refined_artifact_content)))

        except Exception as e:
            logger.exception("Refining the artifact content failed. Using original content instead.")
            selected_artifacts = refined_artifact_content
        return selected_artifacts

    @staticmethod
    def _get_selected_artifacts(original_artifact_content: Dict[str, List[str]],
                                selected_artifact_nums: Set[int], offset: int = 0) -> Dict[str, List[str]]:
        """
        Retrieves only the content selected in the artifact nums
        :param original_artifact_content: The list of original artifact content
        :param selected_artifact_nums: The list of numbers corresponding to the selected artifacts
        :param offset: The amount to offset the artifact numbers by
        :return: The list of selected artifact content
        """
        return {items[0]: items[1] for i, items in enumerate(original_artifact_content.items())
                if i + 1 + offset in selected_artifact_nums}
