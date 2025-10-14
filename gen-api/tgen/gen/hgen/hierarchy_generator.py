from typing import Dict, Type

from gen_common.data.exporters.safa_exporter import SafaExporter
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.infra.base_object import BaseObject
from gen_common.llm.prompts.questionnaire_prompt import QuestionnairePrompt
from gen_common.pipeline.abstract_pipeline import AbstractPipeline
from gen_common.pipeline.util import PipelineUtil
from gen_common.summarize.summarizer_args import SummarizerArgs
from gen_common.util.list_util import ListUtil

from gen.hgen.common.hgen_util import SAVE_DATASET_DIRNAME
from gen.hgen.hgen_args import HGenArgs
from gen.hgen.hgen_prompts import SUMMARY_QUESTIONNAIRE
from gen.hgen.hgen_state import HGenState
from gen.hgen.steps.step_create_clusters import CreateClustersStep
from gen.hgen.steps.step_create_hgen_dataset import CreateHGenDatasetStep
from gen.hgen.steps.step_detect_duplicate_artifacts import DetectDuplicateArtifactsStep
from gen.hgen.steps.step_find_homes_for_orphans import FindHomesForOrphansStep
from gen.hgen.steps.step_generate_artifact_content import GenerateArtifactContentStep
from gen.hgen.steps.step_generate_explanations_for_links import GenerateExplanationsForLinksStep
from gen.hgen.steps.step_generate_inputs import GenerateInputsStep
from gen.hgen.steps.step_generate_trace_links import GenerateTraceLinksStep
from gen.hgen.steps.step_initialize_dataset import InitializeDatasetStep
from gen.hgen.steps.step_name_artifacts import NameArtifactsStep
from gen.hgen.steps.step_refine_generations import RefineGenerationsStep


class HierarchyGenerator(AbstractPipeline[HGenArgs, HGenState], BaseObject):
    """
    Responsible for generating higher-level artifacts from low-level artifacts
    """
    HGEN_SECTION_TITLE = "Hgen"
    PROJECT_SUMMARY_SECTIONS = []
    steps = [InitializeDatasetStep,
             GenerateInputsStep,
             CreateClustersStep,
             GenerateArtifactContentStep,
             RefineGenerationsStep,
             NameArtifactsStep,
             GenerateTraceLinksStep,
             DetectDuplicateArtifactsStep,
             FindHomesForOrphansStep,
             GenerateExplanationsForLinksStep,
             CreateHGenDatasetStep]

    def __init__(self, args: HGenArgs):
        """
        Initializes the generator with necessary trainer information
        :param args: The arguments required for the hierarchy generation
        """
        summarizer_args = SummarizerArgs(
            summarize_code_only=True,
            do_resummarize_artifacts=False,
            project_summary_sections=ListUtil.append_if_exists(
                self.PROJECT_SUMMARY_SECTIONS,
                args.seed_project_summary_section,
                as_new_list=True
            )
        )
        super().__init__(args, HierarchyGenerator.steps, summarizer_args=summarizer_args)
        self.args = args

    def _get_new_project_summary_sections(self, target_type: str) -> Dict:
        """
        Gets the hgen section to create in the project summary
        :param target_type: The target type to create
        :return: Dictionary mapping section title to the prompt to create it
        """
        hgen_section_questionnaire: QuestionnairePrompt = SUMMARY_QUESTIONNAIRE
        hgen_section_questionnaire.format_value(target_type=target_type)
        new_sections = {self.HGEN_SECTION_TITLE: hgen_section_questionnaire}
        return new_sections

    def state_class(self) -> Type[HGenState]:
        """
        Gets the class used for the pipeline state.
        :return: the state class
        """
        return HGenState

    def run(self, **kwargs) -> PromptDataset:
        """
        Runs the hierarchy generator to create a new trace dataset containing generated higher-level artifacts
        :return: Path to exported dataset of generated artifacts
        """
        super().run(**kwargs)
        dataset = self.state.final_dataset
        assert dataset is not None, f"Final dataset is not set."
        save_path = PipelineUtil.save_dataset_checkpoint(dataset, self.args.export_dir, filename=SAVE_DATASET_DIRNAME)
        PipelineUtil.save_dataset_checkpoint(dataset, save_path, filename="safa", exporter_class=SafaExporter)
        return dataset

    def get_input_output_counts(self) -> Dict[str, int]:
        """
        Gets the number of input and generated artifacts
        :return: The number of input and generated artifacts
        """
        return {"N Input Artifact": len(self.state.source_dataset.artifact_df),
                "N Output Artifacts": len(self.state.refined_content)}
