from typing import Type

from tgen.common.util.base_object import BaseObject
from tgen.common.util.pipeline_util import PipelineUtil
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.hgen_util import SAVE_DATASET_DIRNAME
from tgen.hgen.steps.step_create_hgen_dataset import CreateHGenDatasetStep
from tgen.hgen.steps.step_generate_artifact_content import GenerateArtifactContentStep
from tgen.hgen.steps.step_generate_inputs import GenerateInputsStep
from tgen.hgen.steps.step_initialize_dataset import InitializeDatasetStep
from tgen.hgen.steps.step_refine_generations import RefineGenerationsStep
from tgen.state.pipeline.abstract_pipeline import AbstractPipeline


class HierarchyGenerator(AbstractPipeline[HGenArgs, HGenState], BaseObject):
    """
    Responsible for generating higher-level artifacts from low-level artifacts
    """
    steps = [InitializeDatasetStep,
             GenerateInputsStep,
             GenerateArtifactContentStep,
             RefineGenerationsStep,
             CreateHGenDatasetStep]

    def __init__(self, args: HGenArgs):
        """
        Initializes the generator with necessary trainer information
        :param args: The arguments required for the hierarchy generation
        """
        super().__init__(args, HierarchyGenerator.steps)
        self.args = args

    def state_class(self) -> Type[HGenState]:
        """
        Gets the class used for the pipeline state.
        :return: the state class
        """
        return HGenState

    def run(self) -> PromptDataset:
        """
        Runs the hierarchy generator to create a new trace dataset containing generated higher-level artifacts
        :return: Path to exported dataset of generated artifacts
        """

        super().run()

        dataset = self.state.final_dataset
        assert dataset is not None, f"Final dataset is not set."
        save_path = PipelineUtil.save_dataset_checkpoint(dataset, self.args.export_dir, filename=SAVE_DATASET_DIRNAME)
        PipelineUtil.save_dataset_checkpoint(dataset, save_path, filename="safa", exporter_class=SafaExporter)
        return dataset
